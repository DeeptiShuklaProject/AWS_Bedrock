

# Building Lambda functions with Java
<a name="lambda-java"></a>

You can run Java code in AWS Lambda. Lambda provides [runtimes](lambda-runtimes.md) for Java that run your code to process events. Your code runs in an Amazon Linux environment that includes AWS credentials from an AWS Identity and Access Management (IAM) role that you manage.

Lambda supports the following Java runtimes.<a name="java-runtimes"></a>


| Name | Identifier | Operating system | Deprecation date | Block function create | Block function update | 
| --- | --- | --- | --- | --- | --- | 
| Java 25 | `java25` | Amazon Linux 2023 |  Jun 30, 2029  |  Jul 31, 2029  |  Aug 31, 2029  | 
| Java 21 | `java21` | Amazon Linux 2023 |  Jun 30, 2029  |  Jul 31, 2029  |  Aug 31, 2029  | 
| Java 17 | `java17` | Amazon Linux 2 |  Jun 30, 2027  |  Jul 31, 2027  |  Aug 31, 2027  | 
| Java 11 | `java11` | Amazon Linux 2 |  Jun 30, 2027  |  Jul 31, 2027  |  Aug 31, 2027  | 
| Java 8 | `java8.al2` | Amazon Linux 2 |  Jun 30, 2027  |  Jul 31, 2027  |  Aug 31, 2027  | 

AWS provides the following libraries for Java functions. These libraries are available through [Maven Central Repository](https://search.maven.org/search?q=g:com.amazonaws).
+ [com.amazonaws:aws-lambda-java-core](https://github.com/aws/aws-lambda-java-libs/tree/master/aws-lambda-java-core) (required) – Defines handler method interfaces and the context object that the runtime passes to the handler. If you define your own input types, this is the only library that you need.
+ [com.amazonaws:aws-lambda-java-events](https://github.com/aws/aws-lambda-java-libs/tree/master/aws-lambda-java-events) – Input types for events from services that invoke Lambda functions.
+ [com.amazonaws:aws-lambda-java-log4j2](https://github.com/aws/aws-lambda-java-libs/tree/master/aws-lambda-java-log4j2) – An appender library for Apache Log4j 2 that you can use to add the request ID for the current invocation to your [function logs](java-logging.md).
+ [AWS SDK for Java 2.0](https://github.com/aws/aws-sdk-java-v2) – The official AWS SDK for the Java programming language.
+ [AWS Lambda Durable Execution SDK for Java](https://github.com/aws/aws-durable-execution-sdk-java) – Build reliable multi-step applications and AI workflows that checkpoint progress, automatically recover from failures, and pause execution. For more information, see [Lambda durable functions](durable-functions.md).

Add these libraries to your build definition as follows:

------
#### [ Gradle ]

```
dependencies {
    implementation 'com.amazonaws:aws-lambda-java-core:1.2.2'
    implementation 'com.amazonaws:aws-lambda-java-events:3.11.1'
    runtimeOnly 'com.amazonaws:aws-lambda-java-log4j2:1.5.1'
    implementation 'software.amazon.lambda.durable:aws-durable-execution-sdk-java:1.0.1'
}
```

------
#### [ Maven ]

```
  <dependencies>
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-lambda-java-core</artifactId>
      <version>1.2.2</version>
    </dependency>
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-lambda-java-events</artifactId>
      <version>3.11.1</version>
    </dependency>
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-lambda-java-log4j2</artifactId>
      <version>1.5.1</version>
    </dependency>
    <dependency>
      <groupId>software.amazon.lambda.durable</groupId>
      <artifactId>aws-durable-execution-sdk-java</artifactId>
      <version>1.0.1</version>
    </dependency>
  </dependencies>
```

------

**Important**  
Don't use private components of the JDK API, such as private fields, methods, or classes. Non-public API components can change or be removed in any update, causing your application to break.

**To create a Java function**

1. Open the [Lambda console](https://console.aws.amazon.com/lambda).

1. Choose **Create function**.

1. Configure the following settings:
   + **Function name**: Enter a name for the function.
   + **Runtime**: Choose **Java 25**.

1. Choose **Create function**.

The console creates a Lambda function with a handler class named `Hello`. Since Java is a compiled language, you can't view or edit the source code in the Lambda console, but you can modify its configuration, invoke it, and configure triggers.

**Note**  
To get started with application development in your local environment, deploy one of the [sample applications](java-samples.md) available in this guide's GitHub repository.

The `Hello` class has a function named `handleRequest` that takes an event object and a context object. This is the [handler function](java-handler.md) that Lambda calls when the function is invoked. The Java function runtime gets invocation events from Lambda and passes them to the handler. In the function configuration, the handler value is `example.Hello::handleRequest`.

To update the function's code, you create a deployment package, which is a .zip file archive that contains your function code. As your function development progresses, you will want to store your function code in source control, add libraries, and automate deployments. Start by [creating a deployment package](java-package.md) and updating your code at the command line.

The function runtime passes a context object to the handler, in addition to the invocation event. The [context object](java-context.md) contains additional information about the invocation, the function, and the execution environment. More information is available from environment variables.

Your Lambda function comes with a CloudWatch Logs log group. The function runtime sends details about each invocation to CloudWatch Logs. It relays any [logs that your function outputs](java-logging.md) during invocation. If your function returns an error, Lambda formats the error and returns it to the invoker.

**Topics**
+ [Define Lambda function handler in Java](java-handler.md)
+ [Deploy Java Lambda functions with .zip or JAR file archives](java-package.md)
+ [Deploy Java Lambda functions with container images](java-image.md)
+ [Working with layers for Java Lambda functions](java-layers.md)
+ [Customize serialization for Lambda Java functions](java-custom-serialization.md)
+ [Customize Java runtime startup behavior for Lambda functions](java-customization.md)
+ [Using the Lambda context object to retrieve Java function information](java-context.md)
+ [Log and monitor Java Lambda functions](java-logging.md)
+ [Instrumenting Java code in AWS Lambda](java-tracing.md)
+ [Java sample applications for AWS Lambda](java-samples.md)