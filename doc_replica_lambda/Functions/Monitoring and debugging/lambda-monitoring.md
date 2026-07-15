

# Monitoring, debugging, and troubleshooting Lambda functions
<a name="lambda-monitoring"></a>

AWS Lambda integrates with other AWS services to help you monitor and troubleshoot your Lambda functions. Lambda automatically monitors Lambda functions on your behalf and reports metrics through Amazon CloudWatch. To help you monitor your code when it runs, Lambda automatically tracks the number of requests, the invocation duration per request, and the number of requests that result in an error. 

You can use other AWS services to troubleshoot your Lambda functions. This section describes how to use these AWS services to monitor, trace, debug, and troubleshoot your Lambda functions and applications. For details about function logging and errors in each runtime, see individual runtime sections. 

**Topics**
+ [Pricing](#monitoring-console-metrics-pricing)
+ [Using CloudWatch metrics with Lambda](monitoring-metrics.md)
+ [Working with Lambda function logs](monitoring-logs.md)
+ [Logging AWS Lambda API calls using AWS CloudTrail](logging-using-cloudtrail.md)
+ [Visualize Lambda function invocations using AWS X-Ray](services-xray.md)
+ [Monitor function performance with Amazon CloudWatch Lambda Insights](monitoring-insights.md)
+ [Monitoring Lambda applications](applications-console-monitoring.md)
+ [Monitor application performance with Amazon CloudWatch Application Signals](monitoring-application-signals.md)
+ [Remotely debug Lambda functions with Visual Studio Code](debugging.md)

## Pricing
<a name="monitoring-console-metrics-pricing"></a>

CloudWatch has a perpetual free tier. Beyond the free tier threshold, CloudWatch charges for metrics, dashboards, alarms, logs, and insights. For more information, see [Amazon CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/#Vended_Logs).