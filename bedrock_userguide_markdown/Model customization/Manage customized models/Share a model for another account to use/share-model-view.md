

# View information about shared models
<a name="share-model-view"></a>

To learn how to view information about models that you've shared with other accounts or models that have been shared with you, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view models that you've shared with other accounts**

1. Sign in to the AWS Management Console and open the AWS RAM console at [https://console.aws.amazon.com/ram/home](https://console.aws.amazon.com/ram/home).

1. Follow the steps at [Viewing resource shares you created in AWS Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/working-with-sharing-view-rs.html).

**To view models shared with you by other accounts**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. Models that have been shared with you by other accounts will be shown in the following ways, depending on whether you've [copied them to a Region](copy-model.md):

   1. Shared models that you haven't copied to a Region yet are listed in the **Models shared with you** section.

   1. Shared models that have been copied to the current Region are listed in the **Models** section with a **Share status** of `Shared`.

------
#### [ API ]

To view information about models that you've shared, send a [GetResourceShares](https://docs.aws.amazon.com/ram/latest/APIReference/API_GetResourceShares.html) request with an [AWS Resource Access Manager endpoint](https://docs.aws.amazon.com/general/latest/gr/ram.html) and specify `SELF` in the `resourceOwner` field. You can use the optional fields to filter for specific models or resource shares.

To view information about models that have been shared with you, send a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and specify `false` with the `isOwned` filter.

------