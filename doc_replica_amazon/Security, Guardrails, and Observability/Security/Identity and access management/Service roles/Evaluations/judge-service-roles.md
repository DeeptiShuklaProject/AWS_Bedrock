

# Required service role permissions for creating a model evaluation job that uses a judge model
<a name="judge-service-roles"></a>

To create a model evaluation job that uses a LLM as judge, you must specify a service role. The policy you attach grants Amazon Bedrock access to resources in your account, and allows Amazon Bedrock to invoke the selected model on your behalf.

The trust policy defines Amazon Bedrock as the service principal using `bedrock.amazonaws.com`. Each of the following policy examples shows you the exact IAM actions that are required based on each service invoked in the model evaluation job

To create a custom service role as described below, see [Creating a role that uses a custom trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html) in the *IAM User Guide*.

## Required Amazon Bedrock IAM actions
<a name="judge-service-roles-br"></a>

You need to create a policy that allows Amazon Bedrock to invoke the models you plan to specify in the model evaluation job. To learn more about managing access to Amazon Bedrock models, see [Request access to models](model-access.md). In the `"Resource"` section of the policy, you must specify at least one ARN of a model you have access too. To use a model encrypted with customer managed key KMS key, you must add the required IAM actions and resources to the IAM service role policy. You must also add the service role to the AWS KMS key policy.

The service role must include access to at least one supported evaluator model. For a list of currently supported evaluator models, see [Supported models](evaluation-judge.md#evaluation-judge-supported).

------
#### [ JSON ]

****  

```
{
	"Version":"2012-10-17",		 	 	 
	"Statement": [
		{
			"Sid": "BedrockModelInvoke",
			"Effect": "Allow",
			"Action": [
				"bedrock:InvokeModel",
				"bedrock:CreateModelInvocationJob",
				"bedrock:StopModelInvocationJob"
			],
			"Resource": [
				"arn:aws:bedrock:us-east-1::foundation-model/*",
				"arn:aws:bedrock:us-east-1:111122223333:inference-profile/*",
				"arn:aws:bedrock:us-east-1:111122223333:provisioned-model/*",
				"arn:aws:bedrock:us-east-1:111122223333:imported-model/*"
			]
		}
	]
}
```

------

## Required Amazon S3 IAM actions and resources
<a name="judge-service-roles-s3"></a>

Your service role policy needs to include access to the Amazon S3 bucket where you want the output of model evaluation jobs saved, and access to the prompt dataset you have specified in your `CreateEvaluationJob` request or via the Amazon Bedrock console.

------
#### [ JSON ]

****  

```
{
	"Version":"2012-10-17",		 	 	 
	"Statement": [
		{
			"Sid": "FetchAndUpdateOutputBucket",
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
				"arn:aws:s3:::my_customdataset1_bucket",
	            "arn:aws:s3:::my_customdataset1_bucket/myfolder",
	            "arn:aws:s3:::my_customdataset2_bucket",
				"arn:aws:s3:::my_customdataset2_bucket/myfolder"
			]
		}
	]
}
```

------