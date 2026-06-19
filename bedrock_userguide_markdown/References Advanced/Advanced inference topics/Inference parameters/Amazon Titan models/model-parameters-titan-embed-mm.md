

# Amazon Titan Multimodal Embeddings G1
<a name="model-parameters-titan-embed-mm"></a>

This section provides request and response body formats and code examples for using Amazon Titan Multimodal Embeddings G1.

**Topics**
+ [Request and response](#model-parameters-titan-embed-mm-request-response)
+ [Example code](#api-inference-examples-titan-embed-mm)

## Request and response
<a name="model-parameters-titan-embed-mm-request-response"></a>

The request body is passed in the `body` field of an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) request.

------
#### [ Request ]

The request body for Amazon Titan Multimodal Embeddings G1 includes the following fields.

```
{
    "inputText": string,
    "inputImage": base64-encoded string,
    "embeddingConfig": {
        "outputEmbeddingLength": 256 | 384 | 1024
    }
}
```

At least one of the following fields is required. Include both to generate an embeddings vector that averages the resulting text embeddings and image embeddings vectors.
+ **inputText** – Enter text to convert to embeddings.
+ **inputImage** – Encode the image that you want to convert to embeddings in base64 and enter the string in this field. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#api-inference-examples-titan-embed-mm).

The following field is optional.
+ **embeddingConfig** – Contains an `outputEmbeddingLength` field, in which you specify one of the following lengths for the output embeddings vector.
  + 256
  + 384
  + 1024 (default)

------
#### [ Response ]

The `body` of the response contains the following fields.

```
{
    "embedding": [float, float, ...],
    "inputTextTokenCount": int,
    "message": string
}
```

The fields are described below.
+ **embedding** – An array that represents the embeddings vector of the input you provided.
+ **inputTextTokenCount** – The number of tokens in the text input.
+ **message** – Specifies any errors that occur during generation.

------

## Example code
<a name="api-inference-examples-titan-embed-mm"></a>

The following examples show how to invoke the Amazon Titan Multimodal Embeddings G1 model with on-demand throughput in the Python SDK. Select a tab to view an example for each use-case.

------
#### [ Text embeddings ]

This example shows how to call the Amazon Titan Multimodal Embeddings G1 model to generate text embeddings.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate embeddings from text with the Amazon Titan Multimodal Embeddings G1 model (on demand).
"""

import json
import logging
import boto3


from botocore.exceptions import ClientError

class EmbedError(Exception):
    "Custom exception for errors returned by Amazon Titan Multimodal Embeddings G1"

    def __init__(self, message):
        self.message = message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_embeddings(model_id, body):
    """
    Generate a vector of embeddings for a text input using Amazon Titan Multimodal Embeddings G1 on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embeddings that the model generated, token information, and the
        reason the model stopped generating embeddings.
    """

    logger.info("Generating embeddings with Amazon Titan Multimodal Embeddings G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get('body').read())

    finish_reason = response_body.get("message")

    if finish_reason is not None:
        raise EmbedError(f"Embeddings generation error: {finish_reason}")

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Multimodal Embeddings G1 example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "amazon.titan-embed-image-v1"
    input_text = "What are the different services that you offer?"
    output_embedding_length = 256

    # Create request body.
    body = json.dumps({
        "inputText": input_text,
        "embeddingConfig": {
            "outputEmbeddingLength": output_embedding_length
        }
    })


    try:

        response = generate_embeddings(model_id, body)

        print(f"Generated text embeddings of length {output_embedding_length}: {response['embedding']}")
        print(f"Input text token count:  {response['inputTextTokenCount']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
        
    except EmbedError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(f"Finished generating text embeddings with Amazon Titan Multimodal Embeddings G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Image embeddings ]

This example shows how to call the Amazon Titan Multimodal Embeddings G1 model to generate image embeddings.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate embeddings from an image with the Amazon Titan Multimodal Embeddings G1 model (on demand).
"""

import base64
import json
import logging
import boto3

from botocore.exceptions import ClientError

class EmbedError(Exception):
    "Custom exception for errors returned by Amazon Titan Multimodal Embeddings G1"

    def __init__(self, message):
        self.message = message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_embeddings(model_id, body):
    """
    Generate a vector of embeddings for an image input using Amazon Titan Multimodal Embeddings G1 on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embeddings that the model generated, token information, and the
        reason the model stopped generating embeddings.
    """

    logger.info("Generating embeddings with Amazon Titan Multimodal Embeddings G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get('body').read())

    finish_reason = response_body.get("message")

    if finish_reason is not None:
        raise EmbedError(f"Embeddings generation error: {finish_reason}")

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Multimodal Embeddings G1 example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # Read image from file and encode it as base64 string.
    with open("/path/to/image", "rb") as image_file:
        input_image = base64.b64encode(image_file.read()).decode('utf8')

    model_id = 'amazon.titan-embed-image-v1'
    output_embedding_length = 256

    # Create request body.
    body = json.dumps({
        "inputImage": input_image,
        "embeddingConfig": {
            "outputEmbeddingLength": output_embedding_length
        }
    })


    try:

        response = generate_embeddings(model_id, body)

        print(f"Generated image embeddings of length {output_embedding_length}: {response['embedding']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
        
    except EmbedError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(f"Finished generating image embeddings with Amazon Titan Multimodal Embeddings G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Text and image embeddings ]

This example shows how to call the Amazon Titan Multimodal Embeddings G1 model to generate embeddings from a combined text and image input. The resulting vector is the average of the generated text embeddings vector and the image embeddings vector.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate embeddings from an image and accompanying text with the Amazon Titan Multimodal Embeddings G1 model (on demand).
"""

import base64
import json
import logging
import boto3

from botocore.exceptions import ClientError

class EmbedError(Exception):
    "Custom exception for errors returned by Amazon Titan Multimodal Embeddings G1"

    def __init__(self, message):
        self.message = message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_embeddings(model_id, body):
    """
    Generate a vector of embeddings for a combined text and image input using Amazon Titan Multimodal Embeddings G1 on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embeddings that the model generated, token information, and the
        reason the model stopped generating embeddings.
    """

    logger.info("Generating embeddings with Amazon Titan Multimodal Embeddings G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get('body').read())

    finish_reason = response_body.get("message")

    if finish_reason is not None:
        raise EmbedError(f"Embeddings generation error: {finish_reason}")

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Multimodal Embeddings G1 example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "amazon.titan-embed-image-v1"
    input_text = "A family eating dinner"
    # Read image from file and encode it as base64 string.
    with open("/path/to/image", "rb") as image_file:
        input_image = base64.b64encode(image_file.read()).decode('utf8')
    output_embedding_length = 256

    # Create request body.
    body = json.dumps({
        "inputText": input_text,
        "inputImage": input_image,
        "embeddingConfig": {
            "outputEmbeddingLength": output_embedding_length
        }
    })


    try:

        response = generate_embeddings(model_id, body)

        print(f"Generated embeddings of length {output_embedding_length}: {response['embedding']}")
        print(f"Input text token count:  {response['inputTextTokenCount']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
        
    except EmbedError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(f"Finished generating embeddings with Amazon Titan Multimodal Embeddings G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------