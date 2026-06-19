

# Cohere Embed v3
<a name="model-parameters-embed-v3"></a>

**Topics**
+ [Request and Response](#model-parameters-embed-v3-request-response)
+ [Code example](#api-inference-examples-cohere-embed-v3)

## Request and Response
<a name="model-parameters-embed-v3-request-response"></a>

------
#### [ Request ]

The Cohere Embed models have the following inference parameters. 

```
{
    "input_type": "search_document|search_query|classification|clustering|image",
    "texts":[string],
    "images":[image_base64_image_uri]
    "truncate": "NONE|START|END",
    "embedding_types": embedding_types
}
```

The following are required parameters.
+ **texts** – An array of strings for the model to embed. Each text has a maximum length of 512 tokens (approximately 2,048 characters). 1 token is about 4 characters.

  The following are text per call and character limits.

**Texts per call**  
    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed-v3.html)

**Characters**  
    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed-v3.html)
+ **input\_type** – Prepends special tokens to differentiate each type from one another. You should not mix different types together, except when mixing types for for search and retrieval. In this case, embed your corpus with the `search_document` type and embedded queries with type `search_query` type. 
  + `search_document` – In search use-cases, use `search_document` when you encode documents for embeddings that you store in a vector database.
  + `search_query` – Use `search_query` when querying your vector DB to find relevant documents.
  + `classification` – Use `classification` when using embeddings as an input to a text classifier.
  + `clustering` – Use `clustering` to cluster the embeddings.
  + `images` – This is an array of images.
    + An array of image data URIs for the model to embed. Maximum number of images per call is 1 (i.e, the model only supports one image input).
    + The image must be a valid data URI. The image must be in either image/jpeg or image/png format and has a maximum size of 5MB.
    + Only one of either “images” or “texts” must be provided.

The following are optional parameters:
+  **truncate** – Specifies how the API handles inputs longer than the maximum token length. Use one of the following:
  + `NONE` – Returns an error when the input exceeds the maximum input token length. 
  + `START` – Discards the start of the input. 
  + `END` – (Default) Discards the end of the input.

  If you specify `START` or `END`, the model discards the input until the remaining input is exactly the maximum input token length for the model.
+  **embedding\_types** – Specifies the types of embeddings you want to have returned. Optional and default is `None`, which returns the `Embed Floats` response type. Can be one or more of the following types:
  + `float` – Use this value to return the default float embeddings. 
  + `int8` – Use this value to return signed int8 embeddings. 
  + `uint8` – Use this value to return unsigned int8 embeddings. 
  + `binary` – Use this value to return signed binary embeddings. 
  + `ubinary` – Use this value to return unsigned binary embeddings. 

For more information, see [https://docs.cohere.com/reference/embed](https://docs.cohere.com/reference/embed) in the Cohere documentation.

------
#### [ Response ]

The `body` response from a call to `InvokeModel` is the following:

```
{
    "embeddings": [
        [ {{array of 1024 floats.}} ]
    ],
    "id": string,
    "response_type" : "embeddings_floats,
    "texts": [string],
    "images": [image_description]
}
```

The `body` response has the following fields:
+ **id** – An identifier for the response. 
+ **response\_type** – The response type. This value is always `embeddings_floats`. 
+ **embeddings** – An array of embeddings, where each embedding is an array of floats with 1024 elements. The length of the `embeddings` array will be the same as the length of the original `texts` array. 
+ **texts** – An array containing the text entries for which embeddings were returned. 
+ **images** – An array of a description for each image input.

  An `image_description`image\_description is of this form:

  ```
  {
      "width": long,
      "height": long,
      "format": string,
      "bit_depth": long
  }
  ```

  If image was used as input, the `“texts”` response field will be an empty array. Vice-versa is not true (i.e, when texts is used, `“images”` will not be in the response)

For more information, see [https://docs.cohere.com/reference/embed](https://docs.cohere.com/reference/embed).

------

## Code example
<a name="api-inference-examples-cohere-embed-v3"></a>

This examples shows how to call the *Cohere Embed English* model.

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate text embeddings using the Cohere Embed English model.
"""
import json
import logging
import boto3


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text_embeddings(model_id, body, region_name):
    """
    Generate text embedding by using the Cohere Embed model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The reqest body to use.
        region_name (str): The AWS region to invoke the model on
    Returns:
        dict: The response from the model.
    """

    logger.info("Generating text embeddings with the Cohere Embed model %s", model_id)

    accept = '*/*'
    content_type = 'application/json'

    bedrock = boto3.client(service_name='bedrock-runtime', region_name=region_name)

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    logger.info("Successfully generated embeddings with Cohere model %s", model_id)

    return response


def main():
    """
    Entrypoint for Cohere Embed example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    region_name = 'us-east-1'

    model_id = 'cohere.embed-english-v3'
    text1 = "hello world"
    text2 = "this is a test"
    input_type = "search_document"
    embedding_types = ["int8", "float"]

    try:
        body = json.dumps({
            "texts": [
                text1,
                text2],
            "input_type": input_type,
            "embedding_types": embedding_types
        })
        
        response = generate_text_embeddings(model_id=model_id, body=body, region_name=region_name)

        response_body = json.loads(response.get('body').read())

        print(f"ID: {response_body.get('id')}")
        print(f"Response type: {response_body.get('response_type')}")

        print("Embeddings")
        embeddings = response_body.get('embeddings')
        for i, embedding_type in enumerate(embeddings):
            print(f"\t{embedding_type} Embeddings:")
            print(f"\t{embeddings[embedding_type]}")

        print("Texts")
        for i, text in enumerate(response_body.get('texts')):
            print(f"\tText {i}: {text}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    else:
        print(
            f"Finished generating text embeddings with Cohere model {model_id}.")


if __name__ == "__main__":
    main()
```

**Image Input**

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate image embeddings using the Cohere Embed English model.
"""
import json
import logging
import boto3
import base64


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_base64_image_uri(image_file_path: str, image_mime_type: str):
    with open(image_file_path, "rb") as image_file:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{image_mime_type};base64,{base64_image}"


def generate_image_embeddings(model_id, body, region_name):
    """
    Generate image embedding by using the Cohere Embed model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The reqest body to use.
        region_name (str): The AWS region to invoke the model on
    Returns:
        dict: The response from the model.
    """

    logger.info("Generating image embeddings with the Cohere Embed model %s", model_id)

    accept = '*/*'
    content_type = 'application/json'

    bedrock = boto3.client(service_name='bedrock-runtime', region_name=region_name)

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    logger.info("Successfully generated embeddings with Cohere model %s", model_id)

    return response


def main():
    """
    Entrypoint for Cohere Embed example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    region_name = 'us-east-1'

    image_file_path = "image.jpg"
    image_mime_type = "image/jpg"

    model_id = 'cohere.embed-english-v3'
    input_type = "image"
    images = [get_base64_image_uri(image_file_path, image_mime_type)]
    embedding_types = ["int8", "float"]

    try:
        body = json.dumps({
            "images": images,
            "input_type": input_type,
            "embedding_types": embedding_types
        })
        
        response = generate_image_embeddings(model_id=model_id, body=body, region_name=region_name)

        response_body = json.loads(response.get('body').read())

        print(f"ID: {response_body.get('id')}")
        print(f"Response type: {response_body.get('response_type')}")

        print("Embeddings")
        embeddings = response_body.get('embeddings')
        for i, embedding_type in enumerate(embeddings):
            print(f"\t{embedding_type} Embeddings:")
            print(f"\t{embeddings[embedding_type]}")

        print("Texts")
        for i, text in enumerate(response_body.get('texts')):
            print(f"\tText {i}: {text}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    else:
        print(
            f"Finished generating text embeddings with Cohere model {model_id}.")


if __name__ == "__main__":
    main()
```