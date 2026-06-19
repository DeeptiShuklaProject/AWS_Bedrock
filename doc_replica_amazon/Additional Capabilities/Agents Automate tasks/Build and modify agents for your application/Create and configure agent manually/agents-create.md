

# Create and configure agent manually
<a name="agents-create"></a>

To create an agent with Amazon Bedrock, you set up the following components:
+ The configuration of the agent, which defines the purpose of the agent and indicates the foundation model (FM) that it uses to generate prompts and responses.
+ At least one of the following:
  + Action groups that define what actions the agent is designed to perform.
  + A knowledge base of data sources to augment the generative capabilities of the agent by allowing search and query.

You can minimally create an agent that only has a name. To **Prepare** an agent so that you can [test](agents-test.md) or [deploy](agents-deploy.md) it, you must minimally configure the following components:


****  

| Configuration | Description | 
| --- | --- | 
| Agent resource role | The ARN of the [service role with permissions to call API operations on the agent](agents-permissions.md) | 
| Foundation model (FM) | An FM for the agent to invoke to perform orchestration | 
| Instructions | Natural language describing what the agent should do and how it should interact with users | 

You should also configure at least one action group or knowledge base for the agent. If you prepare an agent with no action groups or knowledge bases, it will return responses based only on the FM and instructions and [base prompt templates](advanced-prompts.md).

To learn how to create an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

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

1. In the **Agent details** section, you can set up the following configurations:

   1. Edit the **Agent name** or **Agent description**.

   1. For the **Agent resource role**, select one of the following options:
      + **Create and use a new service role** – Let Amazon Bedrock create the service role and set up the required permissions on your behalf.
      + **Use an existing service role** – Use a [custom role](agents-permissions.md) that you set up previously.

   1. For **Select model**, select an FM for your agent to invoke during orchestration.

      By default, models optimized for agents are shown. To see all models supported by Amazon Bedrock Agents, clear **Bedrock Agents optimized**.
**Tip**  
To use cross-Region inference with your agent, specify an inference profile ID in the `foundationModel` field when using the API. For more information, see [Increase throughput with cross-Region inference](cross-region-inference.md).  
![Foundation models available for agents, with optimization status for the agent framework.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/agents/agents-optimized-model-selection.png)

   1. In **Instructions for the Agent**, enter details to tell the agent what it should do and how it should interact with users. The instructions replace the $instructions$ placeholder in the [orchestration prompt template](prompt-placeholders.md#placeholders-orchestration). Following is an example of instructions:

      ```
      {{You are an office assistant in an insurance agency. You are friendly and polite. You help with managing insurance claims and coordinating pending paperwork.}}
      ```

   1. If you expand **Additional settings**, you can modify the following configurations:
      + **Code Interpreter** – (Optional) Choose whether to enable agent to handle tasks that involve writing, running, testing, and troubleshooting code. For details, see [Generate, run, and test code with code interpretation](agents-code-interpretation.md).
      + **User input** – (Optional) Choose whether to allow the agent to request more information from the user if it doesn't have enough information. For details, see [Configure agent to request information from user](agents-user-input.md).
      + **KMS key selection** – (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with your own customer managed key, for the KMS key selection section, select **Customize encryption settings (advanced)**. To create a new key, select **Create an AWS KMS key** and then refresh this window. To use an existing key, select a key for **Choose an AWS KMS key**.
      + **Idle session timeout** – By default, if a user hasn't responded for 30 minutes in a session with an Amazon Bedrock agent, the agent no longer maintains the conversation history. Conversation history is used to both resume an interaction and to augment responses with context from the conversation. To change this default length of time, enter a number in the **Session timeout** field and choose a unit of time.

   1. For the **IAM permissions** section, for **Agent resource role**, choose a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role). To let Amazon Bedrock create the service role on your behalf, choose **Create and use a new service role**. To use a [custom role](agents-permissions.md) that you created previously, choose **Use an existing service role**.
**Note**  
The service role that Amazon Bedrock creates for you doesn't include permissions for features that are in preview. To use these features, [attach the correct permissions to the service role](agents-permissions.md).

   1. (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with your own customer managed key, for the **KMS key selection** section, select **Customize encryption settings (advanced)**. To create a new key, select **Create an AWS KMS key** and then refresh this window. To use an existing key, select a key for **Choose an AWS KMS key**.

   1. (Optional) To associate tags with this agent, for the **Tags – optional** section, choose **Add new tag** and provide a key-value pair.

   1. When you are done setting up the agent configuration, select **Next**.

1. In the **Action groups** section, you can choose **Add** to add action groups to your agent. For more information on setting up action groups, see [Use action groups to define actions for your agent to perform](agents-action-create.md). To learn how to add action groups to your agent, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

1. In the **Knowledge bases** section, you can choose **Add** to associate knowledge groups with your agent. For more information on setting up knowledge bases, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md). To learn how to associate knowledge bases with your agent, see [Augment response generation for your agent with knowledge base](agents-kb-add.md).

1. In the **Guardrails details** section, you can choose **Edit** to associate a guardrail with your agent to block and filter out harmful content. Select a guardrail you want to use from the drop down menu under **Select guardrail** and then choose the version to use under **Guardrail version**. You can select **View** to see your Guardrail settings. For more information, see [Detect and filter harmful content by using Amazon Bedrock Guardrails](guardrails.md).

1. In the **Orchestration strategy** section, you can choose **Edit** to customize your agent's orchestration. For more information about the orchestration strategy you can use for your agent, see [Customize agent orchestration strategy](orch-strategy.md).

1. In the **Multi-agent collaboration** section, you can choose **Edit** to create a multi-agent collaboration team. For more information about multi-agent collaboration, see [Use multi-agent collaboration with Amazon Bedrock Agents](agents-multi-agent-collaboration.md).

1. When you finish configuring your agent, select one of the following options:
   + To stay in the **Agent builder**, choose **Save**. You can then **Prepare** the agent to test it with your updated configurations in the test window. To learn how to test your agent, see [Test and troubleshoot agent behavior](agents-test.md).
   + To return to the **Agent Details** page, choose **Save and exit**.

------
#### [ API ]

To create an agent, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

[See code examples](bedrock-agent_example_bedrock-agent_CreateAgent_section.md)

To prepare your agent and test or deploy it, so that you can [test](agents-test.md) or [deploy](agents-deploy.md) it, you must minimally include the following fields (if you prefer, you can skip these configurations and configure them later by sending an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request):


****  

| Field | Use case | 
| --- | --- | 
| agentResourceRoleArn | To specify an ARN of the service role with permissions to call API operations on the agent | 
| foundationModel | To specify a foundation model (FM) for the agent to orchestrate with | 
| instruction | To provide instructions to tell the agent what to do. Used in the $instructions$ placeholder of the orchestration prompt template. | 

The following fields are optional:


****  

| Field | Use case | 
| --- | --- | 
| description | Describes what the agent does | 
| idleSessionTTLInSeconds | Duration after which the agent ends the session and deletes any stored information. | 
| customerEncryptionKeyArn | ARN of a KMS key to encrypt agent resources | 
| tags | To associate [tags](tagging.md) with your agent. | 
| promptOverrideConfiguration | To [customize the prompts](advanced-prompts.md) sent to the FM at each step of orchestration. | 
| guardrailConfiguration | To add a [guardrail](guardrails.md) to the agent. Specify the ID or ARN of the guardrail and the version to use. | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 
| cachingState | To enable prompt caching of input to the agent. For more information, see [Prompt caching for faster model inference](prompt-caching.md). | 
| reasoning\_config | To enable model reasoning so that the model explains how it reached its conclusions. Use inside of a additionalModelRequestFields field. You must specify the number of budget\_tokens that are used for model reasoning, which are a subset of the output tokens. For more information, see [Enhance model responses with model reasoning](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-reasoning.html). | 

The response returns an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object that contains details about your newly created agent. If your agent fails to be created, the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object in the response returns a list of `failureReasons` and a list of `recommendedActions` for you to troubleshoot.

```
    def create_agent(self, agent_name, foundation_model, role_arn, instruction):
        """
        Creates an agent that orchestrates interactions between foundation models,
        data sources, software applications, user conversations, and APIs to carry
        out tasks to help customers.

        :param agent_name: A name for the agent.
        :param foundation_model: The foundation model to be used for orchestration by the agent.
        :param role_arn: The ARN of the IAM role with permissions needed by the agent.
        :param instruction: Instructions that tell the agent what it should do and how it should
                            interact with users.
        :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
        """
        try:
            response = self.client.create_agent(
                agentName=agent_name,
                foundationModel=foundation_model,
                agentResourceRoleArn=role_arn,
                instruction=instruction,
            )
        except ClientError as e:
            logger.error(f"Error: Couldn't create agent. Here's why: {e}")
            raise
        else:
            return response["agent"]
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------