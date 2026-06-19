

# Modify an agent-knowledge base association
<a name="agents-kb-edit"></a>

To learn how to modify an agent-knowledge base association, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To modify an agent-knowledge base association**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**

1. In the **Action groups** section, select an action group to edit. Then choose **Edit**.

1. Edit the existing fields as necessary. For more information, see [Augment response generation for your agent with knowledge base](agents-kb-add.md).

1. To control whether the agent can use the knowledge base, select **Enabled** or **Disabled**. Use this function to help troubleshoot your agent's behavior.

1. To remain in the same window so that you can test your change, choose **Save**. To return to the **Working draft** page, choose **Save and exit**.

1. To apply the changes that you made to the agent before testing it, choose **Prepare** in the **Test** window or at the top of the **Working draft** page.

------
#### [ API ]

To modify the configuration of a knowledge base associated with an agent, send an [UpdateAgentKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentKnowledgeBase.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same. You must specify the `agentVersion` as `DRAFT`. For more information about required and optional fields, see [Augment response generation for your agent with knowledge base](agents-kb-add.md).

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

------