

# Key definitions for Amazon Bedrock Flows
<a name="key-definitions-flow"></a>

The following list introduces you to the basic concepts of Amazon Bedrock Flows.
+ **Flow** – A flow is a construct consisting of a name, description, permissions, a collection of nodes, and connections between nodes. When a flow is invoked, the input in the invocation is sent through each node of the flow until an output node is reached. The response of the invocation returns the final output.
+ **Node** – A node is a step inside a flow. For each node, you configure its name, description, input, output, and any additional configurations. The configuration of a node differs based on its type. To learn more about different node types, see [Node types for your flow](flows-nodes.md).
+ **Connection** – There are two types of connections used in Amazon Bedrock Flows:
  + A **data connection** is drawn between the output of one node (the *source node*) and the input of another node (the *target node*) and sends data from an upstream node to a downstream node. In the Amazon Bedrock console, data connections are solid gray lines.
  + A **conditional connection** is drawn between a condition in a condition node and a downstream node and sends data from the node that precedes the condition node to a downstream node if the condition is fulfilled. In the Amazon Bedrock console, conditional connections are dotted purple lines.
+ **Expressions** – An expression defines how to extract an input from the whole input entering a node. To learn how to write expressions, see [Use expressions to define inputs by extracting the relevant part of a whole input in Amazon Bedrock FlowsDefine inputs with expressions](flows-expressions.md).
+ **Flow builder** – The Flow builder is a tool on the Amazon Bedrock console to build and edit flows through a visual interface. You use the visual interface to drag and drop nodes onto the interface and configure inputs and outputs for these nodes to define your flow.
+ In the following sections, we will use the following terms:
  + **Whole input** – The entire input that is sent from the previous node to the current node.
  + **Upstream** – Refers to nodes that occur earlier in the flow.
  + **Downstream** – Refers to nodes that occur later in the flow.
  + **Input** – A node can have multiple inputs. You use expressions to extract the relevant parts of the whole input to use for each individual input. In the Amazon Bedrock console flow builder, an input appears as a circle on the left edge of a node. Connect each input to an output of an upstream node.
  + **Output** – A node can have multiple outputs. In the Amazon Bedrock console flow builder, an output appears as a circle on the right edge of a node. Connect each output to at least one input in a downstream node.
  + **Branch** – If an output from a node is sent to more than one node, or if a condition node is included, the path of a flow will split into multiple branches. Each branch can potentially yield another output in the flow invocation response.