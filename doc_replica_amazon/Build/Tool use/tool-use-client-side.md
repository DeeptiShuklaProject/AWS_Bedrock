

# Client-side tool use
<a name="tool-use-client-side"></a>

If you use the Responses API, Chat Completions API, Converse API, or InvokeModel API to send the request, then the model uses client-side tool calling. This means that in your code, you call the tool on the model's behalf. In this scenario, assume the tool implementation is an API. The tool could just as easily be a database, Lambda function, or some other software. You decide how you want to implement the tool. You then continue the conversation with the model by supplying a message with the result from the tool. Finally, the model generates a response for the original message that includes the tool results that you sent to the model.

Let us define the tool we will use for tool use. The following Python examples show how to use a tool that returns the most popular song on a fictional radio station.

```
def get_most_popular_song(station_name: str) -> str:
    stations = {
        "Radio Free Mars": "Starman – David Bowie",
        "Neo Tokyo FM": "Plastic Love – Mariya Takeuchi",
        "Cloud Nine Radio": "Blinding Lights – The Weeknd",
    }
    return stations.get(station_name, "Unknown Station – No chart data available")
```

**Using Responses API for client-side tooling**

You can use the [Function calling](https://platform.openai.com/docs/guides/function-calling) feature provided by OpenAI to call this tool. Responses API is OpenAI's preferred API. Here is the Python code for Responses API for client-side tooling:

```
from openai import OpenAI
import json

client = OpenAI()

response = client.responses.create(
    model="oss-gpt-120b",
    input="What is the most popular song on Radio Free Mars?",
    tools=[
        {
            "type": "function",
            "name": "get_most_popular_song",
            "description": "Returns the most popular song on a radio station",
            "parameters": {
                "type": "object",
                "properties": {
                    "station_name": {
                        "type": "string",
                        "description": "Name of the radio station"
                    }
                },
                "required": ["station_name"]
            }
        }
    ]
)

if response.output and response.output[0].content:
    tool_call = response.output[0].content[0]
    args = json.loads(tool_call["arguments"])
    result = get_most_popular_song(args["station_name"])
    
    final_response = client.responses.create(
        model="oss-gpt-120b",
        input=[
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result
            }
        ]
    )
    
    print(final_response.output_text)
```

**Using Chat Completions API for client-side tooling**

You can use the Chat Completions API also. Here is the Python code for using Chat Completions:

```
    from openai import OpenAI
import json

client = OpenAI()

completion = client.chat.completions.create(
    model="oss-gpt-120b",
    messages=[{"role": "user", "content": "What is the most popular song on Neo Tokyo FM?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_most_popular_song",
            "description": "Returns the most popular song on a radio station",
            "parameters": {
                "type": "object",
                "properties": {
                   "station_name": {"type": "string", "description": "Name of the radio station"}
                },
                "required": ["station_name"]
            }
        }
    }]
)

message = completion.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_most_popular_song(args["station_name"])

    followup = client.chat.completions.create(
        model="oss-gpt-120b",
        messages=[
            {"role": "user", "content": "What is the most popular song on Neo Tokyo FM?"},
            message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": result}
        ]
    )

    print(followup.choices[0].message.content)
```

For more details on the using Function Calling on Responses API and Chat Completions API, see [Function Calling](https://platform.openai.com/docs/guides/function-calling) in OpenAI.

**Using Converse API for client-side tooling**

You can use the [Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) to let a model use a tool in a conversation. The following Python examples show how to use a tool that returns the most popular song on a fictional radio station.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Shows how to use tools with the Converse API and the Cohere Command R model."""

import logging
import json
import boto3
from botocore.exceptions import ClientError


class StationNotFoundError(Exception):
    """Raised when a radio station isn't found."""
    pass


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_top_song(call_sign):
    """Returns the most popular song for the requested station.

    Args:
        call_sign (str): The call sign for the station for which you want
            the most popular song.

    Returns:
        response (json): The most popular song and artist.
    """
    song = ""
    artist = ""

    if call_sign == 'WZPZ':
        song = "Elemental Hotel"
        artist = "8 Storey Hike"
    else:
        raise StationNotFoundError(f"Station {call_sign} not found.")

    return song, artist


def generate_text(bedrock_client, model_id, tool_config, input_text):
    """Generates text using the supplied Amazon Bedrock model. If necessary,
    the function handles tool use requests and sends the result to the model.

    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The Amazon Bedrock model ID.
        tool_config (dict): The tool configuration.
        input_text (str): The input text.

    Returns:
        Nothing.
    """
    logger.info("Generating text with model %s", model_id)

    # Create the initial message from the user input.
    messages = [{"role": "user",
                 "content": [{"text": input_text}]}]

    response = bedrock_client.converse(modelId=model_id,
                                       messages=messages,
                                       toolConfig=tool_config)

    output_message = response['output']['message']
    messages.append(output_message)

    stop_reason = response['stopReason']

    if stop_reason == 'tool_use':
        # Tool use requested. Call the tool and send the result to the model.
        tool_requests = response['output']['message']['content']

        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool = tool_request['toolUse']
                logger.info("Requesting tool %s. Request: %s",
                            tool['name'], tool['toolUseId'])

                if tool['name'] == 'top_song':
                    tool_result = {}
                    try:
                        song, artist = get_top_song(tool['input']['sign'])
                        tool_result = {"toolUseId": tool['toolUseId'],
                                       "content": [{"json": {"song": song, "artist": artist}}]}
                    except StationNotFoundError as err:
                        tool_result = {"toolUseId": tool['toolUseId'],
                                       "content": [{"text": err.args[0]}],
                                       "status": 'error'}

                    tool_result_message = {"role": "user",
                                           "content": [{"toolResult": tool_result}]}
                    messages.append(tool_result_message)

        # Send the tool result to the model.
        response = bedrock_client.converse(modelId=model_id,
                                           messages=messages,
                                           toolConfig=tool_config)

        output_message = response['output']['message']

    # print the final response from the model.
    for content in output_message['content']:
        print(json.dumps(content, indent=4))


def main():
    """Entrypoint for tool use example."""
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "cohere.command-r-v1:0"
    input_text = "What is the most popular song on WZPZ?"

    tool_config = {
        "tools": [
            {
                "toolSpec": {
                    "name": "top_song",
                    "description": "Get the most popular song played on a radio station.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "sign": {
                                    "type": "string",
                                    "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ, and WKRP."
                                }
                            },
                            "required": ["sign"]
                        }
                    }
                }
            }
        ]
    }

    bedrock_client = boto3.client(service_name='bedrock-runtime')

    try:
        print(f"Question: {input_text}")
        generate_text(bedrock_client, model_id, tool_config, input_text)
    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")
    else:
        print(f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()
```

**Using Invoke APIs for client-side tool use**

It is possible to use tools with the base inference operations ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)). To find the inference parameters that you pass in the request body, see the [inference parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html) for the model that you want to use.