

# Use cases for Amazon Bedrock Guardrails
<a name="guardrails-use"></a>

After you create a guardrail, you can apply with the following features:
+ [Model inference](inference.md) – Apply a guardrail to submitted prompts and generated responses when running inference on a model.
+ [Agents](agents.md) – Associate a guardrail with an agent to apply it to prompts sent to the agent and responses returned from it.
+ [Knowledge base](knowledge-base.md) – Apply a guardrail when querying a knowledge base and generating responses from it.
+ [Flow](flows.md) – Add a guardrail to a prompt node or knowledge base node in a flow to apply it to inputs and outputs of these nodes.

The following table describes how to include a guardrail for each of these features using the AWS Management Console or the Amazon Bedrock API.


****  

| Use case | Console | API | 
| --- | --- | --- | 
| Model inference | Select the guardrail when [using a playground](playgrounds.md). | Specify in the header in an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) request or include in the guardrailConfig field in the body of a [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) request. | 
| Associate with an agent | When you [create or update](agents-build-modify.md) the agent, specify in the Guardrail details section of the Agent builder. | Include a guardrailConfiguration field in the body of a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request. | 
| Use when querying a knowledge base | Follow the steps in the [Guardrails](kb-test-config.md#kb-test-config-guardrails) section of the query configurations. Add a guardrail when you set Configurations. | Include a guardrailConfiguration field in the body of a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request. | 
| Include in a prompt node in a flow | When you [create](flows-create.md) or [update](flows-modify.md) a flow, select the prompt node and specify the guardrail in the Configure section. | When you define the prompt node in the nodes field in a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request, include a guardrailConfiguration field in the [PromptFlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptFlowNodeConfiguration.html). | 
| Include in a knowledge base node in a flow | When you [create](flows-create.md) or [update](flows-modify.md) a flow, select the knowledge base node and specify the guardrail in the Configure section. | When you define the knowledge base node in the nodes field in a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request, include a guardrailConfiguration field in the [KnowledgeBaseFlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_KnowledgeBaseFlowNodeConfiguration.html). | 

This section covers using a guardrail with model inference and the Amazon Bedrock API. You can use the base inference operations ([InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)) and the Converse API ([Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) and [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)). With both sets of operations you can use a guardrail with synchronous and streaming model inference. You can also selectively evaluate user input and can configure streaming response behavior. 

**Topics**
+ [Use your guardrail with inference operations to evaluate user input](guardrails-input-tagging-base-inference.md)
+ [Use the ApplyGuardrail API in your application](guardrails-use-independent-api.md)
+ [Use the InvokeGuardrailChecks API in your application](guardrails-use-invoke-guardrail-checks.md)