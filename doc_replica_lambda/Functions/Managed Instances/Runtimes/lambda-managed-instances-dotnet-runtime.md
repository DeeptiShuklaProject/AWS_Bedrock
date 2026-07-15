

# .NET runtime for Lambda Managed Instances
<a name="lambda-managed-instances-dotnet-runtime"></a>

For .NET runtimes, Lambda Managed Instances use a single .NET process per execution environment. Multiple concurrent requests are processed using .NET Tasks.

## Concurrency configuration
<a name="lambda-managed-instances-dotnet-concurrency-config"></a>

The maximum number of concurrent requests which Lambda sends to each execution environment is controlled by the `PerExecutionEnvironmentMaxConcurrency` setting in the function configuration. This is an optional setting, and the default value varies depending on the runtime. For .NET runtimes, the default is 32 concurrent requests per vCPU, or you can configure your own value. Lambda automatically adjusts the number of concurrent requests up to the configured maximum based on the capacity of each execution environment to absorb those requests.

## Building functions for multi-concurrency
<a name="lambda-managed-instances-dotnet-building"></a>

You should apply the same concurrency safety practices when using Lambda Managed Instances as you would in any other multi-concurrent environment. Since the handler object is shared across all Tasks any mutable state must be thread-safe. This includes collections, database connections and any static objects that are modified during request processing.

AWS SDK clients are thread safe and do not require special handling.

**Example: Database connection pools**

The following code uses a static database connection object which is shared between concurrent requests. The `SqlConnection` object is not thread safe.

```
public class DBQueryHandler
{
    // Single connection shared across threads - NOT SAFE
    private SqlConnection connection;

    public DBQueryHandler()
    {
        connection = new SqlConnection("your-connection-string-here");
        connection.Open();
    }

    public string Handle(object input, ILambdaContext context)
    {
        using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT ..."; // your query

        using var reader = cmd.ExecuteReader();

        ...
    }
}
```

To address this, use a separate connection for each request, drawn from a connection pool. ADO.NET providers like `Microsoft.Data.SqlClient` automatically support connection pooling when the connection object is opened.

```
public class DBQueryHandler
{
    public DBQueryHandler()
    {
    }

    public string Handle(object input, ILambdaContext context)
    {
        using var connection = new SqlConnection("your-connection-string-here");
        connection.Open();
        using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT ..."; // your query

        using var reader = cmd.ExecuteReader();

        ...
    }
}
```

**Example: Collections**

Standard .NET collections are not thread safe:

```
public class Handler
{
    private static List<string> items = new List<string>();
    private static Dictionary<string, object> cache = new Dictionary<string, object>();

    public string FunctionHandler(object input, ILambdaContext context)
    {
        items.Add(context.AwsRequestId);
        cache["key"] = input;

        return "Success";
    }
}
```

Use collections from the `System.Collections.Concurrent` namespace for concurrency safety:

```
public class Handler
{
    private static ConcurrentBag<string> items = new ConcurrentBag<string>();
    private static ConcurrentDictionary<string, object> cache = new ConcurrentDictionary<string, object>();

    public string FunctionHandler(object input, ILambdaContext context)
    {
        items.Add(context.AwsRequestId);
        cache["key"] = input;

        return "Success";
    }
}
```

## Shared /tmp directory
<a name="lambda-managed-instances-dotnet-shared-tmp"></a>

The `/tmp` directory is shared across all concurrent requests in the execution environment. Concurrent writes to the same file can cause data corruption, for example if another request overwrites the file. To address this, either implement file locking for shared files or use unique file names per request to avoid conflicts. Remember to clean up unneeded files to avoid exhausting the available space.

## Logging
<a name="lambda-managed-instances-dotnet-logging"></a>

Log interleaving (log entries from different requests being interleaved in logs) is normal in multi-concurrent systems. Functions using Lambda Managed Instances always use the structured JSON log format introduced with [advanced logging controls](monitoring-logs.md#monitoring-cloudwatchlogs-advanced). This format includes the `requestId`, allowing log entries to be correlated to a single request. When you use the `context.Logger` object to generate logs, the `requestId` is automatically included in each log entry. For further information, see [Using Lambda advanced logging controls with .NET](csharp-logging.md#csharp-logging-advanced).

## Request context
<a name="lambda-managed-instances-dotnet-request-context"></a>

Use the `context.AwsRequestId` property to access to the request ID for the current request.

Use the `context.TraceId` property to access the X-Ray trace ID. This provides concurrency-safe access to the trace ID for the current request. Lambda does not support the `_X_AMZN_TRACE_ID` environment variable with Lambda Managed Instances. The X-Ray trace ID is propagated automatically when using the AWS SDK.

Use `ILambdaContext.RemainingTime` to detect timeouts. See [Error handling and recovery](lambda-managed-instances-execution-environment.md#lambda-managed-instances-error-handling) for more information.

**Example: Timeout handling**

Check remaining time before each unit of work and stop processing before the timeout fires. Configure the buffer based on the expected duration of your next chunk of work.

```
private static readonly TimeSpan Buffer = TimeSpan.FromMilliseconds(2000);

public APIGatewayProxyResponse FunctionHandler(APIGatewayProxyRequest request, ILambdaContext context)
{
    var items = JsonSerializer.Deserialize<List<string>>(request.Body);
    foreach (var item in items)
    {
        if (context.RemainingTime < Buffer)
            return new APIGatewayProxyResponse { StatusCode = 206, Body = "Timeout approaching, stopping early" };
        ProcessItem(item);
    }
    return new APIGatewayProxyResponse { StatusCode = 200, Body = "Done" };
}
```

**Example: Propagating deadlines to downstream calls**

When making calls to downstream services, propagate the remaining time as a timeout to avoid hanging on network calls that would outlive your invocation. Use a `CancellationToken` with a shared client rather than creating a new client per invocation:

```
using Amazon.S3;

private static readonly IAmazonS3 s3 = new AmazonS3Client();

public async Task<string> FunctionHandler(APIGatewayProxyRequest request, ILambdaContext context)
{
    var timeout = context.RemainingTime - TimeSpan.FromMilliseconds(500);
    if (timeout < TimeSpan.FromSeconds(1)) timeout = TimeSpan.FromSeconds(1);

    using var cts = new CancellationTokenSource(timeout);
    await s3.GetObjectAsync("my-bucket", "my-key", cts.Token);
    return "Done";
}
```

## Initialization and shutdown
<a name="lambda-managed-instances-dotnet-init-shutdown"></a>

Function initialization occurs once per execution environment. Objects created during initialization are shared across requests.

For Lambda functions with extensions, the execution environment emits a SIGTERM signal during shut down. This signal is used by extensions to trigger clean up tasks, such as flushing buffers. You can subscribe to SIGTERM events to trigger function clean-up tasks, such as closing database connections. To learn more about the execution environment lifecycle, see [Understanding the Lambda execution environment lifecycle](lambda-runtime-environment.md).

## Dependency versions
<a name="lambda-managed-instances-dotnet-dependencies"></a>

Lambda Managed Instances requires the following minimum package versions:
+ Amazon.Lambda.Core: version 2.7.1 or later
+ Amazon.Lambda.RuntimeSupport: version 1.14.1 or later
+ OpenTelemetry.Instrumentation.AWSLambda: version 1.14.0 or later
+ AWSXRayRecorder.Core: version 2.16.0 or later
+ AWSSDK.Core: version 4.0.0.32 or later

## Powertools for AWS Lambda (.NET)
<a name="lambda-managed-instances-dotnet-powertools"></a>

[Powertools for AWS Lambda (.NET)](https://docs.aws.amazon.com/powertools/dotnet/) and [AWS Distro for OpenTelemetry - Instrumentation for DotNet](https://github.com/aws-observability/aws-otel-dotnet-instrumentation) currently do not support Lambda Managed Instances.

## Next steps
<a name="lambda-managed-instances-dotnet-next-steps"></a>
+ Review [Java runtime for Lambda Managed Instances](lambda-managed-instances-java-runtime.md)
+ Review [Node.js runtime for Lambda Managed Instances](lambda-managed-instances-nodejs-runtime.md)
+ Review [Python runtime for Lambda Managed Instances](lambda-managed-instances-python-runtime.md)
+ Learn about [scaling Lambda Managed Instances](lambda-managed-instances-scaling.md)