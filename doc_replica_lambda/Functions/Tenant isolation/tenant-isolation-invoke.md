

# Invoking Lambda functions with tenant isolation
<a name="tenant-isolation-invoke"></a>

When invoking a function that has tenant isolation enabled, you must provide a `tenant-id` parameter. This parameter ensures that your function invocation is processed in an execution environment dedicated to that specific tenant.

## Invoking functions with tenant isolation (AWS CLI)
<a name="tenant-isolation-invoke-cli"></a>

**Synchronous invocation**

For synchronous invocations, add the `--tenant-id` parameter to your [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) command:

```
aws lambda invoke \
    --function-name {{image-analysis}} \
    --tenant-id {{blue}} \
    response.json
```

**Asynchronous invocation**

For asynchronous invocations, include both the `--tenant-id` and `--invocation-type Event` parameters:

```
aws lambda invoke \
    --function-name {{image-analysis}} \
    --tenant-id {{blue}} \
    --invocation-type Event \
    response.json
```

## Invoking functions with tenant isolation (API)
<a name="tenant-isolation-invoke-api"></a>

When using the [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) API action directly, include the tenant identifier using the `X-Amzn-Tenant-Id` parameter in your request.

**Example API request**

```
POST /2015-03-31/functions/{{image-analysis}}/invocations HTTP/1.1
Host: lambda.{{us-east-1}}.amazonaws.com
Content-Type: application/json
Authorization: AWS4-HMAC-SHA256 Credential=...
X-Amz-Tenant-Id: {{blue}}

{
    "key1": "value1",
    "key2": "value2"
}
```

## Invoking functions with tenant isolation (API Gateway)
<a name="tenant-isolation-invoke-apigateway"></a>

When using API Gateway REST APIs to trigger tenant-isolated Lambda functions, you must configure API Gateway to map client request properties to the `X-Amz-Tenant-Id` header that Lambda expects. API Gateway uses Lambda's [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) API action, which requires the tenant ID to be passed using the `X-Amz-Tenant-Id` HTTP header. You can configure API Gateway to inject this HTTP header into the Lambda invocation request with a value obtained from client request properties such as HTTP headers, query parameters, or path parameters. You must first map the client request property before you can override the `X-Amz-Tenant-Id` header.

**Note**  
You cannot use HTTP APIs to invoke tenant-isolated Lambda functions because it is not possible to override the `X-Amz-Tenant-Id` header.

**Using request headers**

Configure your API Gateway integration to map a custom header from the client request to the `X-Amz-Tenant-Id` header. The following example shows a client request with an `x-tenant-id` header:

```
POST /api/process HTTP/1.1
Host: {{your-api-id}}.execute-api.{{us-east-1}}.amazonaws.com
Content-Type: application/json
x-tenant-id: {{blue}}

{
    "data": "sample payload"
}
```

In your API Gateway method configuration, you must:

1. Enable the client request header parameter (for example, `method.request.header.x-tenant-id`)

1. Map the client header to the Lambda integration header using `integration.request.header.X-Amz-Tenant-Id`

**Using query parameters**

Similarly, you can map query parameters to the `X-Amz-Tenant-Id` header:

```
GET /api/process?tenant-id={{blue}}&data={{sample}} HTTP/1.1
Host: {{your-api-id}}.execute-api.{{us-east-1}}.amazonaws.com
```

Configure the method to enable the query parameter and map it to the integration header.

## Invoking functions with tenant isolation (SDK)
<a name="tenant-isolation-invoke-sdk"></a>

When using AWS SDKs to invoke tenant-isolated functions, include the tenant identifier in your invocation request.

------
#### [ Python ]

```
import boto3
import json

lambda_client = boto3.client('lambda')

response = lambda_client.invoke(
    FunctionName='{{image-analysis}}',
    TenantId='{{blue}}',
    Payload=json.dumps({
        'key1': 'value1',
        'key2': 'value2'
    })
)

result = json.loads(response['Payload'].read())
```

------
#### [ Node.js ]

```
const AWS = require('aws-sdk');
const lambda = new AWS.Lambda();

const params = {
    FunctionName: '{{image-analysis}}',
    TenantId: '{{blue}}',
    Payload: JSON.stringify({
        key1: 'value1',
        key2: 'value2'
    })
};

lambda.invoke(params, (err, data) => {
    if (err) {
        console.error(err);
    } else {
        const result = JSON.parse(data.Payload);
        console.log(result);
    }
});
```

------
#### [ Java ]

```
import software.amazon.awssdk.services.lambda.LambdaClient;
import software.amazon.awssdk.services.lambda.model.InvokeRequest;
import software.amazon.awssdk.services.lambda.model.InvokeResponse;
import software.amazon.awssdk.core.SdkBytes;

public class TenantIsolationExample {

    public static void main(String[] args) {
        LambdaClient lambdaClient = LambdaClient.create();

        String payload = "{\"key1\": \"value1\", \"key2\": \"value2\"}";

        InvokeRequest request = InvokeRequest.builder()
                .functionName("{{image-analysis}}")
                .tenantId("{{blue}}")
                .payload(SdkBytes.fromUtf8String(payload))
                .build();

        InvokeResponse response = lambdaClient.invoke(request);
    }
}
```

------