

# Cohere Command models
<a name="model-parameters-cohere-command"></a>

You make inference requests to an Cohere Command model with [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming). You need the model ID for the model that you want to use. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). 

**Topics**
+ [Request and Response](#model-parameters-cohere-command-request-response)
+ [Code example](#api-inference-examples-cohere-command)

## Request and Response
<a name="model-parameters-cohere-command-request-response"></a>

------
#### [ Request ]

The Cohere Command models have the following inference parameters. 

```
{
    "prompt": string,
    "temperature": float,
    "p": float,
    "k": float,
    "max_tokens": int,
    "stop_sequences": [string],
    "return_likelihoods": "GENERATION|ALL|NONE",
    "stream": boolean,
    "num_generations": int,
    "logit_bias": {token_id: bias},
    "truncate": "NONE|START|END"
}
```

The following are required parameters.
+ **prompt** – (Required) The input text that serves as the starting point for generating the response.

  The following are text per call and character limits.

**Texts per call**  
    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)

**Characters**  
    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)

The following are optional parameters.
+ **return\_likelihoods** – Specify how and if the token likelihoods are returned with the response. You can specify the following options. 
  + `GENERATION` – Only return likelihoods for generated tokens.
  + `ALL` – Return likelihoods for all tokens.
  + `NONE` – (Default) Don't return any likelihoods.
+ **stream** – ( Required to support streaming) Specify `true` to return the response piece-by-piece in real-time and `false` to return the complete response after the process finishes.
+ **logit\_bias** – Prevents the model from generating unwanted tokens or incentivizes the model to include desired tokens. The format is `{token_id: bias}` where bias is a float between -10 and 10. Tokens can be obtained from text using any tokenization service, such as Cohere’s Tokenize endpoint. For more information, see [Cohere documentation](https://docs.cohere.com/docs).    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+  **num\_generations** – The maximum number of generations that the model should return.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+  **truncate** – Specifies how the API handles inputs longer than the maximum token length. Use one of the following:
  + `NONE` – Returns an error when the input exceeds the maximum input token length. 
  + `START` – Discard the start of the input. 
  + `END` – (Default) Discards the end of the input.

  If you specify `START` or `END`, the model discards the input until the remaining input is exactly the maximum input token length for the model.
+ **temperature** – Use a lower value to decrease randomness in the response.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+ **p** – Top P. Use a lower value to ignore less probable options. Set to 0 or 1.0 to disable. If both `p` and `k` are enabled, `p` acts after `k`.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+ **k** – Top K. Specify the number of token choices the model uses to generate the next token. If both `p` and `k` are enabled, `p` acts after `k`.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+ **max\_tokens** – Specify the maximum number of tokens to use in the generated response.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)
+ **stop\_sequences** – Configure up to four sequences that the model recognizes. After a stop sequence, the model stops generating further tokens. The returned text doesn't contain the stop sequence.

------
#### [ Response ]

The response has the following possible fields:

```
{
    "generations": [
        {
            "finish_reason": "COMPLETE | MAX_TOKENS | ERROR | ERROR_TOXIC",
            "id": string,
            "text": string,
            "likelihood" : float,
            "token_likelihoods" : [{"token" : string, "likelihood": float}],
            "is_finished" : true | false,
            "index" : integer
           
        }
    ],
    "id": string,
    "prompt": string
}
```
+ `generations` — A list of generated results along with the likelihoods for tokens requested. (Always returned). Each generation object in the list contains the following fields.
  + `id` — An identifier for the generation. (Always returned).
  + `likelihood` — The likelihood of the output. The value is the average of the token likelihoods in `token_likelihoods`. Returned if you specify the `return_likelihoods` input parameter.
  + `token_likelihoods` — An array of per token likelihoods. Returned if you specify the `return_likelihoods` input parameter.
  + `finish_reason` — The reason why the model finished generating tokens. `COMPLETE` - the model sent back a finished reply. `MAX_TOKENS` – the reply was cut off because the model reached the maximum number of tokens for its context length. `ERROR ` – something went wrong when generating the reply. `ERROR_TOXIC` – the model generated a reply that was deemed toxic. `finish_reason` is returned only when `is_finished`=`true`. (Not always returned). 
  + `is_finished` — A boolean field used only when `stream` is `true`, signifying whether or not there are additional tokens that will be generated as part of the streaming response. (Not always returned)
  + `text` — The generated text.
  + `index` — In a streaming response, use to determine which generation a given token belongs to. When only one response is streamed, all tokens belong to the same generation and index is not returned. `index` therefore is only returned in a streaming request with a value for `num_generations` that is larger than one.
+ `prompt` — The prompt from the input request (always returned).
+ `id` — An identifier for the request (always returned).

For more information, see [Generate](https://docs.cohere.com/reference/generate-1) in the Cohere documentations.

------

## Code example
<a name="api-inference-examples-cohere-command"></a>

This examples shows how to call the *Cohere Command* model.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate text using a Cohere model.
"""
import json
import logging
import boto3


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using a Cohere model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The reqest body to use.
    Returns:
        dict: The response from the model.
    """

    logger.info("Generating text with Cohere model %s", model_id)

    accept = 'application/json'
    content_type = 'application/json'

    bedrock = boto3.client(service_name='bedrock-runtime')

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    logger.info("Successfully generated text with Cohere model %s", model_id)

    return response


def main():
    """
    Entrypoint for Cohere example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = 'cohere.command-text-v14'
    prompt = """Summarize this dialogue: 
"Customer: Please connect me with a support agent.
AI: Hi there, how can I assist you today?
Customer: I forgot my password and lost access to the email affiliated to my account. Can you please help me?
AI: Yes of course. First I'll need to confirm your identity and then I can connect you with one of our support agents.
"""
    try:
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.6,
            "p": 1,
            "k": 0,
            "num_generations": 2,
            "return_likelihoods": "GENERATION"
        })
        response = generate_text(model_id=model_id,
                                 body=body)

        response_body = json.loads(response.get('body').read())
        generations = response_body.get('generations')

        for index, generation in enumerate(generations):

            print(f"Generation {index + 1}\n------------")
            print(f"Text:\n {generation['text']}\n")
            if 'likelihood' in generation:
                print(f"Likelihood:\n {generation['likelihood']}\n")
            
            print(f"Reason: {generation['finish_reason']}\n\n")

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