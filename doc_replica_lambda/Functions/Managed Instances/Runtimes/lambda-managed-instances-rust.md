

# Rust support for Lambda Managed Instances
<a name="lambda-managed-instances-rust"></a>

## Concurrency configuration
<a name="lambda-managed-instances-rust-concurrency-config"></a>

The maximum number of concurrent requests which Lambda sends to each execution environment is controlled by the `PerExecutionEnvironmentMaxConcurrency` setting in the function configuration. This is an optional setting, and the default value for Rust is 8 concurrent requests per vCPU, or you can configure your own value. This value determines the number of Tokio tasks spawned by the runtime and is static for the lifetime of the execution environment. Each worker handles exactly one in-flight request at a time, with no multiplexing per worker. Lambda automatically adjusts the number of concurrent requests up to the configured maximum based on the capacity of each execution environment to absorb those requests.

## Building functions for multi-concurrency
<a name="lambda-managed-instances-rust-building"></a>

You should apply the same thread safety practices when using Lambda Managed Instances as you would in any other multi-threaded environment. Since the handler object is shared across all worker threads, any mutable state must be thread-safe. This includes collections, database connections, and any static objects that are modified during request processing.

To enable concurrent request handling, add the `concurrency-tokio` feature flag to your `Cargo.toml` file.

```
[dependencies]  
lambda_runtime = { version = "1", features = ["concurrency-tokio"] }
```

The `lambda_runtime::run_concurrent(…)` entry point must be called from within a Tokio runtime, typically provided by the `#[tokio::main]` attribute on your main function. Your handler closure must implement [https://doc.rust-lang.org/std/clone/trait.Clone.html](https://doc.rust-lang.org/std/clone/trait.Clone.html) \+ [https://doc.rust-lang.org/std/marker/trait.Send.html](https://doc.rust-lang.org/std/marker/trait.Send.html). This allows the framework to share your handler across multiple async tasks safely. If those bounds are not met, your code will not compile.

When you need shared state across invocations (a database pool, a config struct), wrap it in [https://doc.rust-lang.org/std/sync/struct.Arc.html](https://doc.rust-lang.org/std/sync/struct.Arc.html) and clone the `Arc` into each invocation.

All AWS SDK for Rust clients are concurrency-safe and require no special handling.

### Example: AWS SDK client
<a name="lambda-managed-instances-rust-example-sdk"></a>

The following example uses an S3 client to upload an object on each invocation. The client is cloned directly into the closure without `Arc`:

```
let config = aws_config::load_defaults(BehaviorVersion::latest()).await;  
let s3_client = aws_sdk_s3::Client::new(&config);  
  
run_concurrent(service_fn(move |event: LambdaEvent<Request>| {  
    let s3_client = s3_client.clone(); // cheap clone, no Arc needed  
    async move {  
        s3_client.put_object()  
            .bucket(&event.payload.bucket)  
            .key(&event.payload.key)  
            .body(event.payload.body.into_bytes().into())  
            .send()  
            .await?;  
        Ok(Response { message: "uploaded".into() })  
    }  
}))  
.await
```

### Example: Database connection pools
<a name="lambda-managed-instances-rust-example-db"></a>

When your handler needs access to shared state such as a client and configuration, wrap it in [https://doc.rust-lang.org/std/sync/struct.Arc.html](https://doc.rust-lang.org/std/sync/struct.Arc.html) and clone the `Arc` into each invocation:

```
#[derive(Debug)]  
struct AppState {  
    dynamodb_client: DynamoDbClient,  
    table_name: String,  
    cache_ttl: Duration,  
}  
  
let config = aws_config::load_defaults(BehaviorVersion::latest()).await;  
let state = Arc::new(AppState {  
    dynamodb_client: DynamoDbClient::new(&config),  
    table_name: std::env::var("TABLE_NAME").expect("TABLE_NAME must be set"),  
    cache_ttl: Duration::from_secs(300),  
});  
  
run_concurrent(service_fn(move |event: LambdaEvent<Request>| {  
    let state = state.clone();  
    async move { handle(event, state).await }  
}))  
.await
```

## Shared /tmp directory
<a name="lambda-managed-instances-rust-tmp"></a>

The `/tmp` directory is shared across all concurrent invocations in the same execution environment. Use unique file names per invocation (e.g. include the request ID) or implement explicit file locking to avoid data corruption.

## Logging
<a name="lambda-managed-instances-rust-logging"></a>

Log interleaving (log entries from different requests being interleaved in logs) is normal in multi-concurrent systems. Functions using Lambda Managed Instances support structured JSON log format via Lambda's [advanced logging controls](monitoring-logs.md#monitoring-cloudwatchlogs-advanced). This format includes the `requestId`, allowing log entries to be correlated to a single request. For further information, see [Implementing advanced logging with the Tracing crate](rust-logging.md#rust-logging-tracing).

## Request Context
<a name="lambda-managed-instances-rust-context"></a>

The `Context` object is passed directly to each handler invocation. Use `event.context.request_id` to access the request ID for the current request.

Use `event.context.xray_trace_id` to access the X-Ray trace ID. Lambda does not support the `_X_AMZN_TRACE_ID` environment variable with Lambda Managed Instances. The X-Ray trace ID is propagated automatically when using the AWS SDK for Rust.

Use `event.context.deadline` to detect timeouts — it contains the invocation deadline in milliseconds.

## Initialization and shutdown
<a name="lambda-managed-instances-rust-lifecycle"></a>

Function initialization occurs once per execution environment. Objects created during initialization are shared across requests.

For Lambda functions with extensions, the execution environment emits a SIGTERM signal during shut down. This signal is used by extensions to trigger clean up tasks, such as flushing buffers. `lambda_runtime` offers a helper to simplify configuring graceful shutdown signal handling, [https://docs.rs/lambda_runtime/latest/lambda_runtime/fn.spawn_graceful_shutdown_handler.html](https://docs.rs/lambda_runtime/latest/lambda_runtime/fn.spawn_graceful_shutdown_handler.html). To learn more about the execution environment lifecycle, see [Understanding the Lambda execution environment lifecycle](lambda-runtime-environment.md).

## Dependency versions
<a name="lambda-managed-instances-rust-dependencies"></a>

Lambda Managed Instances requires the following minimum package version:
+ `lambda_runtime`: version 1.1.1 or later, with the `concurrency-tokio` feature enabled
+ The minimum supported Rust version (MSRV) is 1.84.0.