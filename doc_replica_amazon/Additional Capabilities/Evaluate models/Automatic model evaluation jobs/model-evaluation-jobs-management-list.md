

# List automatic model evaluation jobs in Amazon Bedrock
<a name="model-evaluation-jobs-management-list"></a>

You can list your current automatic model evaluation jobs that you've already created using the AWS CLI, or a supported AWS SDK. In the Amazon Bedrock console, you can also view a table containing your current model evaluation jobs.

The following examples show you how to find your model evaluation jobs using the AWS Management Console, AWS CLI and SDK for Python.

------
#### [ Amazon Bedrock console ]

1. Open the Amazon Bedrock console: [https://console.aws.amazon.com/bedrock/home](https://console.aws.amazon.com/bedrock/home)

1. In the navigation pane, choose **Model evaluation**.

1. In the **Model Evaluation Jobs** card, you can find a table that lists the model evaluation jobs you have already created.

------
#### [ AWS CLI ]

In the AWS CLI, you can use the `help` command to view parameters are required, and which parameters are optional when using `list-evaluation-jobs`.

```
aws bedrock list-evaluation-jobs help
```

The follow is an example of using `list-evaluation-jobs` and specifying that maximum of 5 jobs be returned. By default jobs are returned in descending order from the time when they where started.

```
aws bedrock list-evaluation-jobs --max-items 5
```

------
#### [ SDK for Python ]

The following examples show how to use the AWS SDK for Python to find a model evaluation job you have previously created. 

```
import boto3
client = boto3.client('bedrock')

job_request = client.list_evaluation_jobs(maxResults=20)

print (job_request)
```

------