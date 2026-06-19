

# Required permissions for batch inference
<a name="batch-inference-permissions"></a>

To carry out batch inference, you must set up permissions for the following IAM identities:

**Warning**  
Foundation model resources used in batch inference are owned by the Amazon Bedrock service, not by your AWS account. If your IAM policies include organization-based conditions on resources (such as `aws:ResourceOrgID`), batch inference requests to foundation models will fail with `AccessDeniedException`. Remove organization resource conditions from policies that apply to Amazon Bedrock foundation model resources.
+ The IAM identity that will create and manage batch inference jobs.
+ The batch inference [service role](security-iam-sr.md) that Amazon Bedrock assumes to perform actions on your behalf.

To learn how to set up permissions for each identity, navigate through the following topics:

**Topics**
+ [Required permissions for an IAM identity to submit and manage batch inference jobs](#batch-inference-permissions-user)
+ [Required permissions for a service role to carry out batch inference](#batch-inference-permissions-service)

## Required permissions for an IAM identity to submit and manage batch inference jobs
<a name="batch-inference-permissions-user"></a>

For an IAM identity to use this feature, you must configure it with the necessary permissions. To do so, do one of the following:
+ To allow an identity to carry out all Amazon Bedrock actions, attach the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) policy to the identity. If you do this, you can skip this topic. This option is less secure.
+ As a security best practice, you should grant only the necessary actions to an identity. This topic describes the permissions that you need for this feature.

To restrict permissions to only actions that are used for batch inference, attach the following identity-based policy to an IAM identity:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "BatchInference",
            "Effect": "Allow",
            "Action": [  
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel",
                "bedrock:ListInferenceProfiles",
                "bedrock:GetInferenceProfile",
                "bedrock:ListCustomModels",
                "bedrock:GetCustomModel",
                "bedrock:TagResource", 
                "bedrock:UntagResource", 
                "bedrock:ListTagsForResource",
                "bedrock:CreateModelInvocationJob",
                "bedrock:GetModelInvocationJob",
                "bedrock:ListModelInvocationJobs",
                "bedrock:StopModelInvocationJob"
            ],
            "Resource": "*"
        }
    ]   
}
```

------

To further restrict permissions, you can omit actions, or you can specify resources and condition keys by which to filter permissions. For more information about actions, resources, and condition keys, see the following topics in the *Service Authorization Reference*:
+ [Actions defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) – Learn about actions, the resource types that you can scope them to in the `Resource` field, and the condition keys that you can filter permissions on in the `Condition` field.
+ [Resource types defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-resources-for-iam-policies) – Learn about the resource types in Amazon Bedrock.
+ [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) – Learn about the condition keys in Amazon Bedrock.

The following policy is an example that scopes down permissions for batch inference to only allow a user with the account ID `123456789012` to create batch inference jobs in the `us-west-2` Region, using the Anthropic Claude 3 Haiku model:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CreateBatchInferenceJob",
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateModelInvocationJob"
            ],
            "Resource": [
                "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                "arn:aws:bedrock:us-west-2:123456789012:model-invocation-job/*"
            ]
        }
    ]
}
```

------

## Required permissions for a service role to carry out batch inference
<a name="batch-inference-permissions-service"></a>

Batch inference is carried out by a [service role](security-iam-sr.md) that assumes your identity to perform actions on your behalf. You can create a service role in the following ways:
+ Let Amazon Bedrock automatically create a service role with the necessary permissions for you by using the AWS Management Console. You can select this option when you create a batch inference job.
+ Create a custom service role for Amazon Bedrock by using AWS Identity and Access Management and attach the necessary permissions. When you submit the batch inference job, you then specify this role. For more information about creating a custom service role for batch inference, see [Create a custom service role for batch inference](batch-iam-sr.md). For more general information about creating service roles, see [Create a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) in the IAM User Guide.

**Important**  
If the S3 bucket in which you [uploaded your data for batch inference](batch-inference-data.md) is in a different AWS account, you must configure an S3 bucket policy to allow the service role access to the data. You must manually configure this policy even if you use the console to automatically create a service role. To learn how to configure an S3 bucket policy for Amazon Bedrock resources, see [Attach a bucket policy to an Amazon S3 bucket to allow another account to access it](s3-bucket-access.md#s3-bucket-access-cross-account).
Foundation models in Amazon Bedrock are AWS-managed resources that cannot be used with IAM policy conditions requiring customer ownership. These models are owned and operated by AWS, and cannot be owned by individual customers. Any IAM policy condition that checks for customer-owned resources (such as conditions using resource tags, organization ID, or other ownership attributes) will fail when applied to foundation models, potentially blocking legitimate access to these services.  
For example, if your policy includes an `aws:ResourceOrgID` condition like this:  

  ```
  {
    "Condition": {
      "StringEqualsIgnoreCase": {
        "aws:ResourceOrgID": ["o-xxxxxxxx"]
      }
    }
  }
  ```
Your batch inference job will fail with `AccessDeniedException`. Remove the `aws:ResourceOrgID` condition or create separate policy statements for foundation models.