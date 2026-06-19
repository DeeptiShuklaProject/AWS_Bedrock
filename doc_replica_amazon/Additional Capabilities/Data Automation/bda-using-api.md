

# Using the Bedrock Data Automation API
<a name="bda-using-api"></a>

The Amazon Bedrock Data Automation (BDA) feature provides a streamlined API workflow for processing your data. For all modalities, this workflow consists of three main steps: creating a project, invoking the analysis, and retrieving the results. To retrieve custom output for your processed data, you provide the Blueprint ARN when you invoke the analysis operation.

## Create a Data Automation Project
<a name="create-data-automation-project"></a>

To begin processing files with BDA, you first need to create a Data Automation Project. This can be done in two ways, with the CreateDataAutomationProject operation or the Amazon Amazon Bedrock Console.

### Using the API
<a name="using-the-api"></a>

When using the API to create a project, you invoke the CreateDataAutomationProject. When creating a project, you must define your configuration settings for the type of file you tend to process (the modality you intend to use). Here's an example of how you might configure the standard output for images:

```
{
    "standardOutputConfiguration": {
        "image": {
            "state": "ENABLED",
            "extraction": {
                "category": {
                    "state": "ENABLED",
                    "types": [
                        "CONTENT_MODERATION",
                        "TEXT_DETECTION"
                    ]
                },
                "boundingBox": {
                    "state": "ENABLED"
                }
            },
            "generativeField": {
                "state": "ENABLED",
                "types": [
                    "IMAGE_SUMMARY",
                    "IAB"
                ]
            }
        }
    }
}
```

The API validates the input configuration. It creates a new project with a unique ARN. The project settings are stored for future use. If a project is created with no parameters, the default settings will apply. For example, when processing images, image summarization and text detection will be enabled by default.

There's a limit to the number of projects that can be created per AWS account. Certain combinations of settings may not be allowed or may require additional permissions.

------
#### [ Async ]

**Invoke Data Automation Async**

You have a project set up, you can start processing images using the [InvokeDataAutomationAsync](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomationAsync.html) operation. If using custom output, you can submit one or more blueprint ARNs per request.

This API call initiates the asynchronous processing of your files in a specified S3 bucket. The API accepts the project ARN and the file to be processed, then starts the asynchronous processing job. An `invocationArn` is returned for tracking the process. Errors will be raised if the project doesn't exist, or if the caller doesn't have the necessary permissions, or if the input files aren't in a supported format.

The following is the structure of the JSON request:

```
{
   {
   "blueprints": [ 
      { 
         "blueprintArn": "{{string}}",
         "stage": "{{string}}",
         "version": "{{string}}"
      }
   ],
   "clientToken": "{{string}}",
   "dataAutomationConfiguration": { 
      "dataAutomationProjectArn": "{{string}}",
      "stage": "{{string}}"
   },
   "dataAutomationProfileArn": "{{string}}",
   "encryptionConfiguration": { 
      "kmsEncryptionContext": { 
         "string" : "{{string}}" 
      },
      "kmsKeyId": "{{string}}"
   },
   "inputConfiguration": { 
      "assetProcessingConfiguration": { 
         "video": { 
            "segmentConfiguration": { ... }
         }
      "s3Uri": "{{string}}"
   },
   "notificationConfiguration": { 
      "eventBridgeConfiguration": { 
         "eventBridgeEnabled": {{boolean}}
      }
   },
   "outputConfiguration": { 
      "s3Uri": "{{string}}"
   },
   "tags": [ 
      { 
         "key": "s{{string}}",
         "value": "{{string}}"
      }
   ]
}
}
```

When you run `InvokeDataAutomationAsync` on a video file, you can set a 5 minute or longer section of a video that will be treated as a full video for the data extraction. This time is set with a timestamp of the starting millisecond and ending millisecond. This information is added in the `assetProcessingConfiguration` element.

------
#### [ Sync ]

**Invoke Data Automation**

Alternatively, you can use the [InvokeDataAutomation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomation.html) operation. The `InvokeDataAutomation` operation only supports processing images.

This API call initiates the synchronous processing of the provided via an S3 reference, or in the payload. The API accepts the project ARN and the file to be processed, and returns the structured insights in the response. Errors will be raised if the project doesn't exist, or if the caller doesn't have the necessary permissions, or if the input files aren't in a supported format. If the analyzed image is semantically classified as a document, this will also be raised as an error, because the InvokeDataAutomation only supports Images. To prevent this error, you may use Modality Routing on your project to force routing of all image file types as Images (see [Disabling modalities and routing file types](bda-routing-enablement.md)).

Here is the structure of the JSON request for both image and document. Sync API request supports both image bytes and S3 bucket. To use image bytes, simply replace `“s3Uri”: “string”` in “inputConfiguration” section with `“bytes“: “base64-encoded string“` `outputConfiguration` is optional with default is inline output. If S3 uri is provided as outputConfiguration, encrypted output will be put into the specified S3 bucket.

```
{
   {
    "blueprints": [ 
       { 
          "blueprintArn": "string",  //use for image
          "stage": "string",
          "version": "string"
       }
    ],
    "dataAutomationConfiguration": { 
       "dataAutomationProjectArn": "string",
       "stage": "string"
    },
    "dataAutomationProfileArn": "string",
    "inputConfiguration": { 
          "s3Uri": "string"
    },
    "outputConfiguration": { 
       "s3Uri": "string"
    }  
 }
}
```

The output includes unique structures depending on both the file, operations, and custom output configuration specified in the call to InvokeDataAutomation. Note that this response includes both the standard and custom output responses.

------

Here is the structure of the JSON response with both standard and custom output configuration:

```
{
  "semanticModality": "IMAGE",
  "outputSegments": [
    {
      "customOutputStatus": "MATCH",
      "standardOutput": {
        "image": {
          "summary": "This image shows a white Nike running shoe with a black Nike swoosh logo on the side. The shoe has a modern design with a thick, cushioned sole and a sleek upper part. The word \"ROUKEA\" is visible on the sole of the shoe, repeated twice. The shoe appears to be designed for comfort and performance, suitable for running or athletic activities. The background is plain and dark, highlighting the shoe.",
          "iab_categories": [
            {
              "category": "Style and Fashion",
              "confidence": 0.9890000000000001,
              "taxonomy_level": 1,
              "parent_name": "",
              "id": "0ebe86c8-e9af-43f6-a7bb-182a61d2e1fd",
              "type": "IAB"
            },
            {
              "category": "Men's Fashion",
              "confidence": 0.9890000000000001,
              "taxonomy_level": 2,
              "parent_name": "Style and Fashion",
              "id": "13bd456a-3e1b-4681-b0dd-f42a8d5e5ad5",
              "type": "IAB"
            },
            {
              "category": "Style and Fashion",
              "confidence": 0.853,
              "taxonomy_level": 1,
              "parent_name": "",
              "id": "177b29a1-0e40-45c1-8540-5f49a3d7ded3",
              "type": "IAB"
            },
            {
              "category": "Women's Fashion",
              "confidence": 0.853,
              "taxonomy_level": 2,
              "parent_name": "Style and Fashion",
              "id": "f0197ede-3ba6-498b-8f7b-43fecc5735ef",
              "type": "IAB"
            }
          ],
          "content_moderation": [],
          "logos": [
            {
              "id": "2e109eb6-39f5-4782-826f-911b62d277fb",
              "type": "LOGOS",
              "confidence": 0.9170872209665809,
              "name": "nike",
              "locations": [
                {
                  "bounding_box": {
                    "left": 0.3977411523719743,
                    "top": 0.4922481227565456,
                    "width": 0.2574246356942061,
                    "height": 0.15461772197001689
                  }
                }
              ]
            }
          ],
          "text_words": [
            {
              "id": "f70301df-5725-405e-b50c-612e352467bf",
              "type": "TEXT_WORD",
              "confidence": 0.10091366487951722,
              "text": "ROUKEA",
              "locations": [
                {
                  "bounding_box": {
                    "left": 0.6486002310163024,
                    "top": 0.6783271480251003,
                    "width": 0.13219473954570082,
                    "height": 0.05802226710963898
                  },
                  "polygon": [
                    {
                      "x": 0.6486002310163024,
                      "y": 0.7025876947351404
                    },
                    {
                      "x": 0.7760931467045249,
                      "y": 0.6783271480251003
                    },
                    {
                      "x": 0.7807949705620032,
                      "y": 0.7120888684246991
                    },
                    {
                      "x": 0.6533020989743271,
                      "y": 0.7363494151347393
                    }
                  ]
                }
              ],
              "line_id": "9147fec0-d869-4d58-933e-93eb7164c404"
            }
          ],
          "text_lines": [
            {
              "id": "9147fec0-d869-4d58-933e-93eb7164c404",
              "type": "TEXT_LINE",
              "confidence": 0.10091366487951722,
              "text": "ROUKEA",
              "locations": [
                {
                  "bounding_box": {
                    "left": 0.6486002310163024,
                    "top": 0.6783271480251003,
                    "width": 0.13219473954570082,
                    "height": 0.05802226710963898
                  },
                  "polygon": [
                    {
                      "x": 0.6486002310163024,
                      "y": 0.7025876947351404
                    },
                    {
                      "x": 0.7760931467045249,
                      "y": 0.6783271480251003
                    },
                    {
                      "x": 0.7807949705620032,
                      "y": 0.7120888684246991
                    },
                    {
                      "x": 0.6533020989743271,
                      "y": 0.7363494151347393
                    }
                  ]
                }
              ]
            }
          ]
        },
        "statistics": {
          "iab_category_count": 4,
          "content_moderation_count": 0,
          "logo_count": 1,
          "line_count": 1,
          "word_count": 1
        },
        "metadata": {
          "semantic_modality": "IMAGE",
          "image_width_pixels": 173,
          "image_height_pixels": 148,
          "image_encoding": "jpeg",
          "s3_bucket": "test-bucket",
          "s3_key": "uploads/test-image.jpeg"
        }
      },
      "customOutput": {
        "matched_blueprint": {
          "arn": "arn:aws:bedrock:us-east-1:123456789012:blueprint/test",
          "version": "1",
          "name": "test-blueprint",
          "confidence": 1.0
        },
        "inference_result": {
          "product_details": {
            "product_category": "footwear"
          },
          "image_sentiment": "Positive",
          "image_background": "Solid color",
          "image_style": "Product image",
          "image_humor": false
        }
      }
    }
  ]
}
```

## Get Data Automation Status
<a name="get-data-automation-status"></a>

To check the status of your processing job and retrieve results, use GetDataAutomationStatus.

The GetDataAutomationStatus API allows you to monitor the progress of your job and access the results once processing is complete. The API accepts the invocation ARN returned by InvokeDataAutomationAsync. It checks the current status of the job and returns relevant information. Once the job is complete, it provides the location of the results in S3.

If the job is still in progress, it returns the current state (e.g., "InProgress"). If the job is complete, it returns "Success" along with the S3 location of the results. If there was an error, it returns "ServiceError" or "ClientError" with error details.

The following is the format of the request JSON:

```
{
   "InvocationArn": "string" // Arn
}
```

## Async Output Response
<a name="async-output-response"></a>

The results of the file processing are stored in the S3 bucket configured for the input images. The output includes unique structures depending on both the file modality and the operation types specified in the call to InvokeDataAutomationAsync. 

For information on the standard outputs for a given modality, see [Standard output in Bedrock Data Automation](bda-standard-output.md).

As an example, for images it can include information on the following:
+ Image Summarization: A descriptive summary or caption of the image.
+ IAB Classification: Categorization based on the IAB taxonomy.
+ Image Text Detection: Extracted text with bounding box information.
+ Content Moderation: Detects inappropriate, unwanted, or offensive content in an image.

The following is an example snippet of the output for image processing:

```
{
    "metadata": {
        "id": "image_123",
        "semantic_modality": "IMAGE",
        "s3_bucket": "my-s3-bucket",
        "s3_prefix": "images/",
        "image_width_pixels": 1920,
        "image_height_pixels": 1080
    },
    "image": {
        "summary": "A lively party scene with colorful decorations and supplies",
        "iab_categories": [
            {
                "category": "Party Supplies",
                "confidence": 0.9,
                "parent_name": "Events & Attractions"
            }
        ],
        "content_moderation": [
            {
                "category": "Drugs & Tobacco Paraphernalia & Use",
                "confidence": 0.7
            }
        ],
        "text_words": [
            {
                "id": "word_1",
                "text": "lively",
                "confidence": 0.9,
                "line_id": "line_1",
                "locations": [
                    {
                        "bounding_box": {
                            "left": 100,
                            "top": 200,
                            "width": 50,
                            "height": 20
                        },
                        "polygon": [
                            {
                                "x": 100,
                                "y": 200
                            },
                            {
                                "x": 150,
                                "y": 200
                            },
                            {
                                "x": 150,
                                "y": 220
                            },
                            {
                                "x": 100,
                                "y": 220
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

This structured output allows for easy integration with downstream applications and further analysis.

## Blueprint Optimization APIs
<a name="blueprint-optimization-apis"></a>

### InvokeBlueprintOptimizationAsync
<a name="invoke-blueprint-optimization-async"></a>

You can improve blueprint accuracy by providing example content assets with the correct expected results. Blueprint instruction optimization uses your examples to refine the natural language instructions in your blueprint fields, which improves your inference *Results* accuracy.

For a blueprint, you can call InvokeBlueprintOptimizationAsync API which initiates the asynchronous optimization job to improve Blueprint field instructions based on ground truth data.

**Request Body**  


```
{
    "blueprint": {
        "blueprintArn": "arn:aws:bedrock:us-east-1:123456789012:blueprint/my-document-processor",
        "stage": "DEVELOPMENT"
    },
    "samples": [
        {
            "assetS3Object": {
                "s3Uri": "s3://my-optimization-bucket/samples/document1.pdf"
            },
            "groundTruthS3Object": {
                "s3Uri": "s3://my-optimization-bucket/ground-truth/document1-expected.json"
            }
        }
    ],
    "outputConfiguration": {
        "s3Object": {
            "s3Uri": "s3://my-optimization-bucket/results/optimization-output"
        }
    },
    "dataAutomationProfileArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-profile/my-profile"
}
```

**Response**  


```
{
    "invocationArn": "arn:aws:bedrock:us-east-1:123456789012:blueprint-optimization-invocation/opt-12345abcdef"
}
```

**Important**  
Save the invocationArn to monitor the optimization job status.

### GetBlueprintOptimizationStatus
<a name="get-blueprint-optimization-status"></a>

Retrieves the current status and results of a blueprint optimization job outputted by calling the InvokeBlueprintOptimizationAsync async API. GetBlueprintOptimizationStatus accepts the invocation ARN returned by InvokeBlueprintOptimizationAsync.

**Response**  


```
{
    "status": "Success",
    "outputConfiguration": {
        "s3Object": {
            "s3Uri": "s3://my-optimization-bucket/results/optimization-output"
        }
    }
}
```

**Status Values:**  

+ Created - Job has been created
+ InProgress - Optimization is running
+ Success - Optimization completed successfully
+ ServiceError - Internal service error occurred
+ ClientError - Invalid request parameters

### CopyBlueprintStage
<a name="copy-blueprint-stage"></a>

Copies the Blueprint from source stage to the target stage (eg. DEVELOPMENT stage to LIVE stage). This will be used to sync all the configuration including the optimizationSamples field between stages.

**Request Body**  


```
{
    "blueprintArn": "arn:aws:bedrock:us-east-1:123456789012:blueprint/my-document-processor",
    "sourceStage": "DEVELOPMENT",
    "targetStage": "LIVE"
}
```

**Stage Values:**  

+ DEVELOPMENT - Development/testing stage
+ LIVE - Production stage

**Response**  


```
{}
```

**Warning**  
This operation overwrites the target stage configuration and cannot be easily undone. Ensure thorough testing before copying to LIVE stage.