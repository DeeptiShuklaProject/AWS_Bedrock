

# Handle computer use tool requests from agents in conversations
<a name="agent-computer-use-handle-tools"></a>

When your agent requests a tool, the response to your InvokeAgent API operation includes a `returnControl` payload that includes the tool to use and the tool action in the invocationInputs. For more information about return control to agent developer, see [Return control to the agent developer by sending elicited information in an InvokeAgent response](agents-returncontrol.md).

**Topics**
+ [Return control example](#agent-computer-use-tool-request-format)
+ [Code example to parse the tool request](#agent-computer-use-implementation-example)

## Return control example
<a name="agent-computer-use-tool-request-format"></a>

The following is an example of a `returnControl` payload with a request to use the `ANTHROPIC.Computer` tool with the `screenshot` action.

```
{
    "returnControl": {
        "invocationId": "invocationIdExample",
        "invocationInputs": [{
            "functionInvocationInput": {
                "actionGroup": "my_computer",
                "actionInvocationType": "RESULT",
                "agentId": "agentIdExample",
                "function": "computer",
                "parameters": [{
                    "name": "action",
                    "type": "string",
                    "value": "screenshot"
                }]
            }
        }]
    }
}
```

## Code example to parse the tool request
<a name="agent-computer-use-implementation-example"></a>

The following code shows how to extract the computer use tool choice in an InvokeAgent response, map it to mock tool implementations for different tools, and then send the result of the tool use in a subsequent InvokeAgent request.
+ The `manage_computer_interaction` function runs a loop where it calls the InvocationAgent API operation and parses the response until there is no task to complete. When it parses the response, it extracts any tools to use from the `returnControl` payload and passes the `handle_computer_action` function.
+ The `handle_computer_action` maps the function name to mock implementations for four actions. For example tool implementations, see [computer-use-demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/) in the Anthropic GitHub repository. 

For more information about computer use tools, including implementation examples and tool descriptions, see [Computer use (beta)](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) in the Anthropic documentation.

```
import boto3
from botocore.exceptions import ClientError
import json


def handle_computer_action(action_params):
    """
    Maps computer actions, like taking screenshots and moving the mouse to mock implementations and returns
    the result.

    Args:
        action_params (dict): Dictionary containing the action parameters
            Keys:
                - action (str, required): The type of action to perform (for example 'screenshot' or 'mouse_move')
                - coordinate (str, optional): JSON string containing [x,y] coordinates for mouse_move

    Returns:
        dict: Response containing the action result.
    """

    action = action_params.get('action')
    if action == 'screenshot':
        # Mock screenshot response
        with open("mock_screenshot.png", 'rb') as image_file:
            image_bytes = image_file.read()
        return {
            "IMAGES": {
                "images": [
                    {
                        "format": "png",
                        "source": {
                            "bytes": image_bytes
                        },
                    }
                ]
            }
        }
    elif action == 'mouse_move':
        # Mock mouse movement
        coordinate = json.loads(action_params.get('coordinate', '[0, 0]'))
        return {
            "TEXT": {
                "body": f"Mouse moved to coordinates {coordinate}"
            }
        }
    elif action == 'left_click':
        # Mock mouse left click
        return {
            "TEXT": {
                "body": f"Mouse left clicked"
            }
        }
    elif action == 'right_click':
        # Mock mouse right click
        return {
            "TEXT": {
                "body": f"Mouse right clicked"
            }
        }

    ### handle additional actions here


def manage_computer_interaction(bedrock_agent_runtime_client, agent_id, alias_id):
    """
    Manages interaction between an Amazon Bedrock agent and computer use functions.

    Args:
        bedrock_agent_runtime_client: Boto3 client for Bedrock agent runtime
        agent_id (str): The ID of the agent
        alias_id (str): The Alias ID of the agent

    The function:
    - Initiates a session with initial prompt
    - Makes agent requests with appropriate parameters
    - Processes response chunks and return control events
    - Handles computer actions via handle_computer_action()
    - Continues interaction until task completion
    """
    session_id = "session123"
    initial_prompt = "Open a browser and go to a website"
    computer_use_results = None
    current_prompt = {{initial_prompt}}

    while True:
        # Make agent request with appropriate parameters
        invoke_params = {
            "agentId": agent_id,
            "sessionId": session_id,
            "inputText": current_prompt,
            "agentAliasId": alias_id,
        }

        # Include session state if we have results from previous iteration
        if computer_use_results:
            invoke_params["sessionState"] = computer_use_results["sessionState"]

        try:
            response = bedrock_agent_runtime_client.invoke_agent(**invoke_params)
        except ClientError as e:
            print(f"Error: {e}")

        has_return_control = False

        # Process the response
        for event in response.get('completion'):
            if 'chunk' in event:
                chunk_content = event['chunk'].get('bytes', b'').decode('utf-8')
                if chunk_content:
                    print("\nAgent:", chunk_content)

            if 'returnControl' in event:
                has_return_control = True
                invocationId = event["returnControl"]["invocationId"]
                if "invocationInputs" in event["returnControl"]:
                    for invocationInput in event["returnControl"]["invocationInputs"]:
                        func_input = invocationInput["functionInvocationInput"]

                        # Extract action parameters
                        params = {p['name']: p['value'] for p in func_input['parameters']}

                        # Handle computer action and get result
                        action_result = handle_computer_action(params)

                        # Print action result for testing
                        print("\nExecuting function:", func_input['function'])
                        print("Parameters:", params)

                        # Prepare the session state for the next request
                        computer_use_results = {
                            "sessionState": {
                                "invocationId": invocationId,
                                "returnControlInvocationResults": [{
                                    "functionResult": {
                                        "actionGroup": func_input['actionGroup'],
                                        "responseState": "REPROMPT",
                                        "agentId": func_input['agentId'],
                                        "function": func_input['function'],
                                        "responseBody": action_result
                                    }
                                }]
                            }
                        }

        # If there's no return control event, the task is complete
        if not has_return_control:
            print("\nTask completed!")
            break

        # Use empty string as prompt for subsequent iterations
        current_prompt = ""
def main():
    bedrock_agent_runtime_client = boto3.client(service_name="bedrock-agent-runtime",
                                         region_name="{{REGION}}"
                                         )

    agent_id = "{{AGENT_ID}}"
    alias_id = "{{ALIAS_ID}}"

    manage_computer_interaction(bedrock_agent_runtime_client, agent_id, alias_id)


if __name__ == "__main__":
    main()
```

The output should be similar to the following:

```
Executing function: computer
Parameters: {'action': 'screenshot'}

Executing function: computer
Parameters: {'coordinate': '[467, 842]', 'action': 'mouse_move'}

Executing function: computer
Parameters: {'action': 'left_click'}

Agent: I've opened Firefox browser. Which website would you like to visit?

Task completed!
```