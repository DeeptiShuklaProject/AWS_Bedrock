

# Invoke an agent from your application
<a name="agents-invoke-agent"></a>

Use your agent in an application by making an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). 

By default, the response from `InvokeAgent` includes a chunk that contains the complete response from the agent, which can take a while to complete. Alternatively, you can configure `InvokeAgent` to stream the response in multiple smaller chunks. This decreases the latency of the initial response from the agent. 

**Streaming responses**

You can optionally enable streaming of the response by setting the `streamFinalResponse` to `true` in streaming configurations ( [StreamingConfigurations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_StreamingConfigurations.html)). The response stream contains multiple events with chunks for each part of the response in order.

To stream responses, make sure the agent execution role includes the `bedrock:InvokeModelWithResponseStream` permission for the configured Agent model. For more information, see [Identity-based permissions for the Agents service role](agents-permissions.md#agents-permissions-identity).

If your agent is configured with a Guardrail, you can also specify the `applyGuardrailInterval` in the `StreamingConfigurations`, to control how often an `ApplyGuardrail` call is made on outgoing response characters (for example, every 50 characters).

By default, the guardrail interval is set to 50 characters. If a larger interval is specified, the response will be generated in larger chunks with fewer `ApplyGuardrail` calls. The following examples show the response generated for *Hello, I am an agent* input string.

**Example response in chunks: Interval set to 3 characters**

```
'Hel', 'lo, ', 'I am', ' an', ' Age', 'nt'
```

Each chunk has at least 3 characters except for the last chunk.

**Example response in chunks: Interval set to 20 or more characters**

```
'Hello, I am an Agent'
```

## Invoke an agent
<a name="invoke-agent-example"></a>

The following Python example shows how to call the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) operation and display the output from the agent, as well as any [trace](trace-events.md) information that the call generates. 

**To invoke an agent**

1. Create an agent by following the instructions at [Create and configure agent manually](agents-create.md). Note the ID for the agent. If necessary, you can get the ID later. For more information, see [View information about an agent](agents-view.md).

1. Create an alias for the agent, by following the instructions at [Create an alias for your agent](deploy-agent-proc.md). Note the ID of the alias. If necessary, you can get the ID later. For more information, see [View information about aliases of agents in Amazon Bedrock](agents-alias-view.md).

1. Run the following code. Update the value of `agent_id` to your agent's ID and the value of `alias_id` to the alias ID of the agent. To stream the response from the agent, change the value of `streamFinalResponse` to `True`. You can also change the guardrail interval by changing the value of `applyGuardrailInterval`.

   ```
   import boto3
   import logging
   
   from botocore.exceptions import ClientError
   
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def invoke_agent(client, agent_id, alias_id, prompt, session_id):
           response = client.invoke_agent(
               agentId=agent_id,
               agentAliasId=alias_id,
               enableTrace=True,
               sessionId = session_id,
               inputText=prompt,
               streamingConfigurations = { 
       "applyGuardrailInterval" : {{20}},
         "streamFinalResponse" : {{False}}
               }
           )
           completion = ""
           for event in response.get("completion"):
               #Collect agent output.
               if 'chunk' in event:
                   chunk = event["chunk"]
                   completion += chunk["bytes"].decode()
               
               # Log trace output.
               if 'trace' in event:
                   trace_event = event.get("trace")
                   trace = trace_event['trace']
                   for key, value in trace.items():
                       logging.info("%s: %s",key,value)
   
           print(f"Agent response: {completion}")
   
   
   if __name__ == "__main__":
   
       client=boto3.client(
               service_name="bedrock-agent-runtime"
           )
       
       agent_id = "{{AGENT_ID}}"
       alias_id = "{{ALIAS_ID}}"
       session_id = "{{MY_SESSION_ID}}"
       prompt = "{{Prompt to send to agent}}"
   
       try:
   
           invoke_agent(client, agent_id, alias_id, prompt, session_id)
   
       except ClientError as e:
           print(f"Client error: {str(e)}")
           logger.error("Client error: %s", {str(e)})
   ```