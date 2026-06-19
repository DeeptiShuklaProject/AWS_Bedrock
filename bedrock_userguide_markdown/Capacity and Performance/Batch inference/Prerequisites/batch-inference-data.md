

# Format and upload your batch inference data
<a name="batch-inference-data"></a>

You must add your batch inference data to an S3 location that you'll choose or specify when submitting a model invocation job. The S3 location must contain the following items:
+ At least one JSONL file that defines the model inputs. A JSONL contains rows of JSON objects. Your JSONL file must end in the extension .jsonl and be in the following format:

  ```
  { "recordId" : "{{string}}", "modelInput" : {{{JSON body}}} }
  ...
  ```

  Each line contains a JSON object with a `recordId` field and a `modelInput` field. The format of the `modelInput` JSON object depends on the model invocation type that you choose when you [create the batch inference job](batch-inference-create.md). If you use the `InvokeModel` type (default), the format must match the `body` field for the model that you use in the `InvokeModel` request (see [Inference request parameters and response fields for foundation models](model-parameters.md)). If you use the `Converse` type, the format must match the request body of the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API.
**Note**  
If you omit the `recordId` field, Amazon Bedrock adds it in the output.
The order of records in the output JSONL file is not guaranteed to match the order of records in the input JSONL file.
You specify the model that you want to use when you create the [batch inference job](batch-inference-create.md).
+ (If your input content contains an Amazon S3 location) Some models allow you to define the content of the input as an S3 location. See [Example video input for Amazon Nova](#batch-inference-data-ex-s3).
**Warning**  
When using S3 URIs in your prompts, all resources must be in the same S3 bucket and folder. The `InputDataConfig` parameter must specify the folder path containing all linked resources (such as videos or images), not just an individual `.jsonl` file. Note that S3 paths are case-sensitive, so ensure your URIs match the exact folder structure.

Ensure that your inputs conform to the batch inference quotas. You can search for the following quotas at [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock):
+ **Minimum number of records per batch inference job** – The minimum number of records (JSON objects) across JSONL files in the job.
+ **Records per input file per batch inference job** – The maximum number of records (JSON objects) in a single JSONL file in the job.
+ **Records per batch inference job** – The maximum number of records (JSON objects) across JSONL files in the job.
+ **Batch inference input file size** – The maximum size of a single file in the job.
+ **Batch inference job size** – The maximum cumulative size of all input files.

To better understand how to set up your batch inference inputs, see the following examples:

## Example text input for Anthropic Claude 3 Haiku
<a name="batch-inference-data-ex-text"></a>

If you plan to run batch inference using the [Messages API](model-parameters-anthropic-claude-messages.md) format for the Anthropic Claude 3 Haiku model, you might provide a JSONL file containing the following JSON object as one of the lines:

```
{
    "recordId": "CALL0000001", 
    "modelInput": {
        "anthropic_version": "bedrock-2023-05-31", 
        "max_tokens": 1024,
        "messages": [ 
            { 
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": "Summarize the following call transcript: ..." 
                    } 
                ]
            }
        ]
    }
}
```

## Example video input for Amazon Nova
<a name="batch-inference-data-ex-s3"></a>

If you plan to run batch inference on video inputs using the Amazon Nova Lite or Amazon Nova Pro models, you have the option of defining the video in bytes or as an S3 location in the JSONL file. For example, you might have an S3 bucket whose path is `s3://batch-inference-input-bucket` and contains the following files:

```
s3://batch-inference-input-bucket/
├── videos/
│   ├── video1.mp4
│   ├── video2.mp4
│   ├── ...
│   └── video50.mp4
└── input.jsonl
```

A sample record from the `input.jsonl` file would be the following:

```
{
    "recordId": "RECORD01",
    "modelInput": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "You are an expert in recipe videos. Describe this video in less than 200 words following these guidelines: ..."
                    },
                    {
                        "video": {
                            "format": "mp4",
                            "source": {
                                "s3Location": {
                                    "uri": "{{s3://batch-inference-input-bucket/videos/video1.mp4}}",
                                    "bucketOwner": "{{111122223333}}"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
}
```

When you create the batch inference job, you must specify the folder path `s3://batch-inference-input-bucket` in your `InputDataConfig` parameter. Batch inference will process the `input.jsonl` file at this location, along with any referenced resources (such as the video files in the `videos` subfolder).

The following resources provide more information about submitting video inputs for batch inference:
+ To learn how to validate Amazon S3 URIs in an input request, see the [Amazon S3 URL Parsing blog](https://aws.amazon.com/blogs/devops/s3-uri-parsing-is-now-available-in-aws-sdk-for-java-2-x/).
+ For more information on how to set up invocation records for video understanding with Nova, see [Amazon Nova vision prompting guidelines](https://docs.aws.amazon.com/nova/latest/userguide/prompting-vision-prompting.html).

## Example Converse input
<a name="batch-inference-data-ex-converse"></a>

If you set the model invocation type to `Converse` when creating the batch inference job, the `modelInput` field must use the Converse API request format. The following example shows a JSONL record for a Converse batch inference job:

```
{
    "recordId": "CALL0000001",
    "modelInput": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "Summarize the following call transcript: ..."
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1024
        }
    }
}
```

For the full list of fields supported in the Converse request body, see [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) in the API reference.

The following topic describes how to set up S3 access and batch inference permissions for an identity to be able to carry out batch inference.