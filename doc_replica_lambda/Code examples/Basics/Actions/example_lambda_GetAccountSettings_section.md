

# Use `GetAccountSettings` with a CLI
<a name="example_lambda_GetAccountSettings_section"></a>

The following code examples show how to use `GetAccountSettings`.

------
#### [ CLI ]

**AWS CLI**  
**To retrieve details about your account in an AWS Region**  
The following `get-account-settings` example displays the Lambda limits and usage information for your account.  

```
aws lambda get-account-settings
```
Output:  

```
{
    "AccountLimit": {
       "CodeSizeUnzipped": 262144000,
       "UnreservedConcurrentExecutions": 1000,
       "ConcurrentExecutions": 1000,
       "CodeSizeZipped": 52428800,
       "TotalCodeSize": 80530636800
    },
    "AccountUsage": {
       "FunctionCount": 4,
       "TotalCodeSize": 9426
    }
}
```
For more information, see [AWS Lambda Limits](https://docs.aws.amazon.com/lambda/latest/dg/limits.html) in the *AWS Lambda Developer Guide*.  
+  For API details, see [GetAccountSettings](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/get-account-settings.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: This sample displays to compare the Account Limit and Account Usage**  

```
Get-LMAccountSetting | Select-Object @{Name="TotalCodeSizeLimit";Expression={$_.AccountLimit.TotalCodeSize}}, @{Name="TotalCodeSizeUsed";Expression={$_.AccountUsage.TotalCodeSize}}
```
**Output:**  

```
TotalCodeSizeLimit TotalCodeSizeUsed
------------------ -----------------
       80530636800          15078795
```
+  For API details, see [GetAccountSettings](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: This sample displays to compare the Account Limit and Account Usage**  

```
Get-LMAccountSetting | Select-Object @{Name="TotalCodeSizeLimit";Expression={$_.AccountLimit.TotalCodeSize}}, @{Name="TotalCodeSizeUsed";Expression={$_.AccountUsage.TotalCodeSize}}
```
**Output:**  

```
TotalCodeSizeLimit TotalCodeSizeUsed
------------------ -----------------
       80530636800          15078795
```
+  For API details, see [GetAccountSettings](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.