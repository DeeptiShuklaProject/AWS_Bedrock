

# Deleting Vocabulary List
<a name="bda-library-deleting-cv"></a>

Use the [InvokeDataAutomationLibraryIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_InvokeDataAutomationLibraryIngestionJob.html) with "DELETE" operation type to remove specific entities from your library.

## AWS CLI Example:
<a name="bda-library-deleting-cv-cli"></a>

### Option 1: Using S3 Manifest file
<a name="bda-library-deleting-cv-option1"></a>

#### Step 1: Create a JSONL manifest file
<a name="bda-library-deleting-cv-option1-step1"></a>

Create a simple s3 manifest file with a list of entityIds.

Example: `cv-delete-manifest.json`

```
{"entityIds": ["medical-en", "medical-es"]}
```

#### Step 2: Upload the manifest to S3
<a name="bda-library-deleting-cv-option1-step2"></a>

```
aws s3 cp vocabulary-manifest.json s3://my-bucket/manifests/
```

#### Step 3: Start the ingestion job
<a name="bda-library-deleting-cv-option1-step3"></a>

Use the [InvokeDataAutomationLibraryIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_InvokeDataAutomationLibraryIngestionJob.html) to start a vocabulary ingestion job with an operation type DELETE

**Request**

```
aws bedrock-data-automation invoke-data-automation-library-ingestion-job \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --entity-type "VOCABULARY" \
    --operation-type "DELETE" \
    --input-configuration '{"s3Object":{"s3Uri":"s3://my-bucket/manifests/cv-delete-manifest.json"}}' \
    --output-configuration '{"s3Uri":"s3://my-bucket/outputs/"}'
```

**Response:**

```
{
  "jobArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library-ingestion-job/job-12345"
}
```

### Option 2: Using inline payload
<a name="bda-library-deleting-cv-option2"></a>

**Request**

```
aws bedrock-data-automation invoke-data-automation-library-ingestion-job \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --entity-type "VOCABULARY" \
    --operation-type "DELETE" \
    --input-configuration '{"inlinePayload":{"deleteEntitiesInfo":{"entityIds": ["medical-en"]}}}' \
    --output-configuration '{"s3Uri": "s3://my-bucket/outputs/"}'
```

## AWS Console Example:
<a name="bda-library-deleting-cv-console"></a>

1. Navigate to the "Library details" page for your library

1. Choose the desired entity from the "Custom vocabulary lists"

1. Choose "Delete custom vocabulary list"