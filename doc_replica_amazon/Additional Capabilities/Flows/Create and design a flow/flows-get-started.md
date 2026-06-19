

# Create your first flow in Amazon Bedrock
<a name="flows-get-started"></a>

Whenever you create a flow, the Amazon Bedrock console creates a getting started flow for you. The flow includes with a **Flow input** node, a **Prompt** node and a **Flow output** node. When you run the flow, you enter a topic for the flow which uses the prompt node to summarize the topic. Before you can run the flows, you need to set the model for the prompt. 

To create a flow, you provide a name and description for the flow. By default Amazon Bedrock creates a service role with the proper permissions. Optionally, you can specify an existing service role.

Amazon Bedrock encrypts your data at rest. By default, Amazon Bedrock encrypts this data using an AWS managed key. Optionally, you can encrypt the flow execution data using a customer managed key. For more information, see [Encryption of Amazon Bedrock Flows resources](encryption-flows.md).

After you finish with the getting started flow, or if you don't need it, you can continue building your flow. We recommend that you read [How Amazon Bedrock Flows works](flows-how-it-works.md) to familiarize yourself with concepts and terms in Amazon Bedrock Flows and to learn about the types of nodes that are available to you. For more information, see [Design a flow in Amazon Bedrock](flows-design.md).

**To create your first flow**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Amazon Bedrock Flows** from the left navigation pane.

1. In the **Amazon Bedrock Flows** section, choose **Create flow**.

1. Enter a **Name** for the flow and an optional **Description**.

1. For the **Service role name**, choose one of the following options:
   + **Create and use a new service role** – Let Amazon Bedrock create a service role for you to use.
   + **Use an existing service role ** – Select a custom service role that you set up previously. For more information, see [Create a service role for Amazon Bedrock Flows in Amazon Bedrock](flows-permissions.md).

1. (Optional) Encrypt your flow with a customer managed key by doing the following: 

   1. Select **Additional configurations**.

   1. In **KMS key selection**, select **Customize encryption settings (advanced)**. Then do one of the following in **Choose an AWS KMS key**:
      + To use an existing key, enter the ARN or find the key that you want to use. 
      + To create a new key, choose **Create an AWS KMS key** to open the AWS Key Management Service console and [create the key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html). When you create the key, note the ARN for key. Back in the Amazon Bedrock console, enter the ARN for the key in **Choose an AWS KMS key**.

   For more information, see [Encryption of Amazon Bedrock Flows resources](encryption-flows.md)

1. Choose **Create**. Amazon Bedrock creates the getting started flow and takes you to the **flow builder**.

1. In the **flow builder** section, note that the center pane (canvas) displays a **Flow input** node, a **Prompt** node and a **Flow output**. The nodes are already connected together. 

1. In the canvas, select the **prompt** node.

1. In the flow builder pane, select the **Configurations** section.

1. Under **Node name**, make sure the **Define in node** is selected.

1. In **Select a model**, select a model to use.

1. Choose **Save** to save your flow.

1. In the **Test flow** pane on the right, enter a topic for the flow to summarize.

1. Choose **Run** to run the flow. The flow displays the summarized topic.