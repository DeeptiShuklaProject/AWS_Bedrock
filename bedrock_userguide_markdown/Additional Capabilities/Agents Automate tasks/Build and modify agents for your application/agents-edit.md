

# Modify an agent
<a name="agents-edit"></a>

After you create an agent, you can update its configuration as required. The configuration applies to the working draft.

To learn how to modify an agent, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To edit an agent's configuration or its components**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent Builder**

1. Edit the existing information in the **Agent details** section, or choose **Add**, **Edit**, or **Delete** in any of the other subsections and modify as necessary. To edit an action group or knowledge base, select it in the respective section. For more information about the components of the agent that you can edit, see [Create and configure agent manually](agents-create.md).
**Note**  
If you change the foundation model, any [prompt templates](advanced-prompts.md) that you modified will be set to default for that model.

1. When you're done editing the information, choose **Save** to remain in the same window or **Save and exit** to return to the agent details page. A success banner appears at the top. To apply the new configurations to your agent, select **Prepare** in the test window.

**To edit the tags associated with an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose an agent in the **Agents** section.

1. In the **Tags** section, choose **Manage tags**.

1. To add a tag, choose **Add new tag**. Then enter a **Key** and optionally enter a **Value**. To remove a tag, choose **Remove**. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

1. When you're done editing tags, choose **Submit**.

------
#### [ API ]

To modify an agent, send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same. For more information about required and optional fields, see [Create and configure agent manually](agents-create.md).

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

To add tags to an agent, send a [TagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_TagResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and include the Amazon Resource Name (ARN) of the agent. The request body contains a `tags` field, which is an object containing a key-value pair that you specify for each tag.

To remove tags from an agent, send an [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UntagResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and include the Amazon Resource Name (ARN) of the agent. The `tagKeys` request parameter is a list containing the keys for the tags that you want to remove.

------