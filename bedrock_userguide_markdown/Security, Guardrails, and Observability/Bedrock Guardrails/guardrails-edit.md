

# Modify your guardrail
<a name="guardrails-edit"></a>

You can edit your guardrails by following these steps for the Amazon Bedrock console or API:

------
#### [ Console ]

**To edit a guardrail**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Choose **Guardrails** from the left navigation pane. Then, select a guardrail in the **Guardrails** section.

1. To modify your guardrail's details, select **Edit** in the **Guardrail Overview** section. When you're done, select **Save and exit**.

1. To edit your guardrail's tags, select **Manage tags**. When you're done, select **Save and exit**.

1. To modify the policies that your guardrail uses, select **Working Draft** and then **Edit** for each type of policy that you want to configure. When you're done making changes to your guardrail's policies, select **Save and exit**.

1. When you're done making changes to your guardrail, select **Save and exit**.

------
#### [ API ]

To edit a guardrail, send an [UpdateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UpdateGuardrail.html) request. Include both fields that you want to update as well as fields that you want to keep the same.

------

**Important**  
If you are using a guardrail version, you must create a new version after making changes to the guardrail's working draft. Changes to the working draft are not automatically reflected in existing versions. Create a new version and update your applications to use it.