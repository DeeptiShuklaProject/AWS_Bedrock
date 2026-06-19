

# Create a service role for model customization
<a name="model-customization-iam-role"></a>

To use a custom role for model customization instead of the one Amazon Bedrock automatically creates, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
+ Trust relationship
+ Permissions to access your training and validation data in S3 and to write your output data to S3
+ (Optional) If you encrypt any of the following resources with a KMS key, permissions to decrypt the key (see [Encryption of custom models](encryption-custom-job.md))
  + A model customization job or the resulting custom model
  + The training, validation, or output data for the model customization job

**Topics**
+ [Trust relationship](#model-customization-iam-role-trust)
+ [Permissions to access training and validation files and to write output files in S3](#model-customization-iam-role-s3)
+ [(Optional) Permissions to create a Distillation job with a cross-region inference profiles](#customization-iam-sr-ip)

## Trust relationship
<a name="model-customization-iam-role-trust"></a>

The following policy allows Amazon Bedrock to assume this role and carry out the model customization job. The following shows an example policy you can use.

You can optionally restrict the scope of the permission for [cross-service confused deputy prevention](cross-service-confused-deputy-prevention.md) by using one or more global condition context keys with the `Condition` field. For more information, see [AWS global condition context keys.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
+ Set the `aws:SourceAccount` value to your account ID.
+ (Optional) Use the `ArnEquals` or `ArnLike` condition to restrict the scope to specific model customization jobs in your account ID.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
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
                    "aws:SourceArn": "arn:aws:bedrock:us-east-1:{{111122223333}}:model-customization-job/*"
                }
            }
        }
    ]
}
```

------

## Permissions to access training and validation files and to write output files in S3
<a name="model-customization-iam-role-s3"></a>

Attach the following policy to allow the role to access your training and validation data and the bucket to which to write your output data. Replace the values in the `Resource` list with your actual bucket names.

To restrict access to a specific folder in a bucket, add an `s3:prefix` condition key with your folder path. You can follow the **User policy** example in [Example 2: Getting a list of objects in a bucket with a specific prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#condition-key-bucket-ops-2) 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{training-bucket}}",
                "arn:aws:s3:::{{training-bucket/*}}",
                "arn:aws:s3:::{{validation-bucket}}",
                "arn:aws:s3:::{{validation-bucket/*}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{output-bucket}}",
                "arn:aws:s3:::{{output-bucket/*}}"
            ]
        }
    ]
}
```

------

## (Optional) Permissions to create a Distillation job with a cross-region inference profiles
<a name="customization-iam-sr-ip"></a>

To use a cross-region inference profile for a teacher model in a distillation job, the service role must have permissions to invoke the inference profile in an AWS Region, in addition to the model in each Region in the inference profile.

For permissions to invoke with a cross-Region (system-defined) inference profile, use the following policy as a template for the permissions policy to attach to your service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CrossRegionInference",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:inference-profile/{{${InferenceProfileId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}"
            ]
        }
    ]
}
```

------