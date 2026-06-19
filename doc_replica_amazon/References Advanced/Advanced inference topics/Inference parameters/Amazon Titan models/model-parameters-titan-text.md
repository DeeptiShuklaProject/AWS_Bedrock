

# Amazon Titan Text models
<a name="model-parameters-titan-text"></a>

The Amazon Titan Text models support the following inference parameters.

For more information on Titan Text prompt engineering guidelines, see [Titan Text Prompt Engineering Guidelines](https://d2eo22ngex1n9g.cloudfront.net/Documentation/User+Guides/Titan/Amazon+Titan+Text+Prompt+Engineering+Guidelines.pdf). 

For more information on Titan models, see [Overview of Amazon Titan models](titan-models.md).

**Topics**
+ [Request and response](#model-parameters-titan-request-response)
+ [Code examples](#inference-titan-code)

## Request and response
<a name="model-parameters-titan-request-response"></a>

The request body is passed in the `body` field of an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) request.

------
#### [ Request ]

```
{
    "inputText": string,
    "textGenerationConfig": {
        "temperature": float,  
        "topP": float,
        "maxTokenCount": int,
        "stopSequences": [string]
    }
}
```

The following parameters are required:
+ **inputText** – The prompt to provide the model for generating a response. To generate responses in a conversational style, submit the prompt by using the following format:

  ```
  "inputText": "User: {{<theUserPrompt>}}\nBot:"
  ```

  This format indicates to the model that it should respond on a new line after the user has provided a prompt.

The `textGenerationConfig` is optional. You can use it to configure the following [inference parameters](inference-parameters.md):
+ **temperature** – Use a lower value to decrease randomness in responses.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html)
+ **topP** – Use a lower value to ignore less probable options and decrease the diversity of responses. The minimum value is exclusive of 0 — use a very small value such as 0.0001 instead.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html)
+ **maxTokenCount** – Specify the maximum number of tokens to generate in the response. Maximum token limits are strictly enforced.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html)
+ **stopSequences** – Specify a character sequence to indicate where the model should stop.

------
#### [ InvokeModel Response ]

```
{
    "inputTextTokenCount": int,
    "results": [{
        "tokenCount": int,
        "outputText": "\n{{<response>}}\n",
        "completionReason": "string"
    }]
}
```

The response body contains the following fields:
+ **inputTextTokenCount** – The number of tokens in the prompt.
+ **results** – An array of one item, an object containing the following fields:
  + **tokenCount** – The number of tokens in the response.
  + **outputText** – The text in the response.
  + **completionReason** – The reason the response finished being generated. The following reasons are possible:
    + FINISHED – The response was fully generated.
    + LENGTH – The response was truncated because of the response length you set.
    + STOP\_CRITERIA\_MET – The response was truncated because the stop criteria was reached.
    + RAG\_QUERY\_WHEN\_RAG\_DISABLED – The feature is disabled and cannot complete the query.
    + CONTENT\_FILTERED – The contents were filtered or removed by the content filter applied.

------
#### [ InvokeModelWithResponseStream Response ]

Each chunk of text in the body of the response stream is in the following format. You must decode the `bytes` field (see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md) for an example).

```
{
    "chunk": {
        "bytes": b'{
            "index": int,
            "inputTextTokenCount": int,
            "totalOutputTextTokenCount": int,
            "outputText": "{{<response-chunk>}}",
            "completionReason": "string"
        }'
    }
}
```
+ **index** – The index of the chunk in the streaming response.
+ **inputTextTokenCount** – The number of tokens in the prompt.
+ **totalOutputTextTokenCount** – The number of tokens in the response.
+ **outputText** – The text in the response.
+ **completionReason** – The reason the response finished being generated. The following reasons are possible.
  + FINISHED – The response was fully generated.
  + LENGTH – The response was truncated because of the response length you set.
  + STOP\_CRITERIA\_MET – The response was truncated because the stop criteria was reached.
  + RAG\_QUERY\_WHEN\_RAG\_DISABLED – The feature is disabled and cannot complete the query.
  + CONTENT\_FILTERED – The contents were filtered or removed by the filter applied.

------

## Code examples
<a name="inference-titan-code"></a>

The following example shows how to run inference with the Amazon Titan Text Premier model with the Python SDK.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to create a list of action items from a meeting transcript
with the Amazon Titan Text model (on demand).
"""
import json
import logging
import boto3

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Text models"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using Amazon Titan Text models on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (json): The response from the model.
    """

    logger.info(
        "Generating text with Amazon Titan Text model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Amazon Titan Text model %s", model_id)

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Text model example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        # You can replace the model_id with any other Titan Text Models
        # Titan Text Model family model_id is as mentioned below:
        # amazon.titan-text-premier-v1:0, amazon.titan-text-express-v1, amazon.titan-text-lite-v1
        model_id = 'amazon.titan-text-premier-v1:0'

        prompt = """Meeting transcript: Miguel: Hi Brant, I want to discuss the workstream  
            for our new product launch Brant: Sure Miguel, is there anything in particular you want
            to discuss? Miguel: Yes, I want to talk about how users enter into the product.
            Brant: Ok, in that case let me add in Namita. Namita: Hey everyone 
            Brant: Hi Namita, Miguel wants to discuss how users enter into the product.
            Miguel: its too complicated and we should remove friction.  
            for example, why do I need to fill out additional forms?  
            I also find it difficult to find where to access the product
            when I first land on the landing page. Brant: I would also add that
            I think there are too many steps. Namita: Ok, I can work on the
            landing page to make the product more discoverable but brant
            can you work on the additonal forms? Brant: Yes but I would need 
            to work with James from another team as he needs to unblock the sign up workflow.
            Miguel can you document any other concerns so that I can discuss with James only once?
            Miguel: Sure.
            From the meeting transcript above, Create a list of action items for each person. """

        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 3072,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9
            }
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Token count: {result['tokenCount']}")
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(
            f"Finished generating text with the Amazon Titan Text Premier model {model_id}.")


if __name__ == "__main__":
    main()
```

The following example shows how to run inference with the Amazon Titan Text G1 - Express model with the Python SDK.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to create a list of action items from a meeting transcript
with the Amazon &titan-text-express; model (on demand).
"""
import json
import logging
import boto3

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon &titan-text-express; model"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using Amazon &titan-text-express; model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (json): The response from the model.
    """

    logger.info(
        "Generating text with Amazon &titan-text-express; model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Amazon &titan-text-express; model %s", model_id)

    return response_body


def main():
    """
    Entrypoint for Amazon &titan-text-express; example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-text-express-v1'

        prompt = """Meeting transcript: Miguel: Hi Brant, I want to discuss the workstream  
            for our new product launch Brant: Sure Miguel, is there anything in particular you want
            to discuss? Miguel: Yes, I want to talk about how users enter into the product.
            Brant: Ok, in that case let me add in Namita. Namita: Hey everyone 
            Brant: Hi Namita, Miguel wants to discuss how users enter into the product.
            Miguel: its too complicated and we should remove friction.  
            for example, why do I need to fill out additional forms?  
            I also find it difficult to find where to access the product
            when I first land on the landing page. Brant: I would also add that
            I think there are too many steps. Namita: Ok, I can work on the
            landing page to make the product more discoverable but brant
            can you work on the additonal forms? Brant: Yes but I would need 
            to work with James from another team as he needs to unblock the sign up workflow.
            Miguel can you document any other concerns so that I can discuss with James only once?
            Miguel: Sure.
            From the meeting transcript above, Create a list of action items for each person. """

        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Token count: {result['tokenCount']}")
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(
            f"Finished generating text with the Amazon &titan-text-express; model {model_id}.")


if __name__ == "__main__":
    main()
```