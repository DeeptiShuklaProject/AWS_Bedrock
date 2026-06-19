

# Service role requirements for knowledge base evaluation jobs
<a name="rag-eval-service-roles"></a>

To create a knowledge base evaluation job, you must specify a service role. The policy that you attach to the role grants Amazon Bedrock access to resources in your account, and it allows Amazon Bedrock to do the following:
+ Invoke the models that you select for output generation with the `RetrieveAndGenerate` API action, and evaluate the knowledge base outputs.
+ Invoke the Amazon Bedrock Knowledge Bases `Retrieve` and `RetrieveAndGenerate` API actions on your knowledge base instance.

To create a custom service role, see [Creating a role that uses custom trust policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html) in the *IAM User Guide*.

**Required IAM actions for Amazon S3 access**  
The following example policy grants access to the S3 buckets where both of the following occur: 
+ You save your knowledge base evaluation results.
+ Amazon Bedrock reads your input dataset.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement":
    [
        {
            "Sid": "AllowAccessToCustomDatasets",
            "Effect": "Allow",
            "Action":
            [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource":
            [
                "arn:aws:s3:::{{my_customdataset1_bucket}}",
                "arn:aws:s3:::{{my_customdataset1_bucket/myfolder}}",
                "arn:aws:s3:::{{my_customdataset2_bucket}}",
                "arn:aws:s3:::{{my_customdataset2_bucket/myfolder}}"
            ]
        },
        {
            "Sid": "AllowAccessToOutputBucket",
            "Effect": "Allow",
            "Action":
            [
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:GetBucketLocation",
                "s3:AbortMultipartUpload",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource":
            [
                "arn:aws:s3:::{{my_output_bucket}}",
                "arn:aws:s3:::{{my_output_bucket/myfolder}}"
            ]
        }
    ]
}
```

------

**Required Amazon Bedrock IAM actions**  
You also need to create a policy that allows Amazon Bedrock to do the following:

1. Invoke the models that you plan to specify for the following: 
   + Result generation with the `RetrieveAndGenerate` API action.
   + Evaluation of results.

   For the `Resource` key in the policy, you must specify at least one ARN of a model you have access to. To use a model that's encrypted with a customer-managed KMS key, you must add the required IAM actions and resources to the IAM service role policy. You must also add the service role to the AWS KMS key policy.

1. Call the `Retrieve` and `RetrieveAndGenerate` API actions. Note that, in the automated role creation in the console, we give permissions to both `Retrieve` and `RetrieveAndGenerate` API actions, regardless of the action you choose to evaluate for that job. By doing so, we give additional flexibility and reusability for that role. However, for added security, that automatically-created role is tied to a single knowledge base instance.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AllowSpecificModels",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:CreateModelInvocationJob",
                "bedrock:StopModelInvocationJob",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:GetInferenceProfile",
                "bedrock:GetImportedModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:inference-profile/*",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:provisioned-model/*",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:imported-model/*",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:application-inference-profile/*"
            ]
        },
        {
            "Sid": "AllowKnowledgeBaseAPis",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{knowledge-base-id}}"
            ]
        }
    ]
}
```

------

**Service Principal Requirements**  
You must also specify a trust policy that defines Amazon Bedrock as the service principal. This policy allows Amazon Bedrock to assume the role. The wildcard (`*`) model evaluation job ARN is required so that Amazon Bedrock can create model evaluation jobs in your AWS account.

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
                    "aws:SourceAccount": "{{123456789012}}"
                },
                "ArnEquals": {
                    "aws:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:evaluation-job/*"
                }
            }
        }
    ]
}
```

------