

# Delete session summaries
<a name="agents-memory-delete"></a>

To delete session summaries, send a [DeleteAgentMemory](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_DeleteAgentMemory.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

The following fields are required:


****  

| Field | Short description | 
| --- | --- | 
| agentId | The identifier of the agent. | 
| agentAliasId | The identifier of the agent alias. | 

The following field is optional.


****  

| Field | Short description | 
| --- | --- | 
| memoryId | The identifier of the memory that has the session summaries | 