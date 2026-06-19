

# Create your guardrail
<a name="guardrails-components"></a>

Amazon Bedrock Guardrails offers filters that you can configure to help avoid undesirable and harmful content and remove or mask sensitive information for privacy protection. 

You can configure the following filters with Amazon Bedrock Guardrails:
+ **Content filters** — This filter helps you detect and filter harmful text or image content in input prompts or model responses (excluding reasoning content). Filtering is done based on detection of certain predefined harmful content categories: Hate, Insults, Sexual, Violence, Misconduct and Prompt Attack. You can configure the filter strength for each of these categories based on your use cases. With [Standard tier](guardrails-tiers.md), detection of undesirable content is extended to protect against harmful content within code elements including comments, variable and function names, and string literals. 
+ **Prompt attacks** — Offered as a category within content filters, this filter can help you detect and filter prompt attacks including jailbreaks, prompt injections, and prompt leakages (Standard tier only). This capability helps you detect prompts that are intended to bypass content moderation, override instructions, or generate harmful content.
+ **Denied topics** — You can define a set of topics to avoid within your generative AI application. For example, a banking assistant application can be designed to help avoid topics related to illegal investment advice. With [Standard tier](guardrails-tiers.md), content filters extend to code domains.
+ **Word filters** — You can define a set of custom words or phrases (exact match) that you want to detect and block in the interaction between your users and generative AI applications. For example, you can detect and block profanity (using a ready-to-use option) as well as specific custom words such as competitor names, or other offensive words.
+ **Sensitive information filters** — Can help you detect sensitive content such as Personally Identifiable Information (PII) in standard formats or custom regex entities in user inputs and FM responses. This filter is a probabilistic maching learning (ML) based solution that is context dependent. It detects sensitive information based on the context within input prompts or model responses. Based on your use case, you can block or mask inputs and responses containing sensitive information. For example, you can redact users’ personal information while generating summaries from customer and agent conversation transcripts.
+ **Contextual grounding checks** — Can help you detect and filter hallucinations in model responses if they are not grounded (factually inaccurate or add new information) in the source information or are irrelevant to the user’s query. For example, you can block or flag responses in RAG (retrieval-augmented generation) applications, if the model responses deviate from the information in the retrieved passages or doesn’t answer the question from the user.
+ **Automated reasoning checks** — Can help you validate that model responses adhere to logical rules and policies that you define. You can create policies using natural language that specify the reasoning requirements, and Automated reasoning checks will evaluate whether model outputs comply with these logical constraints. For example, you can ensure that a customer service chatbot only recommends products that are available in the inventory, or verify that financial advice follows regulatory compliance rules.

**Note**  
All blocked content from the above policies will appear as plain text in [Amazon Bedrock Model Invocation Logs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html), if you have enabled them. You can disable Amazon Bedrock Invocation Logs if you do not want your blocked content to appear as plain text in the logs.

A guardrail must contain at least one filter and messaging for when prompts and user responses are blocked. You can opt to use the default messaging. You can add filters and iterate on your guardrail later by following the steps at [Modify your guardrail](guardrails-edit.md).

**Topics**
+ [Configure content filters for Amazon Bedrock Guardrails](guardrails-content-filters-overview.md)
+ [Block denied topics to help remove harmful content](guardrails-denied-topics.md)
+ [Remove a specific list of words and phrases from conversations with word filters](guardrails-word-filters.md)
+ [Remove PII from conversations by using sensitive information filters](guardrails-sensitive-filters.md)
+ [Use contextual grounding check to filter hallucinations in responses](guardrails-contextual-grounding-check.md)
+ [Options for handling harmful content detected by Amazon Bedrock Guardrails](guardrails-harmful-content-handling-options.md)
+ [What are Automated Reasoning checks in Amazon Bedrock Guardrails?](guardrails-automated-reasoning-checks.md)
+ [Code domain support](guardrails-code-domain.md)