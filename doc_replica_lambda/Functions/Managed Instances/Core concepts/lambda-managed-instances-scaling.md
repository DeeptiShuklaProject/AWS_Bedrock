

# Scaling Lambda Managed Instances
<a name="lambda-managed-instances-scaling"></a>

Lambda Managed Instances does not scale when invocations arrive and does not support cold starts. Instead, it scales asynchronously using resource consumption signals. Managed Instances currently scales based on CPU resource utilization and multi-concurrency saturation.

**Key differences:**
+ **Lambda (default):** Scales when there is no free execution environment to handle an incoming invocation (cold start)
+ **Lambda Managed Instances:** Scales asynchronously based on CPU resource utilization and multi-concurrency saturation of execution environments

If your traffic more than doubles within 5 minutes, you may see throttles as Lambda scales up instances and execution environments to meet demand.

## The scaling lifecycle
<a name="lambda-managed-instances-scaling-lifecycle"></a>

Lambda Managed Instances uses a distributed architecture to manage scaling:

**Components:**
+ **Managed Instances** - Run in your account in the subnets you provide
+ **Router and Scaler** - Shared Lambda components that route invocations and manage scaling
+ **Lambda Agent** - Runs on each Managed Instance to manage execution environment lifecycle and monitor resource consumption

**How it works:**

1. When you publish a function version with a capacity provider, Lambda launches Managed Instances in your account. It launches three by default for AZ resiliency and starts three execution environments before marking your function version ACTIVE.

1. Each Managed Instance can run execution environments for multiple functions mapped to the same capacity provider.

1. As traffic flows into your application, execution environments consume resources. The Lambda Agent notifies the Scaler, which decides whether to scale new execution environments or Managed Instances.

1. If Router attempts to send an invocation to an execution environment with high resource consumption, the Lambda Agent on that instance notifies it to retry on another.

1. As traffic decreases, the Lambda Agent notifies Scaler, which makes a decision to scale down execution environments and scale in Managed Instances.

## Adjusting scaling behavior
<a name="lambda-managed-instances-adjusting-scaling"></a>

You can customize the scaling behavior of Managed Instances through five controls:

### Function level controls
<a name="lambda-managed-instances-function-level-controls"></a>

#### 1. Function memory and vCPUs
<a name="lambda-managed-instances-function-memory-vcpus"></a>

Choose the memory size and vCPU allocation for your function. The smallest supported function size is 2GB and 1vCPU.

**Considerations:**
+ Pick a memory and vCPU setting that will support multi-concurrent executions of your function
+ You cannot configure a function with less than 1 vCPU because functions running on Managed Instances should support multi-concurrent workloads
+ You cannot choose less than 2GB because this matches the 2 to 1 memory to vCPU ratio of c instances, which have the lowest ratio
+ For Python applications, you may need to choose a higher ratio of memory to vCPUs, such as 4 to 1 or 8 to 1, because of the way Python handles multi-concurrency
+ If you are running CPU-intensive operations or perform little IO, you should choose more than one vCPU

#### 2. Maximum concurrency
<a name="lambda-managed-instances-maximum-concurrency"></a>

Set the maximum concurrency per execution environment.

**Default behavior:** Lambda chooses sensible defaults that balance resource consumption and throughput that work for a wide variety of applications.

**Adjustment guidelines:**
+ **Increase concurrency:** If your function invocations use very little CPU, you can increase maximum concurrency up to a maximum of 64 per vCPU
+ **Decrease concurrency:** If your application consumes a large amount of memory and very little CPU, you can reduce your maximum concurrency

**Important:** Since Lambda Managed Instances are meant for multi-concurrent applications, execution environments with very low concurrency may experience throttles when scaling. When invocations arrive at an execution environment that has reached its concurrency limit, Lambda routes those invocations elsewhere and scales out new execution environments to handle the load. To identify which resource constraint is causing throttles, monitor the throttle reason metrics (`ConcurrencyThrottles`, `CPUThrottles`, `MemoryThrottles`, and `DiskThrottles`) described in [Types of metrics for Lambda functions](monitoring-metrics-types.md).

#### 3. Execution environments per function
<a name="lambda-managed-instances-execution-environments-per-function"></a>

Set the minimum and maximum number of execution environments for your function.

**Default behavior:** The default minimum is 3 execution environments across Availability Zones, with no default maximum. You can override both values after the function is created.

**Adjustment guidelines:**
+ **Set the minimum:** Provision capacity for baseline traffic and reduce throttles during sudden bursts. Values below 3 reduce Availability Zone redundancy.
+ **Set the maximum:** Cap the number of execution environments to control scale-out and prevent noisy neighbor issues when multiple functions share a Capacity Provider.
+ **Deactivate the function:** Set both minimum and maximum to 0 to deactivate a function without deleting it.

**Example:**

```
aws lambda put-function-scaling-config \
  --function-name my-lmi-function \
  --qualifier '$LATEST.PUBLISHED' \
  --function-scaling-config MinExecutionEnvironments=5,MaxExecutionEnvironments=20 \
  --region us-east-1
```

**Important notes:**
+ **Qualifier scope:** These configurations apply at the function level for each qualified ARN. When set on `$LATEST.PUBLISHED`, the configuration propagates to future `$LATEST.PUBLISHED` versions. When set on a specific version, newly published versions revert to the default values.
+ **Paired configuration:** You must set both the minimum and maximum values together. Any unspecified setting reverts to its default value. Valid values for both `MinExecutionEnvironments` and `MaxExecutionEnvironments` range from 0 to 15000. A minimum of 0 is only valid when the maximum is also 0.
+ **Cost implication:** Function deactivation takes effect at the function-version level. Lambda terminates an underlying EC2 instance once it has no active execution environments, and instance charges continue until termination completes (typically within a few minutes).

### Capacity provider level controls
<a name="lambda-managed-instances-capacity-provider-level-controls"></a>

#### 4. Target resource utilization
<a name="lambda-managed-instances-target-resource-utilization"></a>

Choose your own target for CPU utilization consumption.

**Default behavior:** Lambda maintains enough headroom for your traffic to double within 5 minutes without throttles.

**Optimization options:**
+ If your workload is very steady or if your application is not sensitive to throttles, you may set the target to a high level to achieve higher utilization and lower costs
+ If you want to maintain headroom for bursts of traffic, you can set resource targets to a low level, which will require more capacity

#### 5. Instance type selection
<a name="lambda-managed-instances-instance-type-selection"></a>

Set allowed or excluded instance types.

**Default behavior:** Lambda chooses the best instance types for your workload. Letting Lambda Managed Instances choose instance types is recommended, as restricting the number of possible instance types may result in lower availability.

**Custom configuration:**
+ **Specific hardware requirements:** Set allowed instance types to a list of compatible instances. For example, if you have an application that requires high network bandwidth, you can select several n instance types
+ **Cost optimization:** For testing or development environments, you might choose smaller instance types, like m7a.large instance types

## Scheduled scaling
<a name="lambda-managed-instances-scheduled-scaling"></a>

Use [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html) to adjust your function's minimum and maximum execution environments on a recurring or one-time schedule. This is useful for predictable traffic patterns, such as scaling up before peak hours and scaling down during off-peak hours.

**Scheduler configuration:**
+ Create an EventBridge Scheduler execution role or use an existing role that grants permission to call `lambda:PutFunctionScalingConfig` on your target function.
+ Create a schedule using a cron or rate expression, targeting the `PutFunctionScalingConfig` API as a universal target. Specify the new `MinExecutionEnvironments` and `MaxExecutionEnvironments` values in the Input payload.

**Example 1: Scale to handle planned peak traffic**

Create two schedules to scale up before peak hours and scale down afterward. Each schedule targets the `PutFunctionScalingConfig` API with updated `MinExecutionEnvironments` and `MaxExecutionEnvironments` values.

Scale up at 8:00 AM UTC (min=100, max=1000):

```
aws scheduler create-schedule \
  --name "ScaleUpLambdaManagedInstances" \
  --schedule-expression "cron(0 8 * * ? *)" \
  --flexible-time-window '{"Mode": "OFF"}' \
  --target '{
    "Arn": "arn:aws:scheduler:::aws-sdk:lambda:PutFunctionScalingConfig",
    "RoleArn": "arn:aws:iam::<account-id>:role/eventbridge-scheduler-role",
    "Input": "{\"FunctionName\": \"my-lmi-function\", \"Qualifier\": \"$LATEST.PUBLISHED\", \"FunctionScalingConfig\": {\"MinExecutionEnvironments\": 100, \"MaxExecutionEnvironments\": 1000}}"
  }'
```

Scale down at 6:00 PM UTC (min=5, max=20):

```
aws scheduler create-schedule \
  --name "ScaleDownLambdaManagedInstances" \
  --schedule-expression "cron(0 18 * * ? *)" \
  --flexible-time-window '{"Mode": "OFF"}' \
  --target '{
    "Arn": "arn:aws:scheduler:::aws-sdk:lambda:PutFunctionScalingConfig",
    "RoleArn": "arn:aws:iam::<account-id>:role/eventbridge-scheduler-role",
    "Input": "{\"FunctionName\": \"my-lmi-function\", \"Qualifier\": \"$LATEST.PUBLISHED\", \"FunctionScalingConfig\": {\"MinExecutionEnvironments\": 5, \"MaxExecutionEnvironments\": 20}}"
  }'
```

**Example 2: Deactivate during off-peak hours and reactivate**

Setting both `MinExecutionEnvironments` and `MaxExecutionEnvironments` to 0 deactivates the function version without deleting it. A deactivated function does not automatically scale back up with traffic. You must explicitly reactivate it by setting non-zero values through another scheduled action.

Deactivate at 10:00 PM UTC (min=0, max=0):

```
aws scheduler create-schedule \
  --name "DeactivateLambdaManagedInstances" \
  --schedule-expression "cron(0 22 * * ? *)" \
  --flexible-time-window '{"Mode": "OFF"}' \
  --target '{
    "Arn": "arn:aws:scheduler:::aws-sdk:lambda:PutFunctionScalingConfig",
    "RoleArn": "arn:aws:iam::<account-id>:role/eventbridge-scheduler-role",
    "Input": "{\"FunctionName\": \"my-lmi-function\", \"Qualifier\": \"$LATEST.PUBLISHED\", \"FunctionScalingConfig\": {\"MinExecutionEnvironments\": 0, \"MaxExecutionEnvironments\": 0}}"
  }'
```

Reactivate at 7:00 AM UTC (min=10, max=20):

```
aws scheduler create-schedule \
  --name "ReactivateLambdaManagedInstances" \
  --schedule-expression "cron(0 7 * * ? *)" \
  --flexible-time-window '{"Mode": "OFF"}' \
  --target '{
    "Arn": "arn:aws:scheduler:::aws-sdk:lambda:PutFunctionScalingConfig",
    "RoleArn": "arn:aws:iam::<account-id>:role/eventbridge-scheduler-role",
    "Input": "{\"FunctionName\": \"my-lmi-function\", \"Qualifier\": \"$LATEST.PUBLISHED\", \"FunctionScalingConfig\": {\"MinExecutionEnvironments\": 10, \"MaxExecutionEnvironments\": 20}}"
  }'
```

**Adjustment guidelines:**
+ For workloads with predictable peaks, create multiple schedules to match your traffic pattern: one to scale up your function before peak hours, and another to scale down after peak hours. Each schedule follows the same pattern with updated `MinExecutionEnvironments` and `MaxExecutionEnvironments` values.
+ Scheduled scaling adjusts the provisioned floor and ceiling of execution environments, but actual scaling between min and max still responds to CPU utilization and concurrency saturation.
+ If your traffic more than doubles within 5 minutes of a scheduled scale-up, you might still experience throttles as capacity is provisioned.
+ When scaling to zero to deactivate a function, remember that reactivation requires an explicit `PutFunctionScalingConfig` call with non-zero values.

## Next steps
<a name="lambda-managed-instances-scaling-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Review runtime-specific guides for handling multi-concurrency
+ Configure [VPC connectivity for your capacity providers](lambda-managed-instances-networking.md)
+ Monitor scaling metrics to optimize scaling behavior