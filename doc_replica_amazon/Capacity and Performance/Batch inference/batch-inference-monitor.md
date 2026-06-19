

# Monitor batch inference jobs
<a name="batch-inference-monitor"></a>

Apart from the configurations you set for a batch inference job, you can also monitor its progress by seeing its status. For more information about the possible statuses for a job, see the `status` field in [ModelInvocationJobSummary](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ModelInvocationJobSummary.html).

To track a job's progress, you can use the progress counters that the [GetModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelInvocationJob.html) and [ListModelInvocationJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelInvocationJobs.html) API operations return. These counters show the total number of input records and how many the service has processed. You can monitor completion without checking Amazon S3 output buckets. Alternatively, you can find these numbers in the `manifest.json.out` file in the Amazon S3 bucket that contains the output files. For more information, see [View the results of a batch inference job](batch-inference-results.md). To learn how to download an S3 object, see [Downloading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/download-objects.html).

**Tip**  
Instead of polling for job status, you can use Amazon EventBridge to receive automatic notifications when a batch inference job completes or changes state. For more information, see [Monitor Amazon Bedrock job state changes using Amazon EventBridgeMonitor event changes](monitoring-eventbridge.md).

To learn how to view details about batch inference jobs, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about batch inference jobs**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, select **Batch inference**.

1. In the **Batch inference jobs** section, choose a job.

1. On the job details page, you can view information about the job's configuration and monitor its progress by viewing its **Status**.

------
#### [ API ]

To get information about a batch inference job, send a [GetModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelInvocationJob.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and provide the ID or ARN of the job in the `jobIdentifier` field.

To list information about multiple batch inference jobs, send [ListModelInvocationJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelInvocationJobs.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

The response for `GetModelInvocationJob` and `ListModelInvocationJobs` includes a `modelInvocationType` field that indicates whether the job uses the `InvokeModel` or `Converse` API format.

The response also includes the following fields that you can use to track the progress of a running job:
+ `totalRecordCount` – The total number of records submitted to the batch inference job.
+ `processedRecordCount` – The number of records processed so far, which includes both successes and errors.
+ `successRecordCount` – The number of records successfully processed so far.
+ `errorRecordCount` – The number of records that have caused errors during processing.

To calculate the percentage of progress for a running job, divide `processedRecordCount` by `totalRecordCount`. The counters return `0` when you submit a job but processing has not yet started. While a job is in progress, the counters might be delayed by up to 1 minute.

To list all the tags for a job, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the job.

------