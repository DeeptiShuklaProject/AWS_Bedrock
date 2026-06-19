

# Monitor your model customization job
<a name="model-customization-monitor"></a>

You can track the progress of your model customization job. Each job consists of the following events:
+ **Validation**
+ **Data processing**
+ **Training**

If your job fails for some reason, you can see where in the process the failure occurred. Use this information to [troubleshoot](fine-tuning-troubleshooting.md) the issue.

------
#### [ Console ]

**To monitor the status of your fine-tuning jobs**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. Choose the job from the **Jobs** table to see job-related details.

------
#### [ API ]

To list information about all your model customization jobs, send a [ListModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelCustomizationJobs.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Refer to [ListModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelCustomizationJobs.html) for filters that you can use.

To monitor the status of a model customization job, send a [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) with the `jobArn` of the job.

To list all the tags for a model customization job, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the job.

[See code examples](model-customization-code-samples.md)

------

You can also monitor model customization jobs with Amazon EventBridge. For more information, see [Monitor Amazon Bedrock job state changes using Amazon EventBridgeMonitor event changes](monitoring-eventbridge.md).