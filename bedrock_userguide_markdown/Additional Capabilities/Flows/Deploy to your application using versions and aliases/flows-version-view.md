

# View information about versions of flows in Amazon Bedrock
<a name="flows-version-view"></a>

To learn how to view information about the versions of a flow, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a version of a flow**

1. Open the [AWS Management Console](https://console.aws.amazon.com) and sign in to your account. Navigate to Amazon Bedrock.

1. Select **Flows** from the left navigation pane. Then, in the **Flows** section, select a flow you want to view.

1. Choose the version to view from the **Versions** section.

1. To view details about the nodes and configurations attached to version of the flow, select the node and view the details in the **Flow builder** pane. To make modifications to the flow, use the working draft and create a new version.

------
#### [ API ]

To get information about a version of your flow, send a [GetFlowVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetFlowVersion.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the flow as the `flowIdentifier`. In the `flowVersion` field, specify the version number.

To list information for all versions of a flow, send a [ListFlowVersions](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListFlowVersions.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the flow as the `flowIdentifier`. You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

------