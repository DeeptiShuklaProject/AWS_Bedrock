

# Track agent's step-by-step reasoning process using trace
<a name="trace-events"></a>

Each response from an Amazon Bedrock agent is accompanied by a *trace* that details the steps being orchestrated by the agent. The trace helps you follow the agent's reasoning process that leads it to the response it gives at that point in the conversation.

Use the trace to track the agent's path from the user input to the response it returns. The trace provides information about the inputs to the action groups that the agent invokes and the knowledge bases that it queries to respond to the user. In addition, the trace provides information about the outputs that the action groups and knowledge bases return. You can view the reasoning that the agent uses to determine the action that it takes or the query that it makes to a knowledge base. If a step in the trace fails, the trace returns a reason for the failure. Use the detailed information in the trace to troubleshoot your agent. You can identify steps at which the agent has trouble or at which it yields unexpected behavior. Then, you can use this information to consider ways in which you can improve the agent's behavior.

## Structure of the trace
<a name="trace-understand"></a>

If you enable the trace, in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response, each `chunk` in the stream is accompanied by a `trace` field that maps to a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html) object. The `tracePart` object contains information about the agent and sessions, alongside the agent's reasoning process and and results from calling API functions. 

```
{
    "agentId": "string",
    "agentName": "string",
    "collaboratorName": "string",
    "agentAliasId": "string",
    "sessionId": "string",
    "agentVersion": "string",
    "trace": { ...},    
    "callerChain": [{
        "agentAliasArn": "{{agent alias arn}}"
    }]
}
```

The following list describes the fields of [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html) object:
+ `agentId` – The unique identifier of the agent.
+ `agentName` – The name of the agent.
+ `collaboratorName` – If the multi-agent collaboration is enabled, the name of the collaborator agent.
+ `agentVersion` – The version of the agent.
+ `agentAliasId` – The unique identifier of the alias of the agent.
+ `sessionId` – The unique identifier of the session with the agent.
+ `trace` – Contains the agent's reasoning process and results from calling API actions. See below for more information.
+ `callerChain` – List of callers between the agent that published this trace and the end user.
  + If it is a single agent, this field will contain the alias Arn of the same agent who published the trace.
  + If multi-agent collaboration is enabled, this field will contain the alias Arn of all agents that forwarded the end user request to the current agent. 

 Within the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html) is a `trace` field that maps to a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html) object. The trace is shown as a JSON object in both the console and the API. Each **Step** in the console or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html) in the API can be one of the following traces:
+ [PreProcessingTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingTrace.html) – Traces the input and output of the pre-processing step, in which the agent contextualizes and categorizes user input and determines if it is valid.
+ [OrchestrationTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationTrace.html) – Traces the input and output of the orchestration step, in which the agent interprets the input, invokes action groups, and queries knowledge bases. Then the agent returns output to either continue orchestration or to respond to the user.
+ [PostProcessingTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingTrace.html) – Traces the input and output of the post-processing step, in which the agent handles the final output of the orchestration and determines how to return the response to the user.
+ [CustomOrchestrationTrace](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_CustomOrchestrationTrace.html) – Details about the custom orchestration step in which the agent determines the order in which actions are executed.
+ [RoutingClassifierTrace](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_RoutingClassifierTrace.html) – Traces the input and output of the routing classifier
+ [FailureTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_FailureTrace.html) – Traces the reason that a step failed.
+ [GuardrailTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GuardrailTrace.html) – Traces the actions of the Guardrail.

Each of the traces (except `FailureTrace`) contains a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object. The [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object contains configurations set in the prompt template for the step, alongside the prompt provided to the agent at this step. For more information about how to modify prompt templates, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md). The structure of the `ModelInvocationInput` object is as follows:

```
{
    "traceId": "string",
    "text": "string",
    "type": "PRE_PROCESSING | ORCHESTRATION | ROUTING_CLASSIFIER | KNOWLEDGE_BASE_RESPONSE_GENERATION | POST_PROCESSING",
    "foundationModel":string",
    "inferenceConfiguration": {
        "maximumLength": number,
        "stopSequences": ["string"],
        "temperature": float,
        "topK": float,
        "topP": float
    },
    "promptCreationMode": "DEFAULT | OVERRIDDEN",
    "parserMode": "DEFAULT | OVERRIDDEN",
    "overrideLambda": "string"
}
```

The following list describes the fields of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object:
+ `traceId` – The unique identifier of the trace.
+ `text` – The text from the prompt provided to the agent at this step.
+ `type` – The current step in the agent's process.
+ `foundationModel` – The foundation model of the collaborator agent in the multi-agent collaboration. This field is populated only if the `type` is `ROUTING_CLASSIFIER`. If the default model used for routing prompt is overridden, this field shows the model of the supervisor agent that is used for routing the prompt.
+ `inferenceConfiguration` – Inference parameters that influence response generation. For more information, see [Influence response generation with inference parameters](inference-parameters.md).
+ `promptCreationMode` – Whether the agent's default base prompt template was overridden for this step. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md).
+ `parserMode` – Whether the agent's default response parser was overridden for this step. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md).
+ `overrideLambda` – The Amazon Resource Name (ARN) of the parser Lambda function used to parse the response, if the default parser was overridden. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md).

For more information about each trace type, see the following sections:

### PreProcessingTrace
<a name="trace-preprocessing"></a>

```
{
    "modelInvocationInput": { // see above for details }
    "modelInvocationOutput": {
        "metadata": {
             "usage": {
                  "inputToken":: int,
                  "outputToken":: int
           },
         "rawResponse": {
              "content": "string"
          }
        "parsedResponse": {
            "isValid": boolean,
            "rationale": "string"
        },
        "traceId": "string"
    }
}
```

The [PreProcessingTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingTrace.html) consists of a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object and a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingModelInvocationOutput.html) object. The [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PreProcessingModelInvocationOutput.html) contains the following fields.
+ `metadata` – Contains the following information about the foundation model output.
  + `usage` – Contains the following information of the usage of the foundation model.
    + `inputTokens` – Contains the information about the input tokens from the foundation model usage.
    + `outputTokens` – Contains the information about the output tokens from the foundation model usage.
+ `rawResponse` – Contains the raw output from the foundation model.
  + `content` – The foundation model's raw output content.
+ `parsedResponse` – Contains the following details about the parsed user prompt.
  + `isValid` – Specifies whether the user prompt is valid.
  + `rationale` – Specifies the agent's reasoning for the next steps to take.
+ `traceId` – The unique identifier of the trace.

### OrchestrationTrace
<a name="trace-orchestration"></a>

The [OrchestrationTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationTrace.html) consists of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object, [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html) object, and any combination of the [Rationale](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rationale.html), [InvocationInput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvocationInput.html), and [Observation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html) objects. The [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html) contains the following fields. For more information about [Rationale](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rationale.html), [InvocationInput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvocationInput.html), and [Observation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html) objects, select from the following tabs. 

```
{
    "modelInvocationInput": { // see above for details },
     "modelInvocationOutput": {
        "metadata": {
             "usage": {
                  "inputToken":: int,
                  "outputToken":: int
           },
         "rawResponse": {
              "content": "string"
          },
    "rationale": { ... },
    "invocationInput": { ... },
    "observation": { ... }
}
```

If the `type` is `AGENT_COLLABORATOR` and if the routing was enabled for the supervisor agent, [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OrchestrationModelInvocationOutput.html) will contain the following structure:

```
routingClassifierModelInvocationOutput: {
        traceId: "string",
        rawResponse: "string",
        routerClassifierParsedResponse: {...} 
        metadata: {
            inputTokens: "..."
            outputTokens: "..."    
        }
    }
```

------
#### [ Rationale ]

The [Rationale](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rationale.html) object contains the reasoning of the agent given the user input. Following is the structure:

```
{
       "traceId": "string",
       "text": "string"
    }
```

The following list describes the fields of the [Rationale](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rationale.html) object:
+ `traceId` – The unique identifier of the trace step.
+ `text` – The reasoning process of the agent, based on the input prompt.

------
#### [ InvocationInput ]

The [InvocationInput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvocationInput.html) object contains information that will be input to the action group or knowledge base that is to be invoked or queried. Following is the structure:

```
{
    "traceId": "string",
    "invocationType": "AGENT_COLLABORATOR" | "ACTION_GROUP | KNOWLEDGE_BASE | FINISH",
     "agentCollaboratorInvocationInput": { 
        // see below for details
    },
    "actionGroupInvocationInput": {
        // see below for details
    },
    "knowledgeBaseLookupInput": {
        "knowledgeBaseId": "string",
        "text": "string"
    }
}
```

The following list describes the fields of the [InvocationInput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvocationInput.html) object:
+ `traceId` – The unique identifier of the trace.
+ `invocationType` – Specifies whether the agent is invoking a collaborator agent, an action group or a knowledge base, or ending the session.
+ `agentCollaborationInvocationInput` – Contains the invocation input to the collaborator agents. Appears if the `type` is `AGENT_COLLABORATOR` and if routing is enabled for the supervisor agent. For more information, see [Use multi-agent collaboration with Amazon Bedrock Agents](agents-multi-agent-collaboration.md).
  + The `agentCollaborationInvocationInput ` structure is as follows:

    ```
    {
      "agentCollaboratorName": "string",
      "agentCollaboratorAliasArn": "string",
      "input": {
          "text": "string"           
         }
      }
    ```

    Following are descriptions of the fields:
    + `agentCollaboratorName` – The name of the collaborator agent associated with the supervisor agent.
    + `agentCollaboratorAliasArn` – The alias Arn of the collaborator agent.
    + `input` – The input string for the collaborator agent.
+ `actionGroupInvocationInput` – Appears if the `type` is `ACTION_GROUP`. For more information, see [Define actions in the action group](action-define.md). Can be one of the following structures:
  + If the action group is defined by an API schema, the structure is as follows:

    ```
    {
        "actionGroupName": "string",
        "apiPath": "string",
        "verb": "string",
        "parameters": [
            {
                "name": "string",
                "type": "string",
                "value": "string"
            },
            ...
        ],
        "requestBody": {
            "content": {
                "{{<content-type>}}": [
                    {
                        "name": "string",
                        "type": "string",
                        "value": "string"
                    }   
                ]
            }
        },
        "executionType": "LAMBDA | RETURN_CONTROL",
        "invocationId": "string"
    }
    ```

    Following are descriptions of the fields:
    + `actionGroupName` – The name of the action group that the agent predicts should be invoked.
    + `apiPath` – The path to the API operation to call, according to the API schema.
    + `verb` – The API method being used, according to the API schema.
    + `parameters` – Contains a list of objects. Each object contains the name, type, and value of a parameter in the API operation, as defined in the API schema.
    + `requestBody` – Contains the request body and its properties, as defined in the API schema.
    + `executionType` – Whether fulfillment of the action is passed to a Lambda function (`LAMBDA`) or control is returned through the `InvokeAgent` response (`RETURN_CONTROL`). For more information, see [Handle fulfillment of the action](action-handle.md).
    + `invocationId` – The unique identifier of the invocation. Only returned if the `executionType` is `RETURN_CONTROL`.
  + If the action group is defined by function details, the structure is as follows:

    ```
    {
        "actionGroupName": "string",
        "function": "string",
        "parameters": [
            {
                "name": "string",
                "type": "string",
                "value": "string"
            },
            ...
        ],
        "executionType": "LAMBDA | RETURN_CONTROL",
        "invocationId": "string"
    }
    ```

    Following are descriptions of the fields:
    + `actionGroupName` – The name of the action group that the agent predicts should be invoked.
    + `function` – The name of the function that the agent predicts should be called.
    + `parameters` – The parameters of the function.
    + `executionType` – Whether fulfillment of the action is passed to a Lambda function (`LAMBDA`) or control is returned through the `InvokeAgent` response (`RETURN_CONTROL`). For more information, see [Handle fulfillment of the action](action-handle.md).
    + `invocationId` – The unique identifier of the invocation. Only returned if the `executionType` is `RETURN_CONTROL`.
+ `knowledgeBaseLookupInput` – Appears if the `type` is `KNOWLEDGE_BASE`. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md). Contains the following information about the knowledge base and the search query for the knowledge base:
  + `knowledgeBaseId` – The unique identifier of the knowledge base that the agent will look up.
  + `text` – The query to be made to the knowledge base.

------
#### [ Observation ]

The [Observation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html) object contains the result or output of an agent collaborator, an action group or knowledge base, or the response to the user. Following is the structure:

```
{
    "traceId": "string",
    "type": "AGENT_COLLABORATOR |ACTION_GROUP | KNOWLEDGE_BASE | REPROMPT | ASK_USER | FINISH",
    "agentCollaboratorInvocationOutput": { 
            "agentCollaboratorName": "string",
            "agentCollaboratorAliasArn": "string",
            "output": {
                "text": "string"
            },
    "actionGroupInvocation": {
        "text": "JSON-formatted string"
    },
    "knowledgeBaseLookupOutput": {
        "retrievedReferences": [
            {
                "content": {
                    "text": "string"
                },
                "location": {
                    "type": "S3",
                    "s3Location": {
                        "uri": "string"
                    }
                }
            },
            ...
        ]
    },
    "repromptResponse": {
        "source": "ACTION_GROUP | KNOWLEDGE_BASE | PARSER",
        "text": "string"
    },
    "finalResponse": {
        "text"
    }
}
```

The following list describes the fields of the [Observation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html) object:
+ `traceId` – The unique identifier of the trace.
+ `type` – Specifies whether the agent's observation is returned from the result of an agent collaborator, an action group or a knowledge base, if the agent is reprompting the user, requesting more information, or ending the conversation.
+ `agentCollaboratorInvocationOutput` – Contains the response from the collaborator agent or the final response. Appears if the `type` is `AGENT_COLLABORATOR` and if routing is enabled for the supervisor agent. For more information, see [Use multi-agent collaboration with Amazon Bedrock Agents](agents-multi-agent-collaboration.md). Each response contains the following fields:
  + `agentCollaboratorName` – The name of the collaborator agent sending the response.
  + `agentCollaboratorAliasArn` – The alias Arn of the collaborator agent sending the response.
  + `output` – Contains the response sent by the collaborator agent.
+ `actionGroupInvocationOutput` – Contains the JSON-formatted string returned by the API operation that was invoked by the action group. Appears if the `type` is `ACTION_GROUP`. For more information, see [Define OpenAPI schemas for your agent's action groups in Amazon Bedrock](agents-api-schema.md).
+ `knowledgeBaseLookupOutput` – Contains text retrieved from the knowledge base that is relevant to responding to the prompt, alongside the Amazon S3 location of the data source. Appears if the `type` is `KNOWLEDGE_BASE`. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md). Each object in the list of `retrievedReferences` contains the following fields:
  + `content` – Contains `text` from the knowledge base that is returned from the knowledge base query.
  + `location` – Contains the Amazon S3 URI of the data source from which the returned text was found.
+ `repromptResponse` – Appears if the `type` is `REPROMPT`. Contains the `text` that asks for a prompt again alongside the `source` of why the agent needs to reprompt.
+ `finalResponse` – Appears if the `type` is `ASK_USER` or `FINISH`. Contains the `text` that asks the user for more information or is a response to the user.

------

### PostProcessingTrace
<a name="trace-postprocessing"></a>

```
{
    "modelInvocationInput": { // see above for details }
    "modelInvocationOutput": {
        "rawResponse": {
            "content": "string"
        },
        "metadata": {
            "usage": {
                "inputToken": int,
                "outputToken": int    
             }     
         },
        "parsedResponse": {
            "text": "string"
        },
        "traceId": "string"
    }
}
```

The [PostProcessingTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingTrace.html) consists of a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ModelInvocationInput.html) object and a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingModelInvocationOutput.html) object. The [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingModelInvocationOutput.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PostProcessingModelInvocationOutput.html) contains the following fields:
+ `rawResponse` – Contains the raw output from the foundation model.
  + `content` – The foundation model's raw output content.
+ `metadata` – Contains the following information about the foundation model output.
  + `usage` – Contains the following information of the usage of the foundation model.
    + `inputTokens` – Contains the information about the input tokens from the foundation model usage.
    + `outputTokens` – Contains the information about the output tokens from the foundation model usage.
+ `parsedResponse` – Contains the `text` to return to the user after the text is processed by the parser function.
+ `traceId` – The unique identifier of the trace.

### FailureTrace
<a name="trace-failure"></a>

```
{
    "failureReason": "string",
    "traceId": "string"
}
```

The following list describes the fields of the [FailureTrace](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_FailureTrace.html) object:
+ `failureReason` – The reason that the step failed.
+ `traceId` – The unique identifier of the trace.

### GuardrailTrace
<a name="trace-guardrail"></a>

```
{
    "action": "GUARDRAIL_INTERVENED" | "NONE",
    "inputAssessments": [GuardrailAssessment],
    "outputAssessments": [GuardrailAssessment]
}
```

The following list describes the fields of the GuardrailAssessment object:
+ `action` – indicates whether guardrails intervened or not on the input data. Options are `GUARDRAIL_INTERVENED` or `NONE`.
+ `inputAssessments` – The details of the Guardrail assessment on the user input.
+ `outputAssessments` – The details of the Guardrail assessment on the response.

For more details on the `GuardrailAssessment` object and testing a Guardrail, see [Test your guardrail](guardrails-test.md).

GuardrailAssessment example:

```
{
    "topicPolicy": {
        "topics": [{
            "name": "string",
            "type": "string",
            "action": "string"
        }]
    },
    "contentPolicy": {
        "filters": [{
            "type": "string",
            "confidence": "string",
            "action": "string"
        }]
    },
    "wordPolicy": {
        "customWords": [{
            "match": "string",
            "action": "string"
        }],
        "managedWordLists": [{
            "match": "string",
            "type": "string",
            "action": "string"
        }]
    },
    "sensitiveInformationPolicy": {
        "piiEntities": [{
            "type": "string",
            "match": "string",
            "action": "string"
        }],
        "regexes": [{
            "name": "string",
            "regex": "string",
            "match": "string",
            "action": "string"
        }]
    }
}
```