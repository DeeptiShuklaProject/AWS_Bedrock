

# Stop a model evaluation job in Amazon Bedrock
<a name="model-evaluation-jobs-judge-management-stop"></a>

You can stop a model evaluation job that is currently processing using the AWS Management Console, AWS CLI, or a supported AWS SDK.

The following examples show you how to stop a model evaluation job using the AWS Management Console, AWS CLI, and SDK for Python

------
#### [ Amazon Bedrock console ]

The following example shows you how to stop a model evaluation job using the AWS Management Console

1. Open the Amazon Bedrock console: [https://console.aws.amazon.com/bedrock/home](https://console.aws.amazon.com/bedrock/home)

1. In the navigation pane, choose **Model evaluation**.

1. In the **Model Evaluation Jobs** card, you can find a table that lists the model evaluation jobs you have already created.

1. Select the radio button next to your job's name.

1. Then, choose **Stop evaluation**.

------
#### [ SDK for Python ]

The following example shows you how to stop a model evaluation job using the SDK for Python

```
import boto3
					client = boto3.client('bedrock')
					response = client.stop_evaluation_job(
					## The ARN of the model evaluation job you want to stop.
					jobIdentifier='arn:aws:bedrock:us-west-2:444455556666:evaluation-job/fxaqujhttcza'
					)

					print(response)
```

------
#### [ AWS CLI ]

In the AWS CLI, you can use the `help` command to see which parameters are required, and which parameters are optional when specifying `add-something` in the AWS CLI.

```
aws bedrock create-evaluation-job help
```

The following example shows you how to stop a model evaluation job using the AWS CLI

```
aws bedrock stop-evaluation-job --job-identifier arn:aws:bedrock:us-west-2:444455556666:evaluation-job/fxaqujhttcza
```

------