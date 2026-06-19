

# Sync your structured data store with your Amazon Bedrock knowledge base
<a name="kb-data-source-structured-sync-ingest"></a>

After you connect your knowledge base to a structured data store, you perform a sync to start the metadata ingestion process so that data can be retrieved. The metadata allows Amazon Bedrock Knowledge Bases to translate user prompts into a query for the connected database.

Whenever you make modifications to your database schema, you need to sync the changes.

To learn how to ingest your metadata into your knowledge base and sync with your latest data, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To ingest your data into your knowledge base and sync with your latest data**

1. Open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock/](https://console.aws.amazon.com/bedrock/).

1. From the left navigation pane, select **Knowledge base** and choose your knowledge base.

1. In the **Data source** section, select **Sync** to begin the metadata ingestion process. To stop a data source currently syncing, select **Stop**. A data source must be currently syncing to stop syncing the data source. You can select **Sync** again to ingest the rest of your data.

1. When data ingestion completes, a green success banner appears if it is successful.

1. You can choose a data source to view its **Sync history**. Select **View warnings** to see why a data ingestion job failed.

------
#### [ API ]

To ingest your data into your knowledge base and sync with your latest data, send a [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

Use the `ingestionJobId` returned in the response in a [GetIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) to track the status of the ingestion job.

You can see information for all ingestion jobs for a data source by sending a [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

To stop a data ingestion job that is currently running, send a [StopIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StopIngestionJob.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). You can send a `StartIngestionJob` request again to ingest the rest of your data when you are ready.

------

**Important**  
If you use the Amazon Bedrock Knowledge Bases service role created for you in the console and then sync your data store before granting access to your database to the authentication role that you use, the sync will fail because the user hasn't been granted permissions to access your data store. For information about granting permissions to a role to access your data store, see [Allow knowledge base service role to access your data store](knowledge-base-prereq-structured.md#knowledge-base-prereq-structured-db-access).