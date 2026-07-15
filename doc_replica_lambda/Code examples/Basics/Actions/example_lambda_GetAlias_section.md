

# Use `GetAlias` with a CLI
<a name="example_lambda_GetAlias_section"></a>

The following code examples show how to use `GetAlias`.

------
#### [ CLI ]

**AWS CLI**  
**To retrieve details about a function alias**  
The following `get-alias` example displays details for the alias named `LIVE` on the `my-function` Lambda function.  

```
aws lambda get-alias \
    --function-name {{my-function}} \
    --name {{LIVE}}
```
Output:  

```
{
    "FunctionVersion": "3",
    "Name": "LIVE",
    "AliasArn": "arn:aws:lambda:us-west-2:123456789012:function:my-function:LIVE",
    "RevisionId": "594f41fb-b85f-4c20-95c7-6ca5f2a92c93",
    "Description": "alias for live version of function"
}
```
For more information, see [Configuring AWS Lambda Function Aliases](https://docs.aws.amazon.com/lambda/latest/dg/aliases-intro.html) in the *AWS Lambda Developer Guide*.  
+  For API details, see [GetAlias](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/get-alias.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: This example retrieves the Routing Config weights for a specific Lambda Function Alias.**  

```
Get-LMAlias -FunctionName "MylambdaFunction123" -Name "newlabel1" -Select RoutingConfig
```
**Output:**  

```
AdditionalVersionWeights
------------------------
{[1, 0.6]}
```
+  For API details, see [GetAlias](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: This example retrieves the Routing Config weights for a specific Lambda Function Alias.**  

```
Get-LMAlias -FunctionName "MylambdaFunction123" -Name "newlabel1" -Select RoutingConfig
```
**Output:**  

```
AdditionalVersionWeights
------------------------
{[1, 0.6]}
```
+  For API details, see [GetAlias](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.