

# Troubleshooting Lambda Managed Instances
<a name="lambda-managed-instances-troubleshooting"></a>

## Throttling and scaling issues
<a name="lambda-managed-instances-ts-throttling"></a>

### High error rates during scale-up
<a name="lambda-managed-instances-ts-high-error-rates"></a>

**Problem:** You experience throttling errors (HTTP 429) when traffic increases rapidly.

**Cause:** Lambda Managed Instances scale asynchronously based on CPU resource utilization and multi-concurrency saturation. If your traffic more than doubles within 5 minutes, you may see throttles as Lambda scales up instances and execution environments to meet demand.

**Solution:**
+ **Adjust target resource utilization:** If your workload has predictable traffic patterns, set a lower target resource utilization to maintain additional headroom for traffic bursts.
+ **Pre-warm capacity:** For planned traffic increases, gradually ramp up traffic over a longer period to allow scaling to keep pace.
+ **Monitor scaling metrics:** Track throttle error metrics to understand the reason for throttles and capacity scaling issues.
+ **Review function configuration:** Ensure your function memory and vCPU settings support multi-concurrent executions. Increase function memory or vCPU allocation if needed.

### Slow scale-down
<a name="lambda-managed-instances-ts-slow-scale-down"></a>

**Problem:** Instances take a long time to scale down after traffic decreases.

**Cause:** Lambda Managed Instances scale down gradually to maintain availability and avoid rapid capacity changes that could impact performance.

**Solution:**

This is expected behavior. Lambda scales down instances conservatively to ensure stability. Monitor your CloudWatch metrics to track the number of running instances.

## Concurrency issues
<a name="lambda-managed-instances-ts-concurrency"></a>

### Execution environments with low concurrency experience throttles
<a name="lambda-managed-instances-ts-low-concurrency-throttles"></a>

**Problem:** Your functions experience throttling despite having available capacity.

**Cause:** Execution environments with very low maximum concurrency may have difficulty scaling effectively. Lambda Managed Instances are designed for multi-concurrent applications.

**Solution:**
+ **Increase maximum concurrency:** If your function invocations use very little CPU, increase the maximum concurrency setting up to 64 per vCPU.
+ **Optimize function code:** Review your function code to reduce CPU consumption per invocation, allowing higher concurrency.
+ **Adjust function memory and vCPU:** Ensure your function has sufficient resources to handle multiple concurrent invocations.

### Thread safety issues (Java runtime)
<a name="lambda-managed-instances-ts-thread-safety-java"></a>

**Problem:** Your Java function produces incorrect results or experiences race conditions under load.

**Cause:** Multiple threads execute the handler method simultaneously, and shared state is not thread-safe.

**Solution:**
+ Use `AtomicInteger` or `AtomicLong` for counters instead of primitive types
+ Replace `HashMap` with `ConcurrentHashMap`
+ Use `Collections.synchronizedList()` to wrap `ArrayList`
+ Use `ThreadLocal` for request-specific state
+ Access trace IDs from the Lambda Context object, not environment variables

For detailed guidance, see the [Java runtime for Lambda Managed Instances](lambda-managed-instances-java-runtime.md) documentation.

### State isolation issues (Node.js runtime)
<a name="lambda-managed-instances-ts-state-isolation-nodejs"></a>

**Problem:** Your Node.js function returns data from different requests or experiences data corruption.

**Cause:** Global variables are shared across concurrent invocations on the same worker thread. When async operations yield control, other invocations can modify shared state.

**Solution:**
+ Install and use `@aws/lambda-invoke-store` for all request-specific state
+ Replace global variables with `InvokeStore.set()` and `InvokeStore.get()`
+ Use unique file names in `/tmp` with request IDs
+ Access trace IDs using `InvokeStore.getXRayTraceId()` instead of environment variables

For detailed guidance, see the [Node.js runtime for Lambda Managed Instances](lambda-managed-instances-nodejs-runtime.md) documentation.

### File conflicts (Python runtime)
<a name="lambda-managed-instances-ts-file-conflicts-python"></a>

**Problem:** Your Python function reads incorrect data from files in `/tmp`.

**Cause:** Multiple processes share the `/tmp` directory. Concurrent writes to the same file can cause data corruption.

**Solution:**
+ Use unique file names with request IDs: `/tmp/request_{context.request_id}.txt`
+ Use file locking with `fcntl.flock()` for shared files
+ Clean up temporary files with `os.remove()` after use

For detailed guidance, see the [Python runtime for Lambda Managed Instances](lambda-managed-instances-python-runtime.md) documentation.

## Performance issues
<a name="lambda-managed-instances-ts-performance"></a>

### High memory utilization
<a name="lambda-managed-instances-ts-high-memory"></a>

**Problem:** Your functions experience high memory utilization or out-of-memory errors.

**Cause:** Each concurrent request in Python runs in a separate process with its own memory space. Total memory usage equals per-process memory multiplied by concurrent processes.

**Solution:**
+ Monitor the `MemoryUtilization` metric in CloudWatch
+ Reduce the `MaxConcurrency` setting if memory usage approaches the function's memory limit
+ Increase function memory allocation to support higher concurrency
+ Optimize memory usage by loading data on-demand instead of during initialization

### Inconsistent performance
<a name="lambda-managed-instances-ts-inconsistent-performance"></a>

**Problem:** Function performance varies significantly between invocations.

**Cause:** Lambda may select different instance types based on availability, or functions may be running on instances with varying resource availability.

**Solution:**
+ **Specify allowed instance types:** If you have specific performance requirements, configure allowed instance types in your capacity provider to limit the instance types Lambda can select.
+ **Monitor instance-level metrics:** Track `CPUUtilization` and `MemoryUtilization` at the capacity provider level to identify resource constraints.
+ **Review capacity metrics:** Check `vCPUAvailable` and `MemoryAvailable` to ensure sufficient resources are available on your instances.

## Capacity provider issues
<a name="lambda-managed-instances-ts-capacity-provider"></a>

### Function version fails to become ACTIVE
<a name="lambda-managed-instances-ts-function-not-active"></a>

**Problem:** Your function version remains in a pending state after publishing.

**Cause:** Lambda is launching Managed Instances and starting execution environments. This process takes time, especially for the first function version on a new capacity provider.

**Solution:**

Wait for Lambda to complete the initialization process. Lambda launches three instances by default for AZ resiliency and starts three execution environments before marking your function version ACTIVE. This typically takes several minutes.

### Cannot delete capacity provider
<a name="lambda-managed-instances-ts-cannot-delete"></a>

**Problem:** You receive an error when attempting to delete a capacity provider.

**Cause:** You cannot delete a capacity provider that has function versions attached to it.

**Solution:**

1. Identify all function versions using the capacity provider with the `ListFunctionVersionsByCapacityProvider` API.

1. Delete or update those function versions to remove the capacity provider association.

1. Retry deleting the capacity provider.

### Generic error messages during function publishing
<a name="lambda-managed-instances-ts-generic-errors"></a>

**Problem:** You encounter generic error messages such as "Internal error occurred during publishing" when publishing functions.

**Solution:**
+ **Check IAM permissions:** Ensure you have the `lambda:PassCapacityProvider` permission for the capacity provider you're trying to use.
+ **Verify capacity provider configuration:** Confirm that your capacity provider is in the ACTIVE state using the `GetCapacityProvider` API.
+ **Review VPC configuration:** Ensure the subnets and security groups specified in your capacity provider are correctly configured and accessible.
+ **Check AWS CloudTrail logs:** Review CloudTrail logs for detailed error information about the failed operation.

## Monitoring and observability issues
<a name="lambda-managed-instances-ts-monitoring"></a>

### Missing CloudWatch metrics
<a name="lambda-managed-instances-ts-missing-metrics"></a>

**Problem:** You don't see expected metrics in CloudWatch for your capacity provider or functions.

**Cause:** Metrics are published at 5-minute intervals. New capacity providers or functions may not have metrics available immediately.

**Solution:**

Wait at least 5-10 minutes after publishing a function version before expecting metrics to appear in CloudWatch. Verify you're looking at the correct namespace (`AWS/Lambda`) and dimensions (`CapacityProviderName`, `FunctionName`, or `InstanceType`).

### Cannot find CloudWatch logs
<a name="lambda-managed-instances-ts-no-logs"></a>

**Problem:** Your function executes successfully, but you cannot find logs in CloudWatch Logs.

**Cause:** Lambda Managed Instances run in your VPC and require network connectivity to send logs to CloudWatch Logs. Without proper VPC connectivity configuration, your functions cannot reach the CloudWatch Logs service endpoint.

**Solution:**

Configure VPC connectivity to enable your functions to send logs to CloudWatch Logs. You have three options:

**Option 1: VPC endpoint for CloudWatch Logs (recommended for production)**

1. Open the Amazon VPC console at [console.aws.amazon.com/vpc/](http://console.aws.amazon.com/vpc/).

1. In the navigation pane, choose **Endpoints**.

1. Choose **Create endpoint**.

1. For **Service category**, choose **AWS services**.

1. For **Service name**, select `com.amazonaws.region.logs` (replace `region` with your AWS Region).

1. For **VPC**, select the VPC used by your capacity provider.

1. For **Subnets**, select the subnets where you want to create endpoint network interfaces. For high availability, select subnets in multiple Availability Zones.

1. For **Security groups**, select security groups that allow inbound HTTPS traffic (port 443) from your function's security group.

1. Enable **Private DNS** for the endpoint.

1. Choose **Create endpoint**.

**Option 2: Public subnet with internet gateway**

If your capacity provider uses public subnets, ensure:

1. An internet gateway is attached to your VPC

1. The route table routes `0.0.0.0/0` traffic to the internet gateway

1. Security groups allow outbound HTTPS traffic on port 443

**Option 3: Private subnet with NAT gateway**

If your capacity provider uses private subnets, ensure:

1. A NAT gateway exists in a public subnet

1. The private subnet route table routes `0.0.0.0/0` traffic to the NAT gateway

1. The public subnet route table routes `0.0.0.0/0` traffic to an internet gateway

1. Security groups allow outbound HTTPS traffic on port 443

For detailed guidance on VPC connectivity options, see [VPC connectivity for Lambda Managed Instances](lambda-managed-instances-networking.md).

### Difficulty correlating logs from concurrent requests
<a name="lambda-managed-instances-ts-log-correlation"></a>

**Problem:** Logs from different requests are interleaved, making it difficult to trace individual requests.

**Cause:** Log interleaving is expected and standard behavior in multi-concurrent systems.

**Solution:**
+ **Use structured logging with JSON format:** Include request ID in all log statements
+ **Java:** Use Log4j with `ThreadContext` to automatically include request ID
+ **Node.js:** Use `console.log()` with JSON formatting and include `InvokeStore.getRequestId()`
+ **Python:** Use the standard logging module with JSON formatting and include `context.request_id`

For detailed guidance, see the runtime-specific documentation pages.

## Getting additional help
<a name="lambda-managed-instances-ts-getting-help"></a>

If you continue to experience issues after trying these solutions:

1. **Review CloudWatch metrics:** Check capacity provider and execution environment metrics to identify resource constraints or scaling issues.

1. **Check AWS CloudTrail logs:** Review CloudTrail logs for detailed information about API calls and errors.

1. **Contact AWS Support:** If you cannot resolve the issue, contact AWS Support with details about your capacity provider configuration, function configuration, and the specific error messages you're encountering.

## Next steps
<a name="lambda-managed-instances-ts-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)
+ Monitor Lambda Managed Instances with [CloudWatch metrics](lambda-managed-instances-monitoring.md)
+ Review [best practices for Lambda Managed Instances](lambda-managed-instances-best-practices.md)