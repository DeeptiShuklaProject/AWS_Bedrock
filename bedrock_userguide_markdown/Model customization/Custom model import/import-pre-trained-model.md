

# Import a pre-trained model into Amazon Bedrock
<a name="import-pre-trained-model"></a>

 You can create a custom model in Amazon Bedrock by importing a model you customized in other environments, such as Amazon SageMaker AI. For example, you might have a model that you have created in Amazon SageMaker AI that has proprietary model weights. You can now import that model into Amazon Bedrock and then use Amazon Bedrock features to make inference calls to the model. 

Amazon Bedrock provides two methods for importing custom models. You can import open-source foundation models that you customized, or you can import Amazon Nova models that you fine-tuned in SageMaker AI.
+ **Import open-source models with custom model import jobs** — Choose this method to import customized open-source foundation models. For example, Mistral AI or Llama models. It supports on-demand inference and multiple customization patterns.
+ **Import a customized Amazon Nova model by creating a custom model in Amazon Bedrock** — Choose this method to import an Amazon Nova model that you fine-tuned in SageMaker AI. It requires specialized SageMaker AI training recipes.

**Topics**
+ [Use Custom model import to import a customized open-source model into Amazon Bedrock](model-customization-import-model.md)
+ [Import a SageMaker AI-trained Amazon Nova model](import-with-create-custom-model.md)