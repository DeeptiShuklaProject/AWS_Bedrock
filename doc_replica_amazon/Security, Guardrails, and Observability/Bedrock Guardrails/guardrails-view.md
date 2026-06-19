

# View information about your guardrails
<a name="guardrails-view"></a>

You can view information about your guardrails by following these steps for the AWS Console or API:

------
#### [ Console ]

**To view information about your guardrails versions and settings**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Choose **Guardrails** from the left navigation pane. Then, select a guardrail in the **Guardrails** section.

1. The **Guardrail overview** section displays the configurations of the guardrail that apply to all versions.

1. To view more information about the working draft, select the **Working draft** in the **Working draft** section.

1. To view more information about a specific version of the guardrail, select the version from the **Versions** section.

To learn more about the working draft and guardrail versions, see [Deploy your guardrail](guardrails-deploy.md).

------
#### [ API ]

To get information about a guardrail, send a [GetGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetGuardrail.html) request and include the ID and version of the guardrail. If you don't specify a version, the response returns details for the `DRAFT` version.

The following is the request format:

```
GET /guardrails/{{guardrailIdentifier}}?guardrailVersion={{guardrailVersion}} HTTP/1.1
```

The following is the response format:

```
HTTP/1.1 200
Content-type: application/json

{
  "topicPolicy": {
    "topics": [
      {
        "definition": "string",
        "examples": [
          "string"
        ],
        "name": "string",
        "type": "DENY"
      }
    ]
  },
  "contentPolicy": {
    "filters": [
      {
        "type": "string",
        "inputStrength": "string",
        "outputStrength": "string"
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
        "regex": "string",
        "action": "string"
      }
    ]
  },
  "contextualGroundingPolicy": {
    "groundingFilter": {
      "threshold": float
    },
    "relevanceFilter": {
      "threshold": float
    }
  },
  "createdAt": "string",
  "blockedInputMessaging": "string",
  "blockedOutputsMessaging": "string",
  "description": "string",
  "failureRecommendations": [
    "string"
  ],
  "guardrailArn": "string",
  "guardrailId": "string",
  "kmsKeyArn": "string",
  "name": "string",
  "status": "string",
  "statusReasons": [
    "string"
  ],
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