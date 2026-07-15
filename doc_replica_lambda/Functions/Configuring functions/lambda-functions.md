

# Configuring AWS Lambda functions
<a name="lambda-functions"></a>

Learn how to configure the core capabilities and options for your Lambda function using the Lambda API or console.

**[.zip file archives](configuration-function-zip.md) **  
Create a Lambda function deployment package when you want to include dependencies, custom runtime layers, or any files beyond your function code. The deployment package is a .zip file archive containing your function code and dependencies.

**[Container images](images-create.md) **  
Use container images to package your function code and dependencies when you need more control over the build process, or if your function requires custom runtime configurations. You can build, test, and deploy Lambda functions as container images using tools like Docker CLI.

**[Self-managed S3 code storage](configuration-self-managed-storage.md) **  
Configure your functions and layers to use your own S3 bucket for code storage. Lambda references your code directly from your S3 bucket, eliminating Lambda-managed storage limits and reducing time to first invoke.

**[Memory](configuration-memory.md)**  
Learn how and when to increase function memory.

**[Ephemeral storage](configuration-ephemeral-storage.md) **  
Learn how and when to increase your function's temporary storage capacity.

**[Timeout](configuration-timeout.md) **  
Learn how and when to increase your function's timeout value.

** [ Environment variables](configuration-envvars.md)**  
You can make your function code portable and keep secrets out of your code by storing them in your function's configuration by using environment variables.

**[Outbound networking](configuration-vpc.md) **  
 You can use your Lambda function with AWS resources in an Amazon VPC. Connecting your function to a VPC lets you access resources in a private subnet such as relational databases and caches.

** [Inbound networking](configuration-vpc-endpoints.md)**  
You can use an interface VPC endpoint to invoke your Lambda functions without crossing the public internet.

**[File system](configuration-filesystem.md)**  
 You can use your Lambda function to mount a Amazon EFS to a local directory. A file system allows your function code to access and modify shared resources safely and at high concurrency.

**[Aliases](configuration-aliases.md)**  
You can configure your clients to invoke a specific Lambda function version by using an alias, instead of updating the client.

**[Versions](configuration-versions.md)**  
By publishing a version of your function, you can store your code and configuration as a separate resource that cannot be changed.

**[Tags](configuration-tags.md)**  
Use tags to enable attribute-based access control (ABAC), to organize your Lambda functions, and to filter and generate reports on your functions using the AWS Cost Explorer or AWS Billing and Cost Management services.

**[Response streaming](configuration-response-streaming.md)**  
You can configure your Lambda function URLs to stream response payloads back to clients. Response streaming can benefit latency sensitive applications by improving time to first byte (TTFB) performance. This is because you can send partial responses back to the client as they become available. Additionally, you can use response streaming to build functions that return larger payloads.

**[Metadata endpoint](configuration-metadata-endpoint.md)**  
Use the Lambda metadata endpoint to discover which Availability Zone your function is running in, enabling you to optimize latency by routing to same-AZ resources and to implement AZ-aware resilience patterns.