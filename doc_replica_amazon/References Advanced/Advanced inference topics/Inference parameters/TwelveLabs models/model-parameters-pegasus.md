

# TwelveLabs Pegasus 1.2
<a name="model-parameters-pegasus"></a>

The TwelveLabs Pegasus 1.2 model provides comprehensive video understanding and analysis capabilities. It can analyze video content and generate textual descriptions, insights, and answers to questions about the video.

Use this information to make inference calls to TwelveLabs models with the InvokeModel, InvokeModelWithResponseStream (streaming) operations.
+ Provider — TwelveLabs
+ Categories — Video understanding, content analysis
+ Model ID — `twelvelabs.pegasus-1-2-v1:0`
+ Input modality — Video
+ Output modality — Text
+ Max video size — 1 hour long video (< 2GB file size)

## TwelveLabs Pegasus 1.2 request parameters
<a name="model-parameters-pegasus-request"></a>

The following table describes the input parameters for the TwelveLabs Pegasus 1.2 model:


**TwelveLabs Pegasus 1.2 request parameters**  

| Field | Type | Required | Description | 
| --- | --- | --- | --- | 
| inputPrompt | string | Yes | Prompt to analyze the video. Max: 2000 tokens. | 
| temperature | double | No | Temperature for the model. Controls randomness in the output. Default: 0.2, Min: 0, Max: 1. | 
| responseFormat | Object | No | Lets users specify the structured output format. Currently supports json\_schema only. | 
| mediaSource | object | Yes | Describes the media source. Either base64String or s3Location must be provided. | 
| mediaSource.base64String | string | No | Base64 encoded byte string for the video. Max: 25MB. | 
| mediaSource.s3Location.uri | string | No | S3 URI where the video could be downloaded from. Max: 1 hour long video (< 2GB file size). | 
| mediaSource.s3Location.bucketOwner | string | No | AWS account ID of the bucket owner. | 
| maxOutputTokens | integer | No | The maximum number of tokens to generate. Max: 4096. | 

## TwelveLabs Pegasus 1.2 response fields
<a name="model-parameters-pegasus-response"></a>

The following table describes the output fields for the TwelveLabs Pegasus 1.2 model:


**TwelveLabs Pegasus 1.2 response fields**  

| Field | Type | Description | 
| --- | --- | --- | 
| message | string | Output message containing the model's analysis of the video. | 
| finishReason | string | Stop reason that describes why the output ended. Valid values: stop (API returned the full completions without reaching any limits), length (the generation exceeded the max\_tokens limit). | 

## TwelveLabs Pegasus 1.2 request and response
<a name="model-parameters-pegasus-examples"></a>

The following examples show how to use the TwelveLabs Pegasus 1.2 model with different input sources.

------
#### [ Request ]

The following examples show request formats for the TwelveLabs Pegasus 1.2 model.

**Using base64 encoded video:**

```
{
  "inputPrompt": "tell me about the video",
  "mediaSource": {
      "base64String": "<BASE64 STRING OF VIDEO FILE>"
  },
  "temperature": 0
}
```

**Using S3 stored video:**

```
{
    "inputPrompt": "Tell me about this video",
    "mediaSource": {
        "s3Location": {
            "uri": "s3://path-to-video-object-in-s3",
            "bucketOwner": "bucket-owner-account-id"
        }
    },
    "temperature": 0
}
```

**Using structured output format:**

```
{
    "inputPrompt": "Analyze this video and provide a structured summary",
    "mediaSource": {
        "s3Location": {
            "uri": "s3://path-to-video-object-in-s3",
            "bucketOwner": "bucket-owner-account-id"
        }
    },
    "temperature": 0.2,
    "maxOutputTokens": 2048,
    "responseFormat": {
        "type": "json_schema",
        "jsonSchema": {
            "name": "video_analysis",
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "key_scenes": {"type": "array", "items": {"type": "string"}},
                    "duration": {"type": "string"}
                },
                "required": ["summary", "key_scenes"]
            }
        }
    }
}
```

------
#### [ Response ]

The following examples show response formats from the TwelveLabs Pegasus 1.2 model.

**Standard response:**

```
{
  "message": "This video shows a person walking through a park during sunset. The scene includes trees, a walking path, and golden lighting from the setting sun. The person appears to be enjoying a peaceful evening stroll.",
  "finishReason": "stop"
}
```

**Response with structured output:**

```
{
  "message": "{\"summary\": \"A peaceful evening walk through a park at sunset\", \"key_scenes\": [\"Person entering the park\", \"Walking along tree-lined path\", \"Sunset lighting through trees\", \"Person sitting on bench\"], \"duration\": \"Approximately 2 minutes\"}",
  "finishReason": "stop"
}
```

**Response when max tokens reached:**

```
{
  "message": "This video contains multiple scenes showing various activities. The first scene shows...",
  "finishReason": "length"
}
```

------