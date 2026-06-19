

# Test a flow in Amazon Bedrock
<a name="flows-test"></a>

After you’ve created a flow, you will have a *working draft*. The working draft is a version of the flow that you can iteratively build and test. Each time you make changes to your flow, the working draft is updated.

When you test your flow Amazon Bedrock first verifies the following and throws an exception if the verification fails:
+ Connectivity between all flow nodes.
+ At least one flow output node is configured.
+ Input and output variable types are matched as required.
+ Condition expressions are valid and a default outcome is provided.

If the verification fails, you'll need to fix the errors before you can test and validate the performance of your flow. Following are steps for testing your flow, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To test your flow**

1. If you're not already in the **Flow builder**, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Amazon Bedrock Flows** from the left navigation pane. Then, in the **Amazon Bedrock Flows** section, select a flow you want to test.

   1. Choose **Edit in flow builder**.

1. In the **Flow builder page**, in the right pane, enter an input to invoke your flow. Check that the input data type matches the output data type that you configured for the flow input node.

1. Choose **Run**.

1. Nodes or connections in the flow configuration that trigger errors become higlighted in red and ones that trigger warnings become highlighted in yellow. Read the error messages and warnings, fix the identified issues, save the flow, and run your test again.
**Note**  
You must save the flow for the changes you made to be applied when you test the flow.

1. (Optional) To view the inputs, outputs, and execution duration for each node, choose **Show trace** in the response. For more information, see [Track each step in your flow by viewing its trace in Amazon BedrockTrack each step in your flow by viewing its trace](flows-trace.md). To return to the visual builder, choose **Hide trace** or select the collapse icon.

1. After you are satisfied with your flow performance, choose **Save and exit**.

1. You can continue to iterate on building your flow. When you're satisfied with it and are ready to deploy it to production, create a version of the flow and an alias to point to the version. For more information, see [Deploy a flow to your application using versions and aliases](flows-deploy.md).

------
#### [ API ]

To test your flow, send an [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). Include the ARN or ID of the flow in the `flowIdentifier` field and the ARN or ID of the alias to use in the `flowAliasIdentifier` field.

To view the inputs and outputs for each node, set the `enableTrace` field to `TRUE`. For more information, see [Track each step in your flow by viewing its trace in Amazon BedrockTrack each step in your flow by viewing its trace](flows-trace.md).

The request body specifies the input for the flow and is of the following format:

```
{
   "inputs": [ 
      { 
         "content": { 
            "document": "JSON-formatted string"
         },
         "nodeName": "string",
         "nodeOutputName": "string"
      }
   ],
   "enableTrace": TRUE | FALSE
}
```

Provide the input in the `document` field, provide a name for the input in the `nodeName` field, and provide a name for the input in the `nodeOutputName` field.

The response is returned in a stream. Each event returned contains output from a node in the `document` field, the node that was processed in the `nodeName` field, and the type of node in the `nodeType` field. These events are of the following format:

```
{
    "flowOutputEvent": { 
        "content": { 
            "document": "JSON-formatted string"
        },
        "nodeName": "string",
        "nodeType": "string"
    }
}
```

If the flow finishes, a `flowCompletionEvent` field with the `completionReason` is also returned. If there's an error, the corresponding error field is returned.

------