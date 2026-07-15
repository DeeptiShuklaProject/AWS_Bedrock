

# Using Lambda with infrastructure as code (IaC)
<a name="foundation-iac"></a>

Lambda functions rarely run in isolation. Instead, they often form part of a serverless application with other resources such as databases, queues, and storage. With [infrastructure as code (IaC)](https://aws.amazon.com/what-is/iac/), you can automate your deployment processes to quickly and repeatably deploy and update whole serverless applications involving many separate AWS resources. This approach speeds up your development cycle, makes configuration management easier, and ensures that your resources are deployed the same way every time.

## IaC tools for Lambda
<a name="foundation-iac-tools"></a>

**CloudFormation**  
CloudFormation is the foundational IaC service from AWS. You can use [YAML or JSON templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html) to model and provision your entire AWS infrastructure, including Lambda functions. CloudFormation handles the complexities of creating, updating, and deleting your AWS resources.

**AWS Serverless Application Model (AWS SAM)**  
AWS SAM is an open-source framework built on top of CloudFormation. It provides a simplified syntax for defining serverless applications. Use [AWS SAM templates](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html) to quickly provision Lambda functions, APIs, databases, and event sources with just a few lines of YAML.

**AWS Cloud Development Kit (AWS CDK)**  
The CDK is a code-first approach to IaC. You can define your Lambda-based architecture using TypeScript, JavaScript, Python, Java, C\#/.Net, or Go. Choose your preferred language and use programming elements like parameters, conditionals, loops, composition, and inheritance to define the desired outcome of your infrastructure. The CDK then generates the underlying CloudFormation templates for deployment. For an example of how to use Lambda with CDK, see [Deploying Lambda functions with AWS CDK](lambda-cdk-tutorial.md).

![Diagram showing how AWS SAM and AWS CDK deploy AWS resources and code using CloudFormation](http://docs.aws.amazon.com/lambda/latest/dg/images/IaC_tools.png)


AWS also provides a service called AWS Infrastructure Composer to develop IaC templates using a simple graphical interface. With Infrastructure Composer, you design an application architecture by dragging, grouping, and connecting AWS services in a visual canvas. Infrastructure Composer then creates an AWS SAM template or an CloudFormation template from your design that you can use to deploy your application.

In the [Using Lambda functions in AWS SAM and Infrastructure Composer](foundation-iac-getting-started.md) section below, you use Infrastructure Composer to develop a template for a serverless application based on an existing Lambda function.