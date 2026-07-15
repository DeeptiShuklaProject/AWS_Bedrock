

# Lambda durable functions
<a name="durable-functions"></a>

With AWS Lambda durable functions, you can build resilient multi-step applications and AI workflows that can execute for up to one year while maintaining reliable progress despite interruptions. When a durable function runs, this complete lifecycle is called a durable execution, which uses checkpoints to track progress and automatically recover from failures through replay, re-executing from the beginning while skipping completed work.

Within each function, you use durable operations as fundamental building blocks. Steps execute business logic with built-in retries and progress tracking, while waits suspend execution without incurring compute charges, making them ideal for long-running processes like human-in-the-loop workflows or polling external dependencies. Whether you're processing orders, coordinating microservices, or orchestrating agentic AI applications, durable functions maintain state automatically and recover from failures while you write code in familiar programming languages.

**Note**  
This guide covers Lambda service topics such as deployment, configuration, permissions, invocation, monitoring, and quotas. For SDK programming reference, quickstart tutorials, and language-specific guides, see the [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/).

## Key benefits
<a name="durable-functions-benefits"></a>

**Write resilient code naturally:** With familiar programming constructs, you write code that handles failures automatically. Built-in checkpointing, transparent retries, and automatic recovery mean your business logic stays clean and focused.

**Pay only for what you use:** During wait operations, your function suspends without incurring compute charges. For long-running workflows that wait hours or days, you pay only for actual processing time, not idle waiting.

**Operational simplicity:** With Lambda's serverless model, you get automatic scaling, including scale-to-zero, without managing infrastructure. Durable functions handle state management, retry logic, and failure recovery automatically, reducing operational overhead.

## When to use durable functions
<a name="durable-functions-use-cases"></a>

**Short-lived coordination:** Coordinate payments, inventory, and shipping across multiple services with automatic rollback on failures. Process orders through validation, payment authorization, inventory allocation, and fulfillment with guaranteed completion.

**Process payments with confidence:** Build resilient payment flows that maintain transaction state through failures and handle retries automatically. Coordinate multi-step authorization, fraud checks, and settlement across payment providers with full auditability across steps.

**Build reliable AI workflows:** Create multi-step AI workflows that chain model calls, incorporate human feedback, and handle long-running tasks deterministically during failures. Automatically resume after suspension, and only pay for active execution time.

**Orchestrate complex order fulfillment:** Coordinate order processing across inventory, payment, shipping, and notification systems with built-in resilience. Automatically handle partial failures, preserve order state despite interruptions, and efficiently wait for external events without consuming compute resources.

**Automate multi-step business workflows:** Build reliable workflows for employee onboarding, loan approvals, and compliance processes that span days or weeks. Maintain workflow state across human approvals, system integrations, and scheduled tasks while providing full visibility into process status and history.

### How durable functions compare to Step Functions
<a name="durable-functions-vs-step-functions"></a>

Both durable functions and Step Functions provide workflow orchestration with automatic state management. The key differences are where they run and how you define workflows:
+ **Durable functions:** Run within Lambda, use standard programming languages, managed within Lambda environment
+ **Step Functions:** Standalone service, graph-based DSL or visual designer, fully managed with zero maintenance

Durable functions are ideal for application development in Lambda where workflows are tightly coupled with business logic. Step Functions excels at workflow orchestration across AWS services where you need visual design, native integrations to 220\+ services, and zero-maintenance infrastructure.

For a detailed comparison, see [Durable functions or Step Functions](durable-step-functions.md).

## How it works
<a name="durable-functions-how-it-works"></a>

 Under the hood, durable functions are regular Lambda functions using a checkpoint/replay mechanism to track progress and support long-running operations through user-defined suspension points, commonly referred to as durable execution. After your function resumes from a pause or interruption, the system performs replay. During replay, your code runs from the beginning but skips over completed checkpoints, using stored results instead of re-executing completed operations. This replay mechanism ensures consistency while enabling long-running executions.

To harness this checkpoint-and-replay mechanism in your applications, Lambda provides a durable execution SDK. The SDK abstracts away the complexity of managing checkpoints and replay, exposing simple primitives called durable operations that you use in your code. The SDK is available for JavaScript, TypeScript, Python, and Java, integrating seamlessly with your existing Lambda development workflow.

With the SDK, you wrap your Lambda event handler, which then provides a DurableContext alongside your event. This context gives you access to durable operations like steps and waits. You write your function logic as normal sequential code, but instead of calling services directly, you wrap those calls in steps for automatic checkpointing and retries. When you need to pause execution, you add waits that suspend your function without incurring charges. The SDK handles all the complexity of state management and replay behind the scenes, so your code remains clean and readable.

 ![Diagram showing how Lambda durable functions use checkpoints to persist progress and replay to resume execution after interruptions.](http://docs.aws.amazon.com/lambda/latest/dg/images/how_durable_works.png) 

## Next steps
<a name="durable-functions-next-steps"></a>
+ [AWS Durable Execution SDK Developer Guide](https://docs.aws.amazon.com/durable-execution/) – SDK reference, quickstarts, testing, and language guides
+ [Get started with durable functions](durable-getting-started.md)
+ [Durable functions or Step Functions](durable-step-functions.md)
+ [Monitor and debug durable functions](durable-monitoring.md)
+ [Review security and permissions](durable-security.md)
+ [Encrypting AWS Lambda durable execution data](durable-encryption.md)
+ [Follow best practices](durable-best-practices.md)