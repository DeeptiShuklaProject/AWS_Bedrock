

# Building Lambda functions with Go
<a name="lambda-golang"></a>

Go is implemented differently than other managed runtimes. Because Go compiles natively to an executable binary, it doesn't require a dedicated language runtime. Use an [OS-only runtime](runtimes-provided.md) (the `provided` runtime family) to deploy Go functions to Lambda.

**Topics**
+ [Go runtime support](#golang-al1)
+ [Tools and libraries](#golang-libraries)
+ [Define Lambda function handlers in Go](golang-handler.md)
+ [Using the Lambda context object to retrieve Go function information](golang-context.md)
+ [Deploy Go Lambda functions with .zip file archives](golang-package.md)
+ [Deploy Go Lambda functions with container images](go-image.md)
+ [Working with layers for Go Lambda functions](golang-layers.md)
+ [Log and monitor Go Lambda functions](golang-logging.md)
+ [Instrumenting Go code in AWS Lambda](golang-tracing.md)

## Go runtime support
<a name="golang-al1"></a>

The Go 1.x managed runtime for Lambda is [deprecated](lambda-runtimes.md#runtime-support-policy). If you have functions that use the Go 1.x runtime, you must migrate your functions to `provided.al2023` or `provided.al2`. The `provided.al2023` and `provided.al2` runtimes offer several advantages over `go1.x`, including support for the arm64 architecture (AWS Graviton2 processors), smaller binaries, and slightly faster invoke times.

No code changes are required for this migration. The only required changes relate to how you build your deployment package and which runtime you use to create your function. For more information, see [Migrating AWS Lambda functions from the Go1.x runtime to the custom runtime on Amazon Linux 2](https://aws.amazon.com/blogs/compute/migrating-aws-lambda-functions-from-the-go1-x-runtime-to-the-custom-runtime-on-amazon-linux-2/) on the *AWS Compute Blog*.


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| OS-only Runtime | `provided.al2023` | Amazon Linux 2023 |  Jun 30, 2029  |  Jul 31, 2029  |  Aug 31, 2029  | 
| OS-only Runtime | `provided.al2` | Amazon Linux 2 |  Jul 31, 2026  |  Feb 1, 2027  |  Mar 3, 2027  | 

## Tools and libraries
<a name="golang-libraries"></a>

Lambda provides the following tools and libraries for the Go runtime:
+ [AWS SDK for Go v2](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2): The official AWS SDK for the Go programming language.
+ [github.com/aws/aws-lambda-go/lambda](https://github.com/aws/aws-lambda-go/tree/master/lambda): The implementation of the Lambda programming model for Go. This package is used by AWS Lambda to invoke your [handler](golang-handler.md).
+ [github.com/aws/aws-lambda-go/lambdacontext](https://github.com/aws/aws-lambda-go/tree/master/lambdacontext): Helpers for accessing context information from the [context object](golang-context.md).
+ [github.com/aws/aws-lambda-go/events](https://github.com/aws/aws-lambda-go/tree/master/events): This library provides type definitions for common event source integrations.
+ [github.com/aws/aws-lambda-go/cmd/build-lambda-zip](https://github.com/aws/aws-lambda-go/tree/master/cmd/build-lambda-zip): This tool can be used to create a .zip file archive on Windows.

For more information, see [aws-lambda-go](https://github.com/aws/aws-lambda-go) on GitHub.

Lambda provides the following sample applications for the Go runtime:

**Sample Lambda applications in Go**
+ [go-al2](https://github.com/aws-samples/sessions-with-aws-sam/tree/master/go-al2) – A hello world function that returns the public IP address. This app uses the `provided.al2` custom runtime.
+ [blank-go](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-go) – A Go function that shows the use of Lambda's Go libraries, logging, environment variables, and the AWS SDK. This app uses the `go1.x` runtime.