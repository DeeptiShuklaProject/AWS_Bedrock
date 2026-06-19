

# Updating Vocabulary Entities
<a name="bda-library-updating-cv"></a>

Use the [InvokeDataAutomationLibraryIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_InvokeDataAutomationLibraryIngestionJob.html) with "UPSERT" operation type to update existing vocabulary entities for the same entityId. This will replace the entire entity with the new content.

**Important**  
UPSERT operations are clobber-style at the entity level. The entire entity is replaced, not merged.

## AWS CLI Example:
<a name="bda-library-updating-cv-cli"></a>

*Note that this operation is same as [Adding New Vocabulary Entities](bda-library-adding-cv.md).*

**Request**

```
aws bedrock-data-automation-data-automation invoke-data-automation-library-ingestion-job \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --entity-type "VOCABULARY" \
    --operation-type "UPSERT" \
    --input-configuration '{"s3Object":{"s3Uri":"s3://my-bucket/manifests/vocabulary-manifest.json"}}' \
    --output-configuration '{"s3Uri":"s3://my-bucket/outputs/"}'
```

## AWS Console Example:
<a name="bda-library-updating-cv-console"></a>

1. Navigate to the "Library details" page for your library

1. Select the desired entity from the "Custom vocabulary lists"

1. Make the desired modifications:

   1. Update:

      1. Select the desired phrase

      1. Update the phrase

      1. Choose the check mark to the right of the phrase

   1. Delete

      1. Select the checkbox to the left of the desired phrase(s)

      1. Choose "Delete phrases"

1. Choose "Save updates"

![Custom terminology editor showing phrase ibuprofen updated to display as paracetamol.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-update-cv-console.png)
