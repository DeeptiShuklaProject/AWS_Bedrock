

# Configure Lambda durable functions
<a name="durable-configuration"></a>

Durable execution settings control how long your AWS Lambda function can run, how long the service retains execution history, and which AWS KMS key encrypts your execution data. Configure these settings to enable durable execution for your function.

## Enable durable execution
<a name="durable-config-settings"></a>

Configure the `DurableConfig` object when creating your function to set execution timeout and history retention. You can only enable durable execution when creating a function. You cannot enable it on existing functions.

------
#### [ AWS CLI ]

```
aws lambda create-function \
  --function-name my-durable-function \
  --runtime nodejs24.x \
  --role arn:aws:iam::123456789012:role/my-durable-role \
  --handler index.handler \
  --zip-file fileb://function.zip \
  --durable-config '{"ExecutionTimeout": 3600, "RetentionPeriodInDays": 30, "KMSKeyArn": "arn:aws:kms:us-east-1:111122223333:key/key-id"}'
```

------
#### [ CloudFormation ]

```
Resources:
  MyDurableFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-durable-function
      Runtime: nodejs24.x
      Handler: index.handler
      Code:
        ZipFile: |
          // Your durable function code
      DurableConfig:
        ExecutionTimeout: 3600
        RetentionPeriodInDays: 30
        KMSKeyArn: "arn:aws:kms:us-east-1:111122223333:key/key-id"
```

------

**Configuration parameters:**
+ `ExecutionTimeout` – The maximum time in seconds that a durable execution can run before Lambda stops the execution. This timeout applies to the entire durable execution, not individual function invocations. Valid range: 1–31622400.
+ `RetentionPeriodInDays` – The number of days to retain execution history after a durable execution completes. After this period, execution history is no longer available through the `GetDurableExecutionHistory` API. Valid range: 1–90.
+ `KMSKeyArn` – Optional. The ARN of a customer managed key to encrypt durable execution data. For more information, see [Encrypting Lambda durable execution data](durable-encryption.md).

For the full API reference, see [DurableConfig](https://docs.aws.amazon.com/lambda/latest/api/API_DurableConfig.html) in the Lambda API Reference.

## Configuration best practices
<a name="durable-config-best-practices"></a>

Follow these best practices when configuring durable functions for production use:
+ **Set appropriate execution timeouts** – Configure `ExecutionTimeout` based on your workflow's maximum expected duration. Do not set unnecessarily long timeouts as they affect cost and resource allocation.
+ **Balance retention with storage costs** – Set `RetentionPeriodInDays` based on your debugging and audit requirements. Longer retention periods increase storage costs.
+ **Monitor state size** – Large state objects increase storage costs and can impact performance. Keep state minimal and use external storage for large data.
+ **Configure appropriate logging** – Enable detailed logging for troubleshooting long-running workflows, but consider the impact on log volume and costs.
+ **Encrypt with your own AWS KMS key** – Set `KMSKeyArn` to a customer managed key to control key rotation, audit access, and meet compliance requirements. See [Encrypting AWS Lambda durable execution data](durable-encryption.md).

**Production configuration example:**

```
{
  "ExecutionTimeout": 86400,
  "RetentionPeriodInDays": 7,
  "KMSKeyArn": "arn:aws:kms:us-east-1:111122223333:key/key-id"
}
```

This example sets a 24-hour (86,400 seconds) execution timeout, a 7-day retention period, and a customer managed key for encryption.