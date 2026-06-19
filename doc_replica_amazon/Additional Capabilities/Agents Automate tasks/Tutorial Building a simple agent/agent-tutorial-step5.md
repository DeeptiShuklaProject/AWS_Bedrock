

# Step 5: Call the agent from Python code
<a name="agent-tutorial-step5"></a>

In this step, you'll learn how to programmatically interact with your agent using the AWS SDK for Python (Boto). The example code demonstrates how to use the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) operation, which requires both the AGENT ID and ALIAS ID as parameters to call your agent. The code shows how to send a prompt to your agent, process the response, and handle both streaming and non-streaming response modes. This allows you to integrate your Bedrock agent into your own Python applications.

For more information, see [Invoke an agent from your application](agents-invoke-agent.md).

**To call the agent from Python code**

1. Get the ID for the agent. For more information, see [View information about an agent](agents-view.md).

1. Get the ID for the agent alias. For more information, see [View information about aliases of agents in Amazon Bedrock](agents-alias-view.md).

1. Run the following code. Update the following:
   + **AGENT\_ID** – to your agent's ID.
   + **ALIAS\_ID** – to your agent's Alias ID.
   + **REGION** – to the AWS Region in which you created your agent, such as `us-east-1`. 

   To stream the response from the agent, change the value of `streamFinalResponse` to `True`.

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
       "applyGuardrailInterval" : 20,
         "streamFinalResponse" : False
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
               service_name="bedrock-agent-runtime",
               region_name="{{REGION}}") 
       
       agent_id = "{{AGENT_ID}}"
       alias_id = "{{ALIAS_ID}}"
       session_id = "123456"
       prompt = "What's the current time?"
   
       try:
   
           invoke_agent(client, agent_id, alias_id, prompt, session_id)
   
       except ClientError as e:
           print(f"Client error: {str(e)}")
           logger.error("Client error: %s", {str(e)})
   ```