

# Update access to a shared model
<a name="share-model-edit"></a>

To learn how to update access to models that you've shared with other accounts, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To update access to a model that you've shared**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. In the **Models** section, select a model that you want to update access to.

1. In the **Model sharing details** section, do one of the following:
   + To share the model with another account, choose **Share** and then do the following:

     1. In the **Model sharing details** section, do the following:

        1. In the **Name for shared model** field, give the shared model a name.

        1. In the **Recipient account ID** field, specify the ID of the account that will receive the model.

        1. (Optional) To add tags, expand the **Tags** section. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

     1. Choose **Share model**. After the recipient accepts the model in [Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-shared.html), the model appears in their list of custom models.
   + To delete a model share and revoke access from the accounts specified in that model share, do the following:

     1. Select a model share and choose **Revoke shared model**.

     1. Review the message, type **revoke** in the text box, and choose **Revoke shared model** to confirm revoking of access.

------
#### [ API ]

To share a model with more accounts, do one of the following:
+ Send an [AssociateResourceShare](https://docs.aws.amazon.com/ram/latest/APIReference/API_AssociateResourceShare.html) request with an [AWS Resource Access Manager endpoint](https://docs.aws.amazon.com/general/latest/gr/ram.html). Specify the Amazon Resource Name (ARN) of the resource share in the `resourceShareArn` field and append accounts that you want to share the model with in the list of `principals`.
**Note**  
You can also share more models with the same account or accounts by appending model ARNs to the list of `resourceArns`.
+ Create a new resource share by following the steps in the **API** tab at [Share a model with another account](share-model-share.md).

------