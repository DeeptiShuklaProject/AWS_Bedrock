

# Share a model with another account
<a name="share-model-share"></a>

After you [fulfill the prerequisites](share-model-prereq.md), you can share a model. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. Select the button next to the model that you want to share. Then, choose the three dots (![Vertical ellipsis icon representing a menu or more options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/vertical-ellipsis.png)) and select **Share**.

1. In the **Model sharing details** section, do the following:

   1. In the **Name for shared model** field, give the shared model a name.

   1. In the **Recipient account ID** field, specify the ID of the account that will receive the model.

   1. (Optional) To add tags, expand the **Tags** section. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

1. Choose **Share model**. After the recipient accepts the model in [Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-shared.html), the model appears in their list of custom models.

------
#### [ API ]

To share a model, send a [CreateResourceShare](https://docs.aws.amazon.com/ram/latest/APIReference/API_CreateResourceShare.html) request with an [AWS Resource Access Manager endpoint](https://docs.aws.amazon.com/general/latest/gr/ram.html). Minimally, provide the following fields:


****  

| Field | Use case | 
| --- | --- | 
| Name | To provide a name for the resource share. | 
| resourceArns | To specify the ARNs of each model to share. | 
| principals | To specify the principals to share the model with. | 

The [CreateResourceShare](https://docs.aws.amazon.com/ram/latest/APIReference/API_CreateResourceShare.html) response returns a `resourceShareArn` that you can use to manage the resource share.

The account receiving a model can check whether a model has been shared by sending a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Models that have been shared will show up with a `shared` status of `true`.

------

After sharing the model, the recipient of the model must copy it into a Region to use it. For more information, see [Copy a customized or shared model to use in a Region](copy-model.md).