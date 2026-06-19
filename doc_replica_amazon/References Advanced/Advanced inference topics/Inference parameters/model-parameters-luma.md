

# Luma AI models
<a name="model-parameters-luma"></a>

This section describes the request parameters and response fields for Luma AI models. Use this information to make inference calls to Luma AI models with the [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) operation. This section also includes Python code examples that shows how to call Luma AI models. To use a model in an inference operation, you need the model ID for the model. 
+ Model ID: luma.ray-v2:0
+ Model Name: Luma Ray 2
+ Text to Video Model

Luma AI models process model prompts asynchronously by using the Async APIs including [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html), [GetAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GetAsyncInvoke.html), and [ListAsyncInvokes](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ListAsyncInvokes.html).

Luma AI model processes prompts using the following steps. 
+ The user prompts the model using [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html).
+ Wait until the InvokeJob is finished. You can use `GetAsyncInvoke` or `ListAsyncInvokes` to check the job completion status.
+ The model output will be placed in the specified output Amazon S3 bucket

For more information using the Luma AI models with the APIs, see [Video Generation](https://docs.lumalabs.ai/docs/video-generation).

Luma AI inference call. 

```
POST /async-invoke HTTP/1.1
Content-type: application/json
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "your input text here",
    "aspect_ratio": "16:9",
    "loop": false,
    "duration": "5s",
    "resolution": "720p"
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

**Fields**
+ **prompt** – (string) The content needed in the output video (1 <= length <= 5000 characters).
+ **aspect\_ratio** – (enum) The aspect ratio of the output video ("1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21").
+ **loop** – (boolean) Whether to loop the output video.
+ **duration** – (enum) - The duration of the output video ("5s", "9s").
+ **resolution** – (enum) The resolution of the output video ("540p", "720p").

The MP4 file will be stored in the Amazon S3 bucket as configured in the response.

## Text-to-Video Generation
<a name="luma-text-to-video"></a>

Generate videos from text prompts using the Luma Ray 2 model. The model supports various customization options including aspect ratio, duration, resolution, and looping.

**Basic Text-to-Video Request**

```
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "an old lady laughing underwater, wearing a scuba diving suit"
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

**Advanced Text-to-Video with Options**

```
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "an old lady laughing underwater, wearing a scuba diving suit",
    "aspect_ratio": "16:9",
    "loop": true,
    "duration": "5s",
    "resolution": "720p"
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

**Additional Text-to-Video Example**

Example with resolution and duration parameters.

```
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "a car",
    "resolution": "720p",
    "duration": "5s"
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

## Image-to-Video Generation
<a name="luma-image-to-video"></a>

Transform static images into dynamic videos by providing keyframes. You can specify start frames, end frames, or both to control the video generation process.

**Basic Image-to-Video with Start Frame**

```
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "A tiger walking in snow",
    "keyframes": {
      "frame0": {
        "type": "image",
        "source": {
          "type": "base64",
          "media_type": "image/jpeg",
          "data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3"
        }
      }
    }
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

**Image-to-Video with Start and End Frames**

```
{
  "modelId": "luma.ray-v2:0",
  "modelInput": {
    "prompt": "A tiger walking in snow",
    "keyframes": {
      "frame0": {
        "type": "image",
        "source": {
          "type": "base64",
          "media_type": "image/jpeg",
          "data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3"
        }
      },
      "frame1": {
        "type": "image",
        "source": {
          "type": "base64",
          "media_type": "image/jpeg",
          "data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3"
        }
      }
    },
    "loop": false,
    "aspect_ratio": "16:9"
  },
  "outputDataConfig": {
    "s3OutputDataConfig": {
      "s3Uri": "s3://your-bucket-name"
    }
  }
}
```

**Additional Parameters for Image-to-Video**
+ **keyframes** – (object) Define start (frame0) and/or end (frame1) keyframes
  + **frame0** – Starting keyframe image
  + **frame1** – Ending keyframe image
  + **type** – Must be "image"
  + **source** – Image source

## Troubleshooting
<a name="luma-troubleshooting"></a>

Common issues and solutions when working with Luma AI models:
+ **Job Status "Failed"** - Check that your S3 bucket has proper write permissions and the bucket exists in the same region as your Bedrock service.
+ **Image URL Access Errors** - Ensure image URLs are publicly accessible and use HTTPS. Images must be in supported formats (JPEG, PNG).
+ **Invalid Parameter Errors** - Verify aspect ratio values match supported options ("1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21") and duration is either "5s" or "9s".
+ **Timeout Issues** - Use `GetAsyncInvoke` to check job status rather than waiting synchronously. Video generation can take several minutes.
+ **Prompt Length Errors** - Keep prompts between 1-5000 characters. Longer prompts will be rejected.

## Performance Notes
<a name="luma-performance"></a>

Important considerations for Luma AI model performance and limitations:
+ **Processing Time** - Video generation typically takes 2-5 minutes for 5-second videos and 4-8 minutes for 9-second videos, depending on complexity.
+ **Image Requirements** - Input images should be high quality with minimum resolution of 512x512 pixels. Maximum supported image size is 4096x4096 pixels.
+ **Output Video Size** - Generated videos range from 5-50 MB depending on duration, resolution, and content complexity.
+ **Rate Limits** - Async API calls are subject to service quotas. Monitor your usage and request quota increases if needed.
+ **S3 Storage** - Ensure sufficient S3 storage capacity for output videos and consider lifecycle policies for cost optimization.

## Related Documentation
<a name="luma-cross-references"></a>

For additional information and related services:
+ **Amazon S3 Configuration** - [Creating S3 buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) and [bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html) for output storage.
+ **Async API Operations** - [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html), [GetAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GetAsyncInvoke.html), and [ListAsyncInvokes](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ListAsyncInvokes.html) API reference.
+ **Service Quotas** - [Quotas for Amazon Bedrock](quotas.md) for Bedrock service limits and quota increase requests.
+ **Video Processing Best Practices** - [Making inference requests](inference.md) for general model inference guidance.
+ **Luma AI Documentation** - [Luma Labs Video Generation Documentation](https://docs.lumalabs.ai/docs/video-generation) for detailed model capabilities and advanced features.