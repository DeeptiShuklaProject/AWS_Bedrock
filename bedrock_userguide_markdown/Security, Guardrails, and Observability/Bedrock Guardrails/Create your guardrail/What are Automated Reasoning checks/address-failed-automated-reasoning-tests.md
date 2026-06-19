

# Troubleshoot and refine your Automated Reasoning policy
<a name="address-failed-automated-reasoning-tests"></a>

When an Automated Reasoning policy test fails — the actual result doesn't match the expected result — the issue is either in the translation (natural language was mapped to the wrong variables or values) or in the rules (the policy logic doesn't match your domain). This page provides a systematic approach to diagnosing and fixing both types of issues.

Before you start troubleshooting, make sure you understand the two-step validation process (translate, then validate) described in [Translation: from natural language to formal logic](automated-reasoning-checks-concepts.md#ar-concept-translation). This distinction is the key to efficient debugging.

**Note**  
**Tutorial video:** For a step-by-step walkthrough of refining and troubleshooting an Automated Reasoning policy, watch the following tutorial:  
[Tutorial Demo 3 - Refining the Automated Reasoning policy](https://youtu.be/YmohVGWr_PA)

## Debugging workflow
<a name="debugging-workflow"></a>

When a test fails, use the actual result to identify the type of issue and jump to the relevant section.


| Actual result | Likely cause | Where to look | 
| --- | --- | --- | 
| TRANSLATION\_AMBIGUOUS | The translation models disagreed on how to interpret the input. Usually caused by overlapping variables, vague descriptions, or ambiguous input text. | [Fix translation issues](#fix-translation-issues) | 
| NO\_TRANSLATIONS | The input couldn't be mapped to any policy variables. Either the input is off-topic or the policy is missing variables for the concepts mentioned. | [Fix translation issues](#fix-translation-issues) | 
| TOO\_COMPLEX | The input or policy exceeds processing limits. Often caused by non-linear arithmetic or policies with too many interacting rules. | [Limitations and considerations](guardrails-automated-reasoning-checks.md#automated-reasoning-limitations) | 
| IMPOSSIBLE | The premises contradict each other, or the policy itself contains conflicting rules. | [Fix impossible results](#fix-impossible-results) | 
| VALID, INVALID, or SATISFIABLE (but not what you expected) | Check the translation in the finding first. If the right variables are assigned with the right values, the issue is in your rules. If the translation is wrong, the issue is in your variable descriptions. | Translation wrong: [Fix translation issues](#fix-translation-issues). Rules wrong: [Fix rule issues](#fix-rule-issues). | 

**Tip**  
Always check the translation first. In most cases, the mathematical validation (step 2) is correct — the issue is in how the natural language was translated to formal logic (step 1). Fixing variable descriptions is faster and less risky than changing rules.

## Fix translation issues
<a name="fix-translation-issues"></a>

Translation issues occur when Automated Reasoning checks can't reliably map natural language to your policy's variables. The most visible symptom is a `TRANSLATION_AMBIGUOUS` result, but translation issues can also cause incorrect `VALID`, `INVALID`, or `SATISFIABLE` results when the wrong variables or values are assigned.

### Diagnose TRANSLATION\_AMBIGUOUS results
<a name="fix-translation-ambiguous"></a>

A `TRANSLATION_AMBIGUOUS` finding includes two key fields that help you understand the disagreement:
+ `options` — The competing logical interpretations (up to 2). Each option contains its own translation with premises, claims, and confidence. Compare the options to see where the translation models disagreed.
+ `differenceScenarios` — Scenarios (up to 2) that illustrate how the different interpretations differ in meaning, with variable assignments highlighting the practical impact of the ambiguity.

Examine these fields to identify the specific source of ambiguity, then apply the appropriate fix from the following list.

### Overlapping variable definitions
<a name="fix-overlapping-variables"></a>

When multiple variables could reasonably represent the same concept, the translation models disagree on which one to use.

**Symptom:** The `options` in the `TRANSLATION_AMBIGUOUS` finding show the same concept assigned to different variables. For example, one option assigns "2 years of service" to `tenureMonths = 24` while the other assigns it to `monthsOfService = 24`.

**Fix:** Merge the overlapping variables into a single variable with a comprehensive description. Update all rules that reference the deleted variable to use the remaining one.

**Example:**


| Before (overlapping) | After (merged) | 
| --- | --- | 
| `tenureMonths`: "How long the employee has worked in months."<br />`monthsOfService`: "The employee's months of service." | `tenureMonths`: "The number of complete months the employee has been continuously employed. When users mention years of service, convert to months (for example, 2 years = 24 months). This variable captures all references to employment duration, length of service, time at the company, or seniority."<br />(Delete `monthsOfService` and update rules.) | 

### Incomplete variable descriptions
<a name="fix-incomplete-descriptions"></a>

Variable descriptions that lack detail about how users refer to concepts in everyday language make it difficult to map input to the correct variable.

**Symptom:** The `options` show the correct variable but with different values, or the translation assigns a value that doesn't match what the user said. For example, "2 years" is translated to `tenureMonths = 2` instead of `tenureMonths = 24`.

**Fix:** Update the variable description to include unit conversion rules, synonyms, and alternative phrasings. See [Write comprehensive variable descriptions](automated-reasoning-policy-best-practices.md#bp-variable-descriptions) for detailed guidance.

**Example:**


| Before (incomplete) | After (comprehensive) | 
| --- | --- | 
| isFullTime: "Full-time status." | isFullTime: "Whether the employee works full-time (true) or part-time (false). Set to true when users mention being 'full-time', working 'full hours', or working 40\+ hours per week. Set to false when users mention being 'part-time', working 'reduced hours', or working fewer than 40 hours per week." | 

### Inconsistent value formatting
<a name="fix-inconsistent-formatting"></a>

Translation ambiguity can occur when the system is unsure how to format values such as numbers, dates, or percentages.

**Symptom:** The `options` show the same variable but with different value formats. For example, one option translates "5%" to `interestRate = 5` while the other translates it to `interestRate = 0.05`.

**Fix:** Update the variable description to specify the expected format and include conversion rules. See [Specify units and formats in variable descriptions](automated-reasoning-policy-best-practices.md#bp-units-formats).

### Ambiguous input text
<a name="fix-ambiguous-input"></a>

Sometimes the input itself is genuinely ambiguous — it contains vague pronouns, unclear references, or statements that can be interpreted multiple ways.

**Symptom:** The `options` show fundamentally different interpretations of the same text. For example, "Can they take leave?" could refer to any employee type.

**Fix:** If this is a test, rewrite the input to be more specific. At runtime, your application should ask the user for clarification when it receives a `TRANSLATION_AMBIGUOUS` result. For integration patterns, see [Integrate Automated Reasoning checks in your application](integrate-automated-reasoning-checks.md).

### Adjust the confidence threshold
<a name="fix-confidence-threshold"></a>

If you see `TRANSLATION_AMBIGUOUS` results for inputs that are borderline ambiguous, you can adjust the confidence threshold. Lowering the threshold allows translations with less model agreement to proceed to validation, reducing `TRANSLATION_AMBIGUOUS` results but increasing the risk of incorrect translations.

**Important**  
Adjusting the threshold should be a last resort. In most cases, improving variable descriptions or removing overlapping variables is a better fix because it addresses the root cause. For more information on how thresholds work, see [Confidence thresholds](automated-reasoning-checks-concepts.md#ar-concept-confidence-thresholds).

## Fix rule issues
<a name="fix-rule-issues"></a>

Rule issues occur when the translation is correct but the policy logic doesn't match your domain. You've confirmed that the right variables are assigned with the right values, but the validation result is still wrong.

### Getting VALID when you expected INVALID
<a name="fix-valid-expected-invalid"></a>

The policy doesn't have a rule that prohibits the claim. The response contradicts your domain knowledge, but the policy allows it.

**Diagnosis:** Look at the `supportingRules` in the finding. These are the rules that prove the claim is valid. Check whether these rules are correct or whether a rule is missing.

**Common causes and fixes:**
+ **Missing rule.** Your policy doesn't have a rule that covers this condition. Add a new rule that captures the constraint. For example, if the policy allows parental leave for all full-time employees but should require 12 months of tenure, add: `(=> (and isFullTime (<= tenureMonths 12)) (not eligibleForParentalLeave))`
+ **Rule is too permissive.** An existing rule allows more than it should. Edit the rule to add the missing condition. For example, change `(=> isFullTime eligibleForParentalLeave)` to `(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)`
+ **Missing variable.** The policy doesn't have a variable to capture a relevant concept. Add the variable, write a clear description, and create rules that reference it.

### Getting INVALID when you expected VALID
<a name="fix-invalid-expected-valid"></a>

The policy has a rule that incorrectly prohibits the claim.

**Diagnosis:** Look at the `contradictingRules` in the finding. These are the rules that disprove the claim. Check whether these rules are correct.

**Common causes and fixes:**
+ **Rule is too restrictive.** An existing rule blocks a valid scenario. Edit the rule to relax the condition or add an exception. For example, if the rule requires 24 months of tenure but the policy should require only 12, update the threshold.
+ **Rule was misextracted.** Automated Reasoning checks misinterpreted your source document. Edit the rule to match the intended logic, or delete it and add a correct rule manually.

### Getting SATISFIABLE when you expected VALID
<a name="fix-satisfiable-expected-valid"></a>

The response is correct under some conditions but not all. The policy has additional rules that the response doesn't address.

**Diagnosis:** Compare the `claimsTrueScenario` and `claimsFalseScenario` in the finding. The difference between them shows the conditions that the response doesn't mention.

**Common causes and fixes:**
+ **Response is incomplete.** The test output doesn't mention all the conditions required by the policy. Update the test output to include the missing conditions, or change the expected result to `SATISFIABLE` if incomplete responses are acceptable for your use case.
+ **Policy has unnecessary rules.** The policy requires conditions that aren't relevant to this scenario. Review whether the additional rules should apply and remove them if they don't.

## Fix impossible results
<a name="fix-impossible-results"></a>

An `IMPOSSIBLE` result means Automated Reasoning checks can't evaluate the claims because the premises are contradictory or the policy itself contains conflicting rules. There are two distinct causes.

### Contradictions in the input
<a name="fix-impossible-input-contradictions"></a>

The test input contains statements that contradict each other. For example, "I'm a full-time employee and also part-time" sets `isFullTime = true` and `isFullTime = false` simultaneously, which is logically impossible.

**Diagnosis:** Inspect the `translation` premises in the finding. Look for variables that are assigned contradictory values.

**Fix:** If this is a test, rewrite the input to remove the contradiction. At runtime, your application should handle `IMPOSSIBLE` results by asking the user to clarify their input.

### Conflicts in the policy
<a name="fix-impossible-policy-conflicts"></a>

The policy contains rules that contradict each other, making it impossible for Automated Reasoning checks to reach a conclusion for inputs that involve the conflicting rules.

**Diagnosis:** If the input is valid (no contradictory premises), the issue is in the policy. Check the `contradictingRules` field in the finding to identify which rules conflict. Also check the quality report (see [Use the quality report](#use-quality-report)) — it flags conflicting rules automatically.

**Common causes and fixes:**
+ **Contradictory rules.** Two rules reach opposite conclusions for the same conditions. For example, one rule says full-time employees are eligible for leave, while another says employees in their first year are not eligible, without specifying what happens to full-time employees in their first year. Merge the rules into a single rule with explicit conditions: `(=> (and isFullTime (> tenureMonths 12)) eligibleForLeave)`
+ **Bare assertions.** A bare assertion like `(= eligibleForLeave true)` makes it impossible for any input to claim the user is *not* eligible. Rewrite bare assertions as implications. See [Use implications (=>) to structure rules](automated-reasoning-policy-best-practices.md#bp-use-implications).
+ **Circular dependencies.** Rules that depend on each other in a way that creates logical loops. Simplify the rules to break the cycle, or use intermediate variables to make the logic explicit.

## Use annotations to repair your policy
<a name="use-annotations"></a>

Annotations are targeted corrections you apply to your policy when tests fail. Instead of manually editing rules and variables, you can use annotations to describe the change you want and let Automated Reasoning checks apply it. Annotations are available through both the console and the API.

### Apply annotations in the console
<a name="annotations-console-workflow"></a>

1. Open the failed test and review the findings to understand the issue.

1. Modify the test conditions (for example, add a premise or change the expected result) and rerun the test. If the modified test returns the result you expect, you can apply this modification as an annotation.

1. Choose **Apply annotations**. Automated Reasoning checks starts a build workflow to apply the changes to your policy based on your feedback.

1. On the **Review policy changes** screen, review the proposed changes to your policy's rules, variables, and types. Then select **Accept changes**.

### Apply annotations using the API
<a name="annotations-api-workflow"></a>

Use the `StartAutomatedReasoningPolicyBuildWorkflow` API with `REFINE_POLICY` to apply annotations programmatically. Pass the complete current policy definition alongside the annotations.

Annotation types include:
+ **Variable annotations:** `addVariable`, `updateVariable`, `deleteVariable` — Add missing variables, improve descriptions, or remove duplicates.
+ **Rule annotations:** `addRule`, `updateRule`, `deleteRule`, `addRuleFromNaturalLanguage` — Fix incorrect rules, add missing rules, or remove conflicting rules. Use `addRuleFromNaturalLanguage` to describe a rule in plain English and let Automated Reasoning checks convert it to formal logic.
+ **Type annotations:** `addType`, `updateType`, `deleteType` — Manage custom types (enums).
+ **Feedback annotations:** `updateFromRulesFeedback`, `updateFromScenarioFeedback` — Provide natural language feedback about specific rules or scenarios and let Automated Reasoning checks deduce the necessary changes.

**Example: Add a missing variable and rule using annotations**

```
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-type REFINE_POLICY \
  --source-content "{
    \"policyDefinition\": {{EXISTING_POLICY_DEFINITION_JSON}},
    \"workflowContent\": {
      \"policyRepairAssets\": {
        \"annotations\": [
          {
            \"addVariable\": {
              \"name\": \"tenureMonths\",
              \"type\": \"INT\",
              \"description\": \"The number of complete months the employee has been continuously employed. When users mention years of service, convert to months (for example, 2 years = 24 months).\"
            }
          },
          {
            \"addRuleFromNaturalLanguage\": {
              \"naturalLanguage\": \"If an employee is full-time and has more than 12 months of tenure, then they are eligible for parental leave.\"
            }
          }
        ]
      }
    }
  }"
```

### Annotation examples
<a name="annotations-examples"></a>

**Example 1: Fix a missing tenure requirement**

Problem: The policy approves parental leave for all full-time employees, but the source document requires 12\+ months of tenure.


| Before | After annotation | 
| --- | --- | 
| Rule: `(=> isFullTime eligibleForParentalLeave)`<br />No `tenureMonths` variable. | New variable: `tenureMonths` (INT) — "The number of complete months the employee has been continuously employed."<br />Updated rule: `(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)` | 

**Example 2: Fix overlapping variables causing TRANSLATION\_AMBIGUOUS**

Problem: Two variables (`tenureMonths` and `monthsOfService`) represent the same concept, causing inconsistent translations.

Annotations:

1. `deleteVariable` for `monthsOfService`.

1. `updateVariable` for `tenureMonths` with an improved description that covers all the ways users might refer to employment duration.

1. `updateRule` for any rules that referenced `monthsOfService`, changing them to use `tenureMonths`.

**Example 3: Fix a bare assertion causing IMPOSSIBLE results**

Problem: The rule `(= eligibleForParentalLeave true)` is a bare assertion that makes it impossible for any input to claim the user is not eligible.

Annotations:

1. `deleteRule` for the bare assertion.

1. `addRuleFromNaturalLanguage`: "If an employee is full-time and has more than 12 months of tenure, then they are eligible for parental leave."

## Use the quality report
<a name="use-quality-report"></a>

The quality report is generated after each build workflow and identifies structural issues in your policy that can cause test failures. In the console, quality report issues are surfaced as warnings on the **Definitions** page. Via the API, use `GetAutomatedReasoningPolicyBuildWorkflowResultAssets` with `--asset-type QUALITY_REPORT`.

The quality report flags the following issues:

### Conflicting rules
<a name="quality-report-conflicting-rules"></a>

Two or more rules reach contradictory conclusions for the same set of conditions. Conflicting rules cause your policy to return `IMPOSSIBLE` for all validation requests that involve the conflicting rules.

**Example:** Rule A says `(=> isFullTime eligibleForLeave)` and Rule B says `(=> (<= tenureMonths 6) (not eligibleForLeave))`. For a full-time employee with 3 months of tenure, Rule A says eligible and Rule B says not eligible — a contradiction.

**Fix:** Merge the rules into a single rule with explicit conditions: `(=> (and isFullTime (> tenureMonths 6)) eligibleForLeave)`. Or delete one of the conflicting rules if it was misextracted.

### Unused variables
<a name="quality-report-unused-variables"></a>

Variables that aren't referenced by any rules. Unused variables add noise to the translation process and can cause `TRANSLATION_AMBIGUOUS` results when they compete with similar active variables for the same concept.

**Fix:** Delete unused variables unless you plan to add rules that reference them in a future iteration.

### Unused type values
<a name="quality-report-unused-type-values"></a>

Values in a custom type (enum) that aren't referenced by any rules. For example, if your `LeaveType` enum has values PARENTAL, MEDICAL, BEREAVEMENT, and PERSONAL, but no rule references PERSONAL, it's flagged as unused.

**Fix:** Either add rules that reference the unused value, or remove it from the enum. Unused values can cause translation issues if the input mentions the concept but no rule handles it.

### Disjoint rule sets
<a name="quality-report-disjoint-rule-sets"></a>

Groups of rules that don't share any variables. Disjoint rule sets aren't necessarily a problem — your policy may intentionally cover independent topics (for example, leave eligibility and expense reimbursement). However, they can indicate that variables are missing connections between related rules.

**When to act:** If the disjoint rule sets should be related (for example, they both deal with employee benefits but use different variable names for the same concept), merge the overlapping variables to connect them. If the rule sets are genuinely independent, no action is needed.

## Resolve policy ambiguities
<a name="resolve-policy-ambiguities"></a>

If your tests return `TRANSLATION_AMBIGUOUS` results or your quality report identifies ambiguous variable descriptions, use `StartAutomatedReasoningPolicyBuildWorkflow` with `RESOLVE_POLICY_AMBIGUITIES` to automatically resolve ambiguities in your policy. This workflow analyzes the policy definition and refines variable descriptions and type definitions to reduce translation ambiguity.

### Resolve ambiguities in the console
<a name="resolve-ambiguities-console"></a>

1. Open your Automated Reasoning policy in the console.

1. On the **Definitions** page, choose **Resolve ambiguities**.

1. Review the proposed changes to variable descriptions and type definitions, then choose **Accept changes**.

### Resolve ambiguities using the API
<a name="resolve-ambiguities-api"></a>

```
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-type RESOLVE_POLICY_AMBIGUITIES \
  --source-content "{
    \"policyDefinition\": {{EXISTING_POLICY_DEFINITION_JSON}}
  }"
```

After the workflow completes, retrieve the updated policy definition using `GetAutomatedReasoningPolicyBuildWorkflowResultAssets` with `--asset-type POLICY_DEFINITION`. Review the changes and update your policy's DRAFT using `UpdateAutomatedReasoningPolicy`.

## Use Kiro CLI for policy refinement
<a name="use-kiro-cli-for-refinement"></a>

Kiro CLI provides an interactive chat interface for diagnosing and fixing policy issues. It can load your policy definition and quality report, explain why tests are failing, suggest changes, and apply annotations — all through natural language conversation.

Kiro CLI is particularly useful for:
+ **Understanding failures.** Ask Kiro CLI to load a failing test and explain why it's not returning the expected result. Kiro CLI will analyze the policy definition, the test findings, and the quality report to identify the root cause.
+ **Resolving quality report issues.** Ask Kiro CLI to summarize the quality report and suggest fixes for conflicting rules, unused variables, and overlapping variable descriptions.
+ **Suggesting rule changes.** Describe the behavior you expect and ask Kiro CLI to propose the necessary variable and rule changes. Review the suggestions and instruct Kiro CLI to apply them as annotations.

**Example workflow:**

```
You: The test with ID test-12345 is not returning the expected result.
     Can you load the test definition and findings, look at the policy
     definition, and explain why this test is failing?

Kiro: [analyzes the test and policy] The test expects VALID but gets
      INVALID because rule R3 requires 24 months of tenure, while the
      test input specifies 18 months. The source document says 12 months.
      Rule R3 appears to have been misextracted.

You: Can you suggest changes to fix this?

Kiro: I suggest updating rule R3 to change the tenure threshold from 24
      to 12 months. Here's the updated rule: ...

You: Looks good. Can you use the annotation APIs to submit these changes?

Kiro: [applies annotations via the API]
```

For complete instructions on setting up and using Kiro CLI with Automated Reasoning policies, see [Use Kiro CLI with an Automated Reasoning policy](kiro-cli-automated-reasoning-policy.md).