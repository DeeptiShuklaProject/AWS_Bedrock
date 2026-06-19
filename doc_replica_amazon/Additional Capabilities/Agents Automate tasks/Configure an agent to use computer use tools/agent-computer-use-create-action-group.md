

# Specify the computer use tools for the agent in an action group
<a name="agent-computer-use-create-action-group"></a>

 You can specify the tools available to the agent in the [CreateAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [UpdateAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) API operation. For inline agents, you specify the tool in the [InvokeInlineAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html) API operation. 

In parentActionGroupSignature of the action group, you specify the tool type from the following values:
+ ANTHROPIC.Computer
+ ANTHROPIC.TextEditor 
+ ANTHROPIC.Bash

The following code example shows how to create an action group that specifies the `ANTHROPIC.Computer` tool for the agent’s use.

```
def create_agent_action_group(client, agent_id, agent_version):
"""
Creates an action group that specifies the ANTHROPIC.Computer tool for the agent. 

Args:
    client: Boto3 bedrock-agent client
    agent_id (str): ID of the agent
    agent_version (str): Version of the agent

Returns:
    dict: Response from create_agent_action_group API call
"""
try:
    response = client.create_agent_action_group(
        agentId=agent_id,
        agentVersion=agent_version,
        actionGroupName="my_computer",
        actionGroupState="ENABLED",
        parentActionGroupSignature="ANTHROPIC.Computer",
        parentActionGroupSignatureParams={
            "type": "computer_20241022"
        }
    )
    return response
except ClientError as e:
    print(f"Error: {e}")
```