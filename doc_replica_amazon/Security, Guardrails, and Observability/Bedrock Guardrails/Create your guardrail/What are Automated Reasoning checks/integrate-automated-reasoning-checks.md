

# Integrate Automated Reasoning checks in your application
<a name="integrate-automated-reasoning-checks"></a>

After you deploy your Automated Reasoning policy in a guardrail (see [Deploy your Automated Reasoning policy in your application](deploy-automated-reasoning-policy.md)), you can use it at runtime to validate LLM responses and act on the feedback. This page explains how to call the validation API, interpret the findings programmatically, and implement common integration patterns such as rewriting invalid responses and asking clarifying questions.

Automated Reasoning checks operate in *detect mode* only – they return findings and feedback rather than blocking content. Your application is responsible for deciding what to do with the findings: serve the response, rewrite it, ask for clarification, or fall back to a default behavior.

## How Automated Reasoning checks evaluate content
<a name="evaluate-content"></a>

Automated Reasoning checks translate the content that you submit into a logical *implication* – an "if/then" relationship – and then check that implication against your policy rules. The translation produces two kinds of logical statements:
+ **Premises** – The "if" side: the antecedent conditions and scenario facts that set the context for reasoning (for example, a fact the user states about their situation, or a condition the response makes its answer depend on). Premises are optional.
+ **Claims** – The "then" side: the assertions to validate against your policy rules (typically the substantive statements in the model's response).

Automated Reasoning checks decide which statements are premises and which are claims when they translate the content – the split is not taken directly from the input fields. What you control through the API is whether each piece of content enters as *user-side* input (a question or stated condition) or *agent-side* input (a response to validate). The `query` qualifier marks content as user-side; `guardContent` (or untagged text) marks it as agent-side; `groundingSource` is ignored by Automated Reasoning checks. The translation then derives the premises and claims from the combined input.

Whether you have to tag content, and how, depends on the API that you use.


| API | Tagging required? | How content enters Automated Reasoning checks | 
| --- | --- | --- | 
| ApplyGuardrail | No (optional) | All content that you pass is evaluated. Each content block's qualifiers set whether it enters as user-side (query) or agent-side (guard\_content) input; a block with no qualifier defaults to agent-side. ApplyGuardrail does not append a model response on your behalf, so your content must include at least one agent-side (claim) block. | 
| Converse (plain text only) | Yes | Plain text blocks are not tagged, so Automated Reasoning checks have no content to evaluate and are skipped (automatedReasoningPolicyUnits: 0). Use a guardContent block to opt in. | 
| Converse (with guardContent) | Yes | Use qualifiers on guardContent blocks to mark user-side and agent-side content. The model's response is appended as an agent-side (claim) block automatically. | 
| InvokeModel | Yes | Wrap input text in XML tags and set tagSuffix in the request configuration. The model's response is appended as an agent-side (claim) block automatically. | 

### Key differences between APIs
<a name="evaluate-content-differences"></a>
+ On `Converse` and `InvokeModel`, the model's response is appended as an agent-side (claim) block automatically. As a result, an input that you tag only with `query` still runs Automated Reasoning checks – the response supplies the claim.
+ Omitting tags on `InvokeModel`, or sending only plain text on `Converse`, does not produce an error, but Automated Reasoning checks are not applied. The response indicates this with `automatedReasoningPolicyUnits: 0`.
+ On `InvokeModel`, text between guardrail XML tags that carries no qualifier defaults to agent-side (claim) content.
+ Automated Reasoning checks evaluate the response (the agent-side content); they do not run on a standalone `INPUT`-only evaluation.
+ With `ApplyGuardrail`, no model response is appended for you, so the content you submit must include at least one agent-side (claim) block. If it does not, the request returns a `ValidationException`.

## Integration overview
<a name="integration-overview"></a>

At runtime, the integration follows this flow:

```
User question ──► LLM generates response ──► Validate response
                                                      │
                                            ┌─────────┴─────────┐
                                            │                   │
                                          VALID              Not VALID
                                            │                   │
                                            ▼                   ▼
                                      Serve response     Inspect findings
                                      to user                  │
                                                      ┌────────┴────────┐
                                                      │                 │
                                                 OTHER FINDING     TRANSLATION_
                                                    TYPES       AMBIGUOUS / SATISFIABLE
                                                      │                 │
                                                      ▼                 ▼
                                                 Rewrite using    Ask user for
                                                 AR feedback      clarification
                                                      │                 │
                                                      ▼                 ▼
                                                 Validate again   Validate with
                                                                  clarified input
```

Automated Reasoning findings are returned through any API that supports a Amazon Bedrock Guardrails configuration:
+ `ApplyGuardrail` – Standalone validation API. Use this when you want to validate content independently of the LLM invocation. This is the recommended approach for Automated Reasoning checks because it gives you full control over what content is validated and when.
+ `Converse` and `InvokeModel` – LLM invocation APIs with guardrail configuration. Automated Reasoning findings are returned in the `trace` field of the response.

## Call ApplyGuardrail with Automated Reasoning checks
<a name="call-apply-guardrail-ar"></a>

`ApplyGuardrail` evaluates all the content that you pass. Tagging is optional: by default each content block is treated as agent-side (claim) content and validated against your policy rules, which is the simplest integration path. To give Automated Reasoning checks additional context, you can set `qualifiers` on a content block to mark it as user-side (`query`) input. Unlike `Converse` and `InvokeModel`, `ApplyGuardrail` does not append a model response for you, so the content you submit must include at least one claim block; otherwise the request returns a `ValidationException`.

### Request structure
<a name="call-apply-guardrail-ar-request"></a>

`guardrailIdentifier` (required)  
The guardrail ID or ARN. Use the guardrail that has your Automated Reasoning policy attached.

`guardrailVersion` (required)  
The guardrail version number (for example, `1`). Use a numbered version for production workloads, not `DRAFT`.

`source` (required)  
Set to `OUTPUT` when validating LLM responses. Set to `INPUT` when validating user prompts. For Automated Reasoning checks, you typically validate the LLM output.

`content` (required)  
An array of content blocks to validate. Each block contains a `text` field with the content to check. You can pass the user question and the LLM response as separate content blocks, or combine them into a single block.

### Example: Validate an LLM response using the AWS CLI
<a name="call-apply-guardrail-ar-cli-example"></a>

```
aws bedrock-runtime apply-guardrail \
  --guardrail-identifier "{{your-guardrail-id}}" \
  --guardrail-version "{{1}}" \
  --source OUTPUT \
  --content '[
    {
      "text": {
        "text": "User: Am I eligible for parental leave if I have been working here for 2 years full-time?\nAssistant: Yes, you are eligible for parental leave."
      }
    }
  ]'
```

### Example: Validate an LLM response using Python (boto3)
<a name="call-apply-guardrail-ar-python-example"></a>

```
import boto3
import json

bedrock_runtime = boto3.client("bedrock-runtime", region_name="{{us-east-1}}")

response = bedrock_runtime.apply_guardrail(
    guardrailIdentifier="{{your-guardrail-id}}",
    guardrailVersion="{{1}}",
    source="OUTPUT",
    content=[
        {
            "text": {
                "text": (
                    "User: Am I eligible for parental leave if I have been "
                    "working here for 2 years full-time?\n"
                    "Assistant: Yes, you are eligible for parental leave."
                )
            }
        }
    ],
)

# The AR findings are in the assessments
for assessment in response.get("assessments", []):
    ar_assessment = assessment.get("automatedReasoningPolicy", {})
    findings = ar_assessment.get("findings", [])
    for finding in findings:
        # Each finding is a union — exactly one key is present
        # Possible keys: valid, invalid, satisfiable, impossible,
        #                translationAmbiguous, tooComplex, noTranslations
        print(json.dumps(finding, indent=2, default=str))
```

### Response structure
<a name="call-apply-guardrail-ar-response"></a>

The `ApplyGuardrail` response includes an `assessments` array. Each assessment contains an `automatedReasoningPolicy` object with a `findings` array. Each finding is a union type – exactly one of the following keys is present:
+ `valid`
+ `invalid`
+ `satisfiable`
+ `impossible`
+ `translationAmbiguous`
+ `tooComplex`
+ `noTranslations`

For a detailed description of each finding type and its fields, see [Findings and validation results](automated-reasoning-checks-concepts.md#ar-concept-findings).

## Call Converse with Automated Reasoning checks
<a name="call-converse-ar"></a>

Automated Reasoning checks run on a `Converse` request only when the request includes at least one `guardContent` block. A request that sends only plain `text` does not run Automated Reasoning checks.

### Plain text only (Automated Reasoning checks skipped)
<a name="call-converse-ar-default"></a>

If your `Converse` request uses only plain `text` blocks (no `guardContent` blocks), the text is not tagged for guardrail evaluation, so Automated Reasoning checks have nothing to evaluate and are skipped:

```
{
  "messages": [{"role": "user", "content": [{"text": "Apply a 20% discount to my order"}]}]
}
```

This request returns `automatedReasoningPolicyUnits: 0`. Other guardrail policies (content, topic, word, and sensitive information) still evaluate the content; only Automated Reasoning checks are skipped. To run Automated Reasoning checks, use a `guardContent` block as shown in the next section.

**Important**  
When Automated Reasoning checks are skipped, the request still succeeds with no error – so a misconfigured request can silently go unvalidated. Always confirm your configuration by checking that `automatedReasoningPolicyUnits` is greater than `0` in the response. A value of `0` means Automated Reasoning checks did not run (for example, because the content was not tagged), even though the request succeeded.

### Using guardContent blocks
<a name="call-converse-ar-guardcontent"></a>

To run Automated Reasoning checks on `Converse`, wrap the content you want evaluated in a `guardContent` block and set its qualifiers. This is how you mark which content is user-side and which is agent-side.

**Note**  
The `Converse` API uses snake\_case for qualifier strings (`guard_content`, `grounding_source`), while `InvokeModel` XML tags use camelCase (`guardContent`, `groundingSource`). These map to the same underlying roles.

The following table shows how each qualifier marks content for Automated Reasoning checks.


| Qualifier string (snake\_case) | XML tag equivalent (camelCase) | Automated Reasoning input role | 
| --- | --- | --- | 
| "query" | query | User-side – the user's question or stated conditions. Provides context that the translation can draw premises from. | 
| "guard\_content" | guardContent | Agent-side – content to validate against your policy. Supplies the claims the translation checks. | 
| "grounding\_source" | groundingSource | Ignored by Automated Reasoning checks (used by contextual grounding checks). | 

The qualifier sets only whether content is user-side or agent-side; Automated Reasoning checks derive the actual premises and claims when they translate the combined input. A block with no qualifiers specified defaults to `guard_content` (agent-side). You can specify multiple qualifiers on one block. The precedence order is `guard_content > query > grounding_source`.

**Note**  
On `Converse`, the model's response is appended as an agent-side (claim) block automatically, so a request whose blocks use only `query` still runs Automated Reasoning checks. (When you call `ApplyGuardrail` directly, no response is appended, so you must supply at least one agent-side block yourself or the request returns a `ValidationException`.)

### Example: Call Converse with Automated Reasoning qualifiers using the AWS CLI
<a name="call-converse-ar-cli-example"></a>

```
aws bedrock-runtime converse \
  --model-id "{{model-id}}" \
  --guardrail-config '{
    "guardrailIdentifier": "{{your-guardrail-id}}",
    "guardrailVersion": "{{1}}",
    "trace": "enabled"
  }' \
  --messages '[
    {
      "role": "user",
      "content": [
        {
          "guardContent": {
            "text": {
              "text": "Apply a 20% discount to my order and confirm it is done.",
              "qualifiers": ["query"]
            }
          }
        }
      ]
    }
  ]'
```

### When Automated Reasoning checks run
<a name="call-converse-ar-autowrap"></a>

The following table summarizes whether Automated Reasoning checks run for each `Converse` request shape. In every case where they run, the model's response is appended as an agent-side (claim) block.


| Request shape | Automated Reasoning checks run? | 
| --- | --- | 
| Only plain text blocks, no guardContent | No – content is not tagged, so checks are skipped (automatedReasoningPolicyUnits: 0) | 
| Has guardContent blocks with guard\_content or no qualifiers | Yes | 
| Has guardContent blocks with only query | Yes – the appended model response supplies the claim | 
| Has guardContent blocks with only grounding\_source | Yes – the appended model response supplies the claim. The grounding\_source block itself is ignored (it contributes neither a premise nor a claim), but the request still runs because the response provides claim content. | 

## Call InvokeModel with Automated Reasoning checks
<a name="call-invoke-model-ar"></a>

**Warning**  
You must tag your input with XML guardrail tags for Automated Reasoning checks to evaluate responses. Without tags, Automated Reasoning checks return `automatedReasoningPolicyUnits: 0` – no error is raised and no evaluation occurs.

### How it works
<a name="call-invoke-model-ar-how"></a>

`InvokeModel` requires two things for Automated Reasoning checks:

1. A `tagSuffix` in the body's `amazon-bedrock-guardrailConfig` object.

1. Input text wrapped in XML tags that use that suffix.

The XML tag format is as follows:

```
<amazon-bedrock-guardrails-{{QUALIFIER}}_{{SUFFIX}}>text</amazon-bedrock-guardrails-{{QUALIFIER}}_{{SUFFIX}}>
```

Where:
+ {{QUALIFIER}} is one of `query`, `guardContent`, or `groundingSource` (camelCase in XML).
+ {{SUFFIX}} matches the `tagSuffix` value in the request body.
+ `tagSuffix` must match the pattern `^[a-zA-Z0-9][a-zA-Z0-9-_]{0,18}[a-zA-Z0-9]$` (2–20 characters).

### Tag roles for Automated Reasoning checks
<a name="call-invoke-model-ar-tag-roles"></a>


| XML tag qualifier | Automated Reasoning input role | Meaning | 
| --- | --- | --- | 
| query | User-side | The user's question or stated conditions. Provides context that the translation can draw premises from. | 
| guardContent | Agent-side | Content to validate against your policy. Supplies the claims the translation checks. | 
| groundingSource | Ignored | Not used by Automated Reasoning checks (used by contextual grounding checks). | 

The qualifier sets only whether the tagged text is user-side or agent-side input; Automated Reasoning checks derive the premises and claims when they translate the combined input. Tag the user prompt with `query` to give the checks context. The model's output is automatically appended as an agent-side (claim) block, so tagging the prompt with `query` alone is enough for the checks to run.

**Note**  
Text between guardrail tags that carries no qualifier defaults to agent-side (claim) content. Because `InvokeModel` appends the model's response as a claim, a request that tags the prompt only with `query` still runs Automated Reasoning checks. (This differs from a direct `ApplyGuardrail` call, which appends no response and so returns a `ValidationException` if you supply no claim content.)

### Multi-tag precedence and nesting rules
<a name="call-invoke-model-ar-precedence"></a>

A single text segment can be wrapped in multiple nested tag types. When multiple tags apply to the same content, precedence determines the Automated Reasoning role: `guardContent > query > groundingSource`. If content is tagged with both `guardContent` and `query`, it is treated as a claim.

The following nesting rules apply:
+ Tags of different types can be nested (for example, `<amazon-bedrock-guardrails-query_arp><amazon-bedrock-guardrails-guardContent_arp>text</amazon-bedrock-guardrails-guardContent_arp></amazon-bedrock-guardrails-query_arp>`).
+ Tags of the same type cannot self-nest, and tags must be closed in the reverse order that they were opened. An invalid tag structure returns a `ValidationException`.

### Example: Call InvokeModel with Automated Reasoning tags using the AWS CLI
<a name="call-invoke-model-ar-cli-example"></a>

```
aws bedrock-runtime invoke-model \
  --model-id "{{model-id}}" \
  --guardrail-identifier "{{your-guardrail-id}}" \
  --guardrail-version "{{1}}" \
  --trace "ENABLED" \
  --cli-binary-format raw-in-base64-out \
  --body '{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 256,
    "amazon-bedrock-guardrailConfig": {
      "tagSuffix": "arp"
    },
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "<amazon-bedrock-guardrails-query_arp>Apply a 20% discount to my order and confirm it is done.</amazon-bedrock-guardrails-query_arp>"
          }
        ]
      }
    ]
  }' \
  output.json
```

This request returns `automatedReasoningPolicyUnits: 1`, with Automated Reasoning findings in the trace.

### Default behavior (without tags)
<a name="call-invoke-model-ar-default"></a>

The same request without the XML tags uses plain text:

```
"text": "Apply a 20% discount to my order and confirm it is done."
```

This request returns `automatedReasoningPolicyUnits: 0` – Automated Reasoning checks did not run, and no error is raised. The guardrail still evaluates other policies (content, topic, word, and sensitive information), but Automated Reasoning checks are skipped entirely.

## Interpret Automated Reasoning findings at runtime
<a name="interpret-ar-findings-runtime"></a>

To act on Automated Reasoning findings programmatically, your application needs to extract the finding type, the translation details, and the supporting or contradicting rules. The following sections explain how to parse each part of a finding.

### Determine the finding type
<a name="interpret-ar-finding-type"></a>

Each finding is a union – exactly one key is present. Check which key exists to determine the finding type:

```
def get_finding_type(finding):
    """Return the finding type and its data from an AR finding union."""
    for finding_type in [
        "valid", "invalid", "satisfiable", "impossible",
        "translationAmbiguous", "tooComplex", "noTranslations"
    ]:
        if finding_type in finding:
            return finding_type, finding[finding_type]
    return None, None
```

### Read the translation
<a name="interpret-ar-translation"></a>

Most finding types include a `translation` object that shows how Automated Reasoning checks translated the natural language input into formal logic. The translation contains:
+ `premises` – The conditions extracted from the input (for example, `isFullTime = true`, `tenureMonths = 24`).
+ `claims` – The assertions to validate (for example, `eligibleForParentalLeave = true`).
+ `untranslatedPremises` – Parts of the input that could not be mapped to policy variables. These parts are not validated.
+ `untranslatedClaims` – Claims that could not be mapped to policy variables.

Check `untranslatedPremises` and `untranslatedClaims` to understand the scope of the validation. A `VALID` result only covers the translated claims – untranslated content is not verified.

### Read the supporting or contradicting rules
<a name="interpret-ar-rules"></a>

Depending on the finding type, the finding includes rules that explain the result:
+ `valid` findings include `supportingRules` – the policy rules that prove the claims are correct.
+ `invalid` findings include `contradictingRules` – the policy rules that the claims violate.
+ `satisfiable` findings include both a `claimsTrueScenario` and a `claimsFalseScenario` – showing the conditions under which the claims are true and false.

These rules and scenarios are the key inputs for the rewriting pattern described in [Rewrite invalid responses using AR feedback](#rewrite-invalid-responses).

### Determine the aggregate result
<a name="interpret-ar-aggregate"></a>

A single validation request can return multiple findings. To determine the overall result, sort findings by severity and select the worst. The severity order from worst to best is: `translationAmbiguous`, `impossible`, `invalid`, `satisfiable`, `valid`.

```
SEVERITY_ORDER = {
    "tooComplex": 0,
    "translationAmbiguous": 0,
    "impossible": 1,
    "invalid": 2,
    "satisfiable": 3,
    "valid": 4,
    "noTranslations": 5, 
}

def get_aggregate_result(findings):
    """Return the worst finding type from a list of findings."""
    worst = None
    worst_severity = float("inf")
    for finding in findings:
        finding_type, _ = get_finding_type(finding)
        severity = SEVERITY_ORDER.get(finding_type, 0)
        if severity < worst_severity:
            worst_severity = severity
            worst = finding_type
    return worst
```

## Handle validation outcomes in your application
<a name="handle-validation-outcomes"></a>

Use the aggregate result to decide what your application does next. The following table summarizes the recommended action for each result type.


| Result | What it means | Recommended action | 
| --- | --- | --- | 
| valid | The response is mathematically proven correct given the premises and your policy rules. | Serve the response to the user. Log the finding for audit purposes (see [Build an audit trail](#build-audit-trail)). | 
| invalid | The response contradicts your policy rules. The contradictingRules field identifies which rules were violated. | Rewrite the response using the Automated Reasoning feedback (see [Rewrite invalid responses using AR feedback](#rewrite-invalid-responses)). If rewriting fails after multiple attempts, block the response and return a fallback message. | 
| satisfiable | The response is correct under some conditions but not all. It's not wrong, but it's incomplete – it doesn't mention all the requirements. | Rewrite the response to include the missing conditions. Use the claimsFalseScenario to identify what's missing. Alternatively, you can let your LLM ask the user clarifying questions. | 
| impossible | The premises are contradictory, or the policy contains conflicting rules. | Ask the user to clarify their input (see [Ask clarifying questions](#ask-clarifying-questions)). If the issue persists, it may indicate a policy problem – review the quality report. | 
| translationAmbiguous | The input has multiple valid interpretations. The translation models disagreed on how to map the natural language to policy variables. | Ask the user for clarification to resolve the ambiguity. Use the options and differenceScenarios fields to generate targeted clarifying questions. | 
| tooComplex | The input exceeds processing limits for logical analysis. | Simplify the input by breaking it into smaller parts, or return a fallback message explaining that the response could not be verified. | 
| noTranslations | The input is not relevant to your policy's domain. No policy variables could be mapped. | The content is off-topic for this policy. Serve the response without AR validation, or use other guardrail components (such as topic policies) to handle off-topic content. | 

## Rewrite invalid responses using AR feedback
<a name="rewrite-invalid-responses"></a>

The most powerful integration pattern for Automated Reasoning checks is the *rewriting loop*: when a response is `invalid` or `satisfiable`, your application constructs a prompt that includes the original response, the specific findings, and the policy rules, then asks the LLM to rewrite the response to be consistent with the policy. The rewritten response is validated again, and the loop continues until the response is `valid` or a maximum number of iterations is reached.

### Rewriting loop flow
<a name="rewrite-loop-flow"></a>

```
LLM generates initial response
         │
         ▼
Validate with ApplyGuardrail ◄──────────────────┐
         │                                       │
         ▼                                       │
   ┌─────┴─────┐                                 │
   │           │                                 │
 VALID     Not VALID                             │
   │           │                                 │
   ▼           ▼                                 │
 Done    Construct rewriting prompt              │
         with findings + rules                   │
              │                                  │
              ▼                                  │
         LLM rewrites response                   │
              │                                  │
              ▼                                  │
         Max iterations? ──── No ────────────────┘
              │
             Yes
              │
              ▼
         Return best response
         with warning
```

### Construct the rewriting prompt
<a name="rewrite-prompt-template"></a>

The rewriting prompt should include three pieces of information from the AR findings:

1. The original response that failed validation.

1. The specific finding – including the translated premises, claims, and the contradicting or supporting rules.

1. An instruction to rewrite the response so that it is consistent with the policy rules.

**Example rewriting prompt template:**

```
The following response was checked against our policy and found to be
{finding_type}.

Original response:
{original_response}

The validation found the following issue:
- Premises (what was understood from the input): {premises}
- Claims (what was asserted): {claims}
- Contradicting rules: {contradicting_rules}

Please rewrite the response so that it is consistent with the policy document. 
Keep the same helpful tone and answer the user's question
accurately based on the rules. If you cannot provide an accurate answer
without more information, explain what additional information is needed.
```

**Tip**  
Always include the Retrieval Augmented Generation (RAG) content in your rewriting requests or the policy rules so the LLM has all the context it needs when rewriting. The rewriting prompt template provides the specific finding details, while the system prompt provides the broader policy context. This dual-context approach is demonstrated in the [open-source rewriting chatbot sample](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/responsible_ai/automated-reasoning-rewriting-chatbot).

### Rewriting best practices
<a name="rewrite-best-practices"></a>
+ **Set a maximum iteration count.** The rewriting loop should have a hard limit (typically 2–5 iterations) to prevent infinite loops. If the response is still not `valid` after the maximum iterations, return the best response with a warning or fall back to a default message.
+ **Process findings in priority order.** When multiple findings are returned, address the most severe finding first. The severity order is: `translationAmbiguous`, `impossible`, `invalid`, `satisfiable`, `valid`.
+ **Include policy context in the system prompt.** The LLM needs access either to the source document or the full policy rules to rewrite accurately. You can use a [ Knowledge Base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) to include your documents in the generation request or use the `ExportAutomatedReasoningPolicyVersion` API to retrieve the policy definition and format it for the LLM.
+ **Log each iteration.** Record the original response, the findings, the rewriting prompt, and the rewritten response for each iteration. This audit trail is valuable for debugging and compliance (see [Build an audit trail](#build-audit-trail)).

## Ask clarifying questions
<a name="ask-clarifying-questions"></a>

When Automated Reasoning checks return `translationAmbiguous`, `satisfiable`, or `impossible` results, the LLM may not have enough information to rewrite the response accurately. In these cases, your application can ask the user for clarification, then incorporate the answers into the next validation attempt.

### When to ask for clarification
<a name="clarification-when"></a>
+ **`translationAmbiguous`** – The input has multiple valid interpretations. The `options` field shows the competing interpretations, and the `differenceScenarios` field shows how they differ in practice. Use these to generate targeted questions about the specific ambiguity.
+ **`satisfiable`** – The response is correct under some conditions but not all. The `claimsFalseScenario` shows the conditions under which the response would be incorrect. Ask the user about those specific conditions.
+ **`impossible`** – The input contains contradictory statements. Ask the user to clarify the contradiction.
+ **Rewriting fails** – If the LLM cannot rewrite the response to be `valid` after multiple attempts, it may need additional context from the user. Ask the LLM to generate clarifying questions based on the findings.

### Clarification pattern
<a name="clarification-pattern"></a>

The clarification flow works as follows:

1. Extract the ambiguous variables or missing conditions from the AR findings.

1. Generate clarifying questions – either programmatically from the finding fields, or by asking the LLM to formulate questions based on the findings.

1. Present the questions to the user and collect answers.

1. Incorporate the answers into the context and generate a new response.

1. Validate the new response with `ApplyGuardrail`.

**Example: Generate clarifying questions from a `satisfiable` finding**

```
def generate_clarifying_questions(finding_data, user_question):
    """Ask the LLM to generate clarifying questions from a SATISFIABLE finding."""
    claims_true = json.dumps(
        finding_data.get("claimsTrueScenario", {}), indent=2, default=str
    )
    claims_false = json.dumps(
        finding_data.get("claimsFalseScenario", {}), indent=2, default=str
    )

    prompt = (
        f"A user asked: {user_question}\n\n"
        f"The answer is correct when these conditions hold:\n{claims_true}\n\n"
        f"But incorrect when these conditions hold:\n{claims_false}\n\n"
        f"Generate 1-3 short, specific questions to ask the user to determine "
        f"which conditions apply to their situation. Format each question on "
        f"its own line."
    )

    return generate_response(prompt, "You are a helpful assistant.")
```

## Open-source rewriting chatbot sample
<a name="integration-open-source-sample"></a>

For a complete, production-style implementation of the patterns described on this page, see the [Automated Reasoning checks rewriting chatbot](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/responsible_ai/automated-reasoning-rewriting-chatbot) on GitHub. This sample application demonstrates:
+ An iterative rewriting loop where invalid responses are automatically corrected based on Automated Reasoning feedback.
+ Follow-up questions when the LLM needs additional context from the user to rewrite accurately.
+ A timeout mechanism that automatically resumes processing when users don't respond to clarification questions.
+ Policy context injection into LLM prompts so the LLM can reference the full policy rules during rewriting.
+ JSON audit logging of every validation iteration for compliance and debugging.

The sample uses a Python/Flask backend with a React frontend and communicates with Amazon Bedrock for LLM inference and Amazon Bedrock Guardrails for validation through the `ApplyGuardrail` API.

**Note**  
The sample application includes the policy content directly in the LLM generation prompts to support any Automated Reasoning policy without requiring document uploads. In a production deployment, you would typically use RAG content or feed the LLM the original natural language document instead of the Automated Reasoning policy source code.

## Build an audit trail
<a name="build-audit-trail"></a>

Automated Reasoning findings provide mathematically verifiable proof of validity. For regulated industries and compliance scenarios, this proof is a key differentiator – you can demonstrate that an AI response was verified against specific policy rules with specific variable assignments, not just pattern-matched or probabilistically assessed.

To build an effective audit trail, log the following information for each validation request:
+ **Timestamp and request ID.** When the validation occurred and a unique identifier for the request.
+ **Input content.** The user question and LLM response that were validated.
+ **Finding type and details.** The validation result (`valid`, `invalid`, etc.), the translated premises and claims, and the supporting or contradicting rules.
+ **Action taken.** What your application did with the finding – served the response, rewrote it, asked for clarification, or blocked it.
+ **Rewriting history.** If the response was rewritten, log each iteration: the original response, the rewriting prompt, the rewritten response, and the validation result for each iteration.
+ **Policy version.** The guardrail version and policy version used for validation. This ensures you can reproduce the validation result later.

**Example: Audit log entry structure**

```
{
  "timestamp": "2025-07-21T14:30:00Z",
  "request_id": "req-abc123",
  "guardrail_id": "{{your-guardrail-id}}",
  "guardrail_version": "1",
  "user_question": "Am I eligible for parental leave?",
  "llm_response": "Yes, you are eligible for parental leave.",
  "validation_result": "valid",
  "findings": [
    {
      "type": "valid",
      "premises": "isFullTime = true, tenureMonths = 24",
      "claims": "eligibleForParentalLeave = true",
      "supporting_rules": ["A1B2C3D4E5F6"]
    }
  ],
  "action_taken": "served_response",
  "rewrite_iterations": 0
}
```

**Tip**  
Store audit logs in a durable, tamper-evident store such as Amazon CloudWatch Logs or Amazon S3 with object lock enabled. For compliance scenarios, consider using Lake to query audit logs across your organization.