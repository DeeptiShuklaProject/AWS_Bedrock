

# View information about a Provisioned Throughput
<a name="prov-thru-info"></a>

To learn how to view information about a Provisioned Throughput that you've purchased, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a Provisioned Throughput**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Provisioned Throughput** from the left navigation pane.

1. From the **Provisioned Throughput** section, select a Provisioned Throughput.

1. View the details for the Provisioned Throughput in the **Provisioned Throughput overview** section and the tags associated with your Provisioned Throughput in the **Tags** section.

------
#### [ API ]

To retrieve information about a specific Provisioned Throughput, send a [GetProvisionedModelThroughput](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetProvisionedModelThroughput.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). Specify either the name of the Provisioned Throughput or its ARN as the `provisionedModelId`.

To list information about all the Provisioned Throughputs in an account, send a [ListProvisionedModelThroughputs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListProvisionedModelThroughputs.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). To control the number of results that are returned, you can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

For other optional parameters that you can specify to sort and filter the results, see [ListProvisionedModelThroughputs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListProvisionedModelThroughputs.html).

To list all the tags for a Provisioned Throughput, send a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and include the Amazon Resource Name (ARN) of the Provisioned Throughput.

[See code examples](prov-thru-code-examples.md)

------