

# Fulfill prerequisites to share models
<a name="share-model-prereq"></a>

Amazon Bedrock interfaces with the [AWS Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/) and [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/) services to allow the sharing of models. Before you can share a model with another account, you must fulfill the following prerequisites:

## Create an organization with AWS Organizations and add the model sharer and recipient
<a name="share-model-prereq-orgs"></a>

For an account to share a model with another account, the two accounts must be part of the same organization in AWS Organizations and resource sharing in AWS RAM must be enabled for the organization. To set up an organization and invite accounts to it, do the following:

1. Enable resource sharing through AWS RAM in AWS Organizations by following the steps at [Enable resource sharing within AWS Organizations](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html#getting-started-sharing-orgs) in the AWS RAM User Guide.

1. Create an organization in AWS Organizations by following the steps at [Creating an organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_create.html) in the AWS Organizations User Guide.

1. Invite the account that you want to share the model with by following the steps at [Inviting an AWS account to join your organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html) in the AWS Organizations User Guide.

1. The administrator of the account you sent an invitation to must accept the invitation by following the steps at [Accepting or declining an invitation from an organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html#orgs_manage_accounts_accept-decline-invite).

## Add an identity-based policy to an IAM role to allow it to share a model
<a name="share-model-prereq-ibp"></a>

For a role to have permissions to share a model, it must have permissions to both Amazon Bedrock and AWS RAM actions. Attach the following policies to the role:

1. To provide permissions for a role to manage sharing of a model with another account through AWS Resource Access Manager, attach the following identity-based policy to the role to provide minimal permissions:

------
#### [ JSON ]

****  

   ```
   { 
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
              "Sid": "ShareResources",
              "Effect": "Allow",
              "Action": [
                  "ram:CreateResourceShare",
                  "ram:UpdateResourceShare",
                  "ram:DeleteResourceShare",
                  "ram:AssociateResourceShare",
                  "ram:DisassociateResourceShare",
                  "ram:GetResourceShares"
              ],
              "Resource": [
                  "arn:aws:bedrock:us-east-1::foundation-model/{{model-id}}"
              ]
           }
       ]
   }
   ```

------

   Replace {{${model-arn}}} with the Amazon Resource Name (ARN) of the model that you want to share. Add models to the `Resource` list as necessary. You can review the [Actions, resources, and condition keys for AWS Resource Access Manager](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsresourceaccessmanagerram.html) and modify the AWS RAM actions that the role can carry out as necessary.
**Note**  
You can also attach the more permissive [AWSResourceManagerFullAccess managed policy](https://docs.aws.amazon.com/ram/latest/userguide/security-iam-managed-policies.html#security-iam-managed-policies-AWSResourceAccessManagerFullAccess) to the role.

1. Check that the role has the [AmazonBedrockFullAccess policy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) attached. If it doesn't, you must also attach the following policy to the role to allow it to share models (replacing {{${model-arn}}}) as necessary:

------
#### [ JSON ]

****  

   ```
   { 
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "ShareCustomModels",
               "Effect": "Allow",
               "Action": [
                   "bedrock:GetCustomModel",
                   "bedrock:ListCustomModels",
                   "bedrock:PutResourcePolicy",
                   "bedrock:GetResourcePolicy",
                   "bedrock:DeleteResourcePolicy"
               ],
               "Resource": [
                   "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{model-id}}"
               ]
           }
       ]
   }
   ```

------

## (Optional) Set up KMS key policies to encrypt a model and to allow it to be decrypted
<a name="share-model-prereq-kms"></a>

**Note**  
Skip this prerequisite if the model you're sharing is not encrypted with a customer managed key and you don't plan to encrypt it.

If you need to encrypt a model with a customer managed key before sharing it with another account, attach permissions to the KMS key that you'll use to encrypt the model by following the steps at [Set up key permissions for encrypting custom models](encryption-custom-job.md#encryption-cm).

If the model you share with another account is encrypted with a customer managed key, attach permissions to the KMS key that encrypted the model to allow the recipient account to decrypt it by following the steps at [Set up key permissions for copying custom models](encryption-custom-job.md#encryption-copy).