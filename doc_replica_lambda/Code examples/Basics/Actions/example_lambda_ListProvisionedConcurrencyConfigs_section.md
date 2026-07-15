

# Use `ListProvisionedConcurrencyConfigs` with a CLI
<a name="example_lambda_ListProvisionedConcurrencyConfigs_section"></a>

The following code examples show how to use `ListProvisionedConcurrencyConfigs`.

------
#### [ CLI ]

**AWS CLI**  
**To get a list of provisioned concurrency configurations**  
The following `list-provisioned-concurrency-configs` example lists the provisioned concurrency configurations for the specified function.  

```
aws lambda list-provisioned-concurrency-configs \
    --function-name {{my-function}}
```
Output:  

```
{
    "ProvisionedConcurrencyConfigs": [
        {
            "FunctionArn": "arn:aws:lambda:us-east-2:123456789012:function:my-function:GREEN",
            "RequestedProvisionedConcurrentExecutions": 100,
            "AvailableProvisionedConcurrentExecutions": 100,
            "AllocatedProvisionedConcurrentExecutions": 100,
            "Status": "READY",
            "LastModified": "2019-12-31T20:29:00+0000"
        },
        {
            "FunctionArn": "arn:aws:lambda:us-east-2:123456789012:function:my-function:BLUE",
            "RequestedProvisionedConcurrentExecutions": 100,
            "AvailableProvisionedConcurrentExecutions": 100,
            "AllocatedProvisionedConcurrentExecutions": 100,
            "Status": "READY",
            "LastModified": "2019-12-31T20:28:49+0000"
        }
    ]
}
```
+  For API details, see [ListProvisionedConcurrencyConfigs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/list-provisioned-concurrency-configs.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: This example retrieves the list of provisioned concurrency configurations for a Lambda function.**  

```
Get-LMProvisionedConcurrencyConfigList -FunctionName "MylambdaFunction123"
```
+  For API details, see [ListProvisionedConcurrencyConfigs](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: This example retrieves the list of provisioned concurrency configurations for a Lambda function.**  

```
Get-LMProvisionedConcurrencyConfigList -FunctionName "MylambdaFunction123"
```
+  For API details, see [ListProvisionedConcurrencyConfigs](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.