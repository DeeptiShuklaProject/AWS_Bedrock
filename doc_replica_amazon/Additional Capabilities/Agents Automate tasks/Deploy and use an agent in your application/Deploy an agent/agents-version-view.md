

# View information about versions of agents in Amazon Bedrock
<a name="agents-version-view"></a>

After you create a version of your agent, you can view information about it or delete it. You can create a new version of an agent by creating a new alias or by updating an existing alias.

To learn how to view information about the versions of an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a version of an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose the version to view from the **Versions** section.

1. To view details about the model, action groups, or knowledge bases attached to version of the agent, choose the name of the information that you want to view. You can't modify any part of a version. To make modifications to the agent, use the working draft and create a new version.

------
#### [ API ]

To get information about an agent version, send a [GetAgentVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgentVersion.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `agentId` and `agentVersion`.

To list information about an agent's versions, send a [ListAgentVersions](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentVersions.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the `agentId`. You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

------