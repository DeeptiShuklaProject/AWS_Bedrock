

# Code examples for Lambda using AWS SDKs
<a name="service_code_examples"></a>

The following code examples show how to use Lambda with an AWS software development kit (SDK). 

*Basics* are code examples that show you how to perform the essential operations within a service.

*Actions* are code excerpts from larger programs and must be run in context. While actions show you how to call individual service functions, you can see actions in context in their related scenarios.

*Scenarios* are code examples that show you how to accomplish specific tasks by calling multiple functions within a service or combined with other AWS services.

*AWS community contributions* are examples that were created and are maintained by multiple teams across AWS. To provide feedback, use the mechanism provided in the linked repositories.

For a complete list of AWS SDK developer guides and code examples, see [Using Lambda with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.

**Contents**
+ [Basics](service_code_examples_basics.md)
  + [Hello Lambda](example_lambda_Hello_section.md)
  + [Learn the basics](example_lambda_Scenario_GettingStartedFunctions_section.md)
  + [Actions](service_code_examples_actions.md)
    + [`CreateAlias`](example_lambda_CreateAlias_section.md)
    + [`CreateFunction`](example_lambda_CreateFunction_section.md)
    + [`DeleteAlias`](example_lambda_DeleteAlias_section.md)
    + [`DeleteFunction`](example_lambda_DeleteFunction_section.md)
    + [`DeleteFunctionConcurrency`](example_lambda_DeleteFunctionConcurrency_section.md)
    + [`DeleteProvisionedConcurrencyConfig`](example_lambda_DeleteProvisionedConcurrencyConfig_section.md)
    + [`GetAccountSettings`](example_lambda_GetAccountSettings_section.md)
    + [`GetAlias`](example_lambda_GetAlias_section.md)
    + [`GetFunction`](example_lambda_GetFunction_section.md)
    + [`GetFunctionConcurrency`](example_lambda_GetFunctionConcurrency_section.md)
    + [`GetFunctionConfiguration`](example_lambda_GetFunctionConfiguration_section.md)
    + [`GetPolicy`](example_lambda_GetPolicy_section.md)
    + [`GetProvisionedConcurrencyConfig`](example_lambda_GetProvisionedConcurrencyConfig_section.md)
    + [`Invoke`](example_lambda_Invoke_section.md)
    + [`ListFunctions`](example_lambda_ListFunctions_section.md)
    + [`ListProvisionedConcurrencyConfigs`](example_lambda_ListProvisionedConcurrencyConfigs_section.md)
    + [`ListTags`](example_lambda_ListTags_section.md)
    + [`ListVersionsByFunction`](example_lambda_ListVersionsByFunction_section.md)
    + [`PublishVersion`](example_lambda_PublishVersion_section.md)
    + [`PutFunctionConcurrency`](example_lambda_PutFunctionConcurrency_section.md)
    + [`PutProvisionedConcurrencyConfig`](example_lambda_PutProvisionedConcurrencyConfig_section.md)
    + [`RemovePermission`](example_lambda_RemovePermission_section.md)
    + [`TagResource`](example_lambda_TagResource_section.md)
    + [`UntagResource`](example_lambda_UntagResource_section.md)
    + [`UpdateAlias`](example_lambda_UpdateAlias_section.md)
    + [`UpdateFunctionCode`](example_lambda_UpdateFunctionCode_section.md)
    + [`UpdateFunctionConfiguration`](example_lambda_UpdateFunctionConfiguration_section.md)
+ [Scenarios](service_code_examples_scenarios.md)
  + [Automatically confirm known users with a Lambda function](example_cross_CognitoAutoConfirmUser_section.md)
  + [Automatically migrate known users with a Lambda function](example_cross_CognitoAutoMigrateUser_section.md)
  + [Create a REST API to track COVID-19 data](example_cross_ApiGatewayDataTracker_section.md)
  + [Create a lending library REST API](example_cross_AuroraRestLendingLibrary_section.md)
  + [Create a messenger application](example_cross_StepFunctionsMessenger_section.md)
  + [Create a rest API with function proxy integration](example_api_gateway_GettingStarted_087_section.md)
  + [Create a serverless application to manage photos](example_cross_PAM_section.md)
  + [Create a websocket chat application](example_cross_ApiGatewayWebsocketChat_section.md)
  + [Create an application to analyze customer feedback](example_cross_FSA_section.md)
  + [Creating a monitoring dashboard with function name as a variable](example_cloudwatch_GettingStarted_031_section.md)
  + [Creating your first serverless function](example_lambda_GettingStarted_019_section.md)
  + [Invoke a Lambda function from a browser](example_cross_LambdaForBrowser_section.md)
  + [Transform data with S3 Object Lambda](example_cross_ServerlessS3DataTransformation_section.md)
  + [Use API Gateway to invoke a Lambda function](example_cross_LambdaAPIGateway_section.md)
  + [Use Step Functions to invoke Lambda functions](example_cross_ServerlessWorkflows_section.md)
  + [Use scheduled events to invoke a Lambda function](example_cross_LambdaScheduledEvents_section.md)
  + [Use the Neptune API to query graph data](example_cross_Neptune_Query_section.md)
  + [Using property variables in monitoring dashboards to monitor multiple serverless functions](example_iam_GettingStarted_032_section.md)
  + [Write custom activity data with a Lambda function after Amazon Cognito user authentication](example_cross_CognitoCustomActivityLog_section.md)
+ [Serverless examples](service_code_examples_serverless_examples.md)
  + [Connecting to an Amazon RDS database in a Lambda function](example_serverless_connect_RDS_Lambda_section.md)
  + [Invoke a Lambda function from a Kinesis trigger](example_serverless_Kinesis_Lambda_section.md)
  + [Invoke a Lambda function from a DynamoDB trigger](example_serverless_DynamoDB_Lambda_section.md)
  + [Invoke a Lambda function from a Amazon DocumentDB trigger](example_serverless_DocumentDB_Lambda_section.md)
  + [Invoke a Lambda function from an Amazon MSK trigger](example_serverless_MSK_Lambda_section.md)
  + [Invoke a Lambda function from an Amazon S3 trigger](example_serverless_S3_Lambda_section.md)
  + [Invoke a Lambda function from an Amazon SNS trigger](example_serverless_SNS_Lambda_section.md)
  + [Invoke a Lambda function from an Amazon SQS trigger](example_serverless_SQS_Lambda_section.md)
  + [Reporting batch item failures for Lambda functions with a Kinesis trigger](example_serverless_Kinesis_Lambda_batch_item_failures_section.md)
  + [Reporting batch item failures for Lambda functions with a DynamoDB trigger](example_serverless_DynamoDB_Lambda_batch_item_failures_section.md)
  + [Reporting batch item failures for Lambda functions with an Amazon SQS trigger](example_serverless_SQS_Lambda_batch_item_failures_section.md)
+ [AWS community contributions](service_code_examples_aws_community_contributions.md)
  + [Build and test a serverless application](example_tributary-lite_serverless-application_section.md)