

# Customize your Amazon Bedrock Agent's behavior with custom orchestration
<a name="agents-custom-orchestration"></a>

Amazon Bedrock provides you with an option to customize your agent’s orchestration strategy. Custom orchestration gives you full control of how you want your agents to handle multi-step tasks, make decisions, and execute workflows. 

With custom orchestration you can build Amazon Bedrock Agents that can implement orchestration logic that is specific to your use case. This includes complex orchestration workflows, verification steps, or multi-step processes where agents must perform several actions before arriving at a final answer. 

To use custom orchestration for your agent, create an AWS Lambda function that outlines your orchestration logic. The function controls how the agent responds to input by providing instructions to the Bedrock’s runtime process on when and how to invoke the model, when to invoke actions tools, and then determining the final response. 

Custom orchestration option is available across all AWS Regions where Amazon Bedrock Agents is available. 

You can configure custom orchestration in either the AWS Management Console or through the API. Before you proceed, make sure that you have your AWS Lambda function ready for testing.

------
#### [ Console ]

In the console, you can configure custom orchestration after you have created the agent. You configure them while editing the agent.

**To view or edit custom orchestration for your agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Agents**. Then choose an agent in the **Agents** section.

1. On the agent details page, in the **Working draft** section, select **Working draft**.

1. On the **Working draft** page, in the **Orchestration strategy** section, choose **Edit**.

1. On the **Orchestration strategy** page, in the **Orchestration strategy details** section, choose **Custom orchestration**.

1. For **Custom orchestration Lambda function**, choose the Lambda function from the dropdown menu and for **Function version**, choose the version.

1. To allow the agent to use the template when generating responses, turn on **Activate template**. If this configuration is turned off, the agent doesn't use the template.

1. A green banner appears at the top of the page indicating that the changes have been successfully saved.

1. To save your settings, choose one of the following options:

   1. To remain in the same window so that you can dynamically change the AWS Lambda function while testing your updated agent, choose **Save**.

   1. To save your settings and return to the **Working draft** page, choose **Save and exit**.

1. To test your agent's custom orchestration, choose **Prepare** in the **Test** window.

------
#### [ API ]

To configure custom orchestration using the API operations, send an [UpdateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).Specify the `orchestrationType` object as `CUSTOM_ORCHESTRATION`.

**Example orchestration payload in React**

The following is a react example that shows the chain of thought orchestration. In this example, after each step Amazon Bedrock agent asks the model to predict the next action. Note that the first state of any conversation is always `START`. Events are the responses which the function sends as response to Amazon Bedrock agents.

```
function react_chain_of_thought_orchestration(event) {
                    const incomingState = event.state;
                    
                    let payloadData = '';
                    let responseEvent = '';
                    let responseTrace = '';
                    let responseAttribution = '';
                    
                    if (incomingState == 'START') {
                        // 1. Invoke model in start
                        responseEvent = 'INVOKE_MODEL';
                        payloadData = JSON.stringify(intermediatePayload(event));
                    }
                    else if (incomingState == 'MODEL_INVOKED') {
                       const stopReason = modelInvocationStopReason(event);
                       if (stopReason == "tool_use") {
                           // 2.a. If invoke model predicts tool call, then we send INVOKE_TOOL event
                           responseEvent = 'INVOKE_TOOL';
                              payloadData = toolUsePayload(event);
                    } 
                    else if (stopReason == "end_turn") {
                         // 2.b. If invoke model predicts an end turn, then we send FINISH event
                         responseEvent = 'FINISH';
                         payloadData = getEndTurnPayload(event);
                      }
                    }
                    else if (incomingState == 'TOOL_INVOKED') {
                        // 3. After a tool invocation, we again ask LLM to predict what should be the next step
                        responseEvent = 'INVOKE_MODEL';
                        payloadData = intermediatePayload(event);
                    } 
                    else {
                       // Invalid incoming state
                       throw new Error('Invalid state provided!');
                    }
                    
                       // 4. Create the final payload to send back to BedrockAgent
                       const payload = createPayload(payloadData, responseEvent, responseTrace, ...);
                       return JSON.stringify(payload);
                    }
```

**Example orchestration payload in Lambda**

The following example shows the chain of thought orchestration. In this example, after each step Amazon Bedrock agent asks the model to predict the next action. Note that the first state of any conversation is always `START`. Events are the responses which the function sends as response to Amazon Bedrock agents.

The Payload structure to orchestration Lambda

```
{
    "version": "1.0",
    "state": "START | MODEL_INVOKED | TOOL_INVOKED | APPLY_GUARDRAIL_INVOKED | {{user-defined}}",
    "input": {
        "text": "{{user-provided text or tool results in converse format}}"
    },
    "context": {
        "requestId": "{{invoke agent request id}}",
        "sessionId": "{{invoke agent session id}}",
        "agentConfiguration": {
            "instruction": "{{agent instruction>}},
            "defaultModelId": "{{agent default model id}}",
            "tools": [{
                    "toolSpec": {...} 
                }
                ...
            ],
            "guardrails": {
                "version": "{{guardrail version}}",
                "identifier": "{{guardrail identifier}}"
            }
        },
        "session": [{
            "agentInput": "{{input utterance provided in invokeAgent}}",
            "agentOutput": "{{output response from invokeAgent}}",
            "intermediarySteps": [{
                "orchestrationInput": {
                    "state": "START | MODEL_INVOKED | TOOL_INVOKED | APPLY_GUARDRAIL_INVOKED | {{user defined}}",
                    "text": "..."
                },
                "orchestrationOutput": {
                    "event": "INVOKE_MODEL | INVOKE_TOOL | APPLY_GUARDRAIL | FINISH | {{user defined}}",
                    "text": "{{Converse API request or text}}"
                }
            }]
        }],
        "sessionAttributes": {
            {{key value pairs}}
        },
        "promptSessionAttributes": {
            {{key value pairs}}
        }
    }
}
```

The payload structure from orchestration lambda

```
{
    "version": "1.0",
    "actionEvent": "INVOKE_MODEL | INVOKE_TOOL | APPLY_GUARDRAIL | FINISH | {{user defined}}",
    "output": {
        "text": "{{Converse API request for INVOKE_MODEL, INVOKE_TOOL, APPLY_GUARDRAIL or text for FINISH}}",
        "trace": {
            "event": {
                "text": "{{Trace message to emit as event in InvokeAgent response}}"
            }
        }
    },
    "context": {
        "sessionAttributes": {
            {{key value pairs}}
        },
        "promptSessionAttributes": {
            {{key value pairs}}
        }
    }
}
```

Example of a START\_STATE sent from Amazon Bedrock Agents to the orchestrator Lambda

```
{
    "version": "1.0",
    "state": "START",
    "input": {
        "text": "{\"text\":\"{{invoke agent input text}}\"}"
    },
    "context": {
        ...
    }
}
```

In response if the orchestration Lambda decides to send a INVOKE\_MODEL EVENT response, it might look similar to the following:

```
{
    "version": "1.0",
    "actionEvent": "INVOKE_MODEL",
    "output": {
        "text": "{{converse API request}}",
        "trace": {
            "event": {
                "text": "{{debug trace text}}"
            }
        }
    },
    "context": {}
}
```

Example of a INVOKE\_TOOL\_EVENT using Converse API 

```
{
    "version": "1.0",
    "actionEvent": "INVOKE_TOOL",
    "output": {
        "text": "{\"toolUse\":{\"toolUseId\":\"{{unique id}}\",\"name\":\"{{tool name}}\",\"input\":{}}}"
    }
}
```

------