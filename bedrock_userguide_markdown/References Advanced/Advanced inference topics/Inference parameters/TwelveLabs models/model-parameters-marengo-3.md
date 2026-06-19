

# TwelveLabs Marengo Embed 3.0
<a name="model-parameters-marengo-3"></a>

The TwelveLabs Marengo Embed 3.0 model generates enhanced embeddings from video, text, audio, image, or multi-input (text with multiple images) inputs. This latest version offers improved performance and accuracy for similarity search, clustering, and other machine learning tasks.
+ Provider — TwelveLabs
+ Model ID — twelvelabs.marengo-embed-3-0-v1:0

Marengo Embed 3.0 delivers several key enhancements:
+ **Extended video processing capacity** – Process up to 4 hours of video and audio content. Files can be up to 6 GB, which is double the capacity of previous versions. This makes it ideal for analyzing full sporting events, extended training videos, and complete film productions.
+ **Enhanced sports analysis** – The model delivers significant improvements. It provides better understanding of gameplay dynamics, player movements, and event detection.
+ **Global multilingual support** – Expanded language capabilities from 12 to 36 languages. This enables global organizations to build unified search and retrieval systems that work seamlessly across diverse regions and markets.
+ **Multimodal search precision** – Combine images and descriptive text in a single embedding request. This merges visual similarity with semantic understanding to deliver more accurate and contextually relevant search results.
+ **Reduced embedding dimension** – Reduced from 1024 to 512, which can help reduce storage costs.

The TwelveLabs Marengo Embed 3.0 model supports the Amazon Bedrock Runtime operations in the following table. 
+ For more information about use cases for different API methods, see [Making inference requests](inference.md).
+ For more information about model types, see [Making inference requests](inference.md).
  + For a list of model IDs and to see the models and AWS Regions that TwelveLabs Marengo Embed 3.0 is supported in, search for the model in the table at [Supported foundation models in Amazon Bedrock](models-supported.md).
  + For a full list of inference profile IDs, see [Supported Regions and models for inference profiles](inference-profiles-support.md). The inference profile ID is based on the AWS Region.


****  

| API operation | Supported model types | Input modalities | Output modalities | 
| --- | --- | --- | --- | 
| InvokeModel | US East (N. Virginia) – [Base models](models-supported.md) and [Inference profiles](inference-profiles-support.md)<br />Europe (Ireland) – [Inference profiles](inference-profiles-support.md)<br />Asia Pacific (Seoul) - [Base models](models-supported.md) | Text<br />Image<br />Multi-input (text with multiple images)<br />**Note:** Text and image interleaved is also supported. | Embedding | 
| StartAsyncInvoke | US East (N. Virginia) – [Base models](models-supported.md)<br />Europe (Ireland) – [Base models](models-supported.md)<br />Asia Pacific (Seoul) - [Base models](models-supported.md) | Video<br />Audio<br />Image<br />Text<br />Multi-input (text with multiple images)<br />**Note:** Text and image interleaved is also supported. | Embedding | 

**Note**  
Use `InvokeModel` to generate embeddings for search query. Use `StartAsyncInvoke` to generate embeddings for assets at a large scale.

The following quotas apply to the input:


****  

| Input modality | Maximum | 
| --- | --- | 
| Text | 500 tokens | 
| Image | 5 MB per image | 
| Video (S3) | 6 GB, 4 hour length | 
| Audio (S3) | 6 GB, 4 hour length | 

**Note**  
If you define audio or video inline by using base64-encoding, make sure that the request body payload doesn't exceed the Amazon Bedrock 25 MB model invocation quota.

## Migrate from TwelveLabs Marengo Embed 2.7 to TwelveLabs Marengo Embed 3.0
<a name="model-parameters-marengo-3-migration"></a>

**Important**  
TwelveLabs Marengo Embed 2.7 will be deprecated. Embeddings that you created with TwelveLabs Marengo Embed 2.7 are NOT compatible with TwelveLabs Marengo Embed 3.0. You must regenerate all embeddings with TwelveLabs Marengo Embed 3.0.

To migrate from TwelveLabs Marengo Embed 2.7 to TwelveLabs Marengo Embed 3.0, complete the following steps.

1. Update your code to use the new nested input structure and parameter changes described in the following section.

1. Update the model ID to `twelvelabs.marengo-embed-3-0-v1:0`.

1. Test your integration with the new version.

The following are the key changes between TwelveLabs Marengo Embed 2.7 and TwelveLabs Marengo Embed 3.0.
+ **Nested input structure** – Input parameters are now organized inside objects based on the `inputType` value. For example, if `inputType` is `text`, nest `inputText` within a `text` object.
+ **Combined text and image inputs** – A new `text_image` input type allows you to combine text and image in a single request. This input type is not supported in TwelveLabs Marengo Embed 2.7.
+ **Parameter changes** – The `embeddingOption` parameter values changed:
  + TwelveLabs Marengo Embed 2.7: `visual-text`, `visual-image`, `audio`
  + TwelveLabs Marengo Embed 3.0: `visual`, `audio`, `transcription`

The following examples show the structural changes for text input.

**TwelveLabs Marengo Embed 2.7 (flat structure)**

```
{
    "inputType": "text",
    "inputText": "{{your-text}}",
    "embeddingOption": "visual-text"
}
```

**TwelveLabs Marengo Embed 3.0 (nested structure)**

```
{
    "inputType": "text",
    "text": {
        "inputText": "{{your-text}}"
    },
    "embeddingOption": "visual"
}
```

The following examples show the structural changes for media inputs (image, video, or audio).

**TwelveLabs Marengo Embed 2.7 (flat structure)**

```
{
    "inputType": "{{image|video|audio}}",
    "mediaSource": {
        "s3Location": {
            "bucketName": "{{your-bucket}}",
            "objectKey": "{{your-key}}"
        }
    },
    "embeddingOption": "{{visual-image|audio}}"
}
```

**TwelveLabs Marengo Embed 3.0 (nested structure)**

```
{
    "inputType": "{{image|video|audio}}",
    "{{image|video|audio}}": {
        "mediaSource": {
            "s3Location": {
                "bucketName": "{{your-bucket}}",
                "objectKey": "{{your-key}}"
            }
        }
    },
    "embeddingOption": "{{visual|audio|transcription}}"
}
```

**Topics**
+ [Migrate from TwelveLabs Marengo Embed 2.7 to TwelveLabs Marengo Embed 3.0](#model-parameters-marengo-3-migration)
+ [TwelveLabs Marengo Embed 3.0 request parameters](#model-parameters-marengo-3-async-request)
+ [TwelveLabs Marengo Embed 3.0 response](#model-parameters-marengo-3-response)
+ [TwelveLabs Marengo Embed 3.0 code examples](#model-parameters-marengo-3-examples)

## TwelveLabs Marengo Embed 3.0 request parameters
<a name="model-parameters-marengo-3-async-request"></a>

When you make a request, the field in which the model-specific input is specified depends on the API operation:
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) – In the request `body`.
+ [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) – In the `modelInput` field of the request body.

The format of the model input depends on the input modality:

------
#### [ Text ]

```
{
    "inputType": "text",
    "text": {
        "inputText": "{{string}}"
    }
}
```

------
#### [ Image ]

```
{
  "inputType": "image",
  "image": {
    "mediaSource": {
      "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
      "s3Location": {
        "uri": "s3://{{amzn-s3-demo-bucket}}/folder/dog.jpg",
        "bucketOwner": "{{123456789012}}"
      }
    }
  }
}
```

------
#### [ Text & image ]

```
{
  "inputType": "text_image",
  "text_image": {
    "inputText": "man walking a dog",
    "mediaSource": {
      "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
      "s3Location": {
        "uri": "s3://{{amzn-s3-demo-bucket}}/folder/dog.jpg",
        "bucketOwner": "{{123456789012}}"
      }
    }
  }
}
```

------
#### [ Audio ]

```
{
  "inputType": "audio",
  "audio": {
    "mediaSource": {
      "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
      "s3Location": {
        "uri": "s3://{{amzn-s3-demo-bucket}}/audio/a.wav",
        "bucketOwner": "{{123456789012}}"
      }
    },
    "startSec": 0,
    "endSec": 6,
    "segmentation": {
      "method": "fixed", 
      "fixed": {
        "durationSec": 6
      }
    },
    "embeddingOption": [
      "audio",
      "transcription"
    ], // optional, default=both
    "embeddingType": [
      "separate_embedding"
    ], // optional, default=["separate_embedding"]
    "embeddingScope": [
      "clip",
      "asset"
    ] // optional, one or both
  }
}
```

------
#### [ Video ]

```
{
  "inputType": "video",
  "video": {
    "mediaSource": {
      "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
      "s3Location": {
        "uri": "s3://{{amzn-s3-demo-bucket}}/video/clip.mp4",
        "bucketOwner": "{{123456789012}}"
      }
    },
    "startSec": 0,
    "endSec": 6,
    "segmentation": {
      "method": "dynamic", // dynamic OR fixed, exactly one
      "dynamic": {
        "minDurationSec": 4
      }
      "method": "fixed",
      "fixed": {
        "durationSec": 6
      }
    },
    "embeddingOption": [
      "visual",
      "audio", 
      "transcription"
    ], // optional, default=all
    "embeddingType": [
      "separate_embedding"
    ], // optional, default=["separate_embedding"]
    "embeddingScope": [
      "clip",
      "asset"
    ] // optional, one or both
  }
}
```

------
#### [ Multi-input ]

```
{
  "inputType": "multi_input",
  "multi_input": {
    "inputText": "<@img1> walking a dog with <@img2>", // optional
    "mediaSources": [
      {
        "name": "img1", // required if inputText uses <@name> placeholders
        "mediaType": "image",
        "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
        "s3Location": {
          "uri": "s3://{{amzn-s3-demo-bucket}}/images/person.jpg",
          "bucketOwner": "{{123456789012}}"
        }
      },
      {
        "name": "img2",
        "mediaType": "image",
        "base64String": "{{base64-encoded string}}", // base64String OR s3Location, exactly one
        "s3Location": {
          "uri": "s3://{{amzn-s3-demo-bucket}}/images/dog.jpg",
          "bucketOwner": "{{123456789012}}"
        }
      }
    ]
  }
}
```

------

Expand the following sections for details about the input parameters:

### inputType
<a name="model-parameters-marengo-3-inputType"></a>

Modality for the embedding.
+ **Type:** String
+ **Required:** Yes
+ **Valid values:** `text` \| `image` \| `text_image` \| `audio` \| `video` \| `multi_input`

### inputText
<a name="model-parameters-marengo-3-inputText"></a>

Text to be embedded.
+ **Type:** String
+ **Required:** Yes (for compatible input types)
+ **Compatible input types:** Text

### mediaSource
<a name="model-parameters-marengo-3-mediaSource"></a>

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
<a name="model-parameters-marengo-3-embeddingOption"></a>

Specifies which types of embeddings to retrieve.
+ **Type:** List
+ **Required:** No
+ **Valid values for list members:**
  + `visual` – Visual embeddings from the video.
  + `audio` – Embeddings of the audio in the video.
  + `transcription` – Embeddings of the transcribed text.
+ **Default value:**
  + Video: ["visual", "audio", "transcription"]
  + Audio: ["audio", "transcription"]
+ **Compatible input types:** Video, Audio

### embeddingScope
<a name="model-parameters-marengo-3-embeddingScope"></a>

Specifies the scope of the embeddings to retrieve.
+ **Type:** List
+ **Required:** No
+ **Valid values for list members:**
  + `clip` – Returns embeddings for each clip.
  + `asset` – Returns embeddings for the entire asset.
+ **Compatible input types:** Video, Audio

### startSec
<a name="model-parameters-marengo-3-startSec"></a>

The time point in seconds of the clip where processing should begin.
+ **Type:** Double
+ **Required:** No
+ **Minimum value:** 0
+ **Default value:** 0
+ **Compatible input types:** Video, Audio

### endSec
<a name="model-parameters-marengo-3-endSec"></a>

The time point in seconds where processing should end.
+ **Type:** Double
+ **Required:** No
+ **Minimum value:** startSec \+ segment length
+ **Maximum value:** Duration of media
+ **Default value:** Duration of media
+ **Compatible input types:** Video, Audio

### segmentation
<a name="model-parameters-marengo-3-segmentation"></a>

Defines how the media is divided into segments for embedding generation.
+ **Type:** Object
+ **Required:** No
+ **Compatible input types:** Video, Audio

The segmentation object contains a `method` field and method-specific parameters:
+ `method` – The segmentation method to use. Valid values: `dynamic` \| `fixed`
+ `dynamic` – For video, uses shot boundary detection to divide content dynamically. Contains:
  + `minDurationSec` – Minimum duration for each segment in seconds. Type: Integer. Range: 1-5. Default: 4.
+ `fixed` – Divides content into segments of equal duration. Contains:
  + `durationSec` – Duration of each segment in seconds. Type: Integer. Range: 1-10. Default: 6.

**Default behavior:**
+ Video: Uses dynamic segmentation with shot boundary detection.
+ Audio: Uses fixed segmentation. Content is divided as evenly as possible with segments close to 10 seconds.

### multi\_input
<a name="model-parameters-marengo-3-multi-input"></a>

Contains the multi-input configuration for combining text with multiple images in a single embedding request. Use this input type when you want to create embeddings that capture the relationship between text and multiple images.
+ **Type:** Object
+ **Required:** Yes (when `inputType` is `multi_input`)

The `multi_input` object contains the following fields:
+ `inputText` – (Optional) Text query with placeholder syntax. Use `<@name>` to reference media sources (for example, `"<@img1> walking with <@img2>"`). If provided with placeholders, each `<@name>` must match a `mediaSources[].name`. Maximum: 500 tokens including placeholders.
+ `mediaSources` – (Required) Array of media source objects. Each media source contains image data. The array must contain at least one item.
  + `name` – (Conditional) Unique identifier for this media source. Required only if `inputText` uses `<@name>` placeholders. When provided, must match a placeholder in `inputText` (without the `<@` and `>` characters).
  + `mediaType` – (Required) Type of media. Currently only `"image"` is supported.
  + `base64String` – Base64-encoded image payload. Maximum: 5 MB per image. Provide exactly one of `base64String` or `s3Location`.
  + `s3Location` – S3 location object containing `uri` (S3 URI) and `bucketOwner` (12-digit AWS account ID). Maximum: 5 MB per image. Provide exactly one of `base64String` or `s3Location`.

**Media ordering:**
+ If `inputText` contains `<@name>` placeholders, the order is determined by placeholder order in `inputText`.
+ If `inputText` is omitted or empty, the order defaults to the array order of `mediaSources`.

### embeddingType
<a name="model-parameters-marengo-3-embeddingType"></a>

Controls how embeddings are aggregated across modalities.
+ **Type:** List
+ **Required:** No
+ **Valid values for list members:**
  + `separate_embedding` – Returns embeddings for each modality separately (visual, audio, transcription).
  + `fused_embedding` – Returns a weighted fusion of multiple embedding modalities.
+ **Default value:** ["separate\_embedding"]
+ **Compatible input types:** Video, Audio

**Constraints:**
+ For video: `fused_embedding` requires at least 2 embedding types in `embeddingOption`.
+ For audio: `fused_embedding` requires both `audio` and `transcription` in `embeddingOption`.

### inferenceId
<a name="model-parameters-marengo-3-inferenceId"></a>

Unique identifier for the inference request.
+ **Type:** String
+ **Required:** No

## TwelveLabs Marengo Embed 3.0 response
<a name="model-parameters-marengo-3-response"></a>

The location of the output embeddings and associated metadata depends on the invocation method:
+ InvokeModel – In the response body.
+ StartAsyncInvoke – In the S3 bucket defined in `s3OutputDataConfig`, after the asynchronous invocation job completes.

If there are multiple embeddings vectors, the output is a list of objects, each containing a vector and its associated metadata.

The format of the output embeddings vector is as follows:

```
{
  "data": {
    "embedding": [
    0.111, 0.234, ...
    ],
    "embeddingOption": ["visual", "audio", "transcription", "fused" (for video input) | "audio", "transcription", "fused" (for audio input)],
    "embeddingScope": ["asset" | "clip"],
    "startSec": 0,
    "endSec": 4.2
  }
}
```

The embeddings are returned as an array of floats.

Where you see this response depends on the API method you used:
+ InvokeModel – Appears in the response body.
+ StartAsyncInvoke – Appears at the S3 location that you specified in the request. The response returns an `invocationArn`. You can use this to get metadata about the asynchronous invocation. This includes the status and the S3 location where the results are written.

Expand the following sections for details about the response parameters:

### embedding
<a name="model-parameters-marengo-3-embedding"></a>

Embeddings vector representation of input.
+ **Type:** List of doubles

### embeddingOption
<a name="model-parameters-marengo-3-embeddingOption-response"></a>

The type of embeddings.
+ **Type:** String
+ **Possible values:**
  + visual – Visual embeddings from the video.
  + audio – Embeddings of the audio in the video.
  + transcription – Embeddings of the transcribed text.
  + fused – Weighted fusion of multiple embedding types. Only returned when `embeddingType` includes `"fused_embedding"` in the request.
+ **Compatible input types:** Video, Audio

**Note**  
Not applicable for text, image, text\_image, and multi\_input input types. These return a single embedding without the `embeddingOption` field.

### embeddingScope
<a name="model-parameters-marengo-3-embeddingScope"></a>

Specifies the scope of the embeddings to retrieve.
+ **Type:** String

You can include one or more of the following values:
+ clip: Returns embeddings for each clip.
+ asset: Returns embeddings for the entire asset.

### startSec
<a name="model-parameters-marengo-3-startSec-response"></a>

The start offset of the clip.
+ **Type:** Double
+ **Compatible input types:** Video, Audio

### endSec
<a name="model-parameters-marengo-3-endSec-response"></a>

The end offset of the clip. Not applicable for text, image, text\_image, and multi\_input embeddings.
+ **Type:** Double
+ **Compatible input types:** Video, Audio

## TwelveLabs Marengo Embed 3.0 code examples
<a name="model-parameters-marengo-3-examples"></a>

This section shows how to use the TwelveLabs Marengo Embed 3.0 model with different input types using Python. The examples demonstrate how to define model-specific input and run model invocations.

**Note**  
InvokeModel supports text, image, multi-input, and text with image interleaved input. For video and audio input, use StartAsyncInvoke.

Put your code together in the following steps:

**1. Define model-specific input**  
Define the model-specific input depending on your input type:

------
#### [ Text ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"

model_input = {
    "inputType": "text",
    "text": {
        "inputText": "man walking a dog"
    }
}
```

------
#### [ Image ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"

model_input = {
    "inputType": "image",
    "image": {
        "mediaSource": {
            "s3Location": {
                "uri": "s3://{{amzn-s3-demo-bucket}}/my_image.png",
                "bucketOwner": "{{123456789012}}"
            }
        }
    }
}
```

------
#### [ Text & image ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"

model_input = {
    "inputType": "text_image",
    "text_image": {
        "inputText": "man walking a dog",
        "mediaSource": {
            "s3Location": {
                "uri": "s3://{{amzn-s3-demo-bucket}}/my_image.jpg",
                "bucketOwner": "{{123456789012}}"
            }
        }
    }
}
```

------
#### [ Audio ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"
 
model_input = {
    "inputType": "audio",
    "audio": {
        "mediaSource": {  
            "s3Location": { 
                "uri": "s3://{{amzn-s3-demo-bucket}}/my-audio.wav", 
                "bucketOwner": "{{123456789012}}" 
            }
        },
        "startSec": 0,
        "endSec": 5,
        "segmentation": {
            "method": "fixed",
            "fixed": {
                "durationSec": 5
            }
        },
        "embeddingScope": ["clip", "asset"],
        "embeddingOption": ["audio", "transcription"],
        "embeddingType": ["separate_embedding", "fused_embedding"]
    }
}
```

------
#### [ Video ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"
 
model_input = {
    "inputType": "video",
    "video": {
        "mediaSource": {
            "s3Location": {
                "uri": "s3://{{amzn-s3-demo-bucket}}/my-video.mp4",
                "bucketOwner": "{{123456789012}}"
            }
        },
        "startSec": 10,
        "endSec": 20,
        "segmentation": {
            "method": "fixed",
            "fixed": {
                "durationSec": 5
            }
        },
        "embeddingOption": [
            "visual", 
            "audio"
        ],
        "embeddingType": ["separate_embedding", "fused_embedding"],
        "embeddingScope": [
            "clip",
            "asset"
        ]
    }
}
```

------
#### [ Multi-input ]

```
# Create the model-specific input
model_id = "twelvelabs.marengo-embed-3-0-v1:0"
# Replace the us prefix depending on your region
inference_profile_id = "us.twelvelabs.marengo-embed-3-0-v1:0"

model_input = {
    "inputType": "multi_input",
    "multi_input": {
        "inputText": "<@img1> walking a dog with <@img2>",
        "mediaSources": [
            {
                "name": "img1",
                "mediaType": "image",
                "s3Location": {
                    "uri": "s3://{{amzn-s3-demo-bucket}}/images/person.jpg",
                    "bucketOwner": "{{123456789012}}"
                }
            },
            {
                "name": "img2",
                "mediaType": "image",
                "s3Location": {
                    "uri": "s3://{{amzn-s3-demo-bucket}}/images/dog.jpg",
                    "bucketOwner": "{{123456789012}}"
                }
            }
        ]
    }
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
                "s3Uri": "s3://amzn-s3-demo-bucket"
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