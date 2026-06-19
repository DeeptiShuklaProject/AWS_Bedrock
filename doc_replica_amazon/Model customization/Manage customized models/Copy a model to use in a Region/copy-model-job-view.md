

# View information about model copy jobs
<a name="copy-model-job-view"></a>

To learn how to view information about model copy jobs that you've submitted, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. Select the **Jobs** tab.

1. If a model is still being copied, the **Status** is **Copying**. If it's finished and ready for use, the **Status** is **Completed**.

1. When the job is complete, the model appears in the **Models** section in the **Models** tab in the Region that you copied the model to.

------
#### [ API ]

To get information about a model copy job, send a [GetModelCopyJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCopyJob.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Include the `jobArn` in the request.

To list the model copy jobs that you've submitted, send a [ListModelCopyJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelCopyJobs.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). You can use the headers in the request to specify filters for which jobs to return.

The response returns a list, each of which contains information about a model copy job that you've submitted.

When the job is complete, you should be able to see the copied model by sending a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp), specifying the Region that you copied the model to.

------