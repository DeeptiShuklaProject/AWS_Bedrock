

# Design a flow in Amazon Bedrock
<a name="flows-design"></a>

In this section you design an Amazon Bedrock flow. Before designing a flow, we recommend that you read [How Amazon Bedrock Flows works](flows-how-it-works.md) to familiarize yourself with concepts and terms in Amazon Bedrock Flows and to learn about the types of nodes that are available to you. For example flows that you can try, see [Try example flows](flows-ex.md).

**To build your flow**

1. If you're not already in the **flow builder**, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Amazon Bedrock Flows** from the left navigation pane. Then, choose a flow in the **Amazon Bedrock Flows** section.

   1. Choose **Edit in flow builder**.

1. In the **flow builder** section, the center pane displays a **Flow input** node and a **Flow output** node. These are the input and output nodes for your flow.

1. Do the following to add and configure nodes:

   1. In the **Flow builder** pane, select **Nodes**.

   1. Drag a node you want to use for the first step of your flow and drop it in the center pane.

   1. The circles on the nodes are connection points. To connect your flow input node to the second node, drag a line from the circle on the **Flow input** node to the circle in the **Input** section of the node you just added.

   1. Select the node you just added.

   1. In the **Configure** section of the **Flow builder** pane, provide the configurations for the selected node and define names, data types, and expressions for the inputs and outputs of the node.

   1. In the **Flow builder** pane, select **Nodes**.

   1. Repeat steps to add and configure nodes the remaining nodes in your flow.
**Note**  
If you use a service role that Amazon Bedrock automatically created for you, the role will update with the proper permissions as you add nodes. If you use a custom service role however, you must add the proper permissions to the policy attached to your service role by referring to [Create a service role for Amazon Bedrock Flows in Amazon Bedrock](flows-permissions.md).

1. Connect the **Output** of the last node in your flow with the **Input** of the **Flow output** node. You can have multiple **Flow output** nodes. To add additional flow output nodes, drag the **Flow output** node and drop it next to the node where you want the flow to stop. Make sure to draw connections between the two nodes.

1. Continue to the next procedure to [Test a flow in Amazon Bedrock](flows-test.md) or come back later. To continue to the next step, choose **Save**. To come back later, choose **Save and exit**.

**Delete a node or a connection**

During the process of building your flow, you might need to delete a node or remove node connections.

**To delete a node**

1. Select a node you want to delete.

1. In the **Flow builder** pane, choose the delete icon (![Trash can icon representing a delete action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/trash.png)).
**Note**  
If you use a service role that Amazon Bedrock automatically created for you, the role will update with the proper permissions as you add nodes. If you delete nodes, however, the relevant permissions won't be deleted. We recommend that you delete the permissions that you no longer need by following the steps at [Modifying a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_modify.html).

**To remove a connection**
+ In the **Flow builder** page, hover over the connection you want to remove until you see the expand icon and then drag the connection away from the node.

The following requirements apply to building a flow:
+ Your flow must have only one flow input node and at least one flow output node.
+ You can't include inputs for a flow input node.
+ You can't include outputs for a flow output node.
+ Every output in a node must be connected to an input in a downstream node (in the API, this is done through a [FlowConnection](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConnection.html) with a [FlowDataConnectionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowDataConnectionConfiguration.html)).
+ Every condition (including the default one) in a condition node must be connected to a downstream node (in the API, this is done through a [FlowConnection](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConnection.html) with a [FlowConditionalConnectionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConditionalConnectionConfiguration.html)).

The following pointers apply to building a flow:
+ Begin by setting the data type for the output of the flow input node. This data type should match what you expect to send as the input when you invoke the flow.
+ When you define the inputs for a flow using expressions, check that the result matches the data type that you choose for the input.
+ If you include an iterator node, include a collector node downstream after you've sent the output through the nodes that you need. The collector node will return the outputs in an array.