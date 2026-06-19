

# Amazon Nova models
<a name="model-parameters-nova"></a>

Amazon Nova multimodal understanding models are available for use for inferencing through the Invoke API ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)) and the Converse API ([Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) and [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)). To create conversational applications see [Inference using Converse API](conversation-inference.md). Both of the API methods (Invoke and Converse) follow a very similar request pattern, for more information on API schema and Python code examples see [How to Invoke Amazon Nova Understanding Models](https://docs.aws.amazon.com/nova/latest/userguide/invoke.html).

**Important**  
The timeout period for inference calls to Amazon Nova is 60 minutes. By default, AWS SDK clients timeout after 1 minute. We recommend that you increase the read timeout period of your AWS SDK client to at least 60 minutes. For example, in the AWS Python botocore SDK, change the value of the `read_timeout`field in [botocore.config](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html#) to at least 3600.

The default inference parameters can be found in the [Complete request schema](https://docs.aws.amazon.com/nova/latest/userguide/complete-request-schema.html) section of the Amazon Nova User Guide.

To find the model ID for Amazon Nova models, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check if a feature is supported for Amazon Nova models, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Amazon Nova models support, see [Modality Support](https://docs.aws.amazon.com/nova/latest/userguide/modalities.html). To check which Amazon Bedrock features the Amazon Nova models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check the AWS Regions that Amazon Nova models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Amazon Nova models, you must include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Amazon Nova specific prompt information, see the [Amazon Nova prompt engineering guide](https://docs.aws.amazon.com/nova/latest/userguide/prompting.html).