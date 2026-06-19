

# Monitor Amazon Bedrock job state changes using Amazon EventBridge
<a name="monitoring-eventbridge"></a>

Amazon EventBridge is an AWS service that monitors events from other AWS services in near real-time. You can use Amazon EventBridge to monitor events in Amazon Bedrock and to send event information when they match a rule you define. You can then configure your application to respond automatically to these events. Amazon EventBridge supports monitoring of the following events in Amazon Bedrock:
+ [Model customization jobs](custom-models.md) – The state of a job can be seen in the job details in the AWS Management Console or in a [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html) response. For more information, see [Monitor your model customization job](model-customization-monitor.md).
+ [Batch inference jobs](batch-inference.md) – The state of a job can be seen in the job details in the AWS Management Console or in a [GetModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelInvocationJob.html) response. For more information, see [Monitor batch inference jobs](batch-inference-monitor.md).

Amazon Bedrock emits events on a best-effort basis. Events from Amazon Bedrock are delivered to Amazon EventBridge in near real time. You can create rules that trigger programmatic actions in response to an event. With Amazon EventBridge, you can do the following:
+ Publish notifications whenever there is a state change event in a job that you've submitted, and whether to add new asynchronous workflows in the future. The notification should give you enough information to react to events in downstream workflows.
+ Deliver job status updates without invoking a Get API, which can help handle API rate limit issues, API updates, and reduction in additional compute resources.

There is no cost to receive AWS events from Amazon EventBridge. For more information about, Amazon EventBridge, see [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)

**Topics**
+ [How EventBridge for Amazon Bedrock works](monitoring-eventbridge-how-it-works.md)
+ [[Example] Create a rule to handle Amazon Bedrock state change events](monitoring-eventbridge-create-rule-ex.md)