

# View information about an agent-knowledge base association
<a name="agents-kb-view"></a>

To learn how to view information about a knowledge base, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a knowledge base that's associated with an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**

1. In the **Knowledge bases** section, select the knowledge base for which you want to view information.

------
#### [ API ]

To get information about a knowledge base associated with an agent, send a [GetAgentKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgentKnowledgeBase.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the following fields:

To list information about the knowledge bases associated with an agent, send a [ListAgentKnowledgeBases](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentKnowledgeBases.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `agentId` and `agentVersion` for which you want to see associated knowledge bases.


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

[See code examples](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-agent_example_bedrock-agent_ListAgentKnowledgeBases_section.html)

------