

# Options for handling harmful content detected by Amazon Bedrock Guardrails
<a name="guardrails-harmful-content-handling-options"></a>

You can configure what actions your Amazon Bedrock guardrail takes at runtime when it detects harmful content in prompts (`inputAction`) and responses (`outputAction`).

Guardrails filtering policies support the following actions when harmful content is detected in model inputs and responses:
+ **Block** – Block the content and replace it with blocked messaging.
+ **Mask** – Anonymize the content and replace it with identifier tags (such as `{NAME}` or `{EMAIL}`).

  This option is available only with sensitive information filters. For more information, see [Remove PII from conversations by using sensitive information filters](guardrails-sensitive-filters.md).
+ **Detect** – Take no action but return what the guardrail detects in the trace response. Use this option, known as *detect mode*, to help evaluate whether your guardrail is working the way that you expect.

## Guardrail evaluation with detect mode
<a name="guardrails-harmful-content-handling-options-examples"></a>

Amazon Bedrock Guardrails policies support detect mode, which lets you evaluate your guardrail's performance without applying any action (such as blocking the content).

Using detect mode offers the following benefits:
+ Test different combinations and strengths of your guardrail's policies without impacting the customer experience.
+ Analyze any false positives or negatives and adjust your policy configurations accordingly.
+ Deploy your guardrail only after confirming it works as expected.

## Example: Using detect mode to evaluate content filters
<a name="guardrails-detect-mode-example"></a>

For example, let's say you configure a policy with a content filter strength of `HIGH`. Based on this setting, your guardrail will block content even if it returns a confidence of `LOW` in its evaluation.

To understand this behavior (and make sure that your application doesn't block content you aren't expecting it to), you can configure the policy action as `NONE`. The trace response might look like this:

```
{
    "assessments": [{
        "contentPolicy": {
            "filters": [{
                "action": "NONE",
                "confidence": "LOW",
                "detected": true,
                "filterStrength": "HIGH",
                "type": "VIOLENCE"
            }]
        }
    }]
}
```

This allows you to preview the guardrail evaluation and see that `VIOLENCE` was detected (`true`), but no action was taken because you configured that to `NONE`.

If you don't want to block that text, you might tune the filter strength to `MEDIUM` or `LOW` and redo the evaluation. Once you get the results you're looking for, you can update your policy action to `BLOCK` or `ANONYMIZE`.