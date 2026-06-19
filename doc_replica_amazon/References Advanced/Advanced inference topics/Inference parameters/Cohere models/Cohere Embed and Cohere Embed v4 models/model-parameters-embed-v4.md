

# Cohere Embed v4
<a name="model-parameters-embed-v4"></a>

Cohere Embed v4 is a multimodal embedding model that supports both text and image inputs. It can process interleaved text and image content, making it ideal for document understanding, visual search, and multimodal retrieval applications. The model supports various embedding types including float, int8, uint8, binary, and ubinary formats, with configurable output dimensions from 256 to 1536.

The model ID for Cohere Embed v4 is `cohere.embed-v4`.

**Additional usage notes**  

+ **Context length:** Up to \~128k tokens per document; for RAG, smaller chunks often improve retrieval and cost.
+ **Image sizing:** Images > 2,458,624 pixels are downsampled to that size; images < 3,136 pixels are upsampled.
+ **Interleaved inputs:** Prefer inputs.content[] for page-like multimodal content so text context (e.g., filename, entities) travels with the image.

**Topics**
+ [Request and Response](#model-parameters-embed-v4-request-response)
+ [Request and response for different input\_types](#api-inference-examples-cohere-embed-v4)
+ [Code Examples](#code-examples-cohere-embed-v4)

## Request and Response
<a name="model-parameters-embed-v4-request-response"></a>

------
#### [ Request ]

Content type: application/json

```
{
  "input_type": "search_document | search_query | classification | clustering",
  "texts": ["..."],                      // optional; text-only
  "images": ["data:<mime>;base64,..."],  // optional; image-only
  "inputs": [
    { "content": [
        { "type": "text",      "text": "..." },
        { "type": "image_url", "image_url": {"url": "data:<mime>;base64,..."} }
      ]
    }
  ],                                     // optional; mixed (interleaved) text+image
  "embedding_types": ["float" | "int8" | "uint8" | "binary" | "ubinary"],
  "output_dimension": 256 | 512 | 1024 | 1536,
  "max_tokens": 128000,
  "truncate": "NONE | LEFT | RIGHT"
}
```

**Parameters**  

+ **input\_type** (required) – Adds special tokens to distinguish use cases. Allowed: `search_document`, `search_query`, `classification`, `clustering`. For search/RAG, embed your corpus with `search_document` and queries with `search_query`.
+ **texts** (optional) – Array of strings to embed. Max 96 per call. If you use `texts`, don't send `images` in the same call.
+ **images** (optional) – Array of data-URI base64 images to embed. Max 96 per call. Don't send `texts` and `images` together. (Use `inputs` for interleaved.)
+ **inputs** (optional; mixed/fused modality) – A list where each item has a content list of parts. Each part is `{ "type": "text", "text": ... }` or `{ "type": "image_url", "image_url": {"url": "data:<mime>;base64,..."} }`. Send interleaved page-like content here (e.g., PDF page image \+ caption/metadata). Max 96 items.
+ **embedding\_types** (optional) – One or more of: `float`, `int8`, `uint8`, `binary`, `ubinary`. If omitted, returns float embeddings.
+ **output\_dimension** (optional) – Select vector length. Allowed: `256`, `512`, `1024`, `1536` (default `1536` if unspecified).
+ **max\_tokens** (optional) – Truncation budget per input document. The model supports up to \~128,000 tokens per document; chunk smaller for RAG as appropriate.
+ **truncate** (optional) – How to handle over-length inputs: `LEFT` drops tokens from the start; `RIGHT` drops from the end; `NONE` returns an error if the input exceeds the limit.

**Limits & sizing**  

+ Items per request: up to 96 images. The original image file type must be in a png, jpeg, webp, or gif format and can be up to 5 MB in size.
+ Request size cap: \~20 MB total payload.
+ Maximum input tokens: 128k tokens max. Image files are converted into tokens, and total tokens should be less than 128k.
+ Images: max 2,458,624 pixels before downsampling; images smaller than 3,136 pixels are upsampled. Provide images as `data:<mime>;base64,....`
+ Token accounting (per `inputs` item): Tokens from an image input ≈ (image pixels ÷ 784) x 4 Tokens from an interleaved text and image input = (image pixels ÷ 784) x 4 \+ (text tokens)

**Tip:** For PDFs, convert each page to an image and send via `inputs` along with page metadata (e.g., file\_name, entities) in adjacent text parts.

------
#### [ Response ]

Content type: application/json

If you requested a single embedding type (e.g., only `float`):

```
{
"id": "string",
"embeddings": [[ /* length = output_dimension */ ]],
"response_type": "embeddings_floats",
"texts": ["..."], // present if text was provided
"inputs": [ { "content": [ ... ] } ] // present if 'inputs' was used
}
```

If you requested multiple embedding types (e.g., `["float","int8"]`):

```
{
  "id": "string",
  "embeddings": {
    "float": [[ ... ]],
    "int8":  [[ ... ]]
  },
  "response_type": "embeddings_by_type",
  "texts": ["..."],     // when text used
  "inputs": [ { "content": [ ... ] } ] // when 'inputs' used
}
```
+ The number of returned vectors matches the length of your `texts` array or the number of `inputs` items.
+ Each vector's length equals `output_dimension` (default `1536`).

------

## Request and response for different input\_types
<a name="api-inference-examples-cohere-embed-v4"></a>

**A) Interleaved page (image \+ caption) with compact int8 vectors**

**Request**  


```
{
  "input_type": "search_document",
  "inputs": [
    {
      "content": [
        { "type": "text", "text": "Quarterly ARR growth chart; outlier in Q3." },
        { "type": "image_url", "image_url": {"url": "data:image/png;base64,{{BASE64_PAGE_IMG}}"} }
      ]
    }
  ],
  "embedding_types": ["int8"],
  "output_dimension": 512,
  "truncate": "RIGHT",
  "max_tokens": 128000
}
```

**Response (truncated)**  


```
{
  "id": "836a33cc-61ec-4e65-afaf-c4628171a315",
  "embeddings": { "int8": [[ 7, -3, ... ]] },
  "response_type": "embeddings_by_type",
  "inputs": [
    { "content": [
      { "type": "text", "text": "Quarterly ARR growth chart; outlier in Q3." },
      { "type": "image_url", "image_url": {"url": "data:image/png;base64,{{...}}"} }
    ] }
  ]
}
```

**B) Text-only corpus indexing (default float, 1536-dim)**

**Request**  


```
{
  "input_type": "search_document",
  "texts": [
    "RAG system design patterns for insurance claims",
    "Actuarial loss triangles and reserving primer"
  ]
}
```

**Response (sample)**  


```
{
  "response_type": "embeddings_floats",
  "embeddings": [
    [0.0135, -0.0272, ...],   // length 1536
    [0.0047,  0.0189, ...]
  ]
}
```

## Code Examples
<a name="code-examples-cohere-embed-v4"></a>

------
#### [ Text input ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate embeddings using the Cohere Embed v4 model.
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

    model_id = 'cohere.embed-v4:0'
    text1 = "hello world"
    text2 = "this is a test"
    input_type = "search_document"
    embedding_types = ["float"]

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

------
#### [ Mixed modalities ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate image embeddings using the Cohere Embed v4 model.
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


def generate_embeddings(model_id, body, region_name):
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
    text = "hello world"

    model_id = 'cohere.embed-v4:0'
    input_type = "search_document"
    image_base64_uri = get_base64_image_uri(image_file_path, image_mime_type)
    embedding_types = ["int8","float"]

    try:
        body = json.dumps({
            "inputs": [
                {
                  "content": [
                    { "type": "text", "text": text },
                    { "type": "image_url", "image_url": {"url": "data:image/png;base64,{{image_base64_uri}}"} }
                  ]
                }
              ],
            "input_type": input_type,
            "embedding_types": embedding_types
        })
        
        response = generate_embeddings(model_id=model_id, body=body, region_name=region_name)

        response_body = json.loads(response.get('body').read())

        print(f"ID: {response_body.get('id')}")
        print(f"Response type: {response_body.get('response_type')}")

        print("Embeddings")
        embeddings = response_body.get('embeddings')
        for i, embedding_type in enumerate(embeddings):
            print(f"\t{embedding_type} Embeddings:")
            print(f"\t{embeddings[embedding_type]}")

        print("inputs")
        for i, input in enumerate(response_body.get('inputs')):
            print(f"\tinput {i}: {input}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    else:
        print(
            f"Finished generating embeddings with Cohere model {model_id}.")


if __name__ == "__main__":
    main()
```

------