

# IAM principal attribution
<a name="cost-mgmt-iam-principal-tracking"></a>

Amazon Bedrock automatically captures the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html) identity ([IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) and [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)) for every inference request. You can optionally attach tags to your principals for additional cost dimensions like team, department, or cost center. This gives you per-user and per-role cost visibility without code changes or additional resources.

IAM principal attribution currently works with Amazon Bedrock `bedrock-runtime` APIs ([InvokeModel API](inference-api.md) / [Converse API](conversation-inference.md) / [Chat Completions API](inference-chat-completions.md)). Support for `bedrock-mantle` APIs is coming soon.

## How it works
<a name="cost-mgmt-iam-principal-tracking-how-it-works"></a>

When an IAM user or role makes an inference request, Amazon Bedrock records the caller's identity. This information flows into AWS Cost Explorer and AWS Cost and Usage Reports (CUR 2.0), where you can filter and group costs by identity. No changes to your Amazon Bedrock API calls are required. Attribution is based on who made the call, not on API parameters.

Optionally, you can attach tags to your IAM principals to add organizational dimensions (team, department, cost center) to your billing data. Tags are not required for identity-level attribution. The caller identity is always captured.

**Note**  
IAM principal attribution delivers aggregated cost to AWS Cost Explorer and CUR 2.0. The finest grain is per usage type per day, attributed by identity or tag — it does not produce per-request cost. For per-prompt detail, see [Per-request metadata tagging](cost-mgmt-request-metadata.md) and [Monitor model invocation using CloudWatch Logs and Amazon S3](model-invocation-logging.md).

## Principal types
<a name="cost-mgmt-iam-principal-tracking-principal-types"></a>

Amazon Bedrock captures identity from any IAM principal type. The two most common are IAM users and IAM roles.

**IAM users** call Amazon Bedrock directly using long-lived access keys. The IAM user name and any tags attached to the user are recorded in AWS Billing.

**IAM roles** are assumed by users, applications, or federated identities via AWS STS. When a principal calls `sts:AssumeRole`, the resulting temporary credentials carry the role's identity. Tags can come from two sources:
+ **Principal tags** – Tags attached directly to the IAM role. These are static and apply to every session.
+ **Session tags** – Tags passed at the time of role assumption via AWS STS. These are dynamic and can vary per session, making them useful for passing user-specific attributes like email, team, or cost center through a shared role.

**Important**  
If a session tag and a principal tag share the same key, the session tag value overrides the principal tag value for that session. For more information, see [Pass session tags in AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html).

Most organizations use roles rather than IAM users for Amazon Bedrock access. If multiple users share the same role, session tags are how you distinguish them in billing.

## Setting up IAM principal attribution
<a name="cost-mgmt-iam-principal-tracking-setup"></a>

Identity-level attribution (the caller's IAM user or role ARN) is captured automatically for every Amazon Bedrock request. To add organizational dimensions like team or cost center to your billing data, follow these steps to tag your principals and activate the tags in AWS Billing.

### Step 1: Apply tags to your IAM principals (optional)
<a name="cost-mgmt-iam-principal-tracking-setup-principal-tags"></a>

Tags flow to your billing data in two ways:

**Principal tags** are attached directly to IAM users or roles. Set them once and they apply to every request from that principal. This is ideal for tagging individual developers (IAM users) or applications (IAM roles). You can apply principal tags using the IAM console, the AWS CLI (`aws iam tag-role`, `aws iam tag-user`), or the IAM API (`TagRole`, `TagUser`).

To learn more about IAM tagging and best practices, see [Tags for IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html).

**Session tags** are passed dynamically when assuming an IAM role via AWS STS. They are ideal for federated users (authenticating through an identity provider like Okta, Auth0, or Entra) and LLM gateways that proxy requests on behalf of multiple users or tenants. Session tags can be passed in three ways:
+ **AssumeRole** – Pass `--tags` when calling `sts:AssumeRole` (for example, an LLM gateway assuming a Amazon Bedrock role per user or tenant).
+ **AssumeRoleWithWebIdentity (OIDC)** – Embed tags in the `https://aws.amazon.com/tags` claim in the ID token issued by your identity provider.
+ **AssumeRoleWithSAML** – Map `PrincipalTag:*` attributes in your IdP's SAML assertion.

The IAM role's trust policy must allow `sts:TagSession` for session tags to flow through. To learn more, see [Pass session tags in AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html).

Both principal tags and session tags appear in CUR 2.0 with the `iamPrincipal/` prefix.

### Step 2: Activate cost allocation tags
<a name="cost-mgmt-iam-principal-tracking-setup-activate-tags"></a>

To make your IAM principal tags appear in AWS Cost Explorer and CUR 2.0, you must activate them as cost allocation tags:

1. Open the AWS Billing and Cost Management console.

1. In the navigation pane, choose **Cost allocation tags**.

1. Filter by type **IAM principal** to find the tags you applied to your principals.

1. Select the tags and choose **Activate**.

**Note**  
Tags only appear in AWS Billing after the IAM principal makes at least one Amazon Bedrock API call. Cost allocation tags are not retroactive — only costs incurred after activation are tagged. Tags can take up to 24 hours to appear after activation.

### Step 3: Create a CUR 2.0 data export with IAM-level data
<a name="cost-mgmt-iam-principal-tracking-setup-enable-cur"></a>

To see identity-level cost breakdowns, create a CUR 2.0 data export that includes the caller identity:

1. Open the AWS Billing and Cost Management console.

1. In the navigation pane, choose **Data Exports**.

1. Choose **Create** to create a new CUR 2.0 export.

1. Configure the export and ensure you select the option to include the caller identity ARN.

**Important**  
If you created a CUR 2.0 data export before enabling IAM principal attribution, you must create a new export and select the caller identity option. Existing exports do not retroactively include identity data. You must also ensure that your cost allocation tags are activated (Step 2) for tags to appear in the export.

For more information, see [Creating reports](https://docs.aws.amazon.com/cur/latest/userguide/cur-create.html) in the AWS Cost and Usage Reports User Guide.

## Tagging dimensions
<a name="cost-mgmt-iam-principal-tracking-tagging-dimensions"></a>

You can use any tag key that represents your organizational structure. Common dimensions include:


| Tag key | Purpose | Example values | 
| --- | --- | --- | 
| User | Individual identity | jane@example.com, bob@example.com | 
| Team | Ownership | PlatformEngineering, DataScience | 
| Department | Organizational unit | Engineering, Research, Marketing | 
| CostCenter | Finance mapping | CC-1001, CC-2002 | 
| Environment | Lifecycle stage | Production, Development | 

You can apply up to 50 principal or session tags per IAM user or role.

## Federated access and session tags
<a name="cost-mgmt-iam-principal-tracking-federated"></a>

For organizations using federated identity providers (AWS IAM Identity Center, Okta, Entra, Ping), session tags let you pass user attributes from your IdP to AWS. When a federated user assumes a role through AWS STS, the IdP can pass attributes like user email, team, and cost center as session tags. These tags are captured alongside the Amazon Bedrock request and flow to AWS CUR 2.0 and AWS Cost Explorer.

To set this up:

1. Configure your IdP to include user attributes (email, team, cost center) as SAML attributes or OIDC claims.

1. Map those attributes to AWS session tags in your IAM role's trust policy using `sts:TagSession`.

1. The session tags are then available as cost allocation tags in AWS Billing after activation.

For more information, see [Passing session tags in AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html).

The following Python example shows a gateway assuming its Amazon Bedrock role for a specific user, passing the user as both a `RoleSessionName` (which appears in `identity.arn` in your invocation logs) and as session tags (which surface as cost allocation data in AWS Cost Explorer and CUR 2.0). The role's trust policy must allow `sts:TagSession`. Cache the returned credentials for the session lifetime instead of calling `AssumeRole` on every request.

```
import boto3

sts = boto3.client("sts")

creds = sts.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/BedrockGatewayRole",
    RoleSessionName="alice",                       # appears in identity.arn
    Tags=[
        {"Key": "user", "Value": "alice@example.com"},
        {"Key": "team", "Value": "growth"},
    ],                                             # session tags, surface as cost allocation data
)["Credentials"]

bedrock = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"],
)
# Every call made with this client is attributed to alice in billing
# and carries her identity ARN in invocation logs.
```

**Important**  
Identity and session tags are bound at AWS STS AssumeRole time and are recorded against the session, not the individual request. Their values are constant across every call made with that session's credentials, and they surface only as aggregated billing data. Session tags are not written to your [model invocation logs](model-invocation-logging.md); logs capture the caller's `identity.arn` instead. To distinguish users on a shared session at the request level, use a per-user `RoleSessionName` so the identity ARN differs per user, or set the user in [request metadata](cost-mgmt-request-metadata.md) on each call.

## Invocation patterns
<a name="cost-mgmt-iam-principal-tracking-invocation-patterns"></a>

IAM principal attribution works regardless of how your application calls Amazon Bedrock:


| Pattern | How identity flows | 
| --- | --- | 
| Direct API call | IAM user or role identity captured automatically | 
| API Gateway | Identity of the role invoking Amazon Bedrock is captured | 
| LLM Gateway (LiteLLM, custom) | Identity of the gateway's execution role is captured. Pass session tags from the gateway to preserve user-level attribution. | 
| Federated identity (Okta, Entra) | Session tags from the IdP are captured during role assumption | 

If you use an LLM gateway or API gateway and do not see user-level identity in AWS Billing, confirm that the gateway is passing session tags with each request.

**Note**  
If your gateway re-assumes the role per user to vary identity or session tags, assume the role once per user and cache the credentials for the session lifetime. Calling `sts:AssumeRole` on every request can exceed AWS STS request rate quotas.

## Viewing costs
<a name="cost-mgmt-iam-principal-tracking-viewing-costs"></a>

After activating your cost allocation tags, you can analyze Amazon Bedrock costs by principal in the following tools:
+ **AWS Cost Explorer** – Filter by principal tags to view cost trends by user, team, or department. Group by tag to compare costs across dimensions.
+ **AWS Cost and Usage Reports (CUR 2.0)** – Query CUR data for line-item cost breakdowns by principal tag.

Cost data can take up to 24 hours to appear in AWS Cost Explorer and CUR 2.0 after a request is made.

## Using IAM principal attribution with other methods
<a name="cost-mgmt-iam-principal-tracking-with-other-methods"></a>

IAM principal attribution can be used alongside Projects and application inference profiles. This gives you multi-dimensional cost visibility.

We recommend using Projects for application-level attribution and IAM principal attribution for user-level attribution within the same account.


| Method | Attributes by | Supported APIs | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | --- | --- | 
| IAM principal attribution | Identity (user, role, team) | [InvokeModel API](inference-api.md) / [Converse API](conversation-inference.md) / [Chat Completions API](inference-chat-completions.md) | ![Green circular icon with a white checkmark symbol inside.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circular icon with an X symbol, indicating cancellation or denial.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| Projects (Recommended) | Application or workload | [Responses API](bedrock-mantle.md) / [Chat Completions API](bedrock-mantle.md) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| Application inference profiles | Application or workload | [InvokeModel API](inference-api.md) / [Converse API](conversation-inference.md) / [Chat Completions API](inference-chat-completions.md) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 