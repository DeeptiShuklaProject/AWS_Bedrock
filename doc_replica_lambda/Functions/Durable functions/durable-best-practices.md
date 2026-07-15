

# Best practices for Lambda durable functions
<a name="durable-best-practices"></a>

Durable functions use a replay-based execution model that requires different programming practices than traditional Lambda functions. See [Best practices](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/) in the AWS Durable Execution SDK Developer Guide for guidance on how to write and test durable workflow code.

The following recommendations are best practices for deploying, invoking, and monitoring Lambda durable functions.

## Function versions and aliases
<a name="durable-versioning"></a>

Invoke functions with version numbers or aliases to pin executions to specific code versions. Ensure new code versions can handle state from older versions. Don't rename steps or change their behavior in ways that break replay.

## Monitoring
<a name="durable-monitoring-best-practices"></a>

Enable structured logging with execution IDs and step names. Set up CloudWatch alarms for error rates and execution duration. Use tracing to identify bottlenecks. For detailed guidance, see [Monitoring and debugging](durable-monitoring.md).

## Error handling
<a name="durable-error-handling-best-practices"></a>

In addition to configuring retry strategies for transient failures, configure a dead-letter queue (DLQ) on your durable function to capture events from permanently failed executions. When a durable execution reaches a terminal state (FAILED, STOPPED, or TIMED\_OUT) after an asynchronous invocation, Lambda sends the original triggering event to the DLQ. This allows you to inspect, debug, and optionally reprocess failed events without losing them.

To configure a DLQ, set the `DeadLetterConfig` property on your function to an Amazon SQS queue or Amazon SNS topic ARN. For more information, see [Dead-letter queues](invocation-async-retain-records.md#invocation-dlq).

Follow these best practices for error handling with durable functions:
+ **Configure a DLQ for async invocations** – Always attach a dead-letter queue when invoking durable functions asynchronously. Unlike standard Lambda functions, durable executions are not automatically retried on failure, so the DLQ is your safety net for capturing events that led to permanently failed executions.
+ **Use retry strategies within steps** – Configure explicit retry strategies with appropriate backoff for transient failures. For guidance on configuring retries, see [Retries for durable functions](durable-execution-sdk-retries.md).
+ **Combine DLQs with EventBridge notifications** – Use EventBridge rules to alert on FAILED, STOPPED, and TIMED\_OUT status changes for real-time visibility, and use a DLQ to preserve the original event payload for later analysis or reprocessing.
+ **Monitor DLQ depth** – Create a CloudWatch alarm on the `ApproximateNumberOfMessagesVisible` metric for your DLQ to detect when failures are accumulating.

## Related resources
<a name="durable-additional-resources"></a>
+ [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/)
+ [Monitoring Lambda durable functions](durable-monitoring.md)
+ [Retries for Lambda durable functions](durable-execution-sdk-retries.md)
+ [Testing Lambda durable functions](durable-testing.md)