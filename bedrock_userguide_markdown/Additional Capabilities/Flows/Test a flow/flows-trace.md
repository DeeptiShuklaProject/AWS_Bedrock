

# Track each step in your flow by viewing its trace in Amazon Bedrock
<a name="flows-trace"></a>

When you invoke a flow, you can view the *trace* to see the inputs to and outputs from each node. The trace helps you track the path from the input to the response that it ultimately returns. You can use the trace to troubleshoot errors that occur, to identify steps that lead to an unexpected outcome or performance bottleneck, and to consider ways in which you can improve the flow.

To view the trace, do the following:
+ In the console, follow the steps in the **Console** tab at [Test a flow in Amazon Bedrock](flows-test.md) and choose **Show trace** in the response from flow invocation.
+ In the API, set the `enableTrace` field to `true` in an [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) request. Each `flowOutputEvent` in the response is returned alongside a `flowTraceEvent`.

Each trace event includes the name of the node that either received an input or yielded an output and the date at time at which the input or output was processed. Select a tab to learn more about a type of trace event:

------
#### [ FlowTraceConditionNodeResultEvent ]

This type of trace identifies which conditions are satisfied for a condition node and helps you identify the branch or branches of the flow that are activated during the invocation. The following JSON object shows what a [FlowTraceEvent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowTraceEvent.html) looks like for the result of a condition node:

```
{
    "trace": {
        "conditionNodeOutputTrace": {
            "nodeName": "string",
            "satisfiedConditions": [
                {
                    "conditionName": "string"
                },
                ...
            ],
            "timestamp": timestamp
        }
    }
}
```

------
#### [ FlowTraceNodeInputEvent ]

This type of trace displays the input that was sent to a node. If the event is downstream from an iterator node but upstream from a collector node, the `iterationIndex` field indicates the index of the item in the array that the input is from. The following JSON object shows what a [FlowTraceEvent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowTraceEvent.html) looks like for the input into a node.

```
{
    "trace": {
        "nodeInputTrace": {
            "fields": [
                {
                    "content": {
                        "document": JSON object
                    },
                    "nodeInputName": "string"
                },
                ...
            ],
            "nodeName": "string",
            "timestamp": timestamp,
            "iterationIndex": int
        }
    }
}
```

------
#### [ FlowTraceNodeOutputEvent ]

This type of trace displays the output that was produced by a node. If the event is downstream from an iterator node but upstream from a collector node, the `iterationIndex` field indicates the index of the item in the array that the output is from. The following JSON object shows what a [FlowTraceEvent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FlowTraceEvent.html) looks like for the output from a node.

```
{
    "trace": {
        "nodeOutputTrace": {
            "fields": [
                {
                    "content": {
                        "document": JSON object
                    },
                    "nodeOutputName": "string"
                },
                ...
            ],
            "nodeName": "string",
            "timestamp": timestamp,
            "iterationIndex": int
        }
    }
}
```

------