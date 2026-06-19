

# Subscribing to third-party Bedrock models through Private Offer
<a name="managed-entitlements-subscribing"></a>

Before you can distribute licenses, you must first subscribe to a Bedrock model through AWS Marketplace.

**To subscribe to a third-party Bedrock model through AWS Marketplace**

1. Choose the private offer link from the sellers to get started or sign in to your management account or designated billing account

1. Open the AWS Marketplace console at [https://console.aws.amazon.com/marketplace/](https://console.aws.amazon.com/marketplace/).

1. Navigate to Private Offers for the list of Available Offers

1. Review the subscription agreement and pricing details.

1. Choose **Subscribe** to complete the subscription.

1. You will see a confirmation message indicating your subscription is active.

## To verify license creation
<a name="managed-entitlements-verify-license"></a>

After subscribing, AWS License Manager automatically creates a license for your subscription.

1. Wait 1-2 minutes for the license to be created.

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. Make sure you are in the us-east-1 region.

1. In the navigation pane, choose **Granted Licenses**.

1. You should see a new license for your third-party Bedrock model subscription.

1. The license status should display as **Available**.

**Note**  
The license is always created in the us-east-1 region, regardless of which region you subscribed in. Always check License Manager in us-east-1 to view your licenses.

If the license does not appear after 5 minutes, verify your subscription is active by going to AWS Marketplace Console, choosing Manage Subscriptions, and confirming your third-party Bedrock model subscription shows as Active.