

# OpenAI models
<a name="model-parameters-openai"></a>

OpenAI offers the following open-weight models:
+ [https://huggingface.co/openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) – A smaller model optimized for lower latency and local or specialized use cases.
+ [https://huggingface.co/openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) – A larger model optimized for production and general purpose or high-reasoning use cases.

The following table summarizes information about the models:


| Information | gpt-oss-20b | gpt-oss-120b | 
| --- | --- | --- | 
| Release date | August 5, 2025 | August 5, 2025 | 
| Model ID | openai.gpt-oss-20b-1:0 | openai.gpt-oss-120b-1:0 | 
| Product ID | N/A | N/A | 
| Input modalities supported | Text | Text | 
| Output modalities supported | Text | Text | 
| Context window | 128,000 | 128,000 | 

The OpenAI models support the following features:
+ [Model invocation](inference.md) with the following operations:
  + [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
  + [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
  + [OpenAI Chat completions API](inference-chat-completions.md)
+ [Batch inference](batch-inference.md) with [CreateModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelInvocationJob.html).
+ [Guardrails](guardrails.md) application through the use of headers in the model invocation operations.

**Topics**
+ [OpenAI request body](#model-parameters-openai-request)
+ [OpenAI response body](#model-parameters-openai-response)
+ [Example usage of OpenAI models](#model-parameters-openai-use)

## OpenAI request body
<a name="model-parameters-openai-request"></a>

For information about the parameters in the request body and their descriptions, see [Create chat completion](https://developers.openai.com/api/reference/chat-completions/overview) in the OpenAI documentation.

Use the request body fields in the following ways:
+ In an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or OpenAI Chat Completions request, include the fields in the request body.
+ In a [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) request, do the following:
  + Map the `messages` as follows:
    + For each message whose role is `developer`, add the `content` a [SystemContentBlock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_SystemContentBlock.html) in the `system` array.
    + For each message whose role is `user` or `assistant`, add the `content` to a [ContentBlock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlock.html) in the `content` field and specify the `role` in the `role` field of a [Message](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Message.html) in the `messages` array.
  + Map the values for the following fields to the corresponding fields in the `inferenceConfig` object:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-openai.html)
  + Include any other fields in the `additionalModelRequestFields` object.

**Considerations when constructing the request body**
+ The OpenAI models support only text input and text output.
+ The value in the `model` field must match the one in the header. You can omit this field to let it be automatically populated with the same value as the header.
+ The value in the `stream` field must match the API operation that you use. You can omit this field to let it be automatically populated with the correct value.
  + If you use [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), the `stream` value must be `false`.

## OpenAI response body
<a name="model-parameters-openai-response"></a>

The response body for OpenAI models conforms to the chat completion object returned by OpenAI. For more information about the response fields, see [The chat completion object](https://platform.openai.com/docs/api-reference/chat/object) in the OpenAI documentation.

**Note**  
If you use `InvokeModel`, the model reasoning, surrounded by `<reasoning>` tags, precedes the text content of the response.

## Example usage of OpenAI models
<a name="model-parameters-openai-use"></a>

This section provides some examples of how to use the OpenAI models.

### Prerequisites
<a name="model-parameters-openai-use-prereq"></a>

Before trying out these examples, check that you've fulfilled the prerequisites:
+ **Authentication** – You can authenticate with either your AWS credentials or with an Amazon Bedrock API key.

  Set up your AWS credentials or generate an Amazon Bedrock API key to authenticate your request.
  + To learn about setting up your AWS credentials, see [Programmatic access with AWS security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html).
  + To learn about Amazon Bedrock API keys and how to generate them, see the API keys section in the Build chapter.
**Note**  
If you use the OpenAI Chat completions API, you can only authenticate with an Amazon Bedrock API key.
+ **Endpoint** – Find the endpoint that corresponds to the AWS Region to use in [Amazon Bedrock Runtime endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt). If you use an AWS SDK, you might only need to specify the region code and not the whole endpoint when you set up the client. You must use an endpoint associated with a Region supported by the model used in the example.
+ **Model access** – Request access to an OpenAI model. For more information, see [Manage model access using SDK and CLI](model-access.md#model-access-modify).
+ **(If the example uses an SDK) Install the SDK** – After installation, set up default credentials and a default AWS Region. If you don't set up default credentials or a Region, you'll have to explicitly specify them in the relevant code examples. For more information about standardized credential providers, see [AWS SDKs and Tools standardized credential providers](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html).
**Note**  
If you use the OpenAI SDK, you can only authenticate with an Amazon Bedrock API key and you must explicitly set the Amazon Bedrock endpoint.

Expand the section for the example that you want to see:

### OpenAI Create chat completion
<a name="model-parameters-openai-use-chat-completions"></a>

To see examples of using the OpenAI Create chat completion API, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

The following Python script calls the Create chat completion API with the OpenAI Python SDK:

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1", 
    api_key="$AWS_BEARER_TOKEN_BEDROCK" # Replace with actual API key
)

completion = client.chat.completions.create(
    model="openai.gpt-oss-20b-1:0",
    messages=[
        {
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
)

print(completion.choices[0].message)
```

------
#### [ HTTP request using curl ]

You can run the following command in a terminal to call the Create chat completion API using curl:

```
curl -X POST https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1/chat/completions \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
   -d '{
    "model": "openai.gpt-oss-20b-1:0",
    "messages": [
        {
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
}'
```

------

### InvokeModel
<a name="model-parameters-openai-use-invoke"></a>

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

```
import boto3
import json

# Initialize the Bedrock Runtime client
client = boto3.client('bedrock-runtime')

# Model ID
model_id = 'openai.gpt-oss-20b-1:0'

# Create the request body
native_request = {
  "model": model_id, # You can omit this field
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "assistant", 
      "content": "Hello! How can I help you today?"
    },
    {
      "role": "user",
      "content": "What is the weather like today?"
    }
  ],
  "max_completion_tokens": 150,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": False # You can omit this field
}

# Make the InvokeModel request
response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(native_request)
)

# Parse and print the message for each choice in the chat completion
response_body = json.loads(response['body'].read().decode('utf-8'))

for choice in response_body['choices']:
    print(choice['message']['content'])
```

------

### Converse
<a name="model-parameters-openai-use-converse"></a>

When you use the unified [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API, you need to map the OpenAI Create chat completion fields to its corresponding field in the Converse request body.

For example, compare the following chat completion request body to its corresponding Converse request body:

------
#### [ Create chat completion request body ]

```
{
  "model": "openai.gpt-oss-20b-1:0",
  "messages": [
    {
      "role": "developer",
      "content": "You are a helpful assistant."
    },
    {
      "role": "assistant", 
      "content": "Hello! How can I help you today?"
    },
    {
      "role": "user",
      "content": "What is the weather like today?"
    }
  ],
  "max_completion_tokens": 150,
  "temperature": 0.7
}
```

------
#### [ Converse request body ]

```
{
    "messages": [
        {
            "role": "user", 
            "content": [
                {
                    "text": "Hello! How can I help you today?"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "text": "What is the weather like today?"
                }
            ]
        }
    ],
    "system": [
        {
            "text": "You are a helpful assistant."
        }
    ],
    "inferenceConfig": {
        "maxTokens": 150,
        "temperature": 0.7
    }
}
```

------

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

```
# Use the Conversation API to send a text message to Anthropic Claude.

import boto3
from botocore.exceptions import ClientError

# Initialize the Bedrock Runtime client
client = boto3.client("bedrock-runtime")

# Set the model ID
model_id = "openai.gpt-oss-20b-1:0"

# Set up messages and system message
messages = [
    {
        "role": "assistant", 
        "content": [
            {
                "text": "Hello! How can I help you today?"
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "text": "What is the weather like today?"
            }
        ]
    }
]

system = [
    {
        "text": "You are a helpful assistant."
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=messages,
        system=system,
        inferenceConfig={
            "maxTokens": 150, 
            "temperature": 0.7, 
            "topP": 0.9
        },
    )

    # Extract and print the response text.
    for content_block in response["output"]["message"]["content"]:
        print(content_block)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
```

------

### Guardrails with InvokeModel
<a name="model-parameters-openai-use-guardrails-invoke"></a>

Apply a guardrail when running model invocation by specifying the guardrail ID, version, and whether or not to enable the guardrail trace in the header of a model invocation request.

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

```
import boto3
from botocore.exceptions import ClientError
import json

# Initiate the Amazon Bedrock Runtime client
bedrock_runtime = boto3.client("bedrock-runtime")

# Model ID
model_id = "openai.gpt-oss-20b-1:0"

# Replace with actual values from your guardrail
guardrail_id = "GR12345"
guardrail_version = "DRAFT"

# Create the request body
native_request = {
  "model": model_id, # You can omit this field
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "assistant", 
      "content": "Hello! How can I help you today?"
    },
    {
      "role": "user",
      "content": "What is the weather like today?"
    }
  ],
  "max_completion_tokens": 150,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": False # You can omit this field
}

try:
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(native_request),
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        trace='ENABLED',
    )
    response_body = json.loads(response.get('body').read())
    print("Received response from InvokeModel API (Request Id: {})".format(response['ResponseMetadata']['RequestId']))
    print(json.dumps(response_body, indent=2))

except ClientError as err:
    print("RequestId = " + err.response['ResponseMetadata']['RequestId'])
    raise err
```

------

### Guardrails with OpenAI chat completions
<a name="model-parameters-openai-use-guardrails-chat-completions"></a>

To see examples of using guardrails with OpenAI chat completions, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
import openai
from openai import OpenAIError

# Endpoint for Amazon Bedrock Runtime
bedrock_endpoint = "https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1"

# Model ID
model_id = "openai.gpt-oss-20b-1:0"

# Replace with actual values
bedrock_api_key = "$AWS_BEARER_TOKEN_BEDROCK"
guardrail_id = "GR12345"
guardrail_version = "DRAFT"

client = openai.OpenAI(
    api_key=bedrock_api_key,
    base_url=bedrock_endpoint,
)

try:
    response = client.chat.completions.create(
        model=model_id,
        # Specify guardrail information in the header
        extra_headers={
            "X-Amzn-Bedrock-GuardrailIdentifier": guardrail_id,
            "X-Amzn-Bedrock-GuardrailVersion": guardrail_version,
            "X-Amzn-Bedrock-Trace": "ENABLED",
        },
        # Additional guardrail information can be specified in the body
        extra_body={
            "amazon-bedrock-guardrailConfig": {
                "tagSuffix": "xyz"  # Used for input tagging
            }
        },
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "assistant", 
                "content": "Hello! How can I help you today?"
            },
            {
                "role": "user",
                "content": "What is the weather like today?"
            }
        ]
    )

    request_id = response._request_id
    print(f"Request ID: {request_id}")
    print(response)
    
except OpenAIError as e:
    print(f"An error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        request_id = e.response.headers.get("x-request-id")
        print(f"Request ID: {request_id}")
```

------
#### [ OpenAI SDK (Java) ]

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.HttpResponseFor;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

// Endpoint for Amazon Bedrock Runtime
String bedrockEndpoint = "http://bedrock-runtime.us-west-2.amazonaws.com/openai/v1"

// Model ID
String modelId = "openai.gpt-oss-20b-1:0"

// Replace with actual values
String bedrockApiKey = "$AWS_BEARER_TOKEN_BEDROCK"
String guardrailId = "GR12345"
String guardrailVersion = "DRAFT"

OpenAIClient client = OpenAIOkHttpClient.builder()
        .apiKey(bedrockApiKey)
        .baseUrl(bedrockEndpoint)
        .build()

ChatCompletionCreateParams request = ChatCompletionCreateParams.builder()
        .addUserMessage("What is the temperature in Seattle?")
        .model(modelId)
        // Specify additional headers for the guardrail
        .putAdditionalHeader("X-Amzn-Bedrock-GuardrailIdentifier", guardrailId)
        .putAdditionalHeader("X-Amzn-Bedrock-GuardrailVersion", guardrailVersion)
        // Specify additional body parameters for the guardrail
        .putAdditionalBodyProperty(
                "amazon-bedrock-guardrailConfig",
                JsonValue.from(Map.of("tagSuffix", JsonValue.of("xyz"))) // Allows input tagging
        )
        .build();
        
HttpResponseFor<ChatCompletion> rawChatCompletionResponse =
        client.chat().completions().withRawResponse().create(request);

final ChatCompletion chatCompletion = rawChatCompletionResponse.parse();

System.out.println(chatCompletion);
```

------

### Batch inference
<a name="model-parameters-openai-use-batch"></a>

[Batch inference](batch-inference.md) lets you run model inference asynchronously with multiple prompts. To run batch inference with an OpenAI model, you do the following:

1. Create a JSONL file and populate it with at least the minimum number of JSON objects, each separated by a new line. Each `modelInput` object must conform to the format of the [OpenAI create chat completion](https://developers.openai.com/api/reference/chat-completions/overview) request body. The following shows an example of the first two lines of a JSONL file containing request bodies for OpenAI.

   ```
   {
       "recordId": "RECORD1", 
       "modelInput": {
           "messages": [
               {
                   "role": "system", 
                   "content": "You are a helpful assistant."
               }, 
               {
                   "role": "user", 
                   "content": "Can you generate a question with a factual answer?"
               }
           ], 
           "max_completion_tokens": 1000
       }
   }
   {
       "recordId": "RECORD2", 
       "modelInput": {
           "messages": [
               {
                   "role": "system", 
                   "content": "You are a helpful assistant."
               }, 
               {
                   "role": "user", 
                   "content": "What is the weather like today?"
               }
           ], 
           "max_completion_tokens": 1000
       }
   }
   ...
   ```
**Note**  
The `model` field is optional because the batch inference service will insert it for you based on the header if you omit it.  
Check that your JSONL file conforms to the batch inference quotas as outlined in [Format and upload your batch inference data](batch-inference-data.md).

1. Upload the file to an Amazon S3 bucket.

1. Send a [CreateModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelInvocationJob.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) with the S3 bucket from the previous step specified in the `inputDataConfig` field and the OpenAI model specified in the `modelId` field.

For an end-to-end code example, see [Code example for batch inference](batch-inference-example.md). Replace with the proper configurations for the OpenAI models.