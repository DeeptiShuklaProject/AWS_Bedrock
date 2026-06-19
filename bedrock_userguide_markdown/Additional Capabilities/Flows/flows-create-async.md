

# Run Amazon Bedrock flows asynchronously with flow executions
<a name="flows-create-async"></a>

With flow executions, you can run Amazon Bedrock flows asynchronously. This lets your flows run for longer durations and also yield control so that your application can perform other tasks.

When you run a flow by using the Amazon Bedrock console or with the [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) operation, the flow runs until it finishes or times out at one hour (whichever is first). When you run a flow execution, your flow can run much longer: Individual nodes can run up to five minutes, and your entire flow can run for up to 24 hours.

**Note**  
Flow executions is in preview release for Amazon Bedrock and is subject to change.

## Required permissions for running flow executions
<a name="flows-create-async-permissions"></a>
+ Make sure that your Amazon Bedrock Flows service role has all necessary permissions. For more information, see [Create a service role for Amazon Bedrock Flows in Amazon Bedrock](flows-permissions.md).
+ (Optional) Encrypt your flow execution data with a customer managed AWS KMS key. For more information, see [Encryption of Amazon Bedrock Flows resources](encryption-flows.md).

## Create and manage a flow execution
<a name="flows-create-async-how-to"></a>

You can create a flow execution in the console or by using the [StartFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_StartFlowExecution.html) operation.

------
#### [ Console ]

1. Create a flow by following the instructions at [Create and design a flow in Amazon Bedrock](flows-create.md).

1. Create an alias for the flow by following the instructions at [Create an alias of a flow in Amazon Bedrock](flows-alias-create.md).

1. If you're not already in the **Flow builder**, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Amazon Bedrock Flows** from the left navigation pane, and then choose your flow.

1. Choose the **Executions** tab, then choose **Create execution**. 

1. In the **Create execution** dialog, enter the following

   1. For **Name**, enter a name for the flow execution. 

   1. For **Select alias**, choose the alias of the flow that you want to use.

   1. For **Prompt input**, enter the prompt that you want to start the flow with.

   1. Choose **Create** to create the flow execution and start running it.

1. On the flow details page, choose the **Executions** tab and take note of the flow execution's status in **Execution status**.

1. (Optional) Choose an execution to open the flow and see the execution summary.

   In **Execution output**, you see the output from the flow.

1. (Optional) To stop a flow execution, select the execution and choose **Stop**.

------
#### [ API ]

**Start a flow execution**  
To run a flow execution, send a [StartFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_StartFlowExecution.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). In the request, specify the flow ID and flow alias ID of the flow that you want to run. You can also specify the following:
+ **inputs** – An array containing the [input](flows-nodes.md#flows-nodes-input) node that you want the flow to start running from. You specify the input to send to the prompt flow input node in the `content` field.
+ **name** – A name for the flow execution.

```
{
    "inputs": [{
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document",
        "content": {
            "document": "Test"
        }
    }],
    "name": "MyExecution"
}
```

The response is the Amazon Resource Name (ARN) of the flow execution. You can use the `executionArn` to poll for the current state of the flow, such as when the flow execution finishes or a condition node evaluates its conditions.

```
{
      "executionArn": "arn:aws:bedrock:us-west-2:111122223333:flow/FLOWID/alias/TSTALIASID/execution/MyExecution"
}
```

**Track the progress of a flow execution**  
Use the [GetFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetFlowExecution.html) operation to get the current status of a flow that you identify by its execution ARN. A flow status is either `Running`, `Succeeded`, `Failed`, `TimedOut`, or `Aborted`.

```
{
      "endedAt": null,
      "errors": null,
      "executionArn": "arn:aws:bedrock:us-west-2:111122223333:flow/FLOWID/alias/TSTALIASID/execution/MyExecution",
      "flowAliasIdentifier": "TSTALIASID",
      "flowIdentifier": "FLOWID",
      "flowVersion": "DRAFT",
      "startedAt": "2025-03-20T23:32:28.899221162Z",
      "status": "Running"
}
```

Errors (such as a Lambda node that times out) are returned in the `errors` array like the following example:

```
"errors": [{
    "nodeName": "LambdaNode1",
    "errorType": "ExecutionTimedOut",
    "message": "Call to lambda function timed out"
}],
```

**Get the results of a flow execution**  
Amazon Bedrock writes the outputs of a flow to the flow's [output](flows-nodes.md#flows-nodes-output) nodes. You can get the outputs once the flow completes or while the flow is running (depending on your use case).

If you want the flow to complete first, make a call to `GetFlowExecution` and make sure that the value of the `status` field in the response is `Succeeded`.

To get a list of output events from the flow execution, make a call to [ListFlowExecutionEvents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListFlowExecutionEvents.html). In the response, check for `flowOutputEvent` objects in `flowExecutionEvents`. For example, you can get a flow's output in the `content` field:

```
{
      "flowOutputEvent": {
        "content": {
          "document": "The model response."
        },
        "nodeName": "FlowOutputNode"
      }
}
```

You can limit the output from `ListFlowExecutions` to just input and output nodes by setting the `eventType` query parameter to `Flow`.

**View events**  
To help debug your flow execution, you can use the [ListFlowExecutionEvents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListFlowExecutionEvents.html) operation to view events that nodes generate while the flow is running. Set the `eventType` query parameter to `Node` to see the inputs and outputs of all nodes (including intermediate nodes) in the response that's similar to the following example:

```
{
    "flowExecutionEvents": [{
            "nodeOutputEvent": {
                "fields": [{
                    "content": {
                        "document": "History book"
                    },
                    "name": "document"
                }],
                "nodeName": "FlowInputNode",
                "timestamp": "2025-05-05T18:38:56.637867516Z"
            }
        },
        {
            "nodeInputEvent": {
                "fields": [{
                    "content": {
                        "document": "History book"
                    },
                    "name": "book"
                }],
                "nodeName": "Prompt_1",
                "timestamp": "2025-05-05T18:38:57.434600163Z"
            }
        },
        {
            "nodeOutputEvent": {
                "fields": [{
                    "content": {
                        "document": "Here's a summary of the history book."
                    },
                    "name": "modelCompletion"
                }],
                "nodeName": "Prompt_1",
                "timestamp": "2025-05-05T18:39:06.034157077Z"
            }
        },
        {
            "nodeInputEvent": {
                "fields": [{
                    "content": {
                        "document": "Here's a summary of the history book."
                    },
                    "name": "document"
                }],
                "nodeName": "FlowOutputNode",
                "timestamp": "2025-05-05T18:39:06.453128251Z"
            }
        }
    ]
}
```

**Get a snapshot of your flow execution**  
Amazon Bedrock automatically takes a snapshot of a flow definition and metadata when a flow execution starts. This is helpful since a flow can be updated while it's running asynchronously. To retrieve this snapshot, call the [GetExecutionFlowSnapshot](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetExecutionFlowSnapshot.html) operation. The response includes the following flow fields:
+ **customerEncryptionKeyArn** – The ARN of the AWS KMS key that encrypts the flow.
+ **definition** – The [definition](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowDefinition.html) of the flow.
+ **executionRoleArn** – The ARN of the IAM service role that's used by the flow execution.
+ **flowAliasIdentifier** – The flow's alias ID.
+ **flowIdentifier** – The flow's ID.
+ **flowVersion** – The flow's version.

```
{
      "customerEncryptionKeyArn": null,
      "definition": "{{{flow-definition}}}",
      "executionRoleArn": "arn:aws:iam::111122223333:role/name",
      "flowAliasIdentifier": "TSTALIASID",
      "flowIdentifier": "FLOWID",
      "flowVersion": "DRAFT"
}
```

**List your flow executions**  
You can get a list of your flow executions by calling the [ListFlowExecutions](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListFlowExecutions.html) operation. The response includes a `flowExecutionSummaries` array with information about each of your flow executions in the current AWS Region for a flow or flow alias. Each element includes information such as the execution ARN, the start time, and the current status of the flow.

```
{
    "flowExecutionSummaries": [{
        "createdAt": "2025-03-11T23:21:02.875598966Z",
        "endedAt": null,
        "executionArn": "arn:aws:bedrock:us-west-2:111122223333:flow/FLOWID/alias/TSTALIASID/execution/MyExecution",
        "flowAliasIdentifier": "TSTALIASID",
        "flowIdentifier": "FLOWID",
        "flowVersion": "DRAFT",
        "status": "Running"
    }]
}
```

**Stop a running flow execution**  
If you need to stop a running flow execution, call the [StopFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_StopFlowExecution.html) operation and pass the flow ID, flow alias ID, and the flow execution ID for the execution that you want to stop. 

------

## Flow execution statuses
<a name="flows-async-statuses"></a>

A flow execution can have one of the following statuses:
+ **Running** – The flow execution is in progress.
+ **Succeeded** – The flow execution completed successfully.
+ **Failed** – The flow execution failed due to an error.
+ **TimedOut** – The flow execution exceeded the maximum runtime of 24 hours.
+ **Aborted** – The flow execution was manually stopped using the [StopFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_StopFlowExecution.html) operation.

Flow executions that are no longer running are automatically deleted after 90 days.

## Best practices for flow executions
<a name="flows-async-best-practices"></a>

Consider the following when using flow executions:
+ Regularly poll your flow execution's status using [GetFlowExecution](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetFlowExecution.html) until your flow reaches a terminal state (which is anything other than `Running`).
+ When your flow execution reaches a terminal state, use [ListFlowExecutionEvents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListFlowExecutionEvents.html) to get the results of your flow. For example, you might use these results to build some logic around your flow.
+ Get a snapshot of your flow execution using [GetExecutionFlowSnapshot](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetExecutionFlowSnapshot.html) to help with debugging if issues come up with the execution.