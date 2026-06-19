

# Mistral AI models
<a name="model-parameters-mistral"></a>

This section describes the request parameters and response fields for Mistral AI models. Use this information to make inference calls to Mistral AI models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Mistral AI models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific Mistral AI model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Mistral AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Mistral AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Mistral AI models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Mistral AI models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Mistral AI specific prompt information, see the [Mistral AI prompt engineering guide](https://docs.mistral.ai/guides/prompting_capabilities/).

**Topics**
+ [Mistral AI text completion](model-parameters-mistral-text-completion.md)
+ [Mistral AI chat completion](model-parameters-mistral-chat-completion.md)
+ [Mistral AI Large (24.07) parameters and inference](model-parameters-mistral-large-2407.md)
+ [Pixtral Large (25.02) parameters and inference](model-parameters-mistral-pixtral-large.md)