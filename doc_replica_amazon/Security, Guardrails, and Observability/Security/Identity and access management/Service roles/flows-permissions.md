

# Create a service role for Amazon Bedrock Flows in Amazon Bedrock
<a name="flows-permissions"></a>

To create and manage a flow in Amazon Bedrock, you must use a service role with the necessary permissions outlined on this page. You can use a service role that Amazon Bedrock automatically creates for you in the console or use one that you customize yourself.

**Note**  
If you use the service role that Amazon Bedrock automatically creates for you in the console, it will attach permissions dynamically if you add nodes to your flow and save the flow. If you remove nodes, however, the permissions won't be deleted, so you will have to delete the permissions you no longer need. To manage the permissions for the role that was created for you, follow the steps at [Modifying a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_modify.html) in the IAM User Guide.

To create a custom service role for Amazon Bedrock Flows, create an IAM role by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). Then attach the following permissions to the role.
+ Trust policy
+ The following identity-based permissions:
  + Access to the Amazon Bedrock base models that the flow will use. Add each model that's used in the flow to the `Resource` list.
  + If you invoke a model using Provisioned Throughput, permissions to access and invoke the provisioned model. Add each model that's used in the flow to the `Resource` list.
  + If you invoke a custom model, permissions to access and invoke the custom model. Add each model that's used in the flow to the `Resource` list.
  + Permissions based on the nodes that you add to the flow:
    + If you include prompt nodes that use prompts from Prompt management, you need permissions to access the prompt. Add each prompt that's used in the flow to the `Resource` list.
    + If you include knowledge base nodes, you need permissions to query the knowledge base. Add each knowledge base that's queried in the flow to the `Resource` list.
    + If you include agent nodes, you need permissions to invoke an alias of the agent. Add each agent that's invoked in the flow to the `Resource` list.
    + If you include S3 retrieval nodes, you need permissions to access the Amazon S3 bucket from which data will be retrieved. Add each bucket from which data is retrieved to the `Resource` list.
    + If you include S3 storage nodes, you need permissions to write to the Amazon S3 bucket in which output data will be stored. Add each bucket to which data is written to the `Resource` list.
    + If you include guardrails for a knowledge base node or a prompt node, you need permissions to apply the guardrails in a flow. Add each guardrail that's used in the flow to the `Resource` list.
    + If you include Lambda nodes, you need permissions to invoke the Lambda function. Add each Lambda function which needs to be invoked to the `Resource` list.
    + If you include Amazon Lex nodes, you need permissions to use the Amazon Lex bot. Add each bot alias which needs to be used to the `Resource` list.
    + If you encrypted any resource invoked in a flow, you need permissions to decrypt the key. Add each key to the `Resource` list.
+ If you encrypt the flow, you also need to attach a key policy to the KMS key that you use to encrypt the flow.

**Note**  
The following changes were recently implemented:  
Previously, AWS Lambda and Amazon Lex resources were invoked using the Amazon Bedrock service principal. This behavior is changing for flows created after 2024-11-22 and the Amazon Bedrock Flows service role will be used to invoke the AWS Lambda and Amazon Lex resources. If you created any flows that use either of these resources before 2024-11-22, you should update your Amazon Bedrock Flows service roles with AWS Lambda and Amazon Lex permissions.
Previously, Prompt management resources were rendered using the `bedrock:GetPrompt` action. This behavior is changing for flows created after 2024-11-22 and the `bedrock:RenderPrompt` action will be used to render the prompt resource. If you created any flows that use a prompt resource before 2024-11-22, you should update your Amazon Bedrock Flows service roles with `bedrock:RenderPrompt` permissions.
If you're using a service role that Amazon Bedrock automatically created for you in the console, Amazon Bedrock will attach the corrected permissions dynamically when you save the flow.

**Topics**
+ [Trust relationship](#flows-permissions-trust)
+ [Identity-based permissions for the flows service role.](#flows-permissions-identity)

## Trust relationship
<a name="flows-permissions-trust"></a>

Attach the following trust policy to the flow execution role to allow Amazon Bedrock to assume this role and manage a flow. Replace the {{values}} as necessary. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.

**Note**  
As a best practice, replace the {{\*}} with a flow ID after you have created it.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{FlowsTrustBedrock}}",
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
                    "AWS:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:flow/{{*}}"
                }
            }
        }
    ]
}
```

------

## Identity-based permissions for the flows service role.
<a name="flows-permissions-identity"></a>

Attach the following policy to provide permissions for the service role, replacing {{values}} as necessary. The policy contains the following statements. Omit a statement if it isn't applicable to your use-case. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.
+ Access to the Amazon Bedrock base models that the flow will use. Add each model that's used in the flow to the `Resource` list.
+ If you invoke a model using Provisioned Throughput, permissions to access and invoke the provisioned model. Add each model that's used in the flow to the `Resource` list.
+ If you invoke a custom model, permissions to access and invoke the custom model. Add each model that's used in the flow to the `Resource` list.
+ Permissions based on the nodes that you add to the flow:
  + If you include prompt nodes that use prompts from Prompt management, you need permissions to access the prompt. Add each prompt that's used in the flow to the `Resource` list.
  + If you include knowledge base nodes, you need permissions to query the knowledge base. Add each knowledge base that's queried in the flow to the `Resource` list.
  + If you include agent nodes, you need permissions to invoke an alias of the agent. Add each agent that's invoked in the flow to the `Resource` list.
  + If you include S3 retrieval nodes, you need permissions to access the Amazon S3 bucket from which data will be retrieved. Add each bucket from which data is retrieved to the `Resource` list.
  + If you include S3 storage nodes, you need permissions to write to the Amazon S3 bucket in which output data will be stored. Add each bucket to which data is written to the `Resource` list.
  + If you include guardrails for a knowledge base node or a prompt node, you need permissions to apply the guardrails in a flow. Add each guardrail that's used in the flow to the `Resource` list.
  + If you include Lambda nodes, you need permissions to invoke the Lambda function. Add each Lambda function which needs to be invoked to the `Resource` list.
  + If you include Amazon Lex nodes, you need permissions to use the Amazon Lex bot. Add each bot alias which needs to be used to the `Resource` list.
  + If you encrypted any resource invoked in a flow, you need permissions to decrypt the key. Add each key to the `Resource` list.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{InvokeModel}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{ModelId}}"
            ]
        },
        {
            "Sid": "{{InvokeProvisionedThroughput}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:GetProvisionedModelThroughput"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:provisioned-model/{{ModelId}}"
            ]
        },
        {
            "Sid": "{{InvokeCustomModel}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:GetCustomModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:custom-model/{{ModelId}}"
            ]
        },
        {
            "Sid": "{{UsePromptFromPromptManagement}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:RenderPrompt"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:prompt/{{PromptId}}"
            ]
        },
        {
            "Sid": "{{QueryKnowledgeBase}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{KnowledgeBaseId}}"
            ]
        },
        {
            "Sid": "{{InvokeAgent}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:agent-alias/{{AgentId}}/{{AgentAliasId}}"
            ]
        },
        {
            "Sid": "{{AccessS3Bucket}}",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        },
        {
            "Sid": "{{WriteToS3Bucket}}",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}",
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        },
        {
            "Sid": "{{GuardrailPermissions}}",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{GuardrailId}}"
            ]
        },
        {
            "Sid": "{{LambdaPermissions}}",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:{{us-east-1}}:{{123456789012}}:function:FunctionId"
            ]
        },
        {
            "Sid": "{{AmazonLexPermissions}}",
            "Effect": "Allow",
            "Action": [
                "lex:RecognizeUtterance"
            ],
            "Resource": [ 
                "arn:aws:lex:{{us-east-1}}:{{123456789012}}:bot-alias/{{BotId}}/{{BotAliasId}}"
            ]
        },
        {
            "Sid": "{{KMSPermissions}}",
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
             "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        }
    ]
}
```

------