

# Amazon Titan Image Generator G1 models
<a name="model-parameters-titan-image"></a>

The Amazon Titan Image Generator G1 V1 and Titan Image Generator G1 V2 models support the following inference parameters and model responses when carrying out model inference.

**Topics**
+ [Inference parameters](#model-parameters-titan-image-api)
+ [Examples](#model-parameters-titan-image-code-examples)

## Inference parameters
<a name="model-parameters-titan-image-api"></a>

When you make an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) call using the Amazon Titan Image Generator models, replace the `body` field of the request with the format that matches your use-case. All tasks share an `imageGenerationConfig` object, but each task has a parameters object specific to that task. The following use-cases are supported.


****  

| taskType | Task parameters field | Type of task | Definition | 
| --- | --- | --- | --- | 
| TEXT\_IMAGE | textToImageParams | Generation | Generate an image using a text prompt. | 
| TEXT\_IMAGE | textToImageParams | Generation | (Image conditioning-V2 only) Provide an additional input conditioning image along with a text prompt to generate an image that follows the layout and composition of the conditioning image.  | 
| INPAINTING | inPaintingParams | Editing | Modify an image by changing the inside of a *mask* to match the surrounding background. | 
| OUTPAINTING | outPaintingParams | Editing | Modify an image by seamlessly extending the region defined by the mask. | 
| IMAGE\_VARIATION | imageVariationParams | Editing | Modify an image by producing variations of the original image. | 
| COLOR\_GUIDED\_GENERATION (V2 only) | colorGuidedGenerationParams | Generation | Provide a list of hex color codes along with a text prompt to generate an image that follows the color palette. | 
| BACKGROUND\_REMOVAL (V2 only) | backgroundRemovalParams | Editing | Modify an image by identifying multiple objects and removing the background, outputting an image with a transparent background. | 

Editing tasks require an `image` field in the input. This field consists of a string that defines the pixels in the image. Each pixel is defined by 3 RGB channels, each of which ranges from 0 to 255 (for example, (255 255 0) would represent the color yellow). These channels are encoded in base64.

The image you use must be in JPEG or PNG format.

If you carry out inpainting or outpainting, you also define a *mask*, a Region or Regions that define parts of the image to be modified. You can define the mask in one of two ways.
+ `maskPrompt` – Write a text prompt to describe the part of the image to be masked.
+ `maskImage` – Input a base64-encoded string that defines the masked Regions by marking each pixel in the input image as (0 0 0) or (255 255 255).
  + A pixel defined as (0 0 0) is a pixel inside the mask.
  + A pixel defined as (255 255 255) is a pixel outside the mask.

  You can use a photo editing tool to draw masks. You can then convert the output JPEG or PNG image to base64-encoding to input into this field. Otherwise, use the `maskPrompt` field instead to allow the model to infer the mask.

Select a tab to view API request bodies for different image generation use-cases and explanations of the fields.

------
#### [ Text-to-image generation (Request) ]

A text prompt to generate the image must be <= 512 characters. Resolutions <= 1,408 on the longer side. negativeText (Optional) – A text prompt to define what not to include in the image that is <= 512 characters. See the table below for a full list of resolutions.

```
{
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {
        "text": "string",      
        "negativeText": "string"
    },
    "imageGenerationConfig": {
        "quality": "standard" | "premium",
        "numberOfImages": int,
        "height": int,
        "width": int,
        "cfgScale": float,
        "seed": int
    }
}
```

The `textToImageParams` fields are described below.
+ **text** (Required) – A text prompt to generate the image.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.

------
#### [ Inpainting (Request) ]

text (Optional) – A text prompt to define what to change inside the mask. If you don't include this field, the model tries to replace the entire mask area with the background. Must be <= 512 characters. negativeText (Optional) – A text prompt to define what not to include in the image. Must be <= 512 characters. The size limits for the input image and input mask are <= 1,408 on the longer side of image. The output size is the same as the input size.

```
{
    "taskType": "INPAINTING",
    "inPaintingParams": {
        "image": "base64-encoded string",                         
        "text": "string",
        "negativeText": "string",        
        "maskPrompt": "string",                      
        "maskImage": "base64-encoded string",   
        "returnMask": boolean # False by default                
    },                                                 
    "imageGenerationConfig": {
        "quality": "standard" | "premium",
        "numberOfImages": int,
        "height": int,
        "width": int,
        "cfgScale": float
    }
}
```

The `inPaintingParams` fields are described below. The *mask* defines the part of the image that you want to modify.
+ **image** (Required) – The JPEG or PNG image to modify, formatted as a string that specifies a sequence of pixels, each defined in RGB values and encoded in base64. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ You must define one of the following fields (but not both) to define.
  + **maskPrompt** – A text prompt that defines the mask.
  + **maskImage** – A string that defines the mask by specifying a sequence of pixels that is the same size as the `image`. Each pixel is turned into an RGB value of (0 0 0) (a pixel inside the mask) or (255 255 255) (a pixel outside the mask). For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ **text** (Optional) – A text prompt to define what to change inside the mask. If you don't include this field, the model tries to replace the entire mask area with the background.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.
+ **returnMask** (Optional) – If set to `true`, the response includes the mask image used for the inpainting operation as a base64-encoded string. This is useful for debugging or verifying which area of the image was modified. Default is `false`.

------
#### [ Outpainting (Request) ]

text (Required) – A text prompt to define what to change outside the mask. Must be <= 512 characters. negativeText (Optional) – A text prompt to define what not to include in the image. Must be <= 512 characters. The size limits for the input image and input mask are <= 1,408 on the longer side of image. The output size is the same as the input size. 

```
{
    "taskType": "OUTPAINTING",
    "outPaintingParams": {
        "text": "string",
        "negativeText": "string",        
        "image": "base64-encoded string",                         
        "maskPrompt": "string",                      
        "maskImage": "base64-encoded string",    
        "returnMask": boolean, # False by default                                         
        "outPaintingMode": "DEFAULT | PRECISE"                 
    },                                                 
    "imageGenerationConfig": {
        "quality": "standard" | "premium",
        "numberOfImages": int,
        "height": int,
        "width": int,
        "cfgScale": float
    }
}
```

The `outPaintingParams` fields are defined below. The *mask* defines the Region in the image whose that you don't want to modify. The generation seamlessly extends the Region you define.
+ **image** (Required) – The JPEG or PNG image to modify, formatted as a string that specifies a sequence of pixels, each defined in RGB values and encoded in base64. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ You must define one of the following fields (but not both) to define.
  + **maskPrompt** – A text prompt that defines the mask.
  + **maskImage** – A string that defines the mask by specifying a sequence of pixels that is the same size as the `image`. Each pixel is turned into an RGB value of (0 0 0) (a pixel inside the mask) or (255 255 255) (a pixel outside the mask). For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ **text** (Required) – A text prompt to define what to change outside the mask.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.
+ **outPaintingMode** – Specifies whether to allow modification of the pixels inside the mask or not. The following values are possible.
  + DEFAULT – Use this option to allow modification of the image inside the mask to keep it consistent with the reconstructed background.
  + PRECISE – Use this option to prevent modification of the image inside the mask.
+ **returnMask** (Optional) – If set to `true`, the response includes the mask image used for the outpainting operation as a base64-encoded string. This is useful for debugging or verifying which area of the image was preserved. Default is `false`.

------
#### [ Image variation (Request) ]

Image variation allow you to create variations of your original image based on the parameter values. The size limit for the input image are <= 1,408 on the longer side of image. See the table below for a full list of resolutions. 
+ text (Optional) – A text prompt that can define what to preserve and what to change in the image. Must be <= 512 characters.
+ negativeText (Optional) – A text prompt to define what not to include in the image. Must be <= 512 characters.
+ text (Optional) – A text prompt that can define what to preserve and what to change in the image. Must be <= 512 characters.
+ similarityStrength (Optional) – Specifies how similar the generated image should be to the input image(s) Use a lower value to introduce more randomness in the generation. Accepted range is between 0.2 and 1.0 (both inclusive), while a default of 0.7 is used if this parameter is missing in the request.

```
{
     "taskType": "IMAGE_VARIATION",
     "imageVariationParams": {
         "text": "string",
         "negativeText": "string",
         "images": ["base64-encoded string"],
         "similarityStrength": 0.7,  # Range: 0.2 to 1.0
     },
     "imageGenerationConfig": {
         "quality": "standard" | "premium",
         "numberOfImages": int,
         "height": int,
         "width": int,
         "cfgScale": float
     }
}
```

The `imageVariationParams` fields are defined below.
+ **images** (Required) – A list of images for which to generate variations. You can include 1 to 5 images. An image is defined as a base64-encoded image string. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ **text** (Optional) – A text prompt that can define what to preserve and what to change in the image.
+ **similarityStrength** (Optional) – Specifies how similar the generated image should be to the input images(s). Range in 0.2 to 1.0 with lower values used to introduce more randomness.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.

------
#### [ Conditioned Image Generation (Request) V2 only ]

The conditioned image generation task type allows customers to augment text-to-image generation by providing a “condition image” to achieve more fine-grained control over the resulting generated image.
+ Canny edge detection
+ Segmentation map

Text prompt to generate the image must be <= 512 characters. Resolutions <= 1,408 on the longer side. negativeText (Optional) is a text prompt to define what not to include in the image and is <= 512 characters. See the table below for a full list of resolutions.

```
{
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {
        "text": "string",      
        "negativeText": "string",
        "conditionImage": "base64-encoded string", # [OPTIONAL] base64 encoded image
        "controlMode": "string", # [OPTIONAL] CANNY_EDGE | SEGMENTATION. DEFAULT: CANNY_EDGE
        "controlStrength": float # [OPTIONAL] weight given to the condition image. DEFAULT: 0.7
    },
    "imageGenerationConfig": {
        "quality": "standard" | "premium",
        "numberOfImages": int,
        "height": int,
        "width": int,
        "cfgScale": float,
        "seed": int
    }
}
```
+ **text** (Required) – A text prompt to generate the image.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.
+ **conditionImage** (Optional-V2 only) – A single input conditioning image that guides the layout and composition of the generated image. An image is defined as a base64-encoded image string. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image.
+ **controlMode** (Optional-V2 only) – Specifies that type of conditioning mode should be used. Two types of conditioning modes are supported: CANNY\_EDGE and SEGMENTATION. Default value is CANNY\_EDGE.
+ **controlStrength** (Optional-V2 only) – Specifies how similar the layout and composition of the generated image should be to the conditioningImage. Range in 0 to 1.0 with lower values used to introduce more randomness. Default value is 0.7.

**Note**  
If controlMode or controlStrength are provided, then conditionImage must also be provided.

------
#### [ Color Guided Content (Request) V2 only ]

Provide a list of hex color codes along with a text prompt to generate an image that follows the color palette. A text prompt is required to generate the image must be <= 512 characters. Resolutions maximum is 1,408 on the longer side. A list of 1 to 10 hex color codes are required to specify colors in the generated image, negativeText Optional A text prompt to define what not to include in the image <= 512 characters referenceImage optional an additional reference image to guide the color palette in the generate image. The size limit for user-uploaded RGB reference image is <= 1,408 on the longer side. 

```
{
    "taskType": "COLOR_GUIDED_GENERATION",
    "colorGuidedGenerationParams": {
        "text": "string",      
        "negativeText": "string",
        "referenceImage" "base64-encoded string", # [OPTIONAL]
        "colors": ["string"] # list of color hex codes
    },
    "imageGenerationConfig": {
        "quality": "standard" | "premium",
        "numberOfImages": int,
        "height": int,
        "width": int,
        "cfgScale": float,
        "seed": int
    }
}
```

The colorGuidedGenerationParams fields are described below. Note that this parameter is for V2 only.
+ **text** (Required) – A text prompt to generate the image.
+ **colors** (Required) – A list of up to 10 hex color codes to specify colors in the generated image.
+ **negativeText** (Optional) – A text prompt to define what not to include in the image.
**Note**  
Don't use negative words in the `negativeText` prompt. For example, if you don't want to include mirrors in an image, enter **mirrors** in the `negativeText` prompt. Don't enter **no mirrors**.
+ **referenceImage** (Optional) – A single input reference image that guides the color palette of the generated image. An image is defined as a base64-encoded image string.

------
#### [ Background Removal (Request) ]

The background removal task type automatically identifies multiple objects in the input image and removes the background. The output image has a transparent background. 

**Request format**

```
{
    "taskType": "BACKGROUND_REMOVAL",
    "backgroundRemovalParams": {
        "image": "base64-encoded string"
    }
}
```

**Response format**

```
{
  "images": [
    "base64-encoded string", 
    ...
  ],
  "error": "string" 
}
```

The backgroundRemovalParams field is described below.
+ **image** (Required) – The JPEG or PNG image to modify, formatted as a string that specifies a sequence of pixels, each defined in RGB values and encoded in base64.

------
#### [ Response body ]

```
{
  "images": [
    "base64-encoded string", 
    ...
  ],
  "error": "string" 
}
```

The response body is a streaming object that contains one of the following fields.
+ `images` – If the request is successful, it returns this field, a list of base64-encoded strings, each defining a generated image. Each image is formatted as a string that specifies a sequence of pixels, each defined in RGB values and encoded in base64. For examples of how to encode an image into base64 and decode a base64-encoded string and transform it into an image, see the [code examples](#model-parameters-titan-image-code-examples).
+ `error` – If the request violates the content moderation policy in one of the following situations, a message is returned in this field.
  + If the input text, image, or mask image is flagged by the content moderation policy.
  + If at least one output image is flagged by the content moderation policy

------

The shared and optional `imageGenerationConfig` contains the following fields. If you don't include this object, the default configurations are used.
+ **quality** – The quality of the image. The default value is `standard`. For pricing details, see [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/).
+ **numberOfImages** (Optional) – The number of images to generate.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html)
+ **cfgScale** (Optional) – Specifies how strongly the generated image should adhere to the prompt. Use a lower value to introduce more randomness in the generation.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html)
+ The following parameters define the size that you want the output image to be. For more details about pricing by image size, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).
  + **height** (Optional) – The height of the image in pixels. The default value is 1408.
  + **width** (Optional) – The width of the image in pixels. The default value is 1408.

  The following sizes are permissible.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html)
+ **seed** (Optional) – Use to control and reproduce results. Determines the initial noise setting. Use the same seed and the same settings as a previous run to allow inference to create a similar image.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html)

## Examples
<a name="model-parameters-titan-image-code-examples"></a>

The following examples show how to invoke the Amazon Titan Image Generator models with on-demand throughput in the Python SDK. Select a tab to view an example for each use-case. Each example displays the image at the end.

------
#### [ Text-to-image generation ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an image from a text prompt with the Amazon Titan Image Generator G1 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator G1"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator G1 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator G1 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator G1 example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = 'amazon.titan-image-generator-v1'

    prompt = """A photograph of a cup of coffee from the side."""

    body = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": 0
        }
    })

    try:
        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Inpainting ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use inpainting to generate an image from a source image with 
the Amazon Titan Image Generator G1 model (on demand).
The example uses a mask prompt to specify the area to inpaint.
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator G1"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator G1 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator G1 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator G1 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v1'

        # Read image from file and encode it as base64 string.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "text": "Modernize the windows of the house",
                "negativeText": "bad quality, low res",
                "image": input_image,
                "maskPrompt": "windows"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Outpainting ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use outpainting to generate an image from a source image with 
the Amazon Titan Image Generator G1 model (on demand).
The example uses a mask image to outpaint the original image.
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator G1"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator G1 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator G1 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator G1 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v1'

        # Read image and mask image from file and encode as base64 strings.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')
        with open("/path/to/mask_image", "rb") as mask_image_file:
            input_mask_image = base64.b64encode(
                mask_image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "OUTPAINTING",
            "outPaintingParams": {
                "text": "Draw a chocolate chip cookie",
                "negativeText": "bad quality, low res",
                "image": input_image,
                "maskImage": input_mask_image,
                "outPaintingMode": "DEFAULT"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0
            }
        }
        )

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Image variation ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an image variation from a source image with the
Amazon Titan Image Generator G1 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator G1"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator G1 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator G1 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator G1 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator G1 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v1'

        # Read image from file and encode it as base64 string.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "IMAGE_VARIATION",
            "imageVariationParams": {
                "text": "Modernize the house, photo-realistic, 8k, hdr",
                "negativeText": "bad quality, low resolution, cartoon",
                "images": [input_image],
		"similarityStrength": 0.7,  # Range: 0.2 to 1.0
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator G1 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Image conditioning (V2 only) ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate image conditioning from a source image with the
Amazon Titan Image Generator G1 V2 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator V2"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator V2 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator V2 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator V2 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator V2 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v2:0'

        # Read image from file and encode it as base64 string.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": "A robot playing soccer, anime cartoon style",
                "negativeText": "bad quality, low res",
                "conditionImage": input_image,
                "controlMode": "CANNY_EDGE"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator V2 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Color guided content (V2 only) ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an image from a source image color palette with the
Amazon Titan Image Generator G1 V2 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator V2"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator V2 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator V2 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator V2 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator V2 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v2:0'

        # Read image from file and encode it as base64 string.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "COLOR_GUIDED_GENERATION",
            "colorGuidedGenerationParams": {
                "text": "digital painting of a girl, dreamy and ethereal, pink eyes, peaceful expression, ornate frilly dress, fantasy, intricate, elegant, rainbow bubbles, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration",
                "negativeText": "bad quality, low res",
                "referenceImage": input_image,
                "colors": ["#ff8080", "#ffb280", "#ffe680", "#ffe680"]
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator V2 model {model_id}.")


if __name__ == "__main__":
    main()
```

------
#### [ Background removal (V2 only) ]

```
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an image with background removal with the
Amazon Titan Image Generator G1 V2 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator V2"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator V2 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator V2 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator V2 model %s", model_id)

    return image_bytes


def main():
    """
    Entrypoint for Amazon Titan Image Generator V2 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v2:0'

        # Read image from file and encode it as base64 string.
        with open("/path/to/image", "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": input_image,
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

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
            f"Finished generating image with Amazon Titan Image Generator V2 model {model_id}.")


if __name__ == "__main__":
    main()
```

------