

# Use a Provisioned Throughput with an Amazon Bedrock resource
<a name="prov-thru-use"></a>

After you purchase a Provisioned Throughput, you can use it with the following features:
+ **Model inference** – You can test the Provisioned Throughput in an Amazon Bedrock console playground. When you're ready to deploy the Provisioned Throughput, set up your application to invoke the provisioned model. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To use a Provisioned Throughput in the Amazon Bedrock console playground**

  1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

  1. From the left navigation pane, select **Chat**, **Text**, or **Image** under **Playgrounds**, depending your use case.

  1. Choose **Select model**.

  1. In the **1. Category** column, select a provider or custom model category. Then, in the **2. Model** column, select the model that your Provisioned Throughput is associated with.

  1. In the **3. Throughput** column, select your Provisioned Throughput.

  1. Choose **Apply**.

  To learn how to use the Amazon Bedrock playgrounds, see [Generate responses in the console using playgrounds](playgrounds.md).

------
#### [ API ]

  To run inference using a Provisioned Throughput, send an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) request with an [Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt). Specify the provisioned model ARN as the `modelId` parameter. To see requirements for the request body for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md).

  [See code examples](prov-thru-code-examples.md)

------
+ **Associate a Provisioned Throughput with an agent alias** – You can associate a Provisioned Throughput when you [create](agents-deploy.md) or [update](agents-alias-edit.md) an agent alias. In the Amazon Bedrock console, you choose the Provisioned Throughput when setting up the alias or editing it. In the Amazon Bedrock API, you specify the `provisionedThroughput` in the `routingConfiguration` when you send a [CreateAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentAlias.html) or [UpdateAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentAlias.html); request.