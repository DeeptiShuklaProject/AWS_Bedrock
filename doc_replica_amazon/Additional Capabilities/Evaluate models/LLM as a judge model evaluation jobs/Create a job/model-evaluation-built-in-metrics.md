

# Create a model evaluation job using built-in metrics
<a name="model-evaluation-built-in-metrics"></a>

To create a job using the following instructions, you need a prompt dataset. If you haven't already created one, see [Create a prompt dataset for a model evaluation job that uses a model as judge](model-evaluation-prompt-datasets-judge.md).

------
#### [ Console ]

1. Open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/home).

1. In the left-hand pane under **Inference and assessment**, select **Evaluations**.

1. In the **Model evaluations** pane, choose **Create** and select **Automatic: Model as a judge**.

1. Enter your model evaluation details by doing the following:

   1. In the **Model evaluation details** pane under **Evaluation name**, enter a name for your evaluation job. The name you choose must be unique within your AWS Region.

   1. Optionally, under **Description - *optional***, enter a description for your evaluation job.

   1. Under **Evaluator model**, choose **Select model** and select the judge model you want to perform your evaluation.

1. Enter the inference source for your evaluation job. With Amazon Bedrock model evaluations, you can either evaluate the performance of Amazon Bedrock models, or of other models by providing your own inference response data in the [prompt dataset](model-evaluation-prompt-datasets-judge.md). To select an Amazon Bedrock model, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bedrock models**.

   1. Under **Select model**, choose **Select model**.

   1. In the pop-up, select the model you want to evaluate and choose **Apply**.

   1. (Optional) to change the model's inference parameters, for **Inference configuration**, choose **update**.

1. To bring your own inference response data, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bring your own inference responses**.

   1. For **Source name**, enter a name for the model you used to create the response data. The name you enter must match the `modelIdentifier` parameter in your [prompt dataset](model-evaluation-prompt-datasets-judge.md#model-evaluation-prompt-datasets-judge-byoir).

1. Select the built-in metrics you want the evaluator model to score your generator model's responses against by selecting at least one metric in the **Metrics** pane.

1. Define your input and output locations for your dataset and results by doing the following:

   1. In the **Datasets** pane under **Choose a prompt dataset**, enter the Amazon S3 URI for your prompt dataset, or choose **Browse S3** and select your file. To see a definition of the required prompt dataset format for a model-as-a-judge evaluation job, see [Create a prompt dataset for a model evaluation job that uses a model as judge](model-evaluation-prompt-datasets-judge.md).

   1. Under **Evaluation results**, enter an Amazon S3 location for Amazon Bedrock to save your results, or choose **Browse S3** to select a location.

1. Under **Amazon Bedrock IAM role - Permissions**, select **Create and use a new service role** to have Amazon Bedrock create a new IAM role for the evaluation job, or select **Use an existing service role** to pick an existing IAM role. For a list of the required permissions to create and run an evaluation job, see [Prerequisites](model-evaluation-judge-create.md#model-evaluation-judge-create-prereqs).

1. (Optional) to use your own KMS key to encrypt your evaluation data, under **KMSkey - *Optional***, check **Customize encryption settings (advanced)** and select your AWS KMS key. By default, Amazon Bedrock encrypts your evaluation job data with an AWS-owned KMS key.

1. Choose **Create** to finish creating your evaluation job.

------
#### [ AWS CLI ]
+   
**Example AWS CLI command and JSON file to create an evaluation job for an Amazon Bedrock model**  

  ```
  aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
  ```

  ```
  {
      "jobName": {{"model-eval-llmaj"}},
      "roleArn": "arn:aws:iam::{{111122223333}}:role/Amazon-Bedrock-ModelAsAJudgeTest",
      "applicationType": "ModelEvaluation",
      "evaluationConfig": {
          "automated": {
              "datasetMetricConfigs": [
                  {
                      "taskType": "General",
                      "dataset": {
                          "name": "text_dataset",
                          "datasetLocation": {
                              "s3Uri": "s3://amzn-s3-demo-bucket/input_datasets/text_dataset_input.jsonl"
                          }
                      },
                      "metricNames": [
                          "Builtin.Correctness",
                          "Builtin.Completeness"
                      ]
                  }
              ],
              "evaluatorModelConfig": {
                  "bedrockEvaluatorModels": [
                      {
                          "modelIdentifier": "anthropic.claude-3-haiku-20240307-v1:0"
                      }
                  ]
              }
          }
      },
      "inferenceConfig": {
          "models": [
              {
                  "bedrockModel": {
                      "modelIdentifier": "anthropic.claude-v2",
                      "inferenceParams": "{\"inferenceConfig\":{\"maxTokens\":512,\"temperature\":1,\"topP\":0.999,\"stopSequences\":[\"stop\"]},\"additionalModelRequestFields\":{\"top_k\": 128}}"
                  }
              }
          ]
      },
      "outputDataConfig": {
          "s3Uri": "s3://amzn-s3-demo-bucket/output_data/"
      }
  }
  ```  
**Example AWS CLI command and JSON file to create an evaluation job where you provide your own inference response data**  

  ```
  aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
  ```

  ```
  {
      "jobName": {{"model-eval-llmaj"}},
      "roleArn": "arn:aws:iam::{{111122223333}}:role/Amazon-Bedrock-ModelAsAJudgeTest",
      "evaluationConfig": {
          "automated": {
              "datasetMetricConfigs": [
                  {
                      "taskType": "General",
                      "dataset": {
                          "name": "text_dataset",
                          "datasetLocation": {
                              "s3Uri": "{{s3://amzn-s3-demo-bucket/input/model-eval/fitness-dataset-model-eval-byoi.jsonl}}"
                          }
                      },
                      "metricNames": [
                          "Builtin.Correctness",
                          "Builtin.Completeness"
                      ]
                  }
              ],
              "evaluatorModelConfig": {
                  "bedrockEvaluatorModels": [
                      {
                          "modelIdentifier": "us.meta.llama3-1-70b-instruct-v1:0"
                      }
                  ]
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
          "s3Uri": "s3://amzn-s3-demo-bucket/output/"
      }
  }
  ```

------