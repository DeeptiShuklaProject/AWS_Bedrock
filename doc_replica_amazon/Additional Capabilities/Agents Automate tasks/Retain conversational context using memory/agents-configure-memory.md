

# Enable agent memory
<a name="agents-configure-memory"></a>

To configure memory for your agent, you must first enable memory and then optionally specify the retention period for the memory. You can enable memory for your agent when you [create](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-create.html) or [update](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-manage.html#agents-edit) your agent. 

**Note**  
You can enable memory for Agents on all the models *except* the following:   
Amazon Titan Text Premier
Anthropic Claude Instant
Make sure that the model you are planning to use is available in your Region. For more information, see [Model support by AWS Region.](https://docs.aws.amazon.com//bedrock/latest/userguide/models-supported.html)

To learn how to configure memory for your agent, select the tab corresponding to your method of choice and follow steps.

------
#### [ Console ]

**To configure memory for your agent**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent Builder**

1. In the Agent details section, for **Select model**.

1. In the **Memory** section, do the following:

   1. For **Enable session summarization**, select **Enabled**.

   1. (Optional) For **Memory duration**, enter a number between 1 and 365 to specify the memory duration for your agent. By default, agent retains conversational context for 30 days. 

   1. For **Maximum number of recent sessions**, select a number for maximum number of recent sessions to store as memory.

   1. (Optional) You can optionally make changes to your session summarization prompt. To make changes, in the **Session summarization prompt**, choose **View and edit**.

1. Make sure to first **Save** and then **Prepare** to apply the changes you have made to the agent before testing it. 

------
#### [ API ]

To enable and configure memory for your agent, send an [CreateAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgent.html) or [UpdateAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_UpdateAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

In the Amazon Bedrock API, you specify the `memoryConfiguration` when you send a [CreateAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgent.html) or [UpdateAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_UpdateAgent.html) request. 

The following shows the general format of the `memoryConfiguration`: 

```
"memoryConfiguration": {
"enabledMemoryTypes": [ "SESSION_SUMMARY" ],
"storageDays":{{30}},
"sessionSummaryConfiguration": {
    "maxRecentSessions": {{5}}
    }
}
```

You can optionally configure the memory retention period by assigning the `storageDays` with a number between 1 and 365 days.

**Note**  
If you enable memory for the agent and do not specify `memoryId` when you invoke the agent, agent will not store that specific turn in the memory.

------