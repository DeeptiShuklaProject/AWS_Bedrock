

# Fulfill prerequisites to copy models
<a name="copy-model-prereq"></a>

To allow a role to copy a model, you might have to set up permissions, depending on the role's permissions and the model's configuration. Review the permissions in the following list and the circumstances in which you must configure them:

1. If your role doesn't have the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) policy attached, attach the following identity-based policy to the role to allow the minimal permissions to copy models and to track copy jobs.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "CopyModels",
               "Effect": "Allow",
               "Action": [
                   "bedrock:CreateModelCopyJob",
                   "bedrock:GetModelCopyJob",
                   "bedrock:ListModelCopyJobs"
               ],
               "Resource": [
                   "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{model-id}}"
               ],
               "Condition": {
                   "StringEquals": {
                       "aws:RequestedRegion": [
                           "{{us-east-1}}"
                       ]
                   }
               }
           }
       ]
   }
   ```

------

   Add ARNs of models to the `Resource` list. You can restrict the Regions that the model is copied to by adding Regions to the list in the [`aws:RequestedRegion` condition key.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-requestedregion)

1. (Optional) If the model to be copied is encrypted with a KMS key, attach a [key policy to the KMS key that encrypted the model](encryption-custom-job.md#encryption-key-policy-decrypt) to allow a role to decrypt it. Specify the account that the model will be shared with in the `Principal` field.

1. (Optional) If you plan to encrypt the model copy with a KMS key, attach a [key policy to the KMS key that will be used to encrypt the model](encryption-custom-job.md#encryption-key-policy-encrypt) to allow a role to encrypt the model with the key. Specify the role in the `Principal` field.