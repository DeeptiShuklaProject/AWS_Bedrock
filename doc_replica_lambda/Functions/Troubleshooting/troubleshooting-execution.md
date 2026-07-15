

# Troubleshoot execution issues in Lambda
<a name="troubleshooting-execution"></a>

When the Lambda runtime runs your function code, the event might be processed on an instance of the function that's been processing events for some time, or it might require a new instance to be initialized. Errors can occur during function initialization, when your handler code processes the event, or when your function returns (or fails to return) a response.

Function execution errors can be caused by issues with your code, function configuration, downstream resources, or permissions. If you invoke your function directly, you see function errors in the response from Lambda. If you invoke your function asynchronously, with an event source mapping, or through another service, you might find errors in logs, a dead-letter queue, or an on-failure destination. Error handling options and retry behavior vary depending on how you invoke your function and on the type of error.

When your function code or the Lambda runtime return an error, the status code in the response from Lambda is 200 OK. The presence of an error in the response is indicated by a header named `X-Amz-Function-Error`. 400 and 500-series status codes are reserved for [invocation errors](troubleshooting-invocation.md).

**Topics**
+ [Lambda: Remote debugging with Visual Studio Code](#troubleshooting-execution-remote-debugging)
+ [Lambda: Execution takes too long](#troubleshooting-execution-toolong)
+ [Lambda: Unexpected event payload](#troubleshooting-execution-unexpected-payload)
+ [Lambda: Unexpectedly large payload sizes](#troubleshooting-execution-large-payload)
+ [Lambda: JSON encoding and decoding errors](#troubleshooting-execution-json-encoding)
+ [Lambda: Logs or traces don't appear](#troubleshooting-execution-logstraces)
+ [Lambda: Not all of my function's logs appear](#troubleshooting-execution-missinglogs)
+ [Lambda: The function returns before execution finishes](#troubleshooting-execution-unfinished)
+ [Lambda: Running an unintended function version or alias](#unintended-function)
+ [Lambda: Detecting infinite loops](#infinite-loops)
+ [General: Downstream service unavailability](#downstream-unavailability)
+ [AWS SDK: Versions and updates](#troubleshooting-execution-versions)
+ [Python: Libraries load incorrectly](#troubleshooting-execution-libraries)
+ [Java: Your function takes longer to process events after updating to Java 17 from Java 11](#troubleshooting-execution-java-perf)
+ [Kafka: Error handling and retry configuration issues](#troubleshooting-kafka-error-handling)

## Lambda: Remote debugging with Visual Studio Code
<a name="troubleshooting-execution-remote-debugging"></a>

**Issue:** *Difficulty troubleshooting complex Lambda function behavior in the actual AWS environment*

Lambda provides a remote debugging feature through the AWS Toolkit for Visual Studio Code. For set up and general instructions, see [Remotely debug Lambda functions with Visual Studio Code](debugging.md).

For detailed instructions on troubleshooting, advanced use cases, and region availability, see [Remote debugging Lambda functions](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/lambda-remote-debug.html) in the AWS Toolkit for Visual Studio Code User Guide.

## Lambda: Execution takes too long
<a name="troubleshooting-execution-toolong"></a>

**Issue:** *Function execution takes too long.*

If your code takes much longer to run in Lambda than on your local machine, it may be constrained by the memory or processing power available to the function. [Configure the function with additional memory](configuration-memory.md) to increase both memory and CPU.

## Lambda: Unexpected event payload
<a name="troubleshooting-execution-unexpected-payload"></a>

**Issue:** *Function errors related to malformed JSON or inadequate data validation.*

All Lambda functions receive an event payload in the first parameter of the handler. The event payload is a JSON structure that may contain arrays and nested elements.

Malformed JSON can occur when provided by upstream services that do not use a robust process for checking JSON structures. This occurs when services concatenate text strings or embed user input that has not been sanitized. JSON is also frequently serialized for passing between services. Always parse JSON structures both as the producer and consumer of JSON to ensure that the structure is valid.

Similarly, failing to check for ranges of values in the event payload can result in errors. This example shows a function that calculates a tax withholding:

```
exports.handler = async (event) => {
    let pct = event.taxPct
    let salary = event.salary

    // Calculate % of paycheck for taxes
    return (salary * pct)
}
```

This function uses a salary and tax rate from the event payload to perform the calculation. However, the code fails to check if the attributes are present. It also fails to check data types, or ensure boundaries, such as ensuring that the tax percentage is between 0 and 1. As a result, values outside of these bounds produce nonsensical results. An incorrect type or missing attribute causes a runtime error.

Create tests to ensure that your function handles larger payload sizes. The maximum size for a Lambda event payload is 1 MB. Depending upon the content, larger payloads may mean more items passed to the function or more binary data embedded in a JSON attribute. In both cases, this can result in more processing for a Lambda function.

Larger payloads can also cause timeouts. For example, a Lambda function processes one record per 100 ms and has a timeout of 3 seconds. Processing is successful for 0-29 items in the payload. However, once the payload contains more than 30 items, the function times out and throws an error. To avoid this, ensure that timeouts are set to handle the additional processing time for the maximum number of items expected.

## Lambda: Unexpectedly large payload sizes
<a name="troubleshooting-execution-large-payload"></a>

**Issue:** *Functions are timing out or causing errors due to large payloads.*

Larger payloads can cause timeouts and errors. We recommend creating tests to ensure that your function handles your largest expected payloads, and ensuring the function timeout is properly set.

In addition, certain event payloads can contain pointers to other resources. For example, a Lambda function with 128 MB of memory may perform image processing on a JPG file stored as an object in S3. The function works as expected with smaller image files. However, when a larger JPG file is provided as input, the Lambda function throws an error due to running out of memory. To avoid this, the test cases should include examples from the upper bounds of expected data sizes. The code should also validate payload sizes.

## Lambda: JSON encoding and decoding errors
<a name="troubleshooting-execution-json-encoding"></a>

**Issue:** *NoSuchKey exception when parsing JSON inputs.*

Check to ensure you are processing JSON attributes correctly. For example, for events generated by S3, the `s3.object.key` attribute contains a URL encoded object key name. Many functions process this attribute as text to load the referenced S3 object:

**Example**  

```
const originalText = await s3.getObject({
  Bucket: event.Records[0].s3.bucket.name,
  Key: event.Records[0].s3.object.key
}).promise()
```

This code works with the key name `james.jpg` but throws a `NoSuchKey` error when the name is `james beswick.jpg`. Since URL encoding converts spaces and other characters in a key name, you must ensure that functions decode keys before using this data:

**Example**  

```
const originalText = await s3.getObject({
  Bucket: event.Records[0].s3.bucket.name,
  Key: decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, " "))
}).promise()
```

## Lambda: Logs or traces don't appear
<a name="troubleshooting-execution-logstraces"></a>

**Issue:** *Logs don't appear in CloudWatch Logs.*

**Issue:** *Traces don't appear in AWS X-Ray.*

Your function needs permission to call CloudWatch Logs and X-Ray. Update its [execution role](lambda-intro-execution-role.md) to grant it permission. Add the following managed policies to enable logs and tracing.
+ **AWSLambdaBasicExecutionRole**
+ **AWSXRayDaemonWriteAccess**

When you add permissions to your function, perform a trivial update to its code or configuration as well. This forces running instances of your function, which have outdated credentials, to stop and be replaced.

**Note**  
It may take 5 to 10 minutes for logs to show up after a function invocation.

## Lambda: Not all of my function's logs appear
<a name="troubleshooting-execution-missinglogs"></a>

**Issue:** *Function logs are missing in CloudWatch Logs, even though my permissions are correct*

If your AWS account reaches its [CloudWatch Logs quota limits](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/cloudwatch_limits_cwl.html), CloudWatch throttles function logging. When this happens, some of the logs output by your functions may not appear in CloudWatch Logs.

If your function outputs logs at too high a rate for Lambda to process them, this can also cause log outputs not to appear in CloudWatch Logs. When Lambda can't send logs to CloudWatch at the rate your function produces them, it drops logs to prevent the execution of your function from slowing down. Expect to consistently observe dropped logs when your log throughput exceeds 2 MB/s for a single log stream.

If your function is configured to use [JSON formatted logs](monitoring-cloudwatchlogs-logformat.md), Lambda tries to send a [`logsDropped`](telemetry-schema-reference.md#platform-logsDropped) event to CloudWatch Logs when it drops logs. However, when CloudWatch throttles your function's logging, this event might not reach CloudWatch Logs, so you won't always see a record when Lambda drops logs. 

To check if your AWS account has reached its CloudWatch Logs quota limits, do the following:

1. Open the [Service Quotas console](https://console.aws.amazon.com/servicequotas).

1. In the navigation pane, choose **AWS services**.

1. From the **AWS services** list, search for Amazon CloudWatch Logs.

1. In the **Service quotas** list, choose the `CreateLogGroup throttle limit in transactions per second`, `CreateLogStream throttle limit in transactions per second` and `PutLogEvents throttle limit in transactions per second` quotas to view your utilization.

You can also set CloudWatch alarms to alert you when your account utilization exceeds a limit you specify for these quotas. See [Create a CloudWatch alarm based on a static threshold](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ConsoleAlarms.html) to learn more.

If the default quota limits for CloudWatch Logs aren't enough for your use case, you can [request a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).

## Lambda: The function returns before execution finishes
<a name="troubleshooting-execution-unfinished"></a>

**Issue: (Node.js)** *Function returns before code finishes executing*

Many libraries, including the AWS SDK, operate asynchronously. When you make a network call or perform another operation that requires waiting for a response, libraries return an object called a promise that tracks the progress of the operation in the background.

To wait for the promise to resolve into a response, use the `await` keyword. This blocks your handler code from executing until the promise is resolved into an object that contains the response. If you don't need to use the data from the response in your code, you can return the promise directly to the runtime.

Some libraries don't return promises but can be wrapped in code that does. For more information, see [Define Lambda function handler in Node.js](nodejs-handler.md).

## Lambda: Running an unintended function version or alias
<a name="unintended-function"></a>

**Issue:** *Function version or alias not invoked*

When you publish new Lambda functions in the console or using AWS SAM, the latest code version is represented by `$LATEST`. By default, invocations that don't specify a version or alias automatically targets the `$LATEST` version of your function code.

If you use specific function versions or aliases, these are immutable published versions of a function in addition to `$LATEST`. When troubleshooting these functions, first determine that the caller has invoked the intended version or alias. You can do this by checking your function logs. The version of the function that was invoked is always shown in the START log line:

![debugging ops figure 1](http://docs.aws.amazon.com/lambda/latest/dg/images/debugging-ops-figure-1.png)


## Lambda: Detecting infinite loops
<a name="infinite-loops"></a>

**Issue:** *Infinite loop patterns related to Lambda functions*

There are two types of infinite loops in Lambda functions. The first is within the function itself, caused by a loop that never exits. The invocation ends only when the function times out. You can identify these by monitoring timeouts, and then fixing the looping behavior.

The second type of loop is between Lambda functions and other AWS resources. These occur when an event from a resource like an S3 bucket invokes a Lambda function, which then interacts with the same source resource to trigger another event. This invokes the function again, which creates another interaction with the same S3 bucket, and so on. These types of loops can be caused by a number of different AWS event sources, including Amazon SQS queues and DynamoDB tables. You can use [recursive loop detection](invocation-recursion.md) to identify these patterns.

![debugging ops figure 2](http://docs.aws.amazon.com/lambda/latest/dg/images/debugging-ops-figure-2.png)


You can avoid these loops by ensuring that Lambda functions write to resources that are not the same as the consuming resource. If you must publish data back to the consuming resource, ensure that the new data doesn't trigger the same event. Alternatively, use [event filtering](invocation-eventfiltering.md). For example, here are two proposed solutions to infinite loops with S3 and DynamoDB resources:
+ If you write back to the same S3 bucket, use a different prefix or suffix from the event trigger.
+ If you write items to the same DynamoDB table, include an attribute that a consuming Lambda function can filter on. If Lambda finds the attribute, it will not result in another invocation.

## General: Downstream service unavailability
<a name="downstream-unavailability"></a>

**Issue:** *Downstream services that your Lambda function relies on are unavailable*

For Lambda functions that call out to third-party endpoints or other downstream resources, ensure that they can handle service errors and timeouts. These downstream resources can have variable response times, or become unavailable due to service disruptions. Depending upon the implementation, these downstream errors may appear as Lambda timeouts or exceptions if the service’s error response is not handled within the function code.

Anytime a function depends on a downstream service, such as an API call, implement appropriate error handling and retry logic. For critical services, the Lambda function should publish metrics or logs to CloudWatch. For example, if a third-party payment API becomes unavailable, your Lambda function can log this information. You can then set up CloudWatch alarms to send notifications related to these errors.

Since Lambda can scale quickly, non-serverless downstream services may struggle to handle spikes in traffic. There are three common approaches to handling this:
+  **Caching** – Consider caching the result of values returned by third-party services if they don't change frequently. You can store these values in global variable in your function, or another service. For example, the results for a product list query from an Amazon RDS instance could be saved for a period of time within the function to prevent redundant queries.
+  **Queuing** – When saving or updating data, add an Amazon SQS queue between the Lambda function and the resource. The queue durably persists data while the downstream service processes messages.
+  **Proxies** – Where long-lived connections are typically used, such as for Amazon RDS instances, use a proxy layer to pool and reuse those connections. For relational databases, [ Amazon RDS Proxy](https://github.com/aws-samples/s3-to-lambda-patterns/tree/master/docrepository) is a service designed to help improve scalability and resiliency in Lambda-based applications.

## AWS SDK: Versions and updates
<a name="troubleshooting-execution-versions"></a>

**Issue:** *The AWS SDK included on the runtime is not the latest version*

**Issue:** *The AWS SDK included on the runtime updates automatically*

Runtimes for interpreted languages include a version of the AWS SDK. Lambda periodically updates these runtimes to use the latest SDK version. To find the version of the SDK that's included in your runtime, see the following sections:
+ [Runtime included SDK versions (Node.js)](lambda-nodejs.md#nodejs-sdk-included)
+ [Runtime included SDK versions (Python)](lambda-python.md#python-sdk-included)
+ [Runtime included SDK versions (Ruby)](lambda-ruby.md#ruby-sdk-included)

To use a newer version of the AWS SDK, or to lock your functions to a specific version, you can bundle the library with your function code, or [create a Lambda layer](chapter-layers.md). For details on creating a deployment package with dependencies, see the following topics:

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

## Python: Libraries load incorrectly
<a name="troubleshooting-execution-libraries"></a>

**Issue:** (Python) *Some libraries don't load correctly from the deployment package*

Libraries with extension modules written in C or C\+\+ must be compiled in an environment with the same processor architecture as Lambda (Amazon Linux). For more information, see [Working with .zip file archives for Python Lambda functions](python-package.md).

## Java: Your function takes longer to process events after updating to Java 17 from Java 11
<a name="troubleshooting-execution-java-perf"></a>

**Issue:** (Java) *Your function takes longer to process events after updating to Java 17 from Java 11*

Tune your compiler using the `JAVA_TOOL_OPTIONS` parameter. Lambda runtimes for Java 17 and later Java versions change the default compiler options. The change improves cold start times for short-lived functions, but the previous behavior is better suited to computationally intensive, longer-running functions. Set `JAVA_TOOL_OPTIONS` to `-XX:-TieredCompilation` to revert to the Java 11 behavior. For more information about the `JAVA_TOOL_OPTIONS` parameter, see [Understanding the `JAVA_TOOL_OPTIONS` environment variable](java-customization.md#java-tool-options).

## Kafka: Error handling and retry configuration issues
<a name="troubleshooting-kafka-error-handling"></a>

**Issue:** *Kafka event source mapping fails to configure retry settings or on-failure destinations*

Kafka retry configurations and on-failure destinations are only available for event source mappings with provisioned mode enabled. Ensure that you have configured `MinimumPollers` in your `ProvisionedPollerConfig` before attempting to set retry configurations.

Common configuration errors:
+ **Infinite retries with bisect batch** – You cannot enable `BisectBatchOnFunctionError` when `MaximumRetryAttempts` is set to -1 (infinite). Set a finite retry limit or disable bisect batch.
+ **Same topic recursion** – The Kafka on-failure destination topic cannot be the same as any of your source topics. Choose a different topic name for your dead letter topic.
+ **Invalid Kafka destination format** – Use the `kafka://<topic-name>` format when specifying a Kafka topic as an on-failure destination.
+ **kafka:WriteData permission issues** – Ensure your execution role has `kafka-cluster:WriteData` permissions for the destination topic. Topic doesn't exist timeout exceptions or write API throttling issues may require increasing the account limits.