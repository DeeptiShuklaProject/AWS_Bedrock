

# Create a custom model (AWS SDKs)
<a name="create-custom-model-sdks"></a>

To create a custom model from a SageMaker AI-trained Amazon Nova model stored in Amazon S3, you use the [CreateCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateCustomModel.html) API operation. You can use the following code to create a custom model with the SDK for Python (Boto3). The code creates a custom model and then checks its status until the model is `ACTIVE` and ready to use.

To use the code, update the following parameters. The code sample also includes optional parameters such as `clientRequestToken` for idempotency and `modelTags` for resource tagging. 
+ **modelName** – Give the model a unique name.
+ **s3Uri** – Specify the path to the Amazon-managed Amazon S3 bucket that stores your model artifacts. SageMaker AI creates this bucket when you run your first SageMaker AI training job.
+ **roleArn** – Specify the Amazon Resource Name (ARN) of an IAM service role that Amazon Bedrock assumes to perform tasks on your behalf. For more information about creating this role, see [Create a service role for importing pre-trained models](model-import-iam-role.md).
+ **modelKmsKeyArn** (optional) – Specify a AWS KMS key to encrypt the model in Amazon Bedrock. If you don't provide a AWS KMS key, Amazon Bedrock uses an AWS-managed AWS KMS key to encrypt the model. For information about encryption, see [Encryption of imported custom models](encryption-import-model.md).

After you create the custom model, the model appears in the [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) response with a `customizationType` of `imported`. To track the status of the new model, you use the [GetCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetCustomModel.html) API operation.

```
import boto3
import uuid
from botocore.exceptions import ClientError
import time

def create_custom_model(bedrock_client):
    """
    Creates a custom model in Amazon Bedrock from a SageMaker AI-trained Amazon Nova model stored in Amazon S3.
    Args:
        bedrock_client: The Amazon Bedrock client instance
    Returns:
        dict: Response from the CreateCustomModel API call
    """
    try:
        # Create a unique client request token for idempotency
        client_request_token = str(uuid.uuid4())

        # Define the model source configuration
        model_source_config = {
            's3DataSource': {
                's3Uri': '{{s3://amzn-s3-demo-bucket/folder/}}',
            }
        }

        # Create the custom model
        response = bedrock_client.create_custom_model(
            # Required parameters
            modelName='{{modelName}}',
            roleArn='{{serviceRoleArn}}',
            modelSourceConfig=model_source_config,

            # Optional parameters
            clientRequestToken=client_request_token,
            modelKmsKeyArn='{{keyArn}}',
            modelTags=[
                {
                    'key': 'Environment',
                    'value': 'Production'
                },
                {
                    'key': 'Project',
                    'value': 'AIInference'
                }
            ]
        )

        print(f"Custom model creation initiated. Model ARN: {response['modelArn']}")

        return response

    except ClientError as e:
        print(f"Error creating custom model: {e}")
        raise

def list_custom_models(bedrock_client):
    """
    Lists all custom models in Amazon Bedrock.

    Args:
        bedrock_client: An Amazon Bedrock client.

    Returns:
        dict: Response from the ListCustomModels API call

    """

    try:
        response = bedrock_client.list_custom_models()
        print(f"Total number of custom models: {len(response['modelSummaries'])}")

        for model in response['modelSummaries']:
            print("ARN: " + model['modelArn'])
            print("Name: " + model['modelName'])
            print("Status: " + model['modelStatus'])
            print("Customization type: " + model['customizationType'])
            print("------------------------------------------------------")

        return response

    except ClientError as e:
        print(f"Error listing custom models: {e}")
        raise

def check_model_status(bedrock_client, model_arn):
    """
    Checks the status of a custom model creation.

    Args:
        model_arn (str): The ARN of the custom model
        bedrock_client: An Amazon Bedrock client.

    Returns:
        dict: Response from the GetCustomModel API call

    """

    try:
        max_time = time.time() + 60 * 60  # 1 hour

        while time.time() < max_time:
            response = bedrock_client.get_custom_model(modelIdentifier=model_arn)
            status = response.get('modelStatus')
            print(f"Job status: {status}")
            if status == 'Failed':
                print(f"Failure reason: {response.get('failureMessage')}")
                break
            if status == 'Active':
                print("Model is ready for use.")
                break
            time.sleep(60)

    except ClientError as e:
        print(f"Error checking model status: {e}")
        raise


def main():
    bedrock_client = boto3.client(service_name='bedrock', region_name='{{REGION}}')
    
    # Create the custom model
    model_arn = create_custom_model(bedrock_client)["modelArn"]

    # Check the status of the model
    if model_arn:
        check_model_status(bedrock_client, model_arn)

    # View all custom models
    list_custom_models(bedrock_client)


if __name__ == "__main__":
    main()
```