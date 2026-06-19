

# (Optional) Create a customer managed key for your guardrail for additional security
<a name="guardrails-permissions-kms"></a>

You encrypt your guardrails with customer managed AWS KMS keys. Any user with `CreateKey` permissions can create customer managed keys by using the AWS Key Management Service (AWS KMS) console or [CreateKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateKey.html) operation. In these situations, make sure to create a symmetric encryption key. 

After you create your key, configure the following permission policies.

1. Do the following to create a resource-based key policy:

   1. [Create a key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-overview.html) to create a resource-based policy for your KMS key.

   1. Add the following policy statements to grant permissions to guardrails users and guardrails creators. Replace each `{{role}}` with the role that you want to allow to carry out the specified actions.

------
#### [ JSON ]

****  

      ```
      {
          "Version":"2012-10-17",		 	 	 
          "Id": "KMS key policy",
          "Statement": [
              {
                  "Sid": "PermissionsForGuardrailsCreators",
                  "Effect": "Allow",
                  "Principal": {
                      "AWS": "arn:aws:iam::{{111122223333}}:user/{{role}}"
                  },
                  "Action": [
                      "kms:Decrypt",
                      "kms:GenerateDataKey",
                      "kms:DescribeKey",
                      "kms:CreateGrant"
                  ],
                  "Resource": "*"
              },
              {
                  "Sid": "PermissionsForGuardrailsUsers",
                  "Effect": "Allow",
                  "Principal": {
                      "AWS": "arn:aws:iam::{{111122223333}}:user/{{role}}"
                  },
                  "Action": "kms:Decrypt",
                  "Resource": "*"
              }
          ]
      }
      ```

------

1. Attach the following identity-based policy to a role to allow it to create and manage guardrails. Replace the `{{key-id}}` with the ID of the KMS key that you created.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "AllowRoleToCreateAndManageGuardrails",
               "Effect": "Allow",
               "Action": [
                   "kms:Decrypt",
                   "kms:DescribeKey",
                   "kms:GenerateDataKey",
                   "kms:CreateGrant"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
           }
       ]
   }
   ```

------

1. Attach the following identity-based policy to a role to allow it to use the guardrail you encrypted during model inference or while invoking an agent. Replace the `{{key-id}}` with the ID of the KMS key that you created.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "AllowRoleToUseEncryptedGuardrailDuringInference",
               "Effect": "Allow",
               "Action": [
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{key-id}}"
           }
       ]
   }
   ```

------