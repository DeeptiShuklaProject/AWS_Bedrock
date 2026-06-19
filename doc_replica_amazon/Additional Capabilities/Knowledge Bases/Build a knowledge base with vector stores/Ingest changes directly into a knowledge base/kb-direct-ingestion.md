

# Ingest changes directly into a knowledge base
<a name="kb-direct-ingestion"></a>

Amazon Bedrock Knowledge Bases allows you to modify your data source and sync the changes in one step. You can take advantage of this feature if your knowledge base is connected to one of the following types of data sources:
+ Amazon S3
+ Custom

With direct ingestion, you can directly add, update, or delete files in a knowledge base in a single action and your knowledge base can have access to documents without the need to sync. Direct ingestion uses the `KnowledgeBaseDocuments` API operations to index the documents that you submit directly into the vector store set up for the knowledge base. You can also view the documents in your knowledge base directly with these operations, rather than needing to navigate to the connected data source to view them.

## Differences from syncing a data source
<a name="kb-direct-ingestion-sync-diff"></a>

Amazon Bedrock Knowledge Bases also offers a set of `IngestionJob` API operations that relate to [syncing your data source](kb-data-source-sync-ingest.md). When you sync your data source with a [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request, Amazon Bedrock Knowledge Bases scans each document in the connected data source and verifies whether it has already been indexed into the vector store set up for the knowledge base. If it hasn't, it becomes indexed into the vector store.

With an [IngestKnowledgeBaseDocuments](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_IngestKnowledgeBaseDocuments.html) request, you submit an array of documents to be directly indexed into the vector store. Therefore, you skip the step of adding documents into the data source. See the following paragraphs to understand the use case for these two sets of API operations:

**If you use a custom data source**  
You don't need to sync or use the `IngestionJob` operations. Documents that you add, modify, or delete with the `KnowledgeBaseDocuments` operations or in the AWS Management Console become part of both the custom data source and your knowledge base.

**If you use an Amazon S3 data source**  
You use the two sets of operations in different use cases:
+ After connecting the knowledge base to the S3 data source for the first time, you must sync your data source in the AWS Management Console or by submitting a [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request through the Amazon Bedrock API.
+ Index documents into the vector store set up for your knowledge base or remove the indexed documents in the following ways:

  1. Add documents into your S3 location or delete documents from it. Then sync your data source in the AWS Management Console or submit a `StartIngestionJob` request in the API. For details about syncing and the `StartIngestionJob` operation, see [Sync your data with your Amazon Bedrock knowledge base](kb-data-source-sync-ingest.md).

  1. Ingest S3 documents into the knowledge base directly with an `IngestKnowledgeBaseDocuments` request. For details about directly ingesting documents, see [Ingest documents directly into a knowledge base](kb-direct-ingestion-add.md).
**Warning**  
For S3 data sources, any changes that you index into the knowledge base directly in the AWS Management Console or with the `KnowledgeBaseDocuments` API operations aren't reflected in the S3 location. You can use these API operations to make changes to your knowledge base immediately available in a single step. However, you should follow up by making the same changes in your S3 location so that they aren't overwritten the next time you sync your data source in the AWS Management Console or with `StartIngestionJob`.  
Don't submit an `IngestKnowledgeBaseDocuments` and `StartIngestionJob` request at the same time.

Select a topic to learn how to perform direct ingestion of the documents in your data sources:

**Topics**
+ [Differences from syncing a data source](#kb-direct-ingestion-sync-diff)
+ [Prerequisites for direct ingestion](kb-direct-ingestion-prereq.md)
+ [Ingest documents directly into a knowledge base](kb-direct-ingestion-add.md)
+ [View information about documents in your data source](kb-direct-ingestion-view.md)
+ [Delete documents from a knowledge base directly](kb-direct-ingestion-delete.md)