

# Monitor Amazon Bedrock API calls using CloudTrail
<a name="logging-using-cloudtrail"></a>

Amazon Bedrock is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service in Amazon Bedrock. CloudTrail captures all API calls for Amazon Bedrock as events. The calls captured include calls from the Amazon Bedrock console and code calls to the Amazon Bedrock API operations. If you create a trail, you can enable continuous delivery of CloudTrail events to an Amazon S3 bucket, including events for Amazon Bedrock.

**Note**  
This page describes CloudTrail logging for the `bedrock-runtime.{{region}}.amazonaws.com` endpoint. If your application calls the `bedrock-mantle.{{region}}.api.aws` endpoint, see [Monitor `bedrock-mantle` API calls using CloudTrail](logging-cloudtrail-mantle.md) instead.

If you don't configure a trail, you can still view the most recent events in the CloudTrail console in **Event history**.

Using the information collected by CloudTrail, you can determine the request that was made to Amazon Bedrock, the IP address from which the request was made, who made the request, when it was made, and additional details.

To learn more about CloudTrail, see the [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html).

## Amazon Bedrock information in CloudTrail
<a name="service-name-info-in-cloudtrail"></a>

CloudTrail is enabled on your AWS account when you create the account. When activity occurs in Amazon Bedrock, that activity is recorded in a CloudTrail event along with other AWS service events in **Event history**. You can view, search, and download recent events in your AWS account. For more information, see [Viewing events with CloudTrail Event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html).

For an ongoing record of events in your AWS account, including events for Amazon Bedrock, create a trail. A *trail* enables CloudTrail to deliver log files to an Amazon S3 bucket. By default, when you create a trail in the console, the trail applies to all AWS Regions. The trail logs events from all Regions in the AWS partition and delivers the log files to the Amazon S3 bucket that you specify. Additionally, you can configure other AWS services to further analyze and act upon the event data collected in CloudTrail logs. For more information, see the following:
+ [Overview for creating a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-and-update-a-trail.html)
+ [CloudTrail supported services and integrations](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-aws-service-specific-topics.html)
+ [Configuring Amazon SNS notifications for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/configure-sns-notifications-for-cloudtrail.html)
+ [Receiving CloudTrail log files from multiple Regions](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/receive-cloudtrail-log-files-from-multiple-regions.html) and [Receiving CloudTrail log files from multiple accounts](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-receive-logs-from-multiple-accounts.html)

Every event or log entry contains information about who generated the request. The identity information helps you determine the following:
+ Whether the request was made with root or AWS Identity and Access Management (IAM) user credentials.
+ Whether the request was made with temporary security credentials for a role or federated user.
+ Whether the request was made by another AWS service.

For more information, see the [CloudTrail userIdentity element](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html).

## Amazon Bedrock data events in CloudTrail
<a name="service-name-data-events-cloudtrail"></a>

[Data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events) provide information about the resource operations performed on or in a resource (for example, reading or writing to an Amazon S3 object). These are also known as data plane operations. Data events are often high-volume activities that CloudTrail doesn’t log by default.

Amazon Bedrock logs some [Amazon Bedrock Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html) (such as `InvokeModel`, `InvokeModelWithResponseStream`, `Converse`, `ConverseStream`, and `ListAsyncInvokes`) as [management events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html#logging-management-events).

Amazon Bedrock logs other [Amazon Bedrock Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html) (such as `InvokeModelWithBidirectionalStream`, `GetAsyncInvoke`, and `StartAsyncInvokes`) as data events.

Amazon Bedrock logs all [Agents for Amazon Bedrock Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html) (such as `InvokeAgent` and `InvokeInlineAgent`) actions to CloudTrail as data events.
+ To log [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::AgentAlias` resource type.
+ To log [https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::InlineAgent` resource type.
+ To log [InvokeModelWithBidirectionalStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithBidirectionalStream.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::Model` resource type and `AWS:Bedrock::AsyncInvoke`.
+ To log [GetAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GetAsyncInvoke.html) and [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::Model` resource type and `AWS:Bedrock::AsyncInvoke`.
+ To log [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) and [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::KnowledgeBase` resource type.
+ To log [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html) calls, configure advanced event selectors to record data events for the `AWS::Bedrock::FlowAlias` resource type.
+ To log `RenderPrompt` calls, configure advanced event selectors to record data events for the `AWS::Bedrock::Prompt` resource type. `RenderPrompt` is a permission-only [action](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) that renders prompts, created using [Prompt management](prompt-management.md), for model invocation (`InvokeModel(WithResponseStream)` and `Converse(Stream)`).

From the CloudTrail console, choose **Bedrock agent alias** or **Bedrock knowledge base** for the **Data event type**. You can additionally filter on the `eventName` and `resources.ARN` fields by choosing a custom log selector template. For more information, see [Logging data events with the AWS Management Console](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html).

From the AWS CLI, set the `resource.type` value equal to `AWS::Bedrock::AgentAlias`, `AWS::Bedrock::KnowledgeBase`, or `AWS::Bedrock::FlowAlias` and set the `eventCategory` equal to `Data`. For more information, see [Logging data events with the AWS CLI](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-with-the-AWS-CLI).

The following example shows how to configure a trail to log all Amazon Bedrock data events for all Amazon Bedrock resource types in the AWS CLI.

```
aws cloudtrail put-event-selectors --trail-name {{trailName}} \
--advanced-event-selectors \
'[
  {
    "Name": "Log all data events on an alias of an agent in Amazon Bedrock.",
    "FieldSelectors": [
      { "Field": "eventCategory", "Equals": ["Data"] },
      { "Field": "resources.type", "Equals": ["AWS::Bedrock::AgentAlias"] }
    ]
  },
  {
    "Name": "Log all data events on a knowledge base in Amazon Bedrock.",
    "FieldSelectors": [
      { "Field": "eventCategory", "Equals": ["Data"] },
      { "Field": "resources.type", "Equals": ["AWS::Bedrock::KnowledgeBase"] }
    ]
  },
  {
    "Name": "Log all data events on a flow in Amazon Bedrock.",
    "FieldSelectors": [
      { "Field": "eventCategory", "Equals": ["Data"] },
      { "Field": "resources.type", "Equals": ["AWS::Bedrock::FlowAlias"] }
    ]
  }
  {
    "Name": "Log all data events on a guardrail in Amazon Bedrock.",
    "FieldSelectors": [
      { "Field": "eventCategory", "Equals": ["Data"] },
      { "Field": "resources.type", "Equals": ["AWS::Bedrock::Guardrail"] }
    ]
  }
]'
```

You can additionally filter on the `eventName` and `resources.ARN` fields. For more information about these fields, see [https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedFieldSelector.html](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedFieldSelector.html).

Additional charges apply for data events. For more information about CloudTrail pricing, see [AWS CloudTrail Pricing](https://aws.amazon.com/cloudtrail/pricing/).

## Amazon Bedrock management events in CloudTrail
<a name="bedrock-management-events-cloudtrail"></a>

[Management events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html#logging-management-events) provide information about management operations that are performed on resources in your AWS account. These are also known as control plane operations. CloudTrail logs management event API operations by default.

Amazon Bedrock logs [Amazon Bedrock Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html) (`InvokeModel`, `InvokeModelWithResponseStream`, `Converse`, and `ConverseStream`) as [management events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html#logging-management-events).

Amazon Bedrock logs the remainder of Amazon Bedrock API operations as management events. For a list of the Amazon Bedrock API operations that Amazon Bedrock logs to CloudTrail, see the following pages in the Amazon Bedrock API reference.
+ [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock.html). 
+ [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html). 
+ [Amazon Bedrock Agents Runtime](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html). 
+ [Amazon Bedrock Runtime](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html).

All [Amazon Bedrock API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock.html) and [Agents for Amazon Bedrock API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) are logged by CloudTrail and documented in the [Amazon Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/). For example, calls to the `InvokeModel`, `StopModelCustomizationJob`, and `CreateAgent` actions generate entries in the CloudTrail log files.

[Amazon GuardDuty](https://aws.amazon.com/guardduty/) continuously monitors and analyzes your CloudTrail management and event logs to detect potential security issues. When you enable Amazon GuardDuty for an AWS account, it automatically starts analyzing CloudTrail logs to detect suspicious activity in Amazon Bedrock APIs, such as a user logging in from a new location and using Amazon Bedrock APIs to remove Amazon Bedrock Guardrails, or change the Amazon S3 bucket set for model training data.

## Understanding Amazon Bedrock log file entries
<a name="understanding-bedrock-entries"></a>

A trail is a configuration that enables delivery of events as log files to an Amazon S3 bucket that you specify. CloudTrail log files contain one or more log entries. An event represents a single request from any source and includes information about the requested action, the date and time of the action, request parameters, and so on. CloudTrail log files aren't an ordered stack trace of the public API calls, so they don't appear in any specific order. 

The following example shows a CloudTrail log entry that demonstrates the `InvokeModel` action.

```
{
    "eventVersion": "1.08",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "AROAICFHPEXAMPLE",
        "arn": "arn:aws:iam::111122223333:user/userxyz",
        "accountId": "111122223333",
        "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "userName": "userxyz"
    },
    "eventTime": "2023-10-11T21:58:59Z",
    "eventSource": "bedrock.amazonaws.com",
    "eventName": "InvokeModel",
    "awsRegion": "us-west-2",
    "sourceIPAddress": "192.0.2.0",
    "userAgent": "Boto3/1.28.62 md/Botocore#1.31.62 ua/2.0 os/macos#22.6.0 md/arch#arm64 lang/python#3.9.6 md/pyimpl#CPython cfg/retry-mode#legacy Botocore/1.31.62",
    "requestParameters": {
        "modelId": "stability.stable-diffusion-xl-v0"
    },
    "responseElements": null,
    "requestID": "a1b2c3d4-5678-90ab-cdef-EXAMPLE22222",
    "eventID": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111 ",
    "readOnly": false,
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management",
    "tlsDetails": {
        "tlsVersion": "TLSv1.2",
        "cipherSuite": "cipher suite",
        "clientProvidedHostHeader": "bedrock-runtime.us-west-2.amazonaws.com"
    }
}
```