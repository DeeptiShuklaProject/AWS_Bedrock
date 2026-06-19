

# Track usage and costs in Amazon Bedrock
<a name="cost-management"></a>

Amazon Bedrock provides multiple ways to attribute model inference usage and costs to specific users, teams, applications, environments, or experiments. You can use a single mechanism or combine several. For example, use IAM principal attribution for per-user visibility alongside projects for per-application tagging, and request metadata for per-call experiment tracking.

**Tip**  
If you're not sure which mechanism fits your use case, start with the [Frequently asked questions](cost-mgmt-faq.md) at the end of this chapter. It answers common decision questions like "I want per-user, per-prompt attribution — what are my choices?" and "What's the difference between classic CUR and CUR 2.0?".

## Choosing an approach
<a name="cost-management-choosing-approach"></a>

The cost attribution method you choose depends on which dimension you want to track, which Amazon Bedrock APIs you use, and what level of granularity you need. The following two tables present complementary views. Use the first to look up mechanisms by your goal, and the second to compare mechanisms side by side.

**Choose by goal**  
If you know what you want out of cost tracking, start here.


| If your goal is… | Use | 
| --- | --- | 
| Per-user or per-team dollars on your bill | [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) | 
| Per-application or per-workload dollars | [Application inference profiles](cost-mgmt-application-inference-profiles.md) (bedrock-runtime), or [Projects](cost-mgmt-projects.md) and [Workspaces](cost-mgmt-workspaces.md) (bedrock-mantle) | 
| Per-prompt token usage and cost, sliced by any dimension | [Per-request metadata tagging](cost-mgmt-request-metadata.md), with [model invocation logs](model-invocation-logging.md) | 
| Per-user and per-prompt detail | [Model invocation logs](model-invocation-logging.md), with the user taken from the identity ARN or a [request-metadata](cost-mgmt-request-metadata.md) tag | 
| Both invoice-accurate dollars and per-prompt detail | Combine a native method (for example, [IAM principal attribution](cost-mgmt-iam-principal-tracking.md)) with [Per-request metadata tagging](cost-mgmt-request-metadata.md) | 

**Compare mechanisms**  
The following table compares the available mechanisms by what they let you attribute by, what they output, the granularity of that output, where the data is delivered, and which endpoints they support.


| Mechanism | Attribute by | Output | Granularity | Data destination | Supported APIs | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | --- | --- | --- | --- | --- | 
| [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) | IAM identity | Billed dollars | Aggregated, per usage type per day | AWS Cost Explorer / CUR 2.0 | InvokeModel, Converse, Chat Completions | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Application inference profiles](cost-mgmt-application-inference-profiles.md) | Profile resource tags | Billed dollars | Aggregated, per usage type per day | AWS Cost Explorer / CUR 2.0 | InvokeModel, Converse, Chat Completions | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Projects](cost-mgmt-projects.md) | Project resource tags | Billed dollars | Aggregated, per usage type per day | AWS Cost Explorer / CUR 2.0 | Responses, Chat Completions | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Workspaces](cost-mgmt-workspaces.md) | Project resource tags via workspace header | Billed dollars | Aggregated, per usage type per day | AWS Cost Explorer / CUR 2.0 | Anthropic Messages | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Per-request metadata tagging](cost-mgmt-request-metadata.md) | Per-request key-value tags | Token counts (you convert to cost) | Per request | Invocation logs only | InvokeModel, InvokeModelWithResponseStream, Converse, ConverseStream | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

**Note**  
The native methods ([IAM principal attribution](cost-mgmt-iam-principal-tracking.md), [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Projects](cost-mgmt-projects.md), and [Workspaces](cost-mgmt-workspaces.md)) deliver aggregated billed dollars to AWS Cost Explorer and CUR 2.0. The finest grain is per usage type per day, attributed by identity or tag; they do not produce a per-request row. For per-prompt detail, use [model invocation logs](model-invocation-logging.md), where each call is a separate record carrying its own token counts.

## Attribution behind an LLM gateway
<a name="cost-management-llm-gateway"></a>

When a gateway or proxy calls Amazon Bedrock on behalf of many users, Amazon Bedrock records the gateway's IAM role as the caller's identity. To preserve user-level attribution, choose based on the output you need.
+ For per-user dollars in your billing tools, have the gateway assume its Amazon Bedrock role per user or tenant, using a per-user `RoleSessionName` or session tags. Cache the resulting credentials for the session lifetime to avoid an AWS STS call on every request. For more information, see [IAM principal attribution](cost-mgmt-iam-principal-tracking.md).
+ For per-prompt detail, set the user in [request metadata](cost-mgmt-request-metadata.md) on each call. Request metadata varies per request without additional AWS STS calls, which session tags cannot do on a shared session.