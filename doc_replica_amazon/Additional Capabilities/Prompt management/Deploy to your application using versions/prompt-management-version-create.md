

# Create a version of a prompt in Prompt management
<a name="prompt-management-version-create"></a>

To learn how to create a version of your prompt, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

If you're in the prompt builder, you can create a version of your prompt by choosing **Create version**. Otherwise, do the following:

**To create a version of your prompt**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane. Then, choose a prompt in the **Prompts** section.

1. In the **Prompt versions** section, choose **Create version** to take a snapshot of your draft version.

------
#### [ API ]

To create a version of your prompt, send a [CreatePromptVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreatePromptVersion.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the prompt as the `promptIdentifier`.

The response returns an ID and ARN for the version. Versions are created incrementally, starting from 1.

------