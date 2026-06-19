

# Using Amazon Bedrock Data Automation CLI
<a name="bda-cli-guide"></a>

The Amazon Bedrock Data Automation (BDA) feature provides a streamlined CLI workflow for processing your data. For all modalities, this workflow consists of three main steps: creating a project, creating Blueprints for custom output, and processing documents. This guide walks you through the key CLI commands for working with BDA. 

## Create your first Data Automation project
<a name="create-data-automation-project-cli"></a>

To begin working with BDA, first create a project using the `create-data-automation-project` command.

Consider this sample passport that we'll process:

![Sample US passport showing personal information fields including name, date of birth, and passport number.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/passport2.png)


When creating a project, you must define your configuration settings for the type of file you intend to process. The following command represents a minimal working example for creating an image processing project:

```
aws bedrock-data-automation create-data-automation-project \
    --project-name "ImageProcessingProject" \
    --standard-output-configuration '{
        "image": {
            "extraction": {
                "category": {
                    "state": "ENABLED",
                    "types": ["TEXT_DETECTION"]
                },
                "boundingBox": {
                    "state": "ENABLED"
                }
            },
            "generativeField": {
                "state": "ENABLED"
            }
        }
    }'
```

The command validates the input configuration and creates a new project with a unique ARN. A response would include the project ARN and stage:

```
{
    "projectArn": "Amazon Resource Name (ARN)",
    "projectStage": "DEVELOPMENT",
    "status": "IN_PROGRESS"
}
```

If a project is created with no parameters, the default settings will apply. For example, when processing images, image summarization and text detection will be enabled by default.

## Complete parameter reference
<a name="create-project-parameters"></a>

The following table shows all available parameters for the `create-data-automation-project` command:


**Parameters for create-data-automation-project**  

| Parameter | Required | Default | Description | 
| --- | --- | --- | --- | 
| --project-name | Yes | N/A | Name for the Data Automation project | 
| --project-type | No | The type of the project defines which runtime processing API it may be used with. ASYNC projects may only be used with the invoke-bedrock-data-automation-async API, whereas SYNC projects may only be used with the invoke-bedrock-data-automation API. | 
| --project-stage | No | LIVE | Stage for the project (DEVELOPMENT or LIVE) | 
| --standard-output-configuration | Yes | N/A | JSON configuration for standard output processing | 
| --custom-output-configuration | No | N/A | JSON configuration for custom output processing | 
| --encryption-configuration | No | N/A | Encryption settings for the project | 
| --client-token | No | Auto-generated | Unique identifier for request idempotency | 

## Creating a Blueprint
<a name="create-blueprint-cli"></a>

After creating a project, you can create a Blueprint to define the structure of your data processing using the `create-blueprint` command.

Here's a minimal working example for creating a Blueprint tailored to passport processing:

```
aws bedrock-data-automation create-blueprint \
    --blueprint-name "passport-blueprint" \
    --type "IMAGE" \
    --blueprint-stage "DEVELOPMENT" \
    --schema '{
        "class": "Passport",
        "description": "Blueprint for processing passport images",
        "properties": {
            "passport_number": {
                "type": "string",
                "inferenceType": "explicit",
                "instruction": "The passport identification number"
            },
            "full_name": {
                "type": "string",
                "inferenceType": "explicit",
                "instruction": "The full name of the passport holder"
            }
        }
    }'
```

The command creates a new Blueprint with the specified schema. You can then use this Blueprint when processing documents to extract structured data according to your defined schema.

## Using your Blueprint
<a name="using-blueprint-cli"></a>

### Adding a Blueprint to a project
<a name="adding-blueprint-to-project"></a>

To add a Blueprint to your project, use the `update-data-automation-project` command:

```
aws bedrock-data-automation update-data-automation-project \
    --project-arn "Amazon Resource Name (ARN)" \
    --standard-output-configuration '{
        "image": {
            "extraction": {
                "category": {
                    "state": "ENABLED",
                    "types": ["TEXT_DETECTION"]
                },
                "boundingBox": {
                    "state": "ENABLED"
                }
            },
            "generativeField": {
                "state": "ENABLED",
                "types": ["IMAGE_SUMMARY"]
            }
        }
    }' \
    --custom-output-configuration '{
        "blueprints": [
            {
                "blueprintArn": "Amazon Resource Name (ARN)",
                "blueprintVersion": "1",
                "blueprintStage": "LIVE"
            }
        ]
    }'
```

### Verifying Blueprint integration
<a name="verifying-blueprint-integration"></a>

You can verify the Blueprint integration using the `get-data-automation-project` command:

```
aws bedrock-data-automation get-data-automation-project \
    --project-arn "Amazon Resource Name (ARN)"
```

### Managing multiple Blueprints
<a name="managing-multiple-blueprints"></a>

Use the `list-blueprints` command to view all of your Blueprints:

```
aws bedrock-data-automation list-blueprints
```

## Process Documents Asynchronously
<a name="invoke-data-automation-cli"></a>

Before processing documents with BDA, you must first upload your documents to an S3 bucket.Once you have a project set up, you can process documents using the `invoke-data-automation-async` command:

```
aws bedrock-data-automation-runtime invoke-data-automation-async \
    --input-configuration '{
        "s3Uri": "s3://my-bda-documents/invoices/invoice-123.pdf"
    }' \
    --output-configuration '{
        "s3Uri": "s3://my-bda-documents/output/"
    }' \
    --data-automation-configuration '{
        "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
        "stage": "LIVE"
    }' \
    --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

The command returns an invocation ARN that you can use to check the processing status:

```
{
    "invocationArn": "Amazon Resource Name (ARN)"
}
```

## Check Processing Status
<a name="get-data-automation-status-cli"></a>

To check the status of your processing job, use the `get-data-automation-status` command:

```
aws bedrock-data-automation-runtime get-data-automation-status \
    --invocation-arn "Amazon Resource Name (ARN)"
```

The command returns the current status of the processing job:

```
{
    "status": "COMPLETED",
    "creationTime": "2025-07-09T12:34:56.789Z",
    "lastModifiedTime": "2025-07-09T12:45:12.345Z",
    "outputLocation": "s3://my-bda-documents/output/efgh5678/"
}
```

Possible status values include:
+ `IN_PROGRESS`: The processing job is currently running.
+ `COMPLETED`: The processing job has successfully completed.
+ `FAILED`: The processing job has failed. Check the response for error details.
+ `STOPPED`: The processing job was manually stopped.

## Retrieve Results
<a name="retrieve-results-cli"></a>

Once processing is complete, you can list the output files in your S3 bucket:

```
aws s3 ls s3://my-bda-documents/output/efgh5678/
```

To download the results to your local machine:

```
aws s3 cp s3://my-bda-documents/output/efgh5678/ ~/Downloads/bda-results/ --recursive
```

The output includes structured data based on your project configuration and any Blueprints you've applied.

## Process Documents Synchronously
<a name="process-docs-sync"></a>

Before processing documents with BDA, you must first upload your documents to an S3 bucket. Sync API srupports both input via S3 bucket or image bytes (i.e. processing documents without S3). The command returns structured data based on your project configuration and any Blueprints you've applied:

```
aws bedrock-data-automation-runtime invoke-data-automation \
    --input-configuration '{
        "s3Uri": "s3://my-bda-documents/invoices/invoice-123.pdf"
    }' \
    --data-automation-configuration '{
        "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
        "stage": "LIVE"
    }' \
    --data-automation-profile-arn "Amazon Resource Name (ARN)"
```

## Process Images Synchronously
<a name="process-images-sync"></a>

The command returns structured data based on your project configuration and any Blueprints you've applied:

```
aws bedrock-data-automation-runtime invoke-data-automation \
    --input-configuration '{
        "s3Uri": "s3://my-bda-documents/invoices/advertisement_latest.jpeg"
    }' \
    --data-automation-configuration '{
        "dataAutomationProjectArn": "Amazon Resource Name (ARN)",
        "stage": "LIVE"
    }' \
    --data-automation-profile-arn "Amazon Resource Name (ARN)"
```