

# Building Lambda functions with TypeScript
<a name="lambda-typescript"></a>

You can use the Node.js runtime to run TypeScript code in AWS Lambda. Because Node.js doesn't run TypeScript code natively, you must first transpile your TypeScript code into JavaScript. Then, use the JavaScript files to deploy your function code to Lambda. Your code runs in an environment that includes the AWS SDK for JavaScript, with credentials from an AWS Identity and Access Management (IAM) role that you manage. To learn more about the SDK versions included with the Node.js runtimes, see [Runtime-included SDK versions](lambda-nodejs.md#nodejs-sdk-included).

Lambda supports the following Node.js runtimes.


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| Node.js 24 | `nodejs24.x` | Amazon Linux 2023 |  Apr 30, 2028  |  Jun 1, 2028  |  Jul 1, 2028  | 
| Node.js 22 | `nodejs22.x` | Amazon Linux 2023 |  Apr 30, 2027  |  Jun 1, 2027  |  Jul 1, 2027  | 

**Topics**
+ [Setting up a TypeScript development environment](#typescript-dev)
+ [Type definitions for Lambda](#typescript-type-definitions)
+ [Define Lambda function handler in TypeScript](typescript-handler.md)
+ [Deploy transpiled TypeScript code in Lambda with .zip file archives](typescript-package.md)
+ [Deploy transpiled TypeScript code in Lambda with container images](typescript-image.md)
+ [Using the Lambda context object to retrieve TypeScript function information](typescript-context.md)
+ [Log and monitor TypeScript Lambda functions](typescript-logging.md)
+ [Tracing TypeScript code in AWS Lambda](typescript-tracing.md)

## Setting up a TypeScript development environment
<a name="typescript-dev"></a>

Use a local integrated development environment (IDE) or text editor to write your TypeScript function code. You can’t create TypeScript code on the Lambda console.

You can use either [esbuild](https://esbuild.github.io/) or Microsoft's TypeScript compiler (`tsc`) to transpile your TypeScript code into JavaScript. The [AWS Serverless Application Model (AWS SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html) and the [AWS Cloud Development Kit (AWS CDK)](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) both use esbuild.

When using esbuild, consider the following:
+ There are several [TypeScript caveats](https://esbuild.github.io/content-types/#typescript-caveats).
+ You must configure your TypeScript transpilation settings to match the Node.js runtime that you plan to use. For more information, see [Target](https://esbuild.github.io/api/#target) in the esbuild documentation. For an example of a **tsconfig.json** file that demonstrates how to target a specific Node.js version supported by Lambda, refer to the [TypeScript GitHub repository](https://github.com/tsconfig/bases/blob/main/bases/node14.json).
+ esbuild doesn’t perform type checks. To check types, use the `tsc` compiler. Run `tsc -noEmit` or add a `"noEmit"` parameter to your **tsconfig.json** file, as shown in the following example. This configures `tsc` to not emit JavaScript files. After checking types, use esbuild to convert the TypeScript files into JavaScript.

**Example tsconfig.json**  

```
 {
  "compilerOptions": {
    "target": "es2020",
    "strict": true,
    "preserveConstEnums": true,
    "noEmit": true,
    "sourceMap": false,
    "module":"commonjs",
    "moduleResolution":"node",
    "esModuleInterop": true, 
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true, 
    "isolatedModules": true, 
  },
  "exclude": ["node_modules", "**/*.test.ts"]
}
```

## Type definitions for Lambda
<a name="typescript-type-definitions"></a>

The [@types/aws-lambda](https://www.npmjs.com/package/@types/aws-lambda) package provides type definitions for Lambda functions. Install this package when your function uses any of the following:
+ Common AWS event sources, such as:
  + `APIGatewayProxyEvent`: For [Amazon API Gateway proxy integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html) 
  + `SNSEvent`: For [Amazon Simple Notification Service notifications](with-sns.md)
  + `SQSEvent`: For [Amazon Simple Queue Service messages](with-sqs.md)
  + `S3Event`: For [S3 trigger events](with-s3.md)
  + `DynamoDBStreamEvent`: For [Amazon DynamoDB Streams](with-ddb.md)
+ The Lambda [Context](typescript-context.md) object
+ The [callback](typescript-handler.md#typescript-handler-callback) handler pattern

To add the Lambda type definitions to your function, install `@types/aws-lambda` as a development dependency:

```
npm install -D @types/aws-lambda
```

Then, import the types from `aws-lambda`:

```
import { Context, S3Event, APIGatewayProxyEvent } from 'aws-lambda';

export const handler = async (event: S3Event, context: Context) => {
    // Function code
};
```

The `import ... from 'aws-lambda'` statement imports the type definitions. It does not import the `aws-lambda` npm package, which is an unrelated third-party tool. For more information, see [aws-lambda](https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/aws-lambda) in the DefinitelyTyped GitHub repository.

**Note**  
You don't need [@types/aws-lambda](https://www.npmjs.com/package/@types/aws-lambda) when using your own custom type definitions. For an example function that defines its own type for an event object, see [Example TypeScript Lambda function code](typescript-handler.md#typescript-example-code).