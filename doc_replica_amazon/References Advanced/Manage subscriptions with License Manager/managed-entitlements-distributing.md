

# Distributing licenses
<a name="managed-entitlements-distributing"></a>

After you have subscribed to a third-party Bedrock model and verified that a license has been created, you can create grants to distribute access to other accounts in your organization.

## Understanding grant distribution options
<a name="managed-entitlements-grant-options"></a>

You can distribute licenses using three methods:

**Individual account grants**: Create a grant for a specific AWS account ID. This method gives you precise control over which accounts receive access to the model. The recipient account must accept and activate the grant before using the model.

**Organization grants**: Create a single grant to your entire AWS Organization ID. This method automatically distributes the license to all member accounts in your organization. New accounts that join the organization automatically receive the license. For organizations with all features enabled, grants are automatically accepted and appear in a Disabled state, ready for activation.

**Organizational unit grants**: Create a grant to a specific organizational unit (OU) within your organization. This method distributes the license to all accounts within the specified OU, providing a middle ground between individual account control and organization-wide distribution.

## Create Grants
<a name="managed-entitlements-create-grants"></a>

### Console
<a name="managed-entitlements-create-grants-console"></a>

**To create a grant to an individual account**

1. Sign in to your management account (or delegated administrator account).

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. Make sure you are in the us-east-1 Region.

1. In the navigation pane, choose **Granted Licenses**.

1. Select the license you want to share by choosing the radio button next to the license.

1. Choose **Create grant**.

1. Under **Grant details**, enter a descriptive name for the grant in **Grant name**.

1. Under **AWS account ID or AWS Organization ID or AWS Organizational Unit ID**, enter the 12-digit AWS account ID of the recipient account.

1. Review your grant details.

1. Choose **Create grant**.

The grant is created and will appear in the recipient account's License Manager console in a Pending Acceptance or Disabled state, depending on your organization configuration.

**To create a grant to your organization**

1. Follow steps 1-6 from the previous procedure.

1. Under **Grant details**, enter a descriptive name for the grant in **Grant name**.

1. Under **AWS account ID or AWS Organization ID or AWS Organizational Unit ID**, enter your AWS Organization ID.
   + To find your organization ID, open the AWS Organizations console. The ID appears in the navigation pane and starts with "o-".

1. Review your grant details.

1. Choose **Create grant**.

The grant is created and automatically distributed to all member accounts in your organization. For organizations with all features enabled, grants are automatically accepted and appear in a Disabled state in each member account.

**To create a grant to an organizational unit**

1. Follow steps 1-6 from the create individual grant procedure.

1. Under **Grant details**, enter a descriptive name for the grant in **Grant name**.

1. Under **AWS account ID or AWS Organization ID or AWS Organizational Unit ID**, enter your organizational unit (OU) ID.
   + To find your OU ID, open the AWS Organizations console and navigate to your OU. The ID starts with "ou-".

1. Review your grant details.

1. Choose **Create grant**.

The grant is created and automatically distributed to all member accounts within the specified organizational unit.

Replace the license ARN, account ID, and organization ID with your actual values.

### API
<a name="managed-entitlements-create-grants-api"></a>

Creates a grant to distribute a license to other AWS accounts, organizations, or organizational units through [CreateGrantAPI](https://docs.aws.amazon.com/license-manager/latest/APIReference/API_CreateGrant.html)

## Tracking distributed grants
<a name="managed-entitlements-tracking-grants"></a>

As the grantor or administrator, you can track all grants you have created.

### Console
<a name="managed-entitlements-tracking-grants-console"></a>

**To view your distributed grants**

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. In the navigation pane, choose **Granted Licenses**.

1. Choose the license for which you want to review grants.

1. On the license details page, scroll to the **Grants** section.

1. You will see a list of all grants created for this license, including grant name, recipient, and status.

For organization-wide grants, you can view individual account-level grant statuses by choosing the grant name to see the grant details page.

### API
<a name="managed-entitlements-tracking-grants-api"></a>

You can also view distributed grants using the [ListDistributedGrants API.](https://docs.aws.amazon.com/license-manager/latest/APIReference/API_ListDistributedGrants.html)