

# Create a version of a flow in Amazon Bedrock
<a name="flows-version-create"></a>

When you're satisfied with the configuration of your flow, create a immutable version of the flow that you can point to with an alias. To learn how to create a version of your flow, Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To create a version of your Amazon Bedrock Flows**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Amazon Bedrock Flows** from the left navigation pane. Then, choose a flow in the **Amazon Bedrock Flows** section.

1. In the **Versions** section, choose **Publish version**.

1. After the version is published, a success banner appears at the top.

------
#### [ API ]

To create a version of your flow, send a [CreateFlowVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateFlowVersion.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the flow as the `flowIdentifier`.

The response returns an ID and ARN for the version. Versions are created incrementally, starting from 1.

------