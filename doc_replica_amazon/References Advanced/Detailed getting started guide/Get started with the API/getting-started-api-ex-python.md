

# Run example Amazon Bedrock API requests through the AWS SDK for Python (Boto3)
<a name="getting-started-api-ex-python"></a>

This section guides you through trying out some common operations in Amazon Bedrock with the AWS Python to test that your permissions and authentication are set up properly. Before you run the following examples, you should check that you have fulfilled the following prerequisites:

**Prerequisites**
+ You have an AWS account and a user or role with authentication set up and the necessary permissions for Amazon Bedrock. Otherwise, follow the steps at [Get started with the API](getting-started-api.md).
+ You've installed and set up authentication for the AWS SDK for Python (Boto3). To install Boto3, follow the steps at [Quickstart](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) in the Boto3 documentation. Verify that you've set up your credentials to use Boto3 by following the steps at [Get credentials to grant programmatic access](getting-started-api.md#gs-grant-program-access).

Test that your permissions are set up properly for Amazon Bedrock, using a user or role that you set up with the proper permissions. 

The Amazon Bedrock documentation also includes code examples for other programming languages. For more information, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

**Topics**
+ [List the foundation models that Amazon Bedrock has to offer](#getting-started-api-ex-python-listfm)
+ [Submit a text prompt to a model and generate a text response with InvokeModel](#getting-started-api-ex-python-invoke-text)
+ [Submit a text prompt to a model and generate a text response with Converse](#getting-started-api-ex-python-converse)

## List the foundation models that Amazon Bedrock has to offer
<a name="getting-started-api-ex-python-listfm"></a>

The following example runs the [ListFoundationModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) operation using an Amazon Bedrock client. `ListFoundationModels` lists the foundation models (FMs) that are available in Amazon Bedrock in your Region. Run the following SDK for Python script to create an Amazon Bedrock client and test the [ListFoundationModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) operation:

```
"""
Lists the available Amazon Bedrock models in an &AWS-Region;.
"""
import logging
import json
import boto3


from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_foundation_models(bedrock_client):
    """
    Gets a list of available Amazon Bedrock foundation models.

    :return: The list of available bedrock foundation models.
    """

    try:
        response = bedrock_client.list_foundation_models()
        models = response["modelSummaries"]
        logger.info("Got %s foundation models.", len(models))
        return models

    except ClientError:
        logger.error("Couldn't list foundation models.")
        raise


def main():
    """Entry point for the example. Change aws_region to the &AWS-Region;
    that you want to use."""
   
    aws_region = "us-east-1"

    bedrock_client = boto3.client(service_name="bedrock", region_name=aws_region)
    
    fm_models = list_foundation_models(bedrock_client)
    for model in fm_models:
        print(f"Model: {model["modelName"]}")
        print(json.dumps(model, indent=2))
        print("---------------------------\n")
    
    logger.info("Done.")

if __name__ == "__main__":
    main()
```

If the script is successful, the response returns a list of foundation models that are available in Amazon Bedrock.

## Submit a text prompt to a model and generate a text response with InvokeModel
<a name="getting-started-api-ex-python-invoke-text"></a>

The following example runs the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) operation using an Amazon Bedrock client. `InvokeModel` lets you submit a prompt to generate a model response. Run the following SDK for Python script to create an Amazon Bedrock runtime client and generate a text response with the `` operation:

```
# Use the native inference API to send a text message to Amazon Nova Micro.

import boto3
import json

from botocore.exceptions import ClientError

# Create an Amazon Bedrock Runtime client.
brt = boto3.client("bedrock-runtime")

# Set the model ID, e.g., Amazon Nova Micro.
model_id = "amazon.nova-micro-v1:0"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
native_request = {
    "messages": [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ],
    "inferenceConfig": {
        "maxTokens": 512,
        "temperature": 0.5,
        "topP": 0.9
    },
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = brt.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["output"]["message"]["content"][0]["text"]
print(response_text)
```

If the command is successful, the response returns the text generated by the model in response to the prompt.

## Submit a text prompt to a model and generate a text response with Converse
<a name="getting-started-api-ex-python-converse"></a>

The following example runs the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) operation using an Amazon Bedrock client. We recommend using `Converse` operation over `InvokeModel` when supported, because it unifies the inference request across Amazon Bedrock models and simplifies the management of multi-turn conversations. Run the following SDK for Python script to create an Amazon Bedrock runtime client and generate a text response with the `Converse` operation:

```
# Use the Conversation API to send a text message to Amazon Nova Micro.

import boto3
from botocore.exceptions import ClientError

# Create an Amazon Bedrock Runtime client.
brt = boto3.client("bedrock-runtime")

# Set the model ID, e.g., Amazon Nova Micro.
model_id = "amazon.nova-micro-v1:0"

# Start a conversation with the user message.
user_message = "Describe the purpose of a 'hello world' program in one line."
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = brt.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
```

If the command is successful, the response returns the text generated by the model in response to the prompt.