

# Durable functions or Step Functions
<a name="durable-step-functions"></a>

Both Lambda durable functions and AWS Step Functions enable reliable workflow orchestration with automatic state management and failure recovery. They serve different developer preferences and architectural patterns. Durable functions are optimized for application development within Lambda, while Step Functions is built for workflow orchestration across AWS services.

## When to use durable functions
<a name="durable-sfn-when-durable"></a>

Use durable functions when:
+ Your team prefers standard programming languages and familiar development tools
+ Your application logic is primarily within Lambda functions
+ You want fine-grained control over execution state in code
+ You're building Lambda-centric applications with tight coupling between workflow and business logic
+ You want to iterate quickly without switching between code and visual/JSON designers

## When to use Step Functions
<a name="durable-sfn-when-step"></a>

Use Step Functions when:
+ You need visual workflow representation for cross-team visibility
+ You're orchestrating multiple AWS services and want native integrations without custom SDK code
+ You require zero-maintenance infrastructure (no patching, runtime updates)
+ Non-technical stakeholders need to understand and validate workflow logic

## Decision framework
<a name="durable-sfn-decision-framework"></a>

Use the following questions to determine which service fits your use case:
+ **What's your primary focus?** Application development in Lambda → durable functions. Workflow orchestration across AWS → Step Functions.
+ **What's your preferred programming model?** Standard programming languages → durable functions. Graph-based DSL or visual designer → Step Functions.
+ **How many AWS services are involved?** Primarily Lambda → durable functions. Multiple AWS services → Step Functions.
+ **What development tools do you use?** Lambda developer experience, IDE with LLM agent, programming language-specific unit test frameworks, AWS SAM, AWS CDK, AWS Toolkit → durable functions. Visual workflow builder, AWS CDK to model workflows → Step Functions.
+ **Who manages the infrastructure?** Want flexibility within Lambda → durable functions. Want fully managed, zero-maintenance → Step Functions.

## Feature comparison
<a name="durable-sfn-comparison"></a>

The following table compares key features between Step Functions and Lambda durable functions:


| Feature | AWS Step Functions | Lambda durable functions | 
| --- | --- | --- | 
| Primary focus | Workflow orchestration across AWS | Application development in Lambda | 
| Service type | Standalone, dedicated workflow service | Runs within Lambda | 
| Programming model | Graph-based, Amazon States Language DSL or AWS CDK | Standard programming languages (JavaScript/TypeScript, Python) | 
| Development tools | Visual builder in Console / AWS Toolkit IDE extension, AWS CDK | Lambda DX within IDE and LLM agents, unit test frameworks, AWS SAM, AWS Toolkit IDE extension | 
| Integrations | 220\+ AWS services, 16k APIs | Lambda event-driven programming model extension (event sources) | 
| Management | Fully managed, runtime agnostic, zero maintenance (no patching, runtime updates) | Managed within Lambda environment | 
| Best for | Business process and IT automation, data processing, AI workflows | Distributed transactions, stateful application logic, function orchestration, data processing, AI workflows | 

## Hybrid architectures
<a name="durable-sfn-hybrid"></a>

Many applications benefit from using both services. A common pattern is using durable functions for application-level logic within Lambda, while Step Functions coordinates high-level workflows across multiple AWS services beyond Lambda functions.

## Migration considerations
<a name="durable-sfn-migration"></a>

**Starting simple, evolving complex:** Begin with durable functions for Lambda-centric workflows. Add Step Functions when you need multi-service orchestration or visual workflow design.

**Existing Step Functions users:** Keep Step Functions for established cross-service workflows. Consider durable functions for new Lambda application logic that needs reliability.

## Related resources
<a name="durable-sfn-related"></a>
+ [Lambda durable functions](durable-functions.md)
+ [Orchestrating Lambda functions with Step Functions](with-step-functions.md)
+ [Getting started with durable functions](durable-getting-started.md)