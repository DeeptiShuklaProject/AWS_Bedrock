

# Import a SageMaker AI-trained Amazon Nova model
<a name="import-with-create-custom-model"></a>

**Note**  
To import open-source models into Amazon Bedrock, you use a model import job. For more information, see [Use Custom model import to import a customized open-source model into Amazon Bedrock](model-customization-import-model.md). 

 To import an Amazon Nova model that you customized with SageMaker AI, you create a new custom model in Amazon Bedrock for it. For example, if you used SageMaker AI to fine-tune an Amazon Nova Pro model to improve its performance for a specific use case, you can import the fine-tuned model into Amazon Bedrock as a custom model and use it to run inference. 

 Creating and using a SageMaker AI-trained Amazon Nova model in Amazon Bedrock works as follows: 

1. **Customize the model in SageMaker AI** – Customize a Amazon Nova model through pre-built base recipes using SageMaker AI training jobs. For more information, see [Customizing Amazon Nova models](https://docs.aws.amazon.com/sagemaker/latest/dg/nova-model.html) in the *Amazon SageMaker AI Developer Guide*.

1. **Create a custom model in Amazon Bedrock** – Create a custom model with the [CreateCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateCustomModel.html) API operation. When you create a custom model, Amazon Bedrock validates and then imports the model artifacts from an Amazon-managed Amazon S3 bucket. SageMaker AI creates this bucket when you run your first SageMaker AI training job. For a code sample, see [Create a custom model (AWS SDKs)](create-custom-model-sdks.md).

1.  **Set up inference for the custom model** – After the import process is complete, you can set up inference for the model. For more information, see [Set up inference for a custom model](model-customization-use.md). You manage the custom model just like models you create in Amazon Bedrock through model customization. For more information, see [Customize your model to improve its performance for your use case](custom-models.md).

You can create a custom model from an Amazon Nova model in the following Regions (for more information about Regions supported in Amazon Bedrock, see [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)): 
+ US East (N. Virginia)

**Topics**
+ [Guidelines and requirements](#create-custom-model-considerations)
+ [Create a custom model (AWS SDKs)](create-custom-model-sdks.md)

## Guidelines and requirements
<a name="create-custom-model-considerations"></a>

Before you import an Amazon Nova model, note the following:
+ You must use the US East (N. Virginia) region.
+ When you customize the model in SageMaker AI, you must use one of the following Amazon Nova models:
  + Amazon Nova Lite
  + Amazon Nova Micro
  + Amazon Nova Pro
+ When you customize the model in SageMaker AI, you must use the SageMaker AI Amazon Nova recipes. For more information, see [Amazon Nova recipes](https://docs.aws.amazon.com/sagemaker/latest/dg/nova-model-recipes.html) in the Amazon SageMaker AI Developer Guide. 
+ Your SageMaker AI-trained Amazon Nova models must be stored in an Amazon-managed Amazon S3 bucket. SageMaker AI creates this bucket when you run your first SageMaker AI training job.
+ Your Amazon Bedrock service role must have permissions to access the Amazon-managed Amazon S3 bucket, and if specified, your AWS KMS key. For more information about creating the role, see [Create a service role for importing pre-trained models](model-import-iam-role.md). For information about granting the role permission to use your AWS KMS key, see [Encryption of imported custom models](encryption-import-model.md). 
+ You can only use the Amazon Bedrock APIs to create a custom model from an existing SageMaker AI-trained Amazon Nova model. You can't use the Amazon Bedrock console.