# Section 24 – Interview Questions

<a name="sec-24"></a>

### Basic Level
1. **What is AWS Lambda?**
   * *Answer*: AWS Lambda is a serverless compute service that executes code in response to events without provisioning or managing servers.
2. **How does AWS charge for Lambda?**
   * *Answer*: Based on request count (number of executions) and execution duration (in milliseconds) multiplied by the memory allocated.
3. **What is a Cold Start?**
   * *Answer*: The latency overhead when a function is invoked for the first time or after a code update, requiring AWS to initialize a new microVM container runtime environment.
4. **How do you configure the timeout limit for a Lambda function?**
   * *Answer*: Timeout can be configured from 1 second up to 15 minutes in the function settings.
5. **How does Lambda handle high availability?**
   * *Answer*: AWS Lambda runs execution containers across multiple Availability Zones (AZs) by default.
6. **Can Lambda trigger itself recursively?**
   * *Answer*: Yes, but this should be avoided to prevent run-away invocations and high costs. AWS has recursive loop detection enabled by default to throttle such execution loops.
7. **What is Function as a Service (FaaS)?**
   * *Answer*: A cloud computing service category that allows developers to run customer-defined modular code blocks without managing application servers.
8. **What is the maximum deployment zip file size for a Lambda function?**
   * *Answer*: 50 MB zipped, 250 MB unzipped (including dependencies).
9. **Where does Lambda output stdout messages?**
   * *Answer*: To Amazon CloudWatch Logs automatically.
10. **Is AWS Lambda stateful or stateless?**
    * *Answer*: Stateless. Each execution container can be destroyed and recreated dynamically by the system.

### Intermediate Level
11. **How do you handle secrets or API keys in Lambda?**
    * *Answer*: Store them securely in AWS Secrets Manager or Systems Manager Parameter Store and retrieve them programmatically.
12. **What is a Lambda Layer?**
    * *Answer*: A zip archive containing libraries, dependencies, or custom runtimes that can be shared across multiple Lambda functions.
13. **How do you run a Lambda function inside a VPC?**
    * *Answer*: Configure the function to associate with target VPC subnet IDs and security group IDs.
14. **How does a Lambda function inside a private VPC access the internet?**
    * *Answer*: It must route outbound traffic through a NAT Gateway positioned in a public subnet of that VPC.
15. **What is the maximum size for `/tmp` storage?**
    * *Answer*: Configurable from 512 MB up to 10 GB.
16. **How does Lambda scale concurrently?**
    * *Answer*: By spinning up multiple concurrent execution containers in response to incoming traffic spikes.
17. **What is the maximum timeout limit for an API Gateway request proxying to Lambda?**
    * *Answer*: 29 seconds.
18. **What is Provisioned Concurrency?**
    * *Answer*: A feature that pre-warms a specified number of execution environments to eliminate cold start latency for latency-sensitive applications.
19. **How do you handle SQS message retries with Lambda?**
    * *Answer*: Configure SQS visibility timeout to be at least 6 times the function's timeout, and use a Dead Letter Queue (DLQ) to capture failed messages after a specified number of retries.
20. **What is the difference between execution role and resource-based policy?**
    * *Answer*: Execution roles authorize the Lambda function to access other AWS services, while resource-based policies authorize other services (e.g., S3) to invoke the Lambda function.

### Advanced Level
21. **How do you optimize Lambda cost and performance?**
    * *Answer*: Allocate appropriate memory sizes. Since CPU scales proportionally with memory, allocating more memory can decrease execution time and lower overall cost.
22. **What is Event Source Mapping (ESM)?**
    * *Answer*: An AWS service feature that polls stream or queue sources (like SQS, Kinesis, DynamoDB Streams) and invokes your Lambda function with batches of records.
23. **How does concurrency limits affect other functions in the same AWS region?**
    * *Answer*: By default, all functions in an account share a regional concurrency pool (usually 1,000). A single high-traffic function can consume the entire pool and throttle other functions unless **Reserved Concurrency** is configured.
24. **How do you implement canary deployments with Lambda?**
    * *Answer*: Use Lambda **Aliases** and route a percentage of traffic (e.g., 10%) to the new version using AWS CodeDeploy.
25. **What is a Firecracker MicroVM?**
    * *Answer*: An open-source virtualization technology built by AWS that uses Linux Kernel-based Virtual Machines (KVM) to spin up lightweight execution environments.
26. **What happens to global variables in Python Lambda code between executions?**
    * *Answer*: They are preserved during warm starts as the container is reused, but reset when the execution environment is destroyed.
27. **What is the difference between synchronous and asynchronous invocation?**
    * *Answer*: In synchronous invocation, the client waits for the function's response. In asynchronous invocation, Lambda places the event in a queue and returns a 202 Accepted status immediately, processing the task in the background.
28. **How does AWS X-Ray help in troubleshooting Lambda?**
    * *Answer*: X-Ray traces execution paths across AWS services, helping you identify latency bottlenecks and errors in downstream databases or APIs.
29. **What are the best practices for connecting Lambda to RDS databases?**
    * *Answer*: Use **Amazon RDS Proxy** to manage database connection pools and prevent Lambda from exhausting database connection limits during traffic spikes.
30. **How does Lambda handle failures during asynchronous invocation?**
    * *Answer*: Lambda retries the invocation up to 2 times automatically, with backoff delays, before discarding the event or sending it to a configured Dead Letter Queue (DLQ).

### Scenario-Based
31. **An S3 bucket trigger executes Lambda. The function processes the file, saves it back to the same bucket, and loops infinitely. How do you resolve this?**
    * *Answer*: Use prefix filtering (e.g., only trigger on uploads to `incoming/`) or save processed output files to a separate destination S3 bucket.
32. **Your Lambda functions are being throttled. What steps do you take?**
    * *Answer*: Check if the regional concurrency limit has been reached, request an AWS service quota increase, or allocate **Reserved Concurrency** to protect critical functions.
33. **A database query inside your function works locally but times out in production. What is the issue?**
    * *Answer*: Verify security group rules, network routing tables, and ensure database subnet routes match your Lambda VPC settings.
34. **You need to use a compiled C library in your Python code. How do you deploy it?**
    * *Answer*: Compile the library in an AWS-compatible environment (such as Amazon Linux 2023) and package it as a Lambda Layer.
35. **Your Lambda function takes 2 minutes to initialize but only 50ms to run. How do you optimize this?**
    * *Answer*: Use **Provisioned Concurrency** to pre-warm the execution environments and reduce startup latency for clients.
36. **Your function reads from SQS. You notice some messages are processed twice. Why?**
    * *Answer*: The SQS visibility timeout may be too short, causing other consumers to see and process the message before the first invocation completes. Ensure the visibility timeout is at least 6 times your function's timeout.
37. **A function triggers on DynamoDB Streams. One corrupted record blocks processing for all subsequent items. How do you resolve this?**
    * *Answer*: Enable **SplitBatchOnError** and set **MaximumRecordAgeInSeconds** or **MaximumRetryAttempts** in the Event Source Mapping settings.
38. **A third-party API API requests inside a Lambda function are slow. How do you prevent timeouts?**
    * *Answer*: Set appropriate connection and request timeouts on the HTTP client library in your code, catch timeout errors gracefully, and return user-friendly responses.
39. **How do you securely share custom utility libraries across 20 different Lambda functions?**
    * *Answer*: Build and deploy a central **Lambda Layer** containing the common code libraries and attach it to the 20 functions.
40. **How do you monitor cost metrics for individual Lambda functions?**
    * *Answer*: Apply resource **Tags** (e.g., `Project=Billing`) to the functions and monitor costs using AWS Cost Explorer with tag-based filters.

---
