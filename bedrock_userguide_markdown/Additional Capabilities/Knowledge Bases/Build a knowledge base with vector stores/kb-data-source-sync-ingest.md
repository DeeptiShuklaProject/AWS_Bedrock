

# Sync your data with your Amazon Bedrock knowledge base
<a name="kb-data-source-sync-ingest"></a>

After you create your knowledge base, you ingest or sync your data so that the data can be queried. Ingestion converts the raw data in your data source into vector embeddings, based on the vector embeddings model and configurations you specified.

Before you begin ingestion, check that your data source fulfills the following conditions:
+ You have configured the connection information for your data source. To configure a data source connector to crawl your data from your data source repository, see [Supported data source connectors](https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html). You configure your data source as part of creating your knowledge base.
+ You have configured your chosen vector embeddings model and vector store. See [supported vector embeddings models](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html) and [vector stores for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html). You configure your vector embeddings as part of creating your knowledge base.
+ The files are in supported formats. For more information, see [Support document formats](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html#kb-ds-supported-doc-formats-limits).
+ The files don't exceed the **Ingestion job file size** specified in [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) in the AWS General Reference.
+ If your data source contains metadata files, check the following conditions to ensure that the metadata files aren't ignored:
  + Each `.metadata.json` file shares the same file name and extension as the source file that it's associated with.
  + If the vector index for your knowledge base is in an Amazon OpenSearch Serverless vector store, check that the vector index is configured with the `faiss` engine. If the vector index is configured with the `nmslib` engine, you'll have to do one of the following:
    + [Create a new knowledge base](knowledge-base-create.md) in the console and let Amazon Bedrock automatically create a vector index in Amazon OpenSearch Serverless for you.
    + [Create another vector index](knowledge-base-setup.md) in the vector store and select `faiss` as the **Engine**. Then [create a new knowledge base](knowledge-base-create.md) and specify the new vector index.
  + If the vector index for your knowledge base is in an Amazon Aurora database cluster, we recommend that you use the custom metadata field to store all your metadata in a single column and create an index on this column. If you do not provide the custom metadata field, you must check that the table for your index contains a column for each metadata property in your metadata files before starting ingestion. For more information, see [Prerequisites for using a vector store you created for a knowledge base](knowledge-base-setup.md).

Each time you add, modify, or remove files from your data source, you must sync the data source so that it is re-indexed to the knowledge base. Syncing is incremental, so Amazon Bedrock only processes added, modified, or deleted documents since the last sync.

## How a knowledge base handles resyncs
<a name="kb-data-source-sync-ingest-resync"></a>

Each time you add, modify, or remove files from your data source, you must sync the data source so that it is re-indexed in the knowledge base. Syncing is incremental, so Amazon Bedrock processes only the documents that were added, modified, or deleted since the last sync. When you sync a data source, Amazon Bedrock re-ingests documents to ensure accuracy and consistency. Re-ingestion includes parsing, chunking, generating embeddings, and indexing into the vector store.


**Sync scenarios**  

| Scenario | What happens | 
| --- | --- | 
| No changes detected | The document is skipped. | 
| Content or metadata changed | The document is re-ingested (re-parsed, re-chunked, re-embedded, and re-indexed). | 
| New document added | Only the new document is ingested. | 
| Document deleted | The document is removed from the vector store. | 

### Metadata-only optimization
<a name="kb-data-source-sync-ingest-metadata-optimization"></a>

In certain cases, Amazon Bedrock can update metadata without re-ingesting the document associated with that metadata file. This optimization retrieves existing vector embeddings from the vector store, merges the new metadata, and writes the updated embeddings back, which avoids calls to the embedding model.

This optimization applies only when all of the following conditions are met:
+ Only `metadata.json` files are modified. No content files are changed.
+ The associated content files are not CSV files.
+ The data source does not use a custom transformation Lambda function.

### Re-ingestion behavior for CSV files
<a name="kb-data-source-sync-ingest-csv-reingestion"></a>

CSV files use the `documentStructureConfiguration` field in metadata to control which columns are indexed. Because Amazon Bedrock cannot determine whether this structural configuration changed without re-processing the file, CSV files are always re-ingested when their metadata files are updated.

To learn how to ingest your data into your knowledge base and sync with your latest data, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To ingest your data into your knowledge base and sync with your latest data**

1. Open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock/](https://console.aws.amazon.com/bedrock/).

1. From the left navigation pane, select **Knowledge base** and choose your knowledge base.

1. In the **Data source** section, select **Sync** to begin data ingestion or syncing your latest data. To stop a data source currently syncing, select **Stop**. A data source must be currently syncing to stop syncing the data source. You can select **Sync** again to ingest the rest of your data.

1. When data ingestion completes, a green success banner appears if it is successful.
**Note**  
After data syncing completes, it could take a few minutes for the vector embeddings of the newly synced data to reflect in your knowledge base and be available for querying if you use a vector store other than Amazon Aurora (RDS).

1. You can choose a data source to view its **Sync history**. Select **View warnings** to see why a data ingestion job failed.

------
#### [ API ]

To ingest your data into your knowledge base and sync with your latest data, send a [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `knowledgeBaseId` and `dataSourceId`. You can also stop a data ingestion job that is currently running by sending a [StopIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StopIngestionJob.html) request. Specify the `dataSourceId`, `ingestionJobId`, and `knowledgeBaseId`. A data ingestion job must be currently running in order to stop data ingestion. You can send a `StartIngestionJob` request again to ingest the rest of your data when you are ready.

Use the `ingestionJobId` returned in the response in a [GetIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) to track the status of the ingestion job. In addition, specify the `knowledgeBaseId` and `dataSourceId`.
+ When the ingestion job finishes, the `status` in the response is `COMPLETE`.
**Note**  
After data ingestion completes, it could take few minutes for the vector embeddings of the newly ingested data to be available in the vector store for querying if you use a vector store other than Amazon Aurora (RDS).
+ The `statistics` object in the response returns information about whether ingestion was successful or not for documents in the data source.

You can also see information for all ingestion jobs for a data source by sending a [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `dataSourceId` and the `knowledgeBaseId` of the knowledge base that the data is being ingested to.
+ Filter for results by specifying a status to search for in the `filters` object.
+ Sort by the time that the job was started or the status of a job by specifying the `sortBy` object. You can sort in ascending or descending order.
+ Set the maximum number of results to return in a response in the `maxResults` field. If there are more results than the number you set, the response returns a `nextToken` that you can send in another [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request to see the next batch of jobs.

------