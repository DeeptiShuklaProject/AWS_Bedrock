

# Inference using Responses API
<a name="bedrock-mantle"></a>

Amazon Bedrock provides the OpenAI Responses API via the `bedrock-mantle` endpoint, powered by Mantle, a distributed inference engine for large-scale machine learning model serving. This endpoint allows you to use familiar OpenAI SDKs and tools with Amazon Bedrock models, enabling you to migrate existing applications with minimal code changes—simply update your base URL and API key.

**Important**  
When using the OpenAI SDK with Amazon Bedrock, you must point it to the Amazon Bedrock endpoint, not the OpenAI endpoint. Set the following environment variables:  

```
OPENAI_BASE_URL="https://bedrock-mantle.<your-region>.api.aws/v1"
OPENAI_API_KEY="<your Bedrock API key>"
```
Do not use your OpenAI API key or the OpenAI base URL (`https://api.openai.com/v1`). Those connect to OpenAI directly, not to Amazon Bedrock. To create a Amazon Bedrock API key, see [API keys](api-keys.md).

Key benefits include:
+ **Asynchronous inference** – Support for long-running inference workloads through the Responses API
+ **Stateful conversation management** – Automatically rebuild context without manually passing conversation history with each request
+ **Simplified tool use** – Streamlined integration for agentic workflows
+ **Flexible response modes** – Support for both streaming and non-streaming responses
+ **Easy migration** – Compatible with existing OpenAI SDK codebases

Inference traffic to the `bedrock-mantle` endpoint is governed by a separate set of quotas from the `bedrock-runtime` endpoint. For details on input and output token quotas and how to request increases, see [Quotas for the bedrock-mantle endpoint](quotas-mantle.md).

## Supported Regions and Endpoints
<a name="bedrock-mantle-supported"></a>

The `bedrock-mantle` endpoint is available in the following AWS Regions:


| Region Name | Region | Endpoint | 
| --- | --- | --- | 
| US East (Ohio) | us-east-2 | bedrock-mantle.us-east-2.api.aws | 
| US East (N. Virginia) | us-east-1 | bedrock-mantle.us-east-1.api.aws | 
| US West (Oregon) | us-west-2 | bedrock-mantle.us-west-2.api.aws | 
| Asia Pacific (Jakarta) | ap-southeast-3 | bedrock-mantle.ap-southeast-3.api.aws | 
| Asia Pacific (Mumbai) | ap-south-1 | bedrock-mantle.ap-south-1.api.aws | 
| Asia Pacific (Sydney) | ap-southeast-2 | bedrock-mantle.ap-southeast-2.api.aws | 
| Asia Pacific (Tokyo) | ap-northeast-1 | bedrock-mantle.ap-northeast-1.api.aws | 
| Europe (Frankfurt) | eu-central-1 | bedrock-mantle.eu-central-1.api.aws | 
| Europe (Ireland) | eu-west-1 | bedrock-mantle.eu-west-1.api.aws | 
| Europe (London) | eu-west-2 | bedrock-mantle.eu-west-2.api.aws | 
| Europe (Milan) | eu-south-1 | bedrock-mantle.eu-south-1.api.aws | 
| Europe (Stockholm) | eu-north-1 | bedrock-mantle.eu-north-1.api.aws | 
| South America (São Paulo) | sa-east-1 | bedrock-mantle.sa-east-1.api.aws | 

## Prerequisites
<a name="bedrock-mantle-prereq"></a>

Before using OpenAI APIs, ensure you have the following:
+ **Authentication** – You can authenticate using:
  + Amazon Bedrock API key (required for OpenAI SDK)
  + AWS credentials (supported for HTTP requests)
+ **OpenAI SDK** (optional) – Install the OpenAI Python SDK if using SDK-based requests.
+ **Environment variables** – Set the following environment variables:
  + `OPENAI_API_KEY` – Set to your Amazon Bedrock API key
  + `OPENAI_BASE_URL` – Set to the Amazon Bedrock endpoint for your region (for example, ` https://bedrock-mantle.us-east-1.api.aws/v1`)

## Models API
<a name="bedrock-mantle-models"></a>

The Models API allows you to discover available models in Amazon Bedrock powered by Mantle. Use this API to retrieve a list of models you can use with the Responses API. For complete API details, see the [OpenAI Models documentation](https://developers.openai.com/api/reference/resources/models).

### List available models
<a name="bedrock-mantle-models-list"></a>

To list available models, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# List all available models using the OpenAI SDK
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

from openai import OpenAI

client = OpenAI()

models = client.models.list()

for model in models.data:
    print(model.id)
```

------
#### [ HTTP request ]

Make a GET request to `/v1/models`:

```
# List all available models
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

curl -X GET $OPENAI_BASE_URL/models \
   -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

## Responses API
<a name="bedrock-mantle-responses"></a>

The Responses API provides stateful conversation management with support for streaming, background processing, and multi-turn interactions. For complete API details, see the [OpenAI Responses documentation](https://developers.openai.com/api/reference/resources/responses).

**Note**  
Not all models support the Responses API. To see which models support the Responses API, see [API compatibility](models-api-compatibility.md).

### How the Responses API stores conversation state
<a name="bedrock-mantle-responses-state"></a>

The Responses API can use stored state to enable multi-turn conversations and let you reference previous turns through the `previous_response_id` parameter. Storage is enabled by default but can be disabled per request through the `store` parameter. Stored responses are scoped by Project. A response from one Project cannot be used as the previous response or read in a second Project. For more information about Projects, see [Projects (OpenAI-compatible)](projects.md).
+ When `store` is `true` (the default), Amazon Bedrock retains the response, including the input and output, for 30 days in the source region of the request. During this window you can chain follow-up requests by passing `previous_response_id` and retrieve the response with `GET /v1/responses/{id}`. After 30 days, the response is automatically deleted and is no longer retrievable.
+ When `store` is `false`, Amazon Bedrock does not retain any data from the request or response. The `previous_response_id` parameter cannot be used to continue the conversation.

The default value is `true` to match the OpenAI Responses API specification. Customers who do not want Amazon Bedrock to retain conversation data should explicitly set `store` to `false` on every request. Stored data is kept in the source region of the request, encrypted at rest, and scoped to the calling AWS account's Project resource. The data is stored solely to service your requests and is not used or retained for any other purpose.

### Basic request
<a name="bedrock-mantle-responses-create"></a>

To create a response, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Create a basic response using the OpenAI SDK
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="openai.gpt-oss-120b",
    input=[
        {"role": "user", "content": "Hello! How can you help me today?"}
    ]
)

print(response)
```

------
#### [ HTTP request ]

Make a POST request to `/v1/responses`:

```
# Create a basic response
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

curl -X POST $OPENAI_BASE_URL/responses \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer $OPENAI_API_KEY" \
   -d '{
    "model": "openai.gpt-oss-120b",
    "input": [
        {"role": "user", "content": "Hello! How can you help me today?"}
    ]
}'
```

------

### Stream responses
<a name="bedrock-mantle-responses-streaming"></a>

To receive response events incrementally, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Stream response events incrementally using the OpenAI SDK
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="openai.gpt-oss-120b",
    input=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for event in stream:
    print(event)
```

------
#### [ HTTP request ]

Make a POST request to `/v1/responses` with `stream` set to `true`:

```
# Stream response events incrementally
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

curl -X POST $OPENAI_BASE_URL/responses \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer $OPENAI_API_KEY" \
   -d '{
    "model": "openai.gpt-oss-120b",
    "input": [
        {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
}'
```

------