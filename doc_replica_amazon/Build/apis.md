

# APIs supported by Amazon Bedrock
<a name="apis"></a>

**Inference APIs supported**

Amazon Bedrock provides five main API patterns to perform [inference](inference.md). The APIs are grouped by the service endpoint they use.

**`bedrock-mantle` endpoint**

The `bedrock-mantle.{region}.amazonaws.com` endpoint supports the following APIs:


| **API method** | **Use-case best suited for** | **Key feature** | 
| --- | --- | --- | 
| [Responses API](bedrock-mantle.md) (recommended) | Stateful conversations | Use the Responses API for modern, agentic applications requiring built-in tool use (search, code interpreter), multimodal inputs, and stateful conversations. | 
| [Messages API](inference-messages-api.md) (recommended) | Anthropic-native interface | Use the Messages API for direct access to Anthropic models using the Anthropic-native request and response format. | 
| [Chat Completions](bedrock-mantle.md) | Stateless multi-turn chat | Use the [Chat Completions API](inference-chat-completions.md) for lightweight, stateless, text-focused tasks where you need full control over chat history management and lower latency. | 

**`bedrock-runtime` endpoint**

The `bedrock-runtime.{region}.amazonaws.com` endpoint supports the following APIs:


| **API method** | **Use-case best suited for** | **Key feature** | 
| --- | --- | --- | 
| [Converse](conversation-inference.md) | Multi-turn chat / standardizing | The [Converse API](conversation-inference.md) provides a unified interface for interacting with all models in Amazon Bedrock. | 
| [Invoke](inference-invoke.md) | Single transactions / Large payloads | The Invoke API provides direct access to models with more control over the request and response format. | 
| [Messages API](model-parameters-anthropic-claude-messages.md) | Anthropic-native interface | Use the Messages API via InvokeModel for direct access to Anthropic models using the native request format. | 
| [Chat Completions](inference-chat-completions.md) | Stateless multi-turn chat | Use the Chat Completions API for OpenAI-compatible stateless chat interactions. | 

Read more about the [APIs supported by Amazon Bedrock](inference-api.md).

**Deciding between APIs**

The API you use depends on your use-case.


| **Use Case** | **Recommended API** | 
| --- | --- | 
| Migrating from OpenAI API-compatible endpoint | Use OpenAI-compatible APIs: [Responses API](https://platform.openai.com/docs/api-reference/responses) or [Chat Completions API](inference-chat-completions.md). According to OpenAI, the [recommended](https://platform.openai.com/docs/guides/migrate-to-responses) API long-term is Responses API. | 
| Using models not compatible with OpenAI-compatible endpoint | Use native Amazon Bedrock APIs: [Converse](conversation-inference.md) and [Invoke](inference-invoke.md). For more information, see [Inference using Invoke API](inference-api.md). | 
| Consistent interface across all models | [Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) - Works with all models that support messages. Write code once and use it with different models. For example code, see [Converse API examples](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#message-inference-examples). | 
| Direct model access with full control | [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) - Provides direct access to models with more control over request and response format. Use for generating text, images, and embeddings. For example code, see [Invoke model code examples](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html#inference-example-invoke). | 
| New to Amazon Bedrock | We recommend using open APIs such as [Messages API](model-parameters-anthropic-claude-messages.md), [Chat Completions API](inference-chat-completions.md), or [Responses API](bedrock-mantle.md). These APIs are available on both endpoints, but we recommend the bedrock-mantle endpoint. | 

**Models supported by each API and endpoint**

First, browse our [models](models.md) to decide on the model you want to use. Once you decide on the model you want to use, you can see the APIs it supports and based on that you choose which endpoint to use. The `bedrock-mantle` supports the Responses, Chat Completions, and Messages API. The `bedrock-runtime` supports the Invoke, Converse, Chat Completions, and Messages API. We recommend using the `bedrock-mantle` endpoint whenever possible.