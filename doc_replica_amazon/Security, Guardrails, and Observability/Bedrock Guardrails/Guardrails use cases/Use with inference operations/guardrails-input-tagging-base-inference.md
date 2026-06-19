

# Use your guardrail with inference operations to evaluate user input
<a name="guardrails-input-tagging-base-inference"></a>

You can use guardrails with the base inference operations, [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming). This section covers how you selectively evaluate user input and how you can configure streaming response behavior. Note that for conversational applications, you can achieve the same results with the [Converse API](guardrails-use-converse-api.md).

For example code that calls the base inference operations, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md). For information about using a guardrail with the base inference operations, follow the steps in the API tab of [Test your guardrail](guardrails-test.md). 

**Topics**
+ [Apply tags to user input to filter content](guardrails-tagging.md)
+ [Configure streaming response behavior to filter content](guardrails-streaming.md)
+ [Include a guardrail with the Converse API](guardrails-use-converse-api.md)