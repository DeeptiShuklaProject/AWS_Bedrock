

# Modify a Provisioned Throughput
<a name="prov-thru-edit"></a>

The aspects of a Provisioned Throughput you can edit after purchase depend on the provisioning mode. For Provisioned Throughputs by Model Units, you can edit only the name and tags of your Provisioned Throughput, and the model if it's a custom model.

With Provisioned Throughputs by Tokens, you have more options, including modifying the number of input and output tokens per minute for your Provisioned Throughput.

Refer to the following sections to learn more about editing the type of Provisioned Throughput you want to modify.

## Modify a Provisioned Throughput by Model Units
<a name="prov-thru-edit-MUs"></a>

You can edit the name or tags of an existing Provisioned Throughput.

The following restrictions apply to changing the model that the Provisioned Throughput is associated with:
+ You can't change the model for a Provisioned Throughput associated with a base model.
+ If the Provisioned Throughput is associated with a custom model, you can change the association to the base model that it's customized from, or to another custom model that was derived from the same base model. 

While a Provisioned Throughput is updating, you can run inference using the Provisioned Throughput without disrupting the on-going traffic from your end customers. If you changed the model that the Provisioned Throughput is associated with, you might receive output from the old model until the update is fully deployed.

To learn how to edit a Provisioned Throughput, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Provisioned Throughput** from the left navigation pane.

1. From the **Provisioned Throughput** section, select a Provisioned Throughput.

1. Choose **Edit**. You can edit the following fields:
   + **Provisioned Throughput name** – Change the name of the Provisioned Throughput.
   + **Select model** – If the Provisioned Throughput is associated with a custom model, you can change the associated model.

1. You can edit the tags associated with your Provisioned Throughput in the **Tags** section. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

1. To save your changes, choose **Save edits**.

1. The console displays the **Provisioned Throughput** overview page. The **Status** of the Provisioned Throughput in the Provisioned Throughput table becomes **Updating**. When the Provisioned Throughput is finished being update, the **Status** becomes **In service**. If the update fails, the **Status** becomes **Failed**.

------
#### [ API ]

To edit a Provisioned Throughput, send an [UpdateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UpdateProvisionedModelThroughput.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp).

To learn more about the request body and the parameters you need to supply, see [UpdateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UpdateProvisionedModelThroughput.html) in the *Amazon Bedrock API Reference*.

If the action is successful, the response returns an HTTP 200 status response. To check when the Provisioned Throughput is ready for use, send a [GetProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetProvisionedModelThroughput.html) request and check that the status is `InService`. You can't update or delete a Provisioned Throughput while its status is `Updating`. If the update fails, its status will be `Failed`, and the [GetProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetProvisionedModelThroughput.html) response will contain a `failureMessage`.

To add tags to a Provisioned Throughput, send a [TagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_TagResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the Provisioned Throughput. The request body contains a `tags` field, which is an object containing a key-value pair that you specify for each tag.

To remove tags from a Provisioned Throughput, send an [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UntagResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the Provisioned Throughput. The `tagKeys` request parameter is a list containing the keys for the tags that you want to remove.

[See code examples](prov-thru-code-examples.md)

------