

# Create your Automated Reasoning policy
<a name="create-automated-reasoning-policy"></a>

When you create an Automated Reasoning policy, your source document is translated into a set of formal logic rules and a schema of variables and types. This page walks you through preparing your document, creating the policy, and reviewing the results.

Amazon Bedrock encrypts your Automated Reasoning policy using AWS Key Management Service (KMS). By default, Amazon Bedrock uses a service-owned key. You can optionally specify a customer managed KMS key for additional control over the encryption of your policy data.

To test and use your Automated Reasoning policy, ensure you have [the appropriate permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrail-automated-reasoning-permissions.html).

## Prepare your source document
<a name="prepare-source-document"></a>

Before you open the console or call the API, prepare the document that Automated Reasoning will use to extract rules and variables. The quality of your policy depends directly on the quality of this input.

### Document structure and clarity
<a name="source-document-structure"></a>

Automated Reasoning checks work best with documents that contain clear, unambiguous rules. Each rule should state a condition and an outcome. Avoid vague language, subjective criteria, or rules that depend on external context not present in the document.

**Example: Clear vs. vague rules**


| Clear (good for extraction) | Vague (poor for extraction) | 
| --- | --- | 
| "Full-time employees with at least 12 months of continuous service are eligible for parental leave." | "Eligible employees may apply for parental leave subject to manager approval." | 
| "Refund requests must be submitted within 30 days of purchase. Items must be in original packaging." | "Refunds are handled on a case-by-case basis." | 

### Size limits and splitting large documents
<a name="source-document-size-limits"></a>

Source documents are limited to 5 MB in size and 50,000 characters. Images and tables in documents also count toward the character limit.

If your document exceeds these limits, or if it covers multiple unrelated domains, split it into focused sections. For example, split an employee handbook into separate documents for leave policies, benefits eligibility, and expense reimbursement. Create your policy with the first section, then use iterative policy building (described later on this page) to merge additional sections into the same policy.

### Pre-process complex documents
<a name="source-document-preprocessing"></a>

Documents that contain a lot of boilerplate, legal disclaimers, or content unrelated to the rules you want to enforce will produce noisy policies with unnecessary variables and rules. Before uploading, consider:
+ Removing headers, footers, table of contents, and appendices that don't contain rules.
+ Extracting only the sections that contain the rules relevant to your use case.
+ Simplifying complex tables into plain text statements where possible.

**Tip**  
Start with a focused subset of your rules. Create and test the policy thoroughly, then gradually add more content in subsequent iterations. This approach helps you identify and resolve issues early and makes troubleshooting easier.

### (Optional) Use an LLM to rewrite documents as logical rules
<a name="preprocess-with-llm"></a>

For documents that contain narrative prose, legal language, or complex formatting, consider using a frontier model with advanced reasoning capabilities to rewrite the content as clear, logical rules before uploading it to Automated Reasoning checks. This one-off preprocessing step converts text into a format that Automated Reasoning checks can extract from more accurately, resulting in higher-quality policies with fewer unused variables and bare assertions.

**Note**  
Always review the LLM's output against your original document before using it as source text.

There are two approaches to LLM preprocessing, depending on the complexity of your document and how much control you want over the extraction.

#### Approach 1: Plain text rule extraction
<a name="preprocess-plain-text"></a>

Ask the LLM to rewrite the document as a numbered list of if-then rules. This approach is straightforward and works well for short, focused documents where the rules are relatively clear in the source.

**Example prompt:**

```
You are a logical reasoning expert. Your task is to analyze the provided
source text and rewrite it as a set of clear, logical rules using if-then
statements.

Instructions:
1. Extract the key relationships, conditions, and outcomes from the source text.
2. Convert these into logical implications using "if-then" format.
3. Use clear, precise language that captures the original meaning.
4. Number each rule for easy reference.
5. Ensure rules are mutually consistent and non-contradictory.

Format:
- Rule [N]: If [condition], then [consequence].
- Use "and" to combine multiple conditions.
- Use "or" for alternative conditions.
- Include negations when relevant: If not [condition], then [consequence].

Example:
Source: "Students who complete all assignments and attend at least 80% of
classes will pass the course."
Rule 1: If a student completes all assignments and attends at least 80% of
classes, then they will pass the course.

Source Text:
[Paste your document here]
```

#### Approach 2: Structured rule extraction
<a name="preprocess-structured"></a>

For complex or lengthy documents, ask the LLM to extract rules as structured JSON with metadata for each rule. This approach produces richer output that helps you audit which parts of the document each rule came from, how confident the extraction is, and which rules are inferred rather than directly stated. It also asks the LLM to generate sanity rules — common-sense boundary constraints such as "age must be non-negative" — which translate directly into the boundary rules that Automated Reasoning policies use. For more information on boundary rules, see [Validate ranges for numerical values](automated-reasoning-policy-best-practices.md#bp-validate-ranges).

**Example prompt:**

```
You are a logical reasoning expert. Extract formal logical rules from the
provided text.

Output Format:
For each rule, provide:
- Rule ID: [unique identifier]
- Conditions: [ALL preconditions — preserve compound conditions with AND/OR/NOT]
- Consequence: [the outcome/action]
- Confidence: [high/medium/low based on text clarity]
- Source Reference: [quote or paraphrase from source]
- Rule Type: [explicit/implicit/sanity]

Critical Guidelines:
1. PRESERVE ALL CONDITIONS: Do not drop or simplify conditions.
2. PRESERVE LOGICAL OPERATORS: Maintain AND, OR, NOT relationships exactly.
3. PRESERVE QUANTIFIERS: Keep "all", "any", "at least", numeric thresholds.
4. PRESERVE EXCEPTIONS: Include "unless", "except when" clauses.
5. Make implicit conditions explicit only when clearly implied by context.
6. Use consistent terminology across rules.
7. Flag ambiguities such as unclear, incomplete, or contradictory statements.
8. Add sanity rules for common-sense constraints:
   - Numeric ranges (e.g., "age must be between 0 and 150")
   - Temporal constraints (e.g., "start date must be before end date")
   - Physical limits (e.g., "quantity cannot be negative")
   - Mutual exclusivity (e.g., "status cannot be both active and inactive")

Output Requirements:
- Produce final JSON only (no text or markdown).
- Use the following JSON keys:
  - "rules" for the rules array
  - "ambiguities" for the ambiguities array

Source Text:
[Paste your document here]
```

After running the structured extraction, review the JSON output. Pay special attention to:
+ Rules with `confidence: low` — these may need manual verification against the source document.
+ Rules with `ruleType: implicit` — these were inferred rather than directly stated. Verify they accurately reflect the intent of the source.
+ The `ambiguities` array — these highlight areas where the source document is unclear and may need rewriting before extraction.

Convert the reviewed JSON rules into plain text if-then statements for use as your source document when creating the Automated Reasoning policy.

## Write effective instructions
<a name="write-effective-instructions"></a>

When creating a policy, you can provide optional instructions that guide how Automated Reasoning processes your source document. While optional, good instructions significantly improve the quality of the extracted rules and variables.

Effective instructions should cover three things:

1. **Describe the use case.** Explain what your application does and what type of content the policy will validate. For example: "This policy will validate an HR chatbot that answers employee questions about leave of absence eligibility."

1. **Describe the types of questions users will ask.** Give examples of realistic user questions. For example: "Users will ask questions like 'Am I eligible for parental leave if I've worked here for 9 months?' or 'How many days of bereavement leave can I take?'"

1. **Focus the extraction.** If your document covers multiple topics, tell Automated Reasoning checks which parts to focus on and which to ignore. For example: "Focus on sections 3 through 5 which cover leave policies. Ignore the general company overview in section 1 and the organizational chart in section 2."

**Example instruction:**

```
This policy will validate HR questions about leave eligibility. The document
has sections on different leave types (parental, medical, bereavement, personal).
Users will ask questions like "Am I eligible for parental leave if I've worked
here for 9 months?" or "Can part-time employees take bereavement leave?"
Focus on the eligibility criteria for each leave type. Capture variables that
help determine whether an employee is eligible for a specific type of leave.
```

## Create a policy in the console
<a name="create-automated-reasoning-policy-console"></a>

1. In the left navigation, choose **Automated Reasoning**, and then choose **Create policy**.

1. Enter a **Name** for the policy.

1. (Optional) Enter a **Description** for the policy.

1. <a name="source-document-step"></a>For **Source**, provide the document that describes the rules and policies of your knowledge domain. Do the following:

   1. For **Ingest method**, do one of the following:

      1. Select **Upload document**, then select **Choose file**. Upload a PDF document of the source content.

      1. Select **Enter text**. Paste or enter your source content.

   1. (Recommended) For **Instructions**, provide guidance on how to process your source document. See [Write effective instructions](#write-effective-instructions) for what to include.

1. (Optional) For **Tags**, choose **Add new tag** to tag your policy.

1. (Optional) For **Encryption**, choose a KMS key to encrypt your policy. You can use the default service-owned key or select a customer managed key.

1. Choose **Create policy**.

**Tip**  
If your application expects a specific set of variables, you can pre-define the schema before importing content. Use the `CreateAutomatedReasoningPolicy` API or CloudFormation to create a policy with a `policyDefinition` that contains your desired variables and types but no rules. Then use [Iterative policy building](#iterative-policy-building) to import your source document. Automated Reasoning will use your predefined schema as a starting point and add rules that reference your variables.

## Create a policy using the API
<a name="create-automated-reasoning-policy-api"></a>

An Automated Reasoning policy is a resource in your AWS account identified by an Amazon Resource Name (ARN). Creating a policy through the API is a two-step process: first create the policy resource, then start a build workflow to extract rules from your document.

### Step 1: Create the policy resource
<a name="create-automated-reasoning-policy-api-step1"></a>

Use the `CreateAutomatedReasoningPolicy` API to create the policy resource.

`name` (required)  
The name of the policy. Must be unique within your AWS account and Region.

`description` (optional)  
A description of the policy's purpose.

`policyDefinition` (optional)  
An initial policy definition with rules, variables, and custom types. Use this if you already have a schema you want to start from.

`kmsKeyId` (optional)  
The KMS key identifier for encrypting the policy. If not specified, Amazon Bedrock uses a service-owned key.

`tags` (optional)  
Tags to associate with the policy.

`clientRequestToken` (optional)  
An idempotency token to ensure the operation completes no more than once.

**Example:**

```
aws bedrock create-automated-reasoning-policy \
  --name "{{MyHRPolicy}}" \
  --description "{{Validates HR chatbot responses about leave eligibility}}" \
  --kms-key-id arn:aws:kms:{{us-east-1}}:{{111122223333}}:key/{{12345678-1234-1234-1234-123456789012}}
```

Example response:

```
{
  "createdAt": "2025-07-21T14:43:52.692Z",
  "definitionHash": "f16ba1ceca36e1d21adce559481add6a...",
  "name": "MyHRPolicy",
  "policyArn": "arn:aws:bedrock:us-east-1:111122223333:automated-reasoning-policy/lnq5hhz70wgk",
  "updatedAt": "2025-07-21T14:43:52.692Z",
  "version": "DRAFT"
}
```

### Step 2: Start a build workflow to extract rules
<a name="create-automated-reasoning-policy-api-step2"></a>

Use the `StartAutomatedReasoningPolicyBuildWorkflow` API with the policy ARN from step 1 to extract rules and variables from your source document.

`policyArn` (required)  
The ARN of the policy resource created in step 1.

`buildWorkflowType` (required)  
Set to `INGEST_CONTENT` to extract rules from a document. You can also use `INGEST_CONTENT` to merge the content extracted from a document into an existing policy: include the current policy definition in `sourceContent` alongside the new document, and the extracted rules, variables, and types are composed into the existing definition rather than replacing it. See [Iterative policy building](#iterative-policy-building).

`sourceContent` (required)  
Contains the document to process and an optional starting policy definition.

**Example:**

```
# Encode your PDF to base64
PDF_BASE64=$(base64 -i {{your-policy.pdf}} | tr -d '\n')

# Start the build workflow
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}} \
  --build-workflow-type INGEST_CONTENT \
  --source-content "{
    \"policyDefinition\": {
      \"version\": \"1.0\",
      \"types\": [],
      \"rules\": [],
      \"variables\": []
    },
    \"workflowContent\": {
      \"documents\": [
        {
          \"document\": \"$PDF_BASE64\",
          \"documentContentType\": \"pdf\",
          \"documentName\": \"{{HR Leave Policy}}\",
          \"documentDescription\": \"{{Validates HR chatbot responses about leave eligibility. Users ask questions like 'Am I eligible for parental leave?'}}\"
        }
      ]
    }
  }"
```

**Note**  
In the `policyDefinition` object, the `version` field is required and must be set to `1.0`. It identifies the version of the policy definition schema, and is distinct from the policy resource version (`DRAFT` or a numbered version).

Example response:

```
{
  "policyArn": "arn:aws:bedrock:us-east-1:111122223333:automated-reasoning-policy/lnq5hhz70wgk",
  "buildWorkflowId": "d40fa7fc-351e-47d8-a338-53e4b3b1c690"
}
```

Check the build status with `ListAutomatedReasoningPolicyBuildWorkflows`:

```
aws bedrock list-automated-reasoning-policy-build-workflows \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}
```

## Review the extracted policy
<a name="review-extracted-policy"></a>

After a build completes, review the extracted policy definition before you start testing. Catching issues at this stage saves time compared to discovering them through failed tests later.

In the console, open your policy and go to the **Definitions** page. Via the API, use `GetAutomatedReasoningPolicyBuildWorkflowResultAssets` with `--asset-type POLICY_DEFINITION` to retrieve the extracted definition, and `--asset-type QUALITY_REPORT` to retrieve the quality report. You can see a full list of the assets produced during the workflow, such as the fidelity report, using the `--asset-type ASSET_MANIFEST` parameter.

Check for the following issues:

1. **Unused variables.** In the console, look for warning indicators next to variables. These flag variables that aren't referenced by any rules. Delete unused variables — they add noise to the translation process and can cause `TRANSLATION_AMBIGUOUS` results. In the API, unused variables are listed in the `QUALITY_REPORT` asset.

1. **Duplicate or near-duplicate variables.** Scan the variable list for variables with overlapping meanings, such as `tenureMonths` and `monthsOfService`. Duplicate variables confuse the translation process because Automated Reasoning checks can't determine which one to use for a given concept. Merge or delete duplicates.

1. **Bare assertions (rules not in if-then format).** Skim the rules and look for rules that aren't in if-then format, such as `(= eligibleForParentalLeave true)`. Bare assertions create axioms — statements that are always true — which make certain conditions logically impossible and lead to unexpected `IMPOSSIBLE` results during validation. Rewrite them as conditionals (for example, `(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)`) or delete them. Bare assertions are appropriate only for boundary conditions like `(>= accountBalance 0)`.

1. **Conflicting rules.** The quality report flags rules that contradict each other. Conflicting rules cause your policy to return `IMPOSSIBLE` for all validation requests that involve the conflicting rules. Resolve conflicts by merging the rules or deleting one of them.

1. **Missing rules or variables.** Compare the extracted policy against your source document. If important rules or concepts are missing, you can add them manually or re-create the policy with better instructions.

**Tip**  
The quality report also identifies disjoint rule sets — groups of rules that don't share any variables. Disjoint rule sets aren't necessarily a problem (your policy may cover independent topics), but they can indicate that variables are missing connections between related rules.

## Review the fidelity report
<a name="review-fidelity-report"></a>

When you create a policy from a source document, a fidelity report is automatically generated alongside the extracted policy. The fidelity report measures how accurately the policy represents your source content and provides detailed grounding that links each rule and variable back to specific statements in the document. For more information about fidelity report concepts, see [Fidelity report](automated-reasoning-checks-concepts.md#ar-concept-fidelity-report).

### Review the fidelity report in the console
<a name="review-fidelity-report-console"></a>

In the console, open your policy and choose the **Source Document** tab (next to **Definitions**). The **Source Content** view displays each atomic statement extracted from your document as a numbered row in a table. Each row shows:
+ The statement number and extracted text.
+ The source **Document** the statement came from.
+ The number of **Rules** grounded by that statement.
+ The number of **Variables** grounded by that statement.

Use the **Rules** and **Variables** dropdown filters to focus on statements that ground a specific rule or variable. Use the search bar to find specific content within the extracted statements.

If you edit the policy after the initial extraction — for example, by modifying rules or adding variables — choose the **Regenerate** button to update the fidelity report so it reflects your current policy definition.

### Review the fidelity report using the API
<a name="review-fidelity-report-api"></a>

Use `GetAutomatedReasoningPolicyBuildWorkflowResultAssets` with `--asset-type FIDELITY_REPORT` to retrieve the fidelity report. To regenerate the report after making policy changes, use `StartAutomatedReasoningPolicyBuildWorkflow` with the build workflow type `GENERATE_FIDELITY_REPORT` and provide the source documents in the `generateFidelityReportContent` field. The workflow re-analyzes the documents against the current policy definition and produces a new fidelity report. You can also retrieve the original source documents from a previous build workflow using `--asset-type SOURCE_DOCUMENT` with the `--asset-id` parameter (obtain the asset ID from the asset manifest).

### What to look for
<a name="review-fidelity-report-checklist"></a>

When reviewing the fidelity report from the APIs, pay attention to:
+ **Low coverage score.** A low coverage score indicates that significant portions of your source document were not captured in the policy. Look for statements with 0 rules and 0 variables in the source content view to identify which parts of the document were missed, and consider using iterative policy building to add the missing content. See [Iterative policy building](#iterative-policy-building).
+ **Low accuracy score on individual rules.** Each rule has its own accuracy score and justification. Rules with low accuracy scores may not faithfully represent the source material. Use the **Rules** filter to isolate the grounding statements for a specific rule and compare them against the rule's formal logic to identify misinterpretations.
+ **Ungrounded rules or variables.** Rules or variables that lack grounding statements may have been inferred rather than directly extracted from the document. Verify that these are correct or remove them if they don't reflect your intent.

**Tip**  
The fidelity report is especially useful for collaboration with domain experts who authored the source document. Share the **Source Document** view with them so they can verify that the policy correctly captures their intent without needing to read the formal logic rules directly.

## Iterative policy building
<a name="iterative-policy-building"></a>

For complex domains, build your policy incrementally rather than trying to capture everything in a single document upload. Start with a focused subset of your rules, create and test the policy, then add more content in subsequent iterations.

### Add content in the console
<a name="iterative-building-console"></a>

1. Open your Automated Reasoning policy in the console.

1. On the **Definitions** page, choose **Import**.

1. Select the option to merge the new content with the existing policy definition.

1. Upload or paste the additional source content.

1. Review the updated policy definition and resolve any new conflicts or duplicates.

### Add content using the API
<a name="iterative-building-api"></a>

Call `StartAutomatedReasoningPolicyBuildWorkflow` with `INGEST_CONTENT`, passing the complete current policy definition alongside the new document. You must include the full existing definition — rules, variables, and types — so that the new content is merged with the existing policy rather than replacing it.

```
# First, retrieve the current policy definition
aws bedrock get-automated-reasoning-policy \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}

# Encode the new document
PDF_BASE64=$(base64 -i {{additional-rules.pdf}} | tr -d '\n')

# Start a build workflow with the existing definition + new document
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}} \
  --build-workflow-type INGEST_CONTENT \
  --source-content "{
    \"policyDefinition\": {{EXISTING_POLICY_DEFINITION_JSON}},
    \"workflowContent\": {
      \"documents\": [
        {
          \"document\": \"$PDF_BASE64\",
          \"documentContentType\": \"pdf\",
          \"documentName\": \"{{Additional Benefits Rules}}\",
          \"documentDescription\": \"{{Additional rules covering medical and bereavement leave eligibility.}}\"
        }
      ]
    }
  }"
```

**Important**  
The API supports a maximum of 2 build workflows per policy, with only 1 allowed to be `IN_PROGRESS` at any time. If you need to start a new build and already have 2 workflows, delete an old one first using `DeleteAutomatedReasoningPolicyBuildWorkflow`.

### Import a policy definition using the API
<a name="import-policy-api"></a>

If you already have a policy definition in JSON format, use `StartAutomatedReasoningPolicyBuildWorkflow` with `IMPORT_POLICY` to import it directly. This skips the document extraction step and loads the definition as-is.

```
aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}} \
  --build-workflow-type IMPORT_POLICY \
  --source-content "{
    \"policyDefinition\": {
      \"version\": \"1.0\",
      \"variables\": [
        {
          \"name\": \"isFullTime\",
          \"type\": \"BOOL\",
          \"description\": \"Whether the employee works full-time.\"
        }
      ],
      \"rules\": [
        {
          \"id\": \"{{A1B2C3D4E5F6}}\",
          \"expression\": \"(=> isFullTime eligibleForBenefits)\"
        }
      ],
      \"types\": []
    }
  }"
```

### Iteratively refine a policy using the API
<a name="iteratively-refine-policy-api"></a>

Use `StartAutomatedReasoningPolicyBuildWorkflow` with `ITERATIVELY_REFINE_POLICY` to refine an existing policy using a source document and optional natural language feedback. Unlike `INGEST_CONTENT` which extracts new rules from a document, this workflow uses the document as context to improve the existing policy. Common use cases include:
+ **Fixing failed tests.** When a test returns unexpected results, provide the source document and feedback describing the expected behavior to refine the policy rules.
+ **Addressing feedback about missing concepts.** Provide natural language feedback about concepts that are not currently captured in the policy, along with the source document as context.
+ **Updating after source document changes.** When the source document is revised, provide the updated document and describe the specific changes to incorporate.

`policyDefinition` (required)  
The complete current policy definition to refine.

`workflowContent.iterativeRefinementContent.documents` (required)  
The source document to use as context for the refinement.

`workflowContent.iterativeRefinementContent.feedback` (optional)  
Natural language instructions describing the specific changes or improvements you want. For example, "Add rules for bereavement leave eligibility" or "Update the tenure threshold from 12 months to 6 months based on the new policy revision."

```
# Encode your updated policy document
PDF_BASE64=$(base64 -i {{updated-policy.pdf}} | tr -d '\n')

aws bedrock start-automated-reasoning-policy-build-workflow \
  --policy-arn arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}} \
  --build-workflow-type ITERATIVELY_REFINE_POLICY \
  --source-content "{
    \"policyDefinition\": {{EXISTING_POLICY_DEFINITION_JSON}},
    \"workflowContent\": {
      \"iterativeRefinementContent\": {
        \"documents\": [
          {
            \"document\": \"$PDF_BASE64\",
            \"documentContentType\": \"pdf\",
            \"documentName\": \"{{Updated HR Policy v2}}\",
            \"documentDescription\": \"{{Revised HR leave policy with updated eligibility criteria.}}\"
          }
        ],
        \"feedback\": \"{{Update the tenure requirement for parental leave from 12 months to 6 months, as specified in section 3 of the revised document.}}\"
      }
    }
  }"
```

**Tip**  
Use `ITERATIVELY_REFINE_POLICY` when your source document has been updated and you want the policy to reflect the changes, or when you want to guide the refinement with specific instructions. Use `INGEST_CONTENT` instead when you want to add entirely new content from a new document.

## KMS permissions for Automated Reasoning policies
<a name="automated-reasoning-policy-kms-permissions"></a>

If you specify a customer managed KMS key to encrypt your Automated Reasoning policy, you must configure permissions that allow Amazon Bedrock to use the key on your behalf.

### Key policy permissions
<a name="automated-reasoning-policy-key-policy"></a>

Add the following statement to your KMS key policy to allow Amazon Bedrock to use the key for Automated Reasoning policies:

```
{
  "Sid": "PermissionsForAutomatedReasoningPolicy",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::{{111122223333}}:user/{{role}}"
  },
  "Action": [
    "kms:Decrypt",
    "kms:DescribeKey",
    "kms:GenerateDataKey"
  ],
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "kms:EncryptionContext:aws:bedrock:automated-reasoning-policy": [
        "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{policy-id}}",
        "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{policy-id}}:*"
      ],
      "kms:ViaService": "bedrock.{{us-east-1}}.amazonaws.com"
    }
  }
}
```

### IAM permissions
<a name="automated-reasoning-policy-iam-permissions"></a>

Your IAM principal must have the following permissions to use a customer managed KMS key with Automated Reasoning policies:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowKMSForAutomatedReasoningPolicy",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:{{us-east-1}}:{{111122223333}}:key/{{key-id}}",
      "Condition": {
        "StringEquals": {
          "kms:EncryptionContext:aws:bedrock:automated-reasoning-policy": [
            "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{policy-id}}",
            "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{policy-id}}:*"
          ],
          "kms:ViaService": "bedrock.{{us-east-1}}.amazonaws.com"
        }
      }
    }
  ]
}
```

### Encryption context
<a name="automated-reasoning-policy-encryption-context"></a>

Amazon Bedrock uses encryption context to provide additional security for your Automated Reasoning policies. The encryption context is a set of key-value pairs used as additional authenticated data when encrypting and decrypting your policy.

For Automated Reasoning policies, Amazon Bedrock uses the following encryption context:
+ **Key:** `aws:bedrock:automated-reasoning-policy`
+ **Value:** The Amazon Resource Name (ARN) of your Automated Reasoning policy