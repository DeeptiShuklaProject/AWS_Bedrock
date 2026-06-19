

# Session encryption
<a name="sessions-encryption"></a>

By default, Amazon Bedrock uses AWS-managed keys for session encryption. For more information about the default encryption Amazon Bedrock uses, see [Data encryption](https://docs.aws.amazon.com/bedrock/latest/userguide/data-encryption.html).

 For an additional layer of security, you can encrypt session data with a customer managed key. To use your own key, specify the Amazon Resource Name (ARN) of the key for the `KMSKeyArn` in the [CreateSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_CreateSession.html) API operation. The user or role creating the session must have permission to use the key. You can use the following IAM policy to grant the required permissions. 

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
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:GenerateDataKey"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:aws:bedrock:session:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:session/*"
                },
                "StringEquals": {
                    "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
                }
            }
        }
    ]
}
```

------