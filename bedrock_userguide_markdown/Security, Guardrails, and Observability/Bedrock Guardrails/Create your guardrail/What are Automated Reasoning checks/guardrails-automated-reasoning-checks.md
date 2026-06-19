

# What are Automated Reasoning checks in Amazon Bedrock Guardrails?
<a name="guardrails-automated-reasoning-checks"></a>

## What Automated Reasoning checks do
<a name="automated-reasoning-what-it-does"></a>

A key challenge with large language models (LLMs) is ensuring the accuracy of their responses. Without validation, LLMs can produce hallucinations or inaccurate information that undermines trust. Automated Reasoning checks in Amazon Bedrock Guardrails help solve this problem by using mathematical techniques to validate natural language content against policies you define.

Unlike traditional guardrail components that block or filter content based on pattern matching, Automated Reasoning checks uses formal logic to provide structured feedback about *why* a response is correct or incorrect. This feedback can be used to steer an LLM towards generating content that is provably consistent with your policy. Specifically, Automated Reasoning checks can:
+ **Detect factually incorrect statements** in LLM responses by mathematically proving that generated content contradicts your policy rules.
+ **Highlight unstated assumptions** where a response is consistent with your policy but doesn't address all relevant rules, indicating the response may be incomplete.
+ **Provide mathematically verifiable explanations** for why accurate statements are correct, citing the specific policy rules and variable assignments that support the conclusion.

These capabilities make Automated Reasoning checks different from other Amazon Bedrock Guardrails components. Content filters and topic policies act as binary gates — they block or allow content. Automated Reasoning checks act as a verification layer that provides detailed, actionable feedback you can use to improve responses programmatically.

## When to use Automated Reasoning checks
<a name="automated-reasoning-when-to-use"></a>

Automated Reasoning checks are most valuable when you need to demonstrate the factual basis for an LLM's response. Consider using them when your application involves:
+ **Regulated industries** such as healthcare, human resources, and financial services, where incorrect information can have legal or compliance consequences.
+ **Complex rule sets** such as mortgage approvals, zoning laws, insurance eligibility, or employee benefits, where multiple conditions interact to determine an outcome.
+ **Compliance scenarios** that require auditable AI responses with mathematically verifiable proof that the response is consistent with your policies.
+ **Customer-facing applications** where incorrect guidance could erode trust, such as chatbots that answer questions about company policies, product eligibility, or service terms.

## What Automated Reasoning checks don't do
<a name="automated-reasoning-what-it-doesnt-do"></a>

To set the right expectations, be aware of the following limitations:
+ **No prompt injection protection.** Automated Reasoning checks validate exactly what you send them. If malicious or manipulated content is provided as input, the validation is performed on that content as-is. To detect and block prompt injection attacks, use [Content filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html#guardrails-content-filters) in combination with Automated Reasoning checks.
+ **No off-topic detection.** Automated Reasoning only analyzes text that is relevant to the policy. It ignores unrelated content and cannot tell you whether a response is off-topic. To detect off-topic responses, use [topic policies](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html#guardrails-topic-policies).
+ **No streaming support.** Automated Reasoning checks do not support streaming APIs. You must validate complete responses.
+ **English only.** Automated Reasoning checks currently support English (US) only.
+ **Scope limited to your policy.** A `VALID` result guarantees validity only for the parts of the input captured through policy variables. Statements that fall outside the scope of your policy's variables are not validated. For example, "I can submit my homework late because I have a fake doctor's note" might be deemed valid if the policy has no variable to capture whether the doctor's note is fake.

Automated Reasoning checks complement other Amazon Bedrock Guardrails features like content filters and topic policies. For the best protection, use them together. For more information, see [Guardrail components](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html).

## End-to-end workflow overview
<a name="automated-reasoning-workflow-overview"></a>

Using Automated Reasoning checks involves four phases: creating a policy, testing it, deploying it in a guardrail, and integrating it into your application.

```
Source Document ──► Extracted Policy ──► Testing ──► Deployment ──► Integration
    (rules)          (formal logic)      (verify)    (guardrail)    (validate responses
                                                                     and act on feedback)
```

1. **Create a policy.** Upload a source document that contains the rules you want to enforce. Automated Reasoning extracts formal logic rules and a schema of variables from your document. A fidelity report is automatically generated that measures how accurately the extracted policy represents your source documents, with coverage and accuracy scores and detailed grounding that links each rule and variable back to the specific statements in your source content. Review the extracted policy and fidelity report to ensure the policy captures your rules correctly. For more information, see [Create your Automated Reasoning policy](create-automated-reasoning-policy.md).

1. **Test and refine.** Tests helps ensure that your policy can accurately validate generated content even while you make changes to the policy itself. Create tests that mimic the questions your users will ask and the responses your LLM might generate. Automated Reasoning checks uses foundational models to translation natural language to logic. Use generated scenarios to validate rule correctness and QnA tests to validate the natural language to logic translation accuracy. Refine your policy based on test results. For more information, see [Test an Automated Reasoning policy](test-automated-reasoning-policy.md).

1. **Deploy.** Save an immutable version of your tested policy and attach it to a guardrail. You can automate deployment using CloudFormation or CI/CD pipelines. For more information, see [Deploy your Automated Reasoning policy in your application](deploy-automated-reasoning-policy.md).

1. **Integrate.** At runtime, Automated Reasoning findings are returned through APIs that supports a Amazon Bedrock Guardrails configuration: `Converse`, `InvokeModel`, `InvokeAgent`, and `RetrieveAndGenerate`, as well as the standalone `ApplyGuardrail` API. Inspect the findings to decide whether to serve the response, rewrite it using the feedback, or ask the user for clarification. Automated Reasoning checks operate in *detect mode* only — they return findings and feedback rather than blocking content. For more information on how to integrate Automated Reasoning checks in your application, see [Integrate Automated Reasoning checks in your application](integrate-automated-reasoning-checks.md). For more information on the permissions required to enable Automated Reasoning checks, see [Permissions for Automated Reasoning policies with ApplyGuardrail](guardrail-automated-reasoning-permissions.md).

## Availability and language support
<a name="automated-reasoning-availability"></a>

Automated Reasoning checks in Amazon Bedrock Guardrails is generally available in the following Regions:
+ US East (N. Virginia)
+ US West (Oregon)
+ US East (Ohio)
+ EU (Frankfurt)
+ EU (Paris)
+ EU (Ireland)

Automated Reasoning checks currently support English (US) only.

## Limitations and considerations
<a name="automated-reasoning-limitations"></a>

Before implementing Automated Reasoning checks, be aware of these technical limitations:
+ **Document complexity.** Source documents should be well-structured with clear, unambiguous rules. Highly complex documents with nested conditions or contradictory statements may not extract cleanly into formal logic. Input documents are limited to 5 MB in size and 50,000 characters. You can split larger documents and merge each section into your policy. Images and tables in documents also impact the number of input characters.
+ **Processing time.** Automated Reasoning checks validation adds latency to your application responses. Plan for additional processing time, especially for complex policies with many variables. The number of variables in a policy directly contributes to increases in validation latency.
+ **Policy scope.** To create policies that are easier to maintain, each policy should focus on a specific domain (for example, HR, finance, legal) rather than trying to cover multiple unrelated areas in a single policy.
+ **Variable and rules limits.** Policies with excessive numbers of variables or overly complex rule interactions may hit processing limits or return TOO\_COMPLEX results. See [Amazon Bedrock limits documentation](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) and [Validation results reference](automated-reasoning-checks-concepts.md#ar-concept-validation-results).
+ **Natural language dependency.** The accuracy of validation depends on how well natural language in user prompts and model responses can be translated to your policy's formal logic variables. Automated Reasoning checks use foundational models to translate natural language into logic representations. Variable descriptions influence the quality of this translation.
+ **Non-linear arithmetic.** Automated Reasoning checks might timeout or return TOO\_COMPLEX if constraints involve reasoning with non-linear arithmetic (for example, irrational numbers or exponents).

## Pricing
<a name="automated-reasoning-pricing"></a>

Automated Reasoning checks in Amazon Bedrock Guardrails are charged based on the number of validation requests processed. For current pricing information, see the [Amazon Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/).

Charges are incurred for each validation request, regardless of the result (for example, VALID, INVALID, TRANSLATION\_AMBIGUOUS). To optimize costs:
+ Use appropriate confidence thresholds to balance accuracy with processing requirements.
+ Consider caching validation results for identical or similar queries when appropriate for your use case.
+ Monitor usage patterns and adjust policies to reduce unnecessary validation requests.

## Cross-region inference for policy operations
<a name="automated-reasoning-cross-region-inference"></a>

Automated Reasoning uses cross-region inference to optimize the performance and availability of policy creation and testing operations. Specific API operations automatically distribute processing across AWS Regions within your geographic boundary to ensure reliable service delivery.

The following Automated Reasoning API operations employ cross-region inference:
+ `StartAutomatedReasoningPolicyBuildWorkflow` — Invoked during policy creation and compilation from source documents.
+ `StartAutomatedReasoningPolicyTestWorkflow` — Invoked during policy validation and testing procedures.

These operations invoke large language models to extract formal logic rules from source documents and translate natural language constructs into structured logical representations. To ensure optimal performance and availability, request processing is distributed according to the following geographic routing:
+ **United States Regions:** API requests originating from US East (N. Virginia), US West (Oregon), or US East (Ohio) may be processed in any supported US Region.
+ **European Union Regions:** API requests originating from EU (Frankfurt), EU (Paris), or EU (Ireland) may be processed in any supported EU Region.

**Important**  
Customer data remains within the originating geographic boundary (United States or European Union) and is processed in accordance with AWS data residency commitments. Cross-region inference routes requests exclusively within the same geographic Region to optimize performance and service availability.

Cross-region inference operates transparently without requiring customer configuration. API functionality remains consistent regardless of the specific Region that processes the request.

**Topics**
+ [What Automated Reasoning checks do](#automated-reasoning-what-it-does)
+ [When to use Automated Reasoning checks](#automated-reasoning-when-to-use)
+ [What Automated Reasoning checks don't do](#automated-reasoning-what-it-doesnt-do)
+ [End-to-end workflow overview](#automated-reasoning-workflow-overview)
+ [Availability and language support](#automated-reasoning-availability)
+ [Limitations and considerations](#automated-reasoning-limitations)
+ [Pricing](#automated-reasoning-pricing)
+ [Cross-region inference for policy operations](#automated-reasoning-cross-region-inference)
+ [Automated Reasoning checks concepts](automated-reasoning-checks-concepts.md)
+ [Create your Automated Reasoning policy](create-automated-reasoning-policy.md)
+ [Automated Reasoning policy best practices](automated-reasoning-policy-best-practices.md)
+ [Test an Automated Reasoning policy](test-automated-reasoning-policy.md)
+ [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md)
+ [Use Kiro CLI with an Automated Reasoning policy](kiro-cli-automated-reasoning-policy.md)
+ [Deploy your Automated Reasoning policy in your application](deploy-automated-reasoning-policy.md)
+ [Integrate Automated Reasoning checks in your application](integrate-automated-reasoning-checks.md)