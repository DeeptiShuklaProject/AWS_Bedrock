

# View information about an agent
<a name="agents-view"></a>

After you create an agent, you can view or update its configuration as required. The configuration applies to the working draft. If you no longer need an agent, you can delete it.

To learn how to view information about an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. On the agent details page, you can see configurations that apply to all versions of the agent, associated tags, and its versions and aliases.

1. To see details about the working draft of the agent, choose **Edit in Agent builder**.

------
#### [ API ]

To get information about an agent, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the `agentId`. 

```
    def get_agent(self, agent_id, log_error=True):
        """
        Gets information about an agent.

        :param agent_id: The unique identifier of the agent.
        :param log_error: Whether to log any errors that occur when getting the agent.
                          If True, errors will be logged to the logger. If False, errors
                          will still be raised, but not logged.
        :return: The information about the requested agent.
        """

        try:
            response = self.client.get_agent(agentId=agent_id)
            agent = response["agent"]
        except ClientError as e:
            if log_error:
                logger.error(f"Couldn't get agent {agent_id}. {e}")
            raise
        else:
            return agent
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

To list information about your agents, send a [ListAgents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgents.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). [See code examples](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-agent_example_bedrock-agent_ListAgents_section.html). You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

To list all the tags for an agent, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListTagsForResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and include the Amazon Resource Name (ARN) of the agent.

```
    def list_agents(self):
        """
        List the available Amazon Bedrock Agents.

        :return: The list of available bedrock agents.
        """

        try:
            all_agents = []

            paginator = self.client.get_paginator("list_agents")
            for page in paginator.paginate(PaginationConfig={"PageSize": 10}):
                all_agents.extend(page["agentSummaries"])

        except ClientError as e:
            logger.error(f"Couldn't list agents. {e}")
            raise
        else:
            return all_agents
```

For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------