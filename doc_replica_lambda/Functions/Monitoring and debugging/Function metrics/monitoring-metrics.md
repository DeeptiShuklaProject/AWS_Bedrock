

# Using CloudWatch metrics with Lambda
<a name="monitoring-metrics"></a>

When your AWS Lambda function finishes processing an event, Lambda automatically sends metrics about the invocation to Amazon CloudWatch. You don't need to grant any additional permissions to your execution role to receive function metrics, and there's no additional charge for these metrics.

There are many types of metrics associated with Lambda functions. These include invocation metrics, performance metrics, concurrency metrics, asynchronous invocation metrics, and event source mapping metrics. For more information, see [Types of metrics for Lambda functions](monitoring-metrics-types.md).

In the CloudWatch console, you can [view these metrics](monitoring-metrics-view.md) and build graphs and dashboards with them. You can also set alarms to respond to changes in utilization, performance, or error rates. Lambda sends metric data to CloudWatch in 1-minute intervals. For more immediate insight into your Lambda function, you can create [high-resolution custom metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html). Charges apply for custom metrics and CloudWatch alarms. For more information, see [Amazon CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).