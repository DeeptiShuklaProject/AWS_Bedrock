

# Delete an alias of a flow in Amazon Bedrock
<a name="flows-alias-delete"></a>

To learn how to delete an alias of flow, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To delete an alias**

1. Open the [AWS Management Console](https://console.aws.amazon.com) and sign in to your account. Navigate to Amazon Bedrock.

1. Select **Flows** from the left navigation pane. Then, in the **Flows** section, select a flow.

1. To choose the alias for deletion, in the **Aliases** section, choose the option button next to the alias that you want to delete.

1. Choose **Delete**.

1. A dialog box appears warning you about the consequences of deletion. To confirm that you want to delete the alias, enter **delete** in the input field and choose **Delete**.

1. A banner appears to inform you that the alias is being deleted. When deletion is complete, a success banner appears.

------
#### [ API ]

To delete a flow alias, send a [DeleteFlowAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteFlowAlias.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the ARN or ID of the flow in the `flowIdentifier` field and the ARN or ID of the alias to delete in the `aliasIdentifier` field.

------