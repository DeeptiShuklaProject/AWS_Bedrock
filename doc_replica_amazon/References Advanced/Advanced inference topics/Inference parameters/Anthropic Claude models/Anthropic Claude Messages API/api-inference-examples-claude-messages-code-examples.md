

# Code examples
<a name="api-inference-examples-claude-messages-code-examples"></a>

The following code examples show how to use the messages API. 

**Topics**
+ [Messages code example](#api-inference-examples-claude-messages-code-example)
+ [Multimodal code examples](#api-inference-examples-claude-multimodal-code-example)

## Messages code example
<a name="api-inference-examples-claude-messages-code-example"></a>

This example shows how to send a single turn user message and a user turn with a prefilled assistant message to an Anthropic Claude 3 Sonnet model.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate a message with Anthropic Claude (on demand).
"""
import boto3
import json
import logging

from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_message(bedrock_runtime, model_id, system_prompt, messages, max_tokens):

    body=json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": messages
        }  
    )  

    
    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())
   
    return response_body


def main():
    """
    Entrypoint for Anthropic Claude message example.
    """

    try:

        bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        system_prompt = "Please respond only with emoji."
        max_tokens = 1000

        # Prompt with user turn only.
        user_message =  {"role": "user", "content": "Hello World"}
        messages = [user_message]

        response = generate_message (bedrock_runtime, model_id, system_prompt, messages, max_tokens)
        print("User turn only.")
        print(json.dumps(response, indent=4))

        # Prompt with both user turn and prefilled assistant response.
        #Anthropic Claude continues by using the prefilled assistant text.
        assistant_message =  {"role": "assistant", "content": "<emoji>"}
        messages = [user_message, assistant_message]
        response = generate_message(bedrock_runtime, model_id,system_prompt, messages, max_tokens)
        print("User turn and prefilled assistant response.")
        print(json.dumps(response, indent=4))

    except ClientError as err:
        message=err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " +
            format(message))

if __name__ == "__main__":
    main()
```

## Multimodal code examples
<a name="api-inference-examples-claude-multimodal-code-example"></a>

The following examples show how to pass an image and prompt text in a multimodal message to an Anthropic Claude 3 Sonnet model.

**Topics**
+ [Multimodal prompt with InvokeModel](#api-inference-examples-claude-multimodal-code-example-invoke-model)
+ [Streaming multimodal prompt with InvokeModelWithResponseStream](#api-inference-examples-claude-multimodal-code-example-streaming)

### Multimodal prompt with InvokeModel
<a name="api-inference-examples-claude-multimodal-code-example-invoke-model"></a>

The following example shows how to send a multimodal prompt to Anthropic Claude 3 Sonnet with [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html). 

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to run a multimodal prompt with Anthropic Claude (on demand) and InvokeModel.
"""

import json
import logging
import base64
import boto3

from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_multi_modal_prompt(bedrock_runtime, model_id, messages, max_tokens):
    """
    Invokes a model with a multimodal prompt.
    Args:
        bedrock_runtime: The Amazon Bedrock boto3 client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send to the model.
        max_tokens (int) : The maximum  number of tokens to generate.
    Returns:
        None.
    """



    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body


def main():
    """
    Entrypoint for Anthropic Claude multimodal prompt example.
    """

    try:

        bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        max_tokens = 1000
        input_text = "What's in this image?"
        input_image = "/path/to/image" # Replace with actual path to image file
 
        # Read reference image from file and encode as base64 strings.
        image_ext = input_image.split(".")[-1]
        with open(input_image, "rb") as image_file:
            content_image = base64.b64encode(image_file.read()).decode('utf8')

        message = {
            "role": "user",
            "content": [
                {
                    "type": "image", 
                    "source": {
                        "type": "base64",
                        "media_type": f"image/{image_ext}", 
                        "data": content_image
                    }
                },
                {
                    "type": "text", 
                    "text": input_text
                }
            ]
        }

    
        messages = [message]

        response = run_multi_modal_prompt(
            bedrock_runtime, model_id, messages, max_tokens)
        print(json.dumps(response, indent=4))

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " +
              format(message))


if __name__ == "__main__":
    main()
```

### Streaming multimodal prompt with InvokeModelWithResponseStream
<a name="api-inference-examples-claude-multimodal-code-example-streaming"></a>

The following example shows how to stream the response from a multimodal prompt sent to Anthropic Claude 3 Sonnet with [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html). 

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to stream the response from Anthropic Claude Sonnet (on demand) for a 
multimodal request.
"""

import json
import base64
import logging
import boto3

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def stream_multi_modal_prompt(bedrock_runtime, model_id, input_text, image, max_tokens):
    """
    Streams the response from a multimodal prompt.
    Args:
        bedrock_runtime: The Amazon Bedrock boto3 client.
        model_id (str): The model ID to use.
        input_text (str) : The prompt text
        image (str) : The path to  an image that you want in the prompt.
        max_tokens (int) : The maximum  number of tokens to generate.
    Returns:
        None.
    """

    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": input_text},
                    {"type": "image", "source": {"type": "base64",
                                                 "media_type": "image/jpeg", "data": encoded_string.decode('utf-8')}}
                ]
            }
        ]
    })

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body, modelId=model_id)

    for event in response.get("body"):
        chunk = json.loads(event["chunk"]["bytes"])

        if chunk['type'] == 'message_delta':
            print(f"\nStop reason: {chunk['delta']['stop_reason']}")
            print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
            print(f"Output tokens: {chunk['usage']['output_tokens']}")

        if chunk['type'] == 'content_block_delta':
            if chunk['delta']['type'] == 'text_delta':
                print(chunk['delta']['text'], end="")


def main():
    """
    Entrypoint for Anthropic Claude Sonnet multimodal prompt example.
    """

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    input_text = "What can you tell me about this image?"
    image = "/path/to/image"
    max_tokens = 100

    try:

        bedrock_runtime = boto3.client('bedrock-runtime')

        stream_multi_modal_prompt(
            bedrock_runtime, model_id, input_text, image, max_tokens)

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))


if __name__ == "__main__":
    main()
```