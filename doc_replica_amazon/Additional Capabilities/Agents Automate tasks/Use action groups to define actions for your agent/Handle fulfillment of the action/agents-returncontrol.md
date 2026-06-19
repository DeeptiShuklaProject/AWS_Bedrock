

# Return control to the agent developer by sending elicited information in an InvokeAgent response
<a name="agents-returncontrol"></a>

Rather than sending the information that your agent has elicited from the user to a Lambda function for fulfillment, you can instead choose to return control to the agent developer by sending the information in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. You can configure return of control to the agent developer when creating or updating an action group. Through the API, you specify `RETURN_CONTROL` as the `customControl` value in the `actionGroupExecutor` object in a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) request. For more information, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

If you configure return of control for an action group, and if the agent determines that it should call an action in this action group, the API or function details elicited from the user will be returned in the `invocationInputs` field in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response, alongside a unique `invocationId`. You can then do the following:
+ Set up your application to invoke the API or function that you defined, provided the information returned in the `invocationInputs`.
+ Send the results from your application's invocation in another [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request, in the `sessionState` field, to provide context to the agent. You must use the same `invocationId` and `actionGroup` that were returned in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. This information can be used as context for further orchestration, sent to post-processing for the agent to format a response, or used directly in the agent's response to the user.
**Note**  
If you include `returnControlInvocationResults` in the `sessionState` field, the `inputText` field will be ignored.

To learn how to configure return of control to the agent developer while creating the action group, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

## Example for returning control to the agent developer
<a name="agents-returncontrol-ex"></a>

For example, you might have the following action groups:
+ A `PlanTrip` action group with a `suggestActivities` action that helps your users find activities to do during a trip. The `description` for this action says `This action suggests activities based on retrieved weather information`.
+ A `WeatherAPIs` action group with a `getWeather` action that helps your user get the weather for a specific location. The action's required parameters are `location` and `date`. The action group is configured to return control to the agent developer.

The following is a hypothetical sequence that might occur:

1. The user prompts your agent with the following query: **What should I do today?** This query is sent in the `inputText` field of an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request.

1. Your agent recognizes that the `suggestActivities` action should be invoked, but given the description, predicts that it should first invoke the `getWeather` action as context for helping to fulfill the `suggestActivities` action.

1. The agent knows that the current `date` is `2024-09-15`, but needs the `location` of the user as a required parameter to get the weather. It reprompts the user with the question "Where are you located?"

1. The user responds **Seattle**.

1. The agent returns the parameters for `getWeather` in the following [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response (select a tab to see examples for an action group defined with that method):

------
#### [ Function details ]

   ```
   HTTP/1.1 200
   x-amzn-bedrock-agent-content-type: application/json
   x-amz-bedrock-agent-session-id: session0
   Content-type: application/json
    
   {
       "returnControl": {
           "invocationInputs": [{
               "functionInvocationInput": {
                   "actionGroup": "WeatherAPIs",
                   "function": "getWeather",
                   "parameters": [
                       {
                           "name": "location",
                           "type": "string",
                           "value": "seattle"
                       },
                       {
                           "name": "date",
                           "type": "string",
                           "value": "2024-09-15"
                       }
                   ]
               }
           }],
           "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172"
       }
   }
   ```

------
#### [ OpenAPI schema ]

   ```
   HTTP/1.1 200
   x-amzn-bedrock-agent-content-type: application/json
   x-amz-bedrock-agent-session-id: session0
   Content-type: application/json
   
   {
       "invocationInputs": [{
           "apiInvocationInput": {
               "actionGroup": "WeatherAPIs",
               "apiPath": "/get-weather",
               "httpMethod": "get",
               "parameters": [
                   {
                       "name": "location",
                       "type": "string",
                       "value": "seattle"
                   },
                   {
                       "name": "date",
                       "type": "string",
                       "value": "2024-09-15"
                   }
               ]
           }
       }],
       "invocationId": "337cb2f6-ec74-4b49-8141-00b8091498ad"
   }
   ```

------

1. Your application is configured to use these parameters to get the weather for `seattle` for the date `2024-09-15`. The weather is determined to be rainy.

1. You send these results in the `sessionState` field of another [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request, using the same `invocationId`, `actionGroup`, and `function` as the previous response. Select a tab to see examples for an action group defined with that method:

------
#### [ Function details ]

   ```
   POST https://bedrock-agent-runtime.us-east-1.amazonaws.com/agents/{{AGENT12345}}/agentAliases/TSTALIASID/sessions/abb/text
               
   {
       "enableTrace": true,
       "sessionState": {
           "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172",
           "returnControlInvocationResults": [{
               "functionResult": {
                   "actionGroup": "WeatherAPIs",
                   "function": "getWeather",
                   "responseBody": {
                       "TEXT": {
                           "body": "It's rainy in Seattle today."
                       }
                   }
               }
           }]
       }
   }
   ```

------
#### [ OpenAPI schema ]

   ```
   POST https: //bedrock-agent-runtime.us-east-1.amazonaws.com/agents/AGENT12345/agentAliases/TSTALIASID/sessions/abb/text
    
   {
       "enableTrace": true,
       "sessionState": {
           "invocationId": "337cb2f6-ec74-4b49-8141-00b8091498ad",
           "returnControlInvocationResults": [{
               "apiResult": {
                   "actionGroup": "WeatherAPIs",
                   "httpMethod": "get",
                   "apiPath": "/get-weather",
                   "responseBody": {
                       "application/json": {
                           "body": "It's rainy in Seattle today."
                       }
                   }
               }
           }]
       }
   }
   ```

------

1. The agent predicts that it should call the `suggestActivities` action. It uses the context that it's rainy that day and suggests indoor, rather than outdoor, activities for the user in the response.

### Example for returning control to the collaborator agent
<a name="collaborator-agent-returncontrol-ex"></a>

If you are using [multi-agent collaboration](agents-multi-agent-collaboration.md) and if an agent collaborator chooses to return control by sending the information in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response, the information is returned in supervisor agent response with additional identifiers `agentId` and `collaboratorName`. Select a tab to see examples for an action group defined with that method: 

------
#### [ Function details ]

```
HTTP/1.1 200
x-amzn-bedrock-agent-content-type: application/json
x-amz-bedrock-agent-session-id: session0
Content-type: application/json
 
{
    "returnControl": {
        "invocationInputs": [{
            "functionInvocationInput": {
                "agentId": "AGENTID",
                "collaboratorName": "WeatherAgent"
                "actionGroup": "WeatherAPIs",
                "function": "getWeather",
                "parameters": [
                    {
                        "name": "location",
                        "type": "string",
                        "value": "seattle"
                    },
                    {
                        "name": "date",
                        "type": "string",
                        "value": "2024-09-15"
                    }
                ]
            }
        }],
        "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172"
    }
}
```

------
#### [ OpenAPI Schema ]

```
HTTP/1.1 200
x-amzn-bedrock-agent-content-type: application/json
x-amz-bedrock-agent-session-id: session0
Content-type: application/json

{
    "invocationInputs": [{
        "apiInvocationInput": {
            "actionGroup": "WeatherAPIs",
            "agentId": "AGENTID",
            "collaboratorName": "WeatherAgent"
            "apiPath": "/get-weather",
            "httpMethod": "get",
            "parameters": [
                {
                    "name": "location",
                    "type": "string",
                    "value": "seattle"
                },
                {
                    "name": "date",
                    "type": "string",
                    "value": "2024-09-15"
                }
            ]
        }
    }],
    "invocationId": "337cb2f6-ec74-4b49-8141-00b8091498ad"
}
```

------

Invoker of supervisor agent sends the results in the `sessionState` field back to supervisor agent with the corresponding `agentId` for it to be propagated to the right agent collaborator.

------
#### [ Function details ]

```
POST https://bedrock-agent-runtime.us-east-1.amazonaws.com/agents/AGENT12345/agentAliases/TSTALIASID/sessions/abb/text
            
{
    "enableTrace": true,
    "sessionState": {
        "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172",
        "returnControlInvocationResults": [{
            "functionResult": {
                "agentId": "AGENTID",
                "actionGroup": "WeatherAPIs",
                "function": "getWeather",
                "responseBody": {
                    "TEXT": {
                        "body": "It's rainy in Seattle today."
                    }
                }
            }
        }]
    }
}
```

------
#### [ OpenAPI Schema ]

```
POST https: //bedrock-agent-runtime.us-east-1.amazonaws.com/agents/AGENT12345/agentAliases/TSTALIASID/sessions/abb/text
 
{
    "enableTrace": true,
    "sessionState": {
        "invocationId": "337cb2f6-ec74-4b49-8141-00b8091498ad",
        "returnControlInvocationResults": [{
            "apiResult": {
                "agentId": "AGENTID",
                "actionGroup": "WeatherAPIs",
                "httpMethod": "get",
                "apiPath": "/get-weather",
                "responseBody": {
                    "application/json": {
                        "body": "It's rainy in Seattle today."
                    }
                }
            }
        }]
    }
}
```

------