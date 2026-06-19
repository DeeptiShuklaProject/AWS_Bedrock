

# Getting Library Details
<a name="bda-library-getting-details"></a>

Use the [GetDataAutomationLibrary](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_GetDataAutomationLibrary.html) API to retrieve information about an existing library.

## AWS CLI Example:
<a name="bda-library-getting-details-cli"></a>

**Request**

```
aws bedrock-data-automation get-data-automation-library \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary"
```

**Response:**

```
{
  "library": {
    "libraryArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary",
    "libraryName": "healthcare-vocabulary",
    "libraryDescription": "Medical terminology for transcription accuracy",
    "status": "ACTIVE",
    "creationTime": "2026-01-01T00:00:00Z",
    "entityTypes": [
      {
        "entityType": "VOCABULARY",
        "entityMetadata": "{\"entityCount\": 150}"
      }
    ]
  }
}
```

## AWS Console Example:
<a name="bda-library-getting-details-console"></a>

1. Navigate to "Manage libraries" page in BDA Console

1. Select the desired library from the list of libraries

![Custom vocabulary page showing library details and empty vocabulary lists table.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-get-details-console.png)
