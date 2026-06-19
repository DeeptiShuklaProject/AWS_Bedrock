

# Encrypt agent sessions with customer managed key (CMK)
<a name="ltm-permissions"></a>

If you've enabled memory for your agent and if you encrypt agent sessions with a customer managed key, you must configure the following key policy and the calling identity IAM permissions to configure your customer managed key.

**Customer managed key policy**

Amazon Bedrock uses these permissions to generate encrypted data keys and then use the generated keys to encrypt agent memory. Amazon Bedrock also needs permissions to re-encrypt the the generated data key with different encryption contexts. Re-encrypt permissions are also used when customer managed key transitions between another customer managed key or service owned key. For more information, see [Hierarchical Keyring](https://docs.aws.amazon.com//database-encryption-sdk/latest/devguide/use-hierarchical-keyring.html).

Replace the `$region`, `account-id`, and `${caller-identity-role}` with appropriate values.

```
{
    "Version": "2012-10-17",		 	 	 
    {
        "Sid": "Allow access for bedrock to enable long term memory",
        "Effect": "Allow",
        "Principal": {
            "Service": [
                "bedrock.amazonaws.com",
            ],
        },
        "Action": [
            "kms:GenerateDataKeyWithoutPlainText",
            "kms:ReEncrypt*"
        ],
        "Condition": {
            "StringEquals": {
                "aws:SourceAccount": "$account-id"
            },
            "ArnLike": {
                "aws:SourceArn": "arn:aws:bedrock:$region:$account-id:agent-alias/*"
            }
        }
        "Resource": "*"
    },
    {
        "Sid": "Allow the caller identity control plane permissions for long term memory",
        "Effect": "Allow", 
        "Principal": {
            "AWS": "arn:aws:iam::${account-id}:role/${caller-identity-role}"
        },
        "Action": [
            "kms:GenerateDataKeyWithoutPlainText",
            "kms:ReEncrypt*"
        ],
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:EncryptionContext:aws-crypto-ec:aws:bedrock:arn": "arn:aws:bedrock:${region}:${account-id}:agent-alias/*"
            }
        }
    },
    {
        "Sid": "Allow the caller identity data plane permissions to decrypt long term memory",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::${account-id}:role/${caller-identity-role}"
        },
        "Action": [
            "kms:Decrypt"
        ],
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:EncryptionContext:aws-crypto-ec:aws:bedrock:arn": "arn:aws:bedrock:${region}:${account-id}:agent-alias/*",
                "kms:ViaService": "bedrock.$region.amazonaws.com" 
            }
        }
    }
}
```

**IAM permissions to encrypt and decrypt agent memory**

The following IAM permissions are needed for the identity calling Agents API to configure KMS key for agents with memory enabled. Amazon Bedrock agents use these permissions to make sure that the caller identity is authorized to have permissions mentioned in the key policy above for APIs to manage, train, and deploy models. For the APIs that invoke agents, Amazon Bedrock agent uses caller identity's `kms:Decrypt` permissions to decrypty memory.

Replace the `$region`, `account-id`, and `${key-id}` with appropriate values.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AgentsControlPlaneLongTermMemory",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKeyWithoutPlaintext", 
                "kms:ReEncrypt*"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/KeyId",
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:aws-crypto-ec:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent-alias/*"
                }
            }
        },
        {
            "Sid": "AgentsDataPlaneLongTermMemory",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/KeyId",
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:aws-crypto-ec:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent-alias/*"
                }
            }
        }
    ]
}
```

------