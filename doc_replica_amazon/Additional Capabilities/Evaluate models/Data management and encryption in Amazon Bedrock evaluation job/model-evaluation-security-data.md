

# AWS Key Management Service support in model evaluation jobs
<a name="model-evaluation-security-data"></a>

Amazon Bedrock uses the following IAM and AWS KMS permissions to use your AWS KMS key to decrypt your files and access them. It saves those files to an internal Amazon S3 location managed by Amazon Bedrock and uses the following permissions to encrypt them.

## IAM policy requirements
<a name="model-evaluation-security-kms-policy-1"></a>

The IAM policy associated with the IAM role that you're using to make requests to Amazon Bedrock must have the following elements. To learn more about managing your AWS KMS keys, see [Using IAM policies with AWS Key Management Service](https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies.html).

Model evaluation jobs in Amazon Bedrock use AWS owned keys. These KMS keys are owned by Amazon Bedrock. To learn more about AWS owned keys, see [AWS owned keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk) in the *AWS Key Management Service Developer Guide*.

**Required IAM policy elements**
+ `kms:Decrypt` — For files that you've encrypted with your AWS Key Management Service key, provides Amazon Bedrock with permissions to access and decrypt those files.
+ `kms:GenerateDataKey` — Controls permission to use the AWS Key Management Service key to generate data keys. Amazon Bedrock uses `GenerateDataKey` to encrypt the temporary data it stores for the evaluation job.
+ `kms:DescribeKey` — Provides detailed information about a KMS key. 
+ `kms:ViaService` — The condition key limits use of an KMS key to requests from specified AWS services. You must specify Amazon S3 as a service because Amazon Bedrock stores a temporary copy of your data in an Amazon S3 location that it owns.

The following is an example IAM policy that contains only the required AWS KMS IAM actions and resources. 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CustomKMSKeyProvidedToBedrock",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/[[keyId]]"
            ]
        },
        {
            "Sid": "CustomKMSDescribeKeyProvidedToBedrock",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/[[keyId]]"
            ]
        }
    ]
}
```

------

### Setting up KMS permissions for roles calling CreateEvaluationJob API
<a name="model-evaluation-kms-create-job-1"></a>

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