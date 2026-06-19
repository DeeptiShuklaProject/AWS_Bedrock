

# Configure response generation for reasoning models with Knowledge Bases
<a name="kb-test-configure-reasoning"></a>

Certain foundation models can perform model reasoning, where they take a larger, complex task and break it down into smaller, simpler steps. This process, often referred to as chain of thought (CoT) reasoning, can improve model accuracy by giving the model a chance to think before it responds. Model reasoning is most useful for task such as multi-step analysis, math problems, and complex reasoning tasks. For more information, see [Enhance model responses with model reasoning](inference-reasoning.md).

**Note**  
This page describes how to use the reasoning configuration specifically for Amazon Bedrock Knowledge Bases. For information about configuring reasoning for direct model invocation using the `InvokeModel` API, see [Enhance model responses with model reasoning](inference-reasoning.md).

When model reasoning is enabled, it can result in improved accuracy with better citation results but can result in a latency increase. The following are some considerations when you query the data sources and generate responses using reasoning models with Amazon Bedrock Knowledge Bases.

**Topics**
+ [Reasoning models](#kb-test-reasoning-models)
+ [Using model reasoning for Claude 3.7 Sonnet](#kb-test-reasoning-using)
+ [General considerations](#kb-test-reasoning-general-considerations)
+ [Retrieve and generate API considerations](#kb-test-reasoning-api-considerations)

## Reasoning models
<a name="kb-test-reasoning-models"></a>

To see which models support reasoning, please visit [models at a glance](model-cards.md) and choose the model you are interested in.

## Using model reasoning for Claude 3.7 Sonnet
<a name="kb-test-reasoning-using"></a>

**Note**  
Model reasoning is always enabled for the DeepSeek-R1 model. The model does not support toggling the reasoning capability on and off.

When using the Claude 3.7 Sonnet model, model reasoning can be enabled or disabled using the `additionalModelRequestFields` parameter of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) API. This parameter accepts any key-value pairs. For example, you can add a `reasoningConfig` field and use a `type` key to enable or disable reasoning, as shown below.

```
{
   "input": { 
      "text": "string",
      "retrieveAndGenerateConfiguration": { 
      "knowledgeBaseConfiguration": { 
         "generationConfiguration": { 
            "additionalModelRequestFields": {
                "reasoningConfig" : {
                    "type": "enabled",
                    "budget_tokens": INT_VAL, #required when enabled
                }
            }
         },
         "knowledgeBaseId": "string",
      },
      "type": "string"
   },
   "sessionId": "string"
}
```

## General considerations
<a name="kb-test-reasoning-general-considerations"></a>

The following are some general considerations for using the reasoning models for Knowledge Bases.
+ The reasoning models will have up to five minutes to respond to a query. If the model takes more than five minutes to respond to the query, it results in a time out.
+ To avoid exceeding the five-minute timeout, model reasoning is enabled only at the generation step when you configure your queries and response generation. The orchestration step cannot have model reasoning.
+ The reasoning models can use up to 8192 tokens to respond to queries, which will include both the output and thinking tokens. Any request that has a request for maximum number of output tokens greater than this limit will result in an error.

## Retrieve and generate API considerations
<a name="kb-test-reasoning-api-considerations"></a>

The following are some considerations when using the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) API for the reasoning models.
+ By default, when reasoning is disabled for all models including the Claude 3.7 Sonnet, the temperature is set to zero. When reasoning is enabled, the temperature must be set to one.

  ```
  "inferenceConfig": {
      "textInferenceConfig": {
          "maxTokens": 8192,
          "temperature": 1
      }
  }
  ```
+ The parameter, Top P, must be disabled when reasoning is enabled for the Claude 3.7 Sonnet model. Top P is an additional model request field that determines the percentile of possible tokens to select from during generation. By default, the Top P value for other Anthropic Claude models is one. For the Claude 3.7 Sonnet model, this value will be disabled by default.
+ When model reasoning is in use, it can result in an increase in latency. When using this API operation and the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerateStream.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerateStream.html) API operation, you might notice a delay in receiving the response from the API.