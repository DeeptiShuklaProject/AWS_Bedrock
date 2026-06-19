

# Improve the relevance of query responses with a reranker model in Amazon Bedrock
<a name="rerank"></a>

Amazon Bedrock provides access to reranker models that you can use when querying to improve the relevance of the retrieved results. A reranker model calculates the relevance of chunks to a query and reorders the results based on the scores that it calculates. By using a reranker model, you can return responses that are better suited to answering the query. Or, you can include the results in a prompt when running model inference to generate more pertinent and accurate responses. With a reranker model, you can retrieve fewer, but more relevant, results. By feeding these results to the foundation model that you use to generate a response, you can also decrease cost and latency.

Reranker models are trained to identify relevance signals based on a query and then use those signals to rank documents. Because of this, the models can provide more relevant, more accurate results.

**Note**  
You can use reranking for only textual data.

For information about pricing for reranking models, see [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/).

Reranking requires the following input, at the minimum:
+ A reranker model that takes a user query and assesses the relevance of the data sources that it can access.
+ The user query.
+ A list of documents that the reranker must reorder according to their relevance to the query.

You can use reranker models in Amazon Bedrock in the following ways:
+ Call the [Rerank](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rerank.html) operation directly through the Amazon Bedrock API. The `Rerank` operation sends the query, documents, and any additional configurations as input to a reranker model. The model then reranks the documents by relevance to the query and returns the documents in the response.
+ If you're using [Amazon Bedrock Knowledge Bases](knowledge-base.md) for building your Retrieval Augmented Generation (RAG) application, use a reranker model while calling the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) operation or when querying your knowledge base in the AWS Management Console. The results from reranking override the default ranking that Amazon Bedrock Knowledge Bases determines.

**Topics**
+ [Pricing](rerank-pricing.md)
+ [Supported Regions/models](rerank-supported.md)
+ [Permissions](rerank-prereq.md)
+ [Use a reranker model](rerank-use.md)