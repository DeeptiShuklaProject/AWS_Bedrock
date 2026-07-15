

# Python runtime for Lambda Managed Instances
<a name="lambda-managed-instances-python-runtime"></a>

The Lambda runtime uses multiple Python processes to handle concurrent requests. Each concurrent request runs in a separate process with its own memory space and initialization. Each process handles one request at a time, synchronously. Processes don't share memory directly, so global variables, module-level caches, and singleton objects are isolated between concurrent requests.

## Concurrency configuration
<a name="lambda-managed-instances-python-concurrency-config"></a>

The maximum number of concurrent requests which Lambda sends to each execution environment is controlled by the `PerExecutionEnvironmentMaxConcurrency` setting in the function configuration. This is an optional setting, and the default value varies depending on the runtime. For Python runtimes, the default is 16 concurrent requests per vCPU, or you can configure your own value. This value also determines the number of processes used by the Python runtime. Lambda automatically adjusts the number of concurrent requests up to the configured maximum based on the capacity of each execution environment to absorb those requests.

**Important**  
Using process-based concurrency means each runtime worker process performs its own initialization. Total memory usage equals the per-process memory multiplied by the number of concurrent processes. If you are loading large libraries or data sets and have high concurrency, you will have a large memory footprint. According to your workload, you may need to tune your CPU-to-memory ratio or use a lower concurrency setting to avoid exceeding the available memory. You can use the `MemoryUtilization` metric in CloudWatch to track memory consumption.

## Building functions for multi-concurrency
<a name="lambda-managed-instances-python-building"></a>

Due to the process-based multi-concurrency model, Lambda Managed Instances functions using Python runtimes do not access in-memory resources concurrently from multiple invokes. You do not need to apply coding practices for in-memory concurrency safety.

## Shared /tmp directory
<a name="lambda-managed-instances-python-shared-tmp"></a>

The `/tmp` directory is shared across all concurrent requests in the execution environment. Concurrent writes to the same file can cause data corruption, for example if another process overwrites the file. To address this, either implement file locking for shared files or use unique file names per process or per request to avoid conflicts. Remember to clean up unneeded files to avoid exhausting the available space.

## Logging
<a name="lambda-managed-instances-python-logging"></a>

Log interleaving (log entries from different requests being interleaved in logs) is normal in multi-concurrent systems.

Functions using Lambda Managed Instances always use the structured JSON log format introduced with [advanced logging controls](monitoring-logs.md#monitoring-cloudwatchlogs-advanced). This format includes the `requestId`, allowing log entries to be correlated to a single request. When you use the `logging` module from the Python standard library in Lambda, the `requestId` is automatically included in each log entry. For further information, see [Using Lambda advanced logging controls with Python](https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-advanced).

## Request context
<a name="lambda-managed-instances-python-request-context"></a>

Use `context.aws_request_id` to access to the request ID for the current request.

With Python runtimes, you can use the `_X_AMZN_TRACE_ID` environment variable to access the X-Ray trace ID with Lambda Managed Instances. The X-Ray trace ID is propagated automatically when using the AWS SDK.

Use `context.get_remaining_time_in_millis()` to detect timeouts. See [Error handling and recovery](lambda-managed-instances-execution-environment.md#lambda-managed-instances-error-handling) for more information.

**Example: Timeout handling**

Check remaining time before each unit of work and stop processing before the timeout fires. Configure `BUFFER_MS` based on the expected duration of your next chunk of work.

```
BUFFER_MS = 2000  # Configure based on your next chunk of work

def handler(event, context):
    for item in event["items"]:
        if context.get_remaining_time_in_millis() < BUFFER_MS:
            return {"statusCode": 206, "body": "Timeout approaching, stopping early"}
        process_item(item)
    return {"statusCode": 200, "body": "Done"}
```

**Example: Propagating deadlines to downstream calls**

When making calls to downstream services, propagate the remaining time as a timeout to avoid hanging on network calls that would outlive your invocation. The boto3 SDK does not support per-request timeouts on an existing client, so you must create a client with the desired timeout. For high-throughput functions, evaluate whether a fixed timeout configured at initialization is more appropriate than per-request client creation.

```
import boto3
from botocore.config import Config

def handler(event, context):
    remaining = context.get_remaining_time_in_millis() / 1000
    timeout = max(1, remaining - 0.5)
    s3 = boto3.client("s3", config=Config(read_timeout=timeout, connect_timeout=timeout))
    response = s3.get_object(Bucket="my-bucket", Key="my-key")
    return {"statusCode": 200, "body": "Done"}
```

## Initialization and shutdown
<a name="lambda-managed-instances-python-init-shutdown"></a>

Function initialization occurs once per process. You may see repeat log entries if your function emits logs during initialization.

For Lambda functions with extensions, the execution environment emits a SIGTERM signal during shut down. This signal is used by extensions to trigger clean up tasks, such as flushing buffers. You can subscribe to SIGTERM events to trigger function clean-up tasks, such as closing database connections. To learn more about the execution environment lifecycle, see [Understanding the Lambda execution environment lifecycle](lambda-runtime-environment.md).

## Dependency versions
<a name="lambda-managed-instances-python-dependencies"></a>

Lambda Managed Instances requires the following minimum package versions:
+ Powertools for AWS Lambda (Python): version 3.23.0 or later

## Powertools for AWS Lambda (Python)
<a name="lambda-managed-instances-python-powertools"></a>

Powertools for AWS Lambda (Python) is compatible with Lambda Managed Instances and provides utilities for logging, tracing, metrics, and more. For more information, see [Powertools for AWS Lambda (Python)](https://github.com/aws-powertools/powertools-lambda-python).

## Next steps
<a name="lambda-managed-instances-python-next-steps"></a>
+ Review [Java runtime for Lambda Managed Instances](lambda-managed-instances-java-runtime.md)
+ Review [Node.js runtime for Lambda Managed Instances](lambda-managed-instances-nodejs-runtime.md)
+ Review [.NET runtime for Lambda Managed Instances](lambda-managed-instances-dotnet-runtime.md)
+ Learn about [scaling Lambda Managed Instances](lambda-managed-instances-scaling.md)