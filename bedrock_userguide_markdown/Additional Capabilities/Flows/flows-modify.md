

# Modify a flow in Amazon Bedrock
<a name="flows-modify"></a>

To learn how to modify a flow, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To modify the details of a flow**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Amazon Bedrock Flows** from the left navigation pane. Then, in the **Amazon Bedrock Flows** section, select a flow.

1. In the **Flow details** section, choose **Edit**. 

1. You can edit the name, description, and associate a different service role for the flow.

1. Select **Save changes**.

**To modify a flow**

1. If you're not already in the **flow builder**, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Amazon Bedrock Flows** from the left navigation pane. Then, choose a flow in the **Amazon Bedrock Flows** section.

   1. Choose **Edit in flow builder**.

1. Add, remove, and modify nodes and connections as necessary. For more information, refer to [Create and design a flow in Amazon Bedrock](flows-create.md) and [Node types for your flow](flows-nodes.md).

1. When you're done modifying your flow, choose **Save** or **Save and exit**.

------
#### [ API ]

To edit a flow, send an [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include both fields that you want to maintain and fields that you want to change. For considerations on the fields in the request, see [Create and design a flow in Amazon Bedrock](flows-create.md).

------