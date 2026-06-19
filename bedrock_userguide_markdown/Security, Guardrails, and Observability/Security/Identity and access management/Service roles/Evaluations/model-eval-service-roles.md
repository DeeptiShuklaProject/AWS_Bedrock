

# Service role requirements for human-based model evaluation jobs
<a name="model-eval-service-roles"></a>

To create a model evaluation job that uses human evaluators, you must specify two service roles.

The following lists summarize the IAM policy requirements for each required service role that must be specified in the Amazon Bedrock console.

**Summary of IAM policy requirements for the Amazon Bedrock service role**
+ You must attach a trust policy which defines Amazon Bedrock as the service principal.
+ You must allow Amazon Bedrock to invoke the selected models on your behalf.
+ You must allow Amazon Bedrock to access the S3 bucket that holds your prompt dataset and the S3 bucket where you want the results saved.
+ You must allow Amazon Bedrock to create the required human loop resources in your account.
+ (Recommended) Use a `Condition` *block* to specify accounts that can access.
+ (Optional) You must allow Amazon Bedrock to decrypt your KMS key if you've encrypted your prompt dataset bucket or the Amazon S3 bucket where you want the results saved.

**Summary of IAM policy requirements for the Amazon SageMaker AI service role**
+ You must attach a trust policy which defines SageMaker AI as the service principal.
+ You must allow SageMaker AI to access the S3 bucket that holds your prompt dataset and the S3 bucket where you want the results saved.
+ (Optional) You must allow SageMaker AI to use your customer managed keys if you've encrypted your prompt dataset bucket or the location where you wanted the results.

To create a custom service role, see [Creating a role that uses a custom trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html) in the *IAM User Guide*.

**Required Amazon S3 IAM actions**  
The following policy example grants access to the S3 buckets where your model evaluation results are saved, and access to the custom prompt dataset you have specified. You need to attach this policy to both the SageMaker AI service role and the Amazon Bedrock service role.

------
#### [ JSON ]

****  

```
{
"Version":"2012-10-17",		 	 	 
"Statement": [
    {
        "Sid": "AllowAccessToCustomDatasets",
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:ListBucket"
        ],
        "Resource": [
            "arn:aws:s3:::{{custom-prompt-dataset}}"
        ]
    },
    {
        "Sid": "AllowAccessToOutputBucket",
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:ListBucket",
            "s3:PutObject",
            "s3:GetBucketLocation",
            "s3:AbortMultipartUpload",
            "s3:ListBucketMultipartUploads"
        ],
        "Resource": [
            "arn:aws:s3:::{{model_evaluation_job_output}}"
        ]
    }
]
}
```

------

**Required Amazon Bedrock IAM actions**  
To allow Amazon Bedrock to invoke the model you plan to specify in the automatic model evaluation job, attach the following policy to the Amazon Bedrock service role. In the `"Resource"` section of the policy, you must specify at least one ARN of a model you have access too. To use a model encrypted with customer managed key KMS key, you must add the required IAM actions and resources to the IAM service role. You must also add any required AWS KMS key policy elements.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AllowAccessToBedrockResources",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:CreateModelInvocationJob",
                "bedrock:StopModelInvocationJob",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:GetInferenceProfile", 
                "bedrock:ListInferenceProfiles",
                "bedrock:GetImportedModel",
                "bedrock:GetPromptRouter",
                "sagemaker:InvokeEndpoint"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/*",
                "arn:aws:bedrock:*:{{111122223333}}:inference-profile/*",
                "arn:aws:bedrock:*:{{111122223333}}:provisioned-model/*",
                "arn:aws:bedrock:*:{{111122223333}}:imported-model/*",
                "arn:aws:bedrock:*:{{111122223333}}:application-inference-profile/*",
                "arn:aws:bedrock:*:{{111122223333}}:default-prompt-router/*",
                "arn:aws:sagemaker:*:{{111122223333}}:endpoint/*",
                "arn:aws:bedrock:*:{{111122223333}}:marketplace/model-endpoint/all-access"
            ]
        }
    ]
}
```

------

**Required Amazon Augmented AI IAM actions**  
You also must create a policy that allows Amazon Bedrock to create resources related to human-based model evaluation jobs. Because Amazon Bedrock creates the needed resources to start the model evaluation job, you must use `"Resource": "*"`. You must attach this policy to the Amazon Bedrock service role.

------
#### [ JSON ]

****  

```
{
"Version":"2012-10-17",		 	 	 
"Statement": [
    {
        "Sid": "ManageHumanLoops",
        "Effect": "Allow",
        "Action": [
            "sagemaker:StartHumanLoop",
            "sagemaker:DescribeFlowDefinition",
            "sagemaker:DescribeHumanLoop",
            "sagemaker:StopHumanLoop",
            "sagemaker:DeleteHumanLoop"
        ],
        "Resource": "*"
    }
]
}
```

------

**Service principal requirements (Amazon Bedrock)**  
You must also specify a trust policy that defines Amazon Bedrock as the service principal. This allows Amazon Bedrock to assume the role.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AllowBedrockToAssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "111122223333"
                },
                "ArnEquals": {
                    "aws:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:evaluation-job/*"
                }
            }
        }
    ]
}
```

------

**Service principal requirements (SageMaker AI)**  
You must also specify a trust policy that defines Amazon Bedrock as the service principal. This allows SageMaker AI to assume the role.

------
#### [ JSON ]

****  

```
{
"Version":"2012-10-17",		 	 	 
"Statement": [
{
  "Sid": "AllowSageMakerToAssumeRole",
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