

# Configure Lambda functions to send information that an Amazon Bedrock agent elicits from the user
<a name="agents-lambda"></a>

You can define a Lambda function to program the business logic for an action group. After an Amazon Bedrock agent determines the API operation that it needs to invoke in an action group, it sends information from the API schema alongside relevant metadata as an input event to the Lambda function. To write your function, you must understand the following components of the Lambda function:
+ **Input event** – Contains relevant metadata and populated fields from the request body of the API operation or the function parameters for the action that the agent determines must be called.
+ **Response** – Contains relevant metadata and populated fields for the response body returned from the API operation or the function.

You write your Lambda function to define how to handle an action group and to customize how you want the API response to be returned. You use the variables from the input event to define your functions and return a response to the agent.

**Note**  
An action group can contain up to 11 API operations, but you can only write one Lambda function. Because the Lambda function can only receive an input event and return a response for one API operation at a time, you should write the function considering the different API operations that may be invoked.

For your agent to use a Lambda function, you must attach a resource-based policy to the function to provide permissions for the agent. For more information, follow the steps at [Resource-based policy to allow Amazon Bedrock to invoke an action group Lambda function](agents-permissions.md#agents-permissions-lambda). For more information about resource-based policies in Lambda, see [Using resource-based policies for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html) in the AWS Lambda Developer Guide.

To learn how to define a function while creating the action group, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

**Topics**
+ [Lambda input event from Amazon Bedrock](#agents-lambda-input)
+ [Lambda response event to Amazon Bedrock](#agents-lambda-response)
+ [Action group Lambda function example](#agents-lambda-example)

## Lambda input event from Amazon Bedrock
<a name="agents-lambda-input"></a>

When an action group using a Lambda function is invoked, Amazon Bedrock sends a Lambda input event of the following general format. You can define your Lambda function to use any of the input event fields to manipulate the business logic within the function to successfully perform the action. For more information about Lambda functions, see [Event-driven invocation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html#event-driven-invocation) in the AWS Lambda Developer Guide.

The input event format depends on whether you defined the action group with an API schema or with function details:
+ If you defined the action group with an API schema, the input event format is as follows:

  ```
  {
      "messageVersion": "1.0",
      "agent": {
          "name": "string",
          "id": "string",
          "alias": "string",
          "version": "string"
      },
      "inputText": "string",
      "sessionId": "string",
      "actionGroup": "string",
      "apiPath": "string",
      "httpMethod": "string",
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
              "{{<content_type>}}": {
                  "properties": [
                     {
                         "name": "string",
                         "type": "string",
                         "value": "string"
                      },
                              ...
                  ]
              }
          }
      },
      "sessionAttributes": {
          "{{string}}": "string",
      },
      "promptSessionAttributes": {
          "{{string}}": "string"
      }
  }
  ```
+ If you defined the action group with function details, the input event format is as follows:

  ```
  {
      "messageVersion": "1.0",
      "agent": {
          "name": "string",
          "id": "string",
          "alias": "string",
          "version": "string"
      },
      "inputText": "string",
      "sessionId": "string",
      "actionGroup": "string",
      "function": "string",
      "parameters": [
          {
              "name": "string",
              "type": "string",
              "value": "string"
          },
      ...
      ],
      "sessionAttributes": {
          "{{string}}": "string",
      },
      "promptSessionAttributes": {
          "{{string}}": "string"
      }
  }
  ```

The following list describes the input event fields;
+ `messageVersion` – The version of the message that identifies the format of the event data going into the Lambda function and the expected format of the response from a Lambda function. Amazon Bedrock only supports version 1.0.
+ `agent` – Contains information about the name, ID, alias, and version of the agent that the action group belongs to.
+ `inputText` – The user input for the conversation turn.
+ `sessionId` – The unique identifier of the agent session.
+ `actionGroup` – The name of the action group.
+ `parameters` – Contains a list of objects. Each object contains the name, type, and value of a parameter in the API operation, as defined in the OpenAPI schema, or in the function.
+ If you defined the action group with an API schema, the input event contains the following fields:
  + `apiPath` – The path to the API operation, as defined in the OpenAPI schema.
  + `httpMethod` – The method of the API operation, as defined in the OpenAPI schema.
  + `requestBody` – Contains the request body and its properties, as defined in the OpenAPI schema for the action group.
+ If you defined the action group with function details, the input event contains the following field:
  + `function` – The name of the function as defined in the function details for the action group.
+ `sessionAttributes` – Contains [session attributes](agents-session-state.md) and their values. These attributes are stored over a [session](advanced-prompts.md#advanced-prompts-terminology) and provide context for the agent.
+ `promptSessionAttributes` – Contains [prompt session attributes](agents-session-state.md) and their values. These attributes are stored over a [turn](advanced-prompts.md#advanced-prompts-terminology) and provide context for the agent.

## Lambda response event to Amazon Bedrock
<a name="agents-lambda-response"></a>

Amazon Bedrock expects a response from your Lambda function that matches the following format. The response consists of parameters returned from the API operation. The agent can use the response from the Lambda function for further orchestration or to help it return a response to the customer.

**Note**  
The maximum payload response size matches the maximum size of a synchronous response from the Lambda function. For more information, see the *invocation payload* resource [quota](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html#function-configuration-deployment-and-execution) in the AWS Lambda Developer Guide.

The input event format depends on whether you defined the action group with an API schema or with function details:
+ If you defined the action group with an API schema, the response format is as follows:

  ```
  {
      "messageVersion": "1.0",
      "response": {
          "actionGroup": "string",
          "apiPath": "string",
          "httpMethod": "string",
          "httpStatusCode": number,
          "responseBody": {
              "{{<contentType>}}": {
                  "body": "JSON-formatted string" 
              }
          }
      },
      "sessionAttributes": {
          "{{string}}": "string",
          ...
      },
      "promptSessionAttributes": {
          "{{string}}": "string",
          ...
      },
      "knowledgeBasesConfiguration": [
          {
              "knowledgeBaseId": "string",
              "retrievalConfiguration": {
                  "vectorSearchConfiguration": {
                      "numberOfResults": int,
                      "overrideSearchType": "HYBRID | SEMANTIC",
                      "filter": [RetrievalFilter](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html) object
                  }
              }
          },
          ...
      ]
  }
  ```
+ If you defined the action group with function details, the response format is as follows:

  ```
  {
      "messageVersion": "1.0",
      "response": {
          "actionGroup": "string",
          "function": "string",
          "functionResponse": {
              "responseState": "FAILURE | REPROMPT",
              "responseBody": {
                  "{{<functionContentType>}}": { 
                      "body": "JSON-formatted string"
                  }
              }
          }
      },
      "sessionAttributes": {
          "{{string}}": "string",
      },
      "promptSessionAttributes": {
          "{{string}}": "string"
      },
      "knowledgeBasesConfiguration": [
          {
              "knowledgeBaseId": "string",
              "retrievalConfiguration": {
                  "vectorSearchConfiguration": {
                      "numberOfResults": int,
                      "filter": {
                          [RetrievalFilter](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html) object
                      }
                  }
              }
          },
          ...
      ]
  }
  ```

The following list describes the response fields:
+ `messageVersion` – The version of the message that identifies the format of the event data going into the Lambda function and the expected format of the response from a Lambda function. Amazon Bedrock only supports version 1.0.
+ `response` – Contains the following information about the API response.
  + `actionGroup` – The name of the action group.
  + If you defined the action group with an API schema, the following fields can be in the response:
    + `apiPath` – The path to the API operation, as defined in the OpenAPI schema.
    + `httpMethod` – The method of the API operation, as defined in the OpenAPI schema.
    + `httpStatusCode` – The HTTP status code returned from the API operation.
    + `responseBody` – Contains the response body, as defined in the OpenAPI schema.
  + If you defined the action group with function details, the following fields can be in the response:
    + `responseState` (Optional) – Set to one of the following states to define the agent's behavior after processing the action:
      + FAILURE – The agent throws a `DependencyFailedException` for the current session. Applies when the function execution fails because of a dependency failure.
      + REPROMPT – The agent passes a response string to the model to reprompt it. Applies when the function execution fails because of invalid input.
    + `responseBody` – Contains an object that defines the response from execution of the function. The key is the content type (currently only `TEXT` is supported) and the value is an object containing the `body` of the response.
+ (Optional) `sessionAttributes` – Contains session attributes and their values. For more information, see [Session and prompt session attributes](agents-session-state.md#session-state-attributes).
+ (Optional) `promptSessionAttributes` – Contains prompt attributes and their values. For more information, see [Session and prompt session attributes](agents-session-state.md#session-state-attributes).
+ (Optional) `knowledgeBasesConfiguration` – Contains a list of query configurations for knowledge bases attached to the agent. For more information, see [Knowledge base retrieval configurations](agents-session-state.md#session-state-kb).

## Action group Lambda function example
<a name="agents-lambda-example"></a>

The following is a minimal example of how the Lambda function can be defined in Python. Select the tab corresponding to whether you defined the action group with an OpenAPI schema or with function details:

------
#### [ OpenAPI schema ]

```
def lambda_handler(event, context):

    agent = event['agent']
    actionGroup = event['actionGroup']
    api_path = event['apiPath']
    # get parameters
    get_parameters = event.get('parameters', [])
    # post parameters
    post_parameters = event['requestBody']['content']['application/json']['properties']

    response_body = {
        'application/json': {
            'body': "{{sample response}}"
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return api_response
```

------
#### [ Function details ]

```
def lambda_handler(event, context):

    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    response_body = {
        'TEXT': {
            'body': "sample response"
        }
    }
    
    function_response = {
        'actionGroup': event['actionGroup'],
        'function': event['function'],
        'functionResponse': {
            'responseBody': response_body
        }
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    action_response = {
        'messageVersion': '1.0', 
        'response': function_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return action_response
```

------