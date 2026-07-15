

# Deploy and invoke Lambda durable functions with the AWS CLI
<a name="durable-getting-started-cli"></a>

Use the AWS CLI to create and deploy Lambda durable functions with imperative commands. This approach gives you direct control over each step of the deployment process.

## Prerequisites
<a name="durable-cli-prerequisites"></a>
+ Install and configure the AWS CLI. For instructions, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
+ Create a deployment package with your function code and the durable execution SDK.
+ Create an IAM execution role with checkpoint permissions.

## Create the execution role
<a name="durable-cli-create-role"></a>

Create an IAM role with permissions for basic Lambda execution and checkpoint operations.

**To create the execution role**

1. Create a trust policy document that allows Lambda to assume the role. Save this as `trust-policy.json`:

   ```
   {
     "Version": "2012-10-17",		 	 	 
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "lambda.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

1. Create the role:

   ```
   aws iam create-role \
     --role-name {{durable-function-role}} \
     --assume-role-policy-document file://trust-policy.json
   ```

1. Attach the durable execution policy for checkpoint operations and basic execution:

   ```
   aws iam attach-role-policy \
     --role-name {{durable-function-role}} \
     --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicDurableExecutionRolePolicy
   ```

The `AWSLambdaBasicDurableExecutionRolePolicy` managed policy includes the required permissions for checkpoint operations (`lambda:CheckpointDurableExecution` and `lambda:GetDurableExecutionState`) and basic Lambda execution.

## Create the durable function
<a name="durable-cli-create-function"></a>

Create your durable function with the `--durable-config` parameter.

**To create a durable function**

1. Package your function code with dependencies into a .zip file:

   ```
   zip -r function.zip index.mjs node_modules/
   ```
**Note**  
For Java-based durable functions, you need to compile your function code and dependencies into a single .zip file or Java Archive (JAR) file. For more information, see [Deploy Java Lambda functions with .zip or JAR file archives](java-package.md).

1. Create the function with durable execution enabled:

   ```
   aws lambda create-function \
     --function-name {{myDurableFunction}} \
     --runtime nodejs22.x \
     --role {{arn:aws:iam::123456789012:role/durable-function-role}} \
     --handler index.handler \
     --zip-file fileb://function.zip \
     --durable-config '{"ExecutionTimeout": 3600, "RetentionPeriodInDays": 7}'
   ```

**Note**  
You can only enable durable execution when creating the function. You cannot enable it on existing functions.

## Publish a version
<a name="durable-cli-publish-version"></a>

While durable functions can be invoked using the `$LATEST` version qualifier, you must always use a qualified ARN pointing to a stable version to ensure deterministic execution of your code.

```
aws lambda publish-version \
  --function-name {{myDurableFunction}} \
  --description "Initial version"
```

The command returns the version ARN. Note the version number (for example, `:1`) at the end of the ARN.

Optionally, create an alias that points to the version:

```
aws lambda create-alias \
  --function-name {{myDurableFunction}} \
  --name prod \
  --function-version 1
```

## Invoke the durable function
<a name="durable-cli-invoke"></a>

Invoke your durable function using the qualified ARN (version or alias).

**Note**  
**Idempotent invocations:** To prevent duplicate executions when retrying failed invocations, you can provide an execution name that ensures at-most-once execution semantics. See [Idempotency](durable-execution-idempotency.md) for details.

**Synchronous invocation**  
For executions that complete within 15 minutes, use synchronous invocation:

```
aws lambda invoke \
  --function-name {{myDurableFunction:1}} \
  --payload '{"orderId": "order-12345"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

Or using an alias:

```
aws lambda invoke \
  --function-name {{myDurableFunction:prod}} \
  --payload '{"orderId": "order-12345"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

**Asynchronous invocation**  
For long-running executions, use asynchronous invocation:

```
aws lambda invoke \
  --function-name {{myDurableFunction:prod}} \
  --invocation-type Event \
  --payload '{"orderId": "order-12345"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

With asynchronous invocation, Lambda returns immediately. The function continues executing in the background.

**Note**  
You can use `$LATEST` for prototyping and testing in the console. For production workloads, use a published version or alias.

## Manage durable executions
<a name="durable-cli-manage-executions"></a>

Use the following commands to manage and monitor durable function executions.

**List executions**  
List all executions for a durable function:

```
aws lambda list-durable-executions-by-function \
  --function-name {{myDurableFunction}}
```

**Get execution details**  
Get details about a specific execution:

```
aws lambda get-durable-execution \
  --durable-execution-arn {{arn:aws:lambda:us-east-1:123456789012:function:myDurableFunction:my-function-version/durable-execution/my-execution-name/my-execution-id}}
```

**Get execution history**  
View the checkpoint history for an execution:

```
aws lambda get-durable-execution-history \
  --durable-execution-arn {{arn:aws:lambda:us-east-1:123456789012:function:myDurableFunction:my-function-version/durable-execution/my-execution-name/my-execution-id}}
```

**Stop an execution**  
Stop a running durable execution:

```
aws lambda stop-durable-execution \
  --durable-execution-arn {{arn:aws:lambda:us-east-1:123456789012:function:myDurableFunction:my-function-version/durable-execution/my-execution-name/my-execution-id}}
```

## Update function code
<a name="durable-cli-update-function"></a>

Update your durable function code and publish a new version:

**To update and publish a new version**

1. Update the function code:

   ```
   aws lambda update-function-code \
     --function-name {{myDurableFunction}} \
     --zip-file fileb://function.zip
   ```

1. Wait for the update to complete:

   ```
   aws lambda wait function-updated \
     --function-name {{myDurableFunction}}
   ```

1. Publish a new version:

   ```
   aws lambda publish-version \
     --function-name {{myDurableFunction}} \
     --description "Updated order processing logic"
   ```

1. Update the alias to point to the new version:

   ```
   aws lambda update-alias \
     --function-name {{myDurableFunction}} \
     --name prod \
     --function-version 2
   ```

**Important**  
Running executions continue using the version they started with. New invocations use the updated alias version.

## View function logs
<a name="durable-cli-view-logs"></a>

View your durable function's logs in CloudWatch Logs:

```
aws logs tail /aws/lambda/myDurableFunction --follow
```

Filter logs for a specific execution:

```
aws logs filter-log-events \
  --log-group-name /aws/lambda/myDurableFunction \
  --filter-pattern "exec-abc123"
```

## Clean up resources
<a name="durable-cli-cleanup"></a>

Delete your durable function and associated resources:

```
# Delete the function
aws lambda delete-function --function-name {{myDurableFunction}}

# Delete the IAM role policies
aws iam detach-role-policy \
  --role-name {{durable-function-role}} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam detach-role-policy \
  --role-name {{durable-function-role}} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicDurableExecutionRolePolicy

# Delete the role
aws iam delete-role --role-name {{durable-function-role}}
```

## Next steps
<a name="durable-cli-next-steps"></a>

After deploying your durable function with the AWS CLI:
+ Monitor executions using the `list-durable-executions-by-function` and `get-durable-execution` commands
+ View checkpoint operations in AWS CloudTrail data events
+ Set up CloudWatch alarms for execution failures or long-running executions
+ Automate deployments using shell scripts or CI/CD pipelines

For more information about AWS CLI commands for Lambda, see the [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html).