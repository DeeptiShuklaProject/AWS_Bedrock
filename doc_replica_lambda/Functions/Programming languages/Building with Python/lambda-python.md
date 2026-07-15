

# Building Lambda functions with Python
<a name="lambda-python"></a>

You can run Python code in AWS Lambda. Lambda provides [runtimes](lambda-runtimes.md) for Python that run your code to process events. Your code runs in an environment that includes the SDK for Python (Boto3), with credentials from an AWS Identity and Access Management (IAM) role that you manage. To learn more about the SDK versions included with the Python runtimes, see [Runtime-included SDK versions](#python-sdk-included).

Lambda supports the following Python runtimes.


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| Python 3.14 | `python3.14` | Amazon Linux 2023 |  Jun 30, 2029  |  Jul 31, 2029  |  Aug 31, 2029  | 
| Python 3.13 | `python3.13` | Amazon Linux 2023 |  Jun 30, 2029  |  Jul 31, 2029  |  Aug 31, 2029  | 
| Python 3.12 | `python3.12` | Amazon Linux 2023 |  Oct 31, 2028  |  Nov 30, 2028  |  Jan 10, 2029  | 
| Python 3.11 | `python3.11` | Amazon Linux 2 |  Jun 30, 2027  |  Jul 31, 2027  |  Aug 31, 2027  | 
| Python 3.10 | `python3.10` | Amazon Linux 2 |  Oct 31, 2026  |  Feb 1, 2027  |  Mar 3, 2027  | 

**To create a Python function**

1. Open the [Lambda console](https://console.aws.amazon.com/lambda).

1. Choose **Create function**.

1. Configure the following settings:
   + **Function name**: Enter a name for the function.
   + **Runtime**: Choose **Python 3.14**.

1. Choose **Create function**.

The console creates a Lambda function with a single source file named `lambda_function`. You can edit this file and add more files in the built-in code editor. In the **DEPLOY** section, choose **Deploy** to update your function's code. Then, to run your code, choose **Create test event** in the **TEST EVENTS** section.

Your Lambda function comes with a CloudWatch Logs log group. The function runtime sends details about each invocation to CloudWatch Logs. It relays any [logs that your function outputs](python-logging.md) during invocation. If your function returns an error, Lambda formats the error and returns it to the invoker.

**Topics**
+ [Runtime-included SDK versions](#python-sdk-included)
+ [Disabled Python features](#python-disabled-features)
+ [Response format](#python-response-format)
+ [Graceful shutdown for extensions](#python-graceful-shutdown)
+ [Define Lambda function handler in Python](python-handler.md)
+ [Working with .zip file archives for Python Lambda functions](python-package.md)
+ [Deploy Python Lambda functions with container images](python-image.md)
+ [Working with layers for Python Lambda functions](python-layers.md)
+ [Using the Lambda context object to retrieve Python function information](python-context.md)
+ [Log and monitor Python Lambda functions](python-logging.md)
+ [AWS Lambda function testing in Python](python-testing.md)
+ [Instrumenting Python code in AWS Lambda](python-tracing.md)

## Runtime-included SDK versions
<a name="python-sdk-included"></a>

The version of the AWS SDK included in the Python runtime depends on the runtime version and your AWS Region. To find the version of the SDK included in the runtime you're using, create a Lambda function with the following code.

```
import boto3
import botocore

def lambda_handler(event, context):
   print(f'boto3 version: {boto3.__version__}')
   print(f'botocore version: {botocore.__version__}')
```

## Disabled Python features
<a name="python-disabled-features"></a>

The following table lists Python features which are disabled in the Lambda managed runtimes and container base images for Python. These features must be enabled when the Python runtime executable is compiled and cannot be enabled by using an execution-time flag. To use these features in Lambda, you can deploy your own Python runtime build with these features enabled, using a [container image](python-image.md#python-image-clients) or [custom runtime](runtimes-custom.md).


| Python feature | Affected Python versions | Status | 
| --- | --- | --- | 
| Just-in-Time (JIT) compiler | Python 3.13 and later | The JIT compiler is experimental and is not recommended for production workloads. It is therefore disabled in the Lambda Python runtimes. | 
| Free-threading | Python 3.13 and later | Free threading (option to disable the global interpreter lock) is disabled in Lambda Python builds due to the performance impact on single-threaded code. | 

## Response format
<a name="python-response-format"></a>

In Python 3.12 and later Python runtimes, functions return Unicode characters as part of their JSON response. Earlier Python runtimes return escaped sequences for Unicode characters in responses. For example, in Python 3.11, if you return a Unicode string such as "こんにちは", it escapes the Unicode characters and returns "\\u3053\\u3093\\u306b\\u3061\\u306f". The Python 3.12 runtime returns the original "こんにちは".

Using Unicode responses reduces the size of Lambda responses, making it easier to fit larger responses into the 6 MB maximum payload size for synchronous functions. In the previous example, the escaped version is 32 bytes—compared to 17 bytes with the Unicode string.

When you upgrade to Python 3.12 or later Python runtimes, you might need to adjust your code to account for the new response format. If the caller expects escaped Unicode, you must either add code to the returning function to escape the Unicode manually, or adjust the caller to handle the Unicode return.

## Graceful shutdown for extensions
<a name="python-graceful-shutdown"></a>

Python 3.12 and later Python runtimes offer improved graceful shutdown capabilities for functions with [external extensions](lambda-extensions.md). When Lambda shuts down an execution environment, it sends a `SIGTERM` signal to the runtime and then a `SHUTDOWN` event to each registered external extension. You can catch the `SIGTERM` signal in your Lambda function and clean up resources such as database connections that were created by the function.

To learn more about the execution environment lifecycle, see [Understanding the Lambda execution environment lifecycle](lambda-runtime-environment.md). For examples of how to use graceful shutdown with extensions, see the [AWS Samples GitHub repository](https://github.com/aws-samples/graceful-shutdown-with-aws-lambda).