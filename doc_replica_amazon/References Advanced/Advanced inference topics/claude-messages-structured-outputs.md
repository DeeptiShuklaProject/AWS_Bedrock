

# Get validated JSON results from models
<a name="claude-messages-structured-outputs"></a>

You can use structured outputs with Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.5, and Claude Opus 4.6 through the Converse API ([Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)) or the InvokeModel API ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)) on the `bedrock-runtime` endpoint. Structured outputs is *not* supported on the Anthropic Messages API path on the `bedrock-mantle` endpoint (`https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`); the `output_config.format` parameter is rejected with a `400` error.

To learn more, see [Get validated JSON results from models](structured-output.md).