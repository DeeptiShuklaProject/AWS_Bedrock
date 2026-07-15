

# Monitoring Lambda functions with tenant isolation
<a name="tenant-isolation-monitor"></a>

You can monitor your tenant-isolated Lambda functions using Amazon CloudWatch, AWS X-Ray, and by accessing real-time telemetry data for extensions [using the Telemetry API](telemetry-api.md).

## Understanding logging for tenant isolated mode
<a name="tenant-isolation-logging"></a>

For functions using tenant isolation, Lambda automatically includes the tenant identifier in [function logs](monitoring-logs.md) when you have [JSON logging enabled](monitoring-cloudwatchlogs-logformat.md), making it easier to monitor and debug tenant-specific issues. Lambda creates a separate [CloudWatch log stream](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) for each execution environment. You can use CloudWatch Logs Insights to find log streams that belong to a particular tenant by filtering by tenant identifier:

```
fields @logStream, @message
| filter tenantId=='BlueTenant' or record.tenantId=='BlueTenant'
| stats count() as logCount by @logStream
| sort @timestamp desc
```

You can also use this parameter to retrieve tenant-specific logs across all log streams:

```
fields @message
| filter tenantId=='BlueTenant' or record.tenantId=='BlueTenant'
| limit 1000
```

The `tenantId` property is included for platforms events (like `platform.start` and `platform.report`) and custom logs you print in your function code, as shown below:

```
{
    "time": "2025-10-13T19:48:06.990Z",
    "type": "platform.start",
    "record": {
        "requestId": "a0f40320-b43c-44b3-91bf-d5b5240a1bed",
        "functionArn": "arn:aws:lambda:us-east-1:xxxxxx:function:multitenant-function-1",
        "version": "$LATEST",
        {{"tenantId": "BlueTenant"}}"
    }
}
{
    "timestamp": "2025-10-13T19:48:06.992Z",
    "level": "INFO",
    "requestId": "a0f40320-b43c-44b3-91bf-d5b5240a1bed",
    {{"tenantId": "BlueTenant"}}",
    "message": "custom log line1"
}
{
    "timestamp": "2025-10-13T19:48:07.022Z",
    "level": "WARN",
    "requestId": "a0f40320-b43c-44b3-91bf-d5b5240a1bed",
    {{"tenantId": "BlueTenant"}}",
    "message": "custom log line2"
}
```