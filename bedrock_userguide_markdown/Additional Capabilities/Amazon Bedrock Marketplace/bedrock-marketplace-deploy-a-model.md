

# Deploy a model
<a name="bedrock-marketplace-deploy-a-model"></a>

After you've subscribed to a model, you deploy it to a SageMaker AI endpoint. You make inference calls to the endpoint. The model is hosted by SageMaker AI. During the deployment process, you provide the following information:
+ The name of the SageMaker AI endpoint
+ The number of instances taking inference calls to the endpoint
+ The instance type of the endpoint

You can also configure optional advanced options such as tags.

A SageMaker AI service role is automatically created for SageMaker AI to assume and perform actions on your behalf. For more information about Amazon SageMaker AI permissions, see [How to use SageMaker AI execution roles](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html ).

Alternatively, you can choose an existing role or create a new one. To learn how to deploy an Amazon Bedrock Marketplace model, select the tab corresponding to your method of choice and follow the steps.

**To deploy a model**

1. Sign in to the AWS Management Console using an IAM role with Amazon Bedrock permissions.

1. In the search bar, specify "Amazon Bedrock" and choose the **Amazon Bedrock** from the dropdown list.

1. From the navigation pane, choose **Model Catalog**.

1. Choose the model card for the model that you're deploying.

1. Choose **Deploy**.

1. For **Endpoint Name**, specify the name of the endpoint.

1. Choose the number of instances and select the instance type.

1. Under **Advanced Settings**, you can optionally:

   1. Set up your VPC

   1. Configure the service access role

   1. Customize your encryption settings

   1. Add tags

1. Choose **Deploy** to deploy your Amazon Bedrock Marketplace model to an SageMaker AI endpoint. This process usually takes 10-15 minutes.

Use the `CreateMarketplaceModelEndpoint` operation to create an endpoint. Some models have an end-user license agreement (EULA). To accept the EULA, you set the `AcceptEula` to `True`.

The following example uses an example AWS Command Line Interface command to create an endpoint:

```
aws bedrock create-marketplace-model-endpoint --model-source-identifier {{HubContentArn}} --endpoint-config "{\"sageMaker\":{\"initialInstanceCount\":{{1}},\"instanceType\":\"{{ml.g5.xlarge}}\",\"executionRole\":\"arn:aws:iam::{{111122223333}}:role/{{example-IAM-role}}\"}}" --endpoint-name "{{example-endpoint-name}}"
```

**Note**  
The responses for the `CreateMarketplaceModelEndpoint`, `UpdateMarketplaceModelEndpoint` and `RegisterMarketplaceModelEndpoint` operations are the same.

```
{"marketplaceModelEndpoint":{"createdAt":"2024-11-12T02:31:58.201474085Z","endpoint":{"sageMaker":{"executionRole":"arn:aws:iam::{{111122223333}}:role/service-role/{{amazon-sagemaker-execution-role}}","initialInstanceCount":1,"instanceType":"ml.g5.2xlarge","kmsEncryptionKey":null,"vpc":null}},"endpointArn":"arn:aws:sagemaker:region:{{555555555555}}:endpoint/{{example-endpoint-name}}","endpointStatus":"Creating","endpointStatusMessage":"","modelSourceIdentifier":"arn:aws:sagemaker:region:aws:hub-content/SageMakerPublicHub/Model/{{example-model-name}}/1.2.2","status":"ACTIVE","statusMessage":"","updatedAt":"2024-11-12T02:31:58.201474085Z"}}
```

You can modify the endpoint in both Amazon Bedrock Marketplace and Amazon SageMaker AI. We recommend only modifying the endpoint within Amazon Bedrock. If you modify the endpoint within SageMaker AI, you might not be able to use the endpoint within Amazon Bedrock. The following are the modifications that can cause the endpoint to fail within Amazon Bedrock:
+ Setting [EnableNetworkIsolation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html#sagemaker-CreateModel-request-EnableNetworkIsolation) to `False`
+ Modifying the model definition within the [PrimaryContainer](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html#sagemaker-CreateModel-request-PrimaryContainer) object

For the endpoint to be operational, it must be registered and in service. You can use the following AWS Command Line Interface command to check the status of the endpoint.

```
aws bedrock get-marketplace-model-endpoint --endpoint-arn arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint-name}}            
```

The endpoint must have the following status for you to use it with Amazon Bedrock:

```
endpointStatus: InService
status: REGISTERED
```

If you've made a modification that has caused the endpoint to fail, you can deregister and reregister the endpoint. Use the `DeregisterEndpoint` operation to deregister the endpoint. Use the `RegisterEndpoint` operation to reregister it.

```
aws bedrock deregister-marketplace-model-endpoint --endpoint-arn arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint-name}}
```

```
aws bedrock register-marketplace-model-endpoint --endpoint-identifier arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint-name}} --model-source-identifier
         {{HubContentArn}}
```