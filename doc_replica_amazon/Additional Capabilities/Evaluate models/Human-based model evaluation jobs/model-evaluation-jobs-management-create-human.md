

# Create a human-based model evaluation job
<a name="model-evaluation-jobs-management-create-human"></a>

The following examples show how to create a model evaluation job that uses human workers.

**Console**

**To create a model evaluation job that uses human workers**

1. Open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/).

1. In the navigation pane, under **Inference and Assessment**, select **Evaluations**.

1. In the **Model evaluation** pane, under **Human**, choose **Create** and select **Human: Bring your own work team**.

1. On the **Specify job details** page provide the following.

   1. **Evaluation name** — Give the model evaluation job a name that describes the job. This name is shown in your model evaluation job list. The name must be unique in your account in an AWS Region. 

   1. **Description** (Optional) — Provide an optional description.

   1. Choose **Next**.

1. On the **Set up evaluation** page, under **Inference source**, select the source for your model evaluation. You can evaluate the performance of Amazon Bedrock models, or of other models by providing your own inference response data in your prompt dataset. You can select up to two inference sources. For jobs with two sources, you don't have to choose the same type for both sources; you can select one Amazon Bedrock model, and provide your own inference response data for the second source. To evaluate Amazon Bedrock models, do the following:

   1. Under **Select source**, select **Bedrock models**.

   1. Choose **Select model** to choose the model you want to evaluate.

   1. To select a second model, choose **Add model** and repeat the preceding steps.

1. To bring your own inference response data, do the following:

   1. Under **Select source**, select **Bring your own inference responses**.

   1. For **Source Name**, enter a name for the model you used to create the response data. The name you enter must match the `modelIdentifier` parameter in your [prompt dataset](model-evaluation-prompt-datasets-custom-human.md#model-evaluation-prompt-datasets-custom-human-byoir).

   1. To add a second source, choose **Add model** and repeat the preceding steps.

1. For **Task type**, select the type of task you want the model to perform during the model evaluation job. All instructions for the model must be included in the prompts themselves. The task type does not control the model's responses.

1. In the **Datasets** pane, provide the following.

   1. Under **Choose a prompt dataset**, specify the S3 URI of your prompt dataset file or choose **Browse S3** to see available S3 buckets. You can have a maximum of 1000 prompts in a custom prompt dataset.

   1. Under **Evaluation results destination**, specify the S3 URI of the directory where you want the results of your model evaluation job saved, or choose **Browse S3** to see available S3 buckets.

1. (Optional) Under **KMS key - Optional**, provide the ARN of a customer managed key you want to use to encrypt your model evaluation job.

1. In the **Amazon Bedrock IAM role – Permissions** pane, do the following. To learn more about the required permissions for model evaluations, see [Service role requirements for model evaluation jobs](model-evaluation-security-service-roles.md).

   1. To use an existing Amazon Bedrock service role, choose **Use an existing role**. Otherwise, use **Create a new role** to specify the details of your new IAM service role.

   1. In **Service role name**, specify the name of your IAM service role.

   1. When ready, choose **Create role** to create the new IAM service role. 

1. Choose **Next**.

1. Under **Work team**, use the **Select team** dropdown to select an existing team, or create a new team by doing the following:

   1. Under **Team name**, enter a name for your team.

   1. Under **Email addresses**, enter the email addresses of the human workers in your team.

   1. Under **Number of workers per prompt**, select the number of workers who evaluate each prompt. After the responses for each prompt have been reviewed by the number of workers you selected, the prompt and its responses will be taken out of circulation from the work team. The final results report will include all ratings from each worker.
**Important**  
Large language models are known to occasionally hallucinate and produce toxic or offensive content. Your workers may be shown toxic or offensive material during this evaluation. Ensure you take proper steps to train and notify them before they work on the evaluation. They can decline and release tasks or take breaks during the evaluation while accessing the human evaluation tool.

1. Under **Human workflow IAM role - Permissions**, select an existing role, or select **Create a new role**.

1. Choose **Next**.

1. Under **Evaluation instructions**, provide instructions for completing the task. You can preview the evaluation UI that your work team uses to evaluate the responses, including the metrics, rating methods, and your instructions. This preview is based on the configuration you have created for this job.

1. Choose **Next**.

1. Review your configuration and choose **Create** to create the job.
**Note**  
Once the job has successfully started, the status changes to **In progress**. When the job has finished, the status changes to **Completed**. While a model evaluation job is still **In progress**, you can choose to the stop the job before all the models' responses have been evaluated by your work team. To do so, choose **Stop evaluation** on the model evaluation landing page. This will change the **Status** of the model evaluation job to **Stopping**. Once the model evaluation job has successfully stopped, you can delete the model evaluation job.

**API and AWS CLI**

When you create a human-based model evaluation job outside of the Amazon Bedrock console, you need to create an Amazon SageMaker AI flow definition ARN.

The flow definition ARN is where a model evaluation job's workflow is defined. The flow definition is used to define the worker interface and the work team you want assigned to the task, and connecting to Amazon Bedrock.

For model evaluation jobs started using Amazon Bedrock API operations you *must* create a flow definition ARN using the AWS CLI or a supported AWS SDK. To learn more about how flow definitions work, and creating them programmatically, see [Create a Human Review Workflow (API)](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-create-flow-definition.html#a2i-create-human-review-api) in the *SageMaker AI Developer Guide*.

In the [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateFlowDefinition.html](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateFlowDefinition.html) you must specify `AWS/Bedrock/Evaluation` as input to the `AwsManagedHumanLoopRequestSource`. The Amazon Bedrock service role must also have permissions to access the output bucket of the flow definition.

The following is an example request using the AWS CLI. In the request, the `HumanTaskUiArn` is a SageMaker AI owned ARN. In the ARN, you can only modify the AWS Region.

```
aws sagemaker create-flow-definition --cli-input-json '
{
	"FlowDefinitionName": "human-evaluation-task01",
	"HumanLoopRequestSource": {
        "AwsManagedHumanLoopRequestSource": "AWS/Bedrock/Evaluation"
    },
    "HumanLoopConfig": {
		"WorkteamArn": "arn:aws:sagemaker:AWS Region:111122223333:workteam/private-crowd/my-workteam",
		## The Task UI ARN is provided by the service team, you can only modify the AWS Region.
		"HumanTaskUiArn":"arn:aws:sagemaker:AWS Region:394669845002:human-task-ui/Evaluation"
		"TaskTitle": "Human review tasks",
		"TaskDescription": "Provide a real good answer",
		"TaskCount": 1,
		"TaskAvailabilityLifetimeInSeconds": 864000,
		"TaskTimeLimitInSeconds": 3600,
		"TaskKeywords": [
		    "foo"
        ]
    },
    "OutputConfig": {
        "S3OutputPath": "s3://amzn-s3-demo-destination-bucket"
    },
    "RoleArn": "arn:aws:iam::111122223333:role/SageMakerCustomerRoleArn"
}'
```

After creating your flow definition ARN, use the following examples to create human-based model evaluation job using the AWS CLI or a supported AWS SDK.

------
#### [ AWS CLI ]

The following example command and JSON file shows you how to create a model evaluation job using human workers where you provide your own inference response data. To learn how to specify a prompt dataset for a model evaluation job with human workers, see [Create a custom prompt dataset for a model evaluation job that uses human workers](model-evaluation-prompt-datasets-custom-human.md).

**Example AWS CLI command and JSON file to create an evaluation job using your own inference response data**  

```
aws bedrock create-evaluation-job --cli-input-json file://my_eval_job.json
```

```
{
    "jobName": {{"model-eval-llama-vs-my-other-model"}},
    "roleArn": {{"arn:aws:iam::111122223333:role/service-role/Amazon-Bedrock-IAM-Role-20250218T223671"}},
    "evaluationConfig": {
        "human": {
            "customMetrics": [
                {
                    "description": "Measures the organization and structure of a generated text.",
                    "name": "Coherence",
                    "ratingMethod": "ThumbsUpDown"
                },
                {
                    "description": "Indicates the accuracy of a generated text.",
                    "name": "Accuracy",
                    "ratingMethod": "ComparisonChoice"
                }
            ],
            "datasetMetricConfigs": [
                {
                    "dataset": {
                        "datasetLocation": {
                            "s3Uri": "s3://amzn-s3-demo-bucket/input/model-eval/fitness-dataset-model-eval-byoir-2-models.jsonl"
                        },
                        "name": "dataset1"
                    },
                    "metricNames": [
                        "Coherence",
                        "Accuracy"
                    ],
                    "taskType": "Generation"
                }
            ],
            "humanWorkflowConfig": {
                "flowDefinitionArn": {{"arn:aws:sagemaker:us-east-1:111122223333:flow-definition/bedrock-fitness-human-byoir"}},
                "instructions": "<h3>The following are the metrics and their descriptions for this evaluation</h3>\n<p><strong>Coherence</strong>: Measures the organization and structure of a generated text. - <em>Thumbs up/down</em>\n<strong>Accuracy</strong>: Indicates the accuracy of a generated text. - <em>Choice buttons</em></p>\n<h3>Instructions for how to use the evaluation tool</h3>\n<p>The evaluation creator should use this space to write detailed descriptions for every rating method so your evaluators know how to properly rate the responses with the buttons on their screen.</p>\n<h4>For example:</h4>\n<p>If using <strong>Likert scale - individual</strong>, define the 1 and 5 of the 5 point Likert scale for each metric so your evaluators know if 1 or 5 means favorable/acceptable/preferable.\nIf using <strong>Likert scale - comparison</strong>, describe what the evaluator is looking for to determine their preference between two responses.\nIf using <strong>Choice buttons</strong>, describe what is preferred according to your metric and its description.\nIf using <strong>Ordinal ranking</strong>, define what should receive a #1 ranking according to your metric and its description.\nIf using <strong>Thumbs up/down</strong>, define what makes an acceptable response according to your metric and its description.</p>\n<h3>Describing your ground truth responses if applicable to your dataset</h3>\n<p>Describe the purpose of your ground truth responses that will be shown on screen next to each model response. Note that the ground truth responses you provide are not rated/scored by the evaluators - they are meant to be a reference standard for comparison against the model responses.</p>"
            }
        }
    },
    "inferenceConfig": {
        "models": [
            {
                "precomputedInferenceSource": {
                    "inferenceSourceIdentifier": "llama-3-1-80b"
                }
            },
            {
                "precomputedInferenceSource": {
                    "inferenceSourceIdentifier": "my_other_model"
                }
            }
        ]
    },
    "outputDataConfig": {
        "s3Uri": "s3://amzn-s3-demo-bucket/output/"
    }
}
```

------
#### [ SDK for Python ]

The following code example shows you how to create a model evaluation job that uses human workers via the SDK for SDK for Python.

```
import boto3
client = boto3.client('bedrock')

job_request = client.create_evaluation_job(
    jobName="111122223333-job-01",
    jobDescription="two different task types",
    roleArn="arn:aws:iam::111122223333:role/example-human-eval-api-role",
    inferenceConfig={
        ## You must specify and array of models
        "models": [
            {
                "bedrockModel": {
                    "modelIdentifier":"arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-text-lite-v1",
                    "inferenceParams":"{\"inferenceConfig\":{\"maxTokens\": 512,\"temperature\":0.7,\"topP\":0.9}}"
                }

            },
            {
                "bedrockModel": {
                    "modelIdentifier": "anthropic.claude-v2",
                    "inferenceParams": "{\"inferenceConfig\":{\"maxTokens\":512,\"temperature\":1,\"topP\":0.999,\"stopSequences\":[\"stop\"]},\"additionalModelRequestFields\":{\"top_k\": 128}}"
                }
            }
        ]
    },
    outputDataConfig={
        "s3Uri":"s3://job-bucket/outputs/"
    },
    evaluationConfig={
        "human": {
        "humanWorkflowConfig": {
            "flowDefinitionArn": "arn:aws:sagemaker:us-west-2:111122223333:flow-definition/example-workflow-arn",
            "instructions": "some human eval instruction"
        },
        "customMetrics": [
            {
                "name": "IndividualLikertScale",
                "description": "testing",
                "ratingMethod": "IndividualLikertScale"
            }
        ],
        "datasetMetricConfigs": [
            {
                "taskType": "Summarization",
                "dataset": {
                    "name": "Custom_Dataset1",
                    "datasetLocation": {
                        "s3Uri": "s3://job-bucket/custom-datasets/custom-trex.jsonl"
                    }
                },
                "metricNames": [
                  "IndividualLikertScale"
                ]
            }
        ]
      }

    }
)

print(job_request)
```

------