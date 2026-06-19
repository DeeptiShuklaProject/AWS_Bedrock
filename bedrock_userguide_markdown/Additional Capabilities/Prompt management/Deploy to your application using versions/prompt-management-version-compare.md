

# Compare versions of a prompt in Prompt management
<a name="prompt-management-version-compare"></a>

The Amazon Bedrock console offers a tool to let you compare versions of a prompt that you've created in Prompt management. The tool highlights fields that exist in one version that don't exist in the other.

**To compare prompt versions**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane. Then, choose a prompt in the **Prompts** section.

1. In the **Versions** section, select the checkboxes next to two prompts to compare.

1. Choose **Compare**.

1. The JSON objects defining each prompt version are shown side by side. Differences between the versions are shown as follows:
   + Fields that exist in one version, but don't exist in the other, are marked by a plus (\+) symbol and highlighted in green.
   + Fields that don't exist in one version, but exist in the other, are marked by a minus (-) symbol and highlighted in red.

1. To compare output model responses for the different versions, fill in the **Test variables** and choose **Run prompt**.