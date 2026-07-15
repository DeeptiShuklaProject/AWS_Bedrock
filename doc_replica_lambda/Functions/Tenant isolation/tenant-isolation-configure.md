

# Enabling tenant isolation for Lambda functions
<a name="tenant-isolation-configure"></a>

To activate tenant isolation mode, create a new Lambda function. You cannot enable tenant isolation on existing functions.

**Topics**
+ [Enabling tenant isolation (console)](#tenant-isolation-console)
+ [Enabling tenant isolation (AWS CLI)](#tenant-isolation-cli)
+ [Enabling tenant isolation (API)](#tenant-isolation-api)
+ [Enabling tenant isolation (CloudFormation)](#tenant-isolation-cfn)

## Enabling tenant isolation (console)
<a name="tenant-isolation-console"></a>

**To create a Lambda function using the console**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose **Create function**.

1. Select **Author from scratch**.

1. In the **Basic information** pane, for **Function name**, enter `image-analysis`.

1. For **Runtime**, choose any of the [supported Lambda runtimes](lambda-runtimes.md#runtimes-supported).

1. Under additional configurations, **Tenant isolation mode**, select **Enable**.

1. Review your settings, and choose **Create function**.

## Enabling tenant isolation (AWS CLI)
<a name="tenant-isolation-cli"></a>

**Create function with tenant isolation**

When creating a new function using the CLI, add the `--tenancy-config '{"TenantIsolationMode": "PER_TENANT"}'` option to your [create-function](https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html) request. Example:

```
aws lambda create-function \
    --function-name {{image-analysis}} \
    --runtime {{nodejs24.x}} \
    --zip-file fileb://image-analysis-function.zip \
    --handler image-analysis-function.handler \
    --role {{arn:aws:iam:123456789012:role/execution-role}} \
    --tenancy-config '{"TenantIsolationMode": "PER_TENANT"}'
```

## Enabling tenant isolation (API)
<a name="tenant-isolation-api"></a>

**To enable tenant isolation using the Lambda API**

1. Create a new function with tenant isolation enabled by using the [CreateFunction](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html) API action with the `TenancyConfig` parameter.

1. Confirm that tenant isolation is enabled for the function by using the [GetFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_GetFunctionConfiguration.html) action. If the response shows that `TenantIsolationMode` is `PER_TENANT`, then tenant isolation is enabled for the function:

   ```
   "TenancyConfig": { 
           "TenantIsolationMode": "PER_TENANT"
        }
   ```

Invoke the function version with the [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) action. For more information, see [Invoking Lambda functions with tenant isolation](tenant-isolation-invoke.md).

## Enabling tenant isolation (CloudFormation)
<a name="tenant-isolation-cfn"></a>

The following CloudFormation template creates a new Lambda function with tenant isolation enabled:

```
MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: {{my-sample-python-lambda}}
      Runtime: {{python3.14}}
      Role: !GetAtt LambdaExecutionRole.Arn
      Handler: index.lambda_handler
      TenancyConfig:
        TenantIsolationMode: PER_TENANT
      Code:
        ZipFile: |
          import json

          def lambda_handler(event, context):
              return {
                  'statusCode': {{200}},
                  'body': json.dumps(f'Hello from Lambda! Tenant-ID: {context.tenant_id}')
              }
      Timeout: {{10}}
      MemorySize: {{128}}
```