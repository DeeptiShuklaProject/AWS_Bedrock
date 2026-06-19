

# Analyze the results of a model customization job
<a name="model-customization-analyze"></a>

When your model customization job completes, you can analyze the results of the customization process. The following artifacts are uploaded to the S3 bucket that you specify when creating your model customization job:
+ **Training and validation metrics** – Amazon Bedrock provides training metrics for all model customization jobs. Validation metrics are also included with some model customization jobs.
+ **Synthetic data (Model Distillation only)** – Sample prompts from the synthetic dataset that Amazon Bedrock generated from your teacher model and used to fine tune your student model during the [distillation job](submit-model-distillation-job.md). This information can help you further understand and validate how your custom model was trained.
+ **Prompt insights (Model Distillation only)** – A report of input prompts that were accepted and rejected (along with a reason why) during distillation. This information can help you fix and refine your prompts if you need to run another distillation job.

 Amazon Bedrock stores your customized models in AWS managed storage scoped to your AWS account.

You can also evaluate your model by running a model evaluation job. For more information, see [Evaluate the performance of Amazon Bedrock resources](evaluation.md).

The following example shows where you can fine training and validation metrics in an S3 bucket:

```
- model-customization-job-{{training-job-id}}/
    - training_artifacts/
        - step_wise_training_metrics.csv
    - validation_artifacts/
        - post_fine_tuning_validation/
            - validation_metrics.csv
```

Use the `step_wise_training_metrics.csv` and the `validation_metrics.csv` files to analyze the model customization job and to help you adjust the model as necessary.

The columns in the `step_wise_training_metrics.csv` file are as follows.
+ `step_number` – The step in the training process. Starts from 0.
+ `epoch_number` – The epoch in the training process.
+ `training_loss` – Indicates how well the model fits the training data. A lower value indicates a better fit.
+ `perplexity` – Indicates how well the model can predict a sequence of tokens. A lower value indicates better predictive ability.

The columns in the `validation_metrics.csv` file are the same as the training file, except that `validation_loss` (how well the model fits the validation data) appears in place of `training_loss`.



You can find the output files by opening up the [https://console.aws.amazon.com/s3](https://console.aws.amazon.com/s3) directly or by finding the link to the output folder within your model details. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. In the **Models** tab, select a model to view its details. The **Job name** can be found in the **Model details** section.

1. To view the output S3 files, select the **S3 location** in the **Output data** section.

1. Find the training and validation metrics files in the folder whose name matches the **Job name** for the model.

------
#### [ API ]

To list information about all your custom models, send a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) (see link for request and response formats and field details) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Refer to [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) for filters that you can use.

To list all the tags for a custom model, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the custom model.

To monitor the status of a model customization job, send a [GetCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetCustomModel.html) (see link for request and response formats and field details) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) with the `modelIdentifier`, which is either of the following.
+ The name that you gave the model.
+ The ARN of the model.

You can see `trainingMetrics` and `validationMetrics` for a model customization job in either the [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html) or [GetCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetCustomModel.html) response.

To download the training and validation metrics files, follow the steps at [Downloading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/download-objects.html). Use the S3 URI you provided in the `outputDataConfig`.

[See code examples](model-customization-code-samples.md)

------