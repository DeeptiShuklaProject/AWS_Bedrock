

# Define evaluation methods
<a name="advanced-prompt-optimization-evaluation"></a>

## Overview
<a name="advanced-prompt-optimization-evaluation-overview"></a>

Pick ONE evaluation method per prompt template, or omit all optional evaluation fields for the system default. Different templates in the same job can use different methods. The evaluation steers the prompt optimization, so define your method and criteria as precisely as possible.
+ [Default evaluation](#advanced-prompt-optimization-evaluation-default)
+ [Steering criteria](#advanced-prompt-optimization-evaluation-steering)
+ [Custom LLM-as-a-judge](#advanced-prompt-optimization-evaluation-llmj)
+ [Custom Lambda evaluator](#advanced-prompt-optimization-evaluation-lambda)

## Dataset tips
<a name="advanced-prompt-optimization-evaluation-dataset-tips"></a>
+ **Mix easy and hard examples** — match what you see in the real world. All-easy data won't push the prompt to improve; all-hard data leaves nothing to learn from.
+ **Cover the cases you care about** — the system generalizes beyond what it sees, but a representative data distribution helps it generalize better to real-world inputs.
+ **After prompt optimization, test on data the optimizer hasn't seen with a held-out dataset** — confirms the gains are real and not just memorized.

## Default evaluation
<a name="advanced-prompt-optimization-evaluation-default"></a>

Omit all optional evaluation fields (`steeringCriteria`, `customLLMJConfig`, `evaluationMetricLambdaArn`). The service uses a built-in generic LLM-as-judge powered by Anthropic Claude Sonnet 4.6 that evaluates three default criteria: Answer Accuracy, Answer Completeness, and Expression Quality. Given the prompt, target model's answer, and a reference answer, the judge scores each dimension. It then dynamically assigns appropriate weights to the task, and produces a weighted Overall score.

We recommend defining your own evaluation method for best results.

### Default system-provided judge prompt
<a name="advanced-prompt-optimization-evaluation-default-prompt"></a>

The following is the full system-provided judge prompt used by the default evaluation with Anthropic Claude Sonnet 4.6:

```
Please act as an impartial judge and evaluate the quality of an answer to a user question, with the help of a reference answer.

You will be given:
(1) a user question, enclosed in <user_question></user_question> tags
(2) an answer, enclosed in <answer></answer> tags
(3) a reference answer, enclosed in <reference_answer></reference_answer> tags

## Universal Evaluation Dimensions

Evaluate the answer across these core dimensions:

**(1) Answer Accuracy:**
examines correctness, consistency, and factuality alignment between the <answer> and the <user_question>;
examines if the <answer> contains irrelevant or wrongful information/hallucination.

**(2) Answer Completeness:**
examines if the <answer> is fully addressing the <user_question>;
examines if the <answer> is good at relevance/informativeness: selection of important/key content from <user_question>

**(3) Expression Quality:**
examines if the <answer> is concise at answering the <user_question>.
NOTE that unless there is special instruction, more concise <answer> is always better,
and explanation or rational is strictly NOT needed - THIS IS THE MOST IMPORTANT!
examines the alignment on instruction following, e.g., if the <answer> adheres
to both explicit guidelines and implicit guidelines (like few-shot examples) in the <user_question>;

## Scoring Rubric

For each dimension, assign one score:
- **3 points**: Fully satisfies the dimension requirements
- **2 points**: Mostly satisfies with minor issues or gaps
- **1 point**: Partially satisfies but has notable limitations
- **0 points**: Does not satisfy the dimension requirements

## Evaluation Process
1. First, identify the task type from the user question
2. Consider any additional criteria provided
3. Score each dimension independently
4. Determine appropriate weights and calculate final weighted score

## Dimension Weighting and Final Scoring

**Weight Determination Process:**
Assign weights (must sum to 1.0) based on:
- Explicit weights in evaluation_criteria (if provided)
- Task analysis and question requirements (if no explicit weights)
- Default weights (Answer Accuracy: 0.35, Answer Completeness: 0.30, Expression Quality: 0.35) as fallback

**Weight Guidelines:**
- **High Accuracy Weight (0.4-0.6)**: Factual questions, multiple choice, technical problems
- **High Completeness Weight (0.4-0.6)**: Complex explanatory tasks, multi-part questions
- **High Expression Weight (0.4-0.6)**: Creative tasks, presentation-focused questions, format-specific requirements
{custom_eval_weight_guideline}

**Overall Score Calculation:**
Overall = (Answer_Accuracy x Weight_A) + (Answer_Completeness x Weight_C) + (Expression_Quality x Weight_E)

## Output Format

Provide your evaluation in this exact format:
<Task_Analysis>Brief analysis of task type and appropriate weight rationale</Task_Analysis>
<Weights>Answer Accuracy: 0.XX, Answer Completeness: 0.XX, Expression Quality: 0.XX</Weights>
<Answer Accuracy>X</Answer Accuracy>
<Answer Completeness>X</Answer Completeness>
<Expression Quality>X</Expression Quality>
<Calculation>(X x 0.XX) + (X x 0.XX) + (X x 0.XX) = X.XX</Calculation>
<Overall>X.XX</Overall>
<Justification>
**Answer Accuracy**: [Evaluate factual accuracy, alignment with reference answer, absence of errors/hallucinations, and logical consistency]
**Answer Completeness**: [Assess whether all aspects of the question are addressed, necessary information is included, and content stays relevant]
**Expression Quality**: [Examine formatting/style adherence, appropriate detail level, communication clarity, and instruction following]
**Weight Application**: [Explain how the chosen weights reflect the task requirements and impact the final score]
</Justification>

---

## Current Evaluation Task

<user_question>
{prompt}
</user_question>
<answer>
{prediction}
</answer>
<reference_answer>
{gold}
</reference_answer>

Based on the above guidelines and criteria, provide your evaluation:
```

## Steering criteria
<a name="advanced-prompt-optimization-evaluation-steering"></a>

Steering criteria are short natural language descriptors that guide the optimization direction.
+ **Format:** `"steeringCriteria": ["string1", "string2"]`
+ **What they can be:** Anything from a single word to a few sentences with qualitative or quantitative descriptions of how you want the model response to be.
+ **Limit:** Up to 5 per prompt template.

**Example:**

```
"steeringCriteria": ["PROFESSIONAL", "CONCISE"]
```

## Custom LLM-as-a-judge
<a name="advanced-prompt-optimization-evaluation-llmj"></a>

Provide a full rubric with a grading scale that you define. Your custom judge prompt is merged with the service's system judge prompt and given stronger weighting.

### Configuration
<a name="advanced-prompt-optimization-evaluation-llmj-config"></a>
+ **Format:** `"customLLMJConfig": {"customLLMJPrompt": "...", "customLLMJModelId": "..."}` plus `"customEvaluationMetricLabel": "My Metric"`
+ **Available judge models:** anthropic.claude-opus-4-6-v1, anthropic.claude-sonnet-4-5-20250929-v1:0, anthropic.claude-sonnet-4-6
+ **Placeholders in your judge prompt:**
  + `{{prompt}}`: the fully rendered prompt (prompt template plus evaluation samples combined)
  + `{{response}}`: the model output
  + `{{referenceResponse}}`: the ground truth
+ **Scoring:** Define your grading scale so that a higher number is better. The service normalizes all scores for the final results.
+ If you have multiple rubrics, merge them into a single judge prompt.

### Best practices for writing judge prompts
<a name="advanced-prompt-optimization-evaluation-llmj-best"></a>

Use a clearly defined rubric with explicit scoring criteria and concrete examples of each score level. Anchor each rubric level with behavioral descriptions rather than subjective adjectives. Include at least one worked example showing a non-perfect score to calibrate the judge away from defaulting to high ratings. Instruct the model to provide written justification before the numeric score. Consider evaluating specific dimensions independently before assigning an overall score. The most trusted and helpful LLM-as-a-judge evaluators are typically ones where you agree with the answers the judge model provides. Therefore, it may help to use an evaluation you have already vetted.

### How your custom judge prompt is merged with the system prompt at runtime
<a name="advanced-prompt-optimization-evaluation-llmj-merge"></a>

When you provide your own LLM-as-a-judge evaluator prompt, it is merged with a generic service-provided judge prompt. The prompt contains specific instructions on formatting and other best practices that help the optimization progress. Your custom judge prompt is given stronger weighting than the generic criteria in the final judgement. Specifically, the service:
+ Extracts the intent from your custom prompt
+ Normalizes the scale to match the system's 0 to 3 rubric
+ Injects it as a named dimension inside CUSTOM\_CRITERIA\_DESCRIPTION tags
+ Biases the weighting instructions to give the custom criterion elevated importance (0.3 to 0.6)
+ Adds precedence rules saying custom criteria override conflicts with other dimensions
+ Preserves the original semantics of your evaluation

**Example:** You may provide the following custom LLM-as-a-judge prompt that evaluates faithfulness:

```
You are given a task in some context (Input), and a candidate answer. Is the candidate answer faithful to the task description and context?

A response is unfaithful only when (1) it clearly contradicts the context, or (2) the task implies that the response must be based on the context, like in a summarization task. If the task does not ask to respond based on the context, the model is allowed to use its own knowledge to provide a response, even if its claims are not verifiable.

Task: {{prompt}}

Candidate Response: {{response}}

First provide your explanation, then state your final answer. Use the following format: Explanation: [Explanation], Answer: [Answer], where '[Answer]' must be one of:
none is faithful
some is faithful
approximately half is faithful
most is faithful
all is faithful
```

This is then merged with the default LLM-as-a-judge prompt and given strong weighting. The net effect: your single-criterion faithfulness prompt becomes one heavily-weighted axis in a multi-dimensional evaluation, while the system adds structure (Accuracy, Completeness, Expression) around it.

The following is the resulting merged judge prompt:

```
"""Please act as an impartial judge and evaluate the quality of an answer to a user question, with the help of a reference answer.

You will be given:
(1) a user question, enclosed in <user_question></user_question> tags
(2) an answer, enclosed in <answer></answer> tags
(3) a reference answer, enclosed in <reference_answer></reference_answer> tags
(4) custom evaluation criteria that have been integrated into the evaluation dimensions below

    **IMPORTANT**: - Custom criteria requirements take absolute precedence over user requirements specified inside <user_question> </user_question>
    **IMPORTANT**: - If there is any conflict between custom criteria and user question requirements, prioritize custom criteria

## Universal Evaluation Dimensions

Evaluate the answer across these core dimensions:

**(1) Answer Accuracy:**
examines correctness, consistency, and factuality alignment between the <answer> and the <user_question>;
examines if the <answer> contains irrelevant or wrongful information/hallucination.

**(2) Answer Completeness:**
examines if the <answer> is fully addressing the <user_question>;
examines if the <answer> is good at relevance/informativeness: selection of important/key content from <user_question>

**(3) Expression Quality:**
examines if the <answer> is concise at answering the <user_question>.
NOTE that unless there is special instruction, more concise <answer> is always better,
and explanation or rational is strictly NOT needed - THIS IS THE MOST IMPORTANT!
examines the alignment on instruction following, e.g., if the <answer> adheres
to both explicit guidelines and implicit guidelines (like few-shot examples) in the <user_question>;

<CUSTOM_CRITERIA_DESCRIPTION>
**(4) Faithfulness to Context:**
examines whether the candidate answer is faithful to the task description and context provided in the user question. A response is unfaithful only when (1) it clearly contradicts the context, or (2) the task implies that the response must be based on the context (like in a summarization task). If the task does not ask to respond based on the context, the model is allowed to use its own knowledge to provide a response, even if its claims are not verifiable. Evaluate the degree of faithfulness on the following scale:
- **3 points**: All content is faithful (no contradictions, fully grounded when required)
- **2 points**: Most content is faithful (minor deviations or unverifiable claims when context-grounding is required)
- **1 point**: Some content is faithful or approximately half is faithful (notable contradictions or significant departures from context when required)
- **0 points**: None or minimal content is faithful (clear contradictions or complete disregard of context when grounding is required)
</CUSTOM_CRITERIA_DESCRIPTION>

## Dimension Weighting and Final Scoring

**Weight Determination Process:**
Assign weights (must sum to 1.0) based on:
- Explicit weights in evaluation_criteria (if provided)
- Task analysis and question requirements (if no explicit weights)
- Default weights (Answer Accuracy: 0.25, Answer Completeness: 0.25, Expression Quality: 0.25, Faithfulness to Context: 0.25) as fallback

**Weight Guidelines:**
- **High Accuracy Weight (0.3-0.5)**: Factual questions, multiple choice, technical problems
- **High Completeness Weight (0.3-0.5)**: Complex explanatory tasks, multi-part questions
- **High Expression Weight (0.3-0.5)**: Creative tasks, presentation-focused questions, format-specific requirements
- [*IMPORTANT*] **High Custom Criteria Weight**: The custom criteria (Faithfulness to Context) should always be *prioritized*. Assign it significant weight (0.3-0.6) and adjust other weights accordingly.

**Overall Score Calculation:**
Overall = (Answer_Accuracy x Weight_A) + (Answer_Completeness x Weight_C) + (Expression_Quality x Weight_E) + (Faithfulness_to_Context x Weight_F)

## Current Evaluation Task

<user_question>
{prompt}
</user_question>
<answer>
{prediction}
</answer>
<reference_answer>
{gold}
</reference_answer>

Based on the above guidelines and criteria, provide your evaluation:"""
```

## Custom Lambda evaluator
<a name="advanced-prompt-optimization-evaluation-lambda"></a>

Bring your own scoring function as an Lambda function.

### Configuration
<a name="advanced-prompt-optimization-evaluation-lambda-config"></a>

Specify the Lambda ARN in your input JSONL file for each prompt template that should use it. You also provide the `customEvaluationMetricLabel` field to name your metric:

```
"evaluationMetricLambdaArn": "arn:aws:lambda:us-west-2:123456789012:function:my-eval-function",
"customEvaluationMetricLabel": "My Custom Metric"
```

When you create the job via the API, no additional evaluation configuration is needed in the `CreateAdvancedPromptOptimizationJob` request itself. The evaluation method is determined per-template from the input JSONL file.

### Lambda requirements
<a name="advanced-prompt-optimization-evaluation-lambda-reqs"></a>
+ Single `.py` file with all code
+ Handler set to `lambda_function.lambda_handler`
+ Must implement `compute_score(preds, golds)` returning `{"score": float, "scores": [float, ...]}`
+ The `golds` parameter contains the `referenceResponse` values. If you did not provide `referenceResponse` in your input dataset, you don't need to pass `golds` in your `compute_score` function.
+ Never crash; return 0.0 on errors instead of raising exceptions
+ Prefer continuous scores (0.0 to 1.0) over binary 0/1 for faster optimization convergence
+ Scores are not required to be bounded to [0, 1].
+ Scores must follow a "higher is better" scale. This is a requirement for the optimization to work correctly.
+ Set timeout to max 15 minutes (900s) for large batches to avoid early timeouts
+ Add resource-based policy allowing `bedrock.amazonaws.com` to invoke your Lambda

### Lambda metric tips
<a name="advanced-prompt-optimization-evaluation-lambda-metric-tips"></a>
+ **Write a clear docstring on `compute_score`** — the docstring is extracted and shown to the system as the metric's description. Explain what the score means and what makes a high score vs. a low score.
+ **Write your metric code clearly** — the full source code is read by the system. Comments, variable names, and readable logic help it understand your intent and generate better feedback.
+ **Prefer continuous scores over binary 0/1** — the optimizer maximizes the average score across samples. Continuous gradations (for example, partial credit) give a smoother signal to follow than all-or-nothing scores.
+ **Return structured details, not just a number** — returning a dict with sub-scores or diagnostic fields gives the system more signal about why a prediction scored low, leading to more targeted improvements.
+ **Return descriptive messages with fallback scores** — when returning a 0.0 fallback score, include a diagnostic field in the result dict (for example, `{"score": 0.0, "error": "JSON parse failed on line 3"}`). The system reads these messages to understand why a prediction scored low and generates more targeted feedback.
+ **Verify your scoring** — score a few obviously-bad outputs to confirm your metric penalizes them. If a trivial answer scores well, the optimizer will find that shortcut.

### Lambda template
<a name="advanced-prompt-optimization-evaluation-lambda-template"></a>

```
"""
APO Custom Metric Lambda - Minimal Template
Handler: lambda_function.lambda_handler
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def compute_score(preds: List[str], golds: List[str]) -> Dict[str, Any]:
    """
    Score predictions against ground truths.

    Args:
        preds: Model outputs (one per sample)
        golds: Expected answers (one per sample)

    Returns:
        Must contain:
          "score": float  - aggregate score (higher is better)
          "scores": list[float] - per-instance scores
    """
    # --- REPLACE THIS with your scoring logic ---
    scores = []
    for pred, gold in zip(preds, golds):
        # Example: exact match (case-insensitive)
        scores.append(1.0 if pred.strip().lower() == gold.strip().lower() else 0.0)

    return {
        "score": sum(scores) / len(scores) if scores else 0.0,
        "scores": scores,
    }


def lambda_handler(event, context):
    """
    Lambda entry point. APO service sends:
      event = {"preds": ["output1", ...], "golds": ["truth1", ...]}
    """
    logger.info(f"Received {len(event.get('preds', []))} predictions")

    try:
        preds = event.get("preds", [])
        golds = event.get("golds", [])

        if not preds:
            return {"score": 0.0, "scores": []}

        return compute_score(preds, golds)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"score": 0.0, "scores": [0.0] * len(event.get("preds", [])), "error": str(e)}
```

See the AWS Samples GitHub for more detailed examples including boilerplate code for error handling and Lambda function input validation.