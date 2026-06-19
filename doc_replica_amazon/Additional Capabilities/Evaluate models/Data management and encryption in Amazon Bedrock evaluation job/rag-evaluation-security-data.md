

# Data encryption for knowledge base evaluation jobs
<a name="rag-evaluation-security-data"></a>

During a knowledge base evaluation job, Amazon Bedrock makes a temporary copy of your data. Amazon Bedrock deletes the data after the job finishes. To encrypt the data, Amazon Bedrock uses a KMS key. It uses either a KMS key that you specify or a key that Amazon Bedrock owns.

Amazon Bedrock requires the IAM and AWS KMS permissions in the following sections so that it can use your KMS key to do the following:
+ Decrypt your data.
+ Encrypt the temporary copy that Amazon Bedrock makes.

When you create a knowledge base evaluation job, you can choose to use a KMS key that Amazon Bedrock owns, or you can choose your own customer-managed key. If you don't specify a customer-managed key, Amazon Bedrock uses its key by default.

Before you can use a customer-managed key, you must do the following:
+ Add the required IAM actions and resources to the IAM service role’s policy.
+ Add the required KMS key policy elements.
+ Create a policy that can interact with your customer-managed key. This is specified in a separate KMS key policy.

## Required policy elements
<a name="rag-evel-policy-elements"></a>

The IAM and KMS key policies in the following sections include the following required elements:
+ `kms:Decrypt` – For files that you've encrypted with your KMS key, provides Amazon Bedrock with permissions to access and decrypt those files.
+ `kms:GenerateDataKey` – Controls permission to use the KMS key to generate data keys. Amazon Bedrock uses `GenerateDataKey` to encrypt the temporary data that it stores for the evaluation job.
+ `kms:DescribeKey` – Provides detailed information about a KMS key.
+ `kms:ViaService` – The condition key limits use of a KMS key to request from specified AWS services. You must specify the following services:
  + Amazon S3, because Amazon Bedrock stores a temporary copy of your data in an Amazon S3 location that Amazon Bedrock owns.
  + Amazon Bedrock, because the evaluation service calls the Amazon Bedrock Knowledge Bases API to execute the knowledge base workflow.
+ `kms:EncryptionContext:context-key` – This condition key limits access to the AWS KMS operations so that they are specific only to the provided [encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html).

## IAM policy requirements
<a name="rag-eval-iam-policies"></a>

In the IAM role that you use to with Amazon Bedrock, the associated IAM policy must have the following elements. To learn more about managing your AWS KMS keys, see [Using IAM policies with AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies.html).

Knowledge base evaluation jobs in Amazon Bedrock use AWS owned keys. For more information about AWS owned keys, see [AWS owned keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk) in the *AWS Key Management Service Developer Guide*.

The following is an example IAM policy that contains only the required AWS KMS actions and resources:

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
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ],
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": [
                        "s3.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "CustomKMSKeyProvidedToBedrockEvalKMS",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ],
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:evaluationJobArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:evaluation-job/*"
                }
            }
        },
        {
            "Sid": "CustomKMSKeyProvidedToBedrockKBDecryption",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ],
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:knowledgeBaseArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/*"
                }
            }
        },
        {
            "Sid": "CustomKMSKeyProvidedToBedrockKBEncryption",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ],
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:knowledgeBaseArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/*"
                },
                "StringEquals": {
                    "kms:ViaService": [
                        "bedrock.us-east-1.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "CustomKMSKeyProvidedToBedrockKBGenerateDataKey",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ],
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:CustomerAwsAccountId": "{{123456789012}}",
                    "kms:EncryptionContext:SessionId": "*"
                },
                "StringEquals": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "CustomKMSDescribeKeyProvidedToBedrock",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/*"
            ]
        }
    ]
}
```

------

## AWS KMS key policy requirements
<a name="rag-eval-kms-policies"></a>

Every KMS key must have one key policy. The statements in the key policy determine who has permission to use the KMS key and how they can use it. You can also use IAM policies and grants to control access to the KMS keys, but every KMS key must have a key policy.

You must add the following statement to your existing KMS key policy. It provides Amazon Bedrock with permissions to temporarily store your data in an S3 bucket using the KMS key that you've specified.

### Setting up KMS permissions for roles calling CreateEvaluationJob API
<a name="model-evaluation-kms-create-job-2"></a>

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