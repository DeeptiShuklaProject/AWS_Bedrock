

# Purchase Provisioned Throughput for a custom model
<a name="custom-model-use-pt"></a>

To use a custom model with dedicated compute capacity and guaranteed throughput, you can purchase Provisioned Throughput for it. You can then use the resulting provisioned model for inference. For more information about Provisioned Throughput, see [Increase model invocation capacity with Provisioned Throughput in Amazon Bedrock](prov-throughput.md).

------
#### [ Console ]

**To purchase Provisioned Throughput for a custom model.**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. In the **Models** tab, choose the radio button next to the model for which you want to buy Provisioned Throughput or select the model name to navigate to the details page.

1. Select **Purchase Provisioned Throughput**.

1. For more details, follow the steps in the provisioned throughput documentation.

1. After purchasing Provisioned Throughput for your custom model, follow the steps in the provisioned throughput usage documentation.

When you carry out any operation that supports usage of custom models, you will see your custom model as an option in the model selection menu.

------
#### [ API ]

To purchase Provisioned Throughput for a custom model, follow the steps in the provisioned throughput documentation to send a [CreateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateProvisionedModelThroughput.html) (see link for request and response formats and field details) request with a [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Use the name or ARN of your custom model as the `modelId`. The response returns a `provisionedModelArn` that you can use as the `modelId` when making an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) request.

[See code examples](model-customization-code-samples.md)

------