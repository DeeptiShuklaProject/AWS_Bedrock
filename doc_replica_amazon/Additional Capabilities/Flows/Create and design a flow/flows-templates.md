

# Use a template to create an Amazon Bedrock flow
<a name="flows-templates"></a>

To help you get started with defining and orchestrating Amazon Bedrock Flows, you can use templates to create flows for a variety of flow configurations. For example, you can use a template to see a flow that includes a knowledge base or a flow that uses conditions to direct flow logic. 

You access the templates from the [Amazon Bedrock Flows Samples](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file) GitHub repository. The Amazon Bedrock console also provides a link to the repository from the canvas page for a flow. 

The flow templates are provided as [JSON templates](https://github.com/aws-samples/amazon-bedrock-flows-samples/tree/main/templates) for each supported flow definition and a Python script that you use to create and run the flow. You can also access the flow from the Amazon Bedrock console.

The repository provides the following templates:
+  [Knowledege base flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#1-knowledgebase-flow-1) – Shows how to integrate and query a [knowledge base](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#1-knowledgebase-flow-1), including RAG (Retrieval Augmented Generation) and Knowledge base search and retrieval.
+  [Multi-turn Conversation agent flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#2-multi-turn-conversation-agent-flow-1) – Shows how to perform interactive, stateful conversations with a flow. For more information, see [Converse with an Amazon Bedrock flow](flows-multi-turn-invocation.md).
+  [Conditions Flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#3-conditions-flow-1) – Shows how to perform conditional logic and branching within a flow. 
+ [ Prompt Node with Guardrail Flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#4-prompt-node-with-guardrail-flow-1) – Shows how to safeguard a prompt node with a guardrail.
+  [Iterator and Collector Flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#5-iterator--collector-flow-1) – Shows how to process multiple inputs and aggregate responses.
+  [Multi-agent flow](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#5-iterator--collector-flow-1) – Shows various agent-based workflows, including multi-agent collaboration and task delegation.

Before you can run the script you need to create the Amazon Bedrock resources, such as a knowledge base or agent, that the flow uses. It is your responsibility to delete the these resources when you no longer need them. 

To create and run a flow from a template, you run the script (`flow_manager.py`). The script prompts for any additional information that it needs, such as the flow template you want to use and identifiers for resources that the template needs. You can include a test prompt to try with the flow.

Optionally, you can set the AWS Region that you want the flow to be created in. The script creates the necessary resources with a default set of [IAM role permissions](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#iam-role-permissions). You can also choose to use an IAM role that you create.

If you want to use the flow in the Amazon Bedrock console, don't use the `--cleanup` parameter as this deletes the flow after the script runs the flow. If you don't use `--cleanup`, you will have to delete the flow, when you no longer need it. 

For more information, see [https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file\#how-to-use](https://github.com/aws-samples/amazon-bedrock-flows-samples?tab=readme-ov-file#how-to-use).

