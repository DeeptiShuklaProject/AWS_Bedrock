

# Required Key policy elements to encrypt your model evaluation job using AWS KMS
<a name="model-evaluation-security-kms"></a>

Every AWS KMS key must have exactly one key policy. The statements in the key policy determine who has permission to use the AWS KMS key and how they can use it. You can also use IAM policies and grants to control access to the AWS KMS key, but every AWS KMS key must have a key policy.

**Required AWS KMS key policy elements in Amazon Bedrock**
+ `kms:Decrypt` — For files that you've encrypted with your AWS Key Management Service key, provides Amazon Bedrock with permissions to access and decrypt those files.
+ `kms:GenerateDataKey` — Controls permission to use the AWS Key Management Service key to generate data keys. Amazon Bedrock uses `GenerateDataKey` to encrypt the temporary data it stores for the evaluation job.
+ `kms:DescribeKey` — Provides detailed information about a KMS key. 

You must add the following statement to your existing AWS KMS key policy. It provides Amazon Bedrock with permissions to temporarily store your data in an Amazon Bedrock service bucket using the AWS KMS that you've specified.

```
{
	"Effect": "Allow",
	"Principal": {
	    "Service": "bedrock.amazonaws.com"
	},
	"Action": [
	    "kms:GenerateDataKey",
	    "kms:Decrypt",
	    "kms:DescribeKey"
	],
	"Resource": "*",
	"Condition": {
	    "StringLike": {
	        "kms:EncryptionContext:evaluationJobArn": "arn:aws:bedrock:{{region}}:{{accountId}}:evaluation-job/*",
	        "aws:SourceArn": "arn:aws:bedrock:{{region}}:{{accountId}}:evaluation-job/*"
	    }
	}
}
```

The following is an example of a complete AWS KMS policy.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "key-consolepolicy-3",
    "Statement": [
        {
            "Sid": "EnableIAMUserPermissions",
            "Effect": "Allow",
            "Principal": {
            "AWS": "arn:aws:iam::{{111122223333}}:root"
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "BedrockDataKeyAndDecrypt",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "*",
            "Condition": {
                "ArnLike": {
                    "kms:EncryptionContext:evaluationJobArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:evaluation-job/*",
                    "aws:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:evaluation-job/*"
                }
            }
        },
        {
            "Sid": "BedrockDescribeKey",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "kms:DescribeKey",
            "Resource": "*",
            "Condition": {
                "ArnLike": {
                    "aws:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:evaluation-job/*"
                }
            }
        }
    ]
}
```

------

## Setting up KMS permissions for roles calling CreateEvaluationJob API
<a name="model-evaluation-kms-create-job"></a>

Make sure you have DescribeKey, GenerateDataKey, and Decrypt permissions for your role used to create the evaluation job on the KMS key that you use in your evaluation job.

Example KMS key policy

```
{
    "Statement": [
       {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::account-id:role/APICallingRole"
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kmsDescribeKey"
            ],
            "Resource": "*"
       }
   ]
}
```

Example IAM Policy for Role Calling CreateEvaluationJob API

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CustomKMSKeyProvidedToBedrockEncryption",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{keyYouUse}}"
            ]
        }
    ]
}
```

------