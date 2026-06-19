

# Sync a data source
<a name="kb-managed-sync"></a>

After you create your knowledge base, you ingest or sync your data so that the data can be queried. Ingestion converts the raw data in your data source into vector embeddings.

Before you begin ingestion, check that your data source fulfills the following conditions:
+ You have configured the connection information for your data source. See [Connect a data source](kb-managed-connect-ds.md). You configure your data source as part of creating your knowledge base.
+ You have configured your chosen vector embeddings model. See [supported vector embeddings models](kb-managed-create.md#kb-managed-embedding-models). You configure your vector embeddings as part of creating your knowledge base.
+ The files are in supported formats. For more information, see [Supported document formats](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html#kb-ds-supported-doc-formats-limits).
+ The files don't exceed the **Ingestion job file size** specified in [Service quotas](kb-managed-quotas.md) and quotas in the AWS General Reference.

Each time you add, modify, or remove files from your data source, you must sync the data source so that it is re-indexed to the knowledge base. Syncing is incremental, so Amazon Bedrock only processes added, modified, or deleted documents since the last sync.

To learn how to ingest your data into your knowledge base and sync with your latest data, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To ingest your data into your knowledge base and sync with your latest data**

1. Sign in to the AWS Management Console and navigate to Amazon Bedrock AgentCore > **Built-in tools** > **Knowledge Base**.

1. Choose your knowledge base.

1. In the **Data source** section, select **Sync** to begin data ingestion or syncing your latest data. To stop a data source currently syncing, select **Stop**. A data source must be currently syncing in order to stop syncing the data source. You can select **Sync** again to ingest the rest of your data.

1. When data ingestion completes, a green success banner appears if it is successful.

1. You can choose a data source to view its **Sync history**. Select **View warnings** to see why a data ingestion job failed.

------
#### [ API ]

To ingest your data into your knowledge base and sync with your latest data, send a [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `knowledgeBaseId` and `dataSourceId`. You can also stop a data ingestion job that is currently running by sending a [StopIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StopIngestionJob.html) request. Specify the `dataSourceId`, `ingestionJobId`, and `knowledgeBaseId`. A data ingestion job must be currently running in order to stop data ingestion. You can send a `StartIngestionJob` request again to ingest the rest of your data when you are ready.

Use the `ingestionJobId` returned in the response in a [GetIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) to track the status of the ingestion job. In addition, specify the `knowledgeBaseId` and `dataSourceId`.
+ When the ingestion job finishes, the `status` in the response is `COMPLETE`.
+ The `statistics` object in the response returns information about whether ingestion was successful or not for documents in the data source.

You can also see information for all ingestion jobs for a data source by sending a [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `dataSourceId` and the `knowledgeBaseId` of the knowledge base that the data is being ingested to.
+ Filter for results by specifying a status to search for in the `filters` object.
+ Sort by the time that the job was started or the status of a job by specifying the `sortBy` object. You can sort in ascending or descending order.
+ Set the maximum number of results to return in a response in the `maxResults` field. If there are more results than the number you set, the response returns a `nextToken` that you can send in another [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request to see the next batch of jobs.

------