

# Delete documents from a knowledge base directly
<a name="kb-direct-ingestion-delete"></a>

If you no longer need a document in your knowledge base, you can delete it directly. To learn how to delete documents from your data source and knowledge base, expand the section that corresponds to your use case:

## Use the console
<a name="kb-direct-ingestion-delete-console"></a>

To delete documents from your data source and knowledge base directly using the AWS Management Console, do the following:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, select the knowledge base from which to delete documents.

1. In the **Data source** section, select the data source from which to delete documents.

1. In the **Documents** section, select a document to delete. Then choose **Delete document**. Review the message and confirm.

## Use the API
<a name="kb-direct-ingestion-delete-api"></a>

To delete specific documents from your data source through the Amazon Bedrock API, send a [DeleteKnowledgeBaseDocuments](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteKnowledgeBaseDocuments.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the IDs of the data source and the knowledge base it's connected to.

For each document that you want to delete, add a [DocumentIdentifier](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DocumentIdentifier.html) item in the `documentIdentifiers` array in one of the following formats:
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

**Warning**  
Documents that you delete directly from a knowledge base connected to an S3 data source aren't deleted from the S3 bucket itself. We recommend that you delete these documents from the S3 bucket, so that they aren't reintroduced if you sync your data source.