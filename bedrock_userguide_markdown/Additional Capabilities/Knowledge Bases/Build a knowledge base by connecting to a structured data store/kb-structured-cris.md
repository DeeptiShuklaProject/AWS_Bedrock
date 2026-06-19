

# Cross-region inference for knowledge bases with structured data store
<a name="kb-structured-cris"></a>

Starting May 10, 2026, Amazon Bedrock Knowledge Bases with structured data store will use cross-region inference to process your API requests. With cross-region inference, Amazon Bedrock Knowledge Bases will automatically select the optimal region within your geography to process your inference request, maximizing available compute resources and model availability, and providing the best customer experience. This applies to the [GenerateQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerateQuery.html), [Retrieve](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html), and [RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) API operations when used with a structured data store.

Cross-region inference requests stay within the AWS Regions that are part of the geography where your data originally resides. For example, a request made within the US is kept within AWS Regions in the US. Although your knowledge base data remains stored only in the primary Region, input prompts and output results may be processed in another Region within the same geography. All data is transmitted encrypted across Amazon's secure network.

For the following Regions, geo-specific cross-region inference is not available, and inference requests may be processed in Regions outside of the local geography:
+ Asia Pacific (Seoul) (`ap-northeast-2`)
+ Asia Pacific (Mumbai) (`ap-south-1`)
+ Asia Pacific (Singapore) (`ap-southeast-1`)
+ South America (São Paulo) (`sa-east-1`)

**Note**  
There is no additional cost for using cross-region inference with knowledge bases with structured data store.

Cross-region inference is automatically enabled for all knowledge bases with structured data store. No configuration changes are required. For more information about cross-region inference and supported Regions, see [Increase throughput with cross-Region inference](cross-region-inference.md).