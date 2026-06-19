

# Converse with an Amazon Bedrock flow
<a name="flows-multi-turn-invocation"></a>

**Note**  
Amazon Bedrock Flows multi-turn conversation is in preview release for Amazon Bedrock and is subject to change.

Amazon Bedrock Flows multi-turn conversation enables dynamic, back-and-forth conversations between users and flows, similar to a natural dialogue. When an agent node requires clarification or additional context, it can intelligently pause the flow's execution and prompt the user for specific information. This creates a more interactive and context-aware experience, as the node can adapt its behavior based on user responses. For example, if an initial user query is ambiguous or incomplete, the node can ask follow-up questions to gather the necessary details. Once the user provides the requested information, the flow seamlessly resumes execution with the enriched input, ensuring more accurate and relevant results. This capability is particularly valuable for complex scenarios where a single interaction may not be sufficient to fully understand and address the user's needs.

**Topics**
+ [How to process a multi-turn conversation in a flow](#flows-multi-turn-invocation-how)
+ [Creating and running an example flow](#flows-multi-turn-invocation-example-flow)

## How to process a multi-turn conversation in a flow
<a name="flows-multi-turn-invocation-how"></a>

To use a multi-turn conversation in a flow, you need an [agent node](flows-nodes.md#flows-nodes-agent) connected to an Amazon Bedrock agent. When you run the flow, a multi-turn conversation happens when the agent needs further information from the user before it can continue. This section describes a flow that uses an agent with the following instructions:

```
You are a playlist creator for a radio station. 
When asked to create a playlist, ask for the number of songs,
the genre of music, and a theme for the playlist.
```

For information about creating an agent see [Automate tasks in your application using AI agents](agents.md). 

### Step 1: Start the flow
<a name="flows-multi-turn-invocation-start-flow"></a>

You start a flow by calling the [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) operation. You include the initial content that you want to send to the flow. In the following example, the `document` field contains a request to *Create a playlist*. Each conversation has a unique identifer (*execution ID*) that identifies the conversation within the flow. To get the execution ID, you don't send the`executionID` field in your first call to `InvokeFlow`. The response from `InvokeFlow` includes the execution ID. In your code, use the identifer to track multiple conversations and identify a conversation in further calls to the `InvokeFlow` operation. 

The following is example JSON for a request to `InvokeFlow`.

```
{
  "flowIdentifier": "XXXXXXXXXX",
  "flowAliasIdentifier": "YYYYYYYYYY",
  "inputs": [
    {
      "content": {
        "document": "Create a playlist."
      },
      "nodeName": "FlowInputNode",
      "nodeOutputName": "document"
    }
  ]
}
```

### Step 2: Retrieve agent requests
<a name="flows-multi-turn-invocation-retrieve-requests"></a>

If the agent node in the flow decides that it needs more information from the user, the response stream (`responseStream`) from `InvokeFlow` includes an `FlowMultiTurnInputRequestEvent` event object. The event has the requested information in the `content` (`FlowMultiTurnInputContent`) field. In the following example, the request in the `document` field is for information about the number of songs, genre of music, and theme for the playlist. In your code, you then need to get that information from the user.

The following is an example `FlowMultiTurnInputRequestEvent` JSON object.

```
{
    "nodeName": "AgentsNode_1",
    "nodeType": "AgentNode",
    "content": {
        "document": "Certainly! I'd be happy to create a playlist for you. To make sure it's tailored to your preferences, could you please provide me with the following information:
        1. How many songs would you like in the playlist?
        2. What genre of music do you prefer? 
        3. Is there a specific theme or mood you'd like for the playlist? Once you provide these details, I'll be able to create a customized playlist just for you."
    }
}
```

Since the flow cannot continue until more input is received, the flow also emits a `FlowCompletionEvent` event. A flow always emits the `FlowMultiTurnInputRequestEvent` before the `FlowCompletionEvent`. If the value of `completionReason` in the `FlowCompletionEvent` event is `INPUT_REQUIRED`, the flow need more information before it can continue. 

The following is an example `FlowCompletionEvent` JSON object.

```
{
    "completionReason": "INPUT_REQUIRED"
}
```

### Step 3: Send the user response to the flow
<a name="flows-multi-turn-invocation-continue"></a>

Send the user response back to the flow by calling the `InvokeFlow` operation again. Be sure to include the `executionId`for the conversation.

The following is example JSON for the request to `InvokeFlow`. The `document` field contains the response from the user.

```
{
  "flowIdentifier": "AUS7BMHXBE",
  "flowAliasIdentifier": "4KUDB8VBEF",
  "executionId": "b6450554-f8cc-4934-bf46-f66ed89b60a0",
  "inputs": [
    {
      "content": {
        "document": "1. 5 songs 2. Welsh rock music 3. Castles"
      },
      "nodeName": "AgentsNode_1",
      "nodeInputName": "agentInputText"
    }
  ]
}
```

If the flow needs more information, the flow creates further `FlowMultiTurnInputRequestEvent` events.

### Step 4: End the flow
<a name="flows-multi-turn-invocation-end"></a>

When no more information is needed, the flow emits a `FlowOutputEvent` event which contains the final response.

The following is an example `FlowOutputEvent` JSON object.

```
{
    "nodeName": "FlowOutputNode",
    "content": {
        "document": "Great news! I've created a 5-song Welsh rock playlist centered around the theme of castles. 
        Here's the playlist I've put together for you: Playlist Name: Welsh Rock Castle Anthems 
        Description: A 5-song Welsh rock playlist featuring songs about castles 
        Songs: 
        1. Castell y Bere - Super Furry Animals 
        2. The Castle - Manic Street Preachers 
        3. Caerdydd (Cardiff Castle) - Stereophonics 
        4. Castell Coch - Catatonia 
        5. Chepstow Castle - Feeder 
        This playlist combines Welsh rock bands with songs that reference castles or specific Welsh castles. 
        Enjoy your castle-themed Welsh rock music experience!"
     }
}
```

The flow also emits a `FlowCompletionEvent` event. The value of `completionReason` is `SUCCESS`. 

The following is an example `FlowCompletionEvent` JSON object.

```
{
    "completionReason": "SUCCESS"
}
```

The following sequence diagram shows the steps in a multi-turn flow.

![Flow steps for a multi-turn conversation.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/flows/flows-multi-turn-steps.png)


## Creating and running an example flow
<a name="flows-multi-turn-invocation-example-flow"></a>

In this example, you create a flow that uses an agent to create playlists for a radio station. The agent asks clarifying questions to determine the number of songs, the genre of music, and the theme for the playlist.

**To create the flow**

1. Create an agent in the Amazon Bedrock console by following the instructions at [Create and configure agent manually](agents-create.md). 
   + For step *2.d*, enter **You are a playlist creator for a radio station. When asked to create a playlist, ask for the number of songs, the genre of music, and a theme for the playlist.**.
   + For step *2.e*, in **User input**, choose **Enabled**. Doing this lets the agent request more information, as needed.

1. Create the flow by following the instructions at [Create and design a flow in Amazon Bedrock](flows-create.md). Make sure the flow has an input node, an agents node, and an output node. 

1. Link the agent node to the agent that you created in step 1. The flow should look like the following image.  
![Flow multi-turn conversation.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/flows/flows-multi-turn.png)

1. Run the flow in the Amazon Bedrock console. For testing you can trace the steps that the flow makes. For more information, see [Test a flow in Amazon Bedrock](flows-test.md).

The following Python code example shows how use the flow. 

To run the code, specify the following:
+ `region_name` – The AWS Region in which you are running the flow.
+ `FLOW_ID` – The ID of the flow.
+ `FLOW_ALIAS_ID` – The alias ID of the flow.

For information about getting the IDs, see [View information about flows in Amazon Bedrock](flows-view.md). The code prompts for an initial request to send to the flow and requests more input as needed by the flow. The code doesn't manage other requests from the agent, such as requests to call AWS Lambda functions. For more information, see [How Amazon Bedrock Agents works](agents-how.md). While running, the code generates `FlowTraceEvent` objects that you can use to track the path from the input to the response that flow returns. For more information, see [Track each step in your flow by viewing its trace in Amazon BedrockTrack each step in your flow by viewing its trace](flows-trace.md).

```
"""
Runs an Amazon Bedrock flow and handles muli-turn interaction for a single conversation.

"""
import logging
import boto3
import botocore



import botocore.exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def invoke_flow(client, flow_id, flow_alias_id, input_data, execution_id):
    """
    Invoke an Amazon Bedrock flow and handle the response stream.

    Args:
        client: Boto3 client for Amazon Bedrock agent runtime
        flow_id: The ID of the flow to invoke
        flow_alias_id: The alias ID of the flow
        input_data: Input data for the flow
        execution_id: Execution ID for continuing a flow. Use the value None on first run.

    Returns:
        Dict containing flow_complete status, input_required info, and execution_id
    """

    response = None
    request_params = None

    if execution_id is None:
        # Don't pass execution ID for first run.
        request_params = {
            "flowIdentifier": flow_id,
            "flowAliasIdentifier": flow_alias_id,
            "inputs": [input_data],
            "enableTrace": True
        }
    else:
        request_params = {
            "flowIdentifier": flow_id,
            "flowAliasIdentifier": flow_alias_id,
            "executionId": execution_id,
            "inputs": [input_data],
            "enableTrace": True
        }

    response = client.invoke_flow(**request_params)
    if "executionId" not in request_params:
        execution_id = response['executionId']

    input_required = None
    flow_status = ""

    # Process the streaming response
    for event in response['responseStream']:
        # Check if flow is complete.
        if 'flowCompletionEvent' in event:
            flow_status = event['flowCompletionEvent']['completionReason']

        # Check if more input us needed from user.
        elif 'flowMultiTurnInputRequestEvent' in event:
            input_required = event

        # Print the model output.
        elif 'flowOutputEvent' in event:
            print(event['flowOutputEvent']['content']['document'])

        elif 'flowTraceEvent' in event:
            logger.info("Flow trace:  %s", event['flowTraceEvent'])

    return {
        "flow_status": flow_status,
        "input_required": input_required,
        "execution_id": execution_id
    }


if __name__ == "__main__":

    session = boto3.Session(profile_name='default', region_name='YOUR_FLOW_REGION')
    bedrock_agent_client = session.client('bedrock-agent-runtime')
    
    # Replace these with your actual flow ID and alias ID
    FLOW_ID = 'YOUR_FLOW_ID'
    FLOW_ALIAS_ID = 'YOUR_FLOW_ALIAS_ID'


    flow_execution_id = None
    finished = False

    # Get the intial prompt from the user.
    user_input = input("Enter input: ")

    flow_input_data = {
        "content": {
            "document": user_input
        },
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document"
    }

    logger.info("Starting flow %s", FLOW_ID)

    try:
        while not finished:
            # Invoke the flow until successfully finished.

            result = invoke_flow(
                bedrock_agent_client, FLOW_ID, FLOW_ALIAS_ID, flow_input_data, flow_execution_id)
            status = result['flow_status']
            flow_execution_id = result['execution_id']
            more_input = result['input_required']
            if status == "INPUT_REQUIRED":
                # The flow needs more information from the user.
                logger.info("The flow %s requires more input", FLOW_ID)
                user_input = input(
                    more_input['flowMultiTurnInputRequestEvent']['content']['document'] + ": ")
                flow_input_data = {
                    "content": {
                        "document": user_input
                    },
                    "nodeName": more_input['flowMultiTurnInputRequestEvent']['nodeName'],
                    "nodeInputName": "agentInputText"

                }
            elif status == "SUCCESS":
                # The flow completed successfully.
                finished = True
                logger.info("The flow %s successfully completed.", FLOW_ID)

    except botocore.exceptions.ClientError as e:
        print(f"Client error: {str(e)}")
        logger.error("Client error: %s", {str(e)})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.error("An error occurred: %s", {str(e)})
        logger.error("Error type: %s", {type(e)})
```