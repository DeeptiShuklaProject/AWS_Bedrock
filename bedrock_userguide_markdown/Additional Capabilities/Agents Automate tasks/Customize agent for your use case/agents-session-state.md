

# Control agent session context
<a name="agents-session-state"></a>

For greater control of session context, you can modify the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState) object in your agent. The [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState) object contains information that can be maintained across turns (separate [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request and responses). You can use this information to provide conversational context for the agent during user conversations.

The general format of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState) object is as follows.

```
{
    "sessionAttributes": {
        "{{<attributeName1>}}": "{{<attributeValue1>"}},
        "{{<attributeName2>}}": "{{<attributeValue2>"}},
        ...
    },
     "conversationHistory": {
          "messages": [{
              "role": "user | assistant",
              "content": [{
                  "text": "string"
              }]
          }],
               },
    "promptSessionAttributes": {
        "{{<attributeName3>}}": "{{<attributeValue3>"}},
        "{{<attributeName4>}}": "{{<attributeValue4>"}},
        ...
    },
    "invocationId": "string",
    "returnControlInvocationResults": [
        [ApiResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ApiResult.html) or [FunctionResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_FunctionResult.html),
        ...
    ],
    "knowledgeBases": [
       {
        "knowledgeBaseId": "string",
        "retrievalConfiguration": {
            "vectorSearchConfiguration": {
                "overrideSearchType": "HYBRID | SEMANTIC",
                "numberOfResults": int,
                "filter": [RetrievalFilter](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html) object
            }
        }
       },
       ...
    ]
}
```

Select a topic to learn more about fields in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_SessionState.html#bedrock-Type-agent-runtime_SessionState) object.

**Topics**
+ [Session and prompt session attributes](#session-state-attributes)
+ [Session attribute example](#session-attribute-ex)
+ [Prompt session attribute example](#prompt-session-attribute-ex)
+ [Action group invocation results](#session-state-return-control)
+ [Knowledge base retrieval configurations](#session-state-kb)

## Session and prompt session attributes
<a name="session-state-attributes"></a>

Amazon Bedrock Agents allows you to define the following types of contextual attributes that persist over parts of a session:
+ **sessionAttributes** – Attributes that persist over a [session](advanced-prompts.md#advanced-prompts-terminology) between a user and agent. All [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) requests made with the same `sessionId` belong to the same session, as long as the session time limit (the `idleSessionTTLinSeconds`) has not been surpassed.
+ **conversationHistory** – For multi-agent collaboration, accepts additional context for processing run time requests if `conversationalHistorySharing` is enabled for a collaborator agent. By default, this field is automatically constructed by supervisor agent when invoking the collaborator agent. You can optionally use this field to provide additional context. For more information, see [Use multi-agent collaboration with Amazon Bedrock Agents](agents-multi-agent-collaboration.md).
+ **promptSessionAttributes** – Attributes that persist over a single [turn](advanced-prompts.md#advanced-prompts-terminology) (one [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) call). You can use the $prompt\_session\_attributes$ [placeholder](prompt-placeholders.md) when you edit the orchestration base prompt template. This placeholder will be populated at runtime with the attributes that you specify in the `promptSessionAttributes` field.

You can define the session state attributes at two different steps:
+ When you set up an action group and [write the Lambda function](agents-lambda.md), include `sessionAttributes` or `promptSessionAttributes` in the [response event](agents-lambda.md#agents-lambda-response) that is returned to Amazon Bedrock.
+ During runtime, when you send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request, include a `sessionState` object in the request body to dynamically change the session state attributes in the middle of the conversation.

## Session attribute example
<a name="session-attribute-ex"></a>

The following example uses a session attribute to personalize a message to your user.

1. Write your application code to ask the user to provide their first name and the request they want to make to the agent and to store the answers as the variables {{<first\_name>}} and {{<request>}}.

1. Write your application code to send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request with the following body:

   ```
   {
       "inputText": "{{<request>}}",
       "sessionState": {
           "sessionAttributes": {
               "firstName": "{{<first_name>}}"
           }
       }
   }
   ```

1. When a user uses your application and provides their first name, your code will send the first name as a session attribute and the agent will store their first name for the duration of the [session](advanced-prompts.md#advanced-prompts-terminology).

1. Because session attributes are sent in the [Lambda input event](agents-lambda.md#agents-lambda-input), you can refer to these session attributes in a Lambda function for an action group. For example, if the action [API schema](agents-api-schema.md) requires a first name in the request body, you can use the `firstName` session attribute when writing the Lambda function for an action group to automatically populate that field when sending the API request.

## Prompt session attribute example
<a name="prompt-session-attribute-ex"></a>

The following general example uses a prompt session attribute to provide temporal context for the agent.

1. Write your application code to store the user request in a variable called {{<request>}}.

1. Write your application code to retrieve the time zone at the user's location if the user uses a word indicating relative time (such as "tomorrow") in the {{<request>}}, and store in a variable called {{<timezone>}}.

1. Write your application to send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request with the following body:

   ```
   {
       "inputText": "{{<request>}}",
       "sessionState": {
           "promptSessionAttributes": {
               "timeZone": "{{<timezone>}}"
           }
       }
   }
   ```

1. If a user uses a word indicating relative time, your code will send the `timeZone` prompt session attribute and the agent will store it for the duration of the [turn](advanced-prompts.md#advanced-prompts-terminology).

1. For example, if a user asks **I need to book a hotel for tomorrow**, your code sends the user's time zone to the agent and the agent can determine the exact date that "tomorrow" refers to.

1. The prompt session attribute can be used at the following steps.
   + If you include the $prompt\_session\_attributes$ [placeholder](prompt-placeholders.md) in the orchestration prompt template, the orchestration prompt to the FM includes the prompt session attributes.
   + Prompt session attributes are sent in the [Lambda input event](agents-lambda.md#agents-lambda-input) and can be used to help populate API requests or returned in the [response](agents-lambda.md#agents-lambda-response).

## Action group invocation results
<a name="session-state-return-control"></a>

If you configured an action group to [return control in an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response](agents-returncontrol.md), you can send the results from invoking the action group in the `sessionState` of a subsequent [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response by including the following fields:
+ `invocationId` – This ID must match the `invocationId` returned in the [ReturnControlPayload](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ReturnControlPayload.html) object in the `returnControl` field of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response.
+ `returnControlInvocationResults` – Includes results that you obtain from invoking the action. You can set up your application to pass the [ReturnControlPayload](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ReturnControlPayload.html) object to perform an API request or call a function that you define. You can then provide the results of that action here. Each member of the `returnControlInvocationResults` list is one of the following:
  + An [ApiResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ApiResult.html) object containing the API operation that the agent predicted should be called in a previous [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) sequence and the results from invoking the action in your systems. The general format is as follows:

    ```
    {
        "actionGroup": "string",
        "agentId" : :string",
        "apiPath": "string",
        "confirmationState" : "CONFIRM | DENY",
        "httpMethod": "string",
        "httpStatusCode": integer,
        "responseBody": {
            "TEXT": {
                "body": "string"
            }
        }
    }
    ```
  + A [FunctionResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_FunctionResult.html) object containing the function that the agent predicted should be called in a previous [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) sequence and the results from invoking the action in your systems. The general format is as follows:

    ```
    {
        "actionGroup": "string",
        "agentId" : :string",
        "confirmationState" : "CONFIRM | DENY",
        "function": "string",
        "responseBody": {
            "TEXT": {
                "body": "string"
            }
        }
    }
    ```

The results that are provided can be used as context for further orchestration, sent to post-processing for the agent to format a response, or used directly in the agent's response to the user.

## Knowledge base retrieval configurations
<a name="session-state-kb"></a>

To modify the retrieval configuration of knowledge bases that are attached to your agent, include the `knowledgeBaseConfigurations` field with a list of configurations for each knowledge base whose configurations you want to specify. Specify the `knowledgeBaseId`. In the `vectorSearchConfiguration` field, you can specify the following query configurations (for more information about these configurations, see [Configure and customize queries and response generation](kb-test-config.md)):
+ **Search type** – Whether the knowledge base searches only vector embeddings (`SEMANTIC`) or both vector embeddings and raw text (`HYBRID`). Use the `overrideSearchType` field.
+ **Maximum number of retrieved results** – The maximum number of results from query retrieval to use in the response.
+ **Metadata and filtering** – Filters that you can configure to filter the results based on metadata attributes in the data source files.