

# Submit a model customization job for fine-tuning
<a name="model-customization-submit"></a>

You can create a custom model by using fine-tuning in the Amazon Bedrock console or API. You can further fine tune an existing custom model. The customization job can take several hours. The duration of the job depends on the size of the training data (number of records, input tokens, and output tokens), number of epochs, and batch size.

## Prerequisites
<a name="submit-model-customization-job-prerequisites"></a>
+ Create an AWS Identity and Access Management (IAM) service role to access the S3 bucket where you want to store your model customization training and validation data. You can create this role automatically by using the AWS Management Console or manually. For more information on the manual option, see [Create an IAM service role for model customization](custom-model-job-access-security.md#custom-model-job-service-role).
+ (Optional) Encrypt input and output data, your customization job, or inference requests made to custom models. For more information, see [Encryption of custom models](encryption-custom-job.md).
+ (Optional) Create a virtual private cloud (VPC) to protect your customization job. For more information, see [(Optional) Protect your model customization jobs using a VPC](custom-model-job-access-security.md#vpc-model-customization).

## Submit your job
<a name="submit-model-customization-job-how-to"></a>

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

To submit a model customization job in the console, carry out the following steps.

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. In the **Models** tab, choose **Customize model** and then **Create Fine-tuning job**.

1. In the **Model details** section, do the following.

   1. Choose the model that you want to customize with your own data and give your resulting model a name. You can choose either a foundation model or a previously customized model (fine-tuned or distilled) as your base model.

   1. (Optional) By default, Amazon Bedrock encrypts your model with a key owned and managed by AWS. To use a [custom KMS key](encryption-custom-job.md), select **Model encryption** and choose a key.

   1. (Optional) To associate [tags](tagging.md) with the custom model, expand the **Tags** section and select **Add new tag**.

1. In the **Job configuration** section, enter a name for the job and optionally add any tags to associate with the job.

1. (Optional) To use a [virtual private cloud (VPC) to protect your training data and customization job](custom-model-job-access-security.md#vpc-model-customization), select a VPC that contains the input data and output data Amazon S3 locations, its subnets, and security groups in the **VPC settings** section.
**Note**  
If you include a VPC configuration, the console cannot create a new service role for the job. [Create a custom service role](model-customization-iam-role.md) and add permissions similar to the example described in [Attach VPC permissions to a model customization role](custom-model-job-access-security.md#vpc-data-access-role).

1. In the **Input data** section, select the S3 location of the training dataset file and, if applicable, the validation dataset file.

1. In the **Hyperparameters** section, input values for [hyperparameters](custom-models-hp.md) to use in training.

1. In the **Output data** section, enter the Amazon S3 location where Amazon Bedrock should save the output of the job. Amazon Bedrock stores the training loss metrics and validation loss metrics for each epoch in separate files in the location that you specify.

1. In the **Service access** section, select one of the following: 
   + **Use an existing service role** – Select a service role from the dropdown list. For more information on setting up a custom role with the appropriate permissions, see [Create a service role for model customization](model-customization-iam-role.md).
   + **Create and use a new service role** – Enter a name for the service role.

1. Choose **Fine-tune model** to begin the job.

------
#### [ API ]

**Request**

Send a [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) (see link for request and response formats and field details) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) to submit a model customization job. Minimally, you must provide the following fields.
+ `roleArn` – The ARN of the service role with permissions to customize models. Amazon Bedrock can automatically create a role with the appropriate permissions if you use the console, or you can create a custom role by following the steps at [Create a service role for model customization](model-customization-iam-role.md).
**Note**  
If you include a `vpcConfig` field, make sure that the role has the proper permissions to access the VPC. For an example, see [Attach VPC permissions to a model customization role](custom-model-job-access-security.md#vpc-data-access-role).
+ `baseModelIdentifier` – The [model ID](models-supported.md) or ARN of the foundation model or previously customized model (fine-tuned or distilled) to customize.
+ `customModelName` – The name to give the newly customized model.
+ `jobName` – The name to give the training job.
+ `hyperParameters` – [Hyperparameters](custom-models-hp.md) that affect the model customization process.
+ `trainingDataConfig` – An object containing the Amazon S3 URI of the training dataset. Depending on the customization method and model, you can also include a `validationDataConfig`. For more information about preparing the datasets, see [Prepare data for fine-tuning your models](model-customization-prepare.md).
+ `validationDataconfig` – An object containing the Amazon S3 URI of the validation dataset.
+ `outputDataConfig` – An object containing the Amazon S3 URI to write the output data to.

If you don't specify the `customizationType`, the model customization method defaults to `FINE_TUNING`.

To prevent the request from completing more than once, include a `clientRequestToken`.

You can include the following optional fields for extra configurations.
+ `jobTags` and/or `customModelTags` – Associate [tags](tagging.md) with the customization job or resulting custom model.
+ `customModelKmsKeyId` – Include a [custom KMS key](encryption-custom-job.md) to encrypt your custom model.
+ `vpcConfig` – Include the configuration for a [virtual private cloud (VPC) to protect your training data and customization job](custom-model-job-access-security.md#vpc-model-customization).

**Response**

The response returns a `jobArn` that you can use to [monitor](model-customization-monitor.md) or [stop](model-customization-stop.md) the job.

[See code examples](model-customization-code-samples.md)

------