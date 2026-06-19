

# Frequently asked questions
<a name="cost-mgmt-faq"></a>

This section answers common questions about choosing and combining the Amazon Bedrock cost attribution mechanisms.

## Choosing a method
<a name="cost-mgmt-faq-choosing"></a>

**Q: I want per-user, per-prompt attribution. What are my choices?**

A: Use [model invocation logs](model-invocation-logging.md), not the billing-based methods. The native methods ([IAM principal attribution](cost-mgmt-iam-principal-tracking.md), [Projects](cost-mgmt-projects.md), [Application inference profiles](cost-mgmt-application-inference-profiles.md), and [Workspaces](cost-mgmt-workspaces.md)) only ever produce aggregated dollars in AWS Cost Explorer and CUR — never a per-request row. The per-prompt view exists only in your logs, where the user can come from one of two places.

The first option is to set a request-metadata tag on each call:

```
client.converse(
    modelId=...,
    messages=[...],
    requestMetadata={"user": "alice@example.com"},
)
```

The second is to rely on the auto-captured `identity.arn`, which works if your caller assumes its IAM role with a per-user `RoleSessionName`. You compute cost from the logged token counts. If you also want invoice-accurate dollars per user, run [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) alongside.

**Q: I have a specific scenario. Which method should I use?**

A: Match your scenario to a method using the following table.


| Scenario | Use | 
| --- | --- | 
| You need each team's spend on your monthly bill. | [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) (tag by team), or a tagged [Projects](cost-mgmt-projects.md) or [Application inference profiles](cost-mgmt-application-inference-profiles.md) | 
| You need cost per individual prompt, by feature. | [Per-request metadata tagging](cost-mgmt-request-metadata.md) with [model invocation logs](model-invocation-logging.md) | 
| You run many models and want one cost bucket per application. | [Projects](cost-mgmt-projects.md) on bedrock-mantle — a single project can span many models | 
| You're on InvokeModel or Converse and want per-application dollars. | [Application inference profiles](cost-mgmt-application-inference-profiles.md) | 
| You front Amazon Bedrock with a gateway serving many users. | Per-user sts:AssumeRole for billing dollars, plus [Per-request metadata tagging](cost-mgmt-request-metadata.md) for per-prompt detail | 

**Q: Should I use Projects or application inference profiles?**

A: Both deliver aggregated dollars in AWS Cost Explorer and CUR. Choose by endpoint and scale.
+ [Application inference profiles](cost-mgmt-application-inference-profiles.md) work on the `bedrock-runtime` endpoint (InvokeModel and Converse), but they are model-specific. You create one profile per model, so the resource count grows as you add models or teams.
+ [Projects](cost-mgmt-projects.md) work on the `bedrock-mantle` endpoint (Responses and Chat Completions), and a single project can span many models. They scale better when you have many models per workload, but they are mantle-only.

Use [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) alongside either one for per-user detail.

## Cost and Usage Report questions
<a name="cost-mgmt-faq-cur"></a>

**Q: What's the difference between classic CUR and CUR 2.0 for cost attribution?**

A: Activated cost allocation tags from [Projects](cost-mgmt-projects.md), [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Workspaces](cost-mgmt-workspaces.md), and IAM principal tags appear in both classic CUR and CUR 2.0. The difference is the automatic caller-identity column that makes [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) work with no tagging. That column — the "who made the call" data — exists only in a CUR 2.0 (AWS Data Exports) export with the caller-identity option selected. If you want native per-user attribution in your line-item data, you need CUR 2.0.

**Q: Can I see cost for an individual prompt in AWS Cost Explorer or CUR?**

A: No. Both classic CUR and CUR 2.0 aggregate cost by usage type over an hour or a day, and neither carries a per-request identifier on its line items. Per-prompt detail lives only in your [model invocation logs](model-invocation-logging.md). Join logs to CUR at the model and usage-type grain for reconciliation, not for per-prompt cost.

**Q: My costs are in CUR but my tags and tokens are in logs. How do I combine them?**

A: There are two patterns. For invoice-accurate totals, join logs to CUR at the model/usage-type/day grain. For per-prompt cost, compute it from the logged token counts and the published per-token rates. The following CloudWatch Logs Insights query produces the per-user, per-model token totals that feed the calculation:

```
fields requestMetadata.user as user, modelId,
       input.inputTokenCount as inTokens,
       output.outputTokenCount as outTokens
| stats sum(inTokens) as totalInput,
        sum(outTokens) as totalOutput,
        count() as calls
        by user, modelId
```

The computed figure is an estimate. It does not reflect discounts, commitments, batch pricing, free tier, or provisioned throughput unless you model them. For details, see [Getting cost from your logs](cost-mgmt-request-metadata.md#cost-mgmt-request-metadata-getting-cost).

## How the mechanisms differ
<a name="cost-mgmt-faq-differences"></a>

**Q: What's the difference between an IAM session tag and request metadata?**

A: Binding and destination. A session tag is set once at `sts:AssumeRole` and is constant for every call made with that session's credentials; it surfaces only as aggregated billing data in AWS Cost Explorer and CUR 2.0. Request metadata is set per call, varies per request, and lands in your invocation logs.

For per-user, per-prompt attribution, use request metadata. For per-user dollars on the bill, use session tags or rely on the caller identity ARN.

**Q: Does request metadata show up on my bill?**

A: No. Request metadata is not a cost allocation tag. It is written only to your [model invocation logs](model-invocation-logging.md) and never appears in AWS Cost Explorer or CUR. Use it for operational and per-prompt analysis, and use a native method (such as [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) or [Projects](cost-mgmt-projects.md)) for billed dollars.

## Implementation
<a name="cost-mgmt-faq-implementation"></a>

**Q: How does attribution work behind an LLM gateway?**

A: Amazon Bedrock records the gateway's role as the caller's identity. To preserve user-level attribution, assume the role per user, cache the credentials for the session lifetime, and pass the user as a session tag (for billing dollars) and/or as a `RoleSessionName` (so the user lands in `identity.arn` in your logs):

```
sts.assume_role(
    RoleArn=GATEWAY_ROLE,
    RoleSessionName="alice",
    Tags=[{"Key": "user", "Value": "alice@example.com"}],
)
```

For per-prompt detail without an AWS STS call per request, set the user in [request metadata](cost-mgmt-request-metadata.md) on each call instead.

**Q: Can I require that every call is tagged?**

A: Not from the Amazon Bedrock side. Request metadata is opt-in per call, and Amazon Bedrock does not reject calls that omit it. It is not an AWS Tag Policy, which only governs resources. Enforce tagging in a shared client or LLM gateway that stamps it on every request. For attribution that is always present with no per-call code, use [IAM principal attribution](cost-mgmt-iam-principal-tracking.md), since the caller identity is captured automatically.

**Q: Which fields do I set on each call, and which are automatic?**

A: Almost everything in the log record is captured automatically by Amazon Bedrock: `accountId`, `region`, `modelId`, `requestId`, `identity.arn`, the input and output token counts, and the schema metadata. The only field you supply per call is `requestMetadata`. You don't set `modelId` as a tag; it's the model or inference profile you invoked.