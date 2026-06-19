

# Stability AI models
<a name="model-parameters-stability-diffusion"></a>

This section describes the request parameters and response fields for Stability AI models. Use this information to make inference calls to Stability AI models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) operation. This section also includes Python code examples that shows how to call Stability AI models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if the Converse API supports a specific Stability AI model, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Stability AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Stability AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Stability AI models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Stability AI models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Stability AI specific prompt information, see the [Stability AI prompt engineering guide](https://platform.stability.ai/docs/getting-started).

## Supported models and image services
<a name="supported-stability-models"></a>

Amazon Bedrock supports the following Stability AI models and image services.

**Note**  
Support for all other Stability AI models are in the process of being deprecated.


| Model | Use cases | Example | 
| --- | --- | --- | 
| [Stable Image Ultra](model-parameters-diffusion-stable-ultra-text-image-request-response.md) |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)  | A luxury brand uses Stable Image Ultra to create stunning visuals of its latest collection for magazine spreads, ensuring a premium feel that matches its high standards. | 
| [Stable Diffusion 3.5 Large](model-parameters-diffusion-3-5-large.md) |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)  | A game development team uses SD3.5 Large to create detailed environmental textures and character concepts, accelerating their creative pipeline. | 
| [Stable Image Core](model-parameters-diffusion-stable-image-core-text-image-request-response.md) |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)  | An online retailer uses Stable Image Core to quickly generate product images for new arrivals, allowing it to list items faster and keep its catalog up-to-date. | 
| [Stability AI Image Services](stable-image-services.md) |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)  | A media company uses search and recolor, style transfer, and remove background to generate variations of images for an advertising campaign. | 

**Topics**
+ [Supported models and image services](#supported-stability-models)
+ [Stable Image Ultra request and response](model-parameters-diffusion-stable-ultra-text-image-request-response.md)
+ [Stability.ai Stable Diffusion 3.5 Large](model-parameters-diffusion-3-5-large.md)
+ [Stable Image Core request and response](model-parameters-diffusion-stable-image-core-text-image-request-response.md)
+ [Stability AI Image Services](stable-image-services.md)