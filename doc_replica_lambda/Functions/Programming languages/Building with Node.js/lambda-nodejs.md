

# Building Lambda functions with Node.js
<a name="lambda-nodejs"></a>

You can run JavaScript code with Node.js in AWS Lambda. Lambda provides [runtimes](lambda-runtimes.md) for Node.js that run your code to process events. Your code runs in an environment that includes the AWS SDK for JavaScript, with credentials from an AWS Identity and Access Management (IAM) role that you manage. To learn more about the SDK versions included with the Node.js runtimes, see [Runtime-included SDK versions](#nodejs-sdk-included).

Lambda supports the following Node.js runtimes.<a name="nodejs-supported-runtimes"></a>


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| Node.js 24 | `nodejs24.x` | Amazon Linux 2023 |  Apr 30, 2028  |  Jun 1, 2028  |  Jul 1, 2028  | 
| Node.js 22 | `nodejs22.x` | Amazon Linux 2023 |  Apr 30, 2027  |  Jun 1, 2027  |  Jul 1, 2027  | 

**To create a Node.js function**

1. Open the [Lambda console](https://console.aws.amazon.com/lambda).

1. Choose **Create function**.

1. Configure the following settings:
   + **Function name**: Enter a name for the function.
   + **Runtime**: Choose **Node.js 24.x**.

1. Choose **Create function**.

The console creates a Lambda function with a single source file named `index.mjs`. You can edit this file and add more files in the built-in code editor. In the **DEPLOY** section, choose **Deploy** to update your function's code. Then, to run your code, choose **Create test event** in the **TEST EVENTS** section.

The `index.mjs` file exports a function named `handler` that takes an event object and a context object. This is the [handler function](nodejs-handler.md) that Lambda calls when the function is invoked. The Node.js function runtime gets invocation events from Lambda and passes them to the handler. In the function configuration, the handler value is `index.handler`.

When you save your function code, the Lambda console creates a .zip file archive deployment package. When you develop your function code outside of the console (using an IDE) you need to [create a deployment package](nodejs-package.md) to upload your code to the Lambda function.

The function runtime passes a context object to the handler, in addition to the invocation event. The [context object](nodejs-context.md) contains additional information about the invocation, the function, and the execution environment. More information is available from environment variables.

Your Lambda function comes with a CloudWatch Logs log group. The function runtime sends details about each invocation to CloudWatch Logs. It relays any [logs that your function outputs](nodejs-logging.md) during invocation. If your function returns an error, Lambda formats the error and returns it to the invoker.

**Topics**
+ [Runtime-included SDK versions](#nodejs-sdk-included)
+ [Using keep-alive for TCP connections](#nodejs-keep-alive)
+ [CA certificate loading](#nodejs-certificate-loading)
+ [Experimental Node.js features](#nodejs-experimental-features)
+ [Define Lambda function handler in Node.js](nodejs-handler.md)
+ [Deploy Node.js Lambda functions with .zip file archives](nodejs-package.md)
+ [Deploy Node.js Lambda functions with container images](nodejs-image.md)
+ [Working with layers for Node.js Lambda functions](nodejs-layers.md)
+ [Using the Lambda context object to retrieve Node.js function information](nodejs-context.md)
+ [Log and monitor Node.js Lambda functions](nodejs-logging.md)
+ [Instrumenting Node.js code in AWS Lambda](nodejs-tracing.md)

## Runtime-included SDK versions
<a name="nodejs-sdk-included"></a>

All [supported Lambda Node.js runtimes](#nodejs-supported-runtimes) include a specific minor version of the AWS SDK for JavaScript v3, not the [latest version](https://github.com/aws/aws-sdk-js-v3/releases). The specific minor version that's included in the runtime depends on the runtime version and your AWS Region. To find the specific version of the SDK included in the runtime that you're using, create a Lambda function with the following code.

**Example index.mjs**  

```
import packageJson from '@aws-sdk/client-s3/package.json' with { type: 'json' };

export const handler = async () => ({ version: packageJson.version });
```
This returns a response in the following format:  

```
{
  "version": "3.632.0"
}
```

For more information, see [Using the SDK for JavaScript v3 in your handler](nodejs-handler.md#nodejs-example-sdk-usage).

## Using keep-alive for TCP connections
<a name="nodejs-keep-alive"></a>

The default Node.js HTTP/HTTPS agent creates a new TCP connection for every new request. To avoid the cost of establishing new connections, keep-alive is enabled by default in all [supported Node.js runtimes](#nodejs-supported-runtimes). Keep-alive can reduce request times for Lambda functions that make multiple API calls using the SDK.

To disable keep-alive, see [Reusing connections with keep-alive in Node.js](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/node-reusing-connections.html) in the *AWS SDK for JavaScript 3.x Developer Guide*. For more information about using keep-alive, see [HTTP keep-alive is on by default in modular AWS SDK for JavaScript](https://aws.amazon.com/blogs/developer/http-keep-alive-is-on-by-default-in-modular-aws-sdk-for-javascript/) on the AWS Developer Tools Blog.

## CA certificate loading
<a name="nodejs-certificate-loading"></a>

For Node.js runtime versions up to Node.js 18, Lambda automatically loads Amazon-specific CA (certificate authority) certificates to make it easier for you to create functions that interact with other AWS services. For example, Lambda includes the Amazon RDS certificates necessary for validating the [server identity certificate](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html) installed on your Amazon RDS database. This behavior can have a performance impact during cold starts.

Starting with Node.js 20, Lambda no longer loads additional CA certificates by default. The Node.js 20 runtime contains a certificate file with all Amazon CA certificates located at `/var/runtime/ca-cert.pem`. To restore the same behavior from Node.js 18 and earlier runtimes, set the `NODE_EXTRA_CA_CERTS` [environment variable](configuration-envvars.md) to `/var/runtime/ca-cert.pem`.

For optimal performance, we recommend bundling only the certificates that you need with your deployment package and loading them via the `NODE_EXTRA_CA_CERTS` environment variable. The certificates file should consist of one or more trusted root or intermediate CA certificates in PEM format. For example, for RDS, include the required certificates alongside your code as `certificates/rds.pem`. Then, load the certificates by setting `NODE_EXTRA_CA_CERTS` to `/var/task/certificates/rds.pem`.

## Experimental Node.js features
<a name="nodejs-experimental-features"></a>

The upstream Node.js language releases enable some experimental features by default. Lambda disables these features to ensure runtime stability and consistent performance. The following table lists the experimental features that Lambda disables.


| Experimental feature | Supported Node.js versions | Node.js flag applied by Lambda | Lambda flag to re-enable | 
| --- | --- | --- | --- | 
| Support for importing modules using require in ES modules | Node.js 20, Node.js 22, Node.js 24 | `--no-experimental-require-module` | `--experimental-require-module` | 
| Support for automatically detecting ES vs CommonJS modules | Node.js 22, Node.js 24 | `--no-experimental-detect-module` | `--experimental-detect-module` | 

To enable a disabled experimental feature, set the re-enable flag in the `NODE_OPTIONS` environment variable. For example, to enable ES module require support, set `NODE_OPTIONS` to `--experimental-require-module`. Lambda detects this override and removes the corresponding disable flag.

**Important**  
 Using experimental features can lead to instability and performance issues. These features might be changed or removed in future Node.js versions. Functions that use experimental features aren't eligible for the Lambda Service Level Agreement (SLA) or AWS Support.