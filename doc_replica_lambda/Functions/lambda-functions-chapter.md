

# AWS Lambda Functions
<a name="lambda-functions-chapter"></a>

**Tip**  
Join Serverless experts for free hands-on workshops to learn how to build Serverless applications with best practices. [Click here](https://aws-experience.com/amer/smb/events/series/Get-Hands-On-With-Serverless?trk=188abe3e-9f94-4e84-aefb-398d944ad567%26sc_channel%3Del) to sign up.

AWS Lambda is a compute service that runs code without the need to manage servers. Your code runs, scaling up and down automatically, with pay-per-use pricing. To get started, see [Create your first function](getting-started.md).

You can use Lambda for:
+ **File processing**: Process files automatically when uploaded to Amazon Simple Storage Service. See [file processing examples](example-apps.md#examples-apps-file) for details.
+ **Long-running workflows:** Use [durable Lambda functions](durable-functions.md) to build stateful, multi-step workflows that can run for up to one year. Perfect for order processing, approval workflows, human-in-the-loop processes, and complex data pipelines that need to remember their progress.
+ **Database operations and integration examples**: Respond to database changes and automate data workflows. See [database examples](example-apps.md#examples-apps-database) for details.
+ **Scheduled and periodic tasks**: Run automated operations on a regular schedule using EventBridge. See [scheduled task examples](example-apps.md#examples-apps-scheduled) for details.
+ **Stream processing**: Process real-time data streams for analytics and monitoring. See [Kinesis Data Streams](with-kinesis.md) for details.
+ **Web applications**: Build scalable web apps that automatically adjust to demand.
+ **Mobile backends**: Create secure API backends for mobile and web applications.
+ **IoT backends**: Handle web, mobile, IoT, and third-party API requests. See [IoT](services-iot.md) for details.

For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/).

## Functions and durable functions
<a name="whatis-function-types"></a>

[Lambda functions](#lambda-functions-chapter) run for up to 15 minutes and are ideal for event-driven tasks like processing API requests, handling file uploads, or responding to database changes. [Durable functions](durable-functions.md) extend this model for workloads that need to run longer and survive interruptions. They can execute for up to one year, automatically checkpointing their progress so they resume reliably after failures. Use durable functions when you need multi-step workflows, human-in-the-loop approvals, or coordination across services over extended periods.

## How Lambda works
<a name="how-lambda-works"></a>

When using Lambda, you are responsible only for your code. Lambda runs your code on a high-availability compute infrastructure and manages all the computing resources, including server and operating system maintenance, capacity provisioning, automatic scaling, and logging.

Because Lambda is a serverless, event-driven compute service, it uses a different programming paradigm than traditional web applications. The following model illustrates how Lambda works:

1. You write and organize your code in [Lambda functions](concepts-basics.md#gettingstarted-concepts-function), which are the basic building blocks you use to create a Lambda application.

1. You control security and access through [Lambda permissions](lambda-permissions.md), using [execution roles](lambda-intro-execution-role.md) to manage what AWS services your functions can interact with and what resource policies can interact with your code.

1. Event sources and AWS services [trigger](concepts-event-driven-architectures.md) your Lambda functions, passing event data in JSON format, which your functions process (this includes event source mappings).

1. [Lambda runs your code](concepts-how-lambda-runs-code.md) with language-specific runtimes (like Node.js and Python) in execution environments that package your runtime, layers, and extensions.

**Tip**  
To learn how to build **serverless solutions**, check out the [Serverless Developer Guide](https://docs.aws.amazon.com/serverless/latest/devguide/).

## Key features
<a name="features"></a>

**Configure, control, and deploy secure applications:**
+ [Environment variables](configuration-envvars.md) modify application behavior without new code deployments.
+ [Versions](configuration-versions.md) safely test new features while maintaining stable production environments.
+ [Layers](chapter-layers.md) optimize code reuse and maintenance by sharing common components across multiple functions.
+ [Code signing](configuration-codesigning.md) enforce security compliance by ensuring only approved code reaches production systems.

**Scale and perform reliably:**
+ [Concurrency and scaling controls](lambda-concurrency.md) precisely manage application responsiveness and resource utilization during traffic spikes.
+ [SnapStart](snapstart.md) significantly reduce cold start times. Lambda SnapStart can provide as low as sub-second startup performance, typically with no changes to your function code.
+ [Response streaming](configuration-response-streaming.md) optimize function performance by delivering large payloads incrementally for real-time processing.
+ [Container images](images-create.md) package functions with complex dependencies using container workflows.

**Connect and integrate seamlessly:**
+ [VPC networks](configuration-vpc.md) secure sensitive resources and internal services.
+ [File systems](configuration-filesystem.md) integration that shares persistent data and manage stateful operations across function invocations.
+ [Function URLs](urls-configuration.md) create public-facing APIs and endpoints without additional services.
+ [Extensions](lambda-extensions.md) augment functions with monitoring, security, and operational tools.

## Related information
<a name="what-is-lambda-moreinfo"></a>
+ For information on how Lambda works, see [How Lambda works](concepts-basics.md).
+ To start using Lambda, see [Create your first Lambda function](getting-started.md).
+ For a list of example applications, see [Getting started with example applications and patterns](example-apps.md).

## Security in AWS Lambda
<a name="lambda-security"></a>

Cloud security at AWS is the highest priority. As an AWS customer, you benefit from a data center and network architecture that is built to meet the requirements of the most security-sensitive organizations.

Security is a shared responsibility between AWS and you. The [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) describes this as security *of* the cloud and security *in* the cloud:
+ **Security of the cloud** – AWS is responsible for protecting the infrastructure that runs AWS services in the AWS Cloud. AWS also provides you with services that you can use securely. Third-party auditors regularly test and verify the effectiveness of our security as part of the [AWS compliance programs](https://aws.amazon.com/compliance/programs/). To learn about the compliance programs that apply to AWS Lambda, see [AWS services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/).
+ **Security in the cloud** – Your responsibility is determined by the AWS service that you use. You are also responsible for other factors including the sensitivity of your data, your company’s requirements, and applicable laws and regulations. 

This documentation helps you understand how to apply the shared responsibility model when using Lambda. The following topics show you how to configure Lambda to meet your security and compliance objectives. You also learn how to use other AWS services that help you to monitor and secure your Lambda resources.

For more information about applying security principles to Lambda applications, see [Security](https://serverlessland.com/content/service/lambda/guides/aws-lambda-operator-guide/security-ops) in Serverless Land.

**Topics**
+ [Data protection in AWS Lambda](security-dataprotection.md)
+ [Using service-linked roles for Lambda](using-service-linked-roles.md)
+ [Identity and Access Management for AWS Lambda](security-iam.md)
+ [Create a governance strategy for Lambda functions and layers](governance-concepts.md)
+ [Compliance validation for AWS Lambda](security-compliance.md)
+ [Resilience in AWS Lambda](security-resilience.md)
+ [Infrastructure security in AWS Lambda](security-infrastructure.md)
+ [Securing workloads with public endpoints](security-public-endpoints.md)
+ [Using code signing to verify code integrity with Lambda](configuration-codesigning.md)