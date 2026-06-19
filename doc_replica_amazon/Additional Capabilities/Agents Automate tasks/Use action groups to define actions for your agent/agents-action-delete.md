

# Delete an action group
<a name="agents-action-delete"></a>

To learn how to delete an action group, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To delete an action group**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**

1. In the **Action groups** section, choose the option button that's next to the action group you want to delete.

1. A dialog box appears warning you about the consequences of deletion. To confirm that you want to delete the action group, enter **delete** in the input field and then select **Delete**.

1. When deletion is complete, a success banner appears.

1. To apply the changes that you made to the agent before testing it, choose **Prepare** in the **Test** window or at the top of the **Working draft** page.

------
#### [ API ]

To delete an action group, send a [DeleteAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteAgentActionGroup.html) request. Specify the `actionGroupId` and the `agentId` and `agentVersion` from which to delete it. By default, the `skipResourceInUseCheck` parameter is `false` and deletion is stopped if the resource is in use. If you set `skipResourceInUseCheck` to `true`, the resource will be deleted even if the resource is in use.

To apply the changes to the working draft, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include the `agentId` in the request. The changes apply to the `DRAFT` version, which the `TSTALIASID` alias points to.

------