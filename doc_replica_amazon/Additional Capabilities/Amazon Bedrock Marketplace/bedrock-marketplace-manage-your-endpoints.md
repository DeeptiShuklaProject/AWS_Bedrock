

# Manage your endpoints
<a name="bedrock-marketplace-manage-your-endpoints"></a>

You view and manage your Amazon Bedrock Marketplace model endpoints in the following ways:
+ Editing the number of instances or instance types
+ Changing the tags
+ Deleting the endpoint

You can also register and de-register endpoints of Amazon Bedrock Marketplace models that you created from SageMaker AI.

**To manage your endpoints**

1. Sign in to the AWS Management Console using an IAM role with Amazon Bedrock permissions.

1. In the search bar, specify "Amazon Bedrock" and choose **Amazon Bedrock** from the dropdown list.

1. Choose **Marketplace deployments** under **Foundation models**

1. Choose **Register**, **Edit**, or **Delete** from the **Action** bar.

1. To view additional details, choose the endpoint.

You can use the following AWS Command Line Interface command to delete the endpoint.

```
aws bedrock delete-marketplace-model-endpoint --endpoint-arn "arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint}}"
```

The preceding command doesn't return a response.

You can use the following AWS Command Line Interface command to update the endpoint.

```
aws bedrock update-marketplace-model-endpoint --endpoint-config "{\"sageMaker\":{\"initialInstanceCount\":2,\"instanceType\":\"ml.g5.xlarge\",\"executionRole\":\"arn:aws:iam::{{111122223333}}:role/service-role/{{example-sagemaker-service-role}}\"}}" --endpoint-arn "arn:aws:sagemaker:region:account-number:endpoint/example-endpoint-name"
```

**Note**  
The responses for the `CreateMarketplaceModelEndpoint`, `RegisterMarketplaceModelEndpoint`, and `UpdateMarketplaceModelEndpoint` operations are the same.