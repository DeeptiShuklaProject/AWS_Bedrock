

# Build
<a name="build"></a>

This section covers how to interact with Amazon Bedrock programmatically. Choose an endpoint, pick an API, and start making inference requests.

**Quick start**


| **Your situation** | **Recommended path** | 
| --- | --- | 
| Use OpenAI APIs | Use the bedrock-mantle endpoint with the [Responses API](bedrock-mantle.md) | 
| Use Anthropic APIs | Use the Messages API (available on both bedrock-mantle and bedrock-runtime; we recommend bedrock-mantle) | 
| Want a unified AWS-native interface across all models | Use the bedrock-runtime endpoint with the [Converse API](conversation-inference.md) | 
| Need direct model control or non-text modalities | Use the bedrock-runtime endpoint with the [Invoke API](inference-invoke.md) | 

**Topics**
+ [Endpoints supported by Amazon Bedrock](endpoints.md)
+ [APIs supported by Amazon Bedrock](apis.md)
+ [Making inference requests](inference.md)
+ [Use a tool to complete an Amazon Bedrock model response](tool-use.md)
+ [Projects (OpenAI-compatible)](projects.md)
+ [Workspaces (Anthropic-compatible)](workspaces.md)
+ [API keys](api-keys.md)