

# Setting up managed entitlements
<a name="managed-entitlements-setup"></a>

Complete the following setup steps once for your AWS Organization. After setup is complete, you can subscribe to third-party Bedrock models and distribute licenses across your organization.

## Step 1: Determine if you need a delegated admin
<a name="managed-entitlements-delegated-admin"></a>

If you will manage licenses directly from the management account, skip to Step 2. To delegate license management to a member account, designate a delegated administrator first.

**To designate a delegated administrator**

1. Sign in to your management account.

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. In the navigation pane, choose **Settings**.

1. Under **Delegated administrator**, enter the AWS account ID of the member account you want to designate.

1. Choose **Save changes**.

The delegated administrator account can now create grants and distribute licenses independently from the management account. The delegated administrator can distribute entitlements using individual account IDs, organization ID, or organizational unit IDs.

You can also designate a delegated administrator using the RegisterDelegatedAdministrator API.

Once designated, the delegated administrator completes Steps 2 and 3 from their account.

## Step 2: Enable service-linked roles and trusted access
<a name="managed-entitlements-enable-slr"></a>

You must enable trusted access and create service-linked roles for both AWS License Manager and AWS Marketplace. Complete these steps from your management account.

**To set up AWS License Manager**

1. Sign in to your management account.

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. Make sure you are in the us-east-1 (N. Virginia) Region. All license resources are created and managed in this region.

1. When you first access the License Manager console, a popup appears asking you to create a service-linked role. Choose **Create service-linked role** to accept.

1. In the navigation pane, choose **Settings**.

1. Under Account management, choose Link AWS Organization accounts.

This enables cross-account grant acceptance and creates a trusted access relationship between AWS Organizations and AWS License Manager.

**To set up AWS Marketplace**

1. While still signed in to your management account, open the AWS Marketplace console at [https://console.aws.amazon.com/marketplace/](https://console.aws.amazon.com/marketplace/).

1. In the navigation pane, choose **Settings**.

1. Under **AWS License Manager Integration**, choose **View setting details**.

1. Select both checkboxes:
   + **Enable trusted access across your organization**
   + **AWS Marketplace license management service-linked role for this account**

1. Choose **Create integration**.

This creates both the service-linked role and trusted access relationship.

**Important**  
When you select **Enable trusted access across your organization** from the management account, service-linked roles are automatically created for all member accounts in your organization. This ensures that any account that receives a grant will be able to use it.

## Step 3: Verify your setup
<a name="managed-entitlements-verify-setup"></a>

After completing the setup steps, verify that everything is configured correctly.

**To verify AWS License Manager configuration**

1. In the AWS License Manager console, choose **Settings** in the navigation pane.

1. Under **Account management**, confirm you see **AWS Organizations account linking: Enabled**.

1. Under **Organization details**, you should see your Organization ID.

**To verify AWS Marketplace configuration**

1. In the AWS Marketplace console, choose **Settings** in the navigation pane.

1. Under **AWS License Manager Integration**, confirm you see **Organization integration: Enabled**.

1. You should also see **Trusted access status: Enabled**.

**To verify service-linked roles**

1. Open the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

1. In the navigation pane, choose **Roles**.

1. In the search box, enter "AWSServiceRoleForAWSLicenseManager" and verify the role exists.

1. In the search box, enter "AWSServiceRoleForMarketplaceLicenseManagement" and verify the role exists.

If you do not see these roles, wait 2-3 minutes for IAM propagation and refresh the console. If roles still do not appear, you may need to create them manually by going to IAM console, choosing **Create role**, selecting **AWS service**, and finding License Manager or Marketplace in the service list.