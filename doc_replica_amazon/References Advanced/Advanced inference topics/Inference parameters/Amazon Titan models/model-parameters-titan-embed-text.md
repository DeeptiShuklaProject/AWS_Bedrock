

# Amazon Titan Embeddings G1 - Text
<a name="model-parameters-titan-embed-text"></a>

Titan Embeddings G1 - Text does not support the use of inference parameters. The following sections detail the request and response formats and provides a code example.

**Topics**
+ [Request and response](#model-parameters-titan-embed-text-request-response)
+ [Example code](#api-inference-examples-titan-embed-text)

## Request and response
<a name="model-parameters-titan-embed-text-request-response"></a>

The request body is passed in the `body` field of an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) request. 

------
#### [ V2 Request ]

The inputText parameter is required. The normalize and dimensions parameters are optional.
+ inputText – Enter text to convert to an embedding.
+ normalize – (optional) Flag indicating whether or not to normalize the output embedding. Defaults to true.
+ dimensions – (optional) The number of dimensions the output embedding should have. The following values are accepted: 1024 (default), 512, 256.
+ embeddingTypes – (optional) Accepts a list containing "float", "binary", or both. Defaults to `float`. 

```
{
    "inputText": string,
    "dimensions": int,
    "normalize": boolean,
    "embeddingTypes": list
}
```

------
#### [ V2 Response ]

The fields are described below.
+ embedding – An array that represents the embedding vector of the input you provided. This will always be type `float`.
+ inputTextTokenCount – The number of tokens in the input.
+ embeddingsByType – A dictionary or map of the embedding list. Depends on the input, lists "float", "binary", or both.
  + Example: `"embeddingsByType": {"binary": [int,..], "float": [float,...]}`
  + This field will always appear. Even if you don't specify `embeddingTypes` in your input, there will still be “float”. Example: `"embeddingsByType": {"float": [float,...]}`

```
{
    "embedding": [float, float, ...],
    "inputTextTokenCount": int,
    "embeddingsByType": {"binary": [int,..], "float": [float,...]}
}
```

------
#### [ G1 Request ]

The only available field is `inputText`, in which you can include text to convert into an embedding.

```
{
    "inputText": string
}
```

------
#### [ G1 Response ]

The `body` of the response contains the following fields.

```
{
    "embedding": [float, float, ...],
    "inputTextTokenCount": int
}
```

The fields are described below.
+ **embedding** – An array that represents the embedding vector of the input you provided.
+ **inputTextTokenCount** – The number of tokens in the input.

------

## Example code
<a name="api-inference-examples-titan-embed-text"></a>

The following examples show how to call the Amazon Titan Embeddings models to generate embedding. Select the tab that corresponds to the model you're using:

------
#### [ Amazon Titan Text Embeddings V2 ]

When using Titan Text Embeddings V2, the `embedding` field is not in the response if the `embeddingTypes` only contains `binary`. 

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an embedding with the Amazon Titan Text Embeddings V2 Model
"""

import json
import logging
import boto3


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_embedding(model_id, body):
    """
    Generate an embedding with the vector representation of a text input using Amazon Titan Text Embeddings G1 on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embedding created by the model and the number of input tokens.
    """

    logger.info("Generating an embedding with Amazon Titan Text Embeddings V2 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get('body').read())

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Embeddings V2 - Text example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "amazon.titan-embed-text-v2:0"
    input_text = "What are the different services that you offer?"


    # Create request body.
    body = json.dumps({
        "inputText": input_text,
        "embeddingTypes": ["binary"]
    })


    try:

        response = generate_embedding(model_id, body)

        print(f"Generated an embedding: {response['embeddingsByType']['binary']}") # returns binary embedding
        print(f"Input text: {input_text}")
        print(f"Input Token count:  {response['inputTextTokenCount']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))

    else:
        print(f"Finished generating an embedding with Amazon Titan Text Embeddings V2 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Amazon Titan Embeddings G1 - Text ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an embedding with the Amazon Titan Embeddings G1 - Text model (on demand).
"""

import json
import logging
import boto3


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_embedding(model_id, body):
    """
    Generate an embedding with the vector representation of a text input using Amazon Titan Embeddings G1 - Text on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (JSON): The embedding created by the model and the number of input tokens.
    """

    logger.info("Generating an embedding with Amazon Titan Embeddings G1 - Text model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get('body').read())

    return response_body


def main():
    """
    Entrypoint for Amazon Titan Embeddings G1 - Text example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = "amazon.titan-embed-text-v1"
    input_text = "What are the different services that you offer?"


    # Create request body.
    body = json.dumps({
        "inputText": input_text,
    })


    try:

        response = generate_embedding(model_id, body)

        print(f"Generated an embedding: {response['embedding']}")
        print(f"Input Token count:  {response['inputTextTokenCount']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))

    else:
        print(f"Finished generating an embedding with Amazon Titan Embeddings G1 - Text model {model_id}.")


if __name__ == "__main__":
    main()
```

------