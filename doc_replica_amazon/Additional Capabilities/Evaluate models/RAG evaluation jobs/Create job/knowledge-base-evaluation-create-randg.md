

# Creating a retrieve-and-generate RAG evaluation job
<a name="knowledge-base-evaluation-create-randg"></a>

You can create a RAG evaluation job using the AWS Management Console, AWS CLI, or a supported AWS SDK.

This type of job requires access to an evaluator model. For a list of supported evaluator models, see [Supported models](evaluation-kb.md#evaluation-kb-supported). 

To create a job using the following instructions, you need a prompt dataset. If you haven't already created one, see [Create a prompt dataset for a RAG evaluation in Amazon Bedrock](knowledge-base-evaluation-prompt.md).

------
#### [ Console ]

1. Open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/home).

1. In the left-hand pane under **Inference and assessment**, select **Evaluations**.

1. In the **RAG evaluations** pane, choose **Create**.

1. Enter your RAG evaluation details by doing the following:

   1. In the **Evaluation details** pane under **Evaluation name**, enter a name for your evaluation job. The name you choose must be unique within your AWS Region.

   1. Optionally, under **Description - *optional***, enter a description for your evaluation job.

   1. Under **Evaluator model**, choose **Select model** and select the evaluator model you want to perform your evaluation.

1. Enter the inference source for your evaluation job. With Amazon Bedrock RAG evaluations, you can either evaluate the performance of Amazon Bedrock Knowledge Bases, or of other RAG sources by providing your own inference response data in the [prompt dataset](knowledge-base-evaluation-prompt.md). To select an Amazon Bedrock Knowledge Base, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bedrock Knowledge Base**.

   1. Under **Choose a Knowledge Base**, select a Knowledge Base using the dropdown list.

1. To bring your own inference response data, do the following:

   1. In the **Inference source** pane, under **Select source** select **Bring your own inference responses**.

   1. For **Source name**, enter a name for the RAG source you used to create the response data. The name you enter must match the `knowledgeBaseIdentifier` parameter in your [prompt dataset](knowledge-base-evaluation-prompt.md).

1. In the **Inference source** pane, under **Evaluation type**, select **Retrieval and response generation**.

1. Select the built-in metrics you want the evaluator model to use by selecting at least one metric in the **Metrics** pane.

1. Define your input and output locations for your dataset and results by doing the following:

   1. In the **Datasets** pane under **Choose a prompt dataset**, enter the Amazon S3 URI for your prompt dataset, or choose **Browse S3** and select your file. To see a definition of the required prompt dataset format for a retrieve-only evaluation job, see [Create a prompt dataset for retrieve-only RAG evaluation jobs](knowledge-base-evaluation-prompt-retrieve.md).

   1. Under **Evaluation results**, enter an Amazon S3 location for Amazon Bedrock to save your results, or choose **Browse S3** to select a location.

1. Under **Amazon Bedrock IAM role - Permissions**, select **Create and use a new service role** to have Amazon Bedrock create a new IAM role for the evaluation job, or select **Use an existing service role** to pick an existing IAM role. For a list of the required permissions to create and run an evaluation job, see [Prerequisites](knowledge-base-evaluation-create.md#knowledge-base-evaluation-create-prereqs).

1. (Optional) to use your own KMS key to encrypt your evaluation data, under **KMSkey - *Optional***, check **Customize encryption settings (advanced)** and select your AWS KMS key. By default, Amazon Bedrock encrypts your evaluation job data with an AWS-owned KMS key.

1. Choose **Create** to finish creating your evaluation job.

------
#### [ AWS CLI ]

**Create a retrieve-and-generate evaluation job for an Amazon Bedrock Knowledge Base**
+ Run the following AWS CLI command using the example JSON file.

  ```
  aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
  ```

  ```
  {
      "jobName": {{"my_rag_eval"}},
      "roleArn": {{"arn:aws:iam::111122223333:role/service-role/Amazon-Bedrock-IAM-Role-Amazon-Bedrock-IAM-Role-20250218T063974"}},
      "applicationType": "RagEvaluation",
      "evaluationConfig": {
          "automated": {
              "datasetMetricConfigs": [
                  {
                      "taskType": "General",
                      "dataset": {
                          "name": "text_dataset",
                          "datasetLocation": {
                              "s3Uri": "s3://amzn-s3-demo-bucket/input/retrieve-and-generate/rng-eval-byoir.jsonl"
                          }
                      },
                      "metricNames": [
                          "Builtin.Correctness",
                          "Builtin.Completeness",
                          "Builtin.Helpfulness",
                          "Builtin.LogicalCoherence",
                          "Builtin.Faithfulness",
                          "Builtin.Harmfulness",
                          "Builtin.Stereotyping",
                          "Builtin.Refusal",
                          "Builtin.CitationCoverage",
                          "Builtin.CitationPrecision"
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
          "ragConfigs": [
              {
                  "knowledgeBaseConfig": {
                      "retrieveAndGenerateConfig": {
                          "type": "KNOWLEDGE_BASE",
                          "knowledgeBaseConfiguration": {
                              "knowledgeBaseId": {{"≪Your Knowledge Base ID>"}},
                              "modelArn": "mistral.mistral-large-2402-v1:0",
                              "generationConfiguration": {
                                  "promptTemplate": {
                                      "textPromptTemplate": "$search_results$ hello world template"
                                  }
                              },
                              "orchestrationConfiguration": {
                                  "queryTransformationConfiguration": {
                                      "type": "QUERY_DECOMPOSITION"
                                  }
                               }
                          }
                      }
                  }
              }
          ]
      },
      "outputDataConfig": {
          "s3Uri": "s3://amzn-s3-demo-bucket/output/"
      }
  }
  ```

**Create a retrieve-and-generate evaluation job with your own inference response data**
+ Run the following AWS CLI command using the example JSON file.

  ```
  aws bedrock create-evaluation-job --cli-input-json file://{{my_eval_job.json}}
  ```

  ```
  {
      "jobName": {{"my_rag_eval"}},
      "roleArn": {{"arn:aws:iam::111122223333:role/service-role/Amazon-Bedrock-IAM-Role-Amazon-Bedrock-IAM-Role-20250218T063974"}},
      "applicationType": "RagEvaluation",
      "evaluationConfig": {
          "automated": {
              "datasetMetricConfigs": [
                  {
                      "taskType": "General",
                      "dataset": {
                          "name": "text_dataset",
                          "datasetLocation": {
                              "s3Uri": "s3://amzn-s3-demo-bucket/input/retrieve-and-generate/rng-eval-byoir.jsonl"
                          }
                      },
                      "metricNames": [
                          "Builtin.Correctness",
                          "Builtin.Completeness",
                          "Builtin.Helpfulness",
                          "Builtin.LogicalCoherence",
                          "Builtin.Faithfulness",
                          "Builtin.Harmfulness",
                          "Builtin.Stereotyping",
                          "Builtin.Refusal",
                          "Builtin.CitationCoverage",
                          "Builtin.CitationPrecision"
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
          "ragConfigs": [
              {
                  "precomputedRagSourceConfig": {
                      "retrieveAndGenerateSourceConfig": {
                          "ragSourceIdentifier": {{"my_rag_source"}}
                      }
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

The following python example demonstrates how to make a *Retrieve and generate* boto3 API request.

```
import boto3
client = boto3.client('bedrock')

job_response = client.create_evaluation_job(
    jobName="my_evaluation_job",
    jobDescription="two different task types",
    roleArn="arn:aws:iam::111122223333:role/role-name",
    applicationType="RagEvaluation",
    inferenceConfig={
        "ragConfigs": [
            {
                "knowledgeBaseConfig": {
                    "retrieveAndGenerateConfig": {
                        "type": "KNOWLEDGE_BASE",
                        "knowledgeBaseConfiguration": {
                            "knowledgeBaseId": "73SPNQM4CI",
                            "modelArn": "anthropic.claude-3-sonnet-20240229-v1:0",
                            "generationConfiguration": {
                                "promptTemplate": {
                                    "textPromptTemplate": "$search_results$ hello world template"
                                }
                            },
                             "retrievalConfiguration": {
                                 "vectorSearchConfiguration": {
                                     "numberOfResults": 10,
                                     "overrideSearchType": "HYBRID"
                                }
                             }
                        }
                    }
                }
            }
        ]
    },
    outputDataConfig={
        "s3Uri":"s3://amzn-s3-demo-bucket-model-evaluations/outputs/"
    },
    evaluationConfig={
        "automated": {
            "datasetMetricConfigs": [
                {
                    "taskType": "Summarization",
                    "dataset": {
                        "name": "RagDataset",
                        "datasetLocation": {
                            "s3Uri": "s3://amzn-s3-demo-bucket-input-data/data_3_rng.jsonl"
                        }
                    },
                    "metricNames": [
                        "Builtin.Faithfulness"
                    ]
                }
            ],
            "evaluatorModelConfig":
                {
                    "bedrockEvaluatorModels": [{
                        "modelIdentifier": "meta.llama3-1-70b-instruct-v1:0"
                    }]
                }
        }
    }
)

print(job_response)
```

------