

# Manage model subscriptions with License Manager
<a name="managed-entitlements"></a>

**Note**  
The following guidance applies only to third-party serverless models that require AWS Marketplace subscriptions.

Organizations with multiple AWS accounts often need to provide third-party Bedrock model access across many accounts. Without centralized management, each account must have AWS Marketplace permissions and create its own subscriptions—adding operational overhead and making it difficult to enforce consistent access policies.

Managed entitlements for Amazon Bedrock solves this by letting you subscribe once from a management account and distribute access to member accounts across your AWS Organization. It works with both types of Bedrock subscriptions:
+ **Auto-enablement** – When Bedrock automatically creates a subscription on first model invocation
+ **Private offers** – Custom pricing and terms negotiated with a seller through AWS Marketplace

The distribution workflow uses AWS License Manager. When you subscribe to a model, a license is automatically created. You then create grants to share that license with other accounts in your organization. Recipients activate their grants to begin using the model—no additional marketplace transactions required.

**Note**  
All licenses are created in the us-east-1 region, regardless of where you subscribe or invoke models.