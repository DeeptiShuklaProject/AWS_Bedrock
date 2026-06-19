

# Disassociate a knowledge base from an agent
<a name="agents-kb-delete"></a>

To learn how to disassociate a knowledge base from an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To disassociate a knowledge base from an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**

1. In the **Knowledge bases** section, choose the option button that's next to the knowledge base that you want to delete. Then choose **Delete**.

1. Confirm the message that appears and then choose **Delete**.

1. To apply the changes that you made to the agent before testing it, choose **Prepare** in the **Test** window or at the top of the **Working draft** page.

------
#### [ API ]

To disassociate a knowledge base from an agent, send a [DisassociateAgentKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DisassociateAgentKnowledgeBase.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `knowledgeBaseId` and the `agentId` and `agentVersion` of the agent from which to disassociate it.

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

------