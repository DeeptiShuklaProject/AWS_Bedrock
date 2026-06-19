

# Example configurations, results, and scores
<a name="guardrails-use-invoke-guardrail-checks-examples"></a>

The following blocks show each check's request configuration alongside the result it returns, including example scores.

**Content filter**

Content filter returns one entry per requested category, each with a `severityScore` between 0.0 and 1.0. A higher score indicates a stronger match to that category. You pick the threshold that counts as a violation. If you need a highly restricted experience to block content, set the threshold at the lower end.

```
// config
"contentFilter": {
  "categories": [
    { "category": "VIOLENCE" },
    { "category": "HATE" }
  ]
}
// result
"contentFilter": {
  "results": [
    { "category": "VIOLENCE", "severityScore": 0.8 },
    { "category": "HATE",     "severityScore": 0.2 }
  ]
}
```

**Prompt attack**

Prompt attack returns one entry per requested category with a `severityScore`.

```
// config
"promptAttack": {
  "categories": [
    { "category": "JAILBREAK" },
    { "category": "PROMPT_LEAKAGE" }
  ]
}
// result
"promptAttack": {
  "results": [
    { "category": "JAILBREAK",      "severityScore": 0.6 },
    { "category": "PROMPT_LEAKAGE", "severityScore": 0.2 }
  ]
}
```

**Sensitive information**

Sensitive information returns one entry per detected entity instance. Each entry has a `confidenceScore`, the `messageIndex` and `contentIndex` it appeared in, and the begin/end character offsets within that block, which is enough for client-side masking or redaction. Results are capped at a service-defined maximum; if more entities exist than the cap, `truncated` is `true`.

```
// config
"sensitiveInformation": {
  "entities": [
    { "type": "EMAIL" },
    { "type": "US_SOCIAL_SECURITY_NUMBER" },
    { "type": "CREDIT_DEBIT_CARD_NUMBER" }
  ]
}
// result
"sensitiveInformation": {
  "results": [
    {
      "type": "EMAIL",
      "confidenceScore": 0.8,
      "messageIndex": 0,
      "contentIndex": 0,
      "beginOffset": 12,
      "endOffset": 28
    }
  ],
  "truncated": false
}
```

Unlike the other checks, sensitive information findings scale with the content. Results are capped at a service-defined maximum of 1000 entities; if more entities exist than the cap, `truncated` is `true`. For exhaustive masking on very long content, run the check on smaller segments.