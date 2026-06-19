

# Prerequisites for using Amazon Bedrock Guardrails
<a name="guardrails-prereq"></a>

Before you can use Amazon Bedrock Guardrails, you must fulfill the following prerequisites:

1. Ensure that your IAM role has the [necessary permissions to perform actions related to Amazon Bedrock Guardrails](guardrails-permissions.md).

Before creating your guardrail, consider preparing the following in advance:
+ Look at the available [content filters](guardrails-content-filters.md) and determine the strength that you want to apply to each filter for prompts and model responses.
+ Determine the [topics to block](guardrails-denied-topics.md), consider how to define them, and decide which sample phrases to include. Describe and define the topic in a precise and concise manner. When you define denied topics, avoid using instructions or negative definitions.
+ Prepare a list of words and phrases (each up to three words) to block with [word filters](guardrails-word-filters.md). Your list can contain up to 10,000 items and be up to 50 KB. Save the list in a .txt or .csv file. If you prefer, you can import it from an Amazon S3 bucket using the Amazon Bedrock console.
+ Look at the list of personally identifiable information in [Remove PII from conversations by using sensitive information filters](guardrails-sensitive-filters.md) and consider which ones your guardrail should block or mask.
+ Consider regex expressions that might match sensitive information and consider which ones your guardrail should block or mask with the use of [Sensitive information filters](guardrails-sensitive-filters.md).
+ Develop the messages to send to users when the guardrail blocks a prompt or model response.