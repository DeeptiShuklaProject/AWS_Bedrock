

# Include guardrails in your flow in Amazon Bedrock
<a name="flows-guardrails"></a>

Amazon Bedrock Flows integrates with Amazon Bedrock Guardrails to let you identify and block or filter unwanted content in your flow. To learn how to apply guardrails to supported node types in a flow, see the following table:


****  

| Node type | Console | API | 
| --- | --- | --- | 
| Prompt node | When you [create](flows-create.md) or [update](flows-modify.md) a flow, select the prompt node and specify the guardrail in the Configure section. | When you define the prompt node in the nodes field in a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request, include a guardrailConfiguration field in the [PromptFlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptFlowNodeConfiguration.html). | 
| Knowledge base node | When you [create](flows-create.md) or [update](flows-modify.md) a flow, select the knowledge base node and specify the guardrail in the Configure section. You can only include a guardrail when generating responses based on retrieved results. | When you define the knowledge base node in the nodes field in a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request, include a guardrailConfiguration field in the [KnowledgeBaseFlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_KnowledgeBaseFlowNodeConfiguration.html). You can only include a guardrail when using RetrieveAndGenerate so you must include a modelId. | 

For more information about guardrails, see [Detect and filter harmful content by using Amazon Bedrock Guardrails](guardrails.md).

For more information about node types, see [Node types for your flow](flows-nodes.md).