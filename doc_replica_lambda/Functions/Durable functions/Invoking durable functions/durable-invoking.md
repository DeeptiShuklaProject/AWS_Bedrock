

# Invoking durable Lambda functions
<a name="durable-invoking"></a>

Durable Lambda functions support the same invocation methods as standard Lambda functions. You can invoke durable functions synchronously, asynchronously, or through event source mappings. The invocation process is identical to standard functions, but durable functions provide additional capabilities for long-running executions and automatic state management.

## Invocation methods
<a name="durable-invoking-methods"></a>

**Synchronous invocation:** Invoke a durable function and wait for the response. Synchronous invocations are limited by the Lambda to 15 minutes (or less, depending on the configured function and execution timeout). Use synchronous invocation when you need immediate results or when integrating with APIs and services that expect a response. You can use wait operations for efficient computation without disrupting the caller—the invocation waits for the entire durable execution to complete. For idempotent execution starts, use the execution name parameter as described in [Idempotency](durable-execution-idempotency.md).

```
aws lambda invoke \
  --function-name my-durable-function:1 \
  --cli-binary-format raw-in-base64-out \
  --payload '{"orderId": "12345"}' \
  response.json
```

**Asynchronous invocation:** Queue an event for processing without waiting for a response. Lambda places the event in a queue and returns immediately. Asynchronous invocations support execution durations up to 1 year. Use asynchronous invocation for fire-and-forget scenarios or when processing can happen in the background. For idempotent execution starts, use the execution name parameter as described in [Idempotency](durable-execution-idempotency.md).

```
aws lambda invoke \
  --function-name my-durable-function:1 \
  --invocation-type Event \
  --cli-binary-format raw-in-base64-out \
  --payload '{"orderId": "12345"}' \
  response.json
```

**Event source mappings:** Configure Lambda to automatically invoke your durable function when records are available from stream or queue-based services like Amazon SQS, Kinesis, or DynamoDB. Event source mappings poll the event source and invoke your function with batches of records. For details about using event source mappings with durable functions, including execution duration limits, see [Event source mappings with durable functions](durable-invoking-esm.md).

For complete details about each invocation method, see [synchronous invocation](invocation-sync.md) and [asynchronous invocation](invocation-async.md).

**Note**  
Durable functions support dead-letter queues (DLQs) for error handling, but don't support Lambda destinations. Configure a DLQ to capture records from failed invocations.

## Qualified ARNs requirement
<a name="durable-invoking-qualified-arns"></a>

Durable functions require qualified identifiers for invocation. You must invoke durable functions using a version number, alias, or `$LATEST`. You can use either a full qualified ARN or a function name with version/alias suffix. You cannot use an unqualified identifier (without a version or alias suffix).

**Valid invocations:**

```
# Using full ARN with version number
arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:1

# Using full ARN with alias
arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:prod

# Using full ARN with $LATEST
arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:$LATEST

# Using function name with version number
my-durable-function:1

# Using function name with alias
my-durable-function:prod
```

**Invalid invocations:**

```
# Unqualified ARN (not allowed)
arn:aws:lambda:us-east-1:123456789012:function:my-durable-function

# Unqualified function name (not allowed)
my-durable-function
```

This requirement ensures that durable executions remain consistent throughout their lifecycle. When a durable execution starts, it's pinned to the specific function version. If your function pauses and resumes hours or days later, Lambda invokes the same version that started the execution, ensuring code consistency across the entire workflow.

**Best practice**  
Use numbered versions or aliases for production durable functions rather than `$LATEST`. Numbered versions are immutable and support deterministic replay. Optionally, aliases provide a stable reference that you can update to point to new versions without changing invocation code. When you update an alias, new executions use the new version, while in-progress executions continue with their original version. You may use `$LATEST` for prototyping or to shorten deployment times during development, understanding that executions might not replay correctly (or even fail) if the underlying code changes during running executions.

## Understanding execution lifecycle
<a name="durable-invoking-execution-lifecycle"></a>

When you invoke a durable function, Lambda creates a durable execution that can span multiple function invocations:

1. **Initial invocation:** Your invocation request creates a new durable execution. Lambda assigns a unique execution ID and starts processing.

1. **Execution and checkpointing:** As your function executes durable operations, the SDK creates checkpoints that track progress.

1. **Suspension (if needed):** If your function uses durable waits, such as `wait` or `waitForCallback`, or automatic step retries, Lambda suspends the execution and stops charging for compute time.

1. **Resumption:** When it's time to resume (including after retries), Lambda invokes your function again. The SDK replays the checkpoint log and continues from where execution paused.

1. **Completion:** When your function returns a final result or throws an unhandled error, the durable execution completes.

For synchronous invocations, the caller waits for the entire durable execution to complete, including any wait operations. If the execution exceeds the invocation timeout (15 minutes or less), the invocation times out. For asynchronous invocations, Lambda returns immediately and the execution continues independently. Use the durable execution APIs to track execution status and retrieve final results.

## Invoking from application code
<a name="durable-invoking-with-sdk"></a>

Use the AWS SDKs to invoke durable functions from your application code. The invocation process is identical to standard functions:

------
#### [ TypeScript ]

```
import { LambdaClient, InvokeCommand } from '@aws-sdk/client-lambda';

const client = new LambdaClient({});

// Synchronous invocation
const response = await client.send(new InvokeCommand({
  FunctionName: 'arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:1',
  Payload: JSON.stringify({ orderId: '12345' })
}));

const result = JSON.parse(Buffer.from(response.Payload!).toString());

// Asynchronous invocation
await client.send(new InvokeCommand({
  FunctionName: 'arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:1',
  InvocationType: 'Event',
  Payload: JSON.stringify({ orderId: '12345' })
}));
```

------
#### [ Python ]

```
import boto3
import json

client = boto3.client('lambda')

# Synchronous invocation
response = client.invoke(
    FunctionName='arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:1',
    Payload=json.dumps({'orderId': '12345'})
)

result = json.loads(response['Payload'].read())

# Asynchronous invocation
client.invoke(
    FunctionName='arn:aws:lambda:us-east-1:123456789012:function:my-durable-function:1',
    InvocationType='Event',
    Payload=json.dumps({'orderId': '12345'})
)
```

------

## Chained invocations
<a name="durable-invoking-chained"></a>

Durable functions can invoke other durable and non-durable functions using the `invoke` operation from `DurableContext`. This creates a chained invocation where the calling function waits (suspends) for the invoked function to complete:

------
#### [ TypeScript ]

```
export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    // Invoke another durable function and wait for result
    const result = await context.invoke(
      'process-order',
      'arn:aws:lambda:us-east-1:123456789012:function:order-processor:1',
      { orderId: event.orderId }
    );
    
    return { statusCode: 200, body: JSON.stringify(result) };
  }
);
```

------
#### [ Python ]

```
@durable_execution
def handler(event, context: DurableContext):
    # Invoke another durable function and wait for result
    result = context.invoke(
        'arn:aws:lambda:us-east-1:123456789012:function:order-processor:1',
        {'orderId': event['orderId']},
        name='process-order'
    )
    
    return {'statusCode': 200, 'body': json.dumps(result)}
```

------

Chained invocations create a checkpoint in the calling function. If the calling function is interrupted, it resumes from the checkpoint with the invoked function's result, without re-invoking the function.

**Note**  
Cross-account chained invocations are not supported. The invoked function must be in the same AWS account as the calling function.