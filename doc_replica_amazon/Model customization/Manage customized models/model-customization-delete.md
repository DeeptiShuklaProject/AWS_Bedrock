

# Delete a custom model
<a name="model-customization-delete"></a>

To delete a custom model, choose the tab for your preferred method, and then follow the steps:

**Before you begin**  
If you're deleting a distilled model, you must first delete any Provisioned Throughput or custom model deployment associated with the model. 

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Provisioned Throughput** from the left navigation pane.

1. From the **Models** section, select a custom model.

1. Choose the options icon (![Vertical ellipsis icon representing a menu or more options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/vertical-ellipsis.png)) and select **Delete**.

1. Follow the instructions to confirm deletion. Your custom model is then deleted.

------
#### [ API ]

To delete a custom model, send a [DeleteCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteCustomModel.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Specify either the name of the custom model or its ARN as the `modelIdentifier`.

------