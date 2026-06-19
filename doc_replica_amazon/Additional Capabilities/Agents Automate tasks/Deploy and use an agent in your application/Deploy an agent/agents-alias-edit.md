

# Edit an alias of an agent in Amazon Bedrock
<a name="agents-alias-edit"></a>

To learn how to edit an alias of an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To edit an alias**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. In the **Aliases** section, choose the option button next to the alias that you want to edit. Then choose **Edit**

1. Edit any of the existing fields as necessary. For more information about these fields, see [Deploy and use an Amazon Bedrock agent in your application](agents-deploy.md).

1. Select **Save**.

**To add or remove tags associated with an alias**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose the alias for which you want to manage tags from the **Aliases** section.

1. In the **Tags** section, choose **Manage tags**.

1. To add a tag, choose **Add new tag**. Then enter a **Key** and optionally enter a **Value**. To remove a tag, choose **Remove**. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

1. When you're done editing tags, choose **Submit**.

------
#### [ API ]

To edit an agent alias, send an [UpdateAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentAlias.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same.

To add tags to an alias, send a [TagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_TagResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and include the Amazon Resource Name (ARN) of the alias. The request body contains a `tags` field, which is an object containing a key-value pair that you specify for each tag.

To remove tags from an alias, send an [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UntagResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and include the Amazon Resource Name (ARN) of the alias. The `tagKeys` request parameter is a list containing the keys for the tags that you want to remove.

------