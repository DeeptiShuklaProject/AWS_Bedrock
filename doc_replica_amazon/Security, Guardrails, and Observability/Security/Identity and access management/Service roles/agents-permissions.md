

# Create a service role for Amazon Bedrock Agents
<a name="agents-permissions"></a>

To use a custom service role for agents instead of the one Amazon Bedrock automatically creates, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
+ Trust policy
+ A policy containing the following identity-based permissions:
  + Access to the Amazon Bedrock base models.
  + Access to the Amazon S3 objects containing the OpenAPI schemas for the action groups in your agents.
  + Permissions for Amazon Bedrock to query knowledge bases that you want to attach to your agents.
  + If any of the following situations pertain to your use case, add the statement to the policy or add a policy with the statement to the service role:
    + (Optional) If you enable multi-agent collaboration, permissions to get the aliases and invoke agent collaborators.
    + (Optional) If you associate a Provisioned Throughput with your agent alias, permissions to perform model invocation using that Provisioned Throughput.
    + (Optional) If you associate a guardrail with your agent, permissions to apply that guardrail. If the guardrail is encrypted with a KMS key, the service role will also need [permissions to decrypt the key](guardrails-permissions-kms.md)
    + (Optional) If you encrypt your agent with a KMS key, [permissions to decrypt the key](encryption-agents.md).

Whether you use a custom role or not, you also need to attach a **resource-based policy** to the Lambda functions for the action groups in your agents to provide permissions for the service role to access the functions. For more information, see [Resource-based policy to allow Amazon Bedrock to invoke an action group Lambda function](#agents-permissions-lambda).

**Topics**
+ [Trust relationship](#agents-permissions-trust)
+ [Identity-based permissions for the Agents service role](#agents-permissions-identity)
+ [(Optional) Identity-based policy to allow Amazon Bedrock to use Provisioned Throughput with your agent alias](#agents-permissions-pt)
+ [(Optional) Identity-based policy to allow Amazon Bedrock to associate and invoke agent collaborators](#agents-permissions-mac)
+ [(Optional) Identity-based policy to allow Amazon Bedrock to use guardrails with your Agent](#agents-permissions-gr)
+ [(Optional) Identity-based policy to allow Amazon Bedrock to access files from S3 to use with code interpretation](#agents-permissions-files-ci)
+ [Resource-based policy to allow Amazon Bedrock to invoke an action group Lambda function](#agents-permissions-lambda)

## Trust relationship
<a name="agents-permissions-trust"></a>

The following trust policy allows Amazon Bedrock to assume this role and create and manage agents. Replace the {{${values}}} as necessary. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.

**Note**  
As a best practice for security purposes, replace the {{\*}} with specific agent IDs after you have created them.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "{{123456789012}}"
                },
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/{{*}}"
                }
            }
        }
    ]
}
```

------

## Identity-based permissions for the Agents service role
<a name="agents-permissions-identity"></a>

Attach the following policy to provide permissions for the service role, replacing {{${values}}} as necessary. The policy contains the following statements. Omit a statement if it isn't applicable to your use-case. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.

**Note**  
If you encrypt your agent with a customer-managed KMS key, refer to [Encryption of agent resources for agents created before January 22, 2025](encryption-agents.md) for further permissions you need to add.
+ Permissions to use Amazon Bedrock foundation models to run model inference on prompts used in your agent's orchestration.
+ Permissions to access your agent's action group API schemas in Amazon S3. Omit this statement if your agent has no action groups.
+ Permissions to access knowledge bases associated with your agent. Omit this statement if your agent has no associated knowledge bases.
+ Permissions to access a third-party (Pinecone or Redis Enterprise Cloud) knowledge base associated with your agent. Omit this statement if your knowledge base is first-party (Amazon OpenSearch Serverless or Amazon Aurora) or if your agent has no associated knowledge bases.
+ Permissions to access a prompt from Prompt management. Omit this statement if you don't plan to test a prompt from prompt management with your agent in the Amazon Bedrock console.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{AgentModelInvocationPermissions}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/anthropic.claude-v2",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/anthropic.claude-v2:1",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/anthropic.claude-instant-v1"
            ]
        },
        {
            "Sid": "{{AgentActionGroupS3}}",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::amzn-s3-demo-bucket/SchemaJson"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        },
        {
            "Sid": "{{AgentKnowledgeBaseQuery}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{knowledge-base-id}}"
            ]
        },
        {
            "Sid": "{{Agent3PKnowledgeBase}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:AssociateThirdPartyKnowledgeBase"
            ],
            "Resource": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{knowledge-base-id}}",
            "Condition": {
                "StringEquals": {
                    "bedrock:ThirdPartyKnowledgeBaseCredentialsSecretArn": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
                }
            }
        },
        {
            "Sid": "{{AgentPromptManagementConsole}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:GetPrompt"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:prompt/{{prompt-id}}"
            ]
        }
    ]
}
```

------

**Important**  
If your agent uses an [inference profile](inference-profiles-support.md) instead of a foundation model directly, you must make the following changes to the `AgentModelInvocationPermissions` statement:  
Add the inference profile ARN to the `Resource` list. The format is `arn:aws:bedrock:{{region}}:{{account-id}}:inference-profile/{{inference-profile-id}}`.
Add the following actions to the `Action` list:  
`bedrock:InvokeModelWithResponseStream`
`bedrock:GetInferenceProfile`
`bedrock:GetFoundationModel`

## (Optional) Identity-based policy to allow Amazon Bedrock to use Provisioned Throughput with your agent alias
<a name="agents-permissions-pt"></a>

If you associate a [Provisioned Throughput](prov-throughput.md) with an alias of your agent, attach the following identity-based policy to the service role or add the statement to the policy in [Identity-based permissions for the Agents service role](#agents-permissions-identity).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
      {        
        "Sid": "UseProvisionedThroughput",
        "Effect": "Allow",
        "Action": [
            "bedrock:InvokeModel", 
            "bedrock:GetProvisionedModelThroughput"
        ],
        "Resource": [
            "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:provisioned-model/{{${provisioned-model-id}}}"
        ]
      }
    ]
}
```

------

## (Optional) Identity-based policy to allow Amazon Bedrock to associate and invoke agent collaborators
<a name="agents-permissions-mac"></a>

If you enable [multi-agent collaboration](agents-multi-agent-collaboration.md), attach the following identity-based policy to the service role or add the statement to the policy in [Identity-based permissions for the Agents service role](#agents-permissions-identity).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AmazonBedrockAgentMultiAgentsPolicyProd",
            "Effect": "Allow",
            "Action": [
                "bedrock:GetAgentAlias",
                "bedrock:InvokeAgent"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:{{agent-alias}}/{{${agent-id}}}/{{${agent-alias-id}}}"
            ]
        }
    ]
}
```

------

## (Optional) Identity-based policy to allow Amazon Bedrock to use guardrails with your Agent
<a name="agents-permissions-gr"></a>

If you associate a [guardrail](guardrails.md) with your agent, attach the following identity-based policy to the service role or add the statement to the policy in [Identity-based permissions for the Agents service role](#agents-permissions-identity).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{ApplyGuardrail}}",
            "Effect": "Allow",
            "Action": "bedrock:ApplyGuardrail",
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{${guardrail-id}}}"
            ]
        }
    ]
}
```

------

## (Optional) Identity-based policy to allow Amazon Bedrock to access files from S3 to use with code interpretation
<a name="agents-permissions-files-ci"></a>

If you enable [Enable code interpretation in Amazon Bedrock](agents-enable-code-interpretation.md), attach the following identity-based policy to the service role or add the statement to the policy in [Identity-based permissions for the Agents service role](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-permissions.html#agents-permissions-identity).

------
#### [ JSON ]

****  

```
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
      {       
        "Sid": "AmazonBedrockAgentFileAccess", 
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:GetObjectVersionAttributes",
            "s3:GetObjectAttributes"
        ],
        "Resource": [
            "arn:aws:s3:::[[customerProvidedS3BucketWithKey]]"
        ]
      }
    ]
}
```

------

## Resource-based policy to allow Amazon Bedrock to invoke an action group Lambda function
<a name="agents-permissions-lambda"></a>

Follow the steps at [Using resource-based policies for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html) and attach the following resource-based policy to a Lambda function to allow Amazon Bedrock to access the Lambda function for your agent's action groups, replacing the {{${values}}} as necessary. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{AccessLambdaFunction}}",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:{{us-east-1}}:{{123456789012}}:function:{{function-name}}",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceAccount": "{{123456789012}}"
                },
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent/{{${agent-id}}}"
                }
            }
        }
    ]
}
```

------