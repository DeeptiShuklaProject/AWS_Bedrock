

# Monitor `bedrock-runtime` inference using CloudWatch metrics
<a name="monitoring-runtime-metrics"></a>

The Amazon Bedrock `bedrock-runtime.{{region}}.amazonaws.com` endpoint publishes metrics to Amazon CloudWatch under the `AWS/Bedrock` namespace. Use these metrics to monitor invocation volume, latency, token consumption, error rates, and model invocation logging delivery.

If your application calls inference through `bedrock-mantle.{{region}}.api.aws`, see [Monitor `bedrock-mantle` inference using CloudWatch metrics](monitoring-mantle-metrics.md) instead.

## Amazon Bedrock runtime metrics
<a name="runtime-cloudwatch-metrics"></a>

The following table describes runtime metrics provided by Amazon Bedrock.


| Metric name | Unit | Description | 
| --- | --- | --- | 
| Invocations | SampleCount | Number of successful requests to the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html), [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API operations. | 
| InvocationLatency | MilliSeconds | The time from when a request is sent to when the last token is received.<br />To distinguish latency increases caused by service-side throughput changes from increases caused by longer model responses, see [Diagnose `InvocationLatency` increases using output tokens per second (OTPS)](monitoring-runtime-otps.md). | 
| InvocationClientErrors | SampleCount | Number of invocations that result in client-side errors. | 
| InvocationServerErrors | SampleCount | Number of invocations that result in AWS server-side errors. | 
| InvocationThrottles | SampleCount | Number of invocations that the system throttled. Throttled requests and other invocation errors don't count as either Invocations or Errors. The number of throttles you see will depend on your retry settings in the SDK. For more information, see [Retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html) in the AWS SDKs and Tools Reference Guide.  | 
| InputTokenCount | SampleCount | Number of tokens in the input. | 
| LegacyModelInvocations | SampleCount | Number of invocations using [Legacy](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_FoundationModelLifecycle.html) models  | 
| OutputTokenCount | SampleCount | Number of tokens in the output. | 
| OutputImageCount | SampleCount | Number of images in the output (only applicable for image generation models). | 
| TimeToFirstToken | MilliSeconds | Time from when a request is sent to when the first token is received, for the [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) streaming API operations. | 
| EstimatedTPMQuotaUsage | SampleCount | Estimated Tokens Per Minute (TPM) quota consumption across the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html), [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API operations. This metric is an approximation and does not reflect the reservation-based token consumption that drives throttling decisions. Throttling is based on the upfront reservation of input tokens plus `max_tokens` (see [How tokens are counted in Amazon Bedrock](quotas-token-burndown.md)), which may differ from this estimate. Do not use this metric as the sole indicator for quota use or capacity planning. | 
| CacheReadInputTokens | SampleCount | Number of input tokens read from the [prompt cache](prompt-caching.md). These tokens are charged at a reduced rate and don't count toward your TPM quota. | 
| CacheWriteInputTokens | SampleCount | Number of input tokens written to the [prompt cache](prompt-caching.md). These tokens count toward your TPM quota. | 

There are also metrics for [Amazon Bedrock Guardrails](monitoring-guardrails-cw-metrics.md) and [Amazon Bedrock Agents](monitoring-agents-cw-metrics.md).

## Model invocation logging CloudWatch metrics
<a name="br-cloudwatch-metrics"></a>

For each delivery success or failure attempt, the following Amazon CloudWatch metrics are emitted under the namespace `AWS/Bedrock`, and `Across all model IDs` dimension:
+ `ModelInvocationLogsCloudWatchDeliverySuccess`
+ `ModelInvocationLogsCloudWatchDeliveryFailure`
+ `ModelInvocationLogsS3DeliverySuccess`
+ `ModelInvocationLogsS3DeliveryFailure`
+ `ModelInvocationLargeDataS3DeliverySuccess`
+ `ModelInvocationLargeDataS3DeliveryFailure`

To retrieve metrics for your Amazon Bedrock operations, you specify the following information:
+ The metric dimension. A *dimension* is a set of name-value pairs that you use to identify a metric. Amazon Bedrock supports the following dimensions:
  + `ModelId` – all metrics
  + `ModelId + ImageSize + BucketedStepSize` – OutputImageCount
+ The metric name, such as `InvocationClientErrors`. 

You can get metrics for Amazon Bedrock with the AWS Management Console, the AWS CLI, or the CloudWatch API. You can use the CloudWatch API through one of the AWS Software Development Kits (SDKs) or the CloudWatch API tools.

To view Amazon Bedrock metrics in the CloudWatch console, go to the metrics section in the navigation pane and select the all metrics option, then search for the model ID.

You must have the appropriate CloudWatch permissions to monitor Amazon Bedrock with CloudWatch For more information, see [ Authentication and Access Control for Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) in the *Amazon CloudWatch User Guide*.