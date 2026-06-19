

# Test your managed knowledge base with queries and responses
<a name="kb-managed-test"></a>

After you set up your managed knowledge base, you can test its behavior in the following ways:
+ Retrieve relevant information from your data sources, by using the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) operation.
+ Use agentic retrieval to decompose complex queries into sub-queries and iteratively retrieve relevant information from your data sources, by using the `AgenticRetrieveStream` operation.
+ Connect to your knowledge base through AgentCore Gateway to expose it as an MCP tool.

Select a topic to learn more about it.

**Topics**
+ [ACL-aware retrieval on managed knowledge bases](kb-test-retrieve-acl.md)
+ [Retrieve the content of documents from knowledge base](kb-test-get-document-content.md)
+ [Use agentic retrieval to query a knowledge base](kb-test-agentic-retrieve.md)
+ [Configure and customize queries for managed knowledge bases](kb-managed-test-config.md)