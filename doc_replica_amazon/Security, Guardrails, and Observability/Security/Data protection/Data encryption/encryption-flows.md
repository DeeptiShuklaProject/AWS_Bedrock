

# Encryption of Amazon Bedrock Flows resources
<a name="encryption-flows"></a>

Amazon Bedrock encrypts your data at rest. By default, Amazon Bedrock encrypts this data using an AWS managed key. Optionally, you can encrypt the data using a customer managed key.

For more information about AWS KMS keys, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the *AWS Key Management Service Developer Guide*.

If you encrypt data with a custom KMS key, you must set up the following identity-based policy and resource-based policy to allow Amazon Bedrock to encrypt and decrypt data on your behalf.

1. Attach the following identity-based policy to an IAM role or user with permissions to make Amazon Bedrock Flows API calls. This policy validates the user making Amazon Bedrock Flows calls has KMS permissions. Replace the {{${region}}}, {{${account-id}}}, {{${flow-id}}}, and {{${key-id}}} with the appropriate values.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "EncryptFlow",
               "Effect": "Allow",
               "Action": [
                   "kms:GenerateDataKey",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
               "Condition": {
                   "StringEquals": {
                       "kms:EncryptionContext:aws:bedrock-flows:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:flow/${flow-id}",
                       "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
                   }
               }
           }
       ]
   }
   ```

------

1. Attach the following resource-based policy to your KMS key. Change the scope of the permissions as necessary. Replace the {{{IAM-USER/ROLE-ARN}}}, {{${region}}}, {{${account-id}}}, {{${flow-id}}}, and {{${key-id}}} with the appropriate values.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "AllowRootModifyKMSId",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::{{123456789012}}:root"
               },
               "Action": "kms:*",
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/KeyId"
           },
           {
               "Sid": "AllowRoleUseKMSKey",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::123456789012:role/RoleName"
               },
               "Action": [
                   "kms:GenerateDataKey",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/${key-id}",
               "Condition": {
                   "StringEquals": {
                       "kms:EncryptionContext:aws:bedrock-flows:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:flow/FlowId",
                       "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
                   }
               }
           }
       ]
   }
   ```

------

1. For [flow executions](flows-create-async.md), attach the following identity-based policy to a [service role with permissions to create and manage flows](flows-permissions.md). This policy validates that the your service role has AWS KMS permissions. Replace the {{region}}, {{account-id}}, {{flow-id}}, and {{key-id}} with the appropriate values.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "EncryptionFlows",
               "Effect": "Allow",
               "Action": [
                   "kms:GenerateDataKey",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}",
               "Condition": {
                   "StringEquals": {
                       "kms:EncryptionContext:aws:bedrock-flows:arn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:flow/{{flow-id}}",
                       "kms:ViaService": "bedrock.{{us-east-1}}.amazonaws.com"
                   }
               }
           }
       ]
   }
   ```

------