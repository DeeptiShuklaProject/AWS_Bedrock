

# Retain conversational context across multiple sessions using memory
<a name="agents-memory"></a>

Memory provides your agent the ability to retain conversational context across multiple sessions and to recall past actions and behaviors. By default, your agent retains conversational context from a single session. To configure memory for your agent, enable the memory setting for your agent and specify the storage duration to retain the memory.

The conversational context is stored in the memory as sessions with each session given a session identifier (ID) that you provide when you invoke the agent. You can specify the same session Id across requests to continue the same conversation. 

After you enable memory for your agent, the current session gets associated with a specific memory context when either of the following occurs:
+ You invoke the agent with the same `sessionId` as the current session and with `endSession` set to `true`.
+ The `idleSessionTimeout` configured for the agent has elapsed.

This memory context is given a unique memory identifier. Your agent uses the memory context to access and use the stored conversation history and conversation summaries to generate responses. 

If you have multiple users, make sure to provide the same memory identifier (memoryId) for the same user. The agent stores the memory for each user against that memoryId and the next time you invoke the agent with the same memoryId, the summary of each session stored in the memory gets loaded to the current session. 

You can access the memory at any time to view the summarized version of the sessions that are stored in the memory. You can also, at any time, clear the memory by deleting all the sessions stored in the memory. 

**Memory summarization**

Your agent uses the memory summarization [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md) to call the foundation model with guidelines to summarize all your sessions. You can optionally modify the default prompt template or provide your own custom parser to parse model output.

Since the summarization process takes place in an asynchronous flow after a session ends, logs for any failures in summarization due to overridden template or parser will be published to your AWS accounts. For more information on enabling the logging, see [Enable memory summarization log delivery](agents-memory-log-delivery-enable.md). 

**Memory duration**

If memory is enabled, your agent retains the sessions in the memory for up to 365 days. You can optionally configure the retention period by specifying a duration between 1 and 365 days. All session summaries beyond this duration will be deleted.