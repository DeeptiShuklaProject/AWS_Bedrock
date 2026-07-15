

# What is AWS Lambda?
<a name="welcome"></a>

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. Lambda automatically manages the underlying infrastructure – including server maintenance, capacity provisioning, scaling, and patching – so you can focus on your application logic.

Lambda provides two compute primitives, each designed for different workload patterns:
+ **[Lambda Functions](lambda-functions-chapter.md)** – Run code in response to events or API calls without managing servers. You write a handler function, connect it to a trigger (API Gateway, Amazon S3, Amazon SQS, EventBridge, and 200\+ other AWS services), and Lambda executes it. Each invocation runs independently with no shared state, scaling horizontally to match demand. Lambda manages execution environments, scaling, routing, and fault tolerance.
+ **[Lambda MicroVMs](lambda-microvms-guide.md)** – Isolated compute environments with near-instant startup and state retention for up to 8 hours. Designed for workloads needing a dedicated compute environment for each individual user or job. Lambda manages isolation, capacity, and networking. Your application uses Lambda MicroVMs APIs and HTTPS endpoints to connect each user/job to their compute environment.

For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/).

## How Lambda Functions and Lambda MicroVMs compare
<a name="lambda-comparison"></a>

Lambda Functions and Lambda MicroVMs share a common serverless foundation:
+ **No server management** – AWS manages underlying infrastructure, instance patching, and capacity.
+ **Pay-per-use billing** – No upfront commitments. You pay only for the resources used.
+ **Managed networking** – Both provide service-managed inbound and outbound network access.
+ **Firecracker virtualization** – VM-level isolation between workloads.

While they share this foundation, they serve different use cases:


|  | **[Lambda Functions](lambda-functions-chapter.md)** | **[Lambda MicroVMs](lambda-microvms-guide.md)** | 
| --- | --- | --- | 
| Best for | Request-response or event-driven workloads (APIs, data processing, automation) | Persistent environments running user or AI-produced untrusted code | 
| Programming model | Function handler invoked in a supported runtime | Any application – run your own binaries, listen on ports, use Linux OS capabilities | 
| Duration | Up to 15 minutes per invocation; multi-step workflows lasting up to a year with Lambda Durable Functions | Up to 8 hours per session; suspend and resume across sessions | 
| Runtime environment | Service-provided language runtimes; support for customer-provided runtimes | Customer-provided MicroVM images | 
| Inbound Networking | Direct invocations or event-source integrations with AWS services; support for response streaming | Inbound access to any port using OSI Layer 7 protocols | 
| Concurrency | One request per execution environment at a time | Multiple concurrent connections per MicroVM | 
| Environment State | Execution environments may be reused (warm starts), but state may not persist across invocations | Memory and disk state preserved on suspend; restored on resume | 
| Scaling | Automatic – Lambda creates and destroys execution environments in response to traffic | Developer-controlled – you create, suspend, resume, and terminate MicroVMs via API | 
| Lifecycle | Fully managed by Lambda | Developer-controlled; optional idle policies for automatic suspend-resume | 
| Pricing | Per-request \+ GB-seconds of execution time | Per-second of compute while running \+ snapshot storage while suspended | 