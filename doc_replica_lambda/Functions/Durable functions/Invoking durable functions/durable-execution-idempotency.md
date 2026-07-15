

# Idempotency
<a name="durable-execution-idempotency"></a>

Durable functions provide built-in idempotency for execution starts through execution names. When you provide an execution name, Lambda uses it to prevent duplicate executions and enable safe retries of invocation requests. Steps have at-least-once execution semantics by default. During replay, the SDK returns checkpointed results without re-executing completed steps, but your business logic must be idempotent to handle potential retries before completion.

**Note**  
Lambda event source mappings (ESM) don't support idempotency at launch. Therefore, each invocation (including retries) starts a new durable execution. To ensure idempotent execution with event source mappings, either implement idempotency logic in your function code such as with [Powertools for AWS Lambda](https://docs.aws.amazon.com//powertools/) or use a regular Lambda function as proxy (dispatcher) to invoke a durable function with an idempotency key (execution name parameter).

## Execution names
<a name="durable-idempotency-execution-names"></a>

You can provide an execution name when invoking a durable function. The execution name acts as an idempotency key, allowing you to safely retry invocation requests without creating duplicate executions. If you don't provide a name, Lambda generates a unique execution ID automatically.

Execution names must be unique within your account and region. When you invoke a function with an execution name that already exists, Lambda behavior depends on the existing execution's state and whether the payload matches.

## Idempotency behavior
<a name="durable-idempotency-behavior"></a>

The following table describes how Lambda handles invocation requests based on whether you provide an execution name, the existing execution state, and whether the payload matches:


| Scenario | Name provided? | Existing execution status | Payload identical? | Behavior | 
| --- | --- | --- | --- | --- | 
| 1 | No | N/A | N/A | New execution started: Lambda generates a unique execution ID and starts a new execution | 
| 2 | Yes | Never existed or retention expired | N/A | New execution started: Lambda starts a new execution with the provided name | 
| 3 | Yes | Running | Yes | Idempotent start: Lambda returns the existing execution information without starting a duplicate. For synchronous invocations, this acts as a reattach to the running execution | 
| 4 | Yes | Running | No | Error: Lambda returns DurableExecutionAlreadyStartedException error because an execution with this name is already running with different payload | 
| 5 | Yes | Closed (succeeded, failed, stopped, or timed out) | Yes | Idempotent start: Lambda returns the existing execution information without starting a new execution. The closed execution result is returned | 
| 6 | Yes | Closed (succeeded, failed, stopped, or timed out) | No | Error: Lambda returns DurableExecutionAlreadyStartedException error because an execution with this name already completed with different payload | 

**Note**  
Scenarios 3 and 5 demonstrate idempotent behavior where Lambda safely handles duplicate invocation requests by returning existing execution information instead of creating duplicates.

## Step idempotency
<a name="durable-idempotency-steps"></a>

Steps have at-least-once execution semantics by default. When your function replays after a wait, callback, or failure, the SDK checks each step against the checkpoint log. For steps that already completed, the SDK returns the checkpointed result without re-executing the step logic. However, if a step fails or the function is interrupted before the step completes, the step may execute multiple times.

The business logic inside your steps must be idempotent to handle potential retries. Use idempotency keys to ensure operations like payments or database writes execute only once, even if the step retries. See [Idempotency and retries](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/idempotency/) in the AWS Durable Execution SDK Developer Guide for details on how to code for idempotency.