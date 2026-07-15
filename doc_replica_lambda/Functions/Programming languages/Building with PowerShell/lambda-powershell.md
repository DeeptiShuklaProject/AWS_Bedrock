

# Building Lambda functions with PowerShell
<a name="lambda-powershell"></a>

The following sections explain how common programming patterns and core concepts apply when you author Lambda function code in PowerShell.

Lambda provides the following sample applications for PowerShell:
+ [blank-powershell](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-powershell) – A PowerShell function that shows the use of logging, environment variables, and the AWS SDK.

Before you get started, you must first set up a PowerShell development environment. For instructions on how to do this, see [Setting Up a PowerShell Development Environment](powershell-devenv.md).

To learn about how to use the AWSLambdaPSCore module to download sample PowerShell projects from templates, create PowerShell deployment packages, and deploy PowerShell functions to the AWS Cloud, see [Deploy PowerShell Lambda functions with .zip file archives](powershell-package.md).

Lambda provides the following runtimes for .NET languages:


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| .NET 10 | `dotnet10` | Amazon Linux 2023 |  Nov 14, 2028  |  Dec 14, 2028  |  Jan 15, 2029  | 
| .NET 9 (container only) | `dotnet9` | Amazon Linux 2023 |  Nov 10, 2026  |  Not scheduled  |  Not scheduled  | 
| .NET 8 | `dotnet8` | Amazon Linux 2023 |  Nov 10, 2026  |  Feb 1, 2027  |  Mar 3, 2027  | 

**Topics**
+ [Setting Up a PowerShell Development Environment](powershell-devenv.md)
+ [Deploy PowerShell Lambda functions with .zip file archives](powershell-package.md)
+ [Define Lambda function handler in PowerShell](powershell-handler.md)
+ [Using the Lambda context object to retrieve PowerShell function information](powershell-context.md)
+ [Log and monitor Powershell Lambda functions](powershell-logging.md)