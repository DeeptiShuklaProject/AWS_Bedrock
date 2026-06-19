

# Controlling Access to Amazon Bedrock Marketplace Models
<a name="control-amazon-bedrock-marketplace"></a>

You can use the [Amazon Bedrock Full Access policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonBedrockFullAccess.html) to provide permissions to SageMaker AI. To prevent users from accessing specific Bedrock Marketplace models while maintaining access to all other models, use a deny policy. The following policy demonstrates how to deny access to a specific model.

Denying Access to Specific Models:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "MarketplaceModelDeny",
            "Effect": "Deny",
            "Action": [
                "sagemaker:*",
                "bedrock:*"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:endpoint/*",
                "arn:aws:sagemaker:*:*:endpoint-config/*",
                "arn:aws:sagemaker:*:*:model/*"
            ],
            "Condition": {
                "StringLike": {
                    "aws:ResourceTag/sagemaker-studio:hub-content-arn": "arn:aws:sagemaker:*:aws:hub-content/SageMakerPublicHub/Model/{{model-id-to-deny}}/*"
                }
            }
        }
    ]
}
```

**Important**  
This policy explicitly denies access to the specified model while allowing access to all other Bedrock Marketplace models (assuming other necessary permissions are in place.

**Allowing Access to Only Specific Models**

To restrict users to accessing only specific Bedrock Marketplace models, use an allow policy with explicit model specifications. The following policy demonstrates how to allow access to only specific models:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "MarketplaceModelAllow",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateEndpoint",
                "sagemaker:CreateEndpointConfig",
                "sagemaker:CreateModel",
                "sagemaker:DeleteEndpoint",
                "sagemaker:UpdateEndpoint"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:endpoint/*",
                "arn:aws:sagemaker:*:*:endpoint-config/*",
                "arn:aws:sagemaker:*:*:model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:CalledViaLast": "bedrock.amazonaws.com",
                    "aws:ResourceTag/sagemaker-sdk:bedrock": "compatible"
                },
                "StringLike": {
                    "aws:ResourceTag/sagemaker-studio:hub-content-arn": "arn:aws:sagemaker:*:aws:hub-content/SageMakerPublicHub/Model/<model-id-to-allow>/*"
                }
            }
        },
        {
            "Sid": "BedrockEndpointTaggingOperations",
            "Effect": "Allow",
            "Action": [
                "sagemaker:AddTags",
                "sagemaker:DeleteTags"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:endpoint/*",
                "arn:aws:sagemaker:*:*:endpoint-config/*",
                "arn:aws:sagemaker:*:*:model/*"
            ],
            "Condition": {
                "StringLike": {
                    "aws:ResourceTag/sagemaker-studio:hub-content-arn": "arn:aws:sagemaker:*:aws:hub-content/SageMakerPublicHub/Model/<model-id-to-allow>/*"
                }
            }
        }
    ]
}
```

------

This policy only allows access to the specified model and denies access to all other models. If basing your policy off of `AmazonBedrockFullAccess`, this should replace the `MarketplaceModelEndpointMutatingAPIs` and `BedrockEndpointTaggingOperations` statements.