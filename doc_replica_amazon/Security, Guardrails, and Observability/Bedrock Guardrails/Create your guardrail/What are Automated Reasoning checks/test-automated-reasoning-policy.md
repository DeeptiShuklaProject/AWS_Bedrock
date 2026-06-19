

# Test an Automated Reasoning policy
<a name="test-automated-reasoning-policy"></a>

Testing validates that your policy's rules are correct and that Automated Reasoning checks can accurately translate natural language into formal logic. You test a policy by sending natural language statements for validation, then inspecting the feedback to ensure the translation uses the right variables and that the rules produce the expected results.

There are two complementary testing approaches: generated scenarios and question-and-answer (QnA) tests. Each targets a different part of the validation pipeline. The recommended workflow is to start with scenarios to validate rule correctness, then add QnA tests to validate translation accuracy.

## Testing strategy: scenarios vs. QnA tests
<a name="testing-strategy"></a>

Automated Reasoning checks validate content in two steps: first, foundation models translate natural language into formal logic; then, mathematical techniques verify the logic against your policy rules. Each testing approach targets a different step in this pipeline.

### Generated scenarios (test rule correctness)
<a name="testing-strategy-scenarios"></a>

Generated scenarios test the *semantics encoded in your policy rules directly*. They remove the uncertainty of natural language translation from the equation, isolating whether the rules themselves are correct.

Scenarios are generated from your policy rules and represent situations that are logically possible given those rules. They are sorted to surface the most likely-to-be-wrong scenarios first. For each scenario, you review the variable assignments and decide:
+ **Thumbs up** — The scenario is realistic and should indeed be possible. Save it as a `SATISFIABLE` test.
+ **Thumbs down** — Something is off. The scenario shouldn't be possible given your domain knowledge. Provide natural language feedback explaining why, and Automated Reasoning checks will attempt to deduce the necessary rule changes.

**Example:** Your policy says full-time employees with 12\+ months of tenure are eligible for parental leave. A generated scenario might show `isFullTime = true, tenureMonths = 3, eligibleForParentalLeave = true`. If this scenario shouldn't be possible (because 3 months is less than 12), you'd give it a thumbs down and explain that employees need at least 12 months of tenure. This indicates a missing or incorrect rule.

Use scenarios as your *first* testing step. They help you catch rule issues before you invest time writing QnA tests.

### QnA tests (test translation accuracy)
<a name="testing-strategy-qna"></a>

QnA tests validate the *full pipeline end-to-end*: natural language translation and rule validation together. They mimic real user interactions and catch translation issues that scenarios can't detect.

Each QnA test consists of:
+ An **input** (optional) — The question a user might ask your application.
+ An **output** — The response your foundation model might generate.
+ An **expected result** — The validation result you expect (for example, `VALID` or `INVALID`).

**Example:** For the same parental leave policy, a QnA test might be: input = "I've been working here for 2 years full-time. Can I take parental leave?", output = "Yes, you are eligible for parental leave.", expected result = `VALID`. This tests whether Automated Reasoning checks correctly translates "2 years" to `tenureMonths = 24` and "full-time" to `isFullTime = true`.

**Tip**  
Create tests that cover both valid and invalid scenarios. For example, if your policy states "Employees need 1 year of service for parental leave," create tests for responses that correctly state this rule *and* tests for responses that incorrectly state a different requirement.

### Recommended testing workflow
<a name="testing-strategy-recommended-workflow"></a>

1. **Generate and review scenarios.** Start here to validate that your rules are correct. Fix any rule issues before proceeding.

1. **Write QnA tests for key use cases.** Focus on the questions your users are most likely to ask and the responses your LLM is most likely to generate. Include edge cases and boundary conditions.

1. **Run all tests.** Check that both scenarios and QnA tests pass.

1. **Iterate.** If tests fail, determine whether the issue is in the rules (fix the policy) or in the translation (improve variable descriptions). For more information, see [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md).

## Generate test scenarios automatically in the console
<a name="generate-automated-reasoning-tests-automatically-console"></a>

1. Go to the Automated Reasoning policy that you want to test (for example, **MyHrPolicy**).

1. Choose **View tests**, then select **Generate**.

1. In the **Generate scenarios** dialog, review the generated scenario and the related rules. Each scenario shows a set of variable assignments that are logically possible given your policy rules. Evaluate whether the scenario is realistic in your domain:
   + If the scenario could happen in your domain (it is *satisfiable*), select the thumbs up icon. This saves the scenario as a test that expects a `SATISFIABLE` result.
   + If the scenario shouldn't be possible, select the thumbs down icon. Provide an annotation explaining why — for example, "Employees need at least 12 months of tenure for parental leave, but this scenario shows 3 months with eligibility." Automated Reasoning checks uses your feedback to deduce rule changes that would prevent this scenario.
   + If you want a different scenario, choose **Regenerate scenario**.
**Tip**  
To inspect the formal logic version of the scenario, enable **Show SMT-LIB**. This is useful for understanding exactly which rules and variable assignments are involved.

1. Select **Save and close** to save the test, or **Save and add another** to continue reviewing scenarios.

1. If you provided annotations (thumbs down feedback) to any scenarios, choose **Apply annotations**. Automated Reasoning checks will start a build workflow to apply the changes to your policy based on your feedback.

1. On the **Review policy changes** screen, review the proposed changes to your policy's rules, variables, and variable types. Then select **Accept changes**.

## Generate test scenarios automatically using the API
<a name="generate-automated-reasoning-tests-api"></a>

To generate test scenarios using the API, first start a `GENERATE_POLICY_SCENARIOS` build workflow, then use `GetAutomatedReasoningPolicyNextScenario` to fetch the generated scenarios one at a time.

**Step 1: Start the scenario generation workflow**

Use `StartAutomatedReasoningPolicyBuildWorkflow` with `GENERATE_POLICY_SCENARIOS` to generate scenarios from your policy's rules.

```
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-type GENERATE_POLICY_SCENARIOS \
  --source-content "{
    \"policyDefinition\": {{EXISTING_POLICY_DEFINITION_JSON}}
  }"
```

**Step 2: Fetch generated scenarios**

Once the workflow completes, use `GetAutomatedReasoningPolicyNextScenario` to retrieve scenarios one at a time.

`policyArn` (required)  
The ARN of the Automated Reasoning policy.

`buildWorkflowId` (required)  
The identifier of the `GENERATE_POLICY_SCENARIOS` build workflow. Retrieve it from the `StartAutomatedReasoningPolicyBuildWorkflow` response or by using the `ListAutomatedReasoningPolicyBuildWorkflows` API.

**Example:**

```
aws bedrock get-automated-reasoning-policy-next-scenario \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-id {{d40fa7fc-351e-47d8-a338-53e4b3b1c690}}
```

The response includes a generated scenario with variable assignments and the related policy rules. Review the scenario and use the `CreateAutomatedReasoningPolicyTestCase` API to save it as a test, or use the annotation APIs to provide feedback if the scenario reveals a rule issue.

## Create a QnA test manually in the console
<a name="create-automated-reasoning-test-manually-console"></a>

1. Go to the Automated Reasoning policy that you want to test (for example, **MyHrPolicy**).

1. Choose **View tests**, then select **Add**.

1. In the **Add tests** dialog, do the following:

   1. For **Input** (optional), enter the question a user might ask. For **Output**, enter the response your foundation model might provide. Together these form a QnA pair that tests how your policy validates real user interactions.

   1. Choose the result you expect from the test (such as **Valid** or **Invalid**).

   1. (Optional) Select a **Confidence threshold**, which is the minimum confidence level for logic validation. Automated Reasoning checks uses multiple LLMs to translate natural language into findings. It returns only findings supported by a significant percentage of the LLM translations. The confidence threshold defines the minimum percentage of support needed for a translation to become a finding with a validity result. Findings below the threshold are surfaced as `TRANSLATION_AMBIGUOUS`.

1. Select **Save** to create the test.

## Create a QnA test using the API
<a name="create-automated-reasoning-test-manually-api"></a>

Use the `CreateAutomatedReasoningPolicyTestCase` API to create a test programmatically.

`policyArn` (required)  
The ARN of the Automated Reasoning policy.

`queryContent` (optional)  
The input query or prompt that generated the content, such as the user question. This provides context for the validation.

`guardContent` (required)  
The output content to validate — the foundation model response that will be checked for accuracy.

`expectedAggregatedFindingsResult` (optional)  
The expected validation result (for example, `VALID` or `INVALID`). The actual result is determined by sorting findings in order of severity and selecting the worst result. The severity order from worst to best is: `TRANSLATION_AMBIGUOUS`, `IMPOSSIBLE`, `INVALID`, `SATISFIABLE`, `VALID`.

`confidenceThreshold` (optional)  
The minimum confidence level for logic validation.

**Example:**

```
aws bedrock create-automated-reasoning-policy-test-case \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --query-content "{{Can I take a leave of absence if I'm a part-time employee?}}" \
  --guard-content "{{No, only full-time employees are eligible for leave of absence.}}" \
  --expected-aggregated-findings-result "{{VALID}}" \
  --confidence-threshold {{0.8}}
```

Example response:

```
{
  "testCaseId": "test-12345abcde",
  "policyArn": "arn:aws:bedrock:us-east-1:111122223333:automated-reasoning-policy/lnq5hhz70wgk"
}
```

## Run tests
<a name="run-automated-reasoning-tests"></a>

### Run tests in the console
<a name="run-automated-reasoning-tests-console"></a>

1. Go to the Automated Reasoning policy that you want to validate (for example, **MyHrPolicy**).

1. Choose **View tests**.

1. Do one of the following:
   + To run all tests, choose **Validate all tests**.
   + To run a single test, select the **Action** button next to the test and choose **Validate**.

### Run tests using the API
<a name="run-automated-reasoning-tests-api"></a>

Use the `StartAutomatedReasoningPolicyTestWorkflow` API to run tests and the `GetAutomatedReasoningPolicyTestResult` API to retrieve results.

`policyArn` (required)  
The ARN of the Automated Reasoning policy.

`buildWorkflowId` (required)  
The identifier of the build workflow to execute the tests against. Retrieve the latest build workflow using the `ListAutomatedReasoningPolicyBuildWorkflows` API.

`testCaseIds` (optional)  
A list of test identifiers to run. If not provided, all tests for the policy are run.

**Example:**

```
# Run tests
aws bedrock start-automated-reasoning-policy-test-workflow \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-id {{d40fa7fc-351e-47d8-a338-53e4b3b1c690}}

# Get results for a specific test
aws bedrock get-automated-reasoning-policy-test-result \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --build-workflow-id {{d40fa7fc-351e-47d8-a338-53e4b3b1c690}} \
  --test-case-id {{test-12345abcde}}
```

The response includes detailed test results with validation findings and execution status. To list all test results for a build workflow, use the `ListAutomatedReasoningPolicyTestResults` API.

## Understand test results
<a name="understand-test-results"></a>

When a test finishes, you receive a set of *findings*. Each finding represents a factual claim extracted from your test input, along with the validation result, the variable assignments used, and the policy rules that support the conclusion. For a detailed description of finding structure and all validation result types, see [Findings and validation results](automated-reasoning-checks-concepts.md#ar-concept-findings).

### Anatomy of a test result
<a name="test-results-anatomy"></a>

Each test result includes:
+ **Expected result** — The result you set when creating the test.
+ **Actual result** — The aggregated result from running the test. This is determined by sorting findings in order of severity and selecting the worst result. The severity order from worst to best is: `TRANSLATION_AMBIGUOUS`, `IMPOSSIBLE`, `INVALID`, `SATISFIABLE`, `VALID`. For example, a test with two `VALID` findings and one `IMPOSSIBLE` finding has an aggregated result of `IMPOSSIBLE`.
+ **Execution result** — Whether the test passed (expected and actual results match) or failed.
+ **Findings** — The individual validation results. Each finding contains the translated premises and claims, a confidence score, variable assignments, and the policy rules that support the conclusion.

### Practical interpretation of results
<a name="test-results-practical-interpretation"></a>

The following table summarizes what each validation result means in practice and what action to take when you see it in a test. For the full reference including finding fields and detailed descriptions, see [Validation results reference](automated-reasoning-checks-concepts.md#ar-concept-validation-results).


| Result | What it means | What to do | 
| --- | --- | --- | 
| VALID | The claims in the response are mathematically proven correct given the premises and your policy rules. The finding includes supportingRules that prove the claims and a claimsTrueScenario demonstrating how the claims are true. | If this is the expected result, the test passes. Check untranslatedPremises and untranslatedClaims for parts of the input that were not validated — a VALID result only covers the translated claims. | 
| INVALID | The claims contradict your policy rules. The finding includes contradictingRules showing which rules were violated. | If this is the expected result, the test passes. If unexpected, check whether the rules are correct or whether the translation assigned the wrong variables. Review the contradictingRules to understand which rules caused the result. | 
| SATISFIABLE | The claims are consistent with your policy but don't address all relevant rules. The response is correct under some conditions but not all. The finding includes both a claimsTrueScenario and a claimsFalseScenario showing the conditions under which the claims are true and false. | Compare the two scenarios to identify the missing conditions. This typically means the response is incomplete — it's not wrong, but it doesn't mention all the requirements. Consider whether your test should expect SATISFIABLE or whether the response should be more complete. | 
| IMPOSSIBLE | Automated Reasoning checks can't evaluate the claims because the premises are contradictory or the policy itself contains conflicting rules. | Check whether the test input contains contradictory statements (for example, "I'm full-time and also part-time"). If the input is valid, the contradiction is likely in your policy — check the quality report for conflicting rules. See [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md). | 
| TRANSLATION\_AMBIGUOUS | The translation from natural language to formal logic was ambiguous. The multiple LLMs used for translation disagreed on how to interpret the input. The finding includes the alternative interpretations to help you understand the disagreement. | This is usually a variable description issue. Review the alternative interpretations to understand where the disagreement is, then improve the relevant variable descriptions. Common causes: overlapping variables, vague descriptions, or ambiguous input text. See [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md). | 
| TOO\_COMPLEX | The input contains too much information for Automated Reasoning checks to process within its latency limits. | Simplify the test input. If the issue persists, your policy may be too complex — consider splitting it into multiple focused policies or simplifying rules that involve non-linear arithmetic. | 
| NO\_TRANSLATIONS | The input couldn't be translated into formal logic. This typically means the input is not relevant to your policy's domain, or the policy doesn't have variables to model the concepts in the input. | If the input should be relevant to your policy, add the missing variables and update your rules. If the input is genuinely off-topic, this result is expected — your application should handle off-topic content separately (for example, using topic policies). | 

### Debugging tips for failed tests
<a name="test-results-debugging-tips"></a>

When a test fails (the actual result doesn't match the expected result), use the following approach to diagnose the issue:

1. **Check the translation first.** Look at the premises and claims in the finding. Are the right variables assigned? Are the values correct? If the translation is wrong, the issue is in your variable descriptions, not your rules. For example, if "2 years" was translated to `tenureMonths = 2` instead of `tenureMonths = 24`, the variable description needs to specify the unit conversion.

1. **Check the rules.** If the translation looks correct, the issue is in your policy rules. Look at the `supportingRules` or `contradictingRules` in the finding to identify which rules are involved. Compare them against your source document.

1. **Check for untranslated content.** Look at `untranslatedPremises` and `untranslatedClaims`. If important parts of the input were not translated, you may need to add variables to capture those concepts.

1. **Check the confidence score.** A low confidence score indicates the translation models disagreed. This suggests the variable descriptions are ambiguous for this type of input.

For detailed troubleshooting guidance, see [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md).