

# Projects
<a name="cost-mgmt-projects"></a>

Amazon Bedrock [Projects](projects.md) provide cost attribution at the application and workload level for the [Responses API](bedrock-mantle.md) and [Chat Completions API](bedrock-mantle.md) on the `bedrock-mantle` endpoint. When you tag a project, those tags flow to AWS Cost Explorer and AWS Cost and Usage Reports (CUR 2.0), so you can filter and group Amazon Bedrock spend by application, team, environment, cost center, or any other dimension.

For cost attribution using Amazon Bedrock runtime APIs ([InvokeModel API](inference-api.md) / [Converse API](conversation-inference.md) / [Chat Completions API](inference-chat-completions.md)), see [Application inference profiles](cost-mgmt-application-inference-profiles.md).

## How cost attribution works
<a name="cost-mgmt-projects-how-it-works"></a>

When you associate an inference request with a project, the project's tags are attached to the billing record for that request. Tags appear as AWS cost allocation tags in CUR and Cost Explorer, with the same behavior as tags on other AWS resources. For more information, see [Organizing and tracking costs using AWS cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html).

Unlike [application inference profiles](cost-mgmt-application-inference-profiles.md), a project is not tied to a specific model. The model is a per-request parameter and the project ID is set on the client, so a single project can span many models. This avoids the per-model resource growth of application inference profiles. Projects apply only to the [`bedrock-mantle`](endpoints.md) endpoint.

Pass the project ID when initializing your client. All requests made with that client are attributed to the project.

**Note**  
Requests that don't specify a project ID are associated with the default project for your account.

------
#### [ Python ]

```
from openai import OpenAI

client = OpenAI(project="proj_123")

response = client.chat.completions.create(
    model="openai.gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello"}]
)
```

------
#### [ cURL ]

```
curl -X POST $OPENAI_BASE_URL/responses \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -H "OpenAI-Project: proj_123" \
    -d '{
        "model": "openai.gpt-oss-120b",
        "input": "Hello"
    }'
```

------

**Note**  
Projects deliver aggregated billed dollars to AWS Cost Explorer and CUR 2.0. The finest grain is per usage type per day; they do not produce per-request cost. [Per-request metadata tagging](cost-mgmt-request-metadata.md) is not available on the `bedrock-mantle` endpoint, so per-prompt cost detail is not currently available for Amazon Bedrock mantle workloads.

## Tagging projects for cost allocation
<a name="cost-mgmt-projects-tagging"></a>

You assign tags when you create or update a project through the [Projects API](projects.md). Common tag dimensions include:


| Tag key | Purpose | Example values | 
| --- | --- | --- | 
| Application | Identify the workload | CustomerChatbot, InternalSearch | 
| Environment | Lifecycle stage | Production, Development, Staging | 
| Team | Ownership | CustomerExperience, PlatformEngineering | 
| CostCenter | Finance mapping | CC-1001, CC-2002 | 

You can define any tags that match your organizational structure. For tag limits and naming rules, see [Tagging Amazon Bedrock resources](tagging.md).

## Viewing project costs
<a name="cost-mgmt-projects-viewing-costs"></a>

After tagging your projects, activate the tags as cost allocation tags in the AWS Billing and Cost Management console:

1. Open the AWS Billing and Cost Management console.

1. In the navigation pane, choose **Cost allocation tags**.

1. Select the tags you applied to your projects.

1. Choose **Activate**.

Tags can take up to 24 hours to appear in Cost Explorer and CUR after activation. Cost allocation tags are not retroactive. Only costs incurred after activation are tagged. For more information, see [Activating user-defined cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html).

After tag activation, you can analyze Amazon Bedrock costs by project in the following tools:
+ **AWS Cost Explorer** – Filter by project tags to view cost trends over time. Group by tag to compare costs across projects.
+ **AWS Cost and Usage Reports (CUR 2.0)** – Query CUR data for line-item cost breakdowns by project tag.