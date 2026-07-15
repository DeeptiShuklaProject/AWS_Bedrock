

# Accessing tenant identifier in Lambda function code
<a name="tenant-isolation-context"></a>

When your Lambda function has tenant isolation enabled, the tenant identifier used to invoke your function is made available within the context object passed to your function handler. You can use this identifier to implement tenant-specific logic, monitoring, and debugging capabilities.

**Topics**
+ [Accessing the tenant identifier](#tenant-isolation-context-access)
+ [Common usage patterns](#tenant-isolation-context-patterns)
+ [Monitoring and debugging](#tenant-isolation-context-monitoring)

## Accessing the tenant identifier
<a name="tenant-isolation-context-access"></a>

The tenant identifier is available through the `tenantId` property of the context object. Note that this property is available during the [invocation phase](lambda-runtime-environment.md#runtimes-lifecycle-invoke), not during the [initialization phase](lambda-runtime-environment.md#runtimes-lifecycle-ib).

------
#### [ Python ]

```
def lambda_handler(event, context):
    tenant_id = context.tenant_id
    print(f"Processing request for tenant: {tenant_id}")
    
    # Implement tenant-specific logic
    if tenant_id == "blue":
        return process_blue_tenant(event)
    elif tenant_id == "green":
        return process_green_tenant(event)
    else:
        return process_default_tenant(event)
```

------
#### [ Node.js ]

```
exports.handler = async (event, context) => {
    const tenantId = context.tenantId;
    console.log(`Processing request for tenant: ${tenantId}`);
    
    // Implement tenant-specific logic
    switch (tenantId) {
        case 'blue':
            return processBlueTenant(event);
        case 'green':
            return processGreenTenant(event);
        default:
            return processDefaultTenant(event);
    }
};
```

------
#### [ Java ]

```
public class TenantHandler implements RequestHandler<Map<String, Object>, String> {
    
    @Override
    public String handleRequest(Map<String, Object> event, Context context) {
        String tenantId = context.getTenantId();
        System.out.println("Processing request for tenant: " + tenantId);
        
        // Implement tenant-specific logic
        switch (tenantId) {
            case "blue":
                return processBlueTenant(event);
            case "green":
                return processGreenTenant(event);
            default:
                return processDefaultTenant(event);
        }
    }
}
```

------

## Common usage patterns
<a name="tenant-isolation-context-patterns"></a>

Here are common ways to use the tenant identifier in your function code:

**Tenant-specific configuration**

Use the tenant ID to load tenant-specific configuration or settings:

```
def lambda_handler(event, context):
    tenant_id = context.tenant_id
    
    # Load tenant-specific configuration
    config = load_tenant_config(tenant_id)
    database_url = config['database_url']
    api_key = config['api_key']
    
    # Process with tenant-specific settings
    return process_request(event, database_url, api_key)
```

**Tenant-specific data access**

Use the tenant ID to ensure data isolation and access control:

```
import boto3

def lambda_handler(event, context):
    tenant_id = context.tenant_id
    
    # Ensure data access is scoped to the tenant
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_data')
    
    user_id = event.get('userId')
    
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'user_id': user_id
        }
    )
    
    return process_results(response.get('Item'), tenant_id)
```

## Monitoring and debugging
<a name="tenant-isolation-context-monitoring"></a>

The tenant identifier is automatically included in Lambda logs when you have [JSON logging enabled](monitoring-cloudwatchlogs-logformat.md), making it easier to monitor and debug tenant-specific issues. You can also use the tenant ID for custom metrics and tracing.

**Example Custom metrics with tenant ID**  
The following example demonstrates how to use the tenant ID to create tenant-specific CloudWatch metrics for monitoring usage patterns and performance by tenant:  

```
import boto3

def lambda_handler(event, context):
    tenant_id = context.tenant_id
    cloudwatch = boto3.client('cloudwatch')
    
    # Record tenant-specific metrics
    cloudwatch.put_metric_data(
        Namespace='MyApp/TenantMetrics',
        MetricData=[
            {
                'MetricName': 'RequestCount',
                'Dimensions': [
                    {
                        'Name': 'TenantId',
                        'Value': tenant_id
                    }
                ],
                'Value': 1,
                'Unit': 'Count'
            }
        ]
    )
    
    return process_request(event, tenant_id)
```