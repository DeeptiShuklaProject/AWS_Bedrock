

# Listing Library Entities
<a name="bda-library-listing-entities"></a>

Use the [ListDataAutomationLibraryEntities](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_ListDataAutomationLibraryEntities.html) api to retrieve the list of entities.

## AWS CLI Example:
<a name="bda-library-listing-entities-cli"></a>

**Request**

```
aws bedrock-data-automation list-data-automation-library-entities \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary" \
    --entity-type "VOCABULARY" \
    --max-results 50
```

**Response**

```
{
    "entities": [
        {
            "vocabulary": {
                "entityId": "medical-en",
                "language": "EN",
                "numOfPhrases": 2,
                "lastModifiedTime": "2026-03-06T07:06:00.413000+00:00"
            }
        }
    ]
}
```

## AWS Console Example:
<a name="bda-library-listing-entities-console"></a>

1. Navigate to the "Library details" page for your library

![Custom vocabulary lists table showing medical-en list with English language and 2 phrases.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-list-entities-console.png)
