

# Use Kiro CLI with an Automated Reasoning policy
<a name="kiro-cli-automated-reasoning-policy"></a>

You can use Kiro CLI to ask questions about your Automated Reasoning policies, understand the behavior of the various rules, and request changes that address failing tests or ambiguities in the policy itself. Kiro CLI is particularly useful for the iterative refinement workflow described in [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md) because it can load your policy definition, analyze test results, and apply annotations through natural language conversation.

## Prerequisites
<a name="kiro-cli-prerequisites"></a>

To use Kiro CLI with your Automated Reasoning policies, you must first complete the following steps:
+ Install the latest version of [Kiro CLI](https://kiro.dev/cli/).
+ Install the latest version of the AWS CLI.
+ Create an Automated Reasoning policy using a document through the console or APIs. To get started quickly, use the built-in sample Homework policy from the console. For more information, see [Create your Automated Reasoning policy](create-automated-reasoning-policy.md).
+ Familiarize yourself with Automated Reasoning checks concepts, particularly policies, rules, variables, and findings. For more information, see [Automated Reasoning checks concepts](automated-reasoning-checks-concepts.md).
+ Copy the content of the contextual prompt provided in [Automated Reasoning policy API context prompt](#kiro-cli-context-prompt) and save it in a Markdown file in your project folder. This prompt helps Kiro CLI use the Automated Reasoning policy control plane and test API correctly.

**Note**  
For the prompt examples below, we use the sample Homework policy. The prompts should work just as well with other policies, simply change the topic highlighted.

**Note**  
Automated Reasoning policies can be complex and require Kiro CLI to reason through complex logical constructs. For best performance, we recommend using larger LLMs such as Anthropic Sonnet 4.5. To change model in Kiro CLI, use the `/model` command.

## Getting started
<a name="kiro-cli-getting-started"></a>

You need the ARN of the Automated Reasoning policy you created to start the workflow with Kiro CLI.

1. Using the console, open your Automated Reasoning policy and from the **Policy Overview** page, open the **Policy details** tab.

1. In the **Policy details** tab, find the policy ARN and copy it to your clipboard.

1. Using the terminal, start a Kiro CLI session with the following command:

   ```
   kiro-cli
   ```

1. With your first prompt, ask Kiro to look for the instructions Markdown file you copied from this page as part of the prerequisites. For example:

   ```
   We will be using Automated Reasoning checks control plane APIs. I have saved an instructions file called {{your_file_name}}.md in this folder. Read this file as it will give you the context you need to work with the APIs.
   ```

1. After Kiro CLI has loaded and understood Automated Reasoning checks' APIs, ask it to load the latest build of your policy and start exploring it. Use a variation of the following prompt with the ARN you copied:

   ```
   Load the policy assets for the latest build of the policy with ARN {{YOUR_POLICY_ARN}}. Make sure you understand the policy with all its rules and variables. Give a high-level description of the policy and the type of content it is capable of validating.
   ```

At this point, Kiro CLI should provide you with a brief description of the policy's rules and variables. Kiro CLI should also load the policy quality report and summarize issues like unused types and variables.

## Resolving policy issues
<a name="kiro-cli-resolving-policy-issues"></a>

You can use Kiro CLI to resolve policy issues reported in the policy report. First, ask Kiro to give you a summary of the quality report:

```
Can you give me a summary of the quality report for this policy?
```

The quality report includes a list of the unused variables, conflicting rules, and disjointed rules and other potential issues with the policy. For more information about interpreting the quality report, see [Use the quality report](address-failed-automated-reasoning-tests.md#use-quality-report).

Conflicting rules will cause your policy to respond with `IMPOSSIBLE` to all validation requests. For more information about conflicting rules and how to resolve them, see [Conflicts in the policy](address-failed-automated-reasoning-tests.md#fix-impossible-policy-conflicts). You can ask Kiro CLI to explain the conflict and propose a solution:

```
Can you look at the conflicting rules, explain how they are used in the policy, why they conflict, and suggest a change such as deleting one of the rules or merging the logic from the two into a single rule?
```

Unused variables can cause validation results to return `TRANSLATION_AMBIGUOUS` results. For more information about why unused variables cause issues, see [Unused variables](automated-reasoning-policy-best-practices.md#bp-anti-unused-variables). You can ask Kiro CLI to help with this issue:

```
I see the quality report lists some unused variables, can you get rid of them?
```

Similarly, ambiguous variables that are semantically similar can cause validation results to return `TRANSLATION_AMBIGUOUS` results. For more information about overlapping variables and how to fix them, see [Overlapping variables](automated-reasoning-policy-best-practices.md#bp-anti-overlapping-variables) and [Overlapping variable definitions](address-failed-automated-reasoning-tests.md#fix-overlapping-variables). You can ask Kiro CLI to help with this issue:

```
Automated Reasoning checks translate input natural language into logical statements that use the schema of variables from the policy. Variables that are semantically similar - ambiguous - can cause issues with inconsistent translations. Can you take a look at the schema of variables and help me identify variables that have potentially overlapping meanings? If you find any, suggest changes like removing one of them or merging them. Variable changes are also likely to require corresponding rule changes.
```

**Note**  
After processing some changes, Kiro CLI will ask for confirmation to apply them. At this point, you can use the Bedrock Console user interface to review the proposed changes in a diff screen. If you use the console to review and approve the changes, do not forget to tell Kiro CLI to reload the latest build of the policy definition.

## Interacting with a policy
<a name="kiro-cli-interacting-with-policy"></a>

You can use Kiro CLI to explore your policy. For example, you could ask Kiro CLI to summarize policy rules related to a specific area. Using the sample homework policy as an example, you could ask Kiro CLI to tell you about the rules that constrain math homework specifically:

```
Can you tell me about the rules that constrain {{math homework}}? Explain the rules themselves and how they fit in the broader policy.
```

You can also use Kiro CLI to add functionality to the policy. Automated Reasoning policies often work around some key output variables that capture the user intent. For example, the sample homework submission policy uses an `isSubmissionAcceptable` variable as the output of its rules. You can use Kiro CLI to alter the policy to capture other possible user questions. When adding new rules, follow the best practices described in [Automated Reasoning policy best practices](automated-reasoning-policy-best-practices.md), particularly [Use implications (=>) to structure rules](automated-reasoning-policy-best-practices.md#bp-use-implications).

## Editing or revising your policy
<a name="kiro-cli-editing-revising-policy"></a>

You can ask Kiro CLI whether the policy is capable of validating specific questions from your users. For example, the homework policy is focused on determining whether a homework submission is acceptable. You can expect a positive answer from Kiro CLI with this question:

```
Can this policy validate answers about whether {{homework submissions are acceptable}}?
```

If you ask about delaying homework submission in the sample Homework policy, Kiro CLI will explain that the policy is not capable of answering these questions:

```
Can this policy validate answers about {{permissible delays in homework submissions}}?
```

Kiro CLI will explain what the policy can and cannot do:

```
> Yes, but with limitations. The policy can validate whether a late submission is acceptable, but it cannot answer general questions about permissible delays.

What it CAN validate:
- Whether a specific late submission is acceptable given the circumstances
- Example: "Student submitted 2 days late with a doctor's note because they were sick before the deadline" → The policy will determine if this is acceptable (it would be)

What it CANNOT validate:
- General questions like "How many days late can a student submit homework?"
- Questions about delay policies without specific submission details
- Hypothetical scenarios without concrete variable values

The late submission logic:
The policy allows late submissions (submissionDate > 0) ONLY if:
1. The student has a valid doctor's note (hasDoctorNote = true), AND
2. The student was sick before the original deadline (wasSickPriorToDeadline = true)

Without both conditions met, any submission after the due date (submissionDate > 0) is automatically rejected.

So it's designed to validate specific submission instances against the rules, not to answer policy interpretation questions.
```

When you discover something the policy cannot do, you can ask Kiro CLI to update the policy to capture this information using the following prompt:

```
I would like the policy to also validate answers about {{by how many days homework submissions can be delayed. Homework submissions accompanied by a doctor note can be up to 7 days late}}. Suggest the necessary variables and rules to capture these new questions.
```

In response to this prompt, Kiro CLI will suggest a set of variables and rules that can be added to the policy to validate the new type of questions. Review the suggestions and if they align with your intent, you can instruct Kiro CLI to use Automated Reasoning checks' annotation APIs to make these changes to the policy:

```
Looks good. Can you use the annotation APIs to submit these changes to the policy.
```

Once Kiro CLI confirms the annotations are ready, you can open your policy in the console to review the annotations. If the annotations are correct, choose **Apply Annotations**.

After applying the annotations, ask Kiro CLI to reload the latest build of the policy to ensure Kiro CLI is working with a current copy:

```
I applied the annotations. Reload the latest build of the policy.
```

## Address failing tests
<a name="kiro-cli-address-failing-tests"></a>

A good way to test that your Automated Reasoning policy can validate natural language generated by your application is to use tests. After creating test Q&As with their expected results, you can use Kiro CLI to understand why a test did not return the expected result and adjust the policy. For more information about creating and running tests, see [Test an Automated Reasoning policy](test-automated-reasoning-policy.md). For a systematic approach to diagnosing test failures without Kiro CLI, see [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md).

1. As a first step, ask Kiro CLI to load the failed test and explain why it is not returning the expected result based on the policy definition. Use the console or APIs to copy the test ID for your failing test. In the console, the test ID is available both in the table that lists tests and the detail page for each test.

   ```
   The test with ID {{YOUR_TEST_ID}} is not returning the expected result. Can you load the test definition and findings, look at the policy definition, and explain why this test is failing.
   ```

1. The explanation from Kiro CLI will give you direction on whether the policy is doing the right thing (and you should change the expected result for the test) or the policy is wrong. You can ask Kiro CLI to suggest changes to the policy to ensure that the test returns the expected result:

   ```
   Can you suggest changes to the policy to ensure this test returns the expected result? Explain why you are suggesting these changes. Only create rules in if/then format.
   ```
**Note**  
When suggesting rule changes, Kiro CLI may try to overfit to the specific example and create rules that are not useful in other use cases. Check the test output and give Kiro CLI guidance to focus it on the right problem. For guidance on writing effective rules, see [Automated Reasoning policy best practices](automated-reasoning-policy-best-practices.md).  
For example, asking Kiro to change the sample Homework policy so that the `SATISFIABLE` test returns `VALID`, may lead Kiro to suggest adding axioms to the policy that make the test always pass, such as creating a rule that says `(false isHomeworkSubmissionAcceptable)`. This would ensure the value is always false. While this technically fixes the problematic test, it is detrimental to the overall policy functionality. Analyzing the scenarios returned by the `SATISFIABLE` test result, you can see that give Kiro CLI better guidance to either create a new rule that only covers the constraints specified in the test, or update the existing rules to only check the test constraints:

1. Once you are happy with the suggested changes, ask Kiro CLI to submit the annotations and review them using the console user interface:

   ```
   Looks good. Can you start a build workflow to apply these changes to the policy.
   ```

1. After applying the changes and moving on to the next failing test, ask Kiro CLI to reload the latest build of the policy:

   ```
   I applied the changes. Reload the latest build of the policy.
   ```

## Next steps
<a name="kiro-cli-next-steps"></a>

Once you are happy with the Automated Reasoning policy, you can deploy it for use in Amazon Bedrock Guardrails. For more information, see [Deploy your Automated Reasoning policy in your application](deploy-automated-reasoning-policy.md).

After deploying your policy, see [Integrate Automated Reasoning checks in your application](integrate-automated-reasoning-checks.md) for guidance on using Automated Reasoning checks at runtime to validate LLM responses and act on the feedback.

## Automated Reasoning policy API context prompt
<a name="kiro-cli-context-prompt"></a>

Copy the following content and save it in a Markdown file in your project folder for Kiro CLI. This prompt provides Kiro CLI with the context it needs to work with the Automated Reasoning policy APIs correctly.

```
# Automated Reasoning Policy APIs and Workflows

## Table of Contents

### Core APIs
- Policy Management
- Policy Versions
- Build Workflows
- Test Management
- Annotations & Scenarios

### Build Workflow Types
- INGEST_CONTENT Workflow
- REFINE_POLICY Workflow
- IMPORT_POLICY Workflow
- GENERATE_FIDELITY_REPORT Workflow
- GENERATE_POLICY_SCENARIOS Workflow
- RESOLVE_POLICY_AMBIGUITIES Workflow
- ITERATIVELY_REFINE_POLICY Workflow

### Annotation Type Reference
- Type Management Annotations
- Variable Management Annotations
- Rule Management Annotations
- Natural Language Rule Creation
- Feedback-Based Updates

### Common Workflows
1. Getting Started (New Policy)
2. Building Policy from Document
3. Policy Development Cycle
4. REFINE_POLICY Workflow (Annotation-Based)

### Testing Workflow
1. Primary Approach: Scenarios API (Recommended)
2. Secondary Approach: Test Cases (User Experience)
3. Test Result Analysis and Troubleshooting

### Build Workflow Monitoring
- Check Build Status
- List Build History
- Best Practice: Clean Build Management
- Troubleshooting Build Failures

### Build Workflow Assets
- Asset Types
- Understanding Conflicting Rules
- Understanding Disjoint Rule Sets
- Advanced Quality Report Analysis

### Additional Topics
- Policy Version Export
- Key Concepts
- Important Format Requirements
- Policy Modeling Best Practices
- ARN Formats

## Core APIs

### Policy Management
- `create-automated-reasoning-policy` - Create initial policy (returns policy ARN). Supports optional `--description`, `--kms-key-id` (for encryption with a customer managed AWS KMS key), `--tags` (up to 200 tags), and `--client-request-token` (idempotency token).
- `get-automated-reasoning-policy` - Retrieve policy (DRAFT version by default with unversioned ARN). Returns `policyId`, `definitionHash`, and `kmsKeyArn` (if a KMS key was provided at creation).
- `update-automated-reasoning-policy` - Update DRAFT policy with new definition. Accepts optional `--name` and `--description` updates alongside `--policy-definition` (required).
- `delete-automated-reasoning-policy` - Delete policy. Supports optional `--force` flag: when true, deletes the policy and all its artifacts (versions, test cases, test results) without validation; when false (default), validates that all artifacts have been deleted first.
- `list-automated-reasoning-policies` - List all policies. Supports optional `--policy-arn` filter to list only versions of a specific policy.

### Policy Versions
- `create-automated-reasoning-policy-version` - Snapshot DRAFT into numbered version. Requires `--last-updated-definition-hash` (concurrency token from get/create/update response). Supports optional `--tags` (up to 200 tags) and `--client-request-token`.
- `export-automated-reasoning-policy-version` - Export specific policy version definition including rules, variables, and types.

### Build Workflows
- `start-automated-reasoning-policy-build-workflow` - Start build process. Valid `--build-workflow-type` values: `INGEST_CONTENT`, `REFINE_POLICY`, `IMPORT_POLICY`, `GENERATE_FIDELITY_REPORT`, `GENERATE_POLICY_SCENARIOS`, `RESOLVE_POLICY_AMBIGUITIES`, `ITERATIVELY_REFINE_POLICY`. Supports optional `--client-request-token` (idempotency token, passed as header).
- `get-automated-reasoning-policy-build-workflow` - Get build workflow status. Status values: `SCHEDULED`, `CANCEL_REQUESTED`, `PREPROCESSING`, `BUILDING`, `TESTING`, `COMPLETED`, `FAILED`, `CANCELLED`.
- `cancel-automated-reasoning-policy-build-workflow` - Cancel running build
- `delete-automated-reasoning-policy-build-workflow` - Delete build workflow. Requires `--last-updated-at` (concurrency token timestamp).
- `list-automated-reasoning-policy-build-workflows` - List build workflows
- `get-automated-reasoning-policy-build-workflow-result-assets` - Get compiled policy assets. Requires `--asset-type`. Valid asset types: `BUILD_LOG`, `QUALITY_REPORT`, `POLICY_DEFINITION`, `GENERATED_TEST_CASES`, `POLICY_SCENARIOS`, `FIDELITY_REPORT`, `ASSET_MANIFEST`, `SOURCE_DOCUMENT`. Supports optional `--asset-id` (required when retrieving `SOURCE_DOCUMENT` assets if multiple source documents were used; obtain from the `ASSET_MANIFEST`).

### Test Management
- `create-automated-reasoning-policy-test-case` - Create test case. Requires `--guard-content` and `--expected-aggregated-findings-result`. Supports optional `--query-content`, `--confidence-threshold` (Double, 0 to 1, minimum confidence level for logic validation), and `--client-request-token`.
- `get-automated-reasoning-policy-test-case` - Get test case details (includes `confidenceThreshold` if set)
- `update-automated-reasoning-policy-test-case` - Update test case. Requires `--guard-content`, `--expected-aggregated-findings-result`, and `--last-updated-at` (concurrency token). Supports optional `--query-content`, `--confidence-threshold`, and `--client-request-token`.
- `delete-automated-reasoning-policy-test-case` - Delete test case. Requires `--last-updated-at` (concurrency token).
- `list-automated-reasoning-policy-test-cases` - List test cases
- `start-automated-reasoning-policy-test-workflow` - Run tests against a completed build. Requires `--build-workflow-id` (the build workflow must show COMPLETED status). Supports optional `--test-case-ids` (array of test case IDs to run; if not provided, all tests for the policy are run) and `--client-request-token`.
- `get-automated-reasoning-policy-test-result` - Get test result for a specific test case. Requires `--build-workflow-id` and `--test-case-id`.
- `list-automated-reasoning-policy-test-results` - List test results. Requires `--build-workflow-id`.

### Annotations & Scenarios
- `get-automated-reasoning-policy-annotations` - Get policy annotations for a build workflow. Requires `--build-workflow-id`. Returns `annotations`, `annotationSetHash` (concurrency token), `buildWorkflowId`, `name`, `policyArn`, and `updatedAt`.
- `update-automated-reasoning-policy-annotations` - Update annotations for a build workflow. Requires `--build-workflow-id`, `--annotations` (array of annotation objects, max 10), and `--last-updated-annotation-set-hash` (concurrency token from get-annotations response). Returns updated `annotationSetHash`.
- `get-automated-reasoning-policy-next-scenario` - Get next test scenario

**Important**: Do NOT use `get-automated-reasoning-policy-annotations` or 
`update-automated-reasoning-policy-annotations` for the `REFINE_POLICY` workflow. Annotations are passed directly in the `start-automated-reasoning-policy-build-workflow` call.

## Build Workflow Types

1. **INGEST_CONTENT** - Process documents to create/extract policy rules
2. **REFINE_POLICY** - Refine and improve existing policies using annotations
3. **IMPORT_POLICY** - Import policies from external sources
4. **GENERATE_FIDELITY_REPORT** - Generate a fidelity report for the policy
5. **GENERATE_POLICY_SCENARIOS** - Generate test scenarios from policy rules
6. **RESOLVE_POLICY_AMBIGUITIES** - Resolve translation ambiguities in variable descriptions and type definitions
7. **ITERATIVELY_REFINE_POLICY** - Refine a policy using source documents and optional natural language feedback

### INGEST_CONTENT Workflow
- **Purpose**: Extract policy rules from documents (PDF/TXT)
- **Input**: Documents + optional existing policy definition
- **Use Cases**: Document-to-policy conversion, incremental policy building
- **Content Structure**: `workflowContent.documents[]`

**CRITICAL: Complete Policy Definition for Incremental Building**

When adding documents to an existing policy, you must include the complete current policy definition:

```json
// CORRECT - Incremental policy building
{
  "policyDefinition": {
    "version": "1.0",
    "types": [/* ALL existing types */],
    "rules": [/* ALL existing rules */],
    "variables": [/* ALL existing variables */]
  },
  "workflowContent": {
    "documents": [/* New documents to process */]
  }
}
```

### REFINE_POLICY Workflow
- **Purpose**: Iteratively improve policies with targeted modifications
- **Input**: Policy definition + annotations for specific changes
- **Use Cases**: Kiro CLI suggestions, test-driven improvements, feedback-based refinement
- **Content Structure**: `workflowContent.policyRepairAssets.annotations[]`

**CRITICAL: Complete Policy Definition Required**

ALL build workflows require the COMPLETE existing policy definition in the `policyDefinition` section, not just the changes you want to make.

**REFINE_POLICY Annotation Types:**

**Top-Level Annotations:**
- **Type Management**: `addType`, `updateType`, `deleteType`
- **Variable Management**: `addVariable`, `updateVariable`, `deleteVariable`
- **Rule Management**: `addRule`, `updateRule`, `deleteRule`
- **Natural Language Rules**: `addRuleFromNaturalLanguage`
- **Feedback-Based Updates**: `updateFromRulesFeedback`, `updateFromScenarioFeedback`

**Sub-Operations (only within `updateType`):**
- `addTypeValue`, `updateTypeValue`, `deleteTypeValue` - Used to modify values within an existing custom type

**important**: Only create rules in if/then format.

### GENERATE_POLICY_SCENARIOS Workflow
- **Purpose**: Generate test scenarios from policy rules to validate rule correctness
- **Input**: Policy definition only
- **Use Cases**: Generating test scenarios for review, identifying rule issues
- **Content Structure**: No `workflowContent` required — only `policyDefinition`
- **Post-Workflow**: Use `GetAutomatedReasoningPolicyNextScenario` to fetch generated scenarios one at a time

### RESOLVE_POLICY_AMBIGUITIES Workflow
- **Purpose**: Automatically resolve translation ambiguities in variable descriptions and type definitions
- **Input**: Policy definition only
- **Use Cases**: Fixing TRANSLATION_AMBIGUOUS test results, improving variable descriptions for clearer translation
- **Content Structure**: No `workflowContent` required — only `policyDefinition`

### ITERATIVELY_REFINE_POLICY Workflow
- **Purpose**: Refine an existing policy using a source document and optional natural language feedback
- **Input**: Policy definition + source document + optional feedback
- **Use Cases**: Updating a policy when the source document changes, guiding refinement with specific instructions
- **Content Structure**: `workflowContent.iterativeRefinementContent.documents[]` + optional `workflowContent.iterativeRefinementContent.feedback`

## Annotation Type Reference

### Type Management Annotations

#### `addType` - Create New Custom Type
```json
{
  "addType": {
    "name": "ApprovalStatus",
    "description": "Status values for approval requests",
    "values": [
      {
        "value": "PENDING",
        "description": "Request is awaiting approval"
      },
      {
        "value": "APPROVED",
        "description": "Request has been approved"
      },
      {
        "value": "REJECTED",
        "description": "Request has been rejected"
      }
    ]
  }
}
```

#### `updateType` - Modify Existing Custom Type
```json
{
  "updateType": {
    "name": "ApprovalStatus",
    "newName": "RequestStatus",
    "description": "Updated status values for all request types",
    "values": [
      {
        "addTypeValue": {
          "value": "ESCALATED",
          "description": "Request escalated to higher authority"
        }
      },
      {
        "updateTypeValue": {
          "value": "PENDING",
          "newValue": "WAITING",
          "description": "Request is waiting for review"
        }
      },
      {
        "deleteTypeValue": {
          "value": "REJECTED"
        }
      }
    ]
  }
}
```

#### `deleteType` - Remove Custom Type
```json
{
  "deleteType": {
    "name": "ObsoleteType"
  }
}
```

### Variable Management Annotations

#### `addVariable` - Create New Variable
```json
{
  "addVariable": {
    "name": "requestAmount",
    "type": "NUMBER",
    "description": "The monetary amount of the approval request in USD"
  }
}
```

#### `updateVariable` - Modify Existing Variable
```json
{
  "updateVariable": {
    "name": "requestAmount",
    "newName": "approvalAmount",
    "description": "The monetary amount requiring approval in USD (updated description)"
  }
}
```

#### `deleteVariable` - Remove Variable
```json
{
  "deleteVariable": {
    "name": "obsoleteVariable"
  }
}
```

### Rule Management Annotations

#### `addRule` - Create New Rule (SMT-LIB)
```json
{
  "addRule": {
    "expression": "(=> (and (= userRole MANAGER) (< requestAmount 10000)) (not approvalRequired))"
  }
}
```

#### `updateRule` - Modify Existing Rule
```json
{
  "updateRule": {
    "ruleId": "A1B2C3D4E5F6",
    "expression": "(=> (and (= userRole MANAGER) (< requestAmount 5000)) (not approvalRequired))"
  }
}
```

#### `deleteRule` - Remove Rule
```json
{
  "deleteRule": {
    "ruleId": "G7H8I9J0K1L2"
  }
}
```

### Natural Language Rule Creation

#### `addRuleFromNaturalLanguage` - Convert Natural Language to Rule
```json
{
  "addRuleFromNaturalLanguage": {
    "naturalLanguage": "Managers can approve expense requests up to $5,000 without additional authorization. Senior managers can approve up to $25,000."
  }
}
```

### Feedback-Based Updates

#### `updateFromRulesFeedback` - Improve Rules Based on Performance
```json
{
  "updateFromRulesFeedback": {
    "ruleIds": ["A1B2C3D4E5F6", "G7H8I9J0K1L2"],
    "feedback": "These rules are too restrictive for emergency scenarios. Add exception handling for urgent requests with proper escalation paths."
  }
}
```

#### `updateFromScenarioFeedback` - Improve Based on Test Scenarios
```json
{
  "updateFromScenarioFeedback": {
    "ruleIds": ["A1B2C3D4E5F6"],
    "scenarioExpression": "(and (= requestType EMERGENCY) (= userRole MANAGER) (> requestAmount 10000))",
    "feedback": "Emergency requests should have different approval thresholds. Current rule blocks legitimate emergency expenses."
  }
}
```

**Important**: Do NOT use `get-automated-reasoning-policy-annotations` or `update-automated-reasoning-policy-annotations` for the `REFINE_POLICY` workflow. Annotations are passed directly in the `start-automated-reasoning-policy-build-workflow` call.

## Common Workflows

### 1. Getting Started (New Policy)

**CRITICAL: Always Create Policy First**

You must create a policy before starting any build workflows.

```bash
# Step 1: Create initial policy (REQUIRED FIRST STEP)
aws bedrock create-automated-reasoning-policy \
  --region us-west-2 \
  --name "YourPolicyName"

# Step 2: Extract the policyArn from the response above, then start build workflow
aws bedrock start-automated-reasoning-policy-build-workflow \
  --region us-west-2 \
  --policy-arn "arn:aws:bedrock:us-west-2:123456789012:automated-reasoning-policy/abcd1234efgh" \
  --build-workflow-type INGEST_CONTENT \
  --source-content <policy-definition>

# Step 3: Get build results
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --region us-west-2 \
  --policy-arn "arn:aws:bedrock:us-west-2:123456789012:automated-reasoning-policy/abcd1234efgh" \
  --build-workflow-id <workflow-id>
```

### 2. Building Policy from Document

**RECOMMENDED: Using CLI Input JSON File**

```bash
# Step 1: Encode PDF to base64 and create JSON file with base64 content
PDF_BASE64=$(base64 -i your-policy.pdf | tr -d '\n')

cat > ingest-policy.json << EOF
{
  "policyArn": "arn:aws:bedrock:us-west-2:123456789012:automated-reasoning-policy/your-actual-policy-id",
  "buildWorkflowType": "INGEST_CONTENT",
  "sourceContent": {
    "policyDefinition": {
      "version": "1.0",
      "types": [],
      "rules": [],
      "variables": []
    },
    "workflowContent": {
      "documents": [
        {
          "document": "$PDF_BASE64",
          "documentContentType": "pdf",
          "documentName": "Company Policy Document",
          "documentDescription": "Main policy document containing business rules and organizational guidelines."
        }
      ]
    }
  }
}
EOF

# Step 2: Use the JSON file
aws bedrock start-automated-reasoning-policy-build-workflow \
  --region us-west-2 \
  --cli-input-json file://ingest-policy.json
```

### 3. Policy Development Cycle

```bash
# 1. Import/process policy definition
aws bedrock start-automated-reasoning-policy-build-workflow \
  --build-workflow-type IMPORT_POLICY

# 2. Update DRAFT with processed definition
aws bedrock update-automated-reasoning-policy \
  --policy-arn <unversioned-arn> \
  --policy-definition <build-output>

# 3. Create versioned snapshot of DRAFT (definitionHash from step 2 response)
aws bedrock create-automated-reasoning-policy-version \
  --policy-arn <unversioned-arn> \
  --last-updated-definition-hash <definition-hash>
```

## Testing Workflow

### Primary Approach: Scenarios API (Recommended)

Use `get-automated-reasoning-policy-next-scenario` for comprehensive policy validation.

The Scenarios API is superior for testing because it:
- Tests formal logic directly - Validates policy rules work correctly
- AI-generated scenarios - Comprehensive coverage of edge cases and rule interactions
- Targets specific rules - Tests individual rules and combinations
- Always works - No natural language translation issues
- Intelligent test generation - AI understands policy logic deeply

```bash
# Generate intelligent test scenarios automatically
aws bedrock get-automated-reasoning-policy-next-scenario \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123"
```

### Secondary Approach: Test Cases (User Experience)

Use manual test cases to validate natural language translation.

```bash
# Create test cases for natural language validation
aws bedrock create-automated-reasoning-policy-test-case \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --guard-content "It is 2:30 PM on a clear day" \
  --query-content "What color should the sky be?" \
  --expected-aggregated-findings-result "VALID" \
  --confidence-threshold 0.8
```

### Test Result Analysis and Troubleshooting

**Understanding Test Results:**

**Scenarios API Results:**
- `expectedResult: SATISFIABLE` - Policy logic works correctly
- API errors or logic conflicts - Policy needs fixing with REFINE_POLICY

**Common Test Case Failure Modes:**

1. **TRANSLATION_AMBIGUOUS**
   - Problem: AI can't map natural language to policy variables
   - Solution: Improve variable descriptions with more natural language synonyms

2. **SATISFIABLE when expecting VALID**
   - Problem: Your expected result label is likely WRONG, not the policy
   - SATISFIABLE = "This scenario is logically consistent with the policy rules"
   - VALID = "This is the correct/expected answer according to the policy"
   - Solution: Change `expectedAggregatedFindingsResult` from `VALID` to `SATISFIABLE`

3. **Empty testFindings arrays**
   - Problem: Translation issues, not rule violations
   - Solution: Focus on improving natural language descriptions, not policy logic

**Valid values for `expectedAggregatedFindingsResult`:**
- `VALID` - The claims are true, implied by the premises and the policy
- `INVALID` - The claims are false, not implied by the premises and policy
- `SATISFIABLE` - The claims can be true or false depending on assumptions
- `IMPOSSIBLE` - Automated Reasoning can't make a statement (e.g., conflicting policy rules)
- `TRANSLATION_AMBIGUOUS` - Ambiguity in translation prevented validity checking
- `TOO_COMPLEX` - Input too complex for Automated Reasoning to process within latency limits
- `NO_TRANSLATION` - Some or all of the input wasn't translated into logic

### Running Tests Against a Build

After creating test cases, run them against a completed build workflow:

```bash
# Run all tests against a completed build
aws bedrock start-automated-reasoning-policy-test-workflow \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123"

# Run specific tests only
aws bedrock start-automated-reasoning-policy-test-workflow \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --test-case-ids '["A1B2C3D4E5F6"]'

# Get result for a specific test case
aws bedrock get-automated-reasoning-policy-test-result \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --test-case-id "A1B2C3D4E5F6"

# List all test results for a build
aws bedrock list-automated-reasoning-policy-test-results \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123"
```

## Build Workflow Monitoring

**Critical Build Limits**: The API supports maximum 2 total build workflows per policy, with only 1 allowed to be IN_PROGRESS at any time. When a build workflow completes, you can instruct the user to review the output using the console. 

### Check Build Status

```bash
aws bedrock get-automated-reasoning-policy-build-workflow \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123"
```

### List Build History

```bash
aws bedrock list-automated-reasoning-policy-build-workflows \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --max-results 50
```

### Best Practice: Clean Build Management

```bash
# 1. Check existing builds before starting new ones
aws bedrock list-automated-reasoning-policy-build-workflows \
  --policy-arn <policy-arn> \
  --max-results 10

# 2. Delete old/completed builds if you have 2 already
aws bedrock delete-automated-reasoning-policy-build-workflow \
  --policy-arn <policy-arn> \
  --build-workflow-id "old-workflow-id" \
  --last-updated-at "2025-11-15T00:41:18.608000+00:00"

# 3. Now start your new build
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn <policy-arn> \
  --build-workflow-type INGEST_CONTENT \
  --source-content <content>
```

## Build Workflow Assets

After a build workflow completes successfully, you can retrieve various assets. After you complete a build workflow, you can ask the user to check the build diff using the Automated Reasoning checks console.

### Asset Types

#### 1. ASSET_MANIFEST - Index of All Assets

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "ASSET_MANIFEST"
```

**What it contains:**
- A manifest listing all available assets and their IDs for the build workflow
- Use this to discover asset IDs needed for retrieving assets

#### 2. POLICY_DEFINITION - The Main Output

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "POLICY_DEFINITION"
```

**What it contains:**
- Compiled policy with extracted/refined rules, variables, and types
- SMT-LIB expressions for all rules
- Complete policy structure ready for deployment

#### 3. BUILD_LOG - Build Process Details

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "BUILD_LOG"
```

**What it shows:**
- Document processing steps - What content was analyzed
- Extraction results - What rules, variables, and types were found
- Processing warnings - Content that couldn't be interpreted
- Success/failure status for each extraction step

#### 4. QUALITY_REPORT - Policy Quality Analysis

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "QUALITY_REPORT"
```

**What it contains:**
- Conflicting rules - Rules that contradict each other
- Unused variables - Variables not referenced by any rules
- Unused type values - Enum values not used in rules
- Disjoint rule sets - Groups of rules that don't interact

#### 5. GENERATED_TEST_CASES - Auto-Generated Tests

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "GENERATED_TEST_CASES"
```

**What it contains:**
- Automatically generated test cases based on the policy rules

#### 6. POLICY_SCENARIOS - Policy Test Scenarios

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "POLICY_SCENARIOS"
```

**What it contains:**
- AI-generated scenarios for comprehensive policy validation

#### 7. FIDELITY_REPORT - Policy Fidelity Analysis

```bash
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "FIDELITY_REPORT"
```

**What it contains:**
- Fidelity analysis results from a GENERATE_FIDELITY_REPORT build workflow

#### 8. SOURCE_DOCUMENT - Original Source Documents

```bash
# Requires --asset-id obtained from the ASSET_MANIFEST
aws bedrock get-automated-reasoning-policy-build-workflow-result-assets \
  --policy-arn "arn:aws:bedrock:region:account:automated-reasoning-policy/policy-id" \
  --build-workflow-id "workflow-123" \
  --asset-type "SOURCE_DOCUMENT" \
  --asset-id "a1b2c3d4-e5f6-4a7b-8c9d-e0f1a2b3c4d5"
```

**What it contains:**
- The original source document used in the build workflow
- The `--asset-id` parameter is required because multiple source documents may have been used
```