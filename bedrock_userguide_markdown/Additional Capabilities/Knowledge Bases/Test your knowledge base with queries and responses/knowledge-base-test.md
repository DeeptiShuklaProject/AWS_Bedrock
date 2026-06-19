

# Test your knowledge base with queries and responses
<a name="knowledge-base-test"></a>

After you set up your knowledge base, you can test its behavior in the following ways:
+ Send queries and retrieving relevant information from your data sources, by using the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) operation.
+ Send queries and generate responses to the queries based on the retrieved information from your data sources.
+ Use a reranking model to retrieve more relevant sources.
+ Use optional metadata filters to specify which documents in your data source can be used.

When you are satisfied with your knowledge base's behavior, you can then set up your application to query the knowledge base or attach the knowledge base to an agent by proceeding to [Deploy your knowledge base for your AI application](knowledge-base-deploy.md).

The test behavior is different based on functionality available in self-managed knowledge bases or managed knowledge bases. If you are using managed knowledge bases, for example, you can use agentic retrieval to decompose complex queries into sub-queries and iteratively retrieve relevant information from your data sources, by using the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html) operation.

Select a topic to learn more about it.

**Topics**
+ [Query a knowledge base and retrieve data](kb-test-retrieve.md)
+ [Test your self-managed knowledge base](kb-test-self-managed.md)
+ [Test your managed knowledge base with queries and responses](kb-managed-test.md)