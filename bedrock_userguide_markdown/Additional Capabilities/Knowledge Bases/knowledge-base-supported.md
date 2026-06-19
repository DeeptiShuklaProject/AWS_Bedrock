

# Supported models and Regions for Amazon Bedrock knowledge bases
<a name="knowledge-base-supported"></a>

To see which models support Knowledge Bases, please refer to [Models at a glance](model-cards.md) and choose the model you are interested in.

Amazon Bedrock Knowledge Bases also supports the use of inference profiles for parsing data or when generating responses. With inference profiles, you can track costs and metrics, and also do cross-Region inference to distribute model inference requests across a set of Regions to allow higher throughput. You can specify an inference profile in a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) or [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request. For more information, see [Set up a model invocation resource using inference profiles](inference-profiles.md).

**Important**  
If you use cross-Region inference, your data can be shared across Regions.

You can also use SageMaker AI models or [custom models](custom-models.md) that you train on your own data.

**Note**  
If you use an SageMaker AI or custom model, you must specify the orchestration and generation prompts (for more information, see **Knowledge base prompt templates** in [Configure and customize queries and response generation](kb-test-config.md)). Your prompts must include information variables to access the user's input and context.

Region and model support differ for some features in Amazon Bedrock Knowledge Bases. Select a topic to view support for a feature:

**Topics**
+ [Supported models for vector embeddings](#knowledge-base-supported-embeddings)
+ [Supported models and Regions for parsing](#knowledge-base-supported-parsing)
+ [Supported models and Regions for reranking results during query](#knowledge-base-supported-rerank)
+ [Supported Regions for Knowledge Bases with structured data stores](#knowledge-base-supported-structured)

## Supported models for vector embeddings
<a name="knowledge-base-supported-embeddings"></a>

Amazon Bedrock Knowledge Bases uses an embedding model to convert your data into vector embeddings and store the embeddings in a vector database. For more information, see [Turning data into a knowledge base](kb-how-data.md).

Amazon Bedrock Knowledge Bases supports vector embeddings using the following foundation models:


| Provider | Model | Model ID | Single-region model support | 
| --- | --- | --- | --- | 
| Amazon | Titan Embeddings G1 - Text | amazon.titan-embed-text-v1 | ap-northeast-1<br />eu-central-1<br />us-east-1<br />us-west-2 | 
| Amazon | Titan Text Embeddings V2 | amazon.titan-embed-text-v2:0 | ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3<br />ap-south-1<br />ap-south-2<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-central-2<br />eu-north-1<br />eu-south-1<br />eu-south-2<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-east-2<br />us-gov-east-1<br />us-gov-west-1<br />us-west-2 | 
| Cohere | Embed English | cohere.embed-english-v3 | ap-northeast-1<br />ap-south-1<br />ap-southeast-1<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Cohere | Embed Multilingual | cohere.embed-multilingual-v3 | ap-northeast-1<br />ap-south-1<br />ap-southeast-1<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 

Embedding models support the following vector types.


****  

| Model name | Supported vector type | Supported number of dimensions | 
| --- | --- | --- | 
| Amazon Titan Embeddings G1 - Text | Floating-point | 1536 | 
| Amazon Titan Text Embeddings V2 | Floating-point, binary | 256, 512, 1024 | 
| Cohere Embed (English) | Floating-point, binary | 1024 | 
| Cohere Embed (Multilingual) | Floating-point, binary | 1024 | 
| Amazon Titan Multimodal Embeddings G1 | Floating-point | 1024 | 
| Cohere Embed v3 (Multimodal) | Floating-point, binary | 1024 | 
| Amazon Nova Multimodal Embeddings | Floating-point | 1024 | 

## Supported models and Regions for parsing
<a name="knowledge-base-supported-parsing"></a>

When converting data into vector embeddings, you have different options for parsing your data in Amazon Bedrock Knowledge Bases. For more information, see [Parsing options for your data source](kb-advanced-parsing.md).

The following lists support for parsing options:
+ The Amazon Bedrock Data Automation parser is supported in US West (Oregon) and is in preview and subject to change.
+ The following foundation model families can be used as a parser:
  + Claude vision models
  + Nova vision models
  + LLama 4 vision models

  For current model availability by Region, see [Supported foundation models in Amazon Bedrock](models-supported.md).

## Supported models and Regions for reranking results during query
<a name="knowledge-base-supported-rerank"></a>

When retrieving knowledge base query results, you can use a reranking model to rerank results from knowledge base query. For more information, see [Query a knowledge base and retrieve data](kb-test-retrieve.md) and [Query a knowledge base and generate responses based off the retrieved data](kb-test-retrieve-generate.md).

For a list of models and Regions that support reranking, see [Supported Regions and models for reranking in Amazon Bedrock](rerank-supported.md).

## Supported Regions for Knowledge Bases with structured data stores
<a name="knowledge-base-supported-structured"></a>

Knowledge Bases with structured data stores allow you to connect knowledge bases to structured data stores and convert natural language queries into SQL queries. For more information, see [Build a knowledge base by connecting to a structured data store](knowledge-base-build-structured.md).

Knowledge Bases with structured data stores are available in the following AWS Regions:
+ Europe (Frankfurt)
+ Europe (Zurich)
+ Europe (Ireland)
+ Europe (London)
+ Europe (Paris)
+ Asia Pacific (Tokyo)
+ Asia Pacific (Seoul)
+ Asia Pacific (Mumbai)
+ Asia Pacific (Singapore)
+ Asia Pacific (Sydney)
+ Canada (Central)
+ South America (São Paulo)
+ US East (N. Virginia)
+ US East (Ohio)
+ US West (Oregon)
+ AWS GovCloud (US-West)