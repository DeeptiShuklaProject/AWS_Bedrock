

# Frequently asked questions
<a name="managed-entitlements-faq"></a>

## Setup and configuration
<a name="managed-entitlements-faq-setup"></a>

**Q: My organization uses consolidated billing only. Can I still use managed entitlements?**

A: Yes, but with limitations. Organizations with consolidated billing can use managed entitlements, but grants will require manual acceptance in each recipient account. For the best experience, we recommend enabling all features in your organization, which allows automatic grant acceptance and organization-wide distribution.

**Q: Can I use a member account instead of the management account to manage licenses?**

A: Yes. You can designate a delegated administrator account to manage license distribution. This member account can create and distribute grants independently from the management account. However, only one delegated administrator is supported per organization.

**Q: Do I need to set up managed entitlements in every AWS region?**

A: No. All license management happens in the us-east-1 (N. Virginia) region regardless of where you use Bedrock models. Once you complete setup in us-east-1, you can invoke licensed models in any supported Bedrock region.

## Private Offers and pricing
<a name="managed-entitlements-faq-pricing"></a>

**Q: How does managed entitlements work with AWS Marketplace Private Offers?**

A: Managed entitlements allows you to accept Private Offers in your management account and then distribute access to additional linked accounts. When you create grants, the Private Offer pricing and terms automatically apply to all recipient accounts. This ensures consistent pricing across your organization and eliminates the need for each account to individually accept the offer.

**Q: Who gets billed when a member account uses a granted license?**

A: The account that holds the original subscription (typically the management account) is billed for all usage across granted accounts. This centralized billing provides clear visibility into total Bedrock costs across your organization.

**Q: Can different member accounts have different pricing for the same model?**

A: No. When you distribute licenses through managed entitlements, all recipient accounts use the same pricing terms as the original subscription, including any Private Offer discounts.

## License distribution
<a name="managed-entitlements-faq-distribution"></a>

**Q: How long does it take for grants to appear in recipient accounts?**

A: For individual account grants, licenses typically appear within 2-3 minutes. For organization-wide grants to thousands of accounts, distribution can take 15-30 minutes or longer. Check the License Manager console to verify grant status.

**Q: Do I need to create a grant for every account that needs access?**

A: No. If your organization has all features enabled, create a single grant to your Organization ID to automatically distribute licenses to all member accounts, including accounts that join later. Otherwise, create individual grants or grants to organizational units (OUs).

**Q: What happens when a new account joins my organization?**

A: If you distributed a grant to your Organization ID, new accounts automatically receive the license and access to the model. For individual account grants, you must manually create a grant for the new account.

**Q: Can I distribute licenses to accounts outside my organization?**

A: No. Managed entitlements only works within your AWS Organization. You cannot share licenses with accounts that are not part of your organization structure.

**Q: Can I grant access to specific organizational units (OUs) instead of my entire organization?**

A: Yes. When creating a grant, you can specify an OU ID to distribute licenses only to accounts within that OU. This provides a middle ground between individual account control and organization-wide distribution.

**Q: I have existing subscriptions in multiple member accounts. How do I migrate to centralized management?**

A: When member accounts have active Bedrock models and their payer account distributes them a subscription to the same model, grant swap takes effect, the entitlements to the first subscription is disabled and they now have entitlements on the new distributed grant.

## Grant management
<a name="managed-entitlements-faq-management"></a>

**Q: Can I temporarily revoke access without deleting the grant?**

A: Yes. You can deactivate the grant to move it to a Disabled state. However, deactivating a grant does not block model access — the member account can still invoke the model. What changes is the billing: while the grant is disabled, the member account will be billed at public rates instead of your negotiated private offer pricing. You can reactivate the grant later to restore private offer terms without needing to recreate it.

**Q: What happens to model access if I delete or deactivate a grant?**

A: The member account will continue to have model access — deleting or deactivating a grant does not interrupt the ability to invoke the model. However, without an active grant, the member account will be billed at public rates instead of any negotiated private offer pricing.

**Q: Can I see which accounts are actually using the licenses I distributed?**

A: In AWS License Manager, you can view which accounts have grants and their activation status. For detailed usage metrics and API call tracking, use AWS CloudTrail. For model invocation metrics, use the Amazon Bedrock console or CloudWatch metrics in each account.

**Q: If I delete a grant by mistake, can I restore it?**

A: No. Deleting a grant is permanent and cannot be undone. However, you can create a new grant to the same account with the same configuration. Model access will not be disrupted — the member account can continue invoking the model during the gap. The key impact is billing: for the duration between the grant deletion and the new grant activation, the member account will be billed at public rates rather than any negotiated private offer pricing.

**Q: What happens to granted licenses in linked accounts when the parent subscription expires in the management account?**

A: The linked accounts will lose access to the model when the parent subscription expires in the management account.

## Special configurations
<a name="managed-entitlements-faq-special"></a>

**Q: How does managed entitlements work for AWS GovCloud customers?**

A: GovCloud customers have a commercial AWS account linked to a GovCloud account. Subscribe to Bedrock models and manage licenses in the commercial account organization hierarchy. When you grant a license to a commercial linked account, the associated GovCloud account automatically receives entitlement and can invoke the model.

**Q: Can I use managed entitlements with AWS Control Tower or AWS Service Catalog?**

A: Yes. You can integrate managed entitlements APIs into your AWS Control Tower account factory or Service Catalog portfolios to automate license distribution when new accounts are created.

**Q: Can multiple management accounts subscribe to the same Bedrock model?**

A: Yes. Different accounts can subscribe to the same model independently. Each subscription creates its own separate license that can be distributed to different sets of member accounts.

## Troubleshooting
<a name="managed-entitlements-faq-troubleshooting"></a>

**Q: Why don't I see my license in License Manager after subscribing?**

A: Licenses can take 1-2 minutes to appear after subscription. Ensure you're viewing License Manager in the us-east-1 region, as all licenses are created there regardless of where you subscribed. If it still doesn't appear after 5 minutes, verify your subscription is active in the AWS Marketplace console.

**Q: My recipient account can't see the grant I created. What should I check?**

A: Verify the recipient is checking License Manager in the us-east-1 region. Confirm you entered the correct 12-digit account ID when creating the grant. Wait 2-3 minutes for grant distribution. For organizations without all features enabled, ensure the recipient account has service-linked roles created.

**Q: Why can't I activate a grant in my account?**

A: Check that the grant is in Disabled or Pending Acceptance state. If you already have an active license for the same model, deactivate or delete it first. Ensure you have the `license-manager:CreateGrantVersion` IAM permission. For consolidated billing organizations, confirm you accepted the grant before attempting activation.