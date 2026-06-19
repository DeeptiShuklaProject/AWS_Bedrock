

# Writer AI Palmyra models
<a name="model-parameters-writer-palmyra"></a>

This section describes the request parameters and response fields for Writer AI models. Use this information to make inference calls to Writer AI models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Writer AI models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific Writer AI model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Writer AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Writer AI models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Writer AI models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Writer AI models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Writer AI specific prompt information, see the [Writer AI prompt engineering guide]().

**Writer Palmyra X4**

Top-ranked on Stanford HELM, Writer Palmyra X4 achieves superior performance on complex tasks and agentic workflows. It combines a 128k token context window with a suite of enterprise-grade capabilities, including advanced reasoning, tool-calling, LLM delegation, built-in RAG, code generation, structured outputs, multi-modality, and multi-lingual support. Using enterprise-specific tools that extend the model's ability to take action, Palmyra X4 enables developers to build apps and agents that updating system, performing transaction, sending email, triggering workflow, and more.

**Writer Palmyra X5**

With a one million token context window, Writer Palmyra X5 marks the end of context constraints for app and agent development. Writer's newest model achieves superior performance on long context inference through expanded memory and processing power, enabling developers to build more complex, multi-step agentic workflows faster. Like Palmyra X4, Palmyra X5 includes a suite of enterprise-ready capabilities, including advanced reasoning, tool-calling, LLM delegation, built-in RAG, code generation, structured outputs, multi-modality, and multi-lingual support

**Topics**
+ [Writer Palmyra X4](model-parameters-palmyra-x4.md)
+ [Writer Palmyra X5](model-parameters-palmyra-x5.md)