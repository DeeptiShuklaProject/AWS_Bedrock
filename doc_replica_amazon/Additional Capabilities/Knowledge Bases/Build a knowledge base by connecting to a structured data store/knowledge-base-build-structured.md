

# Build a knowledge base by connecting to a structured data store
<a name="knowledge-base-build-structured"></a>

Amazon Bedrock Knowledge Bases allows you to connect to structured data stores, which contain data that conforms to a predefined schema. Examples of structured data include tables and databases. Amazon Bedrock Knowledge Bases can convert user queries into language that is suitable for extracting data from supported structured data stores. It can then use the converted query to retrieve data that is relevant to the query and generate appropriate responses. This enables you to use the existing structured data directly without having to convert it to a different format or generate your own SQL queries.

After you set up your knowledge base, you can submit queries to retrieve data from it through the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) operation, or generate responses from the retrieved data through the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) operation. These operations underlyingly convert the user queries into ones that are appropriate for the structured data store connected to the knowledge base.

You also have the option to convert queries independently of retrieving data by using the [GenerateQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerateQuery.html) API operation. This operation converts natural language queries into SQL queries that are appropriate to the data source being queried. You can use this operation independently and insert it into your workflow.

Select a topic to learn about the prerequisites and process for connecting your knowledge base to a structured data store.

**Topics**
+ [Set up your query engine and permissions for creating a knowledge base with structured data store](knowledge-base-prereq-structured.md)
+ [Create a knowledge base by connecting to a structured data store](knowledge-base-structured-create.md)
+ [Sync your structured data store with your Amazon Bedrock knowledge base](kb-data-source-structured-sync-ingest.md)
+ [Cross-region inference for knowledge bases with structured data store](kb-structured-cris.md)