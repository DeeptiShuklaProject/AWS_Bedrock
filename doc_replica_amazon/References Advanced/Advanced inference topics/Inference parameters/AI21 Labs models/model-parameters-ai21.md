

# AI21 Labs models
<a name="model-parameters-ai21"></a>

This section describes the request parameters and response fields for AI21 Labs models. Use this information to make inference calls to AI21 Labs models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call AI21 Labs models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific AI21 Labs model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that AI21 Labs models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the AI21 Labs models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that AI21 Labs models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with AI21 Labs models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For AI21 Labs specific prompt information, see the [AI21 Labs prompt engineering guide](https://docs.ai21.com/docs/prompt-engineering).

**Topics**
+ [AI21 Labs Jurassic-2 models](model-parameters-jurassic2.md)
+ [AI21 Labs Jamba models](model-parameters-jamba.md)