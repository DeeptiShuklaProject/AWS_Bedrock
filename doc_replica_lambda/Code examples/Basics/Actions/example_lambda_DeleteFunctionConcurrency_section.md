

# Use `DeleteFunctionConcurrency` with a CLI
<a name="example_lambda_DeleteFunctionConcurrency_section"></a>

The following code examples show how to use `DeleteFunctionConcurrency`.

------
#### [ CLI ]

**AWS CLI**  
**To remove the reserved concurrent execution limit from a function**  
The following `delete-function-concurrency` example deletes the reserved concurrent execution limit from the `my-function` function.  

```
aws lambda delete-function-concurrency \
    --function-name  {{my-function}}
```
This command produces no output.  
For more information, see [Reserving Concurrency for a Lambda Function](https://docs.aws.amazon.com/lambda/latest/dg/per-function-concurrency.html) in the *AWS Lambda Developer Guide*.  
+  For API details, see [DeleteFunctionConcurrency](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/delete-function-concurrency.html) in *AWS CLI Command Reference*. 

------
#### [ PowerShell ]

**Tools for PowerShell V4**  
**Example 1: This examples removes the Function Concurrency of the Lambda Function.**  

```
Remove-LMFunctionConcurrency -FunctionName "MylambdaFunction123"
```
+  For API details, see [DeleteFunctionConcurrency](https://docs.aws.amazon.com/powershell/v4/reference) in *AWS Tools for PowerShell Cmdlet Reference (V4)*. 

**Tools for PowerShell V5**  
**Example 1: This examples removes the Function Concurrency of the Lambda Function.**  

```
Remove-LMFunctionConcurrency -FunctionName "MylambdaFunction123"
```
+  For API details, see [DeleteFunctionConcurrency](https://docs.aws.amazon.com/powershell/v5/reference) in *AWS Tools for PowerShell Cmdlet Reference (V5)*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.