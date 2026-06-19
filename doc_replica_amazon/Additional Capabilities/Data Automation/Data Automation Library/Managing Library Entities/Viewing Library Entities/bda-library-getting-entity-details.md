

# Getting Library Entity Details
<a name="bda-library-getting-entity-details"></a>

Use the [GetDataAutomationLibraryEntity](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_GetDataAutomationLibraryEntity.html) api to retrieve the list of vocabulary for an entity.

## AWS CLI Example:
<a name="bda-library-getting-entity-details-cli"></a>

**Request**

```
aws bedrock-data-automation get-data-automation-library-entity \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --entity-type "VOCABULARY" \
    --entity-id "medical-en"
```

**Response**

```
{
    "entity": {
        "vocabulary": {
            "entityId": "medical-en",
            "language": "EN",
            "phrases": [
                {
                    "text": "paracetamol"
                },
                {
                    "text": "ibuprofen"
                }
            ],
            "lastModifiedTime": "2026-03-06T07:06:00.413000+00:00"
        }
    }
}
```

## AWS Console Example:
<a name="bda-library-getting-entity-details-console"></a>

1. Navigate to the "Library details" page for your library

1. Choose the desired entity from the list

![Translation management interface showing two phrases, ibuprofen and paracetamol, with language set to English.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-get-entity-details-console.png)
