

# Access and security for Amazon Nova models
<a name="rft-access-security"></a>

Before you begin reinforcement fine-tuning, make sure that you understand what kind of access Amazon Bedrock needs for RFT-specific operations. RFT requires additional permissions beyond standard fine-tuning due to its reward function execution capabilities.

For basic model customization security setup including trust relationships, Amazon S3 permissions, and KMS encryption, see [Create an IAM service role for model customization](custom-model-job-access-security.md#custom-model-job-service-role).

## Prerequisites
<a name="rft-access-prerequisites"></a>

Before adding RFT-specific IAM permissions, you must add the following IAM service roles:
+ [Trust relationship](custom-model-job-access-security.md#custom-model-job-service-role-trust-relationship)
+ [Permissions to access training and validation files and to write output files in S3](custom-model-job-access-security.md#custom-model-job-service-role-s3-permissions)

## RFT-specific IAM permissions
<a name="rft-iam-permissions"></a>

Add these permissions to your existing model customization service role for RFT functionality.

### Lambda permissions for reward functions
<a name="rft-lambda-permissions"></a>

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

### Invocation log access
<a name="rft-api-log-permissions"></a>

To use existing Amazon Bedrock model invocation logs as training data, add permissions to access your Amazon S3 bucket where invocation logs are stored. 

You need to provide Amazon S3 bucket access permissions for the input bucket. The following shows an example policy you can use:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{s3-invocation-logs-bucket}}",
                "arn:aws:s3:::{{s3-invocation-logs-bucket}}/*"
            ]
        }
    ]
}
```

For security setup including basic IAM roles, Amazon S3 permissions, and encryption, see [Create an IAM service role for model customization](custom-model-job-access-security.md#custom-model-job-service-role).

## Grader Lambda function permissions for RLAIF
<a name="rft-grader-lambda-permissions"></a>

If you create your own Lambda function for Reinforcement Learning from AI Feedback (RLAIF) reward functions, you need to add specific permissions to the Lambda execution role.

### Bedrock permissions for LLM judges
<a name="rft-bedrock-permissions"></a>

For LLM-as-Judge reward functions (RLAIF), add permissions to invoke foundation models. The following shows an example policy you can use for your Lambda execution role.

**Note**  
Only add these permissions to your Lambda execution role if you create your own Lambda function. The console handles this automatically when creating Lambda functions through the console.

The following is an example for bedrock LLM as judge invocation using foundation models:

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

The following is an example for bedrock LLM as judge invocation using inference profile:

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
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{amazon.nova-premier-v1:0}}",
                "arn:aws:bedrock:{{us-east-2}}::foundation-model/{{amazon.nova-premier-v1:0}}",
                "arn:aws:bedrock:{{us-west-2}}::foundation-model/{{amazon.nova-premier-v1:0}}"
            ],
            "Condition": {
                "StringLike": {
                    "bedrock:InferenceProfileArn": "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:inference-profile/{{us.amazon.nova-premier-v1:0}}"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:inference-profile/{{us.amazon.nova-premier-v1:0}}"
            ]
        }
    ]
}
```

For information about inference profile prerequisites, see [ Prerequisites for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html).