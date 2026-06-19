

# View data source information for your Amazon Bedrock knowledge base
<a name="kb-managed-ds-info"></a>

You can view information about a data source for your knowledge base, such as the settings and sync history.

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a data source**

1. Sign in to the AWS Management Console and navigate to Amazon Bedrock AgentCore > **Built-in tools** > **Knowledge Base**.

1. Choose your knowledge base.

1. In the **Data source** section, select the data source for which you want to view details.

1. The **Data source overview** contains details about the data source.

1. The **Sync history** contains details about when the data source was synced. To see reasons for why a sync event failed, select a sync event and choose **View warnings**.

------
#### [ API ]

To get information about a data source, send a [GetDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetDataSource.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the `dataSourceId` and the `knowledgeBaseId` of the knowledge base that it belongs to.

To list information about a knowledge base's data sources, send a [ListDataSources](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListDataSources.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ID of the knowledge base.
+ To set the maximum number of results to return in a response, use the `maxResults` field.
+ If there are more results than the number you set, the response returns a `nextToken`. You can use this value in another `ListDataSources` request to see the next batch of results.

To get information about a sync event for a data source, send a [GetIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `dataSourceId`, `knowledgeBaseId`, and `ingestionJobId`.

To list the sync history for a data source in a knowledge base, send a [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request with a [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the ID of the knowledge base and data source. You can set the following specifications.
+ Filter for results by specifying a status to search for in the `filters` object.
+ Sort by the time that the job was started or the status of a job by specifying the `sortBy` object. You can sort in ascending or descending order.
+ Set the maximum number of results to return in a response in the `maxResults` field. If there are more results than the number you set, the response returns a `nextToken` that you can send in another [ListIngestionJobs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListIngestionJobs.html) request to see the next batch of jobs.

------