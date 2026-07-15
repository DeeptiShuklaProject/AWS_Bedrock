

# Powertools for AWS Lambda
<a name="powertools-for-lambda"></a>

Powertools for AWS Lambda (also referred to as Powertools for AWS) provides utility functions, decorators, and middleware that handle common Lambda tasks like structured logging, tracing, metrics collection, and input validation. Use Powertools for AWS Lambda to implement serverless best practices and accelerate development across multiple Lambda functions. Doing this simplifies common development tasks in your Lambda functions.

## Key benefits of Powertools for AWS
<a name="powertools-key-benefits"></a>

While Lambda development is possible without Powertools for AWS, using it offers several advantages:
+ Built-in observability: Structured logging, tracing, and custom metrics
+ Secrets management: Parameter retrieval, secrets handling, and idempotency
+ Progressive Enhancement: Choose the utilities that best suit your needs
+ Accelerated development: Event parsing, validation, and batch processing
+ Best practices: Implementation of AWS Well-Architected serverless patterns

## Integrating Powertools with AWS
<a name="integrating-powertools"></a>

Powertools for AWS helps you build production-ready serverless applications with less custom code. Available in Python, TypeScript/Node.js, .NET, and Java, Powertools for AWS can be included through Lambda Layers, or using the language package manager. Each language implementation provides core features like structured logging, tracing, metrics collection, and event handling, while maintaining idioms natural to each programming language. These implementations are complemented by specialized components for AWS service integration, supporting parameter retrieval, batch processing, and API handling, along with best practices like correlation ID propagation, error handling, and idempotency patterns. Together, these features enable developers to build robust, maintainable serverless applications while reducing custom code overhead.
+ [Powertools for AWS Lambda (Python)](https://docs.powertools.aws.dev/lambda/python/latest/)
+ [Powertools for AWS Lambda (TypeScript)](https://docs.powertools.aws.dev/lambda/typescript/latest/)
+ [Powertools for AWS Lambda (Java)](https://docs.powertools.aws.dev/lambda/java/latest/)
+ [Powertools for AWS Lambda (.NET)](https://docs.powertools.aws.dev/lambda/dotnet/)

## Next steps
<a name="next-steps"></a>

To learn more about working with Powertools for AWS, see the following resources:
+ [Powertools for AWS Lambda workshop](https://catalog.workshops.aws/powertools-for-aws-lambda)
+ [Serverless patterns that use Powertools for AWS](https://serverlessland.com/search?search=powertools)
+ [AWS well-architected serverless lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html)
+ [Building Serverless APIs with Powertools for AWS Lambda](https://catalog.workshops.aws/powertools-for-aws-lambda-event-handler)