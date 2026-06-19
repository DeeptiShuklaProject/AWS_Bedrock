

# Monitor the `bedrock-runtime` endpoint
<a name="monitoring"></a>

The `bedrock-runtime.{{region}}.amazonaws.com` endpoint serves the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html), [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API operations. The topics in this section describe the observability options available for traffic to this endpoint, including Amazon CloudWatch metrics, AWS CloudTrail logging, and model invocation logging.

For more information about CloudWatch, see [What is Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/WhatIsCloudWatch.html) in the *Amazon CloudWatch User Guide*.

If your application calls the `bedrock-mantle.{{region}}.api.aws` endpoint, see [Monitor the `bedrock-mantle` endpoint](monitoring-mantle.md) instead.

**Topics**
+ [Monitor model invocation using CloudWatch Logs and Amazon S3](model-invocation-logging.md)
+ [Monitor `bedrock-runtime` inference using CloudWatch metrics](monitoring-runtime-metrics.md)
+ [Diagnose `InvocationLatency` increases using output tokens per second (OTPS)](monitoring-runtime-otps.md)
+ [Monitor Amazon Bedrock API calls using CloudTrail](logging-using-cloudtrail.md)