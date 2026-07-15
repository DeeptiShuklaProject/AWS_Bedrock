

# Basic concepts
<a name="durable-basic-concepts"></a>

The AWS Durable Execution SDK is the foundation for building durable functions, providing the primitives you need to checkpoint progress, handle retries, and manage execution flow. The SDK is available for JavaScript/TypeScript, Python, and Java. For complete SDK documentation including API reference, quickstart tutorials, and language-specific guides, see the [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/).

## Durable execution
<a name="durable-execution-concept"></a>

A **durable execution** represents the complete lifecycle of a Lambda durable function, using a checkpoint and replay mechanism to track business logic progress, suspend execution, and recover from failures. When functions resume after suspension or interruptions, previously completed checkpoints are replayed and the function continues execution.

The lifecycle may include multiple invocations of a Lambda function to complete the execution, particularly after suspensions or failure recovery. This approach enables your function to run for extended periods (up to one year) while maintaining reliable progress despite interruptions.

**How replay works**  
Lambda keeps a running log of all durable operations (steps, waits, and other operations) as your function executes. When your function needs to pause or encounters an interruption, Lambda saves this checkpoint log and stops the execution. When it's time to resume, Lambda invokes your function again from the beginning and replays the checkpoint log, substituting stored values for completed operations. This means your code runs again, but previously completed steps don't re-execute. Their stored results are used instead.

This replay mechanism is fundamental to understanding durable functions. Your code must be deterministic during replay, meaning it produces the same results given the same inputs. Avoid operations with side effects (like generating random numbers or getting the current time) outside of steps, as these can produce different values during replay and cause non-deterministic behavior.

## DurableContext
<a name="durable-context-concept"></a>

**DurableContext** is the context object your durable function receives. It provides methods for durable operations like steps and waits that create checkpoints and manage execution flow.

Your durable function receives a `DurableContext` instead of the default Lambda context:

------
#### [ TypeScript ]

```
import {
  DurableContext,
  withDurableExecution,
} from "@aws/durable-execution-sdk-js";

export const handler = withDurableExecution(
  async (event: any, context: DurableContext) => {
    const result = await context.step(async () => {
      return "step completed";
    });
    return result;
  },
);
```

------
#### [ Python ]

```
from aws_durable_execution_sdk_python import (
    DurableContext,
    durable_execution,
    durable_step,
)

@durable_step
def my_step(step_context, data):
    # Your business logic
    return result

@durable_execution
def handler(event, context: DurableContext):
    result = context.step(my_step(event["data"]))
    return result
```

------

Through `DurableContext`, your function has access to durable operations that checkpoint progress and coordinate work:
+ **Steps** run business logic with built-in retries and automatic checkpointing. Each step saves its result, so your function resumes from the last completed step after an interruption.
+ **Waits** are planned pauses where your function stops running and stops charging until it's time to continue. Use them for time periods, external callbacks, or polling for a condition.
+ **Invoke** calls other Lambda functions and checkpoints the result. The invoked function can be a standard or durable function. Cross-account invocations are not supported.

For the full language reference to all the available durable operations, see [SDK Reference](https://docs.aws.amazon.com/durable-execution/sdk-reference/) in the AWS Durable Execution SDK Developer Guide.

## Durable function configuration
<a name="durable-configuration-basic"></a>

Durable functions have specific configuration settings that control execution behavior and data retention. These settings are separate from standard Lambda function configuration and apply to the entire durable execution lifecycle.

The **DurableConfig** object defines the configuration for durable functions:

```
{
  "ExecutionTimeout": Integer,
  "RetentionPeriodInDays": Integer
}
```

### Execution timeout
<a name="durable-execution-timeout"></a>

The **execution timeout** controls how long a durable execution can run from start to completion. This is different from the Lambda function timeout, which controls how long a single function invocation can run.

A durable execution can span multiple Lambda function invocations as it progresses through checkpoints, waits, and replays. The execution timeout applies to the total elapsed time of the durable execution, not to individual function invocations.

**Understanding the difference**  
The Lambda function timeout (maximum 15 minutes) limits each individual invocation of your function. The durable execution timeout (maximum 1 year) limits the total time from when the execution starts until it completes, fails, or times out. During this period, your function may be invoked multiple times as it processes steps, waits, and recovers from failures.

For example, if you set a durable execution timeout of 24 hours and a Lambda function timeout of 5 minutes:
+ Each function invocation must complete within 5 minutes
+ The entire durable execution can run for up to 24 hours
+ Your function can be invoked many times during those 24 hours
+ Wait operations don't count against the Lambda function timeout but do count against the execution timeout

You can configure the execution timeout when creating a durable function using the Lambda console, AWS CLI, or AWS SAM. In the Lambda console, choose your function, then Configuration, Durable execution. Set the Execution timeout value in seconds (default: 86400 seconds / 24 hours, minimum: 60 seconds, maximum: 31536000 seconds / 1 year).

**Note**  
The execution timeout and Lambda function timeout are different settings. The Lambda function timeout controls how long each individual invocation can run (maximum 15 minutes). The execution timeout controls the total elapsed time for the entire durable execution (maximum 1 year).

### Retention period
<a name="durable-retention-period"></a>

The **retention period** controls how long Lambda retains execution history and checkpoint data after a durable execution completes. This data includes step results, execution state, and the complete checkpoint log.

After the retention period expires, Lambda deletes the execution history and checkpoint data. You can no longer retrieve execution details or replay the execution. The retention period starts when the execution reaches a terminal state (SUCCEEDED, FAILED, STOPPED, or TIMED\_OUT).

You can configure the retention period when creating a durable function using the Lambda console, AWS CLI, or AWS SAM. In the Lambda console, choose your function, then Configuration, Durable execution. Set the Retention period value in days (default: 14 days, minimum: 1 day, maximum: 90 days).

Choose a retention period based on your compliance requirements, debugging needs, and cost considerations. Longer retention periods provide more time for debugging and auditing but increase storage costs.

## See also
<a name="durable-basic-concepts-see-also"></a>
+ [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/) – Complete SDK reference, quickstart tutorials, testing framework, and language-specific guides.
+ [Durable functions or Step Functions](durable-step-functions.md) – Compare durable functions with Step Functions to understand when each approach is most effective.