

# Build a knowledge base with Amazon Neptune Analytics graphs
<a name="knowledge-base-build-graphs"></a>

Amazon Bedrock Knowledge Bases offers a fully managed GraphRAG feature with Amazon Neptune. GraphRAG is a capability provided with Amazon Bedrock Knowledge Bases that combines graph modeling with generative AI to enhance retrieval-augmented generation (RAG). This feature combines vector search with the ability to quickly analyze large amounts of graph data from Amazon Neptune in RAG applications.

GraphRAG automatically identifies and uses relationships between entities and structural elements within documents ingested into Knowledge Bases. This enables more comprehensive and contextually relevant responses from the foundation models, particularly when the information needs to be connected through multiple logical steps. This means that generative AI applications can deliver more relevant responses in cases where connecting data and reasoning across multiple document chunks is needed. This empowers applications like chatbots to deliver more relevant responses from foundation models (FMs) in cases where related facts, entities, and relationships derived from multiple document sources are required to answer questions.

## GraphRAG Region availability
<a name="knowledge-base-build-graphs-regions"></a>

GraphRAG is available in the following AWS Regions:
+ Europe (Frankfurt)
+ Europe (London)
+ Europe (Ireland)
+ US West (Oregon)
+ US East (N. Virginia)
+ Asia Pacific (Tokyo)
+ Asia Pacific (Singapore)

## Benefits of using GraphRAG
<a name="knowledge-base-build-graphs-benefits"></a>

Amazon Bedrock Knowledge Bases with GraphRAG offers the following benefits:
+ More relevant and comprehensive responses by automatically identifying and using relationships between entities and structural elements (such as section titles) across multiple document sources that are ingested into Amazon Bedrock Knowledge Bases.
+ Enhanced ability to perform exhaustive searches that connect different pieces of content through multiple logical steps, improving upon traditional RAG techniques.
+ Better cross-document reasoning capabilities, allowing for more precise and contextually accurate answers by connecting information across various sources, which helps further enhance accuracy and minimize hallucinations.

## How GraphRAG works
<a name="knowledge-base-build-graphs-works"></a>

After performing an initial vector search for the relevant nodes, Amazon Bedrock Knowledge Bases GraphRAG performs the following steps to generate a better response:

1. Retrieves related graph nodes or chunk identifiers that are linked to the retrieved document chunks.

1. Expands on these related chunks by traversing the graph and retrieving their details from the graph database.

1. Provides more meaningful responses by understanding the relevant entities and focusing on the key connections using this enriched context.

## GraphRAG considerations and limitations
<a name="knowledge-base-build-graphs-considerations"></a>

The following are some limitations when using Amazon Bedrock Knowledge Bases with GraphRAG
+ Configuration options to customize the graph build are not supported.
+ Autoscaling is not supported for Amazon Neptune Analytics graphs.
+ GraphRAG only supports Amazon S3 as the data source.
+ You choose a foundation model for graph construction when you create a knowledge base or configure a data source. Selecting a graph construction model automatically enables contextual enrichment. For more information, see [Choose and update the graph construction model](knowledge-base-build-graphs-build.md#knowledge-base-build-graphs-model).
+ Each data source can have up to 1000 files. You can request to increase this limit to a maximum of 10000 files per data source. Alternatively, you can partition your Amazon S3 bucket into folders, where each folder can contain up to 1000 files.
+ If you use hierarchical chunking as the chunking strategy, GraphRAG retrieves only the child chunks during the search operation. It doesn't replace the child chunks with their corresponding parent chunks. This means your search results contain the specific, detailed content from child chunks rather than the broader context from parent chunks.

**Note**  
When deleting a knowledge base that uses Amazon Neptune Analytics, delete the knowledge base first, then delete the Amazon Neptune Analytics graph. Deleting a knowledge base doesn't automatically delete the underlying graph. Additional charges may be incurred until you explicitly delete the graph. Alternatively, set your data source deletion policy to RETAIN mode to delete the graph first without causing failures. For more information, see [Delete a data source from your Amazon Bedrock knowledge base](kb-ds-delete.md).

**Important**  
Foundation models can reach end-of-life or be deprecated. For example, Claude 3 Haiku has moved to Legacy status. We recommend that you select a currently supported model for graph construction. To check the status of available models, see [Model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html). For information about choosing or updating your graph construction model, see [Choose and update the graph construction model](knowledge-base-build-graphs-build.md#knowledge-base-build-graphs-model).