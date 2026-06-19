

# Amazon Titan models
<a name="model-parameters-titan"></a>

This section describes the request parameters and response fields for Amazon Titan models. Use this information to make inference calls to Amazon Titan models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Amazon Titan models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if the Converse API supports a specific Amazon Titan model, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Amazon Titan models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Amazon Titan models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Amazon Titan models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Amazon Titan models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). 

**Topics**
+ [Amazon Titan Text models](model-parameters-titan-text.md)
+ [Amazon Titan Image Generator G1 models](model-parameters-titan-image.md)
+ [Amazon Titan Embeddings G1 - Text](model-parameters-titan-embed-text.md)
+ [Amazon Titan Multimodal Embeddings G1](model-parameters-titan-embed-mm.md)