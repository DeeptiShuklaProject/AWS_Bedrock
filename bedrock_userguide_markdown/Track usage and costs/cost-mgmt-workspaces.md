

# Workspaces
<a name="cost-mgmt-workspaces"></a>

[Workspaces](workspaces.md) provide cost attribution for the Anthropic-compatible [Messages API](model-parameters-anthropic-claude-messages.md) on the [`bedrock-mantle`](endpoints.md) endpoint. Workspaces are the same underlying resource as [projects](cost-mgmt-projects.md) and are managed using the Amazon Bedrock Projects API. When you tag a workspace, the tags flow to AWS Cost Explorer and AWS Cost and Usage Reports (CUR 2.0), so you can filter and group Amazon Bedrock spend by application, team, environment, cost center, or any other dimension.

For cost attribution using the Responses or Chat Completions APIs on [`bedrock-mantle`](endpoints.md), see [Projects](cost-mgmt-projects.md). For cost attribution on [`bedrock-runtime`](endpoints.md) APIs, see [Application inference profiles](cost-mgmt-application-inference-profiles.md).

## How cost attribution works
<a name="cost-mgmt-workspaces-how-it-works"></a>

You reference a workspace in a Messages API request by setting the `anthropic-workspace` HTTP header. Tags applied to the workspace are attached to the billing record for each request and appear as AWS cost allocation tags in CUR and Cost Explorer.

For details on creating workspaces, managing tags, and using the Messages API with workspaces, see [Workspaces (Anthropic-compatible)](workspaces.md).

**Note**  
Workspaces deliver aggregated billed dollars to AWS Cost Explorer and CUR 2.0. The finest grain is per usage type per day. [Per-request metadata tagging](cost-mgmt-request-metadata.md) is available only on `bedrock-runtime` APIs, so per-prompt cost detail is not currently available for Messages API workloads that use workspaces.

## Viewing workspace costs
<a name="cost-mgmt-workspaces-viewing-costs"></a>

After tagging your workspaces, activate the tags as cost allocation tags in the AWS Billing and Cost Management console:

1. Open the AWS Billing and Cost Management console.

1. In the navigation pane, choose **Cost allocation tags**.

1. Select the tags you applied to your workspaces.

1. Choose **Activate**.

Tags can take up to 24 hours to appear in Cost Explorer and CUR after activation. Cost allocation tags are not retroactive — only costs incurred after activation are tagged. For more information, see [Activating user-defined cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html).

After tag activation, you can analyze Amazon Bedrock costs by workspace in the following tools:
+ **AWS Cost Explorer** – Filter by workspace tags to view cost trends over time. Group by tag to compare costs across workspaces.
+ **AWS Cost and Usage Reports (CUR 2.0)** – Query CUR data for line-item cost breakdowns by workspace tag.