

# DeepSeek models
<a name="model-parameters-deepseek"></a>

DeepSeek’s R1 and V3.1 models are text-to-text models available for use for inferencing through the Invoke API ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)) and the Converse API ([Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) and [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)). 

When you make inference calls with DeepSeek’s models, you must include a prompt for the model. For general information about creating prompts for the DeepSeek models that Amazon Bedrock supports, see [DeepSeek prompt guide](https://api-docs.deepseek.com/guides/reasoning_model). 

**Note**  
You can't remove request access from the Amazon Titan, Amazon Nova, DeepSeek-R1, Mistral AI, Meta Llama 3 Instruct, and Meta Llama 4 models. You can prevent users from making inference calls to these models by using an IAM policy and specifying the model ID. For more information, see [Deny access for inference of foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference                         .html).
For optimal response quality with DeepSeek-R1, limit the `max_tokens` parameter to 8,192 tokens or fewer. While the API accepts up to 32,768 tokens, response quality significantly degrades above 8,192 tokens. This aligns with the model's reasoning capabilities as described in the [inference reasoning guide](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-reasoning.html).

This section describes the request parameters and response fields for DeepSeek models. Use this information to make inference calls to DeepSeek models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) operation. This section also includes Python code examples that shows how to call DeepSeek models.

To use a model in an inference operation, you need the model ID for the model. Since this model is invoked through cross-Region inference, you will need to use the [Inference profile ID](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) as the model ID. For example, for the US, you will use `us.deepseek.r1-v1:0`.
+ Model Name: DeepSeek-R1
+ Text Model

For more information on how to use DeepSeek models with APIs, see [DeepSeek Models](https://deepseek.com/).

**DeepSeek Request and Response**

**Request body**

DeepSeek has the following inference parameters for a Text Completion inference call.

```
{
    "prompt": string,
    "temperature": float, 
    "top_p": float,
    "max_tokens": int,
    "stop": string array
}
```

**Fields:**
+ **prompt** – (string) Required text input of prompt.
+ **temperature** – (float) Numerical value less than or equal to 1.
+ **top\_p** – (float) Numerical value less than or equal to 1.
+ **max\_tokens** – (int) Tokens used, minimum of 1 to a max of 8,192 tokens for optimal quality. While the API accepts up to 32,768 tokens, response quality significantly degrades above 8,192 tokens.
+ **stop** – (string array) Maximum of 10 items.

**Response body**

DeepSeek has the following response parameters for a Text Completion inference call. This example is a text completion from DeepSeek, and does not return a content reasoning block.

```
{
    "choices": [
        {
            "text": string,
            "stop_reason": string
        }
    ]
}
```

**Fields:**
+ **stop\_reason** – (string) The reason why the response stopped generating text. Value of `stop` or `length`.
+ **stop** – (string) The model has finished generating text for the input prompt.
+ **length** – (string) The length of the tokens for the generated text exceeds the value of `max_tokens` in the call to `InvokeModel` ( or `InvokeModelWithResponseStream`, if you are streaming output). The response is truncated to `max_tokens`. Increase the value of `max_tokens` and try your request again.

**Example Code**

This example shows how to call the DeepSeek-R1 model.

```
# Use the API to send a text message to DeepSeek-R1.

import boto3
import json

from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the cross Region inference profile ID for DeepSeek-R1
model_id = "us.deepseek.r1-v1:0"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Embed the prompt in DeepSeek-R1's instruction format.
formatted_prompt = f"""
<｜begin▁of▁sentence｜><｜User｜>{prompt}<｜Assistant｜><think>\n
"""

body = json.dumps({
    "prompt": formatted_prompt,
    "max_tokens": 512,
    "temperature": 0.5,
    "top_p": 0.9,
})

try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=body)

    # Read the response body.
    model_response = json.loads(response["body"].read())
    
    # Extract choices.
    choices = model_response["choices"]
    
    # Print choices.
    for index, choice in enumerate(choices):
        print(f"Choice {index + 1}\n----------")
        print(f"Text:\n{choice['text']}\n")
        print(f"Stop reason: {choice['stop_reason']}\n")
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
```

**Converse**

Request Body - Use this request body example to call the ConverseAPI.

```
{
    "modelId": string, # us.deepseek.r1-v1:0
    "system": [
        {
            "text": string
        }
    ],
    "messages": [
        {
            "role": string,
            "content": [
                {
                    "text": string
                }
            ]
        }
    ],
    "inferenceConfig": {
        "temperature": float,
        "topP": float,
        "maxTokens": int,
        "stopSequences": string array
    },
    "guardrailConfig": { 
        "guardrailIdentifier":"string",
        "guardrailVersion": "string",
        "trace": "string"
    }
}
```

**Fields:**
+ **system** – (Optional) The system prompt for the request.
+ **messages** – (Required) The input messages.
  + **role** – The role of the conversation turn. Valid values are `user` and `assistant`.
  + **content** – (Required) The content of the conversation turn, as an array of objects. Each object contains a typefield, in which you can specify one of the following values:
    + **text** – (Required) If you specify this type, you must include a text field and specify the text prompt as its value.
+ **inferenceConfig** 
  + **temperature** – (Optional) Values: minimum = 0. maximum = 1.
  + **topP** – (Optional) Values: minimum = 0. maximum = 1.
  + **maxTokens** – (Optional) The maximum number of tokens to generate before stopping. Values: minimum = 0. maximum = 32,768.
  + **stopSequences ** – (Optional) Custom text sequences that causes the model to stop generating output. Maximum = 10 items.

Response Body - Use this request body example to call the ConverseAPI.

```
{
    "message": {
        "role" : "assistant",
        "content": [
            {
                "text": string
            },
            {
                "reasoningContent": {
                    "reasoningText": string
                }
            }
        ],
    },
    "stopReason": string,
    "usage": {
        "inputTokens": int,
        "outputTokens": int,
        "totalTokens": int
    }
    "metrics": {
        "latencyMs": int
    }
}
```

**Fields:**
+ **message** – The return response from the model.
+ **role** – The conversational role of the generated message. The value is always `assistant`.
+ **content** – The content generated by the model, which is returned as an array. There are two types of content:
  + **text** – The text content of the response.
  + **reasoningContent** – (Optional) The reasoning content from the model response.
    + **reasoningText** – The reasoning text from the model response.
+ **stopReason** – The reason why the model stopped generating the response. 
  + **end\_turn** – The turn the model reached a stopping point.
  + **max\_tokens** – The generated text exceeded the value of the `maxTokens` input field or exceeded the maximum number of tokens that the model supports.

Example Code - Here is an example of DeepSeek making a to call the ConverseAPI.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the Converse API with DeepSeek-R1 (on demand).
"""

import logging
import boto3

from botocore.client import Config
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_conversation(bedrock_client,
                          model_id,
                          system_prompts,
                          messages):
    """
    Sends messages to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_prompts (JSON) : The system prompts for the model to use.
        messages (JSON) : The messages to send to the model.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Inference parameters to use.
    temperature = 0.5
    max_tokens = 4096

    # Base inference parameters to use.
    inference_config = {
        "temperature": temperature,
        "maxTokens": max_tokens,
    }

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
    )

    # Log token usage.
    token_usage = response['usage']
    logger.info("Input tokens: %s", token_usage['inputTokens'])
    logger.info("Output tokens: %s", token_usage['outputTokens'])
    logger.info("Total tokens: %s", token_usage['totalTokens'])
    logger.info("Stop reason: %s", response['stopReason'])

    return response

def main():
    """
    Entrypoint for DeepSeek-R1 example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "us.deepseek.r1-v1:0"

    # Setup the system prompts and messages to send to the model.
    system_prompts = [{"text": "You are an app that creates playlists for a radio station that plays rock and pop music. Only return song names and the artist."}]
    message_1 = {
        "role": "user",
        "content": [{"text": "Create a list of 3 pop songs."}]
    }
    message_2 = {
        "role": "user",
        "content": [{"text": "Make sure the songs are by artists from the United Kingdom."}]
    }
    messages = []

    try:
        # Configure timeout for long responses if needed
        custom_config = Config(connect_timeout=840, read_timeout=840)
        bedrock_client = boto3.client(service_name='bedrock-runtime', config=custom_config)

        # Start the conversation with the 1st message.
        messages.append(message_1)
        response = generate_conversation(
            bedrock_client, model_id, system_prompts, messages)

        # Add the response message to the conversation.
        output_message = response['output']['message']
        
        # Remove reasoning content from the response
        output_contents = []
        for content in output_message["content"]:
            if content.get("reasoningContent"):
                continue
            else:
                output_contents.append(content)
        output_message["content"] = output_contents
        
        messages.append(output_message)

        # Continue the conversation with the 2nd message.
        messages.append(message_2)
        response = generate_conversation(
            bedrock_client, model_id, system_prompts, messages)

        output_message = response['output']['message']
        messages.append(output_message)

        # Show the complete conversation.
        for message in messages:
            print(f"Role: {message['role']}")
            for content in message['content']:
                if content.get("text"):
                    print(f"Text: {content['text']}")
                if content.get("reasoningContent"):
                    reasoning_content = content['reasoningContent']
                    reasoning_text = reasoning_content.get('reasoningText', {})
                    print()
                    print(f"Reasoning Text: {reasoning_text.get('text')}")
            print()

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    else:
        print(
            f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()
```