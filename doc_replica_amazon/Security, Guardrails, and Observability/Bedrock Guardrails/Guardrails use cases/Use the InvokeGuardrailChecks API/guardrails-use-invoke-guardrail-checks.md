

# Use the InvokeGuardrailChecks API in your application
<a name="guardrails-use-invoke-guardrail-checks"></a>

With the [InvokeGuardrailChecks](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeGuardrailChecks.html) API, you can evaluate user prompts and model responses with specific safeguards such as content filters, prompt attack detection, and sensitive information filters at any point in your application without creating individual guardrail resources. You can use this API in various applications including agentic AI workflows that involve multi-turn conversations where content evaluation is required for each turn. The API is detect-only: it detects undesirable content and returns a numeric score for each safety check so that you can define the threshold and take the required action within your application logic. With these scores, you can build adaptive response logic such as block, bypass, retry, or route for human review based on your custom threshold and your application requirements.

Features of the `InvokeGuardrailChecks` API:
+ **Flexibility** – You can invoke any safety check with the `InvokeGuardrailChecks` API and integrate it anywhere in your application. You can call the API with any safety checks before sending a prompt to the LLM, after receiving the response from the LLM, before executing a tool the model wants to call, after a tool returns a result, or at any other point you want to evaluate content. For example, you might include prompt attack detection for an input prompt along with content moderation with content filters, but check for sensitive information leakage such as PII content with model responses.
+ **No requirement to create resources upfront** – You don't need to create a guardrail resource before you invoke the required safeguards with the API. You don't need to include a `CreateGuardrail` step, and you don't need to track individual guardrail IDs or versions. This is especially valuable for agentic AI workflows where different steps in the loop require different safety postures. You can apply individual safeguards at different steps without creating guardrail resources at each step, which avoids operational overhead.
+ **Detect-only** – The `InvokeGuardrailChecks` API returns findings for each safety check with a numeric score between 0 and 1. The API doesn't block, pass, or redact content. You decide the required action based on your application requirements, such as blocking content, redacting a PII match, or surfacing a warning.
+ **Supported safeguards** – The `InvokeGuardrailChecks` API supports the following safeguards offered by Amazon Bedrock Guardrails:
  + [Block harmful words and conversations with content filters](guardrails-content-filters.md)
  + [Detect prompt attacks with Amazon Bedrock Guardrails](guardrails-prompt-attack.md) – Prompt attack detection is offered as a separate safeguard outside content filters for the `InvokeGuardrailChecks` API. This is different from the `ApplyGuardrail` API where the prompt attack safety check is included as part of content filters.
  + [Remove PII from conversations by using sensitive information filters](guardrails-sensitive-filters.md)

**Topics**
+ [Supported Regions](#guardrails-use-invoke-guardrail-checks-regions)
+ [Concepts: Messages, content block types, and checks](guardrails-use-invoke-guardrail-checks-concepts.md)
+ [Score definitions](guardrails-use-invoke-guardrail-checks-scores.md)
+ [Example configurations, results, and scores](guardrails-use-invoke-guardrail-checks-examples.md)
+ [Using the API](guardrails-use-invoke-guardrail-checks-using.md)
+ [Sample code](guardrails-use-invoke-guardrail-checks-sample-code.md)
+ [Set up permissions](guardrails-use-invoke-guardrail-checks-permissions.md)
+ [Quotas](guardrails-use-invoke-guardrail-checks-quotas.md)

## Supported Regions
<a name="guardrails-use-invoke-guardrail-checks-regions"></a>

The `InvokeGuardrailChecks` API is available in the following AWS Regions:
+ US East (N. Virginia)
+ US East (Ohio)
+ US West (Oregon)
+ Europe (London)
+ Europe (Stockholm)
+ Asia Pacific (Tokyo)
+ Asia Pacific (Sydney)