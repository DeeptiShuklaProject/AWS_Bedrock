

# Configure your agent using conversational builder
<a name="agents-create-cb"></a>

Conversational builder is an interactive assistant that helps in configuring an agent for you. With conversational builder, you use natural language to describe the purpose of your agent which results in a fully testable agent being built that fulfills the purpose. The conversational builder interacts with you to get all the necessary information to build or update your agent.

**Important**  
The conversational builder is available in the Amazon Bedrock console in US East (N. Virginia), US West (Oregon), Europe (Frankfurt), Asia Pacific (Sydney), and Europe (Paris) regions.

Conversational builder performs *only* the following actions based on the interactions:
+ Update your agent’s name and description
+ Generate a summary of the agent instruction based on the instruction you provided in natural language
+ Create an action group 
+ Update an action group’s name and description
+ Define an action group function based off of a summary of the action group
+ Associate, list, and disassociate knowledge base
+ List or delete action groups

The following is an example of an interaction with the conversational builder:

```
Conversational builder: Hello, I can help you update your Agent's configurations.

What configurations would you like to update?
You can say something like "Associate a knowledge base"

User: Create a travel agent
Conversational builder:  What is the purpose of this travel agent? What kind of tasks or capabilities should it have?
User: Travel agent books flights and hotels for vacation
Conversational builder: The travel agent with the purpose of booking flights and hotels for vacations has been successfully created.
```

## Create and configure an agent using conversational builder in the Amazon Bedrock console
<a name="create-configure-cb"></a>

**To create an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane.

1. In the **Agents** section, choose **Create Agent**.

1. (Optional) Change the automatically generated **Name** for the agent and provide an optional **Description** for it.

1. Choose **Create**. Your agent is created and you will be taken to the **Agent builder** for your newly created agent, where you can configure your agent.

1. You can continue to the following procedure to configure your agent or return to the Agent builder later.

**To configure your agent**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**.

1. In the Agent builder, choose **Assistant**

1. In the Agent builder pane, enter the purpose of your agent. See the example interaction to get started interacting with the conversational builder assistant.

1. When conversational builder has completed configuring your agent, select one of the following options:
   + To stay in the **Agent builder**, choose **Save**. You can then **Prepare** the agent to test it with your updated configurations in the test window. To learn how to test your agent, see [Test and troubleshoot agent behavior](agents-test.md).
   + To return to the **Agent Details** page, choose **Save and exit**.

## Add the following permissions to use conversational builder in the Amazon Bedrock console
<a name="permissions-cb"></a>

If you plan to [Configure your agent using conversational builder](#agents-create-cb), make sure to attach the following permissions:

------
#### [ JSON ]

****  

```
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid": "InvokeInlineAgent",
      "Effect": "Allow",
      "Action": "bedrock:InvokeInlineAgent",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "bedrock:InlineAgentName": "AgentName-123"
        }
      }
    },
    {
      "Sid": "InvokeFoundationModel",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/{modelId}"
    },
    {
      "Sid": "S3AccessForKBAndActions",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::bucket-name/*"
    },
    {
      "Sid": "S3AccessForCodeInterpreter",
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAttributes",
        "s3:GetObjectAttributes"
      ],
      "Resource": "arn:aws:s3:::bucket/path/to/file"
    },
    {
      "Sid": "KnowledgeBaseAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:Retrieve",
        "bedrock:RetrieveAndGenerate"
      ],
      "Resource": "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/knowledge-base-id"
    },
    {
      "Sid": "GuardrailAccess",
      "Effect": "Allow",
      "Action": "bedrock:ApplyGuardrail",
      "Resource": "arn:aws:bedrock:us-east-1:123456789012:guardrail/guardrail-id"
    },
    {
      "Sid": "LambdaInvoke",
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:function-name"
    },
    {
      "Sid": "KMSAccess",
      "Effect": "Allow",
      "Action": [
        "kms:GenerateDataKey*",
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/key-id"
    }
  ]
}
```

------