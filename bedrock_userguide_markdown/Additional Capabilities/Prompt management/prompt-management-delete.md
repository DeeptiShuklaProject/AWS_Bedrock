

# Delete a prompt in Prompt management
<a name="prompt-management-delete"></a>

If you no longer need a prompt, you can delete it. Prompts that you delete are retained in the AWS servers for up to fourteen days. To learn how to delete a prompt using Prompt management, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

If you're in the **Prompt details** page for a prompt or in the prompt builder, choose **Delete** to delete a prompt.

**Note**  
If you delete a prompt, all its versions will also be deleted. Any resources using your prompt might experience runtime errors. Remember to disassociate the prompt from any resources using it.

**To delete a prompt**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane.

1. Select a prompt and choose **Delete**.

1. Review the warning that appears, type **confirm**, and then choose **Delete**.

------
#### [ API ]

To delete a prompt, send a [DeletePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeletePrompt.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the prompt as the `promptIdentifier`. To delete a specific version of the prompt, specify the version number in the `promptVersion` field.

------