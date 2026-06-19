

# Processing through CLI
<a name="bda-document-processing-cli"></a>

Before processing documents with BDA, you must first upload your documents to an S3 bucket:

**Syntax**

```
aws s3 cp <source> <target> [--options]
```

Example:

```
aws s3 cp /local/path/document.pdf s3://my-bda-bucket/input/document.pdf
```

------
#### [ Async ]

**Basic processing command structure**

Use the `invoke-data-automation-async` command to process files:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://amzn-s3-demo-bucket/sample-images/sample-image.jpg"
        }' \
        --output-configuration '{
            "s3Uri": "s3://amzn-s3-demo-bucket/output/"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

**Advanced processing command structure**

**Video processing with time segments**

For video files, you can specify time segments to process:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://my-bucket/video.mp4",
            "assetProcessingConfiguration": {
                "video": {
                    "segmentConfiguration": {
                        "timestampSegment": {
                            "startTimeMillis": 0,
                            "endTimeMillis": 300000
                        }
                    }
                }
            }
        }' \
        --output-configuration '{
            "s3Uri": "s3://my-bucket/output/"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

**Using custom blueprints**

You can specify custom blueprints directly in the command:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://my-bucket/document.pdf"
        }' \
        --output-configuration '{
            "s3Uri": "s3://my-bucket/output/"
        }' \
        --blueprints '[
            {
                "blueprintArn": "Amazon Resource Name (ARN)",
                "version": "1",
                "stage": "LIVE"
            }
        ]' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

**Adding encryption configuration**

For enhanced security, you can add encryption configuration:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://my-bucket/document.pdf"
        }' \
        --output-configuration '{
            "s3Uri": "s3://my-bucket/output/"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --encryption-configuration '{
            "kmsKeyId": "Amazon Resource Name (ARN)",
            "kmsEncryptionContext": {
                "Department": "Finance",
                "Project": "DocumentProcessing"
            }
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

**Event notifications**

Enable EventBridge notifications for processing completion:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://my-bucket/document.pdf"
        }' \
        --output-configuration '{
            "s3Uri": "s3://my-bucket/output/"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --notification-configuration '{
            "eventBridgeConfiguration": {
                "eventBridgeEnabled": true
            }
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

**Checking processing status**

Use the `get-data-automation-status` command to check the status of your processing job:

```
aws bedrock-data-automation-runtime get-data-automation-status \
        --invocation-arn "Amazon Resource Name (ARN)"
```

The response will include the current status:

```
{
        "status": "COMPLETED",
        "creationTime": "2025-07-24T12:34:56.789Z",
        "lastModifiedTime": "2025-07-24T12:45:12.345Z",
        "outputLocation": "s3://my-bucket/output/abcd1234/"
        }
```

**Retrieve processing results**

**Locating output files in S3**

List the output files in your S3 bucket:

```
aws s3 ls s3://amzn-s3-demo-bucket/output/
```

Download the results to your local machine:

```
aws s3 cp s3://amzn-s3-demo-bucket/output/ ~/Downloads/bda-results/ --recursive
```

**Understanding output structure**

The output typically includes:
+ `standard-output.json`: Contains standard extraction results
+ `custom-output.json`: Contains results from custom blueprints
+ `metadata.json`: Contains processing metadata and confidence scores

**Common response fields**

Standard output typically includes:
+ `extractedData`: The main extracted information
+ `confidence`: Confidence scores for each extracted field
+ `metadata`: Processing information including timestamps and model details
+ `boundingBoxes`: Location information for detected elements (if enabled)

**Error handling and troubleshooting**

Common error scenarios and solutions:
+ **Invalid S3 URI**: Ensure your S3 bucket exists and you have proper permissions
+ **Missing data-automation-profile-arn**: This parameter is required for all processing requests
+ **Project not found**: Verify your project ARN is correct and the project exists
+ **Unsupported file format**: Check that your file format is supported by BDA

**Adding tags to processing jobs**

You can add tags to help organize and track your processing jobs:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
        --input-configuration '{
            "s3Uri": "s3://my-bucket/document.pdf"
        }' \
        --output-configuration '{
            "s3Uri": "s3://my-bucket/output/"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --tags '[
            {
                "key": "Department",
                "value": "Finance"
            },
            {
                "key": "Project",
                "value": "InvoiceProcessing"
            }
        ]' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

------
#### [ Sync ]

**Basic processing command structure**

Use the `invoke-data-automation` command to process files:

```
        aws bedrock-data-automation-runtime invoke-data-automation \
        --input-configuration '{
            "s3Uri": "s3://amzn-s3-demo-bucket/sample-images/sample-image.jpg"
        }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
        --region "aws-region"
```

**Advanced processing command structure**

Output to S3 bucket

```
        aws bedrock-data-automation-runtime invoke-data-automation \
        --input-configuration '{
            "s3Uri": "s3://amzn-s3-demo-bucket/sample-images/sample-image.jpg"
        }' \
        --output-configuration '{"s3Uri": "s3://amzn-s3-demo-bucket/output/" }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
        --region "aws-region"   //document only
```

Use byte input

```
        aws bedrock-data-automation-runtime invoke-data-automation \
        --input-configuration '{
            "bytes": #blob input
        }' \
        --output-configuration '{"s3Uri": "s3://amzn-s3-demo-bucket/output/" }' \
        --data-automation-configuration '{
            "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
            "stage": "LIVE"
        }' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
        --region "aws-region"
```

**Note**  
**Bytes**  
A blob of base64-encoded document bytes. The maximum size of a document that's provided in a blob of bytes is 50 MB. Type should be Base64-encoded binary data object.

**Use custom blueprints (only for image)**

```
        aws bedrock-data-automation-runtime invoke-data-automation \
        --input-configuration '{
            "s3Uri": "s3://amzn-s3-demo-bucket/sample-images/sample-image.jpg"
        }' \
        --blueprints '[{"blueprintArn": "Amazon Resource Name (ARN)", "version": "1", "stage": "LIVE" } ]' \
        --data-automation-profile-arn "Amazon Resource Name (ARN)"
        --region "aws-region"
```

------