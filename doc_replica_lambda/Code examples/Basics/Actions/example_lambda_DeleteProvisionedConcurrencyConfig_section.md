

# Use `DeleteProvisionedConcurrencyConfig` with a CLI
<a name="example_lambda_DeleteProvisionedConcurrencyConfig_section"></a>

The following code examples show how to use `DeleteProvisionedConcurrencyConfig`.

------
#### [ CLI ]

**AWS CLI**  
**To delete a provisioned concurrency configuration**  
The following `delete-provisioned-concurrency-config` example deletes the provisioned concurrency configuration for the `GREEN` alias of the specified function.  

```
aws lambda delete-provisioned-concurrency-config \
    --function-name {{my-function}} \
    --qualifier {{GREEN}}
```
+  For API details, see [DeleteProvisionedConcurrencyConfig](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/delete-provisioned-concurrency-config.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: This example removes the Provisioned Concurrency Configuration for a specific Alias.**  

```
Remove-LMProvisionedConcurrencyConfig -FunctionName "MylambdaFunction123" -Qualifier "NewAlias1"
```
+  For API details, see [DeleteProvisionedConcurrencyConfig](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: This example removes the Provisioned Concurrency Configuration for a specific Alias.**  

```
Remove-LMProvisionedConcurrencyConfig -FunctionName "MylambdaFunction123" -Qualifier "NewAlias1"
```
+  For API details, see [DeleteProvisionedConcurrencyConfig](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.