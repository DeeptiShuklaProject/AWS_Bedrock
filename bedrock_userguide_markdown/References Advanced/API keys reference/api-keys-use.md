

# Use an Amazon Bedrock API key
<a name="api-keys-use"></a>

You can use your Amazon Bedrock API key in the following ways:
+ **Set it as environment variable** – The Amazon Bedrock service recognizes the environment variable `AWS_BEARER_TOKEN_BEDROCK` You have the following options to set the key:
  + Open a terminal to set it:
    + **MacOS/Linux**

      ```
      export AWS_BEARER_TOKEN_BEDROCK={{${api-key}}}
      ```
    + **Windows**

      ```
      setx AWS_BEARER_TOKEN_BEDROCK "{{${api-key}}}"
      ```
  + Set it as an environment variable in your code before you make the API request. For example, you could include the following lines before making the request:
    + **Python**

      ```
      import os                      
      os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "{{${api-key}}}"
      ```
+ **Specify it in a request** – You can include the Amazon Bedrock API key in the authorization header in the following ways (replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with the actual value):
  + **In a direct HTTP request** – Include the following as an authorization header:

    ```
    Authorization: Bearer {{$AWS_BEARER_TOKEN_BEDROCK}}
    ```
  + **As a parameter in a supported SDK** – Specify the value in the parameter when setting up the client. For example, you can specify it in the `api_key` field when setting up a client with the [OpenAI Python SDK](https://github.com/openai/openai-python?tab=readme-ov-file#usage).

**Note**  
Amazon Bedrock API keys are limited to [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock.html) and [Amazon Bedrock Runtime](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html) actions. You can't use them with the following API operations:  
[InvokeModelWithBidirectionalStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithBidirectionalStream.html).
[Agents for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) or [Agents for Amazon Bedrock Runtime](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) API operations.
[Data Automation for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Data_Automation_for_Amazon_Bedrock.html) or [Runtime for Amazon Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Runtime_for_Amazon_Bedrock_Data_Automation) API operations.

To see an example of using the API key to send a [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) request to generate a response, choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

The following example shows how to send an API request with the AWS SDK for Python (Boto3). If you didn't already set the API key as the `AWS_BEARER_TOKEN_BEDROCK` environment variable, specify it in place of {{${api-key}}} in the following code:

```
import os
import boto3
                        
# If you already set the API key as an environment variable, you can comment this line out                        
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "{{${api-key}}}"

# Create an Amazon Bedrock client
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1" # If you've configured a default region, you can omit this line
)

# Define the model and message
model_id = "us.anthropic.claude-sonnet-4-6"
messages = [{"role": "user", "content": [{"text": "Hello"}]}]

response = client.converse(
    modelId=model_id,
    messages=messages,
)
```

------
#### [ HTTP Client (requests package in Python) ]

**Prerequisite:** Install the `requests` package by opening a terminal and running the following command:

```
python3 -m pip install requests
```

The following example shows how to directly send an API request with an HTTP client. Specify the {{${api-key}}} in the header.

```
import requests

url = "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-6/converse"

payload = {
    "messages": [
        {
            "role": "user",
            "content": [{"text": "Hello"}]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{${api-key}}}"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

------
#### [ HTTP request using cURL ]

The following example shows how to directly send an API request, using cURL. If you didn't set the API key as the AWS\_BEARER\_TOKEN\_BEDROCK environment variable, you'll have to replace `$AWS_BEARER_TOKEN_BEDROCK` in the example with the literal value of the key.

```
curl -X POST "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-6/converse" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
  -d '{
    "messages": [
        {
            "role": "user",
            "content": [{"text": "Hello"}]
        }
    ]
  }'
```

------