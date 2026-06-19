

# Modify an action group
<a name="agents-action-edit"></a>

To learn how to modify an action group, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To modify an action group**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**

1. In the **Action groups** section, select an action group to edit. Then choose **Edit**.

1. Edit the existing fields as necessary. For more information, see [Use action groups to define actions for your agent to perform](agents-action-create.md).

1. To define the schema for the action group with the in-line OpenAPI schema editor, for **Select API schema**, choose **Define with in-line OpenAPI schema editor**. A sample schema appears that you can edit. You can configure the following options:
   + To import an existing schema from Amazon S3 to edit, choose **Import schema**, provide the Amazon S3 URI, and select **Import**.
   + To restore the schema to the original sample schema, choose **Reset** and then confirm the message that appears by choosing **Confirm**.
   + To select a different format for the schema, use the dropdown menu labeled **JSON**.
   + To change the visual appearance of the schema, choose the gear icon below the schema.

1. To control whether the agent can use the action group, select **Enable** or **Disable**. Use this function to help troubleshoot your agent's behavior.

1. To remain in the same window so that you can test your change, choose **Save**. To return to the action group details page, choose **Save and exit**.

1. A success banner appears if there are no issues. If there are issues validating the schema, an error banner appears. To see a list of errors, choose **Show details** in the banner.

1. To apply the changes that you made to the agent before testing it, choose **Prepare** in the **Test** window or at the top of the **Working draft** page.

------
#### [ API ]

To modify an action group, send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same. You must specify the `agentVersion` as `DRAFT`. For more information about required and optional fields, see [Use action groups to define actions for your agent to perform](agents-action-create.md).

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

------