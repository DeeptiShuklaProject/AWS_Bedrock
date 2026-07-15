

# Security and permissions
<a name="lambda-managed-instances-security"></a>

Lambda Managed Instances use **capacity providers as trust boundaries**. Functions execute in containers within these instances, but containers do not provide security isolation between workloads. All functions assigned to the same capacity provider must be mutually trusted.

## Key Security Concepts
<a name="lambda-managed-instances-key-security-concepts"></a>
+ **Capacity Provider**: The security boundary that defines trust levels for Lambda functions
+ **Container Isolation**: Containers are not a security boundary - do not rely on them for security between untrusted workloads
+ **Trust Separation**: Separate workloads that are not mutually trusted by using different capacity providers

## Required Permissions
<a name="lambda-managed-instances-required-permissions"></a>

### PassCapacityProvider Action
<a name="lambda-managed-instances-pass-capacity-provider"></a>

Users need the `lambda:PassCapacityProvider` permission to assign functions to capacity providers. This permission acts as a security gate, ensuring only authorized users can place functions in specific capacity providers.

Account administrators control which functions can use specific capacity providers through the `lambda:PassCapacityProvider` IAM action. This action is required when:
+ Creating functions that use Lambda Managed Instances
+ Updating function configurations to use a capacity provider
+ Deploying functions via infrastructure as code

**Example IAM Policy**

```
{
  "Version": "2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:PassCapacityProvider",
      "Resource": "arn:aws:lambda:*:*:capacity-provider:trusted-workloads-*"
    }
  ]
}
```

### Service-Linked Role
<a name="lambda-managed-instances-service-linked-role"></a>

AWS Lambda uses the `AWSServiceRoleForLambda` service-linked role to manage Lambda Managed Instances ec2 resources in your capacity providers.

## Best Practices
<a name="lambda-managed-instances-security-best-practices"></a>

1. **Separate by Trust Level**: Create different capacity providers for workloads with different security requirements

1. **Use Descriptive Names**: Name capacity providers to clearly indicate their intended use and trust level (e.g., `production-trusted`, `dev-sandbox`)

1. **Apply Least Privilege**: Grant `PassCapacityProvider` permissions only for necessary capacity providers

1. **Monitor Usage**: Use AWS CloudTrail to monitor capacity provider assignments and access patterns

## Next steps
<a name="lambda-managed-instances-security-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Configure [VPC connectivity for your capacity providers](lambda-managed-instances-networking.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)