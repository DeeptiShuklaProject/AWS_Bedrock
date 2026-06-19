

# Run example Amazon Bedrock API requests using an Amazon SageMaker AI notebook
<a name="getting-started-api-ex-sm"></a>

This section guides you through trying out some common operations in Amazon Bedrock with an Amazon SageMaker AI notebook to test that your Amazon Bedrock role permissions are set up properly. Before you run the following examples, you should check that you have fulfilled the following prerequisites:

**Prerequisites**
+ You have an AWS account and have permissions to access a role with the necessary permissions for Amazon Bedrock. Otherwise, follow the steps at [Quickstart](getting-started.md).
+ Carry out the following steps to set up IAM permissions for SageMaker AI and create a notebook:

  1. Modify the [trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#term_trust-policy) of the Amazon Bedrock role that you set up in [Quickstart](getting-started.md) through the [console](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy), [CLI](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-cli.html#roles-managingrole_edit-trust-policy-cli), or [API](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-api.html#roles-managingrole_edit-trust-policy-api). Attach the following trust policy to the role to allow both the Amazon Bedrock and SageMaker AI services to assume the Amazon Bedrock role:

------
#### [ JSON ]

****  

     ```
     {
         "Version":"2012-10-17",		 	 	 
         "Statement": [
             {
                 "Sid": "BedrockTrust",
                 "Effect": "Allow",
                 "Principal": {
                     "Service": "bedrock.amazonaws.com"
                 },
                 "Action": "sts:AssumeRole"
             },
             {
                 "Sid": "SagemakerTrust",
                 "Effect": "Allow",
                 "Principal": {
                     "Service": "sagemaker.amazonaws.com"
                 },
                 "Action": "sts:AssumeRole"
             }
         ]
     }
     ```

------

  1. Sign into the Amazon Bedrock role whose trust policy you just modified.

  1. Follow the steps at [Create an Amazon SageMaker AI Notebook Instance for the tutorial](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-setup-working-env.html) and specify the ARN of the Amazon Bedrock role that you created to create an SageMaker AI notebook instance.

  1. When the **Status** of the notebook instance is **InService**, choose the instance and then choose **Open JupyterLab**.

After you open up your SageMaker AI notebook, you can try out the following examples:

**Topics**
+ [List the foundation models that Amazon Bedrock has to offer](#getting-started-api-ex-sm-listfm)
+ [Submit a text prompt to a model and generate a response](#getting-started-api-ex-sm-converse)

## List the foundation models that Amazon Bedrock has to offer
<a name="getting-started-api-ex-sm-listfm"></a>

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

## Submit a text prompt to a model and generate a response
<a name="getting-started-api-ex-sm-converse"></a>

The following example runs the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) operation using an Amazon Bedrock client. `Converse` lets you submit a prompt to generate a model response. Run the following SDK for Python script to create an Amazon Bedrock runtime client and test the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) operation:

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