

# Identity-based policy examples for Amazon Bedrock
<a name="security_iam_id-based-policy-examples"></a>

By default, users and roles don't have permission to create or modify Amazon Bedrock resources. To grant users permission to perform actions on the resources that they need, an IAM administrator can create IAM policies.

To learn how to create an IAM identity-based policy by using these example JSON policy documents, see [Create IAM policies (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) in the *IAM User Guide*.

For details about actions and resource types defined by Amazon Bedrock, including the format of the ARNs for each of the resource types, see [Actions, Resources, and Condition Keys for Amazon Bedrock ](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html) in the *Service Authorization Reference*.

**Topics**
+ [Policy best practices](#security_iam_service-with-iam-policy-best-practices)
+ [Use the Amazon Bedrock console](#security_iam_id-based-policy-examples-console)
+ [Allow users to view their own permissions](#security_iam_id-based-policy-examples-view-own-permissions)
+ [Deny access for inference of foundation models](#security_iam_id-based-policy-examples-deny-inference)
+ [Allow users to invoke a provisioned model](#security_iam_id-based-policy-examples-perform-actions-pt)
+ [Identity-based policy examples for Amazon Bedrock Agents](security_iam_id-based-policy-examples-agent.md)
+ [Minimal policy for Amazon Bedrock Playground chat](#security_iam_id-based-policy-examples-playground)

## Policy best practices
<a name="security_iam_service-with-iam-policy-best-practices"></a>

Identity-based policies determine whether someone can create, access, or delete Amazon Bedrock resources in your account. These actions can incur costs for your AWS account. When you create or edit identity-based policies, follow these guidelines and recommendations:
+ **Get started with AWS managed policies and move toward least-privilege permissions** – To get started granting permissions to your users and workloads, use the *AWS managed policies* that grant permissions for many common use cases. They are available in your AWS account. We recommend that you reduce permissions further by defining AWS customer managed policies that are specific to your use cases. For more information, see [AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies) or [AWS managed policies for job functions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html) in the *IAM User Guide*.
+ **Apply least-privilege permissions** – When you set permissions with IAM policies, grant only the permissions required to perform a task. You do this by defining the actions that can be taken on specific resources under specific conditions, also known as *least-privilege permissions*. For more information about using IAM to apply permissions, see [ Policies and permissions in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) in the *IAM User Guide*.
+ **Use conditions in IAM policies to further restrict access** – You can add a condition to your policies to limit access to actions and resources. For example, you can write a policy condition to specify that all requests must be sent using SSL. You can also use conditions to grant access to service actions if they are used through a specific AWS service, such as CloudFormation. For more information, see [ IAM JSON policy elements: Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html) in the *IAM User Guide*.
+ **Use IAM Access Analyzer to validate your IAM policies to ensure secure and functional permissions** – IAM Access Analyzer validates new and existing policies so that the policies adhere to the IAM policy language (JSON) and IAM best practices. IAM Access Analyzer provides more than 100 policy checks and actionable recommendations to help you author secure and functional policies. For more information, see [Validate policies with IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html) in the *IAM User Guide*.
+ **Require multi-factor authentication (MFA)** – If you have a scenario that requires IAM users or a root user in your AWS account, turn on MFA for additional security. To require MFA when API operations are called, add MFA conditions to your policies. For more information, see [ Secure API access with MFA](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html) in the *IAM User Guide*.

For more information about best practices in IAM, see [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) in the *IAM User Guide*.

## Use the Amazon Bedrock console
<a name="security_iam_id-based-policy-examples-console"></a>

To access the Amazon Bedrock console, you must have a minimum set of permissions. These permissions must allow you to list and view details about the Amazon Bedrock resources in your AWS account. If you create an identity-based policy that is more restrictive than the minimum required permissions, the console won't function as intended for entities (users or roles) with that policy.

You don't need to allow minimum console permissions for users that are making calls only to the AWS CLI or the AWS API. Instead, allow access to only the actions that match the API operation that they're trying to perform.

To ensure that users and roles can still use the Amazon Bedrock console, also attach the Amazon Bedrock [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) or [AmazonBedrockReadOnly](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockReadOnly) AWS managed policy to the entities. For more information, see [Adding permissions to a user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-add-console) in the *IAM User Guide*.

## Allow users to view their own permissions
<a name="security_iam_id-based-policy-examples-view-own-permissions"></a>

This example shows how you might create a policy that allows IAM users to view the inline and managed policies that are attached to their user identity. This policy includes permissions to complete this action on the console or programmatically using the AWS CLI or AWS API.

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ViewOwnUserInfo",
            "Effect": "Allow",
            "Action": [
                "iam:GetUserPolicy",
                "iam:ListGroupsForUser",
                "iam:ListAttachedUserPolicies",
                "iam:ListUserPolicies",
                "iam:GetUser"
            ],
            "Resource": ["arn:aws:iam::*:user/${aws:username}"]
        },
        {
            "Sid": "NavigateInConsole",
            "Effect": "Allow",
            "Action": [
                "iam:GetGroupPolicy",
                "iam:GetPolicyVersion",
                "iam:GetPolicy",
                "iam:ListAttachedGroupPolicies",
                "iam:ListGroupPolicies",
                "iam:ListPolicyVersions",
                "iam:ListPolicies",
                "iam:ListUsers"
            ],
            "Resource": "*"
        }
    ]
}
```

## Deny access for inference of foundation models
<a name="security_iam_id-based-policy-examples-deny-inference"></a>

To prevent a user from invoking foundation models, you need to deny access to API actions that invoke models directly. The following example shows a identity-based policy that denies access to running inference on a specific model. This policy can be used as a service control policy (SCP) to control model access across an organization.

------
#### [ JSON ]

****  

```
{
          "Version":"2012-10-17",		 	 	 
          "Statement": {
              "Sid": "DenyInference",
              "Effect": "Deny",
              "Action": [
                  "bedrock:InvokeModel",
                  "bedrock:InvokeModelWithResponseStream",
                  "bedrock:CreateModelInvocationJob"
               ],
              "Resource": "arn:aws:bedrock:*::foundation-model/{{model-id}}"
          }
      }
```

------

To deny inference access to all foundation models, use `*` for the model ID. Other actions, such as `Converse` and `StartAsyncInvoke`, are blocked automatically when `InvokeModel` is denied. If you want to explicitly deny all inference actions, you can use `bedrock:InvokeModel*` as a wildcard or add `bedrock:Converse` and `bedrock:ConverseStream` to the action list. For a list of model IDs, see [Supported foundation models in Amazon Bedrock](models-supported.md)

## Allow users to invoke a provisioned model
<a name="security_iam_id-based-policy-examples-perform-actions-pt"></a>

The following is a sample policy that you can attach to an IAM role to allow it to use a provisioned model in model inference. For example, you could attach this policy to a role that you want to only have permissions to use a provisioned model. The role won't be able to manage or see information about the Provisioned Throughput.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{ProvisionedThroughputModelInvocation}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:{{123456789012}}:provisioned-model/{{my-provisioned-model}}"
        }
    ]
}
```

------

## Minimal policy for Amazon Bedrock Playground chat
<a name="security_iam_id-based-policy-examples-playground"></a>

The following policy grants the minimum permissions required to use the Amazon Bedrock Playground in the AWS Management Console to chat with a model. Replace {{<region>}}, {{<account-id>}}, and the model resource ARNs with your values.

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "BedrockConsoleRead",
            "Effect": "Allow",
            "Action": [
                "bedrock:ListFoundationModels",
                "bedrock:ListInferenceProfiles",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:ListCustomModels",
                "bedrock:ListGuardrails",
                "bedrock:ListFoundationModelAgreementOffers",
                "bedrock:ListMarketplaceModelEndpoints",
                "bedrock:ListImportedModels",
                "bedrock:ListPromptRouters",
                "bedrock:GetFoundationModel",
                "bedrock:GetFoundationModelAvailability",
                "bedrock:GetInferenceProfile",
                "bedrock:GetUseCaseForModelAccess",
                "bedrock:PutUseCaseForModelAccess"
            ],
            "Resource": "*"
        },
        {
            "Sid": "SageMakerHubRead",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListHubContents"
            ],
            "Resource": "arn:aws:sagemaker:*:aws:hub/SageMakerPublicHub"
        },
        {
            "Sid": "InvokeModel",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/*",
                "arn:aws:bedrock:{{<region>}}:{{<account-id>}}:inference-profile/*"
            ]
        },
        {
            "Sid": "MarketplaceSubscription",
            "Effect": "Allow",
            "Action": [
                "aws-marketplace:ViewSubscriptions",
                "aws-marketplace:Subscribe"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:CalledViaLast": "bedrock.amazonaws.com"
                }
            }
        }
    ]
}
```

To restrict access to a specific model, replace the `InvokeModel` statement's `Resource` with the specific model and inference profile ARNs.