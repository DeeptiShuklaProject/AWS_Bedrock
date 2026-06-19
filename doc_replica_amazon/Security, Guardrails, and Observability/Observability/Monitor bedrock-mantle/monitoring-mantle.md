

# Monitor the `bedrock-mantle` endpoint
<a name="monitoring-mantle"></a>

The `bedrock-mantle.{{region}}.api.aws` endpoint serves the OpenAI Responses API, the OpenAI Chat Completions API, and the Anthropic Messages API. The topics in this section describe the observability options available for traffic to this endpoint, including Amazon CloudWatch metrics and AWS CloudTrail logging.

If your application calls the `bedrock-runtime.{{region}}.amazonaws.com` endpoint, see [Monitor the `bedrock-runtime` endpoint](monitoring.md) instead.

**Topics**
+ [Monitor `bedrock-mantle` inference using CloudWatch metrics](monitoring-mantle-metrics.md)
+ [Monitor `bedrock-mantle` API calls using CloudTrail](logging-cloudtrail-mantle.md)