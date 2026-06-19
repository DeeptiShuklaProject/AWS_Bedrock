

# Cohere models
<a name="model-parameters-cohere"></a>

This section describes the request parameters and response fields for Cohere models. Use this information to make inference calls to Cohere models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Cohere models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific Cohere model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Cohere models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Cohere models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Cohere models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Cohere models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Cohere specific prompt information, see the [Cohere prompt engineering guide](https://txt.cohere.com/how-to-train-your-pet-llm-prompt-engineering).

**Topics**
+ [Cohere Command models](model-parameters-cohere-command.md)
+ [Cohere Embed and Cohere Embed v4 models](model-parameters-embed.md)
+ [Cohere Command R and Command R\+ models](model-parameters-cohere-command-r-plus.md)