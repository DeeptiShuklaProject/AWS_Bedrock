

# Stability AI Image Services
<a name="stable-image-services"></a>

You can use Stability AI Image Services with Amazon Bedrock to access thirteen specialized image editing tools designed to accelerate professional creative workflows. With Stability AI Image Services you can generate images from a sketch, restructure and restyle an existing image, or remove and replace objects within an image.

This section describes how to make inference calls to Stability AI Image Services using the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html). This section also provides code examples in Python and examples of images before and after using Stability AI Image Services.

Stability AI Image Services are available in the following categories:
+ **Edit** ‐ AI-based image editing services, including inpainting with masks (generative fill), or with words. Includes tools for product placement and advertising, as well as basic tools such as background removal.
+ **Control** ‐ May take prompts, maps and other guides. These services use ControlNets and similar technologies built on Stable Diffusion models.

**Note**  
Subscribing to any edit or control Stability AI Image Service automatically enrolls you in all thirteen available Stability AI Image Services.

**Topics**
+ [Request and response](#model-parameters-stable-image-services-request-response)
+ [Upscale](#stable-image-services-upscale)
+ [Edit](#stable-image-services-edit)
+ [Control](#stable-image-services-control)

## Request and response
<a name="model-parameters-stable-image-services-request-response"></a>

The request body is passed in the `body` field of a request to [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html). 

**Model invocation request body field**

When you make an InvokeModel call using Stability AI Image Services, fill the body field with a JSON object that looks like the following. 

```
{
    'prompt': 'Create an image of a panda'
}
```

**Model invocation responses body field**

When you make an InvokeModel call using Stability AI Image Services, the response looks like the following 

```
{
    'seeds': [2130420379], 
    'finish_reasons': [null], 
    'images': ['...']
}
```
+ **seeds** – (string) List of seeds used to generate images for the model.
+ **finish\_reasons** – Enum indicating whether the request was filtered or not. `null` will indicate that the request was successful. Current possible values: `"Filter reason: prompt", "Filter reason: output image", "Filter reason: input image", "Inference error", null`.
+ **images** – A list of generated images in base64 string format.

For more information, see [https://platform.us.stability.ai/docs/api-reference\#tag/v1generation](https://platform.us.stability.ai/docs/api-reference#tag/v1generation).

## Upscale
<a name="stable-image-services-upscale"></a>

The following section describes the upscale Stability AI Image Services.

### Creative Upscale
<a name="stable-image-services-5"></a>

Creative Upscale takes images between 64x64 and 1 megapixel and upscales them to 4K resolution. This service can upscale images by 20 to 40 times while preserving and often enhancing quality. Creative Upscale works best on highly degraded images and is not for photos of 1 megapixel or above as it performs heavy reimagining.

Creative Upscale has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image to upscale. Every side of the image must be at least 64 pixels. Total pixel count must be between 4,096 and 1,048,576 pixels. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **creativity** ‐ (number) Indicates how creative the model should be when upscaling an image. Higher values will result in more details being added to the image during upscaling. Range between 0.1 and 0.5. Default 0.3
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **style\_preset** ‐ Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-creative-upscale-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London",
        "creativity": 0.30
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-creative-upscale-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London",
        "creativity": 0.30
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Creative Upscale operation using the following prompt: *This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-creative-upscale.jpg)  |  ![Big Ben clock tower showing ornate golden details and white clock faces against cloudy sky.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-creative-upscale.jpg)  | 

### Conservative Upscale
<a name="stable-image-services-6"></a>

Conservative Upscale takes images between 64x64 and 1 megapixel and upscale them to 4K resolution. This service can upscale images by 20 to 40 times while preserving all aspects. Conservative Upscale minimizes alterations to the image and should not be used to reimagine an image.

Conservative Upscale has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image to upscale. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **creativity** ‐ (number) Indicates how creative the model should be when upscaling an image. Higher values will result in more details being added to the image during upscaling. Range between 0.1 and 0.5. Default 0.35
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-conservative-upscale-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London",
        "creativity": 0.30
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-conservative-upscale-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London",
        "creativity": 0.30
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Conservative Upscale operation using the following prompt: *This dreamlike digital art captures a vibrant, kaleidoscopic Big Ben in London*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-conservative-upscale.jpg)  |  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-conservative-upscale.jpg)  | 

### Fast Upscale
<a name="stable-image-services-7"></a>

Fast Upscale enhances image resolution by 4 times using predictive and generative AI. This lightweight and fast service is ideal for enhancing the quality of compressed images, making it suitable for social media posts and other applications.

Fast upscale has the following required parameters:
+ **image** ‐ (string) The Base64 image to upscale. Width must be between 32 and 1,536 pixels. Height must be between 32 and 1,536 pixels. Total pixel count must be between 1,024 and 1,048,576 pixels. Supported formats: jpeg, png, webp.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-fast-upscale-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-fast-upscale-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Fast Upscale operation.


|  Input  |  Output  | 
| --- | --- | 
|  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-fast-upscale.jpg)  |  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-fast-upscale.jpg)  | 

## Edit
<a name="stable-image-services-edit"></a>

The following section describes the edit Stability AI Image Services.

### Inpaint
<a name="stable-image-services-8"></a>

Inpaint intelligently modifies images by filling in or replacing specified areas with new content based on the content of a mask image.

Inpaint has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image to inpaint. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **style\_preset** ‐ (string) Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **mask** ‐ (string) Controls the strength of the inpainting process on a per-pixel basis, either via a second image (passed into this parameter) or via the alpha channel of the image parameter.
  + **Passing in a Mask** ‐ The image passed to this parameter should be a black and white image that represents, at any pixel, the strength of inpainting based on how dark or light the given pixel is. Completely black pixels represent no inpainting strength while completely white pixels represent maximum strength. In the event the mask is a different size than the image parameter, it will be automatically resized.
  + **Alpha Channel Support** ‐ If you don't provide an explicit mask, one will be derived from the alpha channel of the image parameter. Transparent pixels will be inpainted while opaque pixels will be preserved. In the event an image with an alpha channel is provided along with a mask, the mask will take precedence.
+ **grow\_mask** ‐ Grows the edges of the mask outward in all directions by the specified number of pixels. The expanded area around the mask will be blurred, which can help smooth the transition between inpainted content and the original image. Range between 0 and 20. Default 5. Try this parameter if you notice seams or rough edges around the inpainted content. Note that excessive growth may obscure fine details in the mask and/or merge nearby masked regions.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.png"
mask = "./content/mask.png"

region = "us-east-1"
model_id = "us.stability.stable-image-inpaint-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    with open(mask, "rb") as mask_file:
        mask_base64 = base64.b64encode(mask_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "mask": mask_base64,
        "prompt": "artificer of time and space"
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png"
mask = "./content/mask.png"

region = "us-east-1"
model_id = "us.stability.stable-image-inpaint-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    with open(mask, "rb") as mask_file:
        mask_base64 = base64.b64encode(mask_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "mask": mask_base64,
        "prompt": "artificer of time and space"
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of an Inpaint operation.


|  Input  |  Mask  |  Output  | 
| --- | --- | --- | 
|  ![Man in blue three-piece suit standing outdoors at night with city skyline in background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-image-inpaint.jpg)  |  ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/mask-image-inpaint.png)  |  ![Person wearing futuristic armor with glowing blue elements against city skyline at night.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-image-inpaint.jpg)  | 

### Outpaint
<a name="stable-image-services-9"></a>

Outpaint inserts additional content in an image to fill in the space in any direction. Compared to other automated or manual attempts to expand the content in an image, the Outpaint service minimizes indications that the original image has been edited.

Outpaint has the following required parameters:
+ **image** ‐ (string) The Base64 image to outpaint. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.
**Note**  
At least one outpaint direction: (left, right, up, or down) must be supplied with a non-zero value. For best quality results, consider the composition and content of your original image when choosing outpainting directions.

The following parameters are optional:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **style\_preset** ‐ (string) Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **creativity** ‐ (number) Indicates how creative the model should be when outpainting an image. Higher values will result in more creative content being added to the image during outpainting. Range between 0.1 and 1.0. Default 0.5.
+ **left** ‐ (integer) The number of pixels to outpaint on the left side of the image. At least one outpainting direction must be supplied with a non-zero value. Range 0 to 2000. Detault 0.
+ **right** ‐ (integer) The number of pixels to outpaint on the right side of the image. At least one outpainting direction must be supplied with a non-zero value. Range 0 to 2000. Detault 0.
+ **up** ‐ (integer) The number of pixels to outpaint on the top of the image. At least one outpainting direction must be supplied with a non-zero value. Range 0 to 2000. Detault 0.
+ **down** ‐ (integer) The number of pixels to outpaint on the bottom of the image. At least one outpainting direction must be supplied with a non-zero value. Range 0 to 2000. Detault 0.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-outpaint-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "left": 512,
        "right": 512,
        "up": 200,
        "down": 100
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-outpaint-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "left": 512,
        "right": 512,
        "up": 200,
        "down": 100
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of an Outpaint operation.


|  Input  |  Output  | 
| --- | --- | 
|  ![Big Ben clock tower showing ornate Gothic architecture with illuminated clock faces.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-image-outpaint.jpg)  |  ![Big Ben clock tower with ornate Gothic architecture against cloudy sky.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-image-outpaint.jpg)  | 

### Search and Recolor
<a name="stable-image-services-10"></a>

Search and Recolor allows you to change the color of a specific object in an image using a prompt. This service is a specific version of inpainting that does not require a mask. It will automatically segment the object and recolor it using the colors requested in the prompt.

Search and Recolor has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image to recolor. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.
+ **select\_prompt** ‐ (string) Short description of what to search for in the image. Maximum 10000 characters.

The following parameters are optional:
+ **style\_preset** ‐ (string) Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **grow\_mask** ‐ Grows the edges of the mask outward in all directions by the specified number of pixels. The expanded area around the mask will be blurred, which can help smooth the transition between inpainted content and the original image. Range between 0 and 20. Default 5. Try this parameter if you notice seams or rough edges around the inpainted content. Note that excessive growth may obscure fine details in the mask and/or merge nearby masked regions.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-search-recolor-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "pink jacket",
        "select_prompt": "jacket"
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)

    base64_image_data = model_response["images"][0]
    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-search-recolor-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "pink jacket",
        "select_prompt": "jacket"
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Search and Recolor operation using the following prompt: *pink jacket*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Person wearing sunglasses and blue puffer jacket with backpack in snowy mountain setting.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-search-recolor.jpg)  |  ![Person wearing sunglasses and purple winter jacket with backpack in snowy mountain setting.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-search-recolor.jpg)  | 

### Search and Replace
<a name="stable-image-services-11"></a>

Search and Replace allows you to use a search prompt to identify an object in simple language to be replaced. The service will automatically segment the object and replace it with the object requested in the prompt without requiring a mask.

Search and Replace has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image to recolor. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.
+ **search\_prompt** ‐ (string) Short description of what to inpaint in the image. Maximum 10000 characters.

The following parameters are optional:
+ **style\_preset** ‐ (string) Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **grow\_mask** ‐ Grows the edges of the mask outward in all directions by the specified number of pixels. The expanded area around the mask will be blurred, which can help smooth the transition between inpainted content and the original image. Range between 0 and 20. Default 5. Try this parameter if you notice seams or rough edges around the inpainted content. Note that excessive growth may obscure fine details in the mask and/or merge nearby masked regions.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-search-replace-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "jacket",
        "search_prompt": "sweater",
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-search-replace-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "jacket",
        "search_prompt": "sweater",
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")
    image_data = base64.b64decode(base64_image_data)

    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Search and Replace operation using the following prompt: *jacket*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Woman wearing orange sweater outdoors with autumn foliage in background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-search-replace.jpg)  |  ![Woman wearing olive jacket and white shirt outdoors with autumn foliage in background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-search-replace.jpg)  | 

### Erase
<a name="stable-image-services-12"></a>

Erase allows you to remove unwanted elements using image masks, while intelligently maintaining background consistency.

Erase has the following required parameters:
+ **image** ‐ (string) The Base64 image to erase from. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **mask** ‐ (string) Controls the strength of the inpainting process on a per-pixel basis, either via a second image (passed into this parameter) or via the alpha channel of the image parameter.
  + **Passing in a Mask** ‐ The image passed to this parameter should be a black and white image that represents, at any pixel, the strength of inpainting based on how dark or light the given pixel is. Completely black pixels represent no inpainting strength while completely white pixels represent maximum strength. In the event the mask is a different size than the image parameter, it will be automatically resized.
  + **Alpha Channel Support** ‐ If you don't provide an explicit mask, one will be derived from the alpha channel of the image parameter. Transparent pixels will be inpainted while opaque pixels will be preserved. In the event an image with an alpha channel is provided along with a mask, the mask will take precedence.
+ **grow\_mask** ‐ Grows the edges of the mask outward in all directions by the specified number of pixels. The expanded area around the mask will be blurred, which can help smooth the transition between inpainted content and the original image. Range between 0 and 20. Default 5. Try this parameter if you notice seams or rough edges around the inpainted content. Note that excessive growth may obscure fine details in the mask and/or merge nearby masked regions.

**Note**  
For optimal erase results, ensure your mask accurately defines the areas to be removed. If no explicit mask is provided, the service will use the alpha channel of the input image. The mask will take precedence if both are provided.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.png"
mask = "./content/mask.png"

region = "us-east-1"
model_id = "us.stability.stable-image-erase-object-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8'),
    with open(mask, "rb") as mask_file:
        mask_base64 = base64.b64encode(mask_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "mask": mask_base64
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png" 
mask = "./content/mask.png"

region = "us-east-1"
model_id = "us.stability.stable-image-erase-object-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8'),
    with open(mask, "rb") as mask_file:
        mask_base64 = base64.b64encode(mask_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "mask": mask_base64
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of an Erase operation.


|  Input  |  Mask  |  Output  | 
| --- | --- | --- | 
|  ![Overhead view of organized desk with laptop, open notebooks, pens, and plant on wooden surface.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-erase-object.jpg)  |  ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/mask-erase-object.png)  |  ![Overhead view of organized desk with laptop, open notebooks, pencils, and blue journals.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-erase-object.jpg)  | 

### Remove Background
<a name="stable-image-services-13"></a>

Remove Background allows you to isolate subjects from the background with precision.

Remove Background has the following required parameters:
+ **image** ‐ (string) The Base64 image to remove the background from. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-remove-background-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.png"

region = "us-east-1"
model_id = "us.stability.stable-image-remove-background-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")

    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Remove Background operation.


|  Input  |  Output  | 
| --- | --- | 
|  ![Woman wearing orange sweater outdoors with autumn foliage in background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-remove-background.jpg)  |  ![Person wearing orange knit sweater against background with horizontal stripes.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-remove-background.jpg)  | 

## Control
<a name="stable-image-services-control"></a>

The following section describes the control Stability AI Image Services.

### Control Sketch
<a name="stable-image-services-1"></a>

Upgrade rough hand-drawn sketches to refined outputs with precise control. For non-sketch images, Control Sketch allows detailed manipulation of the final appearance by using the contour lines and edges within the image.

Control Sketch has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image of the sketch. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **control\_strength** ‐ (number) How much influence, or control, the image has on the generation. Represented as a float between 0 and 1, where 0 is the least influence and 1 is the maximum. Default 0.7.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **style\_preset** ‐ Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-control-sketch-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "a house with background of mountains and river flowing nearby"
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-control-sketch-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "a house with background of mountains and river flowing nearby"
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Control Sketch call using the following prompt: *a house with background of mountains and river flowing nearby*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Simple line drawing of a house on a hillside with mountains in the background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-control-sketch.jpg)  |  ![Mountain valley with river, green meadows, traditional building, and snow-capped peaks.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-control-sketch.jpg)  | 
|   |  | 

### Control Structure
<a name="stable-image-services-2"></a>

Control Structure allows you to generate images while maintaining the structure of an input image. This is especially valuable for advanced content creation scenarios such as recreating scenes or rendering characters from models.

Control Structure has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image of the sketch. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **control\_strength** ‐ (number) How much influence, or control, the image has on the generation. Represented as a float between 0 and 1, where 0 is the least influence and 1 is the maximum. Default 0.7.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **style\_preset** ‐ Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-control-structure-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "surreal structure with motion generated sparks lighting the scene"

    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-control-structure-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "surreal structure with motion generated sparks lighting the scene"

    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Control Structure operation using the following prompt: *surreal structure with motion generated sparks lighting the scene*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Tunnel-like structure with latticed metal framework creating striped light patterns on floor.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-control-structure.jpg)  |  ![Tunnel interior with illuminated brick pattern and sparks flying at the opening.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-control-structure.jpg)  | 

### Style Guide
<a name="stable-image-services-3"></a>

Style Guide allows you to extract stylistic elements from an input image and use it to guide the creation of an output image based on the prompt. The result is a new image in the same style as the input image.

Style Guide has the following required parameters:
+ **prompt** ‐ What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue. Minimum 0 and Maximum 10000 characters.
+ **image** ‐ (string) The Base64 image of the sketch. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **aspect\_ratio** ‐ (string) Controls the aspect ratio of the generated image. This parameter is only valid for text-to-image requests. Default 1:1. Enum: 16:9, 1:1, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21. Default 1:1.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **fidelity** ‐ (number) How closely the output image's style resembles the input image's style. Range 0 to 1. Default 0.5.
+ **style\_preset** ‐ Guides the image model towards a particular style. Enum: 3d-model, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, photographic, pixel-art, tile-texture.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-style-guide-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "wide shot of modern metropolis" 
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/input.jpg"

region = "us-east-1"
model_id = "us.stability.stable-image-style-guide-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        "image": image_base64,
        "prompt": "wide shot of modern metropolis" 
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Style Guide call using the following prompt: *wide shot of modern metropolis*.


|  Input  |  Output  | 
| --- | --- | 
|  ![Abstract painting with vibrant colors including blue, yellow, green, orange, and red brushstrokes.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-style-guide.jpg)  |  ![Colorful abstract cityscape with buildings in blue, yellow, green, orange, and red tones.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-style-guide.jpg)  | 

### Style Transfer
<a name="stable-image-services-4"></a>

Style Transfer allows you to apply visual characteristics from reference style images to target images. While the Style Guide service extracts stylistic elements from an input image and uses them to guide the creation of an output image based on the prompt, Style Transfer specifically transforms existing content while preserving the original composition. This tool helps create consistent content across multiple assets.

Style Transfer has the following required parameters:
+ **init\_image** ‐ (string) A Base64 image containing the subject you wish to restyle. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.
+ **style\_image** ‐ (string) A Base64 image containing the subject you wish to restyle. Every side of the image must be at least 64 pixels. The total pixel count cannot exceed 9,437,184 pixels. Image aspect ratio must be between 1:2.5 and 2.5:1. Supported formats: jpeg, png, webp.

The following parameters are optional:
+ **prompt** ‐ (string) What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value. A value 0 and 1.0 de-emphasized the word and a value between 1.1 and 2 emphasized the word . For example: The sky was a crisp (blue:0.3) and (green:1.8) would convey a sky that was blue and green, but more green than blue.
+ **negative\_prompt** ‐ (string) A blurb of text describing what you do not wish to see in the output image. This is an advanced feature. Maximum 10000 characters.
+ **seed** ‐ (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range 0 to 4294967294. Default 0.
+ **output\_format** ‐ (string) Dictates the content-type of the generated image. Enum: jpeg, png, webp. Default png.
+ **composition\_fidelity** ‐ (number) How closely the output image's style resembles the input image's style. Range between 0 and 1. Default 0.9.
+ **style\_strength** ‐ (number) Sometimes referred to as denoising, this parameter controls how much influence the style\_image parameter has on the generated image. A value of 0 would yield an image that is identical to the input. A value of 1 would be as if you passed in no image at all. Range between 0 and 1. Default 1.
+ **change\_strength** ‐ (number) How much the original image should change. Range between 0.1 and 1. Default 0.9.

------
#### [ API ]

```
import base64
import json
import requests
import io
import os
from PIL import Image

image = "./content/input.jpg"
style_image = "./content/style.jpg"

region = "us-east-1"
model_id = "us.stability.stable-style-transfer-v1:0"
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"
api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK") # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-keys.html
headers = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    with open(style_image, "rb") as style_image_file:
        style_image_base64 = base64.b64encode(style_image_file.read()).decode('utf-8')

    params = {
        "init_image": image_base64,
        "style_image": style_image_base64,
        "prompt": "statue"
    }
    response = requests.request("POST", url, json=params, headers=headers)
    response.raise_for_status()
    model_response = json.loads(response.text)
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------
#### [ Python ]

```
import boto3
import base64
import io
import json
from PIL import Image

image = "./content/cat_statue_512x512.jpg"
style_image = "./content/glowbot_style.jpg"

region = "us-east-1"
model_id = "us.stability.stable-style-transfer-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=region)

try:
    with open(image, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    with open(style_image, "rb") as style_image_file:
        style_image_base64 = base64.b64encode(style_image_file.read()).decode('utf-8')

    params = {
        "init_image": image_base64,
        "style_image": style_image_base64,
        "prompt": "statue"
    }
    request = json.dumps(params)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]

    if not base64_image_data:
        raise ValueError("No image data found in model response.")

    image_data = base64.b64decode(base64_image_data)
    image = Image.open(io.BytesIO(image_data))
    image.save("image.png")
    print("Successfully saved image.")

except Exception as e:
    print(e)
```

------

The following table shows the input and output images of a Style Transfer call.


|  Input  |  Style  |  Output  | 
| --- | --- | --- | 
|  ![Marble statue of a woman with flowing hair and draped clothing, hand raised to head.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/input-style-transfer.jpg)  |  ![Network of illuminated blue lines connecting buildings in a nighttime cityscape.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/style-style-transfer.jpg)  |  ![Classical statue with cyan lighting in urban setting with modern architecture in background.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/stable-image-services/output-style-transfer.jpg)  | 