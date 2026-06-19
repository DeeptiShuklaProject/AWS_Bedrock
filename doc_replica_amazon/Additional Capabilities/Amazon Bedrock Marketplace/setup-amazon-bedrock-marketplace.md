

# Set up Amazon Bedrock Marketplace
<a name="setup-amazon-bedrock-marketplace"></a>

You can use the [Amazon Bedrock Full Access policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonBedrockFullAccess.html) to provide permissions to SageMaker AI. We recommend using the managed policy, but if you can't use the managed policy, make sure that your IAM role has the following permissions.

The following is a recommended custom policy for Amazon Bedrock Marketplace. For the latest version of the Amazon Bedrock Full Access managed policy, see [AmazonBedrockFullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonBedrockFullAccess.html).

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "BedrockAll",
            "Effect": "Allow",
            "Action": [
                "bedrock:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DescribeKey",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey"
            ],
            "Resource": "arn:*:kms:*:::*"
        },
        {
            "Sid": "APIsWithAllResourceAccess",
            "Effect": "Allow",
            "Action": [
                "iam:ListRoles",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        },
        {
            "Sid": "MarketplaceModelEndpointMutatingAPIs",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateEndpoint",
                "sagemaker:CreateEndpointConfig",
                "sagemaker:CreateModel",
                "sagemaker:DeleteEndpoint",
                "sagemaker:UpdateEndpoint"
            ],
            "Resource": [
                "arn:*:sagemaker:*:*:endpoint/*",
                "arn:*:sagemaker:*:*:endpoint-config/*",
                "arn:*:sagemaker:*:*:model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:CalledViaLast": "bedrock.amazonaws.com"
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
                "arn:*:sagemaker:*:*:endpoint/*",
                "arn:*:sagemaker:*:*:endpoint-config/*",
                "arn:*:sagemaker:*:*:model/*"
            ]
        },
        {
            "Sid": "MarketplaceModelEndpointNonMutatingAPIs",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeEndpoint",
                "sagemaker:DescribeEndpointConfig",
                "sagemaker:DescribeModel",
                "sagemaker:DescribeInferenceComponent",
                "sagemaker:ListEndpoints",
                "sagemaker:ListTags"
            ],
            "Resource": [
                "arn:*:sagemaker:*:*:endpoint/*",
                "arn:*:sagemaker:*:*:endpoint-config/*",
                "arn:*:sagemaker:*:*:model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:CalledViaLast": "bedrock.amazonaws.com"
                }
            }
        },
        {
            "Sid": "BedrockEndpointInvokingOperations",
            "Effect": "Allow",
            "Action": [
                "sagemaker:InvokeEndpoint",
                "sagemaker:InvokeEndpointWithResponseStream"
            ],
            "Resource": [
                "arn:*:sagemaker:*:*:endpoint/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:CalledViaLast": "bedrock.amazonaws.com"
                }
            }
        },
        {
            "Sid": "DiscoveringMarketplaceModel",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeHubContent"
            ],
            "Resource": [
                "arn:*:sagemaker:*:aws:hub-content/SageMakerPublicHub/Model/*",
                "arn:*:sagemaker:*:aws:hub/SageMakerPublicHub"
            ]
        },
        {
            "Sid": "AllowMarketplaceModelsListing",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListHubContents"
            ],
            "Resource": "arn:*:sagemaker:*:aws:hub/SageMakerPublicHub"
        },
        {
            "Sid": "RetrieveSubscribedMarketplaceLicenses",
            "Effect": "Allow",
            "Action": [
                "license-manager:ListReceivedLicenses"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "PassRoleToSageMaker",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:*:iam::*:role/*Sagemaker*ForBedrock*"
            ],
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": [
                        "sagemaker.amazonaws.com",
                        "bedrock.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "PassRoleToBedrock",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "arn:*:iam::*:role/*AmazonBedrock*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": [
                        "bedrock.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

**Important**  
The Amazon Bedrock Full Access policy only provides permissions to the Amazon Bedrock API. To use Amazon Bedrock in the AWS Management Console, your IAM role must also have the following permissions:  

```
{
        "Sid": "AllowConsoleS3AccessForBedrockMarketplace",
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:GetBucketCORS",
          "s3:ListBucket",
          "s3:ListBucketVersions",
          "s3:GetBucketLocation"
        ],
        "Resource": "*"
    }
```

If you’re writing your own policy, you must include the policy statement that allows the Amazon Bedrock Marketplace action for the resource. For example, the following policy allows Amazon Bedrock to use the `InvokeModel` operation for a model that you’ve deployed to an endpoint.

------
#### [ JSON ]

****  

```
{
    
        "Version":"2012-10-17",		 	 	 
        "Statement": [
            {
                "Sid": "BedrockAll",
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel"
                ],
                "Resource": [
                    "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:marketplace/model-endpoint/all-access"
                ]
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": ["sagemaker:InvokeEndpoint"],
                "Resource": "arn:aws:sagemaker:{{us-east-1}}:{{111122223333}}:endpoint/*",
                "Condition": {
                    "StringEquals": {
                        "aws:ResourceTag/project": "{{example-project-id}}",
                        "aws:CalledViaLast": "bedrock.amazonaws.com"
                    }
                }
            }
        ]
    
}
```

------

For more information about setting up Amazon Bedrock, see [Quickstart](getting-started.md).

You might want to use an AWS Key Management Service key to encrypt the endpoint where you've deployed the model. You must modify the preceding policy to have permissions to use the AWS KMS key.

The AWS KMS key must also have permissions to encrypt the endpoint. You must modify the AWS KMS resource policy to encrypt the endpoint. For more information about modifying the policy, see [Using IAM policies with AWS Key Management Service](https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies).

Your AWS KMS key must also have `CreateGrant` permissions. The following is an example of the permissions that must be in the key policy.

```
{
"Sid": "Allow access for AmazonSageMaker-ExecutionRole",
"Effect": "Allow",
"Principal": {
"AWS": "arn:aws:iam::111122223333:role/{{SagemakerExecutionRole}}"
},
"Action": "kms:CreateGrant",
"Resource": "*"
}
```

For more information about providing create grant permissions, see [Granting CreateGrant permission](https://docs.aws.amazon.com/kms/latest/developerguide/create-grant-overview.html#grant-creategrant).