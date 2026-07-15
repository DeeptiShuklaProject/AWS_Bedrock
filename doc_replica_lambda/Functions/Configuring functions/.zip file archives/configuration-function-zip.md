

# Deploying Lambda functions as .zip file archives
<a name="configuration-function-zip"></a>

When you create a Lambda function, you package your function code into a deployment package. Lambda supports two types of deployment packages: container images and .zip file archives. The workflow to create a function depends on the deployment package type. To configure a function defined as a container image, see [Create a Lambda function using a container image](images-create.md).

You can use the Lambda console and the Lambda API to create a function defined with a .zip file archive. You can also upload an updated .zip file to change the function code. 

By default, when you upload a .zip file, Lambda stores a copy of your source code in Lambda-managed storage. With [self-managed S3 code storage](configuration-self-managed-storage.md), Lambda reads your source code from your S3 bucket during function creation and update operations, and does not store a separate copy of your source code. Lambda still creates an internal optimized representation of your code for invocation. Your source code in S3 is not accessed on every cold start.

**Note**  
You cannot change the [deployment package type](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html#lambda-CreateFunction-request-PackageType) (.zip or container image) for an existing function. For example, you cannot convert a container image function to use a .zip file archive. You must create a new function.

**Topics**
+ [Creating the function](#configuration-function-create)
+ [Using the console code editor](#configuration-functions-console-update)
+ [Updating function code](#configuration-function-update)
+ [Changing the runtime](#configuration-function-runtime)
+ [Changing the architecture](#configuration-function-arch)
+ [Using the Lambda API](#configuration-function-api)
+ [Downloading your function code](#configuration-function-download)
+ [CloudFormation](#configuration-function-cloudformation)
+ [Encrypting Lambda .zip deployment packages](encrypt-zip-package.md)

## Creating the function
<a name="configuration-function-create"></a>

When you create a function defined with a .zip file archive, you choose a code template, the language version, and the execution role for the function. You add your function code after Lambda creates the function.

**To create the function**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose **Create function**.

1. Choose **Author from scratch** or **Use a blueprint** to create your function. 

1. Under **Basic information**, do the following:

   1. For **Function name**, enter the function name. Function names are limited to 64 characters in length.

   1. For **Runtime**, choose the language version to use for your function.

   1. (Optional) For **Architecture**, choose the instruction set architecture to use for your function. The default architecture is x86\_64. When you build the deployment package for your function, make sure that it is compatible with this [instruction set architecture](foundation-arch.md).

1. (Optional) Under **Permissions**, expand **Change default execution role**. You can create a new **Execution role** or use an existing role.

1. (Optional) Expand **Advanced settings**. You can choose a **Code signing configuration** for the function. You can also configure an (Amazon VPC) for the function to access.

1. Choose **Create function**.

Lambda creates the new function. You can now use the console to add the function code and configure other function parameters and features. For code deployment instructions, see the handler page for the runtime your function uses. 

------
#### [ Node.js ]

[Deploy Node.js Lambda functions with .zip file archives](nodejs-package.md) 

------
#### [ Python ]

 [Working with .zip file archives for Python Lambda functions](python-package.md) 

------
#### [ Ruby ]

 [Deploy Ruby Lambda functions with .zip file archives](ruby-package.md) 

------
#### [ Java ]

 [Deploy Java Lambda functions with .zip or JAR file archives](java-package.md) 

------
#### [ Go ]

 [Deploy Go Lambda functions with .zip file archives](golang-package.md) 

------
#### [ C\# ]

 [Build and deploy C\# Lambda functions with .zip file archives](csharp-package.md) 

------
#### [ PowerShell ]

 [Deploy PowerShell Lambda functions with .zip file archives](powershell-package.md) 

------

## Using the console code editor
<a name="configuration-functions-console-update"></a>

The console creates a Lambda function with a single source file. For scripting languages, you can edit this file and add more files using the built-in code editor. To save your changes, choose **Save**. Then, to run your code, choose **Test**.

When you save your function code, the Lambda console creates a .zip file archive deployment package. When you develop your function code outside of the console (using an IDE) you need to [create a deployment package](nodejs-package.md) to upload your code to the Lambda function.

## Updating function code
<a name="configuration-function-update"></a>

For scripting languages (Node.js, Python, and Ruby), you can edit your function code in the embedded code editor. If the code is larger than 3MB, or if you need to add libraries, or for languages that the editor doesn't support (Java, Go, C\#), you must upload your function code as a .zip archive. If the .zip file archive is smaller than 50 MB, you can upload the .zip file archive from your local machine. If the file is larger than 50 MB, upload the file to the function from an Amazon S3 bucket.

**To upload function code as a .zip archive**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function to update and choose the **Code** tab.

1. Under **Code source**, choose **Upload from**.

1. Choose **.zip file**, and then choose **Upload**. 

   1. In the file chooser, select the new image version, choose **Open**, and then choose **Save**.

1. (Alternative to step 4) Choose **Amazon S3 location**.

   1. In the text box, enter the S3 link URL of the .zip file archive, then choose **Save**.

When updating function code from an Amazon S3 bucket using the AWS CLI, you can specify the code storage mode. Set `S3ObjectStorageMode` to `REFERENCE` to use [self-managed S3 code storage](configuration-self-managed-storage.md), or `COPY` (default) to use Lambda-managed storage. You can change the storage mode on each update.

```
aws lambda update-function-code \
  --function-name my-function \
  --s3-bucket {{my-bucket}} \
  --s3-key {{my-function.zip}} \
  --s3-object-version {{abc123}} \
  --s3-object-storage-mode REFERENCE
```

## Changing the runtime
<a name="configuration-function-runtime"></a>

If you update the function configuration to use a new runtime, you may need to update the function code to be compatible with the new runtime. If you update the function configuration to use a different runtime, you **must** provide new function code that is compatible with the runtime and architecture. For instructions on how to create a deployment package for the function code, see the handler page for the runtime that the function uses.

The Node.js 20, Python 3.12, Java 21, .NET 8, Ruby 3.3, and later base images are based on the Amazon Linux 2023 minimal container image. Earlier base images use Amazon Linux 2. AL2023 provides several advantages over Amazon Linux 2, including a smaller deployment footprint and updated versions of libraries such as `glibc`. For more information, see [Introducing the Amazon Linux 2023 runtime for AWS Lambda](https://aws.amazon.com/blogs/compute/introducing-the-amazon-linux-2023-runtime-for-aws-lambda/) on the AWS Compute Blog.

**To change the runtime**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function to update and choose the **Code** tab.

1. Scroll down to the **Runtime settings** section, which is under the code editor.

1. Choose **Edit**.

   1. For **Runtime**, select the runtime identifier.

   1. For **Handler**, specify file name and handler for your function.

   1. For **Architecture**, choose the instruction set architecture to use for your function.

1. Choose **Save**.

## Changing the architecture
<a name="configuration-function-arch"></a>

Before you can change the instruction set architecture, you need to ensure that your function's code is compatible with the target architecture. 

If you use Node.js, Python, or Ruby and you edit your function code in the embedded editor, the existing code may run without modification.

However, if you provide your function code using a .zip file archive deployment package, you must prepare a new .zip file archive that is compiled and built correctly for the target runtime and instruction-set architecture. For instructions, see the handler page for your function runtime.

**To change the instruction set architecture**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function to update and choose the **Code** tab.

1. Under **Runtime settings**, choose **Edit**.

1. For **Architecture**, choose the instruction set architecture to use for your function.

1. Choose **Save**.

## Using the Lambda API
<a name="configuration-function-api"></a>

To create and configure a function that uses a .zip file archive, use the following API operations: 
+ [CreateFunction](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html)
+ [UpdateFunctionCode](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionCode.html)
+ [UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html)

## Downloading your function code
<a name="configuration-function-download"></a>

You can download the current unpublished (`$LATEST`) version of your function code .zip via the Lambda console. To do this, first ensure that you have the following IAM permissions:
+ `iam:GetPolicy`
+ `iam:GetPolicyVersion`
+ `iam:GetRole`
+ `iam:GetRolePolicy`
+ `iam:ListAttachedRolePolicies`
+ `iam:ListRolePolicies`
+ `iam:ListRoles`

**To download the function code .zip**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function you want to download the function code .zip for.

1. In the **Function overview**, choose the **Download** button, then choose **Download function code .zip**.

   1. Alternatively, choose **Download AWS SAM file** to generate and download a SAM template based on your function's configuration. You can also choose **Download both** to download both the .zip and the SAM template.

## CloudFormation
<a name="configuration-function-cloudformation"></a>

You can use CloudFormation to create a Lambda function that uses a .zip file archive. In your CloudFormation template, the `AWS::Lambda::Function` resource specifies the Lambda function. For descriptions of the properties in the `AWS::Lambda::Function` resource, see [AWS::Lambda::Function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html) in the *AWS CloudFormation User Guide*.

In the `AWS::Lambda::Function` resource, set the following properties to create a function defined as a .zip file archive:
+ AWS::Lambda::Function
  + PackageType – Set to `Zip`.
  + Code – Enter the Amazon S3 bucket name and .zip file name in the `S3Bucket` and `S3Key`fields. For Node.js or Python, you can provide inline source code of your Lambda function.
  + Runtime – Set the runtime value.
  + Architecture – Set the architecture value to `arm64` to use the AWS Graviton2 processor. By default, the architecture value is `x86_64`.
  + S3ObjectStorageMode – (Optional) Set to `REFERENCE` to use [self-managed S3 code storage](configuration-self-managed-storage.md). Set to `COPY` (default) to use Lambda-managed storage.