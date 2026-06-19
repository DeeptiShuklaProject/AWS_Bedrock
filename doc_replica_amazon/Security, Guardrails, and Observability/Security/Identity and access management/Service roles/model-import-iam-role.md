

# Create a service role for importing pre-trained models
<a name="model-import-iam-role"></a>

To use a custom role for model import create an IAM service role and attach the following permissions. For information on how to create a service role in IAM, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

These permissions apply to both methods of importing models into Amazon Bedrock:
+ **Custom model import jobs** — For importing customized open-source foundation models (such as Mistral AI or Llama models). For more information, see [Use Custom model import to import a customized open-source model into Amazon Bedrock](model-customization-import-model.md).
+ **Create custom model** — For importing Amazon Nova models that you fine-tuned in SageMaker AI. For more information, see [Import a SageMaker AI-trained Amazon Nova model](import-with-create-custom-model.md).

**Topics**
+ [Trust relationship](#model-import-iam-role-trust)
+ [Permissions to access model files in Amazon S3](#model-import-iam-role-s3)

## Trust relationship
<a name="model-import-iam-role-trust"></a>

The following policy allows Amazon Bedrock to assume this role and carry out model import operations. The following shows an example policy you can use.

You can optionally restrict the scope of the permission for [cross-service confused deputy prevention](cross-service-confused-deputy-prevention.md) by using one or more global condition context keys with the `Condition` field. For more information, see [AWS global condition context keys.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
+ Set the `aws:SourceAccount` value to your account ID.
+ (Optional) Use the `ArnEquals` or `ArnLike` condition to restrict the scope to specific operations in your account. The following example restricts access to custom model import jobs.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "1",
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
                    "aws:SourceArn": "arn:aws:bedrock:us-east-1:{{111122223333}}:model-import-job/*"
                }
            }
        }
    ]
}
```

------

## Permissions to access model files in Amazon S3
<a name="model-import-iam-role-s3"></a>

Attach the following policy to allow the role to access model files in Amazon S3 bucket. Replace the values in the `Resource` list with your actual bucket names.

For custom model import jobs, this is your own Amazon S3 bucket containing the customized open-source model files. For creating custom models from SageMaker AI-trained Amazon Nova models, this is the Amazon-managed Amazon S3 bucket where SageMaker AI stores the trained model artifacts. SageMaker AI creates this bucket when you run your first SageMaker AI training job. 

To restrict access to a specific folder in a bucket, add an `s3:prefix` condition key with your folder path. You can follow the **User policy** example in [Example 2: Getting a list of objects in a bucket with a specific prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#condition-key-bucket-ops-2) 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{bucket}}",
                "arn:aws:s3:::{{bucket}}/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        }
    ]
}
```

------