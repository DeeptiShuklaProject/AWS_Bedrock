

# Encryption of agent resources for agents created before January 22, 2025
<a name="encryption-agents"></a>

**Important**  
If you've created your agent *after* January 22, 2025, follow instructions for [Encryption of agent resources](encryption-agents-new.md)

Amazon Bedrock encrypts your agent's session information. By default, Amazon Bedrock encrypts this data using an AWS managed key. Optionally, you can encrypt the agent artifacts using a customer managed key.

For more information about AWS KMS keys, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the *AWS Key Management Service Developer Guide*.

If you encrypt sessions with your agent with a custom KMS key, you must set up the following identity-based policy and resource-based policy to allow Amazon Bedrock to encrypt and decrypt agent resources on your behalf.

1. Attach the following identity-based policy to an IAM role or user with permissions to make `InvokeAgent` calls. This policy validates the user making an `InvokeAgent` call has KMS permissions. Replace the {{${region}}}, {{${account-id}}}, {{${agent-id}}}, and {{${key-id}}} with the appropriate values.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "EncryptDecryptAgents",
               "Effect": "Allow",
               "Action": [
                   "kms:GenerateDataKey",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}",
               "Condition": {
                   "StringEquals": {
                       "kms:EncryptionContext:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/{{agent-id}}"
                   }
               }
           }
       ]
   }
   ```

------

1. Attach the following resource-based policy to your KMS key. Change the scope of the permissions as necessary. Replace the {{${region}}}, {{${account-id}}}, {{${agent-id}}}, and {{${key-id}}} with the appropriate values.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "AllowRootModifyKMSKey",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::{{123456789012}}:root"
               },
               "Action": "kms:*",
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
           },
           {
               "Sid": "AllowBedrockEncryptAgent",
               "Effect": "Allow",
               "Principal": {
                   "Service": "bedrock.amazonaws.com"
               },
               "Action": [
                   "kms:GenerateDataKey",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}",
               "Condition": {
                   "StringEquals": {
                       "kms:EncryptionContext:aws:bedrock:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/{{AgentId}}"
                   }
               }
           },
           {
               "Sid": "AllowRoleEncryptAgent",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::{{123456789012}}:role/{{Role}}"
               },
               "Action": [
                   "kms:GenerateDataKey*",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
           },
           {
               "Sid": "AllowAttachmentPersistentResources",
               "Effect": "Allow",
               "Principal": {
                   "Service": "bedrock.amazonaws.com"
               },
               "Action": [
                   "kms:CreateGrant",
                   "kms:ListGrants",
                   "kms:RevokeGrant"
               ],
               "Resource": "*",
               "Condition": {
                   "Bool": {
                       "kms:GrantIsForAWSResource": "true"
                   }
               }
           }
       ]
   }
   ```

------