

# Prerequisites
<a name="managed-entitlements-prerequisites"></a>

Before you can use managed entitlements for Amazon Bedrock, you must complete the following prerequisites.

## AWS Organization requirements
<a name="managed-entitlements-org-requirements"></a>

**All features enabled**: Your AWS Organization must have all features enabled. Managed Entitlements for Bedrock requires this configuration to function properly. If your organization uses consolidated billing only, you must enable all features before proceeding. To enable all features, see [Enabling all features in your organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_support-all-features.html) in the AWS Organizations User Guide.

To check if your organization has all features enabled, navigate to the AWS Organizations console, choose Settings in the navigation pane, and look for Feature set under Organization details. If it displays All features, you are ready to proceed.

**Management account access**: You must have access to your organization's management account (also called the payer account) to complete the initial setup. The management account is required to enable trusted access and create service-linked roles.

**Member accounts associated**: All member accounts that will receive license grants must already be part of your AWS Organization. If you plan to add new accounts, they will automatically receive any licenses granted to your organization ID.

## Service-linked roles
<a name="managed-entitlements-slr"></a>

Service-linked roles (SLRs) are predefined IAM roles that are linked directly to AWS services. For Managed Entitlements, you must create SLRs for both AWS License Manager and AWS Marketplace. These roles include all permissions that the services require to call other AWS services on your behalf.

**Why SLRs are required**: For AWS Marketplace, this permission is required so that the service can successfully orchestrate license workflows and distributions across multiple AWS services on your behalf. For AWS License Manager, this permission enables the service to auto-accept grants between management and member accounts in an all-features-enabled organization and to track organization activity.

You will create these service-linked roles as part of the setup process described in the next section.