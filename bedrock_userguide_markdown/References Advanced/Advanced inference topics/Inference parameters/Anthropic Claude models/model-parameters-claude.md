

# Anthropic Claude models
<a name="model-parameters-claude"></a>

This section describes the request parameters and response fields for Anthropic Claude models. Use this information to make inference calls to Anthropic Claude models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Anthropic Claude models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific Anthropic Claude model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Anthropic Claude models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Anthropic Claude models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Anthropic Claude models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Anthropic Claude models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Anthropic Claude specific prompt information, see the [Anthropic Claude prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview).

You can use Amazon Bedrock to send [Anthropic Claude Messages API](model-parameters-anthropic-claude-messages.md) inference requests.

You use the messages API to create conversational applications, such as a virtual assistant or a coaching application.

Anthropic Claude models support the use of XML tags to structure and delineate your prompts. For example, you can surround examples in your prompt with an `<examples>` tag. Use descriptive tag names for optimal results. For more information, see [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) in the [Anthropic user guide](https://docs.anthropic.com/en/docs/welcome).

Anthropic Claude models support the use of PDF document processing and citations. Citations provide references to information in the document used by the model in a response.

**Note**  
To use system prompts in inference calls, you must use Anthropic Claude versions that are 2.1 or greater.  
For information about creating system prompts, see [Giving Claude a role with a system prompt](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) in the Anthropic Claude documentation.  
To avoid timeouts with Anthropic Claude version 2.1, we recommend limiting the input token count in the `prompt` field to 180K. We expect to address this timeout issue soon.

In the inference call, fill the `body` field with a JSON object that conforms to a [Anthropic Claude Messages API](model-parameters-anthropic-claude-messages.md) request. 

**Topics**
+ [Anthropic Claude Messages API](model-parameters-anthropic-claude-messages.md)