

# Per-request metadata tagging
<a name="cost-mgmt-request-metadata"></a>

Request metadata lets you attach key-value tags to individual Amazon Bedrock inference calls on the [`bedrock-runtime`](endpoints.md) endpoint. The tags are recorded with the request in your [model invocation logs](model-invocation-logging.md). You can then attribute usage to a team, application, environment, experiment, or any other dimension that varies per call. There is no resource to create or configure ahead of time — each call can carry a different set of tags.

Request metadata is supported on the following [`bedrock-runtime`](endpoints.md) APIs:
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
+ [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)
+ [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
+ [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)

**Note**  
Request metadata is not supported on the [`bedrock-mantle`](endpoints.md) endpoint. For attribution that flows directly into AWS Cost Explorer and AWS Cost and Usage Reports as cost allocation tags, see [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Projects](cost-mgmt-projects.md), or [Workspaces](cost-mgmt-workspaces.md).

## How request metadata works
<a name="cost-mgmt-request-metadata-how-it-works"></a>

You attach metadata to a request differently depending on which API you call:
+ **InvokeModel and InvokeModelWithResponseStream** – Set the `X-Amzn-Bedrock-Request-Metadata` HTTP header on the request. The value is a JSON object whose keys and values are strings you choose.
+ **Converse and ConverseStream** – Set the `requestMetadata` field in the request body. For more information, see [requestMetadata](conversation-inference.md#converse-request-metadata).

Request metadata is recorded in your model invocation logs only when logging is enabled in the AWS Region where the call is made. For setup instructions, see [Monitor model invocation using CloudWatch Logs and Amazon S3](model-invocation-logging.md).

The following example shows an InvokeModel request that tags the call with a team name, an environment, and a test case identifier:

```
POST /model/anthropic.claude-3-haiku-20240307-v1:0/invoke HTTP/1.1
Content-Type: application/json
X-Amzn-Bedrock-Request-Metadata: {"team": "orchestrator", "environment": "preview-test", "test_case": "invoke_model_sync"}

{
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 50,
  "messages": [{"role": "user", "content": "Say hello in one word."}]
}
```

The same header is supported on InvokeModelWithResponseStream:

```
POST /model/anthropic.claude-3-haiku-20240307-v1:0/invoke-with-response-stream HTTP/1.1
Content-Type: application/json
X-Amzn-Bedrock-Request-Metadata: {"team": "orchestrator", "environment": "preview-test", "test_case": "invoke_model_stream"}

{
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 50,
  "messages": [{"role": "user", "content": "Say hello in one word."}]
}
```

**Important**  
When you sign requests with AWS Signature Version 4 (SigV4), include `X-Amzn-Bedrock-Request-Metadata` in the `SignedHeaders` list. Requests that omit the header from the signed list are rejected with an `InvalidSignatureException`. AWS SDKs that expose request metadata as a parameter handle this automatically.

The following example sets request metadata with the AWS SDK for Python (Boto3) on a Converse call. The SDK includes the metadata in the SigV4-signed headers for you.

```
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
    modelId="us.anthropic.claude-opus-4-8",  # or an inference profile ARN
    messages=[{"role": "user", "content": [{"text": "Summarize this ticket."}]}],
    requestMetadata={
        "user": "alice@example.com",
        "team": "growth",
        "feature": "summarizer",
        "environment": "prod",
    },
)
```

## Limits
<a name="cost-mgmt-request-metadata-limits"></a>

Request metadata has the following limits, which apply to both the `X-Amzn-Bedrock-Request-Metadata` header (InvokeModel, InvokeModelWithResponseStream) and the `requestMetadata` body field (Converse, ConverseStream):
+ Maximum 16 metadata entries per request.
+ Keys: maximum 256 characters.
+ Values: maximum 256 characters.
+ Allowed characters: a restricted set of alphanumeric and punctuation characters.

Requests that exceed these limits are rejected with a validation error.

## Where request metadata appears
<a name="cost-mgmt-request-metadata-in-logs"></a>

Request metadata appears in your Amazon Bedrock model invocation logs under the top-level `requestMetadata` field. The following abbreviated log entry shows the field for an InvokeModel call:

```
{
    "schemaType": "ModelInvocationLog",
    "schemaVersion": "1.0",
    "timestamp": "2024-01-15T12:00:00Z",
    "accountId": "123456789012",
    "region": "us-east-1",
    "requestId": "abcd1234-5678-efgh-ijkl-mnopqrstuvwx",
    "operation": "InvokeModel",
    "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
    "requestMetadata": {
        "team": "orchestrator",
        "environment": "preview-test",
        "test_case": "invoke_model_sync"
    },
    "input":  { "...": "..." },
    "output": { "...": "..." }
}
```

You can filter and aggregate logs by metadata fields in Amazon CloudWatch Logs Insights, Amazon S3 query tools such as Amazon Athena, or any other system that reads invocation logs.

## Getting cost from your logs
<a name="cost-mgmt-request-metadata-getting-cost"></a>

Request metadata and token counts are written to your model invocation logs, not to your bill. There are two ways to turn them into cost.

Compute from token counts  
Each log record carries the input, output, cache-read, and cache-write token counts for the request. Multiply these by the per-token rates in [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) and group by any metadata tag. This approach is per-prompt and near real-time, but it is an estimate. You maintain the rate card. It does not reflect discounts, commitments, batch pricing, free tier, or provisioned throughput unless you model them.  
The following CloudWatch Logs Insights query totals tokens per user and model when invocation logs are delivered to CloudWatch Logs:  

```
fields requestMetadata.user as user, modelId,
       input.inputTokenCount as inTokens,
       output.outputTokenCount as outTokens
| stats sum(inTokens) as totalInput,
        sum(outTokens) as totalOutput,
        count() as calls
        by user, modelId
| sort totalInput desc
```
For logs delivered to Amazon S3, the following Amazon Athena query estimates cost by team. Replace the per-token rates with the current rates from [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/), and adjust the table and column references to match your AWS Glue table definition.  

```
SELECT requestMetadata.team       AS team,
       modelId,
       SUM(input.inputTokenCount)  AS input_tokens,
       SUM(output.outputTokenCount) AS output_tokens,
       SUM(input.inputTokenCount)  * 0.000015 AS est_input_cost,
       SUM(output.outputTokenCount) * 0.000075 AS est_output_cost
FROM bedrock_invocation_logs
GROUP BY requestMetadata.team, modelId
ORDER BY est_input_cost DESC;
```

Reconcile against CUR  
Join your invocation logs to your AWS Cost and Usage Report for invoice-accurate totals. Neither classic CUR nor CUR 2.0 includes a per-request identifier on its line items. Both aggregate cost by usage type over an hour or a day. Treat this path as reconciliation at the model and usage-type grain, with the logs providing the per-request detail underneath.

**Note**  
Request metadata and IAM session tags are different mechanisms. Request metadata is set per call and varies per request. It lands in your invocation logs. IAM session tags are bound per session and surface only as aggregated billing data in AWS Cost Explorer and CUR. For per-user, per-prompt attribution, use request metadata or a per-user identity in the ARN rather than session tags.

## Considerations
<a name="cost-mgmt-request-metadata-considerations"></a>
+ Request metadata values are recorded only when model invocation logging is enabled in the call's AWS Region. If logging is not configured, the request still succeeds but the metadata is not retained.
+ Request metadata is not delivered as an AWS cost allocation tag and does not appear in AWS Cost Explorer or CUR. To analyze costs by metadata dimension, join your invocation logs with your Cost and Usage Report on `requestId`. Alternatively, aggregate token counts directly from log records and multiply by the per-token rates in [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/). For attribution that flows natively to Cost Explorer and CUR, use [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Projects](cost-mgmt-projects.md), or [Workspaces](cost-mgmt-workspaces.md).
+ Choose stable, low-cardinality keys such as `team`, `environment`, `feature`, or `experiment` for analytics that are easy to aggregate. Use higher-cardinality values such as session or trace identifiers only when you need to trace individual calls.
+ Avoid placing personally identifiable information (PII), credentials, or other sensitive data in request metadata. Values are stored in your model invocation logs and any system that reads those logs.
+ Request metadata is supplied per call and is not enforced by Amazon Bedrock. Requests that omit it still succeed, and there is no service-side policy to require it. To guarantee coverage across an organization, set request metadata in a shared client or LLM gateway. For attribution that is always present without per-call code, use [IAM principal attribution](cost-mgmt-iam-principal-tracking.md). It captures the caller identity automatically.
+ Request metadata works alongside the other Amazon Bedrock usage tracking methods. You can use [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) for per-identity attribution and [Application inference profiles](cost-mgmt-application-inference-profiles.md) for resource-level cost allocation tags on the same workload.