

# Delete a model evaluation job in Amazon Bedrock
<a name="model-evaluation-jobs-management-delete"></a>

You can delete a model evaluation job by using the Amazon Bedrock console, or by using the [BatchDeleteEvaluationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_BatchDeleteEvaluationJob.html) operation with the AWS CLI, or a supported AWS SDK. 

Before you can delete a model evaluation job, the status of the job must be `FAILED`, `COMPLETED`, or `STOPPED`. You can get the current status for a job from the Amazon Bedrock console or by calling the [ ListEvaluationJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListEvaluationJobs.html). For more information, see [List automatic model evaluation jobs in Amazon BedrockList model evaluation jobs that use human workers in Amazon Bedrock](model-evaluation-jobs-management-list.md). 

You can delete up to 25 model evaluation jobs at a time with the console and with the `BatchDeleteEvaluationJob` operation. If you need to delete more jobs, repeat the console procedure or `BatchDeleteEvaluationJob` call.

If you delete a model evaluation job with the `BatchDeleteEvaluationJob` operation, you need the Amazon Resource Names (ARNs) of the models that you want to delete. For information about getting the ARN for a model, see [List automatic model evaluation jobs in Amazon BedrockList model evaluation jobs that use human workers in Amazon Bedrock](model-evaluation-jobs-management-list.md). 

When you delete a model evaluation job all resources in Amazon Bedrock and Amazon SageMaker AI are removed. Any model evaluation job saved in Amazon S3 buckets are left unchanged. Also, for model evaluation jobs that use human workers, deleting a model evaluation job will not delete the workforce or workteam you have configured in Amazon Cognito or SageMaker AI.

Use the following sections to see examples of how to delete a model evaluation job.

------
#### [ Amazon Bedrock console ]

Use the following procedure to delete model evaluation job using the Amazon Bedrock console. To successfully complete this procedure make sure that your IAM user, group, or role has the sufficient permissions to access the console. To learn more, see [Required console permissions to create an automatic model evaluation job](model-evaluation-type-automatic.md#base-for-automatic).

**To delete multiple model evaluation jobs.**

1. Open the Amazon Bedrock console: [https://console.aws.amazon.com/bedrock/](https://console.aws.amazon.com/bedrock/)

1. In the navigation pane, choose **Model evaluation**.

1. In the **Model Evaluation Jobs** card, use the table to find the model evaluation jobs that you want to delete, select them using the checkbox next to the job's name. You can select up to 25 jobs.

1. Choose **Delete** to delete the model evaluation jobs.

1. If you need to delete more model evaluation jobs, repeat steps 3 and 4.

------
#### [ AWS CLI ]

In the AWS CLI, you can use the `help` command to view parameters are required, and which parameters are optional when using `batch-delete-evaluation-job`.

```
aws bedrock batch-delete-evaluation-job help
```

The follow is an example of using `batch-delete-evaluation-job` and specifying that 2 model evaluation jobs be deleted. You use the `job-identifiers` parameter to specify a list of ARNS for the model evaluation jobs that you want to delete. You can delete up to 25 model evaluation jobs in a single call to `batch-delete-evaluation-job`. If you need to delete more jobs, make further calls to `batch-delete-evaluation-job`.

```
aws bedrock batch-delete-evaluation-job \
--job-identifiers {{arn:aws:bedrock:us-east-1:111122223333:evaluation-job/rmqp8zg80rvg}} {{arn:aws:bedrock:us-east-1:111122223333:evaluation-job/xmfp9zg204fdk}}
```

After submitting you would get the following response.

```
{
	"evaluationJobs": [
		{
			"jobIdentifier": "rmqp8zg80rvg",
			"jobStatus": "Deleting"
		},
		{
			"jobIdentifier": "xmfp9zg204fdk",
			"jobStatus": "Deleting"
		}

	],
	"errors": []
}
```

------
#### [ SDK for Python ]

The following examples show how to use the AWS SDK for Python to delete a model evaluation job. Use the `jobIdentifiers` parameter to specify a list of ARNS for the model evaluation jobs that you want to delete. You can delete up to 25 model evaluation jobs in a single call to `BatchDeleteEvaluationJob`. If you need to delete more jobs, make further calls to `BatchDeleteEvaluationJob`.

```
import boto3
client = boto3.client('bedrock')

job_request = client.batch_delete_model_evaluation_job(jobIdentifiers=["{{arn:aws:bedrock:us-east-1:111122223333:evaluation-job/rmqp8zg80rvg}}", "{{arn:aws:bedrock:us-east-1:111122223333:evaluation-job/xmfp9zg204fdk}}"])

print (job_request)
```

------