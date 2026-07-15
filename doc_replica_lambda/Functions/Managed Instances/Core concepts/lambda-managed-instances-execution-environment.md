

# Understanding the Lambda Managed Instances execution environment
<a name="lambda-managed-instances-execution-environment"></a>

Lambda Managed Instances provide an alternative deployment model that runs your function code on customer-owned Amazon EC2 instances while Lambda manages the operational aspects. The execution environment for Managed Instances has several important differences from Lambda (default) functions, particularly in how it handles concurrent invocations and manages container lifecycles.

**Note:** For information about the Lambda (default) execution environment, see Understanding the Lambda execution environment lifecycle.

## Execution environment lifecycle
<a name="lambda-managed-instances-execution-lifecycle"></a>

The lifecycle of a Lambda Managed Instances function execution environment differs from Lambda (default) in several key ways:

### Init phase
<a name="lambda-managed-instances-init-phase"></a>

During the Init phase, Lambda performs the following steps:
+ Initialize and register all extensions
+ Bootstrap the runtime entrypoint. Runtime spawns the configured number of runtime workers (implementation depends on runtime)
+ Run function initialization code (code outside the handler)
+ Wait for at least one runtime worker to signal readiness by calling `/runtime/invocation/next`

The Init phase is considered complete when extensions have initialized and at least one runtime worker has called `/runtime/invocation/next`. The function is then ready to process invocations.

**Note**  
For Lambda Managed Instances functions, initialization can take up to 15 minutes. The timeout is the maximum of 130 seconds or the configured function timeout (up to 900 seconds).

### Invoke phase
<a name="lambda-managed-instances-invoke-phase"></a>

The Invoke phase for Lambda Managed Instances functions has several unique characteristics:

**Continuous operation.** Unlike Lambda (default), the execution environment remains continuously active, processing invocations as they arrive without freezing between invocations.

**Parallel processing.** Multiple invocations can execute simultaneously within the same execution environment, each handled by a different runtime worker.

**Independent timeouts.** The function's configured timeout applies to each individual invocation. When an invocation times out, Lambda marks that specific invocation as failed but does not interrupt other running invocations or terminate the execution environment.

**Backpressure handling.** If all runtime workers are busy processing invocations, new invocation requests are rejected until a worker becomes available.

## Error handling and recovery
<a name="lambda-managed-instances-error-handling"></a>

Error handling in Lambda Managed Instances function execution environments differs from Lambda (default):

**Runtime worker failures.** If a runtime worker process crashes, the execution environment continues operating with the remaining healthy workers.

**Extension crashes.** If an extension process crashes during initialization or operation, the entire execution environment is marked as unhealthy and is terminated. Lambda creates a new execution environment to replace it.

**No reset/repair.** Unlike Lambda (default), Managed Instances do not attempt to reset and reinitialize the execution environment after errors. Instead, unhealthy containers are terminated and replaced with new ones.

### Invoke timeouts
<a name="lambda-managed-instances-invoke-timeouts"></a>

When an individual invocation times out, Lambda returns a `Task timed out after <timeout> seconds` error with a status of function error to the caller. However, Lambda Managed Instances does not forcibly terminate your code—it continues running in the execution environment. As a function developer, you are responsible for detecting and handling the timeout. The context object exposes the remaining time for the invocation. A zero or negative value indicates the invocation has timed out. Other concurrent invocations in the execution environment continue processing normally.

#### Retry behavior
<a name="lambda-managed-instances-timeout-retry-behavior"></a>

When an invocation times out:
+ **Synchronous invocations:** The caller receives the timeout error and is responsible for retrying.
+ **Asynchronous invocations:** Lambda retries based on your function's retry policy (default: 2 retries). After all retries are exhausted, the event is sent to the configured dead-letter queue or on-failure destination, if any.
+ **Event source mappings:** Retry behavior depends on the event source configuration (for example, batch size, bisect on error, maximum retry attempts). The batch may be retried or sent to an on-failure destination based on your retry policies.

#### What happens if you don't handle the timeout
<a name="lambda-managed-instances-timeout-consequences"></a>

If your code does not check the remaining time and stop execution:
+ **The invocation is already marked as failed.** Lambda has already returned a timeout error to the caller—any work your code completes after the timeout is effectively lost from the caller's perspective.
+ **Resources remain consumed.** Your code continues occupying a runtime worker slot, reducing the concurrency available for new invocations on that instance.
+ **Nondeterministic behavior.** Your code does not stop when the timeout fires—it keeps running in the background. This means side effects can still happen after Lambda has already told the caller the invocation failed. For example, your handler writes a record to DynamoDB, then the timeout fires and Lambda returns a timeout error to the caller, but your code is still running and proceeds to send an SNS notification. The caller retries the invocation, which writes the record again and sends the notification again. You now have duplicate data and duplicate notifications—and no easy way to tell which ones came from the "failed" invocation that was still running in the background.

#### Handling timeouts in your code
<a name="lambda-managed-instances-timeout-handling"></a>

Use the context object to check remaining time and stop processing before the timeout. Configure a buffer based on the expected duration of your next unit of work—for example, if each item takes approximately 500 ms to process, set the buffer to at least 500 ms plus margin.

For language-specific examples of timeout handling, see the request context section of each runtime page:
+ [Node.js request context](lambda-managed-instances-nodejs-runtime.md#lambda-managed-instances-nodejs-request-context)
+ [Python request context](lambda-managed-instances-python-runtime.md#lambda-managed-instances-python-request-context)
+ [Java request context](lambda-managed-instances-java-runtime.md#lambda-managed-instances-java-request-context)
+ [.NET request context](lambda-managed-instances-dotnet-runtime.md#lambda-managed-instances-dotnet-request-context)