

# Test a prompt using Prompt management
<a name="prompt-management-test"></a>

To learn how to test a prompt you created in Prompt management, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To test a prompt in Prompt management**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane. Then, choose a prompt in the **Prompts** section.

1. Choose **Edit in Prompt builder** in the **Prompt draft** section, or choose a version of the prompt in the **Versions** section.

1. (Optional) To provide values for variables in your prompt, you need to first select a model in the **Configurations** pane. Then, enter a **Test value** for each variable in the **Test variables** pane.
**Note**  
These test values are temporary and aren't saved if you save your prompt.

1. To test your prompt, choose **Run** in the **Test window** pane.

1. Modify your prompt or its configurations and then run your prompt again as necessary. If you're satisfied with your prompt, you can choose **Create version** to create a snapshot of your prompt that can be used in production. For more information, see [Deploy a prompt to your application using versions in Prompt management](prompt-management-deploy.md).

You can also test the prompt in the following ways:
+ To test the prompt in a flow, include a prompt node in the flow. For more information, see [Create and design a flow in Amazon Bedrock](flows-create.md) and [Node types for your flow](flows-nodes.md).
+ If didn't configure your prompt with an agent, you can still test the prompt with an agent by importing it when testing an agent. For more information, see [Test and troubleshoot agent behavior](agents-test.md).

------
#### [ API ]

You can test your prompt in the following ways:
+ To run inference on the prompt, send an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) request with an [Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt) and specify the ARN of the prompt in the `modelId` parameter. To pass values for prompt variables, include the `promptVariables` field with a map of variable names to their values:

  ```
  response = bedrock_runtime.converse(
      modelId="arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT_ID:VERSION",
      promptVariables={
          "{{variable_name}}": {"text": "{{value}}"}
      }
  )
  ```

  When invoking a managed prompt, you don't need to specify `messages` or `system` fields — these are defined in the prompt template. You only need to provide values for the variables defined in the prompt. For a complete example, see [Run Prompt management code samples](prompt-management-code-ex.md).
**Note**  
The following restrictions apply when you use a Prompt management prompt with `Converse` or `ConverseStream`:  
You can't include the `additionalModelRequestFields`, `inferenceConfig`, `system`, or `toolConfig` fields.
If you include the `messages` field, the messages are appended after the messages defined in the prompt.
If you include the `guardrailConfig` field, the guardrail is applied to the entire prompt. If you include `guardContent` blocks in the [ContentBlock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlock.html) field, the guardrail will only be applied to those blocks.
+ To test your prompt in a flow, create or edit a flow by sending a [CreateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlow.html) or [UpdateFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateFlow.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Include a SDK for JavaScript in Node.js of the `PromptNode` type and include the ARN of the prompt in the `promptArn` field. Then, send an [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). For more information, see [Create and design a flow in Amazon Bedrock](flows-create.md) and [Node types for your flow](flows-nodes.md).
+ To test your prompt with an agent, use the Amazon Bedrock console (see the **Console** tab), or enter the text of the prompt into the `inputText` field of an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request.

------