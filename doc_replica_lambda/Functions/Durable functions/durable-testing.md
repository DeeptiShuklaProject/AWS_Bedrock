

# Testing Lambda durable functions
<a name="durable-testing"></a>

Use the Durable Execution testing SDKs to run and inspect executions both locally and in the cloud. For authoring tests, assertions, the cloud runner, SAM CLI integration, and complete examples, see [Testing](https://docs.aws.amazon.com/durable-execution/testing/) in the AWS Durable Execution SDK Developer Guide.

## IAM permissions for cloud testing
<a name="durable-cloud-testing"></a>

When you use the cloud runner or `sam remote invoke` to test a deployed durable function, the calling principal needs permission to invoke the function and to read its execution history. Attach the following permissions to your test caller:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:GetDurableExecution",
                "lambda:GetDurableExecutionHistory"
            ],
            "Resource": [
                "arn:aws:lambda:region:account-id:function:function-name",
                "arn:aws:lambda:region:account-id:function:function-name:*"
            ]
        }
    ]
}
```

Replace {{region}}, {{account-id}}, and {{function-name}} with your values.

## Debugging failures
<a name="durable-testing-debugging"></a>

When tests fail, inspect the execution result to understand what went wrong. Check the execution status to see if the function succeeded, failed, or timed out. Read error messages to understand the failure cause.

Inspect individual operation results to find where behavior diverged from expectations. Check step results to see what values were produced. Verify operation ordering to confirm operations executed in the expected sequence. Count operations to ensure the right number of steps, waits, and callbacks were created.

Common issues include non-deterministic code that produces different results on replay, shared state through global variables that breaks during replay, and missing operations due to conditional logic errors. Use standard debuggers and logging to step through function code and track execution flow.

For cloud tests, inspect execution history in CloudWatch Logs to see detailed operation logs. Use tracing to track execution flow across services and identify bottlenecks.