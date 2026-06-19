

# Stable Image Core request and response
<a name="model-parameters-diffusion-stable-image-core-text-image-request-response"></a>

The request body is passed in the `body` field of a request to [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html). 

**Model invocation request body field**

When you make an InvokeModel call using a Stability AI Stable Diffusion Stable Image Core model, fill the body field with a JSON object that looks like the following. 

```
{
        'prompt': 'Create an image of a panda'
    }
```

**Model invocation responses body field**

When you make an InvokeModel call using a Stability AI Stable Diffusion Stable Image Core model, the response looks like the following 

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

------
#### [ Text to image ]

The Stable Image Core model has the following inference parameters for a text to image inference call. 

 **prompt** (Required) – (string) What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results.


| Minimum | Maximum | 
| --- | --- | 
| 0 | 10,000 characters | 

**Optional fields**
+ **aspect\_ratio** – (string) Controls the aspect ratio of the generated image. This parameter is only valid for text-to-image requests. Default 1:1. Enum: 16:9, 1:1, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21.
+ **output\_format** – Specifies the format of the output image. Supported formats: JPEG, PNG. Supported dimensions: height 640 to 1,536 px, width 640 to 1,536 px.
+ **seed** – (number) A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.) Range: 0 to 4294967295.
+ **negative\_prompt** – Keywords of what you do not wish to see in the output image. Max: 10.000 characters.

```
     import boto3
     import json
     import base64
     import io
     from PIL import Image
     
     bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
     response = bedrock.invoke_model(
         modelId='stability.stable-image-core-v1:1',
         body=json.dumps({
             'prompt': 'A car made out of vegetables.'
         })
     )
     output_body = json.loads(response["body"].read().decode("utf-8"))
     base64_output_image = output_body["images"][0]
     image_data = base64.b64decode(base64_output_image)
     image = Image.open(io.BytesIO(image_data))
     image.save("image.png")
```

------