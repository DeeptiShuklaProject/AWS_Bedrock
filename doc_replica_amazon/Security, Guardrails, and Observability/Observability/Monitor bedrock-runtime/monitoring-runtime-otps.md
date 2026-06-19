

# Diagnose `InvocationLatency` increases using output tokens per second (OTPS)
<a name="monitoring-runtime-otps"></a>

The `InvocationLatency` metric reports the wall-clock time of an inference request, from when the request is received to when the last output token is produced. By itself, this metric cannot tell you *why* latency increased. The same elevated value can result from two different conditions:
+ The model is generating tokens more slowly — a service-side throughput change.
+ The model is generating more tokens per request — a workload change such as a longer prompt, an updated system prompt, or a model update that produces longer responses.

Output tokens per second (OTPS) isolates the throughput component, so you can alarm on service-side degradation without producing false positives when output length grows.

**Note**  
OTPS calculation requires the `TimeToFirstToken` metric, which Amazon Bedrock publishes only for the streaming API operations [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html). The procedures in this section apply only to traffic on those operations.

## How `InvocationLatency`, `TimeToFirstToken`, and OTPS relate
<a name="monitoring-runtime-otps-formula"></a>

An inference request passes through two compute-bound stages on the model host:
+ **Prefill.** The model processes the entire input prompt in a single forward pass and produces the first output token. The duration of this stage scales primarily with input length and is the main driver of `TimeToFirstToken`.
+ **Decode.** The model generates each subsequent output token sequentially, one token per forward pass. The total time of this stage scales with the number of output tokens. Per-token decode time is fairly stable for a given model and host load, which is what makes OTPS a useful throughput signal.

These stages produce the following relationship between Amazon Bedrock runtime metrics:

```
InvocationLatency (ms) = TimeToFirstToken (ms) + (OutputTokenCount / OTPS) * 1000
```

Solving for OTPS gives the formula you can compute from published CloudWatch metrics:

```
OTPS = OutputTokenCount / (InvocationLatency - TimeToFirstToken) * 1000
```

A stable OTPS over time indicates that the model is generating at expected throughput, even if `InvocationLatency` is elevated due to longer prompts or longer responses. A drop in OTPS indicates a model-side throughput change, which is the signal you typically want to alarm on.

## Calculate OTPS using a CloudWatch metric math expression
<a name="monitoring-runtime-otps-metric-math"></a>

You can graph OTPS in the CloudWatch console by combining published Amazon Bedrock runtime metrics in a metric math expression. The metrics needed are `InvocationLatency`, `OutputTokenCount`, and `TimeToFirstToken`, all in the `AWS/Bedrock` namespace. For descriptions of these metrics, see [Amazon Bedrock runtime metrics](monitoring-runtime-metrics.md#runtime-cloudwatch-metrics).

1. Open the CloudWatch console and choose **Metrics**, then **All metrics**.

1. Search for `Bedrock` and select the **By ModelId** dimension.

1. Select `InvocationLatency`, `OutputTokenCount`, and `TimeToFirstToken` for the model ID you want to monitor.

1. For each selected metric, set **Statistic** to `p50` and **Period** to **5 minutes**.

1. Choose **Add math**, then **Start with empty expression**.

1. Enter the following expression and label it `OTPS`. Adjust the metric IDs (`m1`, `m2`, `m3`) to match the IDs assigned to `InvocationLatency`, `OutputTokenCount`, and `TimeToFirstToken` in your selection.

   ```
   m2 / (m1 - m3) * 1000
   ```

The graph now shows p50 OTPS per 5-minute window for the selected model. You can use this metric math expression as the basis for an alarm.

## Create a CloudWatch alarm on OTPS
<a name="monitoring-runtime-otps-alarm"></a>

Because OTPS is a metric math expression rather than a published metric, you alarm on it by creating a metric math alarm. Two patterns are useful, depending on whether you have an established throughput baseline.

### Static threshold alarm
<a name="monitoring-runtime-otps-alarm-static"></a>

Use a static threshold alarm when you have an established baseline OTPS for your model, for example from benchmarking or historical traffic.

1. From the OTPS metric math expression created in the preceding procedure, choose the alarm icon to create an alarm.

1. For **Threshold type**, choose **Static**.

1. For the alarm condition, choose **Lower than** and enter your threshold. A common starting point is 80 percent of your expected baseline. For example, if your model typically achieves 55 tokens per second, set the threshold to 44 tokens per second.

1. Under **Additional configuration**, set the evaluation to **3 out of 5** datapoints breaching to reduce noise from transient dips.

1. Set the missing data treatment to **Treat missing data as breaching** if you want gaps to count as degradation, or **Treat missing data as missing** if missing data is expected during low-traffic periods.

### Anomaly detection alarm
<a name="monitoring-runtime-otps-alarm-anomaly"></a>

Use an anomaly detection alarm when workload patterns vary over time and you want the threshold to adapt automatically. Anomaly detection requires sufficient historical data (at least two weeks) to build an accurate model. For new deployments, start with a static threshold.

1. Create the alarm from the OTPS metric math expression as in the preceding procedure, but for **Threshold type**, choose **Anomaly detection**.

1. Choose **Lower than the band**. OTPS drops, not spikes, indicate degradation.

1. Set the anomaly detection threshold to 2 or 3 standard deviations. Lower values produce a more sensitive alarm.

1. Use 3 out of 5 evaluation periods.

1. Set the missing data treatment as described in the static threshold procedure.

## Create the alarm programmatically with the AWS SDK for Python (Boto3)
<a name="monitoring-runtime-otps-boto3"></a>

The following Python example uses the AWS SDK for Python (Boto3) to create the static threshold alarm described in the preceding section. Replace `MODEL_ID`, `OTPS_THRESHOLD`, and `AlarmActions` with values appropriate for your environment.

```
import boto3

cw = boto3.client("cloudwatch", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
ALARM_NAME = "Bedrock-OTPS-Low"
OTPS_THRESHOLD = 44  # tokens/s; set to ~80% of your expected baseline

cw.put_metric_alarm(
    AlarmName=ALARM_NAME,
    AlarmDescription="Fires when Bedrock OTPS drops below threshold, indicating model-side throughput degradation.",
    Metrics=[
        {
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/Bedrock",
                    "MetricName": "InvocationLatency",
                    "Dimensions": [{"Name": "ModelId", "Value": MODEL_ID}],
                },
                "Period": 300,
                "Stat": "p50",
            },
            "ReturnData": False,
        },
        {
            "Id": "m2",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/Bedrock",
                    "MetricName": "OutputTokenCount",
                    "Dimensions": [{"Name": "ModelId", "Value": MODEL_ID}],
                },
                "Period": 300,
                "Stat": "p50",
            },
            "ReturnData": False,
        },
        {
            "Id": "m3",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/Bedrock",
                    "MetricName": "TimeToFirstToken",
                    "Dimensions": [{"Name": "ModelId", "Value": MODEL_ID}],
                },
                "Period": 300,
                "Stat": "p50",
            },
            "ReturnData": False,
        },
        {
            "Id": "otps",
            "Expression": "m2 / (m1 - m3) * 1000",
            "Label": "OTPS",
            "ReturnData": True,
        },
    ],
    ComparisonOperator="LessThanThreshold",
    Threshold=OTPS_THRESHOLD,
    EvaluationPeriods=5,
    DatapointsToAlarm=3,
    TreatMissingData="ignore",
    AlarmActions=[],  # add SNS ARN, for example "arn:aws:sns:us-east-1:123456789012:my-topic"
)

print(f"Alarm '{ALARM_NAME}' created.")
```