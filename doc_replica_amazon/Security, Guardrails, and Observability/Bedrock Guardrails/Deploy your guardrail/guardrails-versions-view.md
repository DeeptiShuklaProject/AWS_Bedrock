

# View information about guardrail versions
<a name="guardrails-versions-view"></a>

To view information about a version or versions of a guardrail, select one of the tabs below and follow the steps indicated:

------
#### [ Console ]

**To view information about your guardrail versions**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Choose **Guardrails** from the left navigation pane. Then, select a guardrail in the **Guardrails** section.

1. In the **Versions** section, select a version to view information about it.

------
#### [ API ]

To get information about a guardrail version, send a [GetGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetGuardrail.html) request and include the ID and version of the guardrail. If you don't specify a version, the response returns details for the `DRAFT` version.

The following is the request format:

```
GET /guardrails/{{guardrailIdentifier}}?guardrailVersion={{guardrailVersion}} HTTP/1.1
```

The following is the response format:

```
HTTP/1.1 200
Content-type: application/json

{
   "blockedInputMessaging": "string",
   "blockedOutputsMessaging": "string",
   "contentPolicy": { 
      "filters": [ 
         { 
            "inputStrength": "NONE | LOW | MEDIUM | HIGH",
            "outputStrength": "NONE | LOW | MEDIUM | HIGH",
            "type": "SEXUAL | VIOLENCE | HATE | INSULTS | MISCONDUCT | PROMPT_ATTACK"
         }
      ]
   },
    "wordPolicy": {
    "words": [
      {
        "text": "string"
      }
    ],
    "managedWordLists": [
      {
        "type": "string"
      }
    ]
  },
  "sensitiveInformationPolicy": {
    "piiEntities": [
      {
        "type": "string",
        "action": "string"
      }
    ],
    "regexes": [
      {
        "name": "string",
        "description": "string",
        "pattern": "string",
        "action": "string"
      }
    ]
  },
   "createdAt": "string",
   "description": "string",
   "failureRecommendations": [ "string" ],
   "guardrailArn": "string",
   "guardrailId": "string",
   "kmsKeyArn": "string",
   "name": "string",
   "status": "string",
   "statusReasons": [ "string" ],
   "topicPolicy": { 
      "topics": [ 
         { 
            "definition": "string",
            "examples": [ "string" ],
            "name": "string",
            "type": "DENY"
         }
      ]
   },
   "updatedAt": "string",
   "version": "string"
}
```

To list information about all your guardrails, send a [ListGuardrails](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListGuardrails.html) request.

The following is the request format:

```
GET /guardrails?guardrailIdentifier={{guardrailIdentifier}}&maxResults={{maxResults}}&nextToken={{nextToken}} HTTP/1.1
```
+ To list the `DRAFT` version of all your guardrails, don't specify the `guardrailIdentifier` field.
+ To list all versions of a guardrail, specify the ARN of the guardrail in the `guardrailIdentifier` field.

You can set the maximum number of results to return in a response in the `maxResults` field. If there are more results than the number you set, the response returns a `nextToken` that you can send in another `ListGuardrails` request to see the next batch of results.

The following is the response format:

```
HTTP/1.1 200
Content-type: application/json

{
   "guardrails": [ 
      { 
         "arn": "string",
         "createdAt": "string",
         "description": "string",
         "id": "string",
         "name": "string",
         "status": "string",
         "updatedAt": "string",
         "version": "string"
      }
   ],
   "nextToken": "string"
}
```

------