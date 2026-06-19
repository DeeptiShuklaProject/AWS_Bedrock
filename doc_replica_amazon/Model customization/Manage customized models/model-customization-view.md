

# View details about a custom model
<a name="model-customization-view"></a>

To learn how to view details about your customized model, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a custom model**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Custom models** under **Tune**.

1. From the **Models** section, select a model.

1. View the details for the custom model configuration and how it was customized.

------
#### [ API ]

To retrieve information about a specific custom model, send a [GetCustomModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetCustomModel.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Specify either the name of the custom model or its ARN as the `modelIdentifier`.

To list information about all the custom models in an account, send a [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). To control the number of results that are returned, you can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

For other optional parameters that you can specify to sort and filter the results, see [ListCustomModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListCustomModels.html).

To list all the tags for a custom model, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the custom model.

------