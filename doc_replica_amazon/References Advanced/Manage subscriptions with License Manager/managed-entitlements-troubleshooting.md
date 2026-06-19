

# Troubleshooting
<a name="managed-entitlements-troubleshooting"></a>

This section provides solutions to common issues you may encounter when using Managed Entitlements for Amazon Bedrock.

## License does not appear in License Manager after subscribing
<a name="managed-entitlements-ts-license-missing"></a>

**Possible causes and solutions**:
+ **Subscription not yet processed**: Wait 5 minutes and refresh the License Manager console. Licenses can take a few minutes to be created after subscription.
+ **Looking in wrong region**: Ensure you are viewing License Manager in the us-east-1 (N. Virginia) region. All licenses are created in us-east-1 regardless of subscription region.
+ **Subscription failed**: Go to AWS Marketplace Console, choose **Manage Subscriptions**, and verify the subscription shows as Active. If not active, retry the subscription process.
+ **Service-linked roles not set up**: Return to the Setting up managed entitlements section and complete all prerequisite steps. Verify SLRs exist in IAM Console by choosing **Roles** and searching for the required role names.

## Grant does not appear in recipient account
<a name="managed-entitlements-ts-grant-missing"></a>

**Possible causes and solutions**:
+ **Grant not yet distributed**: Wait 2-3 minutes after creating the grant. Check the grantor account to confirm the grant was created successfully.
+ **Recipient looking in wrong region**: The recipient must check License Manager in the us-east-1 region. All grants appear only in us-east-1.
+ **Recipient account does not have service-linked roles**: For organizations without all features enabled, each account needs service-linked roles. The recipient should complete the prerequisite steps in their own account.
+ **Wrong account ID used**: Verify the correct 12-digit AWS account ID was entered when creating the grant. Check for typos in the account ID.

## Cannot activate grant
<a name="managed-entitlements-ts-cannot-activate"></a>

**Possible causes and solutions**:
+ **Existing active license for same model**: The recipient account may already have an active license for this model. Deactivate or delete the existing license first, then activate the new grant.
+ **Grant not accepted yet**: For organizations without all features enabled, the recipient must first Accept the grant before it can be activated.
+ **Insufficient IAM permissions**: User needs `license-manager:CreateGrantVersion` permission. Contact your account administrator to grant necessary permissions.
+ **Grant in wrong state**: The grant must be in Disabled or Pending Acceptance state to activate. Check grant status in License Manager console.

## Cannot use Bedrock model after activating grant
<a name="managed-entitlements-ts-cannot-use-model"></a>

**Possible causes and solutions**:
+ **Grant not fully activated**: Check that grant status shows as Active (not Disabled or Pending). Try deactivating and reactivating the grant.
+ **Bedrock permissions missing**: User needs `bedrock:InvokeModel` IAM permission. Add Bedrock permissions to the user's IAM role or policy.
+ **Model not available in region**: Some Bedrock models are only available in specific regions. Check the Bedrock console for model availability in your region.
+ **Billing issue**: Verify the management account has a valid payment method. Check for any account holds or billing issues in the Billing console.

## Access Denied errors when setting up
<a name="managed-entitlements-ts-access-denied"></a>

**Possible causes and solutions**:
+ **Not using management account**: Setup must be done from the management or payer account. Verify you are logged into the correct account by checking the account ID in the console.
+ **Insufficient IAM permissions**: User needs `organizations:EnableAWSServiceAccess` and `iam:CreateServiceLinkedRole` permissions. Contact your administrator to grant necessary permissions.
+ **Organization not set up**: You must have an AWS Organization created first. Create an organization before attempting managed entitlements setup.

## Getting additional help
<a name="managed-entitlements-ts-additional-help"></a>

If you are still experiencing issues after trying these solutions:
+ **Check AWS Service Health Dashboard**: Visit [https://health.aws.amazon.com/health/status](https://health.aws.amazon.com/health/status) and look for any ongoing issues with License Manager, Marketplace, or Bedrock services.
+ **Review AWS CloudTrail logs**: Go to CloudTrail Console, search for events related to License Manager and Marketplace, and look for error messages or failed API calls.
+ **Contact AWS Support**: Open a support case with AWS Support. Include your account IDs, Bedrock model names, error messages, and steps you have taken. Specify that you are using Managed Entitlements for Bedrock.