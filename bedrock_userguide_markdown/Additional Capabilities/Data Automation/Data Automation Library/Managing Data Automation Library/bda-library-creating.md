

# Creating Library
<a name="bda-library-creating"></a>

Use the [CreateDataAutomationLibrary](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_CreateDataAutomationLibrary.html) API to create a new library container.

## AWS CLI Example:
<a name="bda-library-creating-cli"></a>

**Request**

```
aws bedrock-data-automation create-data-automation-library \
    --library-name "healthcare-vocabulary" \
    --library-description "Medical terminology for transcription accuracy" \
    --region us-east-1
```

**Response**

```
{
  "libraryArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary",
  "status": "ACTIVE"
}
```

## AWS Console Example:
<a name="bda-library-creating-console"></a>

1. Navigate to "Manage libraries" page in BDA Console

1. Choose "Create library"

![Create library dialog with fields for library name, description, KMS key , and tags.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-create-console.png)


## Important Notes
<a name="bda-library-creating-notes"></a>

1. Library creation is synchronous and returns immediately

1. Library names must be unique within your account and region

1. The library is empty until you run an entity ingestion job

1. Libraries can be associated with multiple projects