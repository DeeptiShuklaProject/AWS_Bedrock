

# Using the API
<a name="guardrails-use-invoke-guardrail-checks-using"></a>

To run guardrail checks, send an `InvokeGuardrailChecks` request to the Amazon Bedrock runtime endpoint.

## Request format
<a name="guardrails-use-invoke-guardrail-checks-request"></a>

```
{
  "messages": [
    {
      "role": "user",
      "content": [{ "text": "string" }]
    }
  ],
  "checks": {
    "contentFilter": {
      "categories": [
        { "category": "VIOLENCE | HATE | SEXUAL | INSULTS | MISCONDUCT" }
      ]
    },
    "promptAttack": {
      "categories": [
        { "category": "JAILBREAK | PROMPT_INJECTION | PROMPT_LEAKAGE" }
      ]
    },
    "sensitiveInformation": {
      "entities": [
        { "type": "EMAIL | PHONE | US_SOCIAL_SECURITY_NUMBER | ..." }
      ]
    }
  }
}
```
+ `messages` – Required. At least one message with one text content block.
+ `checks` – Required. At least one check field must be set.

## Response format
<a name="guardrails-use-invoke-guardrail-checks-response"></a>

```
{
  "results": {
    "contentFilter":        { "results": [ ... ] },
    "promptAttack":         { "results": [ ... ] },
    "sensitiveInformation": { "results": [ ... ], "truncated": false }
  },
  "usage": {
    "contentFilter":        { "textUnits": 0 },
    "promptAttack":         { "textUnits": 0 },
    "sensitiveInformation": { "textUnits": 0 }
  }
}
```

Only the checks you requested appear under `results` and `usage`. Each `textUnits` value is the number of text units the check evaluated. For the definition of a text unit, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).

## Errors
<a name="guardrails-use-invoke-guardrail-checks-errors"></a>

The following table lists the errors that the `InvokeGuardrailChecks` API can return.


**InvokeGuardrailChecks API errors**  

| HTTP code | Error | Cause | 
| --- | --- | --- | 
| 400 | ValidationException | The request is malformed, is missing required fields, or violates a constraint. | 
| 403 | AccessDeniedException | The caller isn't authorized to invoke the API. | 
| 429 | ThrottlingException | The request rate exceeded the account's quota. Retry with exponential backoff. | 
| 500 | InternalServerException | The service encountered an unexpected error. Retry the request. | 
| 503 | ServiceUnavailableException | The service is temporarily unavailable. Retry with exponential backoff. | 