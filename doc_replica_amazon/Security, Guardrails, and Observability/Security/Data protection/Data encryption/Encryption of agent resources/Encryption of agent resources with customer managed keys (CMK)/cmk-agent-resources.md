

# Encryption of agent resources with customer managed keys (CMK)
<a name="cmk-agent-resources"></a>

You can at any time create a customer managed key to encrypt your agent’s information using the following agent information provided when building your agent.

**Note**  
The following agent resources will only be encrypted for the agents created after January 22, 2025.


****  


- **[CreateAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgent.html)**
  - **CMK enabled fields:** instruction / **Description:** Instructs the agent on what it should do and how it should interact with users
  - **CMK enabled fields:** basePromptTemplate / **Description:** Defines the prompt template with which to replace the default prompt template

- **[CreateAgentActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html)**
  - **CMK enabled fields:** description / **Description:** Description of the action group
  - **CMK enabled fields:** [apiSchema](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_APISchema.html) / **Description:** Contains either the details of the apiSchema for the agent action group or the JSON or YAML-formatted payload defining the schema
  - **CMK enabled fields:** [s3](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_APISchema.html) / **Description:** Contains details about the Amazon S3 object containing the apiSchema for the agent action group
  - **CMK enabled fields:** functionSchema / **Description:** Contains details of the function schema for the agent action group or the JSON-YAML formatted payload defining the schema

- **[AssociateAgentKnowledgeBase](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_AssociateAgentKnowledgeBase.html)**
  - **CMK enabled fields:** description
  - **Description:** Description of what the agent should use the knowledge base for

- **[AssociateAgentCollaborator](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_AssociateAgentCollaborator.html)**
  - **CMK enabled fields:** collaborationInstruction
  - **Description:** Instructions for the collaborator agent



To use a customer managed key, complete the following steps:

1. Create customer managed key with the AWS Key Management Service.

1. Create a key policy and attach to the customer managed key

## Create a customer managed key
<a name="create-cmk-agent"></a>

You can create a symmetric customer managed key by using the AWS Management Console, or the AWS Key Management Service APIs. 

 First make sure that you have `CreateKey` permissions and then, follow the steps for [Creating symmetric customer managed key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk) in the *AWS Key Management Service Developer Guide*.

**Key policy** - key policies control access to your customer managed key . Every customer managed key must have exactly one key policy, which contains statements that determine who can use the key and how they can use it. When you create your customer managed key, you can specify a key policy. For more information, see [Managing access to customer managed key](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) in the *AWS Key Management Service Developer Guide*.

If you have created your agent after January 22, 2025 and want to use customer managed key to encrypt your agent's information, make sure that the user or the role calling the agent API operations has the following permissions in the key policy:
+ [kms:GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html) – returns a unique symmetric data key for use outside of AWS KMS.
+ [kms:Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) – decrypts ciphertext that was encrypted by a KMS key.

Creation of the key returns an `Arn` for the key that you can use as the `customerEncryptionKeyArn`, when creating your agent. 

## Create a key policy and attach it to the customer managed key
<a name="attach-policy-agent"></a>

If you encrypt agent resources with a customer managed key, you must set up an identity-based policy and a resource-based policy to allow Amazon Bedrock to encrypt and decrypt the agent resources on your behalf.

**Identity-based policy**

Attach the following identity-based policy to an IAM role or user with permissions to make calls to agent APIs that encrypt and decrypt agent resources on your behalf. This policy validates the user making API call has AWS KMS permissions. Replace the `${region}`, `${account-id}`, `${agent-id}`, and `${key-id}` with the appropriate values.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "EncryptAgents",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
            "Condition": {
                "StringEquals": {
                    "kms:EncryptionContext:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/${agent-id}"
                }
            }
        }
    ]
}
```

------

**Resource-based policy**

Attach the following resource-based policy to your AWS KMS key *only* if you are creating action groups where the schema in Amazon S3 is encrypted. You do not need to attach resource-based policy for any other use cases.

To attach the following resource-based policy, change the scope of the permissions as necessary and replace the `${region}`, `${account-id}`, `${agent-id}`, and `${key-id}` with the appropriate values.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "Allow account root to modify the KMS key, not used by Amazon Bedrock.",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:root"
            },
            "Action": "kms:*",
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}"
        },
        {
            "Sid": "Allow Amazon Bedrock to encrypt and decrypt Agent resources on behalf of authorized users",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
            "Condition": {
                "StringEquals": {
                    "kms:EncryptionContext:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/${agent-id}"
                }
            }
        }
    ]
}
```

------

## Changing the customer managed key
<a name="change-cmk"></a>

Amazon Bedrock agents do not support re-encryption of versioned agents when the customer managed key associated with the *DRAFT* agent is changed or when you move from customer managed key to AWS owned key. Only the data for the *DRAFT* resource will be re-encrypted with the new key.

Make sure you are not deleting or removing permissions for any keys for a versioned agent if using it to serve production data.

To view and verify the keys being used by a version, call [GetAgentVersion](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_GetAgentVersion.html) and check the `customerEncryptionKeyArn` in the response.