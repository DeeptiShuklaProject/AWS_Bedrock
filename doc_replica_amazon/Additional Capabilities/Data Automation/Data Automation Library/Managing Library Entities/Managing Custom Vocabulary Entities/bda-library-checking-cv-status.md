

# Checking Vocabulary Ingestion Job Status
<a name="bda-library-checking-cv-status"></a>

```
aws bedrock-data-automation get-data-automation-library-ingestion-job \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --job-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library-ingestion-job/job-12345"
```

## Job Statuses:
<a name="bda-library-checking-cv-status-statuses"></a>
+ **IN\_PROGRESS:** Job is currently processing
+ **COMPLETED:** All entities processed successfully
+ **COMPLETED\_WITH\_ERRORS:** Some entities failed (check output for details)
+ **FAILED:** Job failed completely

## Understanding Job Output
<a name="bda-library-checking-cv-status-output"></a>

After job completion, check the S3 output location for detailed results.

```
{
  "metadata": {
    "jobId": "job-12345",
    "manifestS3Bucket": "my-bucket",
    "manifestS3Key": "manifests/vocabulary-manifest.json"
  },
  "vocabulary": {
    "successful": [
      {
        "entityId": "medical-en",
        "itemIndex": 0,
        "description": "Medical terms in English language",
        "phrases": [
          {
            "text": "acetaminophen"
          },
          {
            "text": "ibuprofen"
          },
          {
            "text": "naproxen"
          }
        ],
        "language": "EN"
      }
    ],
    "failed": [
      {
        "entityId": "medical-es",
        "itemIndex": 1,
        "errorType": "ValidationError",
        "errorMessage": "Entity validation failed: Missing required creator property 'language'"
      }
    ]
  }
}
```