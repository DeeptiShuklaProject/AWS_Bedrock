

# View information about documents in your data source
<a name="kb-direct-ingestion-view"></a>

The following topics describe how to view documents in your data source. If your knowledge base is connected to an Amazon S3 data source, you can view the documents in the connected S3 bucket.

**Note**  
If you created a new knowledge base by connecting to an S3 data source, you must sync the data source first before you can use these API operations on the data source.

Expand the method that corresponds to your use case:

## Use the console
<a name="kb-direct-ingestion-view-console"></a>

To view documents in your data source that have been ingested in the AWS Management Console, do the following:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, select the knowledge base whose documents you want to view.

1. In the **Data source** section, select the data source whose documents you want to view.

1. The **Documents** section lists the documents in the data source. These documents have also been ingested into the knowledge base.

## Use the API
<a name="kb-direct-ingestion-view-api"></a>

With the Amazon Bedrock API, you can view a subset or all of the documents in your data source that have been ingested into the knowledge base. Select the topic that pertains to your use case.

**Topics**
+ [View information about a subset of documents in your knowledge base](#kb-direct-ingestion-get)
+ [View information about all documents in your knowledge base](#kb-direct-ingestion-list)

### View information about a subset of documents in your knowledge base
<a name="kb-direct-ingestion-get"></a>

To view information about specific documents in your data source, send a [GetKnowledgeBaseDocuments](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetKnowledgeBaseDocuments.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the IDs of the data source and the knowledge base it's connected to.

For each document that you want to get information for, add a [DocumentIdentifier](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DocumentIdentifier.html) item in the `documentIdentifiers` array in one of the following formats:
+ If the data source is a custom one, specify the ID of the document in the `id` field:

  ```
  { 
      "custom": { 
          "id": "string"
      },
      "dataSourceType": "CUSTOM"
  }
  ```
+ If the data source is an Amazon S3 one, specify the S3 URI of the document in the `uri` field:

  ```
  {
      "dataSourceType": "S3",
      "s3": { 
          "uri": "string"
      }
  }
  ```

The response returns an array of items, each of which contains information about a document that you requested.

### View information about all documents in your knowledge base
<a name="kb-direct-ingestion-list"></a>

To view information about all documents in a data source, send a [ListKnowledgeBaseDocuments](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListKnowledgeBaseDocuments.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the IDs of tthe data source and the knowledge base it's connected to. You also have the following options:
+ Specify the `maxResults` to limit the number of results to return.
+ If the results don't fit into a response, a value is returned in the `nextToken` field of the response. You can use this value in the `nextToken` field of a subsequent request to get the next batch of results.