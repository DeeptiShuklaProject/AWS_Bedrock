

# View information about an action group
<a name="agents-action-view"></a>

To learn how to view information about an action group, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about an action group**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose an agent in the **Agents** section.

1. On the agent details page, for the **Working draft** section, choose the working draft.

1. In the **Action groups** section, choose an action group for which to view information.

------
#### [ API ]

To get information about an action group, send a [GetAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgentActionGroup.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the `actionGroupId`, `agentId`, and `agentVersion`.

To list information about an agent's action groups, send a [ListAgentActionGroups](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentActionGroups.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `agentId` and `agentVersion` for which you want to see action groups. You can include the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

```
    def list_agent_action_groups(self, agent_id, agent_version):
        """
        List the action groups for a version of an Amazon Bedrock Agent.

        :param agent_id: The unique identifier of the agent.
        :param agent_version: The version of the agent.
        :return: The list of action group summaries for the version of the agent.
        """

        try:
            action_groups = []

            paginator = self.client.get_paginator("list_agent_action_groups")
            for page in paginator.paginate(
                    agentId=agent_id,
                    agentVersion=agent_version,
                    PaginationConfig={"PageSize": 10},
            ):
                action_groups.extend(page["actionGroupSummaries"])

        except ClientError as e:
            logger.error(f"Couldn't list action groups. {e}")
            raise
        else:
            return action_groups
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------