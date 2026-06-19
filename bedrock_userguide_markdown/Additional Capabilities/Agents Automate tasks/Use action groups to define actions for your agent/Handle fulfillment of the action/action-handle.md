

# Handle fulfillment of the action
<a name="action-handle"></a>

When you configure the action group, you also select one of the following options for the agent to pass the information and parameters that it receives from the user:
+ Add user input to your agent's action group. With user input, agent can [request user for more information](agents-user-input.md) if it doesn't have enough information to complete a task. 
+ Pass to a [Lambda function that you create](agents-lambda.md) to define the business logic for the action group.
+ Skip using a Lambda function and [return control](agents-returncontrol.md) by passing the information and parameters from the user in the `InvokeAgent` response. The information and parameters can be sent to your own systems to yield results and these results can be sent in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState) of another [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request.
+ Enable user confirmation for an action. Enabling user confirmation can safeguard your application from malicious prompt injections by [requesting confirmation from your application users](agents-userconfirmation.md) before invoking the action group function. 

Select a topic to learn how to configure how fulfillment of the action group is handled after the necessary information has been elicited from the user.

**Topics**
+ [Configure Lambda functions to send information that an Amazon Bedrock agent elicits from the user](agents-lambda.md)
+ [Return control to the agent developer by sending elicited information in an InvokeAgent response](agents-returncontrol.md)
+ [Get user confirmation before invoking action group function](agents-userconfirmation.md)