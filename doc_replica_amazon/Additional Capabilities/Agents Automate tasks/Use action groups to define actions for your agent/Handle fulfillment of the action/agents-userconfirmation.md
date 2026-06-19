

# Get user confirmation before invoking action group function
<a name="agents-userconfirmation"></a>

You can safeguard your application from malicious prompt injections by requesting confirmation from your application users before invoking the action group function. When an end user interacts with your application, Amazon Bedrock Agent figures out the API or knowledge bases to invoke to automate the task for the user. The information from the API or knowledge bases might contain potentially damaging data. Between each iteration if the response contains any instruction, the agent will comply. If the response includes instructions for the model to invoke unintended actions, the agent will go ahead and comply with the instruction. To ensure that certain actions are implemented only after explicit user consent, we recommend that you request confirmation from the end user before invoking the function. 

When you configure your action group, you can choose to enable user confirmation for specific actions. If user confirmation is enabled for an action, agent responds with a confirmation question asking end user to either confirm or deny the action. You can enable user confirmation in the console, using the CLI, or using the SDK. 

To enable user confirmation for an action, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

## How user confirmation works
<a name="user-confirmation-works"></a>

The user confirmation is configured for an action in the action group by the agent developer. If the agent decides that it should call that action, the API or the function details elicited from the user and the user confirmation configured by the agent developer will be returned in the `invocationInputs` field in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response, alongside `invocationType`, and an unique `invocationId`.

The agent invokes the API or the function that was provided in the `invocationInputs`. If the user confirmation is enabled for the function or the API, the user is presented with an option to **CONFIRM** or **DENY** the action mentioned in the response.

The results from the agent’s invocation of the function or API is sent in another [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request, in the `sessionState` field, to provide context to the agent. The request parameter for `InvokeAgent` uses `returnControlInvocationResults`, which is a list of map to `apiResult` or `functionResult` objects. The `apiResult` and `functionResult` objects have an additional field of `confirmationState`. This field has the user confirmation response. 

If the user response is **CONFIRM**, the function or the API in the response is implemented. 

If the user response is **DENY**, the function or the API in the response is not implemented. 

## Examples of the InvokeAgent response and request
<a name="agents-userconfirmation-ex"></a>

**Response**

```
HTTP/1.1 200
x-amzn-bedrock-agent-content-type: contentType
x-amz-bedrock-agent-session-id: sessionId
Content-type: application/json

{
   "chunk": { 
      ...
   },
   ...
   "returnControl": { 
      "invocationId": "string",
      "invocationInputs": [ 
         { ... }
      ]
   },
   "trace": { 
      "agentAliasId": "string",
      "agentId": "string",
      "agentVersion": "string",
      "sessionId": "string",
      "trace": { ... }
   },
}
```

**Request**

```
POST /agents/agentId/agentAliases/agentAliasId/sessions/sessionId/text HTTP/1.1
Content-type: application/json

{
   "enableTrace": boolean,
   "endSession": boolean,
   "inputText": "string",
   "sessionState": { 
      "invocationId": "string",
      "promptSessionAttributes": { 
         "string" : "string" 
      },
      "returnControlInvocationResults": [ 
         { ... }
      ],
      "sessionAttributes": { 
         "string" : "string" 
      }
   }
}
```