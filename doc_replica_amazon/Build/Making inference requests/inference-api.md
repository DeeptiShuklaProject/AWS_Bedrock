

# Inference using Invoke API
<a name="inference-api"></a>

The Invoke API is available on the `bedrock-runtime` endpoint only. Amazon Bedrock offers the following API operations for carrying out model inference with the Invoke API:
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) – Submit a prompt and generate a response. The request body is model-specific. To generate streaming responses, use [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html).
+ [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) – Submit a prompt and generate a response asynchronously that can be retrieved later. Used to generate videos.
+ [InvokeModelWithBidirectionalStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithBidirectionalStream.html) – 

**Note**  
Restrictions apply to the following operations: `InvokeModel`, `InvokeModelWithResponseStream`, `Converse`, and `ConverseStream`. See [API restrictions](inference-api-restrictions.md) for details.

For model inference, you need to determine the following parameters:
+ Model ID – The ID or Amazon Resource Name (ARN) of the model or inference profile to use in the `modelId` field for inference. The following table describes how to find IDs for different types of resources:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/inference-api.html)
+ Request body – Contains the inference parameters for a model and other configurations. Each base model has its own inference parameters. The inference parameters for a custom or provisioned model depends on the base model from which it was created. For more information, see [Inference request parameters and response fields for foundation models](model-parameters.md).

## Submit a single prompt with InvokeModel
<a name="invoke-model-usage"></a>

You run inference on a single prompt by using the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API operations and specifying a model. Amazon Bedrock models differ in whether they accept text, image, or video inputs and whether they can produce outputs of text, image, or embeddings. Some models can return the response in a stream. To check model support for input, output, and streaming support, do one of the following:
+ Check the value in the **Input modalities**, **Output modalities**, or **Streaming supported** columns for a model at [Supported foundation models in Amazon Bedrock](models-supported.md).
+ Send a [GetFoundationModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html) request with the model ID and check the values in the `inputModalities`, `outputModalities`, and `responseStreamingSupported` field.

Run model inference on a prompt by sending an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) request with an [Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt).

**Note**  
Restrictions apply to the following operations: `InvokeModel`, `InvokeModelWithResponseStream`, `Converse`, and `ConverseStream`. See [API restrictions](inference-api-restrictions.md) for details.

The following fields are required:


****  

| Field | Use case | 
| --- | --- | 
| modelId | To specify the model, inference profile, or prompt from Prompt management to use. To learn how to find this value, see [Inference using Invoke API](#inference-api). | 
| body | To specify the inference parameters for a model. To see inference parameters for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md). If you specify a prompt from Prompt management in the modelId field, omit this field (if you include it, it will be ignored). | 

The following fields are optional:


****  

| Field | Use case | 
| --- | --- | 
| accept | To specify the media type for the request body. For more information, see Media Types on the [Swagger website](https://swagger.io/specification/). | 
| contentType | To specify the media type for the response body. For more information, see Media Types on the [Swagger website](https://swagger.io/specification/). | 
| performanceConfigLatency | To specify whether to optimize a model for latency. For more information, see [Optimize model inference for latency](latency-optimized-inference.md). | 
| guardrailIdentifier | To specify a guardrail to apply to the prompt and response. For more information, see [Test your guardrail](guardrails-test.md). | 
| guardrailVersion | To specify a guardrail to apply to the prompt and response. For more information, see [Test your guardrail](guardrails-test.md). | 
| trace | To specify whether to return the trace for the guardrail you specify. For more information, see [Test your guardrail](guardrails-test.md). | 
| serviceTier | To specify the service tier for a request. For more information, see [Service tiers for optimizing performance and cost](service-tiers-inference.md). | 

### Invoke model code examples
<a name="inference-example-invoke"></a>

This topic provides some basic examples for running inference using a single prompt with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) API. For more examples with different models, visit the following resources:
+ Pick an example under the [Code examples for Amazon Bedrock Runtime using AWS SDKs](service_code_examples_bedrock-runtime.md) topic.
+ Visit the inference parameter reference for the desired model at [Inference request parameters and response fields for foundation models](model-parameters.md).

The following examples assume that you've set up programmatic access such that you automatically authenticate to the AWS CLI and the SDK for Python (Boto3) in a default AWS Region when you run these examples. For information on setting up programmating access, see [Get started with the API](getting-started-api.md).

**Note**  
Review the following points before trying out the examples:  
You should test these examples in US East (N. Virginia) (us-east-1), which supports all the models used in the examples.
The `body` parameter can be large, so for some CLI examples, you'll be asked to create a JSON file and provide that file into the `--body` argument instead of specifying it in the command line.
For the image and video examples, you'll be asked to use your own image and video. The examples assume that your image file is named {{image.png}} and that your video file is named {{video.mp4}}.
You might have to convert images or videos into a base64-encoded string or upload them to an Amazon S3 location. In the examples, you'll have to replace the placeholders with the actual base64-encoded string or S3 location.

#### Generate text with a text prompt
<a name="w2aac15c15c30c13c19c11"></a>

The following examples generate a text response to a text prompt using the Amazon Titan Text Premier model. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Run the following command in a terminal and find the generated response in a file called {{invoke-model-output.txt}}.

```
aws bedrock-runtime invoke-model \
    --model-id amazon.titan-text-premier-v1:0 \
    --body '{
        "inputText": "Describe the purpose of a 'hello world' program in one line.",
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.5
        }
    }' \
    --cli-binary-format raw-in-base64-out \
    invoke-model-output.txt
```

------
#### [ Python ]

Run the following Python code example to generate a text response:

```
# Use the native inference API to send a text message to Amazon Titan Text.

import boto3
import json

from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Text Premier.
model_id = "amazon.titan-text-premier-v1:0"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
native_request = {
    "inputText": prompt,
    "textGenerationConfig": {
        "maxTokenCount": 512,
        "temperature": 0.5,
    },
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["results"][0]["outputText"]
print(response_text)
```

------

#### Generate text with a text prompt using service tier
<a name="w2aac15c15c30c13c19c13"></a>

The following examples generate a text response to a text prompt using the OpenAI GPT model with a service tier to prioritize the request. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Run the following command in a terminal and validate the service tier in the response.

```
aws bedrock-runtime invoke-model \
    --model-id openai.gpt-oss-120b-1:0 \
    --body '{
        "messages": [
            {
                "role": "user",
                "content": "Describe the purpose of a '\''hello world'\'' program in one line."
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }' \
    --content-type application/json \
    --accept application/json \
    --service-tier priority \
    --cli-binary-format raw-in-base64-out
```

------
#### [ Python ]

Run the following Python code example to generate a text response with service tier:

```
import boto3
import json

# Create a Bedrock Runtime client
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Define the model ID and request body
model_id = "openai.gpt-oss-120b-1:0"
body = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": "Describe the purpose of a 'hello world' program in one line."
        }
    ],
    "max_tokens": 512,
    "temperature": 0.7
})

# Make the request with service tier
response = bedrock_runtime.invoke_model(
    modelId=model_id,
    body=body,
    contentType="application/json",
    accept="application/json",
    serviceTier="priority"
)

# Parse and print the response
response_body = json.loads(response["body"])
print(response_body)
```

------

#### Generate an image with a text prompt
<a name="w2aac15c15c30c13c19c15"></a>

The following code examples generate an image using a text prompt with the Stable Diffusion XL 1.0 model. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Run the following command in a terminal and find the generated response in a file called {{invoke-model-output.txt}}. The bytes that represent the image can be found in the `base64` field in the response:

```
aws bedrock-runtime invoke-model \
    --model-id stability.stable-image-core-v1:1 \
    --body '{
        "prompt": "A stylized picture of a cute old steampunk robot.",
        "seed": 0
    }' \
    --cli-binary-format raw-in-base64-out \
    invoke-model-output.txt
```

------
#### [ Python ]

Run the following Python code example to generate an image and find the resulting {{stability\_1.png}} image file in a folder called {{output}}.

```
# Use the native inference API to create an image with Amazon Titan Image Generator

import base64
import boto3
import json
import os
import random

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Image Generator G1.
model_id = "amazon.titan-image-generator-v2:0"

# Define the image generation prompt for the model.
prompt = "A stylized picture of a cute old steampunk robot."

# Generate a random seed.
seed = random.randint(0, 2147483647)

# Format the request payload using the model's native structure.
native_request = {
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {"text": prompt},
    "imageGenerationConfig": {
        "numberOfImages": 1,
        "quality": "standard",
        "cfgScale": 8.0,
        "height": 512,
        "width": 512,
        "seed": seed,
    },
}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
response = client.invoke_model(modelId=model_id, body=request)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract the image data.
base64_image_data = model_response["images"][0]

# Save the generated image to a local folder.
i, output_dir = 1, "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
while os.path.exists(os.path.join(output_dir, f"titan_{i}.png")):
    i += 1

image_data = base64.b64decode(base64_image_data)

image_path = os.path.join(output_dir, f"titan_{i}.png")
with open(image_path, "wb") as file:
    file.write(image_data)

print(f"The generated image has been saved to {image_path}")
```

------

#### Generate embeddings from text
<a name="w2aac15c15c30c13c19c19"></a>

The following examples use the Amazon Titan Text Embeddings V2 model to generate binary embeddings for a text input. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Run the following command in a terminal and find the generated response in a file called {{invoke-model-output.txt}}. The resulting embeddings are in the `binary` field.

```
aws bedrock-runtime invoke-model \
    --model-id amazon.titan-embed-text-v2:0 \
    --body '{
        "inputText": "What are the different services that you offer?",
        "embeddingTypes": ["binary"]
    }' \
    --cli-binary-format raw-in-base64-out \
    invoke-model-output.txt
```

------
#### [ Python ]

Run the following Python code example to generate embeddings for the provided text:

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

#### Generate embeddings from an image
<a name="w2aac15c15c30c13c19c21"></a>

The following examples use the Amazon Titan Multimodal Embeddings G1 model to generate embeddings for an image input. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Open a terminal and do the following:

1. Convert an image titled {{image.png}} in your current folder into a base64-encoded string and write it to a file titled {{image.txt}} by running the following command:

   ```
   base64 -i {{image.png}} -o {{image.txt}}
   ```

1. Create a JSON file called {{image-input-embeddings-output.json}} and paste the following JSON, replacing {{${image-base64}}} with the contents of the {{image.txt}} file (make sure there is no new line at the end of the string):

   ```
   {
       "inputImage": "{{${image-base64}}}",
       "embeddingConfig": {
           "outputEmbeddingLength": 256
       }
   }
   ```

1. Run the following command, specifying the {{image-input-embeddings-output.json}} file as the body.

   ```
   aws bedrock-runtime invoke-model \
       --model-id amazon.titan-embed-image-v1 \
       --body file://image-input-embeddings-output.json \
       --cli-binary-format raw-in-base64-out \
       invoke-model-output.txt
   ```

1. Find the resulting embeddings in the {{invoke-model-output.txt}} file.

------
#### [ Python ]

In the following Python script, replace {{/path/to/image}} with the path to an actual image. Then run the script to generate embeddings:

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

#### Generate a text response to an image with an accompanying text prompt
<a name="w2aac15c15c30c13c19c23"></a>

Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

The following example uses the Anthropic Claude 3 Haiku model to generate a response, given an image and a text prompt that asks the contents of the image. Open a terminal and do the following:

1. Convert an image titled {{image.png}} in your current folder into a base64-encoded string and write it to a file titled {{image.txt}} by running the following command:

   ```
   base64 -i {{image.png}} -o {{image.txt}}
   ```

1. Create a JSON file called {{image-text-input.json}} and paste the following JSON, replacing {{${image-base64}}} with the contents of the {{image.txt}} file (make sure there is no new line at the end of the string):

   ```
   {
       "anthropic_version": "bedrock-2023-05-31",
       "max_tokens": 1000,
       "messages": [
           {               
               "role": "user",
               "content": [
                   {
                       "type": "image",
                       "source": {
                           "type": "base64",
                           "media_type": "image/png", 
                           "data": "{{${image-base64}}}"
                       }
                   },
                   {
                       "type": "text",
                       "text": "What's in this image?"
                   }
               ]
           }
       ]
   }
   ```

1. Run the following command to generate a text output, based on the image and the accompanying text prompt, to a file called {{invoke-model-output.txt}}:

   ```
   aws bedrock-runtime invoke-model \
       --model-id anthropic.claude-3-haiku-20240307-v1:0 \
       --body file://image-text-input.json \
       --cli-binary-format raw-in-base64-out \
       {{invoke-model-output.txt}}
   ```

1. Find the output in the {{invoke-model-output.txt}} file in the current folder.

------
#### [ Python ]

In the following python script, replace {{/path/to/image.png}} with the actual path to the image before running the script:

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

------

#### Generate a text response to a video uploaded to Amazon S3 with an accompanying text prompt
<a name="w2aac15c15c30c13c19c25"></a>

The following examples show how to generate a response with the Amazon Nova Lite model, given a video you upload to an S3 bucket and an accompanying text prompt.

**Prerequisite:** Upload a video titled {{video.mp4}} to an Amazon S3 bucket in your account by following the steps at [Uploading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html#upload-objects-procedure) in the Amazon Simple Storage Service User Guide. Take note of the S3 URI of the video.

Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Open a terminal and run the following command, replacing {{s3://amzn-s3-demo-bucket/video.mp4}} with the actual S3 location of your video:

```
aws bedrock-runtime invoke-model \
    --model-id amazon.nova-lite-v1:0 \
    --body '{
        "messages": [          
            {               
                "role": "user",
                "content": [      
                    {                       
                        "video": {     
                            "format": "mp4",   
                            "source": {
                                "s3Location": {
                                    "uri": "{{s3://amzn-s3-demo-bucket/video.mp4}}"
                                }
                            }
                        }                                    
                    },
                    {
                        "text": "What happens in this video?"
                    }
                ]
            }                              
        ]                  
    }' \
    --cli-binary-format raw-in-base64-out \
    {{invoke-model-output.txt}}
```

Find the output in the {{invoke-model-output.txt}} file in the current folder.

------
#### [ Python ]

In the following Python script, replace {{s3://amzn-s3-demo-bucket/video.mp4}} with the actual S3 location of your video. Then run the script:

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to run a multimodal prompt with Nova Lite (on demand) and InvokeModel.
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
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": max_tokens
            }
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body


def main():
    """
    Entrypoint for Nova Lite video prompt example.
    """

    try:

        bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        model_id = "amazon.nova-lite-v1:0"
        max_tokens = 1000
        input_video_s3_uri = "s3://amzn-s3-demo-bucket/video.mp4" # Replace with real S3 URI
        video_ext = input_video_s3_uri.split(".")[-1]
        input_text = "What happens in this video?"

        message = {
            "role": "user",
            "content": [
                {
                    "video": {
                        "format": video_ext,
                        "source": {
                            "s3Location": {
                                "uri": input_video_s3_uri
                            }
                        }
                    }
                },
                {
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
        print("A client error occured: " +
              format(message))


if __name__ == "__main__":
    main()
```

------

#### Generate a text response to a video converted to a base64-encoded string with an accompanying text prompt
<a name="w2aac15c15c30c13c19c27"></a>

The following examples show how to generate a response with the Amazon Nova Lite model, given a video converted to a base64-encoded string and an accompanying text prompt. Choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

Do the following:

1. Convert a video titled {{video.mp4}} in your current folder into base64 by running the following command:

   ```
   base64 -i {{video.mp4}} -o video.txt
   ```

1. Create a JSON file called {{video-text-input.json}} and paste the following JSON, replacing {{${video-base64}}} with the contents of the `video.txt` file (make sure there is no new line at the end):

   ```
   {
       "messages": [          
           {               
               "role": "user",
               "content": [      
                   {                       
                       "video": {     
                           "format": "mp4",   
                           "source": {
                               "bytes": {{${video-base64}}}
                           }
                       }                                    
                   },
                   {
                       "text": "What happens in this video?"
                   }
               ]
           }                              
       ]                  
   }
   ```

1. Run the following command to generate a text output based on the video and the accompanying text prompt to a file called {{invoke-model-output.txt}}:

   ```
   aws bedrock-runtime invoke-model \
       --model-id amazon.nova-lite-v1:0 \
       --body file://video-text-input.json \
       --cli-binary-format raw-in-base64-out \
       {{invoke-model-output.txt}}
   ```

1. Find the output in the {{invoke-model-output.txt}} file in the current folder.

------
#### [ Python ]

In the following Python script, replace {{/path/to/video.mp4}} with the actual path to the video. Then run the script:

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to run a multimodal prompt with Nova Lite (on demand) and InvokeModel.
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
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": max_tokens
            }
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body


def main():
    """
    Entrypoint for Nova Lite video prompt example.
    """

    try:

        bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        model_id = "amazon.nova-lite-v1:0"
        max_tokens = 1000
        input_video = "/path/to/video.mp4" # Replace with real path to video
        video_ext = input_video.split(".")[-1]
        input_text = "What happens in this video?"

        # Read reference video from file and encode as base64 string.
        with open(input_video, "rb") as video_file:
            content_video = base64.b64encode(video_file.read()).decode('utf8')\

        message = {
            "role": "user",
            "content": [
                {
                    "video": {
                        "format": video_ext,
                        "source": {
                            "bytes": content_video
                        }
                    }
                },
                {
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
        print("A client error occured: " +
              format(message))


if __name__ == "__main__":
    main()
```

------

### Invoke model with streaming code example
<a name="inference-examples-stream"></a>

**Note**  
The AWS CLI does not support streaming.

The following example shows how to use the [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API to generate streaming text with Python using the prompt {{write an essay for living on mars in 1000 words}}.

```
import boto3
import json

brt = boto3.client(service_name='bedrock-runtime')

body = json.dumps({
    'prompt': '\n\nHuman: write an essay for living on mars in 1000 words\n\nAssistant:',
    'max_tokens_to_sample': 4000
})
                   
response = brt.invoke_model_with_response_stream(
    modelId='anthropic.claude-v2', 
    body=body
)
    
stream = response.get('body')
if stream:
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            print(json.loads(chunk.get('bytes').decode()))
```