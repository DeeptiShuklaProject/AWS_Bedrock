

# View the trace
<a name="trace-view"></a>

The following describes how to view the trace. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view the trace during a conversation with an agent**

Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the **Agents** section, select the link for the agent that you want to test from the list of agents.

1. The **Test** window appears in a pane on the right.

1. Enter a message and choose **Run**. While the response is generating or after it finishes generating, select **Show trace**.

1. You can view the trace for each **Step** in real-time as your agent performs orchestration.

------
#### [ API ]

To view the trace, send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request with a [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt) and set the `enableTrace` field to `TRUE`. By default, the trace is disabled. or example code, see [Invoke an agent from your application](agents-invoke-agent.md).

If you enable the trace, in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response, each `chunk` in the stream is accompanied by a `trace` field that maps to a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html) object. Within the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_TracePart.html) is a `trace` field that maps to a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Trace.html) object.

------