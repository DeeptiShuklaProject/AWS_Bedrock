

# Code examples for Provisioned Throughput
<a name="prov-thru-code-examples"></a>

The following code examples demonstrate how to create a Provisioned Throughput and how to manage and invoke it, using the AWS CLI and the Python SDK. You can create a Provisioned Throughput from a foundation model or from a model that you've already customized. Before you get started, carry out the following prerequisites:

**Prerequisites**

The following examples use the Amazon Nova Lite model, whose model ID is `amazon.nova-lite-v1:0:24k`. If you haven't already, request access to the Amazon Nova Lite by following the steps at [Manage model access using SDK and CLI](model-access.md#model-access-modify).

If you want to purchase Provisioned Throughput for a different foundation model or a custom model, you'll have to do the following:

1. Find the model's ID (for foundation models), name (for custom models), or ARN (for either) by doing one of the following:
   + If you're purchasing a Provisioned Throughput for a foundation model, find the ID or Amazon Resource Name (ARN) of a model that supports provisioning in one of the following ways:
     + Look up the value in the table.
     + Send a [ListFoundationModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) request and specify the `byInferenceType` value as `PROVISIONED` to see a list of models that support provisioning. Find the value in the `modelId` or `modelArn` field.
   + If you're purchasing a Provisioned Throughput for a custom model, find the name or Amazon Resource Name (ARN) of the model that you customized in one of the following ways:
     + In the Amazon Bedrock console, choose **Custom models** from the left navigation pane. Find the name of your customized model in the **Models** list or select it and find the **Model ARN** in the **Model details**.
     + Send a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) request and find the `modelName` or `modelArn` value of your custom model in the response.

1. Modify the `body` of the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) request in the examples below to match the format of the body of the model by finding it in [Inference request parameters and response fields for foundation models](model-parameters.md).

Choose the tab for your preferred method, and then follow the steps:

------
#### [ AWS CLI ]

1. Send a [CreateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateProvisionedModelThroughput.html) request to create a no-commitment Provisioned Throughput called {{MyPT}}, by running the following command in a terminal:

   ```
   aws bedrock create-provisioned-model-throughput \
      --model-units 1 \
      --provisioned-model-name {{MyPT}} \
      --model-id amazon.nova-lite-v1:0:24k
   ```

1. The response returns a `provisioned-model-arn`. Allow some time for the creation to complete. To check its status, send a [GetProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetProvisionedModelThroughput.html) request and provide the name or ARN of the provisioned model as the `provisioned-model-id`, by running the following command:

   ```
   aws bedrock get-provisioned-model-throughput \
       --provisioned-model-id {{${provisioned-model-arn}}}
   ```

1. Run inference with your provisioned model by sending an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) request. Provide the ARN of the provisioned model that was returned in the `CreateProvisionedModelThroughput` response, as the `model-id`. The output is written to a file named {{output.txt}} in your current folder.

   ```
   aws bedrock-runtime invoke-model \
       --model-id {{${provisioned-model-arn}}} \
       --body '{
                   "messages": [{
                       "role": "user",
                       "content": [{
                           "text": "Hello"
                       }]
                   }],
                   "inferenceConfig": {
                       "temperature":0.7
                   }
               }' \
       --cli-binary-format raw-in-base64-out \
       output.txt
   ```

1. Send a [DeleteProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteProvisionedModelThroughput.html) request to delete the Provisioned Throughput using the following command. You'll no longer be charged for the Provisioned Throughput.

   ```
   aws bedrock delete-provisioned-model-throughput 
     --provisioned-model-id {{MyPT}}
   ```

------
#### [ Python (Boto) ]

The following code snippets walk you through creating a Provisioned Throughput getting information about it, and invoking the Provisioned Throughput.

1. To create a no-commitment Provisioned Throughput called {{MyPT}} and assign the ARN of the Provisioned Throughput to a variable called {{provisioned\_model\_arn}}, send the following [CreateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateProvisionedModelThroughput.html) request:

   ```
   import boto3 
   
   provisioned_model_name = '{{MyPT}}'
   
   bedrock = boto3.client(service_name='bedrock')
   response = bedrock.create_provisioned_model_throughput(
       modelUnits=1,
       provisionedModelName=provisioned_model_name, 
       modelId='amazon.nova-lite-v1:0:24k' 
   )
                           
   {{provisioned_model_arn}} = response['provisionedModelArn']
   ```

1. Allow some time for the creation to complete. You can check its status with the following code snippet. You can provide either the name of the Provisioned Throughput or the ARN returned from the [CreateProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateProvisionedModelThroughput.html) response as the `provisionedModelId`.

   ```
   bedrock.get_provisioned_model_throughput(provisionedModelId=provisioned_model_name)
   ```

1. Run inference with your updated provisioned model with the following command and using the ARN of the provisioned model as the `modelId`.

   ```
   import json
   import logging
   import boto3
   
   from botocore.exceptions import ClientError
   
   
   class ImageError(Exception):
       "Custom exception for errors returned by the model"
   
       def __init__(self, message):
           self.message = message
   
   
   logger = logging.getLogger(__name__)
   logging.basicConfig(level=logging.INFO)
   
   
   def generate_text(model_id, body):
       """
       Generate text using your provisioned custom model.
       Args:
           model_id (str): The model ID to use.
           body (str) : The request body to use.
       Returns:
           response (json): The response from the model.
       """
   
       logger.info(
           "Generating text with your provisioned custom model %s", model_id)
   
       brt = boto3.client(service_name='bedrock-runtime')
   
       accept = "application/json"
       content_type = "application/json"
   
       response = brt.invoke_model(
           body=body, modelId=model_id, accept=accept, contentType=content_type
       )
       response_body = json.loads(response.get("body").read())
   
       finish_reason = response_body.get("error")
   
       if finish_reason is not None:
           raise ImageError(f"Text generation error. Error is {finish_reason}")
   
       logger.info(
           "Successfully generated text with provisioned custom model %s", model_id)
   
       return response_body
   
   
   def main():
       """
       Entrypoint for example.
       """
       try:
           logging.basicConfig(level=logging.INFO,
                               format="%(levelname)s: %(message)s")
   
           model_id = {{provisioned-model-arn}}
   
           body = json.dumps({
               "inputText": "what is AWS?"
           })
   
           response_body = generate_text(model_id, body)
           print(f"Input token count: {response_body['inputTextTokenCount']}")
   
           for result in response_body['results']:
               print(f"Token count: {result['tokenCount']}")
               print(f"Output text: {result['outputText']}")
               print(f"Completion reason: {result['completionReason']}")
   
       except ClientError as err:
           message = err.response["Error"]["Message"]
           logger.error("A client error occurred: %s", message)
           print("A client error occured: " +
                 format(message))
       except ImageError as err:
           logger.error(err.message)
           print(err.message)
   
       else:
           print(
               f"Finished generating text with your provisioned custom model {model_id}.")
   
   
   if __name__ == "__main__":
       main()
   ```

1. Delete the Provisioned Throughput with the following code snippet. You'll no longer be charged for the Provisioned Throughput.

   ```
   bedrock.delete_provisioned_model_throughput(provisionedModelId=provisioned_model_name)
   ```

------