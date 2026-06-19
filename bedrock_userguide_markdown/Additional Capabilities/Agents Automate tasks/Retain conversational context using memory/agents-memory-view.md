

# View memory sessions
<a name="agents-memory-view"></a>

The agent stores the memory for each session against the unique memory identifier (`memoryId`) provided for each user when you invoke the agent. The next time you invoke the agent with the same `memoryId`, the entire memory is loaded to the session. After you end the session, the agent generates a summarized version of the session and stores the session summary.

**Note**  
It can take several minutes after you end your session for the session summaries to appear in the console or in the API response.

To learn how to view the session summaries, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view session summaries,**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. In the **Test** window, choose the expand icon and choose **Memory** tab.

   If you are in **Agent builder** page, in the **Memory** section, choose **View memory**.

1. You can also view memory sessions when you are testing your agent. To view sessions stored in the memory when you are testing,

   1. In the test window, choose **Show trace** and then choose **Memory** tab.
**Note**  
If you are viewing memory sessions when you are testing your agent, you can view the session summary only after the latest session has ended. If you try to view memory sessions when the current session is in progress you will be informed that session summary is being generated and it will take time to generate the sessions. You can force end the current session by choosing the broom icon. 

------
#### [ API ]

To view memory sessions of your agent, send a [GetAgentMemory](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_GetAgentMemory.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

The following fields are required:


****  

| Field | Short description | 
| --- | --- | 
| agentId | The identifier of the agent | 
| agentAliasId | The identifier of the agent alias | 
| memoryId | The identifier of the memory that has the session summaries | 
| memoryType | The type of memory. Valid value: SESSION\_SUMMARY | 

**Note**  
If you are viewing memory sessions when you are testing your agent, you can view the session summary only after the latest session has ended. If you try to view memory sessions when the current session is in progress you will be informed that session summary is being generated and it will take time to generate the sessions. You can force end the current session by sending an [InvokeAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_InvokeAgent.html) request and specifying `Y` for the `endSession` field. 

------