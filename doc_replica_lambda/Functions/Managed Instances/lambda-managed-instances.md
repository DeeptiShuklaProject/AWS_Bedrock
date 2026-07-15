

# Lambda Managed Instances
<a name="lambda-managed-instances"></a>

Lambda Managed Instances enables you to run Lambda functions on your current-generation Amazon EC2 instances, including Graviton4, network-optimized instances, and other specialized compute options, without managing instance lifecycles, operating system and language runtime patching, routing, load balancing, or scaling policies. With Lambda Managed Instances, you benefit from EC2 pricing advantages, including EC2 Savings Plans and Reserved Instances.

For a list of supported instance types, go to the [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/#:~:text=EPU%20pricing%20applies.-,Management%20Fees,-Pricing%20Example%3A%20High) page and select your AWS Region.

## Key capabilities
<a name="lambda-managed-instances-key-capabilities"></a>

Lambda Managed Instances provides the following capabilities:
+ **Choose suitable instances** - Select [appropriate instances](https://aws.amazon.com/lambda/pricing/#:~:text=EPU%20pricing%20applies.-,Management%20Fees,-Pricing%20Example%3A%20High) based on performance and cost requirements, including access to the latest CPUs like Graviton4, configurable memory-CPU ratios, and high-bandwidth networking.
+ **Automatic provisioning** - AWS automatically provisions suitable instances and spins up function execution environments.
+ **Dynamic scaling** - Instances scale dynamically based on your function traffic patterns.
+ **Fully managed experience** - AWS handles infrastructure management, scaling, patching, and routing, with the same extensive event-source integrations you're familiar with.

## When to use Lambda Managed Instances
<a name="lambda-managed-instances-when-to-use"></a>

Consider Lambda Managed Instances for the following use cases:
+ **High volume-predictable workloads** - Ideal for steady-state workloads without unexpected traffic spikes. Lambda Managed Instances scale to handle traffic doubling within five minutes by default.
+ **Performance-critical applications** - Access to latest CPUs, varying memory-CPU ratios, and high network throughput
+ **Regulatory requirements** - Granular governance needs with control over VPC and instance placement
+ **Variety of applications** - Event-driven applications, media/data processing, web applications, and legacy workloads migrating to serverless

## How it works
<a name="lambda-managed-instances-how-it-works"></a>

Lambda Managed Instances uses capacity providers as the foundation for running your functions:

1. **Create a capacity provider** - Define where your functions run by specifying VPC configuration and optionally, instance requirements, and scaling configuration

1. **Create your function** - Create Lambda functions as usual and attach them to a capacity provider

1. **Publish a function version** - Function versions become active on capacity provider instances once published

When you publish a function version with a capacity provider, Lambda launches Managed Instances in your account. It launches three instances by default for AZ resiliency and starts three execution environments before marking your function version ACTIVE. If you attach a function to an existing capacity provider that is already running other functions, Lambda may not spin up new instances if the available instances already have capacity to accommodate the new function's execution environments.

## Concurrency model
<a name="lambda-managed-instances-concurrency-model"></a>

Lambda Managed Instances support multi-concurrent invocations, where one execution environment can handle multiple invocations at the same time. This differs from the Lambda (default) compute type, which provides a single concurrency model where one execution environment can run a maximum of one invoke at a time. Multi-concurrency yields better utilization of your underlying EC2 instances and is especially beneficial for IO-heavy applications like web services or batch jobs. This change in execution model means that thread safety, state management, and context isolation must be handled differently depending on the runtime.

## Tenancy and isolation
<a name="lambda-managed-instances-tenancy-isolation"></a>

Lambda (default) compute type is multi-tenant, making use of Firecracker MicroVM technology to provide isolation between execution environments running on shared Lambda fleets. Lambda Managed Instances run in your account, providing the latest EC2 hardware and pricing options. Managed Instances use containers running on EC2 Nitro instances to provide isolation rather than Firecracker. Capacity providers serve as the security boundary for Lambda functions. Functions execute in containers within instances.

### Understanding managed instances
<a name="lambda-managed-instances-understanding"></a>

Lambda Managed Instances functions run on [EC2 managed instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-managed-instances.html) in your account. These instances are fully managed by Lambda, which means you have restricted permissions on them compared to standard EC2 instances. You can identify Lambda Managed Instances in your account by:
+ The presence of the `Operator` field in EC2 `DescribeInstances` output
+ The `aws:lambda:capacity-provider` tag on the instance

You cannot perform standard EC2 operations directly on these instances, such as terminating them manually. To destroy managed instances, delete the associated capacity provider. Lambda will then terminate the instances as part of the capacity provider deletion process.

Managed instances are hidden from your EC2 console views and API list operations by default. You can adjust the visibility using the [managed resource visibility setting](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-managed-instances.html#managed-resource-visibility-settings). Managed instances remain fully operational and billable in your AWS account.

## Pricing
<a name="lambda-managed-instances-pricing"></a>

Lambda Managed Instances uses EC2-based pricing with a 15% management fee on top of the EC2 instance cost. This pricing model supports EC2 Savings Plans, Reserved Instances and any other pricing discounts applied to your EC2 usage. Refer to pricing page for additional details: [https://aws.amazon.com/lambda/pricing/](https://aws.amazon.com/lambda/pricing/)

To compare the cost of running your functions on Lambda default, Lambda Managed Instances, and self-managed Amazon EC2, use the [Lambda Managed Instances pricing calculator](https://aws-samples.github.io/sample-aws-lambda-managed-instances/).

**Important:** EC2 pricing discounts only apply to the underlying EC2 compute, not to the management fee.

## How Lambda Managed Instances differs from the Lambda (default) compute type
<a name="lambda-managed-instances-comparison"></a>

Lambda Managed Instances changes how Lambda processes requests compared to Lambda (default).

**Key differences:**


|  | Lambda (default) | Lambda Managed Instances | 
| --- | --- | --- | 
| Concurrency model | Single concurrency model where one execution environment can support a maximum of one invocation at a time | Multi-concurrent invocations where one execution environment can handle multiple invocations simultaneously, increasing throughput especially for IO-heavy applications | 
| Tenancy and isolation | Multi-tenant, using Firecracker MicroVM technology to provide isolation between execution environments running on shared Lambda fleets | Run in your account, using EC2 Nitro to provide isolation. Capacity providers serve as the security boundary, with functions executing in containers within instances | 
| Pricing model | Per-request duration pricing | Instance-based pricing with EC2 pricing models, including On-Demand and Reserved Instances, and savings options such as Compute Savings Plans | 
| Scaling behavior | Scales when there is no free execution environment to handle an incoming invocation (cold start). Scales to zero without traffic | Scales asynchronously based on CPU resource utilization only, without cold starts. Scales to minimum execution environments configured without traffic | 
| Best suited for | Functions with bursty traffic that can handle some cold-start time, or applications without sustained load that benefit from scale to zero | High volume predictable traffic functions when you want the flexibility, pricing plans, and hardware options of EC2 | 

## Next steps
<a name="lambda-managed-instances-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)
+ Configure [VPC connectivity for your capacity providers](lambda-managed-instances-networking.md)
+ Understand [security and permissions for Lambda Managed Instances](lambda-managed-instances-security.md)