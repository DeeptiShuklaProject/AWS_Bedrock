

# Cohere Command R and Command R\+ models
<a name="model-parameters-cohere-command-r-plus"></a>

You make inference requests to Cohere Command R and Cohere Command R\+ models with [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming). You need the model ID for the model that you want to use. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). 

**Tip**  
For conversational applications, we recommend that you use the Converse API. The Converse API provides a unified set of parameters that work across all models that support messages. For more information, see [Inference using Converse API](conversation-inference.md).

**Topics**
+ [Request and Response](#model-parameters-cohere-command-request-response)
+ [Code example](#api-inference-examples-cohere-command-r)

## Request and Response
<a name="model-parameters-cohere-command-request-response"></a>

------
#### [ Request ]

The Cohere Command models have the following inference parameters. 

```
{
    "message": string,
    "chat_history": [
        {
            "role":"{{USER or CHATBOT}}",
            "message": string
        }
  
    ],
    "documents": [
        {"title": string, "snippet": string},
    ],
    "search_queries_only" : boolean,
    "preamble" : string,
    "max_tokens": int,
    "temperature": float,
    "p": float,
    "k": float,
    "prompt_truncation" : string,
    "frequency_penalty" : float,
    "presence_penalty" : float,
    "seed" : int,
    "return_prompt" : boolean,
    "tools" : [
        {
            "name": string,
            "description": string,
            "parameter_definitions": {
                "{{parameter name}}": {
                    "description": string,
                    "type": string,
                    "required": boolean
                }
            }
        }
    ],
    "tool_results" : [
        {
            "call": {
                "name": string,
                "parameters": {
                "{{parameter name}}": string
                }
            },
        "outputs": [
                {
                "{{text}}": string
                }
            ]
        }
    ],
    "stop_sequences": [string],
    "raw_prompting" : boolean

}
```

The following are required parameters.
+ **message** – (Required) Text input for the model to respond to.

The following are optional parameters.
+ **chat\_history** – A list of previous messages between the user and the model, meant to give the model conversational context for responding to the user's message. 

  The following are required fields.
  + `role` – The role for the message. Valid values are `USER` or `CHATBOT`. tokens.
  + `message` – Text contents of the message.

  The following is example JSON for the `chat_history` field

  ```
  "chat_history": [
  {"role": "USER", "message": "Who discovered gravity?"},
  {"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
  ]
  ```
+ **documents** – A list of texts that the model can cite to generate a more accurate reply. Each document is a string-string dictionary. The resulting generation includes citations that reference some of these documents. We recommend that you keep the total word count of the strings in the dictionary to under 300 words. An `_excludes` field (array of strings) can be optionally supplied to omit some key-value pairs from being shown to the model. For more information, see the [Document Mode guide](https://docs.cohere.com/docs/retrieval-augmented-generation-rag#document-mode) in the Cohere documentation. 

  The following is example JSON for the `documents` field.

  ```
  "documents": [
  {"title": "Tall penguins", "snippet": "Emperor penguins are the tallest."},
  {"title": "Penguin habitats", "snippet": "Emperor penguins only live in Antarctica."}
  ]
  ```
+ **search\_queries\_only** – Defaults to `false`. When `true`, the response will only contain a list of generated search queries, but no search will take place, and no reply from the model to the user's `message` will be generated. 
+ **preamble** – Overrides the default preamble for search query generation. Has no effect on tool use generations. 
+ **max\_tokens** – The maximum number of tokens the model should generate as part of the response. Note that setting a low value may result in incomplete generations. Setting `max_tokens` may result in incomplete or no generations when used with the `tools` or `documents` fields.
+ **temperature** – Use a lower value to decrease randomness in the response. Randomness can be further maximized by increasing the value of the `p` parameter.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command-r-plus.html)
+ **p** – Top P. Use a lower value to ignore less probable options.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command-r-plus.html)
+ **k** – Top K. Specify the number of token choices the model uses to generate the next token.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command-r-plus.html)
+  **prompt\_truncation** – Defaults to `OFF`. Dictates how the prompt is constructed. With `prompt_truncation` set to `AUTO_PRESERVE_ORDER`, some elements from `chat_history` and `documents` will be dropped to construct a prompt that fits within the model's context length limit. During this process the order of the documents and chat history will be preserved. With `prompt_truncation`` set to `OFF`, no elements will be dropped. 
+  **frequency\_penalty** – Used to reduce repetitiveness of generated tokens. The higher the value, the stronger a penalty is applied to previously present tokens, proportional to how many times they have already appeared in the prompt or prior generation.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command-r-plus.html)
+  **presence\_penalty** – Used to reduce repetitiveness of generated tokens. Similar to `frequency_penalty`, except that this penalty is applied equally to all tokens that have already appeared, regardless of their exact frequencies.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command-r-plus.html)
+ **seed** – If specified, the backend will make a best effort to sample tokens deterministically, such that repeated requests with the same seed and parameters should return the same result. However, determinism cannot be totally guaranteed.
+ **return\_prompt** – Specify `true` to return the full prompt that was sent to the model. The default value is `false`. In the response, the prompt in the `prompt` field.
+ **tools** – A list of available tools (functions) that the model may suggest invoking before producing a text response. When `tools` is passed (without `tool_results`), the `text` field in the response will be `""` and the `tool_calls` field in the response will be populated with a list of tool calls that need to be made. If no calls need to be made, the `tool_calls` array will be empty. 

  For more information, see [Tool Use](https://docs.cohere.com/docs/tool-use) in the Cohere documentation.
**Tip**  
We recommend that you use the Converse API for integrating tool use into your application. For more information, see [Use a tool to complete an Amazon Bedrock model response](tool-use.md). 

  The following is example JSON for the `tools` field.

  ```
  [
      {
          "name": "top_song",
          "description": "Get the most popular song played on a radio station.",
          "parameter_definitions": {
              "sign": {
                  "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ and WKRP.",
                  "type": "str",
                  "required": true
              }
          }
      }
  ]
  ```

  For more information, see [Single-Step Tool Use (Function Calling)](https://docs.cohere.com/docs/tool-use) in the Cohere documentation.
+ **tools\_results** – A list of results from invoking tools recommended by the model in the previous chat turn. Results are used to produce a text response and are referenced in citations. When using `tool_results`, `tools` must be passed as well. Each `tool_result` contains information about how it was invoked, as well as a list of outputs in the form of dictionaries. Cohere’s unique fine-grained citation logic requires the output to be a list. In case the output is just one item, such as `{"status": 200}`, you should still wrap it inside a list. 

  For more information, see [Tool Use](https://docs.cohere.com/docs/tool-use) in the Cohere documentation.

  The following is example JSON for the `tools_results` field.

  ```
  [
      {
          "call": {
              "name": "top_song",
              "parameters": {
                  "sign": "WZPZ"
              }
          },
          "outputs": [
              {
                  "song": "Elemental Hotel"
              }
          ]
      }
  ]
  ```
+  **stop\_sequences** – A list of stop sequences. After a stop sequence is detected, the model stops generating further tokens.
+  **raw\_prompting** – Specify `true`, to send the user’s `message` to the model without any preprocessing, otherwise false.

------
#### [ Response ]

The response has the following possible fields:

```
{
    "response_id": string,
    "text": string,
    "generation_id": string,
    "citations": [
        {
          "start": int,
          "end": int,
          "text": "string",
          "document_ids": [
              "string"
          ]
        }
      ],    
    "finish_reason": string,
    "tool_calls": [
        {
            "name": string,
            "parameters": {
                "{{parameter name}}": string
            }
        }
    ],
    {
    "meta": {
        "api_version": {
            "version": string
        },
        "billed_units": {
            "input_tokens": int,
            "output_tokens": int
        }
    }
}
```
+ **response\_id** — Unique identifier for chat completion
+ **text** — The model’s response to chat message input. 
+ **generation\_id** — Unique identifier for chat completion, used with Feedback endpoint on Cohere’s platform. 
+ **citations** — An array of inline citations and associated metadata for the generated reply. Contains the following fields:
  + **start** — The index that the citation begins at, starting from 0.
  + **end** — The index that the citation ends after, starting from 0.
  + **text** — The text that the citation pertains to.
  + **document\_ids** — An array of document IDs that correspond to documents that are cited for the text.
+ **prompt** — The full prompt that was sent to the model. Specify the `return_prompt` field to return this field. 
+ **finish\_reason** — The reason why the model stopped generating output. Can be any of the following: 
  + **complete** — The completion reached the end of generation token, ensure this is the finish reason for best performance.
  + **error\_toxic** — The generation could not be completed due to our content filters.
  + **error\_limit** — The generation could not be completed because the model’s context limit was reached.
  + **error** — The generation could not be completed due to an error.
  + **user\_cancel** — The generation could not be completed because it was stopped by the user.
  + **max\_tokens** — The generation could not be completed because the user specified a `max_tokens` limit in the request and this limit was reached. May not result in best performance.
+ **tool\_calls** – A list of appropriate tools to calls. Only returned if you specify the `tools` input field.

  For more information, see [Tool Use](https://docs.cohere.com/docs/tool-use) in the Cohere documentation.
**Tip**  
We recommend that you use the Converse API for integrating tool use into your application. For more information, see [Use a tool to complete an Amazon Bedrock model response](tool-use.md). 

  The following is example JSON for the `tool_calls` field.

  ```
  [
          {
              "name": "top_song",
              "parameters": {
                  "sign": "WZPZ"
              }
          }
      ]
  ```
+ **meta** — API usage data (only exists for streaming). 
  + `api_version` — The API version. The version is in the `version` field.
  + `billed_units` — The billed units. Possible values are:
    + `input_tokens` — The number of input tokens that were billed.
    + `output_tokens` — The number of output tokens that were billed.

------

## Code example
<a name="api-inference-examples-cohere-command-r"></a>

This examples shows how to call the *Cohere Command R* model.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the  Cohere Command R model.
"""
import json
import logging
import boto3


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using a Cohere Command R model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The reqest body to use.
    Returns:
        dict: The response from the model.
    """

    logger.info("Generating text with Cohere model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id
    )

    logger.info(
        "Successfully generated text with Cohere Command R model %s", model_id)

    return response


def main():
    """
    Entrypoint for Cohere example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = 'cohere.command-r-v1:0'
    chat_history = [
        {"role": "USER", "message": "What is an interesting new role in AI if I don't have an ML background?"},
        {"role": "CHATBOT", "message": "You could explore being a prompt engineer!"}
    ]
    message = "What are some skills I should have?"

    try:
        body = json.dumps({
            "message": message,
            "chat_history": chat_history,
            "max_tokens": 2000,
            "temperature": 0.6,
            "p": 0.5,
            "k": 250
        })
        response = generate_text(model_id=model_id,
                                 body=body)

        response_body = json.loads(response.get('body').read())
        response_chat_history = response_body.get('chat_history')
        print('Chat history\n------------')
        for response_message in response_chat_history:
            if 'message' in response_message:
                print(f"Role: {response_message['role']}")
                print(f"Message: {response_message['message']}\n")
        print("Generated text\n--------------")
        print(f"Stop reason: {response_body['finish_reason']}")
        print(f"Response text: \n{response_body['text']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    else:
        print(f"Finished generating text with Cohere model {model_id}.")


if __name__ == "__main__":
    main()
```