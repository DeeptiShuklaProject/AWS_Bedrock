

# Node types for your flow
<a name="flows-nodes"></a>

Amazon Bedrock Flows provides the following node types to build your flow. When you configure a node, you provide the following fields:
+ Name – Enter a name for the node.
+ Type – In the console, you drag and drop the type of node to use. In the API, use the `type` field and the corresponding [FlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNodeConfiguration.html) in the `configuration` field.
+ Inputs – Provide the following information for each input:
  + Name – A name for the input. Some nodes have pre-defined names or types that you must use. To learn which ones have pre-defined names, see [Logic node types](#flows-nodes-logic-table).
  + Expression – Define the part of the whole input to use as the individual input. For more information, see [Use expressions to define inputs by extracting the relevant part of a whole input in Amazon Bedrock FlowsDefine inputs with expressions](flows-expressions.md).
  + Type – The data type for the input. When this node is reached at runtime, Amazon Bedrock applies the expression to the whole input and validates that the result matches the data type.
+ Outputs – Provide the following information for each output:
  + Name – A name for the output. Some nodes have pre-defined names or types that you must use. To learn which ones have pre-defined names, see [Logic node types](#flows-nodes-logic-table).
  + Type – The data type for the output. When this node is reached at runtime, Amazon Bedrock validates that the node output matches the data type.
+ Configuration – In the console, you define node-specific fields at the top of the node. In the API, use the appropriate [FlowNodeConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNodeConfiguration.html) and fill in its fields.

Each node type is described below and its structure in the API is provided. Expand a section to learn more about that node type.

## Nodes for controlling flow logic
<a name="flows-nodes-logic"></a>

Use the following node types to control the logic of your flow.

### Flow input node
<a name="flows-nodes-input"></a>

Every flow contains only one flow input node and must begin with it. The flow input node takes the `content` from the `InvokeFlow` request, validates the data type, and sends it to the following node.

The following shows the general structure of an input [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object in the API:

```
{
    "name": "string",
    "type": "Input",
    "outputs": [
        {
            "name": "document",
            "type": "String | Number | Boolean | Object | Array",
        }
    ],
    "configuration": {
        "input": CONTEXT-DEPENDENT
    }
}
```

### Flow output node
<a name="flows-nodes-output"></a>

A flow output node extracts the input data from the previous node, based on the defined expression, and returns it. In the console, the output is the response returned after choosing **Run** in the test window. In the API, the output is returned in the `content` field of the `flowOutputEvent` in the `InvokeFlow` response. A flow can have multiple flow output nodes.

A flow can have multiple flow output nodes if there are multiple branches in the flow.

The following shows the general structure of an output [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Output",
    "inputs": [
        {
            "name": "document",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        }
    ],
    "configuration": {
        "output": CONTEXT-DEPENDENT
    }
}
```

### Condition node
<a name="flows-nodes-condition"></a>

A condition node sends data from the previous node to different nodes, depending on the conditions that are defined. A condition node can take multiple inputs.

For an example, see [Create a flow with a condition node](flows-ex-condition.md).

**To define a condition node**

1. Add as many inputs as you need to evaluate the conditions you plan to add.

1. Enter a name for each input, specify the type to expect, and write an expression to extract the relevant part from the whole input.

1. Connect each input to the relevant output from an upstream node.

1. Add as many conditions as you need.

1. For each condition:

   1. Enter a name for the condition.

   1. Use relational and logical operators to define a condition that compares inputs to other inputs or to a constant.
**Note**  
Conditions are evaluated in order. If more than one condition is satisfied, the earlier condition takes precedence.

   1. Connect each condition to the downstream node to which you want to send the data if that condition is fulfilled.

#### Condition expressions
<a name="flows-nodes-condition-expr"></a>

To define a condition, you refer to an input by its name and compare it to a value using any of the following relational operators:


****  

| Operator | Meaning | Supported data types | Example usage | Example meaning | 
| --- | --- | --- | --- | --- | 
| == | Equal to (the data type must also be equal) | String, Number, Boolean | A == B | If A is equal to B | 
| \!= | Not equal to | String, Number, Boolean | A \!= B | If A isn't equal to B | 
| > | Greater than | Number | A > B | If A is greater than B | 
| >= | Greater than or equal to | Number | A >= B | If A is greater than or equal to B | 
| < | Less than | Number | A < B | If A is less than B | 
| <= | Less than or equal to | Number | A <= B | If A is less than or equal to B | 

You can compare inputs to other inputs or to a constant in a conditional expression. For example, if you have a numerical input called `profit` and another one called `expenses`, both **profit > expenses** or **profit <= 1000** are valid expressions.

You can use the following logical operators to combine expressions for more complex conditions. We recommend that you use parentheses to resolve ambiguities in grouping of expressions:


****  

| Operator | Meaning | Example usage | Example meaning | 
| --- | --- | --- | --- | 
| and | Both expressions are true | (A < B) and (C == 1) | If both expressions are true: [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/flows-nodes.html) | 
| or | At least one expression is true | (A \!= 2) or (B > C) | If either expressions is true: [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/flows-nodes.html) | 
| not | The expression isn't true | not (A > B) | If A isn't greater than B (equivalent to A <= B) | 

In the API, you define the following in the `definition` field when you send a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request:

1. A condition [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object in the `nodes` array. The general format is as follows (note that condition nodes don't have `outputs`):

   ```
   {
       "name": "string",
       "type": "Condition",
       "inputs": [
           {
               "name": "string",
               "type": "String | Number | Boolean | Object | Array",
               "expression": "string"
           }
       ],
       "configuration": {
           "condition": {
               "conditions": [
                   {
                       "name": "string",
                       "expression": "string"
                   },
                   ...
               ]
           }
       }
   }
   ```

1. For each input into the condition node, a [FlowConnection](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConnection.html) object in the `connections` array. Include a [FlowDataConnectionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowDataConnectionConfiguration.html) object in the `configuration` field of the `FlowConnection` object. The general format of the`FlowConnection` object is as follows:

   ```
   {
       "name": "string",
       "source": "string",
       "target": "string",
       "type": "Data",
       "configuration": {
           "data": {
               "sourceOutput": "string",
               "expression": "string"
           }
       }
   }
   ```

1. For each condition (including the default condition) in the condition node, a [FlowConnection](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConnection.html) object in the `connections` array. Include a [FlowConditionalConnectionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConditionalConnectionConfiguration.html) object in the `configuration` field of the `FlowConnection` object. The general format of the [FlowConnection](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowConnection.html) object is as follows:

   ```
   {
       "name": "string",
       "source": "string",
       "target": "string",
       "type": "Conditional",
       "configuration": {
           "conditional": {
               "condition": "string"
           }
       }
   }
   ```

   Use relational and logical operators to define the `condition` that connects this condition `source` node to a `target` node downstream. For the default condition, specify the condition as **default**.

### Iterator node
<a name="flows-nodes-iterator"></a>

An iterator node takes an array and iteratively returns its items as output to the downstream node. The inputs to the iterator node are processed one by one and not in parallel with each other. The flow output node returns the final result for each input in a different response. You can use also use a collector node downstream from the iterator node to collect the iterated responses and return them as an array, in addition to the size of the array.

The following shows the general structure of an iterator [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Iterator",
    "inputs": [
        {
            "name": "array",
            "type": "Array",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "arrayItem",
            "type": "String | Number | Boolean | Object | Array",
        },
        {
            "name": "arraySize",
            "type": "Number"
        }
    ],
    "configuration": {
        "iterator": CONTEXT-DEPENDENT
    }
}
```

### Collector node
<a name="flows-nodes-collector"></a>

A collector node takes an iterated input, in addition to the size that the array will be, and returns them as an array. You can use a collector node downstream from an iterator node to collect the iterated items after sending them through some nodes.

The following shows the general structure of a collector [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Collector",
    "inputs": [
        {
            "name": "arrayItem",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        {
            "name": "arraySize",
            "type": "Number"
        }
    ],
    "outputs": [
        {
            "name": "collectedArray",
            "type": "Array"
        },
    ],
    "configuration": {
        "collector": CONTEXT-DEPENDENT
    }
}
```

### DoWhile loop node
<a name="flows-nodes-dowhile"></a>

A DoWhile loop node executes a sequence of nodes repeatedly while a specified condition remains true. The loop executes at least once before evaluating the condition, making it ideal for scenarios where you need to perform an action and then check if it should be repeated based on the result.

The DoWhile loop node takes input data and passes it through the loop body. After each iteration, the condition is evaluated to determine whether to continue looping or exit. The loop continues as long as the condition evaluates to true, or the `maxIterations` is not exceeded.

The following shows the general structure of a DoWhile loop [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "DoWhile",
    "inputs": [
        {
            "name": "loopInput",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "loopOutput",
            "type": "String | Number | Boolean | Object | Array"
        },
        {
            "name": "iterationCount",
            "type": "Number"
        }
    ],
    "configuration": {
        "doWhile": {
            "condition": "string",
            "maxIterations": "number"
        }
    }
}
```

In the configuration:
+ `condition` – A boolean expression that determines whether to continue looping. Use the same relational and logical operators as condition nodes. The condition is evaluated after each iteration.
+ `maxIterations` – The maximum number of iterations. The default is 10. You must specify a positive number. This parameter helps you avoid infinite loops.

**Note**  
The `maxIterations` parameter has a default value of 10 and only accepts positive numbers. The loop exits when either the condition becomes false or the maximum number of iterations is reached.

## Nodes for handling data in the flow
<a name="flows-nodes-data"></a>

Use the following node types to handle data in your flow:

### Prompt node
<a name="flows-nodes-prompt"></a>

A prompt node defines a prompt to use in the flow. You can use a prompt from Prompt management or define one inline in the node. For more information, see [Construct and store reusable prompts with Prompt management in Amazon Bedrock](prompt-management.md).

For an example, see [Try example flows](flows-ex.md).

The inputs to the prompt node are values to fill in the variables. The output is the generated response from the model.

The following shows the general structure of a prompt [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "prompt",
    "inputs": [
        {
            "name": "content",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        ...
    ],
    "outputs": [
        {
            "name": "modelCompletion",
            "type": "String"
        }
    ],
    "configuration": {
        "prompt": {
            "sourceConfiguration": [PromptFlowNodeSourceConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptFlowNodeSourceConfiguration.html) object (see below),
            "guardrailConfiguration": {
                "guardrailIdentifier": "string",
                "guardrailVersion": "string"
            }
        }
    }
}
```

The [PromptFlowNodeSourceConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptFlowNodeSourceConfiguration.html) object depends on if you use a prompt from Prompt management or if you define it inline:
+ If you use a prompt from Prompt management, the object should be in the following general structure:

  ```
  {
      "resource": {
          "promptArn": "string"
      }
  }
  ```
+ If you define a prompt inline, follow the guidance for defining a variant in the API tab of [Create a prompt using Prompt management](prompt-management-create.md) (note that there is no `name` field in this object, however). The object you use should be in the following general structure:

  ```
  {
      "inline": {
          "modelId": "string",
          "templateType": "TEXT",
          "templateConfiguration": {
              "text": {
                  "text": "string",
                  "inputVariables": [
                      {
                          "name": "string"
                      },
                      ...
                  ]
              }
          },
          "inferenceConfiguration": {
              "text": {
                  "maxTokens": int,
                  "stopSequences": ["string", ...],
                  "temperature": float,
                  "topP": float
              }
          },
          "additionalModelRequestFields": {
              "key": "value",
              ...
          }
      }
  }
  ```

To apply a guardrail from Amazon Bedrock Guardrails to your prompt or the response generated from it, include the `guardrailConfiguration` field and specify the ID or ARN of the guardrail in the `guardrailIdentifier` field and the version of the guardrail in the `guardrailVersion` field.

### Agent node
<a name="flows-nodes-agent"></a>

An agent node lets you send a prompt to an agent, which orchestrates between FMs and associated resources to identify and carry out actions for an end-user. For more information, see [Automate tasks in your application using AI agents](agents.md).

In the configuration, specify the Amazon Resource Name (ARN) of the alias of the agent to use. The inputs into the node are the prompt for the agent and any associated [prompt or session attributes](agents-session-state.md). The node returns the agent's response as an output.

An Agent node can support multi-turn invocations, enabling interactive conversations between users and the Agent during flow execution. When an Agent node requires additional information or clarification, it can pause the flow execution and request specific input from the user. Once the user provides the requested information, the Agent node continues its processing with the new input. This continues until the agent node has all the required information to complete its execution

The following shows the general structure of an agent [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Agent",
    "inputs": [
       {
            "name": "agentInputText"
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        {
            "name": "promptAttributes"
            "type": "Object",
            "expression": "string"
        },
        {
            "name": "sessionAttributes"
            "type": "Object",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "agentResponse",
            "type": "String"
        }
    ],
    "configuration": {
        "agent": {
            "agentAliasArn": "string"
        }
    }
}
```

### Knowledge base node
<a name="flows-nodes-kb"></a>

A knowledge base node lets you send a query to a knowledge base from Amazon Bedrock Knowledge Bases. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md).

In the configuration, provide the `knowledgeBaseId` minimally. You can optionally include the following fields depending on your use case:
+ `modelId` – Include a [model ID](models-supported.md) to use if you want to generate a response based on the retrieved results. To return the retrieved results as an array, omit the model ID.
+ `guardrailConfiguration` – Include the ID or ARN of the guardrail, defined in Amazon Bedrock Guardrails in the `guardrailIdentifier` field and the version of the guardrail in the `guardrailVersion` field.
**Note**  
Guardrails can only be applied when using `RetrieveAndGenerate` in a knowledge base node.

The input into the node is the query to the knowledge base. The output is either the model response, as a string, or an array of the retrieved results.

The following shows the general structure of a knowledge base [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "KnowledgeBase",
    "inputs": [
       {
            "name": "retrievalQuery",
            "type": "String",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "retrievalResults" | "outputText",
            "type": "Array | String"
        }
    ],
    "configuration": {
        "knowledgeBase": {
            "knowledgeBaseId": "string",
            "modelId": "string",
            "guardrailConfiguration": {
                "guardrailIdentifier": "string",
                "guardrailVersion": "string"
            }
        }
    }
}
```

### S3 storage node
<a name="flows-nodes-storage"></a>

An S3 storage node lets you store data in the flow to an Amazon S3 bucket. In the configuration, you specify the S3 bucket to use for data storage. The inputs into the node are the content to store and the [object key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html). The node returns the URI of the S3 location as its output.

The following shows the general structure of an S3 storage [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Storage",
    "inputs": [
        {
            "name": "content",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        {
            "name": "objectKey",
            "type": "String",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "s3Uri",
            "type": "String"
        }
    ],
    "configuration": {
        "retrieval": {
            "serviceConfiguration": {
                "s3": {
                    "bucketName": "string"
                }
            }
        }
    }
}
```

### S3 retrieval node
<a name="flows-nodes-retrieval"></a>

An S3 retrieval node lets you retrieve data from an Amazon S3 location to introduce to the flow. In the configuration, you specify the S3 bucket from which to retrieve data. The input into the node is the [object key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html). The node returns the content in the S3 location as the output.

**Note**  
Currently, the data in the S3 location must be a UTF-8 encoded string.

The following shows the general structure of an S3 retrieval [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Retrieval",
    "inputs": [
        {
            "name": "objectKey",
            "type": "String",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "s3Content",
            "type": "String"
        }
    ],
    "configuration": {
        "retrieval": {
            "serviceConfiguration": {
                "s3": {
                    "bucketName": "string"
                }
            }
        }
    }
}
```

### Lambda function node
<a name="flows-nodes-lambda"></a>

A Lambda function node lets you call a Lambda function in which you can define code to carry out business logic. When you include a Lambda node in a flow, Amazon Bedrock sends an input event to the Lambda function that you specify.

In the configuration, specify the Amazon Resource Name (ARN) of the Lambda function. Define inputs to send in the Lambda input event. You can write code based on these inputs and define what the function returns. The function response is returned in the output.

The following shows the general structure of a Lambda function [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "LambdaFunction",
    "inputs": [
       {
            "name": "codeHookInput",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        ...
    ],
    "outputs": [
        {
            "name": "functionResponse",
            "type": "String | Number | Boolean | Object | Array"
        }
    ],
    "configuration": {
        "lambdaFunction": {
            "lambdaArn": "string"
        }
    }
}
```

#### Lambda input event for a flow
<a name="flows-nodes-lambda-input"></a>

The input event sent to a Lambda function in a Lambda node is of the following format:

```
{
   "messageVersion": "1.0",
   "flow": {
        "flowArn": "string",
        "flowAliasArn": "string"
   },
   "node": {
        "name": "string",
        "inputs": [
            {
               "name": "string",
               "type": "String | Number | Boolean | Object | Array",
               "expression": "string",
               "value": ...
            },
            ...
        ]
   }
}
```

The fields for each input match the fields that you specify when defining the Lambda node, while the value of the `value` field is populated with the whole input into the node after being resolved by the expression. For example, if the whole input into the node is `[1, 2, 3]` and the expression is `$.data[1]`, the value sent in the input event to the Lambda function would be `2`.

For more information about events in Lambda, see [Lambda concepts](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-concepts.html#gettingstarted-concepts-event) in the [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/).

#### Lambda response for a flow
<a name="flows-nodes-lambda-response"></a>

When you write a Lambda function, you define the response returned by it. This response is returned to your flow as the output of the Lambda node.

### Inline code node
<a name="flows-nodes-inline-code"></a>

An inline code node lets you write and execute code directly in your flow, enabling data transformations, custom logic, and integrations without using an external Lambda function. When you include an inline code node in your flow, Amazon Bedrock executes your code in an isolated, AWS managed environment that isn't shared with anyone and doesn't have internet access.

**Note**  
Inline code node is in preview release for Amazon Bedrock and is subject to change.

In the node configuration, specify the code to execute along with the programming language (`Python_3` is currently the only option). Define inputs that your code can access as variables. The result of the last executed line in your code is returned as the node output.

The following example shows the general structure of an inline code [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "InlineCode",
    "inputs": [{
            "name": "string",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        ...
    ],
    "outputs": [{
        "name": "response",
        "type": "String | Number | Boolean | Object | Array"
    }],
    "configuration": {
        "inlineCode": {
            "code": "string",
            "language": "Python_3"
        }
    }
}
```

#### Considerations when using inline code nodes
<a name="flows-nodes-inline-code-usage"></a>

When using inline code nodes in your flow, consider the following:

**Important**  
We recommend that you test your code before adding it to an inline code node.
+ Inline code nodes aren't supported in [asynchronous flow execution](flows-create-async.md).
+ Currently, the only programming language supported by inline code nodes is Python 3.12 (`Python_3)`.
+ Inline code acts like an interactive Python session. Only the result of the last executed line is captured and returned as the node output.
+ Python console output (such output as from the `print` function) isn't captured.
+ Inputs for your inline code node are available as Python variables in your code. Use the exact name of the node input to reference them.
+ Configure the input and output types correctly to avoid runtime errors. You can configure up to five node inputs.
+ You can have up to five inline code nodes per flow.
+ You can have a maximum of 25 running inline code nodes per AWS account.
+ Your code can't exceed 5 MB.

#### Inline code node inputs
<a name="flows-nodes-inline-code-input"></a>

The inputs you define for an inline code node are available as Python variables in your code. For example, if you define an input named `userData`, you can access it directly in your code as `userData`.

The value of each input is populated based on the expression that you define. For example, if the input to the node is `{"name": "John", "age": 30}` and the expression is `$.name`, the value of the input variable would be `"John"`.

#### Inline code node output
<a name="flows-nodes-inline-code-output"></a>

The result of the last executed line in your code is returned as the output of the inline code node. This output is available to subsequent nodes in your flow.

For example, the following code returns a dictionary as the node output:

```
# Process input data
result = {"processed": True, "data": userData}

# The last line's result is returned as the node output
result
```

### Lex node
<a name="flows-nodes-lex"></a>

**Note**  
The Lex node relies on the Amazon Lex service, which might store and use customer content for the development and continuous improvement of other AWS services. As an AWS customer, you can opt out of having your content stored or used for service improvements. To learn how to implement an opt-out policy for Amazon Lex, see [AI services opt-out policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html).

A Lex node lets you call a Amazon Lex bot to process an utterance using natural language processing and to identify an intent, based on the bot definition. For more information, see [Amazon Lex Developer Guide](https://docs.aws.amazon.com/lex/latest/dg/).

In the configuration, specify the Amazon Resource Name (ARN) of the alias of the bot to use and the locale to use. The inputs into the node are the utterance and any accompanying [request attributes](https://docs.aws.amazon.com/lexv2/latest/dg/context-mgmt-request-attribs.html) or [session attributes](https://docs.aws.amazon.com/lexv2/latest/dg/context-mgmt-request-attribs.html). The node returns the identified intent as the output.

**Note**  
Currently, the Lex node doesn't support multi-turn conversations. One Lex node can only process one utterance.

The following shows the general structure of a Lex [FlowNode](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowNode.html) object:

```
{
    "name": "string",
    "type": "Lex",
    "inputs": [
       {
            "name": "inputText",
            "type": "String | Number | Boolean | Object | Array",
            "expression": "string"
        },
        {
            "name": "requestAttributes",
            "type": "Object",
            "expression": "string"
        },
        {
            "name": "sessionAttributes",
            "type": "Object",
            "expression": "string"
        }
    ],
    "outputs": [
        {
            "name": "predictedIntent",
            "type": "String"
        }
    ],
    "configuration": {
        "lex": {
            "botAliasArn": "string",
            "localeId": "string"
        }
    }
}
```

## Summary tables for node types
<a name="flows-nodes-summary-table"></a>

The following tables summarize the inputs and outputs that are allowed for each node type. Note the following:
+ If a name is marked as **Any**, you can provide any string as the name. Otherwise, you must use the value specified in the table.
+ If a type is marked as **Any**, you can specify any of the following data types: String, Number, Boolean, Object, Array. Otherwise, you must use the type specified in the table.
+ You can define multiple inputs for the **Condition**, **Prompt**, **Lambda function**, and **Inline code** nodes.


**Logic node types**  
<a name="flows-nodes-logic-table"></a>
<table>
<thead>
  <tr><th></th><th colspan="3">Input info</th><th colspan="3">Output info</th></tr>
  <tr><th>Node type</th><th>Input</th><th>Name</th><th>Type</th><th>Output</th><th>Name</th><th>Type</th></tr>
</thead>
<tbody>
  <tr><td>Input</td><td>N/A</td><td>N/A</td><td>N/A</td><td>The content field in the InvokeFlow request.</td><td>document</td><td>Any</td></tr>
  <tr><td>Output</td><td>Data to return in the InvokeFlow response.</td><td>document</td><td>Any</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>
  <tr><td>Condition</td><td>Data to send based on a condition.<br />(multiple inputs allowed)</td><td>Any</td><td>Any</td><td>Data to send based on a condition.<br />(specify conditions for different paths)</td><td>Any</td><td>Any</td></tr>
  <tr><td rowspan="2">Iterator</td><td rowspan="2">An array for which you want to apply the following node(s) iteratively to each member.</td><td rowspan="2">array</td><td rowspan="2">Array</td><td>Each item from the array</td><td>arrayItem</td><td>Any</td></tr>
  <tr><td>The size of the input array</td><td>arraySize</td><td>Number</td></tr>
  <tr><td rowspan="2">Collector</td><td>An iteration that you want to consolidate into an array.</td><td>arrayItem</td><td>Any</td><td rowspan="2">An array with all the outputs from the previous node appended.</td><td rowspan="2">collectedArray</td><td rowspan="2">Array</td></tr>
  <tr><td>The size of the output array</td><td>arraySize</td><td>Number</td></tr>
  <tr><td rowspan="2">DoWhile loop</td><td>Data to process in the loop.</td><td>loopInput</td><td>Any</td><td>The final output from the loop after all iterations.</td><td>loopOutput</td><td>Any</td></tr>
  <tr><td>The number of iterations performed.</td><td>iterationCount</td><td>Number</td><td></td><td></td><td></td></tr>
</tbody>
</table>



**Data processing node types**  
<a name="flows-nodes-data-table"></a>
<table>
<thead>
  <tr><th></th><th colspan="3">Input info</th><th colspan="3">Output info</th></tr>
  <tr><th>Node type</th><th>Input</th><th>Name</th><th>Type</th><th>Output</th><th>Name</th><th>Type</th></tr>
</thead>
<tbody>
  <tr><td>Prompt</td><td>A value to fill in a variable in the prompt (multiple inputs allowed).</td><td>{{${variable-name}}}</td><td>Any</td><td>The response returned by the model.</td><td>modelCompletion</td><td>String</td></tr>
  <tr><td rowspan="2">S3 storage</td><td>Data to store in an S3 bucket.</td><td>content</td><td>Any</td><td rowspan="2">The URI of the S3 location.</td><td rowspan="2">s3Uri</td><td rowspan="2">String</td></tr>
  <tr><td>The [object key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html) to use for the S3 object.</td><td>objectKey</td><td>String</td></tr>
  <tr><td>S3 retrieval</td><td>The [object key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html) for the S3 object.</td><td>objectKey</td><td>String</td><td>The data to retrieve from an S3 bucket.</td><td>s3Content</td><td>Any</td></tr>
  <tr><td rowspan="3">Agent</td><td>The prompt to send to the agent.</td><td>agentInputText</td><td>String</td><td rowspan="3">The response returned from the agent.</td><td rowspan="3">agentResponse</td><td rowspan="3">String</td></tr>
  <tr><td>Any [prompt attributes](agents-session-state.md) to send alongside the prompt.</td><td>promptAttributes</td><td>Object</td></tr>
  <tr><td>Any [session attributes](agents-session-state.md) to send alongside the prompt.</td><td>sessionAttributes</td><td>Object</td></tr>
  <tr><td>Knowledge base</td><td>The query to send to the knowledge base.</td><td>retrievalQuery</td><td>String</td><td>The returned results or generated response from the knowledge base.</td><td>retrievalResults</td><td>Array</td></tr>
  <tr><td>Lambda function</td><td>Data to send to the function (multiple inputs allowed).</td><td>Any</td><td>Any</td><td>The response returned from the function.</td><td>functionResponse</td><td>Any</td></tr>
  <tr><td>Inline code node</td><td>Variables for your code to execute (multiple inputs allowed).</td><td>Any</td><td>Any</td><td>The last line executed in your code.</td><td>response</td><td>Any</td></tr>
  <tr><td rowspan="3">Lex</td><td>The utterance to send to the bot.</td><td>inputText</td><td>String</td><td rowspan="3">The intent that the bot predicts for the utterance.</td><td rowspan="3">predictedIntent</td><td rowspan="3">String</td></tr>
  <tr><td>Any [request attributes](https://docs.aws.amazon.com/lexv2/latest/dg/context-mgmt-request-attribs.html) to send alongside the utterance.</td><td>requestAttributes</td><td>Object</td></tr>
  <tr><td>Any [session attributes](https://docs.aws.amazon.com/lexv2/latest/dg/context-mgmt-session-attribs.html) to send alongside the utterance.</td><td>sessionAttributes</td><td>Object</td></tr>
</tbody>
</table>
