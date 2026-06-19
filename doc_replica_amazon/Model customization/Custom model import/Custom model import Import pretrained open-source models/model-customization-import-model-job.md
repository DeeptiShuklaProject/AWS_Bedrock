

# Submit a model import job
<a name="model-customization-import-model-job"></a>

You import a model into Amazon Bedrock by submitting a model import job in the Amazon Bedrock console, using the API, using the AWS CLI or using AWS SDK. In the job you specify the Amazon S3 URI for the source of the model files. Alternatively, if you've created the model in Amazon SageMaker AI, you can specify the SageMaker AI model. During model import, the import job automatically detects your model's architecture. The model import job can take several minutes. During the job, Amazon Bedrock validates that the model that is being imported is using a compatible the model architecture. 

The following procedure shows you how to create a custom model by importing a model that you have already customized. Select the tab corresponding to your method of choice and follow the steps. 

------
#### [ Console ]

To submit a model import job in the console, complete the following steps.

1. If you are importing your model files from Amazon S3, convert the model to the Hugging Face format. 

   1. If your model is a Mistral AI model, use [convert\_mistral\_weights\_to\_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/mistral/convert_mistral_weights_to_hf.py). 

   1. If your model is a Llama model, see [convert\_llama\_weights\_to\_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py). 

   1. Upload the model files to an Amazon S3 bucket in your AWS account. For more information, see [Upload an object to your bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-an-object-bucket.html).

   1. If you are using cross-account Amazon S3 or KMS keys to import your custom model, give Amazon Bedrock access to your AWS account's Amazon S3 or KMS key. For more information, see [Cross-account access to Amazon S3 bucket for custom model import jobs](cross-account-access-cmi.md).

1. In the Amazon Bedrock console, choose **Imported models** under **Foundation models** from the left navigation pane.

1. Choose the **Models** tab.

1. Choose **Import model**.

1. In the **Imported** tab, choose **Import model** to open the **Import model** page.

1. In the **Model details** section, do the following: 

   1. In **Model name** enter a name for the model.

   1. (Optional) To associate [tags](tagging.md) with the model, expand the **Tags** section and select **Add new tag**.

1. In the **Import job name** section, do the following: 

   1. In **Job name** enter a name for the model import job.

   1. (Optional) To associate [tags](tagging.md) with the custom model, expand the **Tags** section and select **Add new tag**.

1. In **Model import settings**, select the import options you want to use.
   + Select **Amazon S3 bucket** or ** Amazon SageMaker AI model** to specify the import source.
   + If you are importing your model files from an Amazon S3 bucket, enter the Amazon S3 location in **S3 location**. Optionally, you can choose **Browse S3** to choose the file location. 
   + If you are importing your model from Amazon SageMaker AI, choose **Amazon SageMaker AI model** and then choose the SageMaker AI model that you want to import in **SageMaker AI models**. 

1. Enter **VPC settings** (optional) to choose a VPC configuration to access your Amazon Amazon S3 data source located in your VPC. You can create and manage a VPC, subnets, and security groups in Amazon VPC. For more information on Amazon VPC, see [(Optional) Protect custom model import jobs using a VPC](vpc-custom-model-import.md).

1. Select **Encryption**, to encrypt your data by default with an AWS key that is owned and managed by you. You can also choose a different key if you select **Customize encryption settings (advanced).**.

1. In the **Service access** section, select one of the following: 
   + **Create and use a new service role** – Enter a name for the service role.
   + **Use an existing service role** – Select a service role from the drop-down list. To see the permissions that your existing service role needs, choose **View permission details**.

     For more information on setting up a service role with the appropriate permissions, see [Create a service role for importing pre-trained models](model-import-iam-role.md).
**Note**  
if you are using cross-account Amazon S3 or KMS keys, edit the service role policy and replace the account id specified for `aws:ResourceAccount` with the AWS account id of the bucket owner. 

1. Choose **Import**.

1. On the **Custom models** page, choose **Imported**.

1. In the **Jobs** section, check the status of the import job. The model name you chose identifies the model import job. The job is complete if the value of **Status** for the model is **Complete**. 

1. Get the model ID for your model by doing the following.

   1. On the **Imported models** page, choose the **Models** tab.

   1. Copy the ARN for the model that you want to use from the **ARN** column.

1. Use your model for inference calls. For more information, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md). You can use the model with on demand throughput. 

   You can also use your model in the Amazon Bedrock text [playground](playgrounds.md).

------
#### [ API ]

**Request**

Send a [CreateModelImportJob](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_CreateModelImportJob.html) (see link for request and response format and field details) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) to submit a custom model import job. Minimally, you must provide the following fields.
+ `roleArn` – The ARN of the service role with permissions to import models. Amazon Bedrock can automatically create a role with the appropriate permissions if you use the console, or you can create a custom role by following the steps at [Create a service role for importing pre-trained models](model-import-iam-role.md).
**Note**  
If you include a `vpcConfig` field, make sure that the role has the proper permissions to access the VPC. For an example, see [Attach VPC permissions to a custom model import role.](vpc-custom-model-import.md#vpc-data-access-role-cmi)
+ `importedModelName` – The name to give the newly imported model.
+ `jobName` – The name to give the import job.
+ `modelDataSource` – The data source for the imported model.

To prevent the request from completing more than once, include a `clientRequestToken`.

You can include the following optional fields for extra configurations.
+ `jobTags` and/or `importedModelTags` – Associate [tags](tagging.md) with the import job or the imported model.
+ `importedModelKmsKeyId` – Include a [Encryption of custom model import](https://docs.aws.amazon.com//bedrock/latest/userguide/encryption-import-model.html) KMS key to encrypt your imported model.
+ `vpcConfig` – Include the vpc configuration to [(Optional) Protect custom model import jobs using a VPC](vpc-custom-model-import.md).

**Response**

The response returns a `jobArn` for the import job that you use to identify the import job in other operations.

The import job will take a while to complete. You can check the current status by calling the [GetModelImportJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelImportJob.html) operation and checking the `Status` field in the response. You can list the current import jobs with the [ListModelImportJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelImportJobs.html). 

To get a list of models that you have imported, call [ListImportedModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListImportedModels.html). To get information about a specific imported model, call [GetImportedModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetImportedModel.html).

To delete an imported model, call [DeleteImportedModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteImportedModel.html).

------