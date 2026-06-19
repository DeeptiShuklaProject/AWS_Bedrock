

# Service role requirements for automatic model evaluation jobs
<a name="automatic-service-roles"></a>

To create an automatic model evaluation job, you must specify a service role. The policy you attach grants Amazon Bedrock access to resources in your account, and allows Amazon Bedrock to invoke the selected model on your behalf.

You must also attach a trust policy that defines Amazon Bedrock as the service principal using `bedrock.amazonaws.com`. Each of the following policy examples shows you the exact IAM actions that are required based on each service invoked in an automatic model evaluation job.

To create a custom service role, see [Creating a role that uses a custom trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html) in the *IAM User Guide*.

**Required Amazon S3 IAM actions**  
The following policy example grants access to the S3 buckets where your model evaluation results are saved, and (optionally) access to any custom prompt datasets you have specified.

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
            "arn:aws:s3:::my_customdataset1_bucket",
            "arn:aws:s3:::my_customdataset1_bucket/myfolder",
            "arn:aws:s3:::my_customdataset2_bucket",
            "arn:aws:s3:::my_customdataset2_bucket/myfolder"
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
            "arn:aws:s3:::my_output_bucket",
            "arn:aws:s3:::my_output_bucket/myfolder"
        ]
    }
]
}
```

------

**Required Amazon Bedrock IAM actions**  
You also need to create a policy that allows Amazon Bedrock to invoke the model you plan to specify in the automatic model evaluation job. To learn more about managing access to Amazon Bedrock models, see [Request access to models](model-access.md). In the `"Resource"` section of the policy, you must specify at least one ARN of a model you have access too. To use a model encrypted with customer managed key KMS key, you must add the required IAM actions and resources to the IAM service role policy. You must also add the service role to the AWS KMS key policy.

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

**Service principal requirements**  
You must also specify a trust policy that defines Amazon Bedrock as the service principal. This allows Amazon Bedrock to assume the role. The wildcard (`*`) model evaluation job ARN is required so that Amazon Bedrock can create model evaluation jobs in your AWS account.

------
#### [ JSON ]

****  

```
{
"Version":"2012-10-17",		 	 	 
"Statement": [{
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
}]
}
```

------