

# Create a model evaluation job using custom metrics
<a name="model-evaluation-custom-metrics-create-job"></a>

To create an evaluation job that uses a custom metric, you need to supply the following:
+ A prompt containing detailed instructions for the judge model to use
+ The evaluator model you want to use for your custom metrics

You can also specify a rating scale (output schema) that the judge model can use to rate the generator model's responses.

You can create an evaluation job with custom metrics using the AWS Management Console, AWS Command Line Interface (AWS CLI), or using the Amazon Bedrock API. Use the following instructions to create your evaluation job. For instructions and guidance on creating the prompt for your metric and on defining the rating scale you specify during creation, see [Create a prompt for a custom metric](model-evaluation-custom-metrics-prompt-formats.md).

When you create an evaluation job with one or more custom metrics, Amazon Bedrock stores your metric definitions as JSON files in the output S3 bucket you specify. You can access these files by navigating to `s3://{{S3-output-bucket-name}}/{{job-name}}/{{job-uuid}}/custom_metrics`. To see the format for JSON definitions of custom metrics, see [Creating a JSON file to create a custom metric](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-json).

To create a job using the following instructions, you also need a prompt dataset. If you haven't already created one, see [Create a prompt dataset for a model evaluation job that uses a model as judge](model-evaluation-prompt-datasets-judge.md).

Use the following instructions to create a model-as-a-judge evaluation job with one or more custom metrics

------
#### [ Console ]

1. Open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/home).

1. In the left-hand pane under **Inference and assessment**, select **Evaluations**.

1. In the **Model evaluations** pane, choose **Create** and select **Automatic: Model as a judge**.

1. Enter your model evaluation details by doing the following:

   1. In the **Model evaluation details** pane under **Evaluation name**, enter a name for your evaluation job. The name you choose must be unique within your AWS Region.

   1. Optionally, under **Description - *optional***, enter a description for your evaluation job.

   1. Under **Evaluator model**, choose **Select model** and select the judge model you want to perform your evaluation job. Note that the model you select here is used to evaluate your generator model against any built-in metrics you select. You can choose a different evaluator model to use for your custom metrics in a later step.

1. Enter the inference source for your evaluation job. With Amazon Bedrock model evaluations, you can either evaluate the performance of Amazon Bedrock models, or of other models by providing your own inference response data in the [prompt dataset](model-evaluation-prompt-datasets-judge.md). To select an Amazon Bedrock model, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bedrock models**.

   1. Under **Select model**, choose **Select model**.

   1. In the pop-up, select the model you want to evaluate and choose **Apply**.

   1. (Optional) to change the model's inference parameters, for **Inference configuration**, choose **update**.

1. To bring your own inference response data, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bring your own inference responses**.

   1. For **Source name**, enter a name for the model you used to create the response data. The name you enter must match the `modelIdentifier` parameter in your [prompt dataset](model-evaluation-prompt-datasets-judge.md#model-evaluation-prompt-datasets-judge-byoir).

1. Choose any built-in metrics you want the evaluator model to score your generator model's responses against by selecting them in the **Metrics** pane.

1. To add one more custom metrics, begin by selecting the evaluator model you want to use to evaluate your metrics. In the **Custom metrics** pane, do the following:

   1. Choose **Select model**.

   1. In the pop-up, select the model you want to use.

   1. Choose **Apply**.

1. Under **Metric name**, enter a name for your metric.

1. You can configure your metric in three ways: by providing a JSON file that specifies the metric, by editing an existing built-in metric prompt from a template, or by entering a prompt directly in the console for the evaluator model to use.

   To create a metric from a JSON file, do the following:

   1. Under **Choose metric type**, select **Import JSON file**.

   1. Under **Import JSON file**, choose **Choose file**.

   1. Using the file picker, select the JSON file with your custom metric definition and choose **Open**. To learn about the schema for specifying a custom metric using a JSON file, and to see some example files, see [Creating a JSON file to create a custom metric](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-json).

   1. (Optional) to create another metric, choose **Add custom metrics**. You can create up to 10 custom metrics for an evaluation job.

      When you have finished creating your custom metrics, proceed to step 13 to configure your datasets for the evaluation job.

1. To create a custom metric from a built-in template, do the following:

   1. Under **Choose metric type**, select **Use a template**.

   1. Under **Select a template**, use the dropdown list to choose an existing built-in metric prompt to use as a starting point for your custom metric.

   1. Under **Instructions** edit the prompt you selected to suit your own use case. For best practices and for a list of required elements when creating a custom metric prompt, see [Create a prompt for a custom metric](model-evaluation-custom-metrics-prompt-formats.md).

   1. If you want your evaluation job to output structured outputs with ranked scores, leave **Output schema enabled (recommended)** checked. Your metric configuration doesn't need to include an output schema, but we recommend that you define one. If you don't use a schema, the results you view will include only explanations without scores or data visualization.

   1. Under **Scale type**, select either **Numerical** or **String** according to your use case, and enter your scale and description definitions in the text boxes. For guidance and best practices on defining output scales, see [Specifying an output schema (rating scale)](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-schema).

   1. (Optional) to create another metric, choose **Add custom metrics**. You can create up to 10 custom metrics for an evaluation job.

      When you have finished creating your custom metrics, proceed to step 13 to configure your datasets for the evaluation job.

1. To create a custom metric from scratch in the console, do the following:

   1. Under **Choose metric type**, select **Custom**.

   1. Under **Instructions**, enter the prompt for your custom metric directly in the text box. For best practices and for a list of required elements when creating a custom metric prompt, see [Prompt construction and best practices](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-create).

   1. If you want your evaluation job to output structured outputs with ranked scores, leave **Output schema enabled (recommended)** checked. Your metric configuration doesn't need to include an output schema, but we recommend that you define one. If you don't use a schema, the results you view will include only explanations without scores or data visualization.

   1. Under **Scale type**, select either **numerical** or **String** according to your use case, and enter your scale and description definitions in the text boxes. For guidance and best practices on defining output scales, see [Specifying an output schema (rating scale)](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-schema).

   1. (Optional) to create another, choose **Add custom metrics**. You can create up to 10 custom metrics for an evaluation job.

      When you have finished creating your custom metrics, proceed to the next step to configure your datasets for the evaluation job.

1. Define your input and output locations for your dataset and results by doing the following:

   1. In the **Datasets** pane under **Choose a prompt dataset**, enter the Amazon S3 URI for your prompt dataset, or choose **Browse S3** and select your file. To see a definition of the required prompt dataset format for a model-as-a-judge evaluation job, see [Create a prompt dataset for a model evaluation job that uses a model as judge](model-evaluation-prompt-datasets-judge.md).

   1. Under **Evaluation results**, enter an Amazon S3 location for Amazon Bedrock to save your results, or choose **Browse S3** to select a location.

1. Under **Amazon Bedrock IAM role - Permissions**, select **Create and use a new service role** to have Amazon Bedrock create a new IAM role for the evaluation job, or select **Use an existing service role** to pick an existing IAM role. For a list of the required permissions to create and run an evaluation job, see [Prerequisites](model-evaluation-judge-create.md#model-evaluation-judge-create-prereqs).

1. (Optional) to use your own KMS key to encrypt your evaluation data, under **KMSkey - *Optional***, check **Customize encryption settings (advanced)** and select your AWS KMS key. By default, Amazon Bedrock encrypts your evaluation job data with an AWS-owned KMS key.

1. Choose **Create** to finish creating your evaluation job.

------
#### [ AWS CLI ]

The following examples show how to make a `create-evaluation-job` request using the AWS CLI for a job that includes a custom metric. Ensure that `applicationType` is specified as `ModelEvaluation`.

You can either evaluate the performance of models in Amazon Bedrock, or you can evaluate other models by providing your own inference response data as part of the prompt dataset. To learn more about how to create a prompt dataset using your own inference responses, see [Create a prompt dataset for a model evaluation job that uses a model as judge](model-evaluation-prompt-datasets-judge.md).

**Example AWS CLI command and JSON file to create an evaluation job with custom metrics for an Amazon Bedrock model**  

```
aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
```

```
{
    "jobName": "custom-metrics-maaj",
    "applicationType": "ModelEvaluation",
    "roleArn": "arn:aws:iam::{{111122223333}}:role/service-role/Amazon-Bedrock-Custom-Metric",
    "evaluationConfig": {
        "automated": {
            "datasetMetricConfigs": [{
                "taskType": "General",
                "dataset": {
                    "name": "text_dataset",
                    "datasetLocation": {
                        "s3Uri": "s3://amzn-s3-demo-bucket/input_datasets/text_dataset_input.jsonl"
                    }
                },
                 "metricNames": [
                        "CustomMetric-Correctness-FloatRatingScale"
                    ]
            }],
            "customMetricConfig": {
                "customMetrics": [{
                        "customMetricDefinition": {
                            "name": "CustomMetric-Correctness-FloatRatingScale",
                            "instructions": "{{<Your complete custom metric prompt including at least one {{input variable}}>}}",
                            "ratingScale": [{
                                    "definition": "Not at all",
                                    "value": {
                                        "floatValue": 0
                                    }
                                },
                                {
                                    "definition": "Somewhat",
                                    "value": {
                                        "floatValue": 1
                                    }
                                },
                                {
                                    "definition": "Mostly",
                                    "value": {
                                        "floatValue": 2
                                    }
                                }
                            ]
                        }
                    }
                ],
                "evaluatorModelConfig": {
                    "bedrockEvaluatorModels": [{
                        "modelIdentifier": "anthropic.claude-3-haiku-20240307-v1:0"
                    }]
                }
            },
            "evaluatorModelConfig": {
                "bedrockEvaluatorModels": [{
                    "modelIdentifier": "mistral.mistral-large-2402-v1:0"
                }]
            }
        }
    },
    "inferenceConfig": {
        "models": [{
            "bedrockModel": {
                "modelIdentifier": "anthropic.claude-v2",
                "inferenceParams": "{\"textGenerationConfig\":{\"maxTokenCount\":256,\"temperature\":0.25,\"topP\":0.25}}"
            }
        }]
    },
    "outputDataConfig": {
        "s3Uri": "s3://amzn-s3-demo-destination-bucket/output/"
    }
}
```
The example JSON file contains two `evaluatorModelConfig` objects. The one inside the `customMetricConfig` object specifies the evaluator model to be used with custom metrics. The other instance specifies the model to use for built-in metrics. Take care to specify these two objects correctly.

**Example AWS CLI command and JSON file to create an evaluation job with custom metrics where you provide your own inference response data**  

```
aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
```

```
{
    "jobName": "custom-metrics-maaj",
    "applicationType": "ModelEvaluation",
    "roleArn": "arn:aws:iam::{{111122223333}}:role/service-role/Amazon-Bedrock-Custom-Metric",
    "evaluationConfig": {
        "automated": {
            "datasetMetricConfigs": [{
                "taskType": "General",
                "dataset": {
                    "name": "text_dataset",
                    "datasetLocation": {
                        "s3Uri": "s3://amzn-s3-demo-bucket/input_datasets/text_dataset_input.jsonl"
                    }
                },
                "metricNames": [
                        "CustomMetric-Correctness-FloatRatingScale"
                    ]
            }],
            "customMetricConfig": {
                "customMetrics": [{
                        "customMetricDefinition": {
                            "name": "CustomMetric-Correctness-FloatRatingScale",
                            "instructions": "{{<Your complete custom metric prompt including at least one {{input variable}}>}}",
                            "ratingScale": [{
                                    "definition": "Not at all",
                                    "value": {
                                        "floatValue": 0
                                    }
                                },
                                {
                                    "definition": "Somewhat",
                                    "value": {
                                        "floatValue": 1
                                    }
                                },
                                {
                                    "definition": "Mostly",
                                    "value": {
                                        "floatValue": 2
                                    }
                                }
                            ]
                        }
                    }
                ],
                "evaluatorModelConfig": {
                    "bedrockEvaluatorModels": [{
                        "modelIdentifier": "anthropic.claude-3-haiku-20240307-v1:0"
                    }]
                }
            },
            "evaluatorModelConfig": {
                "bedrockEvaluatorModels": [{
                    "modelIdentifier": "mistral.mistral-large-2402-v1:0"
                }]
            }
        }
    },
     "inferenceConfig": {
        "models": [
            {
                "precomputedInferenceSource": {
                    "inferenceSourceIdentifier": "my_model"
                }
            }
        ]
    },
    "outputDataConfig": {
        "s3Uri": "s3://amzn-s3-demo-destination-bucket/output/"
    }
}
```
The example JSON file contains two `evaluatorModelConfig` objects. The one inside the `customMetricConfig` object specifies the evaluator model to be used with custom metrics. The other instance specifies the model to use for built-in metrics. Take care to specify these two objects correctly.

------