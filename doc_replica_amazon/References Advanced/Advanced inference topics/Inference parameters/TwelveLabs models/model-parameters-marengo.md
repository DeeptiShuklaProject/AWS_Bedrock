

# TwelveLabs Marengo Embed 2.7
<a name="model-parameters-marengo"></a>

The TwelveLabs Marengo Embed 2.7 model generates embeddings from video, text, audio, or image inputs. These embeddings can be used for similarity search, clustering, and other machine learning tasks.
+ Provider — TwelveLabs
+ Model ID — twelvelabs.marengo-embed-2-7-v1:0

The TwelveLabs Marengo Embed 2.7 model supports the Amazon Bedrock Runtime operations in the following table. 
+ For more information about use cases for different API methods, see [Making inference requests](inference.md).
+ For more information about model types, see [Making inference requests](inference.md).
  + For a list of model IDs and to see the models and AWS Regions that TwelveLabs Marengo Embed 2.7 is supported in, search for the model in the table at [Supported foundation models in Amazon Bedrock](models-supported.md).
  + For a full list of inference profile IDs, see [Supported Regions and models for inference profiles](inference-profiles-support.md). The inference profile ID is based on the AWS Region.


****  

| API operation | Supported model types | Input modalities | Output modalities | 
| --- | --- | --- | --- | 
| InvokeModel | [Inference profiles](inference-profiles-support.md) | Text<br />Image | Embedding | 
| StartAsyncInvoke | [Base models](models-supported.md) | Video<br />Audio<br />Image<br />Text | Embedding | 

**Note**  
Use `InvokeModel` to generate embeddings for search query. Use `StartAsyncInvoke` to generate embeddings for assets at a large scale.

The following quotas apply to the input:


****  

| Input modality | Maximum | 
| --- | --- | 
| Text | 77 tokens | 
| Image | 5 MB | 
| Video (S3) | 2 GB | 
| Audio (S3) | 2 GB | 

**Note**  
If you define audio or video inline by using base64-encoding, make sure that the request body payload doesn't exceed the Amazon Bedrock 25 MB model invocation quota.

**Topics**
+ [TwelveLabs Marengo Embed 2.7 request parameters](#model-parameters-marengo-async-request)
+ [TwelveLabs Marengo Embed 2.7 response](#model-parameters-marengo-response)
+ [TwelveLabs Marengo Embed 2.7 code examples](#model-parameters-marengo-examples)

## TwelveLabs Marengo Embed 2.7 request parameters
<a name="model-parameters-marengo-async-request"></a>

When you make a request, the field in which the model-specific input is specified depends on the API operation:
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) – In the request `body`.
+ [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) – In the `modelInput` field of the request body.

The format of the model input depends on the input modality:

------
#### [ Text ]

```
{
    "inputType": "text",
    "inputText": "{{string}}",
    "textTruncate": "{{string}}
}
```

------
#### [ Inline image ]

```
{
     "inputType": "image",
     "mediaSource": {
          "base64String": "{{base64-encoded string}}"
     }
}
```

------
#### [ S3 image ]

```
{
    "inputType": "image",
    "mediaSource": {
        "s3Location": {
            "uri": "{{string}}",
            "bucketOwner": "{{string}}"
        }
    }
}
```

------
#### [ Inline video ]

```
{
    "inputType": "video",
    "mediaSource": {
        "s3Location": {
            "base64String": "{{base64-encoded string}}"
        }
    },
    "startSec": {{double}},
    "lengthSec": {{double}},
    "useFixedLengthSec": {{double}},
    "embeddingOption": "visual-text" | "visual-image" | "audio"
}
```

------
#### [ S3 video ]

```
{
    "inputType": "image",
    "mediaSource": {
        "s3Location": {
           "uri": "{{string}}",
           "bucketOwner": "{{string}}"
        }
    },
    "startSec": {{double}},
    "lengthSec": {{double}},
    "useFixedLengthSec": {{double}},
    "minClipSec": {{int}},
    "embeddingOption": ["{{string}}"]
}
```

------
#### [ Inline audio ]

```
{
    "inputType": "audio", 
    "mediaSource": { 
        "base64String": "{{base64-encoded string}}"
    },
    "startSec": {{double}},
    "lengthSec": {{double}},
    "useFixedLengthSec": {{double}}
}
```

------
#### [ S3 audio ]

```
{
    "inputType": "audio",
    "mediaSource": {
        "s3Location": {
           "uri": "{{string}}",
           "bucketOwner": "{{string}}"
        }
    },
    "startSec": {{double}},
    "lengthSec": {{double}},
    "useFixedLengthSec": {{double}}
}
```

------

Expand the following sections for details about the input parameters:

### inputType
<a name="model-parameters-marengo-inputType"></a>

Modality for the embedding.
+ **Type:** String
+ **Required:** Yes
+ **Valid values:** `video` \| `text` \| `audio` \| `image`

### inputText
<a name="model-parameters-marengo-inputText"></a>

Text to be embedded.
+ **Type:** String
+ **Required:** Yes (for compatible input types)
+ **Compatible input types:** Text

### textTruncate
<a name="model-parameters-marengo-textTruncate"></a>

Specifies how the platform truncates text.
+ **Type:** String
+ **Required:** No
+ **Valid values:**
  + `end` – Truncates the end of the text.
  + `none` – Returns an error if the text exceeds the limit
+ **Default value:** end
+ **Compatible input types:** Text

### mediaSource
<a name="model-parameters-marengo-mediaSource"></a>

Contains information about the media source.
+ **Type:** Object
+ **Required:** Yes (if compatible type)
+ **Compatible input types:** Image, Video, Audio

The format of the `mediaSource` object in the request body depends on whether the media is defined as a Base64-encoded string or as an S3 location.
+ **Base64-encoded string**

  ```
  {
      "mediaSource": {
          "base64String": "base64-encoded string"
      }
  }
  ```
  + `base64String` – The Base64-encoded string for the media.
+ **S3 location** – Specify the S3 URI and the bucket owner.

  ```
  {
      "s3Location": {
          "uri": "string",
          "bucketOwner": "string"
      }
  }
  ```
  + `uri` – The S3 URI containing the media.
  + `bucketOwner` – The AWS account ID of the S3 bucket owner.

### embeddingOption
<a name="model-parameters-marengo-embeddingOption"></a>

Specifies which types of embeddings to retrieve.
+ **Type:** List
+ **Required:** No
+ **Valid values for list members:**
  + `visual-text` – Visual embeddings optimized for text search.
  + `visual-image` – Visual embeddings optimized for image search.
  + `audio` – Embeddings of the audio in the video.
+ **Default value:** ["visual-text", "visual-image", "audio"]
+ **Compatible input types:** Video, Audio

### startSec
<a name="model-parameters-marengo-startSec"></a>

The time point in seconds of the clip where processing should begin.
+ **Type:** Double
+ **Required:** No
+ **Minimum value:** 0
+ **Default value:** 0
+ **Compatible input types:** Video, Audio

### lengthSec
<a name="model-parameters-marengo-lengthSec"></a>

The time in seconds, counting from the `startSec` time point, after which processing should stop.
+ **Type:** Double
+ **Required:** No
+ **Valid values:** 0 - Duration of media
+ **Default value:** Duration of media
+ **Compatible input types:** Video, Audio

Example:
+ startSec: 5
+ lengthSec: 20
+ Result: The clip is processed from 0:05 to 0:25 (5 seconds \+ 20 seconds).

### useFixedLengthSec
<a name="model-parameters-marengo-useFixedLengthSec"></a>

The duration of each clip for which the model should generate an embedding.
+ **Type:** Double
+ **Required:** No
+ **Value parameters:** 2 - 10. Must be greater than or equal to `minClipSec`.
+ **Default value:** Depends on the type of media:
  + **Video:** Divided dynamically by shot boundary detection.
  + **Audio:** Divided evenly with segments as close to 10 seconds as possible.

    Examples:
    + A 50-second clip is divided into 5 10-second segments.
    + A 16-second clip is divided into 2 8-second segments.
+ **Compatible input types:** – Video, Audio
+ **Notes:** Must be greater than or equal to `minClipSec`.

### minClipSec
<a name="model-parameters-marengo-minClipSec"></a>

Sets a minimum value for each clip in seconds.
+ **Type:** int
+ **Required:** No
+ **Value parameters:** Range: 1-5
+ **Default value:** 4
+ **Compatible input types:** Video
+ **Notes:** Must be less than or equal to `useFixedLengthSec`.

## TwelveLabs Marengo Embed 2.7 response
<a name="model-parameters-marengo-response"></a>

The location of the output embeddings and associated metadata depends on the invocation method:
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) – In the response body.
+ [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) – In the S3 bucket defined in the `s3OutputDataConfig`, after the asynchronous invocation job completes.

If there are multiple embeddings vectors, the output is a list of objects, each containing a vector and its associated metadata.

The format of the output embeddings vector is as follows:

```
{
    "embedding": ["{{string}}"],
    "embeddingOption": "visual-text" | "visual-image" | "audio",
    "startSec": {{double}},
    "endsec": {{double}}
}
```

Expand the following sections for details about the response parameters:

### embedding
<a name="model-parameters-marengo-embedding"></a>

Embeddings vector representation of input.
+ **Type:** List of doubles

### embeddingOption
<a name="model-parameters-marengo-embeddingOption"></a>

The type of embeddings.
+ **Type:** String
+ **Possible values:**
  + `visual-text` – Visual embeddings optimized for text search.
  + `visual-image` – Visual embeddings optimized for image search.
  + `audio` – Embeddings of the audio in the video.
+ **Compatible input types:** Video

### startSec
<a name="model-parameters-marengo-startSec"></a>

The start offset of the clip.
+ **Type:** Double
+ **Compatible input types:** Video, Audio

### endSec
<a name="model-parameters-marengo-endSec"></a>

The end offset of the clip, in seconds.
+ **Type:** Double
+ **Compatible input types:** Video, Audio

## TwelveLabs Marengo Embed 2.7 code examples
<a name="model-parameters-marengo-examples"></a>

This section shows how to use the TwelveLabs Marengo Embed 2.7 model with different input types using Python. The examples demonstrate how to define model-specific input and run model invocations.

**Note**  
InvokeModel supports text and image input only. For video and audio input, use StartAsyncInvoke.

Put your code together in the following steps:

**1. Define model-specific input**  
Define the model-specific input depending on your input type:

------
#### [ Text ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"
                            
model_input = {
  "inputType": "text",
  "inputText": "man walking a dog"
}
```

------
#### [ Inline image ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
   "inputType": "image",
   "mediaSource": {
      "base64String": "example-base64-image"
   }
}
```

------
#### [ S3 image ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
     "inputType": "image",
     "mediaSource": {
          "s3Location": {
               "uri": "s3://amzn-s3-demo-bucket/my_image.png",
               "bucketOwner": "123456789012"
          }
     }
}
```

------
#### [ Inline video ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
    "inputType": "video",
    "mediaSource": {
        "base64String": "base_64_encoded_string_of_video"
    },
    "startSec": 0,
    "lengthSec": 13,
    "useFixedLengthSec": 5,
    "embeddingOption": [
        "visual-text", 
        "audio"
    ]
}
```

------
#### [ S3 video ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
    "inputType": "video",
    "mediaSource": {
        "s3Location": {
            "uri": "amzn-s3-demo-bucket/my-video.mp4",
            "bucketOwner": "123456789012"
        }
    },
    "startSec": 0,
    "lengthSec": 13,
    "useFixedLengthSec": 5,
    "embeddingOption": [
        "visual-text", 
        "audio"
    ]
}
```

------
#### [ Inline audio ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
    "inputType": "audio", 
    "mediaSource": { 
        "base64String": "base_64_encoded_string_of_audio"
    },
    "startSec": 0,
    "lengthSec": 13,
    "useFixedLengthSec": 10
}
```

------
#### [ S3 audio ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-2-7-v1:0"
# Replace the {{us}} prefix depending on your region
inference_profile_id = "{{us}}.twelvelabs.marengo-embed-2-7-v1:0"

model_input = {
    "inputType": "audio",
    "mediaSource": {  
        "s3Location": { 
            "uri": "s3://amzn-s3-demo-bucket/my-audio.wav", 
            "bucketOwner": "123456789012" 
        }
    },
    "startSec": 0,
    "lengthSec": 13,
    "useFixedLengthSec": 10
}
```

------

**2. Run model invocation using the model input**  
Then, add the code snippet that corresponds to your model invocation method of choice.

------
#### [ InvokeModel ]

```
# Run model invocation with InvokeModel
import boto3
import json

# Initialize the Bedrock Runtime client
client = boto3.client('bedrock-runtime')

# Make the request
response = client.invoke_model(
    modelId=inference_profile_id,
    body=json.dumps(model_input)
)

# Print the response body
response_body = json.loads(response['body'].read().decode('utf-8'))

print(response_body)
```

------
#### [ StartAsyncInvoke ]

```
# Run model invocation asynchronously
import boto3
import json

# Initalize the Bedrock Runtime client.
client = boto3.client("bedrock-runtime")

try:
    # Start the asynchronous job
    invocation = client.start_async_invoke(
        modelId=model_id,
        modelInput=model_input,
        outputDataConfig={
            "s3OutputDataConfig": {
                "s3Uri": "s3://&example-s3-destination-bucket;"
            }
        }
    )

    # Print the response JSON
    print("Response:")
    print(json.dumps(invocation, indent=2, default=str))

except Exception as e:
    # Implement error handling here.
    message = e.response["Error"]["Message"]
    print(f"Error: {message}")
```

------