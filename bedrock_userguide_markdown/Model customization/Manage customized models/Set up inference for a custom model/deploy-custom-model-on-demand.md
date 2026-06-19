

# Deploy a custom model for on-demand inference
<a name="deploy-custom-model-on-demand"></a>

 After you create a custom model with a model customization job or import a SageMaker AI-trained custom Amazon Nova model, you can set up on-demand inference for the model. With on-demand inference, you only pay for what you use and you don't need to set up provisioned compute resources. 

To set up on-demand inference for a custom model, you deploy it with a custom model deployment. After you deploy your custom model, you use the deployment's Amazon Resource Name (ARN) as the `modelId` parameter when you submit prompts and generate responses with model inference.

 For information about on-demand inference pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing). You can deploy a custom model for on-demand inference in the following Regions (for more information about Regions supported in Amazon Bedrock, see [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)): 
+ US East (N. Virginia)
+ US West (Oregon)

## Prerequisites for deploying a custom model for on-demand inference
<a name="custom-model-inference-prerequisites"></a>

Before you can deploy a custom model for on-demand inference, make sure you meet the following requirements:
+ You must use the US East (N. Virginia) or US West (Oregon) region.
+ You must customize the model on or after 7/16/2025. For supported models, see [Supported base models](#custom-model-inference-supported-models).
+ Your account must have permission to access the model that you are deploying. For more information about model customization access and security, see [Model customization access and security](custom-model-job-access-security.md).
+ If the model is encrypted with a AWS KMS key, you must have permission to use that key. For more information, see [Encryption of custom models](encryption-custom-job.md).

## Supported base models
<a name="custom-model-inference-supported-models"></a>

You can set up on-demand inference for the following base models:
+ Amazon Nova Lite – Supported Region: US East (N. Virginia)
+ Amazon Nova 2 Lite – Supported Region: US East (N. Virginia)
+ Amazon Nova Micro – Supported Region: US East (N. Virginia)
+ Amazon Nova Pro – Supported Region: US East (N. Virginia)
+ Meta Llama 3.3 70B Instruct – Supported Region: US West (Oregon)

## Deploy a custom model
<a name="deploy-custom-model"></a>

You can deploy a custom model with the Amazon Bedrock console, AWS Command Line Interface, or AWS SDKs. For information about using the deployment for inference, see [Use a deployment for on-demand inference](#use-custom-model-on-demand).

------
#### [ Console ]

You deploy a custom model from the **Custom models** page as follows. You can also deploy a model from the **Custom model on-demand** page with the same fields. To find this page, under **Infer** in the navigation pane, choose **Custom model on-demand**.

**To deploy a custom model**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. In the **Models** tab, choose the radio button for the model you want to deploy.

1. Choose **Set up inference** and choose **Deploy for on-demand**.

1. In **Deployment details**, provide the following information:
   + **Deployment Name** (required) – Enter a unique name for your deployment.
   + **Description** (optional) – Enter a description for your deployment.
   + **Tags** (optional) – Add tags for cost allocation and resource management.

1. Choose **Create**. When the deployment's status is `Active`, your custom model is ready for on-demand inference. For more information about using the custom model, see [Use a deployment for on-demand inference](#use-custom-model-on-demand).

------
#### [ CLI ]

To deploy a custom model for on-demand inference using the AWS Command Line Interface, use the `create-custom-model-deployment` command with your custom model's Amazon Resource Name (ARN). This command uses the [CreateCustomModelDeployment](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateCustomModelDeployment.html) API operation. The response includes the deployment's ARN. When the deployment is active, you use this ARN as the `modelId` when making inference requests. For information about using the deployment for inference, see [Use a deployment for on-demand inference](#use-custom-model-on-demand).

```
aws bedrock create-custom-model-deployment \
--model-deployment-name "{{Unique name}}" \
--model-arn "{{Custom Model ARN}}" \
--description "{{Deployment description}}" \
--tags '[
    {
        "key": "Environment",
        "value": "Production"
    },
    {
        "key": "Team",
        "value": "ML-Engineering"
    },
    {
        "key": "Project",
        "value": "CustomerSupport"
    }
]' \
--client-request-token "{{unique-deployment-token}}" \
--region {{region}}
```

------
#### [ API ]

To deploy a custom model for on-demand inference, use the [CreateCustomModelDeployment](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateCustomModelDeployment.html) API operation with your custom model's Amazon Resource Name (ARN). The response includes the deployment's ARN. When the deployment is active, you use this ARN as the `modelId` when making inference requests. For information about using the deployment for inference, see [Use a deployment for on-demand inference](#use-custom-model-on-demand).

The following code shows how to use the SDK for Python (Boto3) to deploy a custom model.

```
def create_custom_model_deployment(bedrock_client):
    """Create a custom model deployment
    Args:
        bedrock_client: A boto3 Amazon Bedrock client for making API calls

    Returns:
        str: The ARN of the new custom model deployment

    Raises:
        Exception: If there is an error creating the deployment
    """

    try:
        response = bedrock_client.create_custom_model_deployment(
            modelDeploymentName="{{Unique deployment name}}",
            modelArn="{{Custom Model ARN}}",
            description="{{Deployment description}}",
            tags=[
                {'key': 'Environment', 'value': 'Production'},
                {'key': 'Team', 'value': 'ML-Engineering'},
                {'key': 'Project', 'value': 'CustomerSupport'}
            ],
            clientRequestToken=f"deployment-{uuid.uuid4()}"
        )

        deployment_arn = response['customModelDeploymentArn']
        print(f"Deployment created: {deployment_arn}")
        return deployment_arn

    except Exception as e:
        print(f"Error creating deployment: {str(e)}")
        raise
```

------

## Use a deployment for on-demand inference
<a name="use-custom-model-on-demand"></a>

After you deploy your custom model, you use the deployment's Amazon Resource Name (ARN) as the `modelId` parameter when you submit prompts and generate responses with model inference.

For information about making inference requests, see the following topics:
+ [Making inference requests](inference.md)
+ [Prerequisites for running model inference](inference-prereq.md)
+ [Inference using Invoke API](inference-api.md)

## Delete a custom model deployment
<a name="delete-custom-model-deployment"></a>

After you are finished using your model for on-demand inference, you can delete the deployment. After you delete the deployment, you can't use it for on-demand inference but deployment deletion doesn't delete the underlying custom model.

You can delete a custom model deployment with the Amazon Bedrock console, AWS Command Line Interface, or AWS SDKs.

**Important**  
Deleting a custom model deployment is irreversible. Make sure you no longer need the deployment before proceeding with the deletion. If you need to use the custom model for on-demand inference again, you must create a new deployment.

------
#### [ Console ]

**To delete a custom model deployment**

1. In the navigation pane, under **Infer**, choose **Custom model on-demand**.

1. Choose the custom model deployment you want to delete.

1. Choose **Delete**.

1. In the confirmation dialog, enter the deployment name to confirm the deletion.

1. Choose **Delete** to confirm deletion.

------
#### [ CLI ]

To delete a custom model deployment using the AWS Command Line Interface, use the `delete-custom-model-deployment` command with your deployment identifier. This command uses the [DeleteCustomModelDeployment](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteCustomModelDeployment.html) API operation. 

```
aws bedrock delete-custom-model-deployment \
--custom-model-deployment-identifier "{{deployment-arn-or-name}}" \
--region {{region}}
```

------
#### [ API ]

To delete a custom model deployment programmatically, use the [DeleteCustomModelDeployment](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteCustomModelDeployment.html) API operation with the deployment's Amazon Resource Name (ARN) or name. The following code shows how to use the SDK for Python (Boto3) to delete a custom model deployment.

```
def delete_custom_model_deployment(bedrock_client):
    """Delete a custom model deployment

    Args:
        bedrock_client: A boto3 Amazon Bedrock client for making API calls

    Returns:
        dict: The response from the delete operation

    Raises:
        Exception: If there is an error deleting the deployment
    """

    try:
        response = bedrock_client.delete_custom_model_deployment(
            customModelDeploymentIdentifier="{{Deployment identifier}}"
        )

        print("Deleting deployment...")
        return response

    except Exception as e:
        print(f"Error deleting deployment: {str(e)}")
        raise
```

------