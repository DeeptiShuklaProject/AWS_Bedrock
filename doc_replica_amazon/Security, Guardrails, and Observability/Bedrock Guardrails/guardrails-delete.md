

# Delete your guardrail
<a name="guardrails-delete"></a>

You can delete a guardrail when you no longer need to use it. Be sure to disassociate the guardrail from all the resources or applications that use it before you delete the guardrail. You can delete your guardrails by following these steps for the AWS Console or API:

------
#### [ Console ]

**To delete a guardrail**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Choose **Guardrails** from the left navigation pane. Then, select a guardrail in the **Guardrails** section.

1. In the **Guardrails** section, select a guardrail that you want to delete and then choose **Delete**.

1. Enter **delete** in the user input field and choose **Delete** to delete the guardrail.

------
#### [ API ]

To delete a guardrail, send a [DeleteGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteGuardrail.html) request and only specify the ARN of the guardrail in the `guardrailIdentifier` field. Don't specify the `guardrailVersion`

The following is the request format:

```
DELETE /guardrails/{{guardrailIdentifier}}?guardrailVersion={{guardrailVersion}} HTTP/1.1
```

**Warning**  
If you delete a guardrail, all of its versions will be deleted.

If the deletion is successful, the response returns an HTTP 200 status code.

------