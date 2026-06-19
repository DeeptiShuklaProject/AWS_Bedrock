

# Access and security for open-weight models
<a name="rft-open-weight-access-security"></a>

Before you begin reinforcement fine-tuning (RFT), make sure that you understand what kind of access Amazon Bedrock needs for RFT-specific operations. RFT requires additional permissions beyond standard fine-tuning due to its reward function execution capabilities.

## Prerequisites
<a name="fine-tuning-openai-prereq"></a>

Before using Amazon Bedrock's OpenAI-compatible fine-tuning APIs, ensure you have the following:

1. An AWS account with appropriate permissions to access Amazon Bedrock

1. **Authentication** – You can authenticate using:
   + Amazon Bedrock API key (required for OpenAI SDK and available for HTTP requests)
   + AWS credentials (supported for HTTP requests)
**Note**  
If you are using Amazon Bedrock short-term/long-term API keys, then make sure that your role has access to the following IAM policy permissions: `AmazonBedrockMantleFullAccess` and [Lambda permissions for reward functions](#openai-fine-tuning-lambda-permissions).

1. **OpenAI SDK (optional)** – Install the OpenAI Python SDK if using SDK-based requests.

1. **Environment variables** – Set the following environment variables:
   + `OPENAI_API_KEY` – Set to your Amazon Bedrock API key
   + `OPENAI_BASE_URL` – Set to the Amazon Bedrock endpoint for your region (for example, `https://bedrock-mantle.us-west-2.api.aws/v1`)

   For more information, see [Responses API](bedrock-mantle.md#bedrock-mantle-responses).

1. **Training data** formatted as JSONL files with the purpose `fine-tune`. For more information, see [Prepare data for open-weight models](rft-prepare-data-open-weight.md).

## Lambda permissions for reward functions
<a name="openai-fine-tuning-lambda-permissions"></a>

You must add Lambda invocation permissions. The following shows an example policy you can use:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:*:*:function:{{reward-function-name}}"
            ]
        }
    ]
}
```

You can also use Amazon Bedrock hosted models as Judges for setting up reward functions. You will need to add specific permissions to invoke foundation models to the Lambda execution role. In your lambda role, you can configure these managed policies for LLMs for grading. See [AmazonBedrockLimitedAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonBedrockLimitedAccess.html).

The following is an example for invoking Amazon Bedrock foundation models as judge using the Invoke API:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:foundation-model/*"
            ]
        }
    ]
}
```