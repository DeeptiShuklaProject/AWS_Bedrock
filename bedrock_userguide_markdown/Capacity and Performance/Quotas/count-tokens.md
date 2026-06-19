

# Monitor your token usage by counting tokens before running inference
<a name="count-tokens"></a>

When you run model inference, the number of tokens that you send in the input contributes to the cost of the request and towards the quota of tokens that you can use per minute and per day. The [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) API helps you estimate token usage before sending requests to foundation models by returning the token count that would be used if the same input were sent to the model in an inference request.

**Note**  
Using the [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) API doesn't incur charges.

**Note**  
Some Anthropic Claude models – including those that launch with cross-Region inference (CRIS) only on `bedrock-runtime` – don't support [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) on `bedrock-runtime`. For these models, count input tokens by calling Anthropic's `count_tokens` API on the `bedrock-mantle` endpoint instead. See [Count tokens using the bedrock-mantle endpoint](#count-tokens-mantle) for the URL, request body, and an example.

Token counting is model-specific because different models use different tokenization strategies. The token count returned by this operation will match the token count that would be charged if the same input were sent to the model to run inference.

You can use the `CountTokens` API to do the following:
+ Estimate costs before sending inference requests.
+ Optimize prompts to fit within token limits.
+ Plan for token usage in your applications.

**Topics**
+ [Supported models and Regions for token counting](#count-tokens-supported)
+ [Count tokens using the bedrock-runtime endpoint](#count-tokens-use)
+ [Example: count tokens for a bedrock-runtime request](#count-tokens-example)
+ [Count tokens using the bedrock-mantle endpoint](#count-tokens-mantle)

## Supported models and Regions for token counting
<a name="count-tokens-supported"></a>

To see which models support token counting, please visit [models at a glance](model-cards.md) and pick the model you are interested in.

## Count tokens using the bedrock-runtime endpoint
<a name="count-tokens-use"></a>

To count the number of input tokens in an inference request, send a [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) request with an [Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt), Specify the model in the header and the input to count tokens for in the `body` field. The value of the `body` field depends on whether you're counting input tokens for an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) request:
+ For an `InvokeModel` request, the format of the `body` is a string representing a JSON object whose format depends on the model that you specify.
+ For a `Converse` request, the format of the `body` is a JSON object specifying the `messages` and `system` prompts included in the conversation.

## Example: count tokens for a bedrock-runtime request
<a name="count-tokens-example"></a>

The examples in this section let you count tokens for an `InvokeModel` and `Converse` request with Anthropic Claude 3 Haiku.

**Prerequisites**
+ You've downloaded AWS SDK for Python (Boto3) and your configuration is set up such that your credentials and default AWS Region are automatically recognized.
+ Your IAM identity has permissions for the following actions (for more information, see [Action, resources, and condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html)):
  + bedrock:CountTokens – Allows the usage of `CountTokens`.
  + bedrock:InvokeModel – Allows the usage of `InvokeModel` and `Converse`. Should be scoped to the {{arn:${Partition}:bedrock:${Region}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0}}, at minimum.

To try out counting tokens for an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) request, run the following Python code:

```
import boto3
import json

bedrock_runtime = boto3.client("bedrock-runtime")

input_to_count = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 500,
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
})

response = bedrock_runtime.count_tokens(
    modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
    input={
        "invokeModel": {
            "body": input_to_count
        }
    }
)

print(response["inputTokens"])
```

To try out counting tokens for a [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) request, run the following Python code:

```
import boto3
import json 

bedrock_runtime = boto3.client("bedrock-runtime")

input_to_count = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "What is the capital of France?"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "The capital of France is Paris."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "text": "What is its population?"
                }
            ]
        }
    ],
    "system": [
        {
            "text": "You're an expert in geography."
        }
    ]
}

response = bedrock_runtime.count_tokens(
    modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
    input={
        "converse": input_to_count
    }
)

print(response["inputTokens"])
```

## Count tokens using the bedrock-mantle endpoint
<a name="count-tokens-mantle"></a>

The `bedrock-mantle` endpoint exposes Anthropic's `count_tokens` API at `/anthropic/v1/messages/count_tokens`. Use it to count input tokens for Anthropic Claude models that don't support [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) on `bedrock-runtime` – for example, when the model is offered only through cross-Region inference (CRIS) on `bedrock-runtime` and so has no Region-specific endpoint for [CountTokens](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_CountTokens.html) to target. The `/anthropic/v1/messages` path is Claude-specific; non-Anthropic models on `bedrock-mantle` return `The model 'X' does not support the '/anthropic/v1/messages' API`.

**Request details**
+ **URL** – `POST https://bedrock-mantle.{{region}}.api.aws/anthropic/v1/messages/count_tokens`. For supported Regions, see [Supported Regions and Endpoints](bedrock-mantle.md#bedrock-mantle-supported).
+ **Request body** – The Anthropic `count_tokens` shape, including `model`, `messages`, and optional `system` and `tools` fields. See the [Anthropic Messages count tokens reference](https://docs.anthropic.com/en/api/messages-count-tokens).
+ **Authentication** – Either a SigV4 signature with service name `bedrock-mantle`, or an Amazon Bedrock API key passed in the `x-api-key` header. See [API keys](api-keys.md).
+ **IAM action** – `bedrock-mantle:CountTokens`. The authorization is scoped to a Amazon Bedrock [Project](projects.md) resource of the form `arn:aws:bedrock-mantle:{{region}}:{{account-id}}:project/{{project-name}}`. The default project name is `default`.
+ **SDK support** – The AWS SDKs do not currently expose a method that targets this endpoint. Send the request as a SigV4-signed HTTP `POST`, or use any HTTP client with a Amazon Bedrock API key. The `bedrock-runtime` client method `count_tokens` does not target this endpoint and returns a validation error for models that are not supported on `bedrock-runtime`.
+ **Error format** – Errors follow the Anthropic shape: `{"type": "error", "request_id": "...", "error": {"type": "error-type", "message": "error-message"}}`. This differs from the standard AWS JSON error envelope returned by `bedrock-runtime`.

**Note**  
The `count_tokens` endpoint validates the request body using the same schema as the corresponding inference endpoint, so request fields that the model does not support are rejected with HTTP 400. For example, Anthropic Claude Opus 4.7 does not accept `strict: true` on `tools[]` and returns `tools.0.custom.strict: Extra inputs are not permitted`. Consult the [model card](model-cards.md) for the model-specific feature surface.

The following example uses `curl` with a Amazon Bedrock API key to count tokens on the `bedrock-mantle` endpoint:

```
curl -X POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages/count_tokens \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic.claude-opus-4-7",
    "messages": [
        {"role": "user", "content": "How many tokens is this prompt?"}
    ]
  }'
```

The response contains an `input_tokens` field whose value is the token count for the supplied input.