

# Best practices for Lambda Managed Instances
<a name="lambda-managed-instances-best-practices"></a>

## Capacity provider configuration
<a name="lambda-managed-instances-bp-capacity-provider"></a>

**Separate capacity providers by trust level.** Create different capacity providers for workloads with different security requirements. All functions assigned to the same capacity provider must be mutually trusted, as capacity providers serve as the security boundary.

**Use descriptive names.** Name capacity providers to clearly indicate their intended use and trust level (for example, `production-trusted`, `dev-sandbox`). This helps teams understand the purpose and security posture of each capacity provider.

**Use multiple Availability Zones.** Specify subnets across multiple Availability Zones when creating capacity providers. Lambda launches three instances by default for AZ resiliency, ensuring high availability for your functions.

## Instance type selection
<a name="lambda-managed-instances-bp-instance-types"></a>

**Let Lambda choose instance types.** By default, Lambda chooses the best instance types for your workload. We recommend letting Lambda Managed Instances choose instance types for you, as restricting the number of possible instance types may result in lower availability.

**Specify instance types for specific requirements.** If you have specific hardware requirements, set allowed instance types to a list of compatible instances. For example:
+ For applications requiring high network bandwidth, select several n instance types
+ For testing or development environments with cost constraints, choose smaller instance types like m7a.large

## Function configuration
<a name="lambda-managed-instances-bp-function-config"></a>

**Choose appropriate memory and vCPU settings.** Select memory and vCPU configurations that support multi-concurrent executions of your function. The minimum supported function size is 2GB and 1 vCPU.
+ For Python applications, choose a higher ratio of memory to vCPUs (such as 4 to 1 or 8 to 1) because of the way Python handles multi-concurrency
+ For CPU-intensive operations or functions that perform little IO, choose more than one vCPU
+ For IO-heavy applications like web services or batch jobs, multi-concurrency provides the most benefit

**Configure maximum concurrency appropriately.** Lambda chooses sensible defaults for maximum concurrency that balance resource consumption and throughput. Adjust this setting based on your function's resource usage:
+ Increase maximum concurrency (up to 64 per vCPU) if your function invocations use very little CPU
+ Decrease maximum concurrency if your application consumes a large amount of memory and very little CPU

Note that execution environments with very low concurrency may experience throttles and difficulty scaling.

## Scaling configuration
<a name="lambda-managed-instances-bp-scaling"></a>

**Set appropriate target resource utilization.** By default, Lambda maintains enough headroom for your traffic to double within 5 minutes without throttles. Adjust this based on your workload characteristics:
+ For very steady workloads or applications not sensitive to throttles, set the target to a high level to achieve higher utilization and lower costs
+ For workloads with potential traffic bursts, set resource targets to a low level to maintain additional headroom

**Plan for traffic growth.** If your traffic more than doubles within 5 minutes, you may see throttles as Lambda scales up instances and execution environments. Design your application to handle potential throttling during rapid scale-up periods.

## Security
<a name="lambda-managed-instances-bp-security"></a>

**Apply least privilege for PassCapacityProvider permissions.** Grant `lambda:PassCapacityProvider` permissions only for necessary capacity providers. Use resource-level permissions to restrict which capacity providers users can assign to functions.

**Monitor capacity provider usage.** Use AWS CloudTrail to monitor capacity provider assignments and access patterns. This helps identify unauthorized access attempts and ensures compliance with security policies.

**Separate untrusted workloads.** Do not rely on containers for security isolation between untrusted workloads. Use different capacity providers to separate workloads that are not mutually trusted.

## Cost optimization
<a name="lambda-managed-instances-bp-cost"></a>

**Leverage EC2 pricing options.** Take advantage of EC2 Savings Plans and Reserved Instances to reduce costs. These pricing options apply to the underlying EC2 compute (the 15% management fee is not discounted).

**Optimize for steady-state workloads.** Lambda Managed Instances are best suited for steady-state functions with predictable high-volume traffic. For bursty traffic patterns, Lambda (default) may be more cost-effective.

**Monitor resource utilization.** Track CloudWatch metrics to understand CPU and memory utilization. Adjust function memory allocation and instance type selection based on actual usage patterns to optimize costs.

## Monitoring and observability
<a name="lambda-managed-instances-bp-monitoring"></a>

**Monitor capacity provider metrics.** Track capacity provider level metrics including CPUUtilization, MemoryUtilization, vCPUAvailable, and MemoryAvailable to verify sufficient resources are available for your workloads.

**Monitor execution environment metrics.** Track execution environment level metrics including ExecutionEnvironmentConcurrency and ExecutionEnvironmentConcurrencyLimit to understand scaling behavior and identify potential throttling.

**Set up CloudWatch alarms.** Create CloudWatch alarms for key metrics to proactively identify issues:
+ High CPU or memory utilization
+ Low available capacity
+ Approaching concurrency limits

## Language-specific considerations
<a name="lambda-managed-instances-bp-runtime"></a>

**Follow language-specific best practices.** Each programming language handles multi-concurrency differently. Review the language-specific guides for detailed recommendations:
+ **Java:** Use thread-safe collections, `AtomicInteger`, and `ThreadLocal` for request-specific state
+ **Node.js:** Use InvokeStore for all request-specific state and avoid global variables
+ **Python:** Use unique file names in `/tmp` with request IDs and consider process-based memory isolation
+ **Rust:** Use `run_concurrent` instead of `run`, with the `concurrency-tokio` feature enabled. The handler must be `Clone` \+ `Send`.

**Test for thread safety and concurrency issues.** Before deploying to production, thoroughly test your functions for thread safety issues, race conditions, and proper state isolation under concurrent load.

## Next steps
<a name="lambda-managed-instances-bp-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)
+ Configure [VPC connectivity for your capacity providers](lambda-managed-instances-networking.md)
+ Monitor Lambda Managed Instances with [CloudWatch metrics](lambda-managed-instances-monitoring.md)