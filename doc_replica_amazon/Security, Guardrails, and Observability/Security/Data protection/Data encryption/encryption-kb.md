

# Encryption of knowledge base resources
<a name="encryption-kb"></a>

Amazon Bedrock encrypts resources related to your knowledge bases. By default, Amazon Bedrock encrypts this data using an AWS-owned key. Optionally, you can encrypt the model artifacts using a customer managed key.

**Fully managed knowledge bases**

Encryption with a KMS key can occur with the following processes:
+ Transient data storage while ingesting your data sources
+ Permanent data storage while storing your data sources
+ Querying a knowledge base

The following resources used by your knowledge bases can be encrypted with a KMS key. If you encrypt them, you need to add permissions to decrypt the KMS key.
+ Data sources stored in an Amazon S3 bucket

**Custom knowledge bases (vector store)**

Encryption with a KMS key can occur with the following processes:
+ Transient data storage while ingesting your data sources
+ Passing information to OpenSearch Service if you let Amazon Bedrock set up your vector database
+ Querying a knowledge base

The following resources used by your knowledge bases can be encrypted with a KMS key. If you encrypt them, you need to add permissions to decrypt the KMS key.
+ Data sources stored in an Amazon S3 bucket
+ Third-party vector stores

For more information about AWS KMS keys, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the *AWS Key Management Service Developer Guide*.

**Note**  
Amazon Bedrock knowledge bases uses TLS encryption for communication with third-party data source connectors and vector stores where the provider permits and supports TLS encryption in transit.

**Topics**
+ [Encryption of data storage in fully managed knowledge base](#encryption-kb-managed-ingestion)
+ [Encryption of knowledge base retrieval](#encryption-kb-runtime)
+ [Encryption of transient data storage during data ingestion](#encryption-kb-ingestion)
+ [Encryption of information passed to Amazon OpenSearch Service](#encryption-kb-oss)
+ [Encryption of information passed to Amazon S3 Vectors](#encryption-kb-s3-vector)
+ [Permissions to decrypt your AWS KMS key for your data sources in Amazon S3](#encryption-kb-ds)
+ [Permissions to decrypt an AWS Secrets Manager secret for the vector store containing your knowledge base](#encryption-kb-3p)
+ [Permissions for Bedrock Data Automation (BDA) with AWS KMS encryption](#encryption-kb-bda)

## Encryption of data storage in fully managed knowledge base
<a name="encryption-kb-managed-ingestion"></a>

When you create a fully managed knowledge base, you can encrypt the data with a custom KMS key. The KMS key is specified during knowledge base creation and applies to both transient data storage during ingestion and permanent data storage for indexing.

Amazon Bedrock uses a single KMS key, which you specify when you create the knowledge base, to encrypt all of the data in your knowledge base. This includes transient data while your data sources are being ingested and permanent data that is stored for indexing and retrieval.

When you create a fully managed knowledge base with a customer managed key, Amazon Bedrock verifies that it can use the key and then creates a grant on the key. Amazon Bedrock uses this grant to encrypt and decrypt your data during ingestion, indexing, and retrieval, and retires the grant when you delete the knowledge base.

You provide these permissions in the key policy of your AWS KMS key for the IAM identity that creates the knowledge base, as shown in the following example. Replace the example values with your own AWS Region, account ID, and the IAM role or user that creates the knowledge base. The IAM service role that is associated with the knowledge base (the role that Amazon Bedrock uses to read your data sources) does not require any permissions on the KMS key.

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/{{role-name}}"
            },
            "Action": [
                "kms:CreateGrant"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "bedrock.{{region}}.amazonaws.com"
                },
                "ForAllValues:StringEquals": {
                    "kms:GrantOperations": [
                        "CreateGrant",
                        "GenerateDataKey",
                        "GenerateDataKeyWithoutPlaintext",
                        "DescribeKey",
                        "Encrypt",
                        "Decrypt"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/{{role-name}}"
            },
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "bedrock.{{region}}.amazonaws.com"
                }
            }
        }
    ]
}
```

### Monitor your encryption keys for fully managed knowledge bases
<a name="encryption-kb-managed-monitor"></a>

When you use an AWS KMS customer managed key with your knowledge base, you can use [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) or [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to track the requests that Amazon Bedrock sends to AWS KMS.

The following is an example AWS CloudTrail event for that shows the grant that Amazon Bedrock creates on your AWS KMS key when you create a fully managed knowledge base:

```
{
    "eventVersion": "1.09",
    "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROAIGDTESTANDEXAMPLE:SampleUser01",
        "arn": "arn:aws:sts::111122223333:assumed-role/SampleRole/SampleUser01",
        "accountId": "111122223333",
        "accessKeyId": "EXAMPLE",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROAIGDTESTANDEXAMPLE",
                "arn": "arn:aws:iam::111122223333:role/SampleRole",
                "accountId": "111122223333",
                "userName": "SampleRole"
            },
            "attributes": {
                "creationDate": "2024-05-07T21:46:28Z",
                "mfaAuthenticated": "false"
            }
        },
        "invokedBy": "bedrock.amazonaws.com"
    },
    "eventTime": "2024-05-07T21:49:44Z",
    "eventSource": "kms.amazonaws.com",
    "eventName": "CreateGrant",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "bedrock.amazonaws.com",
    "userAgent": "bedrock.amazonaws.com",
    "requestParameters": {
        "granteePrincipal": "bedrock.amazonaws.com",
        "retiringPrincipal": "bedrock.amazonaws.com",
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE",
        "operations": [
            "Decrypt",
            "GenerateDataKey"
        ]
    },
    "responseElements": {
        "grantId": "0ab0ac0d0b000f00ea00cc0a0e00fc00bce000c000f0000000c0bc0a0000aaafSAMPLE",
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE"
    },
    "requestID": "ff000af-00eb-00ce-0e00-ea000fb0fba0SAMPLE",
    "eventID": "ff000af-00eb-00ce-0e00-ea000fb0fba0SAMPLE",
    "readOnly": false,
    "resources": [
        {
            "accountId": "111122223333",
            "type": "AWS::KMS::Key",
            "ARN": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE"
        }
    ],
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management"
}
```

## Encryption of knowledge base retrieval
<a name="encryption-kb-runtime"></a>

You can encrypt sessions in which you generate responses from querying a knowledge base with a KMS key. To do so, include the ARN of a KMS key in the `kmsKeyArn` field when making a [RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request. Attach the following policy, replacing the example values with your own AWS Region, account ID, and AWS KMS key ID to allow Amazon Bedrock to encrypt the session context.

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
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
        }
    ]
}
```

------

## Encryption of transient data storage during data ingestion
<a name="encryption-kb-ingestion"></a>

When you set up a data ingestion job for your custom knowledge base, you can encrypt the job with a custom KMS key.

To allow the creation of a AWS KMS key for transient data storage in the process of ingesting your data source, attach the following policy to your Amazon Bedrock service role. Replace the example values with your own AWS Region, account ID, and AWS KMS key ID.

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
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
            ]
        }
    ]
}
```

------

## Encryption of information passed to Amazon OpenSearch Service
<a name="encryption-kb-oss"></a>

If you opt to let Amazon Bedrock create a vector store in Amazon OpenSearch Service for your knowledge base, Amazon Bedrock can pass a KMS key that you choose to Amazon OpenSearch Service for encryption. To learn more about encryption in Amazon OpenSearch Service, see [Encryption in Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html).

## Encryption of information passed to Amazon S3 Vectors
<a name="encryption-kb-s3-vector"></a>

If you opt to let Amazon Bedrock create an S3 vector bucket and vector index in Amazon S3 Vectors for your knowledge base, Amazon Bedrock can pass a KMS key that you choose to Amazon S3 Vectors for encryption. To learn more about encryption in Amazon S3 Vectors, see [Encryption with Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bucket-encryption.html).

## Permissions to decrypt your AWS KMS key for your data sources in Amazon S3
<a name="encryption-kb-ds"></a>

You store the data sources for your knowledge base in your Amazon S3 bucket. To encrypt these documents at rest, you can use the Amazon S3 SSE-S3 server-side encryption option. With this option, objects are encrypted with service keys managed by the Amazon S3 service. 

For more information, see [Protecting data using server-side encryption with Amazon S3-managed encryption keys (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html) in the *Amazon Simple Storage Service User Guide*.

If you encrypted your data sources in Amazon S3 with a custom AWS KMS key, attach the following policy to your Amazon Bedrock service role to allow Amazon Bedrock to decrypt your key. Replace the example values with your own AWS Region, account ID, and AWS KMS key ID.

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
                "KMS:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
            ],
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": [
                        "s3.us-east-1.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

## Permissions to decrypt an AWS Secrets Manager secret for the vector store containing your knowledge base
<a name="encryption-kb-3p"></a>

If the vector store containing your knowledge base is configured with an AWS Secrets Manager secret, you can encrypt the secret with a custom AWS KMS key by following the steps at [Secret encryption and decryption in AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html).

If you do so, you attach the following policy to your Amazon Bedrock service role to allow it to decrypt your key. Replace the example values with your own AWS Region, account ID, and AWS KMS key ID.

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
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
            ]
        }
    ]
}
```

------

## Permissions for Bedrock Data Automation (BDA) with AWS KMS encryption
<a name="encryption-kb-bda"></a>

When using BDA to process multimodal content with customer-managed AWS KMS keys, additional permissions are required beyond the standard AWS KMS permissions.

Attach the following policy to your Amazon Bedrock service role to allow BDA to work with encrypted multimedia files. Replace the example values with your own AWS Region, account ID, and AWS KMS key ID.

```
{
    "Sid": "KmsPermissionStatementForBDA",
    "Effect": "Allow",
    "Action": [
        "kms:GenerateDataKey",
        "kms:Decrypt",
        "kms:DescribeKey",
        "kms:CreateGrant"
    ],
    "Resource": "arn:aws:kms:{{region}}:{{account-id}}:key/{{key-id}}",
    "Condition": {
        "StringEquals": {
            "aws:ResourceAccount": "{{account-id}}",
            "kms:ViaService": "bedrock.{{region}}.amazonaws.com"
        }
    }
}
```

The BDA-specific permissions include `kms:DescribeKey` and `kms:CreateGrant` actions, which are required for BDA to process encrypted audio, video, and image files.