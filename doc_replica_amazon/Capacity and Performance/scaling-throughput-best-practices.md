

# Scaling and throughput best practices
<a name="scaling-throughput-best-practices"></a>

This topic explains how throughput limits and scheduling work across Amazon Bedrock endpoints and provides best practices for scaling your generative AI applications.

## Amazon Bedrock endpoints
<a name="scaling-endpoints"></a>

Amazon Bedrock supports two endpoints for inference:
+ `bedrock-mantle.{region}.api.aws` — Supports Chat Completions and Responses (from OpenAI), and Messages (from Anthropic).
+ `bedrock-runtime.{region}.amazonaws.com` — Supports Bedrock-native APIs (Invoke and Converse), Chat Completions, and Messages APIs.

For more information about these endpoints and how to choose between them, see [Endpoints supported by Amazon Bedrock](endpoints.md).

### Why the two endpoints behave differently
<a name="scaling-endpoint-differences"></a>

In many traditional multi-tenant services, the architecture is designed around per-account quotas to manage fair-share access to shared resources. This is the approach used with [`bedrock-runtime`](endpoints.md).

With [`bedrock-mantle`](endpoints.md), a different approach is used. This endpoint is architected with advanced scheduling and work-queueing mechanisms that deliver fair-share distribution while supporting higher initial throughput limits. This design also allows `bedrock-mantle` to host a broad set of models and deliver the full breadth of capabilities available across the model catalog. In most cases, requests are served immediately. In some cases, a request may be briefly queued while in-flight workloads complete and throughput becomes available. The sections below explain how to handle these scenarios.

## `bedrock-mantle` endpoint: throughput and quotas
<a name="scaling-mantle-quotas"></a>

The throughput and quota behavior on the `bedrock-mantle` endpoint differs for Anthropic Claude versus other models, as shown in the following table.


|   | Claude 4.7\+ | All other models | 
| --- | --- | --- | 
| Input TPM | 10M \* | No per-customer or per-model TPM limit | 
| Output TPM | 2M | No per-customer or per-model TPM limit | 
| On-demand tiers | Standard | Standard, Priority, Flex (some exceptions) — see the model detail pages for availability | 
| Batch | No | Yes for supported models — see the model detail pages for availability | 
| Reserved capacity | None | None | 

\* Your input TPM limit depends on your usage history with Amazon Bedrock. Check the [Quotas](https://console.aws.amazon.com/bedrock/home#/model-quotas) page in the Amazon Bedrock console for your actual allocation.

## `bedrock-runtime` endpoint: throughput and quotas
<a name="scaling-runtime-quotas"></a>

The following table summarizes the throughput and quotas for `bedrock-runtime`.


|   | Claude 4.7\+ | All other models | 
| --- | --- | --- | 
| Input TPM | 15M \* | Varies \* | 
| Output TPM | Combined with Input TPM. Burndown applies. | None. Burndown applies. | 
| RPM | Not enforced — governed by TPM | Varies by model — see the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home) | 
| On-demand tiers | Standard | Standard, Priority, Flex (some exceptions) — see the model detail pages for availability | 
| Batch | No | Yes for supported models — see the model detail pages for availability | 
| Reserved capacity | None | Reserved Tier/Provisioned Capacity | 

\* Quotas for these models vary based on usage. Check the [Quotas](https://console.aws.amazon.com/bedrock/home#/model-quotas) page in the Amazon Bedrock console for your allocations.

## Understanding HTTP error responses
<a name="scaling-http-errors"></a>

HTTP 429  
A 429 response means your request was throttled. Reduce your request submission rate. On `bedrock-runtime`, if the model has an RPM quota and you need a higher allocation, request an increase through the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home) or contact your AWS account team.

HTTP 503  
A 503 response means that there is increased demand for Amazon Bedrock in this Region. You should reduce your request rate and then either retry with exponential backoff or spread traffic across Regions.

## Recommended error handling
<a name="scaling-error-handling"></a>

### Transient errors (occasional 503 responses)
<a name="scaling-transient-errors"></a>

Implement exponential backoff with random jitter:
+ Start with a short delay (for example, 1 second).
+ Double the delay after each failed attempt.
+ Limit retries to 6 attempts.

Most AWS SDKs and popular HTTP libraries provide built-in support for this pattern.

**Example Retry configuration for `bedrock-runtime` (AWS SDK / boto3)**  

```
import boto3
from botocore.config import Config

config = Config(retries={"total_max_attempts": 6, "mode": "standard"})
client = boto3.client("bedrock-runtime", config=config)
```

**Example Retry configuration for `bedrock-mantle` (OpenAI SDK)**  

```
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url=f"https://bedrock-mantle.{region}.api.aws/v1",
    max_retries=6,
    timeout=60.0,
)
```

**Example Retry configuration for `bedrock-mantle` (Anthropic SDK)**  

```
import anthropic

client = anthropic.Anthropic(
    api_key=api_key,
    base_url=f"https://bedrock-mantle.{region}.api.aws",
    max_retries=6,
    timeout=60.0,
)
```

### Sustained errors (persistent 503 responses)
<a name="scaling-sustained-errors"></a>

If you receive sustained 503 errors, retrying alone will not resolve the issue. Your request rate exceeds available throughput. Take the following steps:
+ Reduce the rate at which your application submits new requests.
+ Implement client-side rate limiting or request queuing.
+ Shed lower-priority requests until throughput recovers.

## Ramping up throughput
<a name="scaling-ramp-up"></a>

When consuming on-demand throughput on the [`bedrock-mantle`](endpoints.md) endpoint, available throughput scales over time. Not all requests within your quota are guaranteed to succeed during periods of high demand, so ramping gradually is important.

### Recommended ramp-up procedure
<a name="scaling-ramp-procedure"></a>

1. Start at your target request volume, for example 500 RPM.

1. If you receive 503 responses, reduce your rate, for example by 50%.

1. Continue reducing by that rate until you reach a steady state where requests are succeeding consistently.

1. Hold at that steady state for a short duration, say 15 minutes.

1. Increase throughput again, for example 50%, and hold for another 15 minutes.

1. Repeat until you reach your target volume.

For example, if your target is 2,000 RPM but you receive 503 errors, reduce to 1,000 RPM. If errors persist, reduce to 500 RPM. Once requests succeed consistently at 500 RPM, hold for 15 minutes, then scale to 750, then 1,125, and so on.

Ramp rates are not adjustable. To request higher TPM quotas, use the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home) or contact your AWS account team.

## Additional best practices
<a name="scaling-additional-best-practices"></a>
+ Use feature flags to gradually transition traffic between models rather than switching all traffic at once.
+ Spread large workloads across multiple minutes and consider time-of-day patterns to avoid peak usage periods.
+ Start testing with small batches and scale gradually. Avoid sending thousands of test requests simultaneously.
+ For large offline data processing, use the [Batch API](batch-inference.md) or [Flex Tier](service-tiers-inference.md) if your application can process responses asynchronously.

## Regional availability and cross-Region inference
<a name="scaling-regional-availability"></a>

On-demand throughput is allocated at the Regional level and varies across Regions. If your workload targets a single Region, you may encounter 503 responses during periods of high demand. To maximize availability and if you are using [`bedrock-runtime`](endpoints.md), use [Global cross-Region inference](global-cross-region-inference.md).

## Getting help
<a name="scaling-getting-help"></a>
+ **Throughput planning** — Contact your AWS account team for throughput forecasting. Plan for 2x to 3x peak throughput during scaling events.
+ **Performance optimization** — Monitor token usage efficiency, optimize prompts to reduce token consumption, and select models based on your use case requirements.
+ **Support escalation** — When opening an AWS Support case for throughput issues, include the following: specific error codes, request IDs, traffic patterns (RPM/TPM), and your scaling timeline.

## Summary of recommendations
<a name="scaling-summary"></a>


| Scenario | Recommendation | 
| --- | --- | 
| General workloads | Use the [`bedrock-mantle` endpoint](endpoints.md) whenever possible. | 
| Occasional 503 errors | Retry with exponential backoff and jitter. | 
| Sustained 503 errors | Reduce request submission rate. Implement client-side rate limiting. | 
| 429 errors | Reduce request rate. On bedrock-runtime, if the model has an RPM quota, request an increase through [Service Quotas](https://console.aws.amazon.com/servicequotas/home). | 
| Large offline processing | Use [Batch API](batch-inference.md) or [Flex Tier](service-tiers-inference.md). | 