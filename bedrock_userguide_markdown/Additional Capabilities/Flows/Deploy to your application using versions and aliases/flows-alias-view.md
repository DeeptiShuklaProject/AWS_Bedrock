

# View information about aliases of flows in Amazon Bedrock
<a name="flows-alias-view"></a>

To learn how to view information about the aliases of a flow, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view the details of an alias**

1. Open the [AWS Management Console](https://console.aws.amazon.com) and sign in to your account. Navigate to Amazon Bedrock.

1. Select **Flows** from the left navigation pane. Then, in the **Flows** section, select a flow.

1. Choose the alias to view from the **Aliases** section.

1. You can view the name and description of the alias and tags that are associated with the alias.

------
#### [ API ]

To get information about an alias of your flow, send a [GetFlowAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetFlowAlias.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the flow as the `flowIdentifier`. In the `aliasIdentifier` field, specify the ID or ARN of the alias.

To list information for all aliases of a flow, send a [ListFlowAliass](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListFlowAliass.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the flow as the `flowIdentifier`. You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

------