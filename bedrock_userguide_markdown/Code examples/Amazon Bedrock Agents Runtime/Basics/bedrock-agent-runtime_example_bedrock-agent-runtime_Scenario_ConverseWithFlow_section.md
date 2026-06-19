

# Converse with an Amazon Bedrock flow
<a name="bedrock-agent-runtime_example_bedrock-agent-runtime_Scenario_ConverseWithFlow_section"></a>

The following code example shows how to use InvokeFlow to converse with an Amazon Bedrock flow that includes an agent node.

For more information, see [Converse with an Amazon Bedrock flow](https://docs.aws.amazon.com/bedrock/latest/userguide/flows-multi-turn-invocation.html).

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent-runtime#code-examples). 

```
"""
Shows how to run an Amazon Bedrock flow with InvokeFlow and handle muli-turn interaction
for a single conversation.
For more information, see https://docs.aws.amazon.com/bedrock/latest/userguide/flows-multi-turn-invocation.html.

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
        client: Boto3 client for Amazon Bedrock agent runtime.
        flow_id: The ID of the flow to invoke.
        flow_alias_id: The alias ID of the flow.
        input_data: Input data for the flow.
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

        # Log trace events.
        elif 'flowTraceEvent' in event:
            logger.info("Flow trace:  %s", event['flowTraceEvent'])

    return {
        "flow_status": flow_status,
        "input_required": input_required,
        "execution_id": execution_id
    }


def converse_with_flow(bedrock_agent_client, flow_id, flow_alias_id):
    """
    Run a conversation with the supplied flow.

    Args:
        bedrock_agent_client: Boto3 client for Amazon Bedrock agent runtime.
        flow_id: The ID of the flow to run.
        flow_alias_id: The alias ID of the flow.

    """

    flow_execution_id = None
    finished = False

    # Get the intial prompt from the user.
    user_input = input("Enter input: ")

    # Use prompt to create input data.
    flow_input_data = {
        "content": {
            "document": user_input
        },
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document"
    }

    try:
        while not finished:
            # Invoke the flow until successfully finished.

            result = invoke_flow(
                bedrock_agent_client, flow_id, flow_alias_id, flow_input_data, flow_execution_id)

            status = result['flow_status']
            flow_execution_id = result['execution_id']
            more_input = result['input_required']
            if status == "INPUT_REQUIRED":
                # The flow needs more information from the user.
                logger.info("The flow %s requires more input", flow_id)
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
                logger.info("The flow %s successfully completed.", flow_id)

    except botocore.exceptions.ClientError as e:
        print(f"Client error: {str(e)}")
        logger.error("Client error: %s", {str(e)})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.error("An error occurred: %s", {str(e)})
        logger.error("Error type: %s", {type(e)})


def main():
    """
    Main entry point for the script.
    """

    # Replace these with your actual flow ID and flow alias ID.
    FLOW_ID = 'YOUR_FLOW_ID'
    FLOW_ALIAS_ID = 'YOUR_FLOW_ALIAS_ID'

    logger.info("Starting conversation with FLOW: %s ID: %s",
                FLOW_ID, FLOW_ALIAS_ID)

    # Get the Bedrock agent runtime client.
    session = boto3.Session(profile_name='default')
    bedrock_agent_client = session.client('bedrock-agent-runtime')

    # Start the conversation.
    converse_with_flow(bedrock_agent_client, FLOW_ID, FLOW_ALIAS_ID)

    logger.info("Conversation with FLOW: %s ID: %s finished",
                FLOW_ID, FLOW_ALIAS_ID)


if __name__ == "__main__":
    main()
```
+  For API details, see [InvokeFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-runtime-2023-12-12/InvokeFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.