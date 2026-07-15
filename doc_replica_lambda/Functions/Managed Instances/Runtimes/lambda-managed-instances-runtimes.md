

# Lambda Managed Instances runtimes
<a name="lambda-managed-instances-runtimes"></a>

Lambda processes requests differently when using Lambda Managed Instances. Instead of handling requests sequentially in each execution environment, Lambda Managed Instances process multiple requests concurrently within each execution environment. This change in execution model means that functions using Lambda Managed Instances need to consider thread safety, state management, and context isolation, concerns which do not arise in the Lambda (default) single-concurrency model. In addition, the multi-concurrency implementation varies between runtimes.

## Supported languages
<a name="lambda-managed-instances-supported-runtimes"></a>

Lambda Managed Instances can be used with the following programming languages and runtimes:
+ **Java:** Java 21 and later.
+ **Python:** Python 3.13 and later.
+ **Node.js:** Node.js 22 and later.
+ **.NET:** .NET 8 and later.
+ **Rust:** Supported using the OS-only runtime `provided.al2023` and later.

## Language-specific considerations
<a name="lambda-managed-instances-runtime-considerations"></a>

Each programming language implements multi-concurrency differently. You need to understand how multi-concurrency is implemented in your chosen programming language to apply the appropriate concurrency best practices.

**Java**

Uses a single process with OS threads for concurrency. Multiple threads execute the handler method simultaneously, requiring thread-safe handling of state and shared resources.

**Python**

Uses multiple Python processes where each concurrent request runs in a separate process. This protects against most concurrency issues, though care is required for shared resources such as the `/tmp` directory.

**Node.js**

Uses [worker threads](https://nodejs.org/api/worker_threads.html) with asynchronous execution. Concurrent requests are distributed across worker threads, and each worker thread can also handle concurrent requests asynchronously, requiring safe handling of state and shared resources.

**.NET**

Uses .NET Tasks with asynchronous processing of multiple concurrent requests. Requires safe handling of state and shared resources.

**Rust**

Uses a single process with async tasks powered by [Tokio](https://tokio.rs/). The handler must be `Clone` \+ `Send`.

## Next steps
<a name="lambda-managed-instances-runtime-next-steps"></a>

For detailed information about each runtime, see the following topics:
+ [Java runtime for Lambda Managed Instances](lambda-managed-instances-java-runtime.md)
+ [Node.js runtime for Lambda Managed Instances](lambda-managed-instances-nodejs-runtime.md)
+ [Python runtime for Lambda Managed Instances](lambda-managed-instances-python-runtime.md)
+ [.NET runtime for Lambda Managed Instances](lambda-managed-instances-dotnet-runtime.md)
+ [Rust support for Lambda Managed Instances](lambda-managed-instances-rust.md)