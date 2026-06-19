

# Stability.ai Stable Diffusion 3.5 Large
<a name="model-parameters-diffusion-3-5-large"></a>

The Stable Diffusion 3.5 Large model uses 8 billion parameters and supports 1 megapixel resolution output for text-to-image and image-to-image generation.

The request body is passed in the `body` field of a request to [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html). 

**Model invocation request body field**

When you make an InvokeModel call using a Stable Diffusion 3.5 Large model, fill the body field with a JSON object that looks like the following.
+ **prompt** – (string) Text description of the desired output image. Maximum 10,000 characters.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)

**Model invocation responses body field**

When you make an `InvokeModel` call using a Stable Diffusion 3.5 Large model, the response looks like the following

```
{
    'seeds': [2130420379], 
    "finish_reasons":[null], 
    "images":["..."]
}
```

A response with a finish reason that is not `null`, will look like the following:

```
{
    "finish_reasons":["Filter reason: prompt"]
}
```
+ **seeds** – (string) List of seeds used to generate images for the model.
+ **finish\_reasons** – Enum indicating whether the request was filtered or not. `null` will indicate that the request was successful. Current possible values: `"Filter reason: prompt", "Filter reason: output image", "Filter reason: input image", "Inference error", null`.
+ **images** – A list of generated images in base64 string format.

------
#### [ Text to image ]

The Stability.ai Stable Diffusion 3.5 Large model has the following inference parameters for a text-to-image inference call.
+ **prompt** (string) – Text description of the desired output image. Maximum 10,000 characters.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)

**Optional parameters**
+ **aspect\_ratio** (string) – Controls the aspect ratio of the generated image. Valid for text-to-image requests only. Enum: 16:9, 1:1, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21. Default 1:1.
+ **mode** (string) (GenerationMode) - Default: text-to-image. Enum: image-to-image or text-to-image. Controls whether this is a text-to-image or image-to-image generation, which affects which parameters are required:
  + text-to-image requires only the prompt parameter.
  + image-to-image requires the prompt, image, and strength parameters.
+ **seed** (number) – Value to control randomness in generation. Range 0 to 4294967294. Default 0 (random seed).    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **negative\_prompt** (string) – Text describing elements to exclude from the output image. Maximum 10,000 characters.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **output\_format** (string) – Output image format. Enum: jpeg, png, webp. Default png.

```
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
response = bedrock.invoke_model(
    modelId='stability.sd3-5-large-v1:0',
    body=json.dumps({
        'prompt': 'A car made out of vegetables.'
    })
)
```

------
#### [ Image to image ]

The Stability.ai Stable Diffusion 3.5 Large model has the following inference parameters for an image-to-image inference call.
+ **prompt** (string) – Text description of the desired output image. Maximum 10,000 characters.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **image** (string) – Base64-encoded input image. Minimum 64 pixels per side. Supported formats: jpeg, png, webp.
+ **mode** (string) (GenerationMode) - Default: text-to-image. Enum: image-to-image or text-to-image. Controls whether this is a text-to-image or image-to-image generation, which affects which parameters are required:
  + text-to-image requires only the prompt parameter.
  + image-to-image requires the prompt, image, and strength parameters.
+ **strength** (number) – Controls influence of the input image on the output. Range 0 to 1. Value of 0 preserves the input image, value of 1 ignores the input image.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **seed** (number) – Value to control randomness in generation. Range 0 to 4294967294. Default 0 (random seed).    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **negative\_prompt** (string) – Text describing elements to exclude from the output image. Maximum 10,000 characters.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-3-5-large.html)
+ **output\_format** (string) – Output image format. Enum: jpeg, png, webp. Default png.

```
import boto3
import base64
import json

# Load and encode image
with open('input_image.jpg', 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
response = bedrock.invoke_model(
    modelId='stability.sd3-5-large-v1:0',
    body=json.dumps({
        'prompt': 'A car made out of vegetables.',
        'image': image_base64,
        'strength': 0.7
    })
)
```

------