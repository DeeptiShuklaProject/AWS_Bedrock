

# Service tiers for optimizing performance and cost
<a name="service-tiers-inference"></a>

Amazon Bedrock offers four service tiers for model inference: Reserved, Priority, Standard, and Flex. With service tiers, you can optimize for availability, cost, and performance.

## Reserved Tier
<a name="w2aac28b5b5"></a>

The Reserved tier provides the ability to reserve prioritized compute capacity for your mission-critical applications that cannot tolerate any downtime. You have the flexibility to allocate different input and output tokens-per-minute capacities to match the exact requirements of your workload and control cost. When your application needs more tokens-per-minute capacity than what you reserved, the service automatically overflows to the Standard tier, ensuring uninterrupted operations. The Reserved tier targets 99.5% uptime for model response. Customers can reserve capacity for 1 month or 3 month duration. Customers pay a fixed price per 1K tokens-per-minute and are billed monthly.

The Reserved tier has the following minimum capacity requirements:
+ **Minimum input tokens-per-minute (TPM):** 100,000
+ **Minimum output tokens-per-minute (TPM):** 10,000

To get access to the Reserved tier, please contact your AWS account team.

**Important**  
When sizing your Reserved tier capacity, note that your tokens-per-minute consumption includes both `InputTokenCount` and `CacheWriteInputTokens`. If you use [prompt caching](prompt-caching.md), you should sum both metrics in Amazon CloudWatch to accurately estimate your required reservation. For more information about how tokens are counted toward your quota, see [Understanding token quota management](quotas-token-burndown.md#quotas-token-burndown-management).

**Note**  
Billing continues until you delete the Reserved Tier reservation with the help of your AWS account manager.

## Priority Tier
<a name="w2aac28b5b7"></a>

The Priority tier delivers the fastest response times for a price premium over standard on-demand pricing. It is best suited for mission-critical applications with customer-facing business workflows that do not warrant 24X7 capacity reservation. Priority tier does not require prior reservation. You can simply set the "service\_tier" optional parameter to "priority" to avail request level prioritization. Priority tier requests are prioritized over Standard and Flex tier requests.

## Standard Tier
<a name="w2aac28b5b9"></a>

The Standard tier provides consistent performance for everyday AI tasks such as content generation, text analysis, and routine document processing. By default all inference requests are routed to the Standard tier when the "service\_tier" parameter is missing. You can also set the "service\_tier" optional parameter to "default" for your inference request to be served with Standard tier.

## Flex Tier
<a name="w2aac28b5c11"></a>

For workloads that can handle longer processing times, the Flex tier offers cost-effective processing for a pricing discount. This helps you optimize cost for workloads such as model evaluations, content summarization, and agentic workflows. You can set the "service\_tier" optional parameter to "flex" for your inference request to be served with the Flex tier and avail the pricing discount.

## Using the service tier capability
<a name="w2aac28b5c13"></a>

To access the service tier capability, you can set the "service\_tier" optional parameter to "reserved", "priority", "default", or "flex" while calling the Amazon Bedrock runtime API.

```
"service_tier" : "reserved | priority | default | flex"
```

Your on-demand quota for a model is shared across the "priority", "default", and "flex" service tiers. Your "reserved" tier capacity reservation is separate from your on-demand quota. The service tier configuration for a served request is visible in API response and AWS CloudTrail Events. You can also view service tier metrics in Amazon CloudWatch Metrics under ModelId, ServiceTier, and ResolvedServiceTier, where ResolvedServiceTier shows the actual tier that served your requests.

For more information about pricing, visit the [pricing page](https://aws.amazon.com/bedrock/pricing/).

Please go to [Models at a glance](model-cards.md) and choose the model you are interested in to see which service tier that model supports.

To control access to service tiers refer [Control access to service tiers](security_iam_id-based-policy-examples-agent.md#security_iam_id-based-policy-examples-service-tiers)