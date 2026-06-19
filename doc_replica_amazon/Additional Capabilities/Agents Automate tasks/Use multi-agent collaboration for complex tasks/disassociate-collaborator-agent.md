

# Disassociate collaborator agent
<a name="disassociate-collaborator-agent"></a>

You can disassociate one or more collaborator agents from the supervisor agent in the Amazon Bedrock console, using the APIs, using the AWS CLI, or by using the AWS SDK. To learn how to disassociate a collaborator agent choose the tab for your preferred method, and then follow the steps:.

------
#### [ Console ]

**To disassociate collaborator agent from the supervisor agent,**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent builder**.

1. In the **Agent builder**, scroll down to the **Multi-agent collaboration** section and choose **Edit**.

1. In the **Multi-agent collaboration** page, choose **Expand all**.

1. In the **Agent collaborator** sections, go to the collaborator agent section you want to disassociate and choose the trash can icon.

1. After you've finished disassociating collaborator agents, choose **Save** and then **Prepare** to test your updated multi-agent collaboration configurations. To learn how to test your multi-agent collaboration team, see [Test and troubleshoot agent behavior](agents-test.md).

1. To return to the **Agent Details** page, choose **Save and exit**.

------
#### [ API ]

To disassociate a collaborator agent, send an `DisassociateAgentCollaborator` request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same..

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

You must minimally include the following fields:


****  

| Field | Use case | 
| --- | --- | 
| agentId | The agent ID. | 
| agentVersion | The agent version. | 
| collaboratorId | The collaborator agent ID. | 

------