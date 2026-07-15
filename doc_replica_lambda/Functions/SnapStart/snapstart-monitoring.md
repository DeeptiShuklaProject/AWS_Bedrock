

# Monitoring for Lambda SnapStart
<a name="snapstart-monitoring"></a>

You can monitor your Lambda SnapStart functions using Amazon CloudWatch, AWS X-Ray, and the [Accessing real-time telemetry data for extensions using the Telemetry API](telemetry-api.md).

**Note**  
The `AWS_LAMBDA_LOG_GROUP_NAME` and `AWS_LAMBDA_LOG_STREAM_NAME` [environment variables](configuration-envvars.md#configuration-envvars-runtime) are not available in Lambda SnapStart functions.

## Understanding logging and billing behavior with SnapStart
<a name="snapstart-cloudwatch"></a>

There are a few differences with the [CloudWatch log stream](monitoring-cloudwatchlogs.md) format for SnapStart functions:
+ **Initialization logs** – When a new execution environment is created, the `REPORT` doesn't include the `Init Duration` field. That's because Lambda initializes SnapStart functions when you create a version instead of during function invocation. For SnapStart functions, the `Init Duration` field is in the `INIT_REPORT` record. This record shows duration details for the [Init phase](lambda-runtime-environment.md#runtimes-lifecycle-ib), including the duration of any `beforeCheckpoint` [runtime hooks](snapstart-runtime-hooks.md).
+ **Invocation logs** – When a new execution environment is created, the `REPORT` includes the `Restore Duration` and `Billed Restore Duration` fields:
  + `Restore Duration`: The time it takes for Lambda to restore a snapshot, load the runtime, and run any after-restore [runtime hooks](snapstart-runtime-hooks.md). The process of restoring snapshots can include time spent on activities outside the MicroVM. This time is reported in `Restore Duration`.
  + `Billed Restore Duration`: The time it takes for Lambda to load the runtime and run any after-restore [runtime hooks](snapstart-runtime-hooks.md).

**Note**  
As with all Lambda functions, duration charges apply to code that runs in the function handler. For SnapStart functions, duration charges also apply to initialization code that's declared outside of the handler, the time it takes for the runtime to load, and any code that runs in a [runtime hook](snapstart-runtime-hooks.md).

The cold start duration is the sum of `Restore Duration` \+ `Duration`.

The following example is a Lambda Insights query that returns the latency percentiles for SnapStart functions. For more information about Lambda Insights queries, see [Example workflow using queries to troubleshoot a function](monitoring-insights.md#monitoring-insights-queries).

```
filter @type = "REPORT"
  | parse @log /\d+:\/aws\/lambda\/(?<function>.*)/
  | parse @message /Restore Duration: (?<restoreDuration>.*?) ms/
  | stats
count(*) as invocations,
pct(@duration+coalesce(@initDuration,0)+coalesce(restoreDuration,0), 50) as p50,
pct(@duration+coalesce(@initDuration,0)+coalesce(restoreDuration,0), 90) as p90,
pct(@duration+coalesce(@initDuration,0)+coalesce(restoreDuration,0), 99) as p99,
pct(@duration+coalesce(@initDuration,0)+coalesce(restoreDuration,0), 99.9) as p99.9
group by function, (ispresent(@initDuration) or ispresent(restoreDuration)) as coldstart
  | sort by coldstart desc
```

## X-Ray active tracing for SnapStart
<a name="snapstart-xray"></a>

You can use [X-Ray](services-xray.md) to trace requests to Lambda SnapStart functions. There are a few differences with the X-Ray subsegments for SnapStart functions:
+ There is no `Initialization` subsegment for SnapStart functions.
+ The `Restore` subsegment shows the time it takes for Lambda to restore a snapshot, load the runtime, and run any after-restore [ runtime hooks](snapstart-runtime-hooks.md). The process of restoring snapshots can include time spent on activities outside the MicroVM. This time is reported in the `Restore` subsegment. You aren't charged for the time spent outside the microVM to restore a snapshot.

## Telemetry API events for SnapStart
<a name="snapstart-telemetry"></a>

Lambda sends the following SnapStart events to the [Telemetry API](telemetry-api.md):
+ [`platform.restoreStart`](telemetry-schema-reference.md#platform-restoreStart) – Shows the time when the [`Restore` phase](lambda-runtime-environment.md#runtimes-lifecycle-restore) started.
+ [`platform.restoreRuntimeDone`](telemetry-schema-reference.md#platform-restoreRuntimeDone) – Shows whether the `Restore` phase was successful. Lambda sends this message when the runtime sends a `restore/next` runtime API request. There are three possible statuses: success, failure, and timeout.
+ [`platform.restoreReport`](telemetry-schema-reference.md#platform-restoreReport) – Shows how long the `Restore` phase lasted and how many milliseconds you were billed for during this phase.

## Amazon API Gateway and function URL metrics
<a name="snapstart-metrics"></a>

If you create a web API [using API Gateway](services-apigateway.md), then you can use the [IntegrationLatency](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html) metric to measure end-to-end latency (the time between when API Gateway relays a request to the backend and when it receives a response from the backend).

If you're using a [Lambda function URL](urls-configuration.md), then you can use the [UrlRequestLatency](urls-monitoring.md) metric to measure end-to-end latency (the time between when the function URL receives a request and when the function URL returns a response).