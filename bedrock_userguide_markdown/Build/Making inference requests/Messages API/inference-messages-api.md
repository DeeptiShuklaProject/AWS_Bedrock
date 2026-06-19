

# Inference using Anthropic Messages API
<a name="inference-messages-api"></a>

The Anthropic Messages API provides native access to Claude models using the Anthropic request and response format. You can use the Messages API on both the `bedrock-mantle` and `bedrock-runtime` endpoints, giving you flexibility to choose the authentication and integration style that fits your application.


| **Endpoint** | **Base URL** | **Use case** | 
| --- | --- | --- | 
| bedrock-mantle | https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages | Recommended for new applications. Supports API key auth and [Workspaces (Anthropic-compatible)](workspaces.md). | 
| bedrock-runtime | https://bedrock-runtime.{region}.amazonaws.com | Use with existing AWS SDK integrations and invocation logging. | 

## Supported Regions
<a name="inference-messages-api-supported"></a>

The Messages API is available on the `bedrock-mantle` endpoint in all Regions that support `bedrock-mantle` (see [Supported Regions and Endpoints](bedrock-mantle.md#bedrock-mantle-supported)). On the `bedrock-runtime` endpoint, it is available in all Regions where Claude models are available. See [Regional availability](models-region-compatibility.md) for details.

## Prerequisites
<a name="inference-messages-api-prereq"></a>

Before using the Messages API, ensure you have the following:
+ **Model access** – Request access to Claude models in the Amazon Bedrock console. See [Request access to models](model-access.md).
+ **Authentication** – Depends on the endpoint:
  + `bedrock-mantle` – Use a Amazon Bedrock API key (see [API keys](api-keys.md)) or AWS SigV4 credentials.
  + `bedrock-runtime` – Use AWS SigV4 credentials via the AWS SDK (boto3, etc.).
+ **Anthropic version header** – All requests require an API version:
  + `bedrock-mantle`: Set `anthropic-version: 2023-06-01` as an HTTP header.
  + `bedrock-runtime`: Set `"anthropic_version": "bedrock-2023-05-31"` in the request body.

## Basic request
<a name="inference-messages-api-basic"></a>

To send a basic message to a Claude model, choose the tab for your preferred method, and then follow the steps:

------
#### [ bedrock-mantle (curl) ]

```
curl -X POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic.claude-sonnet-4-6-v1",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
  }'
```

------
#### [ bedrock-runtime (Python) ]

```
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="anthropic.claude-sonnet-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Explain quantum computing in one sentence."}
        ]
    })
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])
```

------
#### [ bedrock-runtime (AWS CLI) ]

Use the AWS CLI to invoke the model:

```
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-sonnet-4-6-v1 \
  --body '{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
  }' \
  --cli-binary-format raw-in-base64-out \
  output.json
```

------
#### [ bedrock-runtime (curl) ]

You can call `bedrock-runtime` directly with curl by signing the request with AWS SigV4. The example below uses curl's built-in `--aws-sigv4` flag (available in curl 7.75.0 and later):

```
curl -X POST \
  "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-sonnet-4-6-v1/invoke" \
  -H "Content-Type: application/json" \
  --aws-sigv4 "aws:amz:us-east-1:bedrock" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -d '{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
  }'
```

**Note**  
If you are using temporary credentials from AWS STS (for example, an assumed role), also pass the session token by adding `-H "X-Amz-Security-Token: $AWS_SESSION_TOKEN"` to the request. For most use cases we recommend the AWS SDKs or CLI, which handle request signing and credential refresh automatically.

------

## Stream responses
<a name="inference-messages-api-streaming"></a>

To receive response tokens incrementally as they are generated, choose the tab for your preferred method, and then follow the steps:

------
#### [ bedrock-mantle (curl) ]

```
curl -X POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic.claude-sonnet-4-6-v1",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
        {"role": "user", "content": "Write a short poem about cloud computing."}
    ]
  }'
```

------
#### [ bedrock-runtime (Python) ]

```
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model_with_response_stream(
    modelId="anthropic.claude-sonnet-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Write a short poem about cloud computing."}
        ]
    })
)

for event in response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk["type"] == "content_block_delta":
        print(chunk["delta"]["text"], end="")
```

------

## Supported features
<a name="inference-messages-api-features"></a>

In addition to the [Extended thinking](claude-messages-extended-thinking.md), [Adaptive thinking](claude-messages-adaptive-thinking.md), [Structured outputs](claude-messages-structured-outputs.md), [Compaction](claude-messages-compaction.md), [Fallback credit for refused requests (beta)](claude-messages-fallback-credit.md), and [Mid-conversation system messages](claude-messages-mid-conversation-system.md) sections above, the Messages API supports the following features with Claude models:
+ **System prompts** – Set model behavior with a `system` parameter.
+ **Multi-turn conversations** – Pass alternating `user` and `assistant` messages.
+ **Tool use** – Define tools the model can call. See [Use a tool to complete an Amazon Bedrock model response](tool-use.md).
+ **Vision** – Send images in the `content` array alongside text.
+ **Prompt caching** – Cache frequently used context to reduce latency and cost.

For the full Messages API request and response field reference, see [Request and Response](model-parameters-anthropic-claude-messages-request-response.md).

## Count tokens
<a name="inference-messages-api-count-tokens"></a>

To count the number of input tokens that a request would consume before sending it for inference, use the Anthropic `count_tokens` path on the `bedrock-mantle` endpoint. This is the only token-counting path supported for Claude models that are not available on `bedrock-runtime` with a Region-specific endpoint, including Claude models that launch with cross-Region inference (CRIS) only. For details and an example, see [Count tokens using the bedrock-mantle endpoint](count-tokens.md#count-tokens-mantle).