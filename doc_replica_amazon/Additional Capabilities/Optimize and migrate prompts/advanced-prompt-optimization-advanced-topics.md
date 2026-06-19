

# Advanced topics and strategies
<a name="advanced-prompt-optimization-advanced-topics"></a>

## Topics on this page
<a name="advanced-prompt-optimization-advanced-topics-toc"></a>
+ [Multi-objective optimization](#advanced-prompt-optimization-multi-objective)
+ [Optimizing multi-turn and staged prompts](#advanced-prompt-optimization-multi-turn)

## Multi-objective optimization
<a name="advanced-prompt-optimization-multi-objective"></a>

Advanced Prompt Optimization accepts one metric per run — a single scalar score per sample. However, it implicitly supports multi-objective (multi-dimension) optimization: you can bundle multiple objectives into one scalar (a composite metric) and the service optimizes the prompt against that bundle. This section covers the patterns we recommend, when each is appropriate, and the failure modes to watch for.

This applies across verticals — anywhere you care about more than one thing at the same time: accuracy \+ tone, tool-call correctness \+ safety, faithfulness \+ conciseness, latency-friendliness \+ completeness, and more.

### Why one metric is actually multi-objective
<a name="advanced-prompt-optimization-multi-objective-why"></a>

Two facts about the system make this work:
+ **The metric returns a single float value per sample.** The optimization feedback loop reads this scalar as the optimization signal. You can compute it from any number of sub-scores under the hood.
+ **Both metric backends already aggregate sub-scores internally.**
  + The default LLM-as-a-Judge template grades on three dimensions (Answer Accuracy, Answer Completeness, Expression Quality), assigns weights, and emits a single `Overall` score normalized to [0, 1]. Custom criteria are merged into the same scalar. For more information, see [Custom LLM-as-a-judge](advanced-prompt-optimization-evaluation.md#advanced-prompt-optimization-evaluation-llmj).
  + Lambda / custom-code metrics return one number, and you control how it's computed — including any composite of sub-objectives.

So "one metric per run" is a contract about the signal shape, not a limit on what you can optimize for.

### Patterns for bundling multiple objectives into a single metric
<a name="advanced-prompt-optimization-multi-objective-patterns"></a>

Pick one based on how your objectives relate to each other.

#### Pattern 1 — Weighted sum (most common)
<a name="advanced-prompt-optimization-multi-objective-weighted-sum"></a>

`final = w₁·s₁ + w₂·s₂ + ... + wₖ·sₖ`, with weights summing to 1.

**When to use:** Objectives are roughly independent and you can rank them. Trade-offs are acceptable — improving one at the expense of another is OK as long as the sum goes up.

**Choosing weights:**
+ Weight by importance to the user, not by frequency in the dataset.
+ Start coarse: `0.5 / 0.3 / 0.2` is fine. Don't over-tune weights — that's a separate optimization problem.

**Example (agentic / tool-use):**

```
final = 0.5 * tool_correctness + 0.3 * answer_correctness + 0.2 * format_compliance
```

#### Pattern 2 — Hard-fail gates (safety-critical)
<a name="advanced-prompt-optimization-multi-objective-hard-fail"></a>

Define one or more gating objectives. If any gate fails, the score is 0 (or some floor) regardless of the rest. Otherwise, score is the weighted sum of remaining objectives.

```
if not safety_check_passed:
    return 0.0
if wrong_tool_called_for_destructive_action:
    return 0.0
return 0.6 * accuracy + 0.4 * tone
```

**When to use:** At least one objective is non-negotiable (PII leak, wrong account modified, refusal-on-prohibited-content). Use this whenever a "good on average" prompt is unacceptable if it fails the safety bar even occasionally.

**Why this beats just-weighting:** With weights alone, the optimizer can trade safety against quality and still hill-climb the score. A gate makes the trade-off impossible by construction.

#### Pattern 3 — Constraint \+ reward (Pareto-style)
<a name="advanced-prompt-optimization-multi-objective-constraint"></a>

Pick the most important objective as the reward. Express the rest as constraints that, when violated, subtract from the reward (rather than zeroing it out).

```
reward = task_accuracy
penalty = 0.0
if response_too_long:
    penalty += 0.1
if missed_required_disclosure:
    penalty += 0.2
return max(0.0, reward - penalty)
```

**When to use:** You want one primary objective to lead, but soft secondary objectives should still shape the prompt. Less brittle than hard gates, less ambiguous than weighted sums.

#### Pattern 4 — Lambda outer, LLM-as-a-Judge inner (recommended for fuzzy \+ structural mixes)
<a name="advanced-prompt-optimization-multi-objective-lambda-llmj"></a>

A Lambda metric computes deterministic sub-scores (regex, JSON parse, schema validation) and calls an LLM-as-a-Judge sub-evaluation for the fuzzy parts (tone, faithfulness, helpfulness) inside the Lambda function. It then aggregates them into one scalar.

```
def compute_score(prompt, prediction, gold, ...):
    structural = grade_format_and_tools(prediction)        # 0..1 from regex
    semantic   = call_llm_judge(prediction, gold, criteria) # 0..1 from LLMJ
    if structural < 1.0 and is_safety_critical(prompt):
        return 0.0
    return 0.6 * semantic + 0.4 * structural
```

**When to use:** Your objectives mix "easy to test in code" (formats, tool names, length, presence of citations) with "needs a model to judge" (tone, faithfulness, helpfulness). This is often cleaner than asking one LLM-as-a-Judge prompt to produce a single composite score, because the deterministic parts won't drift run-to-run.

#### Pattern 5 — Multi-dimension LLM-as-a-Judge (no Lambda)
<a name="advanced-prompt-optimization-multi-objective-multi-dim-llmj"></a>

Use the built-in LLM-as-a-Judge flow, optionally with a `customLLMJConfig.customLLMJPrompt` that defines your own dimensions and weighting. The judge emits per-dimension scores and an `Overall`; the system parses `Overall` (or averages dimensions if `Overall` is missing) into a [0, 1] scalar.

**When to use:** All your objectives are semantic / fuzzy and you don't have deterministic sub-checks. Fastest to author. Watch for judge variance — re-run the same dataset twice and look at score stability before trusting it as the optimization signal.

### Choosing a pattern
<a name="advanced-prompt-optimization-multi-objective-decision"></a>


| \# | You have... | Use | 
| --- | --- | --- | 
| 1 | 2–4 fuzzy objectives, all semantic | Pattern 5 (multi-dimension LLM-as-a-Judge) | 
| 2 | 2–4 objectives mixing structural and semantic | Pattern 4 (Lambda outer \+ LLM-as-a-Judge inner) | 
| 3 | At least one non-negotiable safety/correctness criterion | Pattern 2 (hard-fail gate) — combine with 1 or 4 | 
| 4 | One clear primary objective \+ soft preferences | Pattern 3 (constraint \+ reward) | 
| 5 | Several roughly-equal independent objectives | Pattern 1 (weighted sum) | 

You can combine patterns. A typical production metric is "weighted sum \+ a hard-fail gate on safety."

### Failure modes to watch for
<a name="advanced-prompt-optimization-multi-objective-failures"></a>
+ **Reward hacking on surface form.** If your sub-score is "did the response contain the word 'sure'," the optimizer will write prompts that force "sure" into every output. Prefer outcome-grounded sub-scores (tool name, slot value, structural validity) over keyword presence.
+ **Judge drift.** A multi-dimension LLM-as-a-Judge metric whose weights vary per call (because the judge is asked to choose them) gives a noisy optimization signal. Pin the weights in your custom criteria, or move dimension weighting into Lambda code.
+ **Composite score saturates.** If the metric hits 0.95 fast and stays there, your sub-scores are too lenient. Tighten rubrics; consider raising the maximum bar (for example, partial credit becomes 0 instead of 1) so the optimizer has headroom.
+ **Sub-objectives conflict directly.** "Conciseness" vs. "completeness" is a real trade-off. The weighted-sum pattern picks an operating point on that frontier; if you don't like it, change the weights.

### Pre-launch checklist
<a name="advanced-prompt-optimization-multi-objective-prelaunch"></a>
+ Compute the metric on the initial prompt over the full dataset and inspect per-dimension averages, not just the scalar. If one dimension is already saturated, consider dropping it from the bundle.
+ Spot-check 5 samples by hand. Does the metric's verdict match your judgment? If not, fix the metric before optimizing the prompt.

## Optimizing multi-turn and staged prompts
<a name="advanced-prompt-optimization-multi-turn"></a>

Advanced Prompt Optimization optimizes a single prompt template against per-sample evaluations. It is not natively turn-aware — it cannot iterate over a dialog or optimize behavior at a specific turn natively. A *staged prompt* is a prompt template where a multi-turn conversation or workflow reuses the same prompt across turns, and the prompt itself contains instructions for each stage, step, or phase of the workflow. To optimize these prompts, flatten the dialog state into the template's input variables, bake the system instructions you want refined into the `promptTemplate`, and probe the turns you actually care about with per-sample reference responses.

This pattern is vertical-agnostic. It applies anywhere a model is invoked repeatedly with growing context — customer-service flows, agentic tool-use loops, multi-step reasoning, tutoring, code-assistant turns, document-grounded QA, triage workflows, and more.

### What Advanced Prompt Optimization actually optimizes
<a name="advanced-prompt-optimization-multi-turn-mental-model"></a>
+ **Input:** A `promptTemplate` string with `{{placeholder}}` variables.
+ **Per sample:** Each `evaluationSamples[i]` provides values for those variables and a `referenceResponse`. The optimizer runs inference, evaluate, feedback, and rewrite independently per sample, then aggregates the metric across samples.
+ **Output:** A refined `promptTemplate`. The variables, the dataset, and the metric are fixed inputs; only the template changes.

Anything you want optimized must live inside the `promptTemplate` itself. Things that vary per sample (the conversation history, the current user query, retrieved context) are `{{variables}}`. The system instructions you want refined are part of the template — never an input variable, or the service has nothing to rewrite.

If you want the service to improve behavior at turn N, express turn N as the rendered prompt-plus-input-variables for one sample, with `referenceResponse` being the desired turn-N model output.

### Pattern A — Stage-at-a-time (recommended starter)
<a name="advanced-prompt-optimization-multi-turn-pattern-a"></a>

Optimize one phase of the dialog at a time. Each evaluation sample represents a single decision point inside that phase.

A "stage" here is whatever you can describe with a coherent set of success criteria. Examples by vertical:
+ **Agentic / tool-use:** plan-formation turn, tool-selection turn, tool-result-interpretation turn, final-answer turn.
+ **Customer support:** intake, verification, action, confirmation, closeout.
+ **Tutoring / education:** assess-knowledge, explain-concept, check-understanding, summarize.
+ **Document QA:** retrieval-grounded answer, follow-up clarification, citation turn.
+ **Coding assistant:** spec-clarification, code generation, code-review/fix, test-write.

#### When to use Pattern A
<a name="advanced-prompt-optimization-multi-turn-pattern-a-when"></a>
+ You can name distinct phases with distinct success criteria.
+ One phase is dragging quality down and you want to fix it without disturbing others.
+ You want fast iteration and a tight, debuggable feedback signal.

#### Template shape
<a name="advanced-prompt-optimization-multi-turn-pattern-a-template"></a>

The stage-specific system instructions are baked into the template (this is what the service rewrites). Only the conversation history and current turn are variables. The structure below is illustrative, not prescribed. Use whatever delimiters or layout your model handles best. The only requirements are: (a) the system instructions you want optimized live inside the template, and (b) the per-sample variables are referenced as `{{variablename}}`.

```
You are an assistant in the {STAGE_NAME} phase of a multi-turn task.
- ...the policy / goals / format / tool-use rules for this phase...
- ...constraints the model must satisfy at this point in the conversation...

Conversation so far:
{{conversation_so_far}}

User's current message:
{{user_query}}
```

#### Sample shape
<a name="advanced-prompt-optimization-multi-turn-pattern-a-sample"></a>

```
{
    "inputVariables": [
        {"conversation_so_far": "user: ...\nassistant: ...\n... (turns 1..N-1)"},
        {"user_query": "...the user input that triggers this stage..."}
    ],
    "referenceResponse": "...the assistant output that satisfies the stage's success criteria..."
}
```

#### Pros and cons
<a name="advanced-prompt-optimization-multi-turn-pattern-a-tradeoffs"></a>

**Pros:** Tight feedback signal, smaller prompts, faster optimization runs, easier to author a focused metric.

**Cons:** Doesn't catch cross-stage drift; you'll run the service once per stage and may need a final integration test.

### Pattern B — Full flattened conversation (advanced)
<a name="advanced-prompt-optimization-multi-turn-pattern-b"></a>

Optimize one large monolithic prompt that owns the entire multi-stage policy. Each sample is the full dialog up to a probe turn.

#### When to use Pattern B
<a name="advanced-prompt-optimization-multi-turn-pattern-b-when"></a>
+ Your production prompt is already monolithic and you don't want to split it.
+ You want the optimizer to see how earlier turns set up later turns, so its rewrites preserve cross-stage flow.
+ Correctness at the probe turn depends on context built up across stages (for example, "by turn N, the right facts must already be referenced" or "the right tool must already have been called").

#### Template shape
<a name="advanced-prompt-optimization-multi-turn-pattern-b-template"></a>

The full monolithic, multi-phase system prompt sits literally inside the template. The service rewrites this body during optimization. The history and current turn remain variables. Choose any layout your model handles well; the requirements are only that the instructions to be optimized are part of the template and per-sample data is referenced via `{{name}}`.

```
You are an assistant for {TASK}. The conversation may proceed through phases:
1. {PHASE_1} — ...
2. {PHASE_2} — ...
3. {PHASE_3} — ...
(...the entire multi-phase policy, tool-use rules, tone, formatting, refusal rules...)

Conversation so far (turns 1..N-1, with role tags):
{{conversation_so_far}}

User's current message:
{{user_query}}
```

#### Sample shape (probe at any turn N)
<a name="advanced-prompt-optimization-multi-turn-pattern-b-sample"></a>

```
{
    "inputVariables": [
        {"conversation_so_far": "user: ...\nassistant: ...\n[tool_call: X(...)]\n... (turns 1..N-1)"},
        {"user_query": "...the user input at turn N..."}
    ],
    "referenceResponse": "...desired assistant output at turn N..."
}
```

#### Why Pattern B can work better than Pattern A
<a name="advanced-prompt-optimization-multi-turn-pattern-b-advantages"></a>
+ The optimizer sees stage progression in `conversation_so_far`, so optimization feedback can reason across stages all at once.
+ A single optimized prompt deploys without stitching multiple optimized stage-prompts together, reducing post-processing for you.

#### Caveats for Pattern B
<a name="advanced-prompt-optimization-multi-turn-pattern-b-caveats"></a>
+ **Stochasticity in earlier turns.** Production assistant turns may not always match the canned `conversation_so_far` exactly. Treat the canned history as the expected trajectory; in production, drift in earlier turns can invalidate the optimization. Use representative, real conversation captures rather than synthesized happy-paths.
+ **Token cost.** Long histories balloon per-trial inference cost. The service runs many candidates × samples × iterations. Budget accordingly, and consider truncating to the most recent K turns plus a summary if cost is the bottleneck.
+ **Reference response bias.** `referenceResponse` should be what a correct assistant would say given that history. If your reference response is too narrow (only one acceptable phrasing), the optimizer will overfit to it. Prefer a metric that grades outcomes (tool name, slot values, decision) over surface-form match where possible.

### Tool-call verification at a specific turn
<a name="advanced-prompt-optimization-multi-turn-tool-call"></a>

The service sees the assistant's text output. To grade "did the model call tool X with the right args at turn N," choose one:
+ **Convention in output:** Have the assistant emit a structured token like `<tool>X(arg=...)</tool>` and grade with regex/JSON parse in a Lambda metric. Cheapest, most reliable.
+ **LLM-as-a-Judge custom criteria:** Provide a `customLLMJPrompt` that asks the judge: "Does the response (a) name the tool `X`, (b) include argument `arg`, (c) match required wording `Y`?" Each sub-check is \+1; aggregate. Easy to author, more variance.
+ **Lambda metric with downstream simulation:** If you have a tool-execution harness, run the model output through it and score on observed side effects. Highest fidelity, most setup.

For composite criteria across many turns or many sub-checks (tool correctness and tone and completeness), see the [Multi-objective optimization](#advanced-prompt-optimization-multi-objective) section.

### Recommended path
<a name="advanced-prompt-optimization-multi-turn-recommended"></a>
+ **Start with Pattern A** on the stage that's hurting quality most. Get a working metric, a 20–50 sample dataset, and one optimization run end-to-end. This validates your dataset and metric before you invest in the larger Pattern B run.
+ **Then run Pattern B once** with the full monolithic prompt and a multi-objective composite metric to catch cross-stage regressions Pattern A can miss.
+ **Iterate dataset before iterating prompt.** If the service's rewrites hill-climb your metric but production behavior doesn't improve, the metric or dataset can often be the problem.

### When not to use Advanced Prompt Optimization for multi-turn
<a name="advanced-prompt-optimization-multi-turn-caveats"></a>
+ **Dialog policy / state-machine bugs** (wrong stage transition logic): a flat prompt rewrite cannot fix this. Fix the orchestration layer first.
+ **Tool schemas wrong:** The service won't change tool definitions. It can only change the prompt that asks the model to use them.
+ **Drift between canned history and live history:** If real conversations diverge wildly from your evaluation samples after a few turns, Pattern B's optimization signal is weak. Capturing real acceptable production traces for optimization runs can help here in addition to the ideal state.
+ **Required behavior depends on private state** the optimizer never sees (for example, user-account data the model only learns via tool calls): make that state explicit in `conversation_so_far` for the probe sample, or accept that the service can only tune the surface behavior.

### Starter checklist
<a name="advanced-prompt-optimization-multi-turn-checklist"></a>
+ Pick the probe turns you care about. Each becomes one or more samples.
+ Decide Pattern A or B (or both — A first, then B).
+ Build 20\+ representative samples with realistic `conversation_so_far` and clean `referenceResponse` values.