

# Adding data sources and starting ingestion
<a name="kb-multimodal-add-data-source-and-ingest"></a>

After creating your knowledge base, add data sources containing your multimodal content and start ingestion jobs to process and index the content.

**Data source deletion behavior**  
When you delete a data source with the deletion policy set to RETAIN, the ingested content remains in the vector database and will continue to be used for retrieval. The content is only removed if you explicitly sync the knowledge base after deleting the data source. Data sources with the default DELETE policy will automatically remove content from the vector database and supplemental storage during deletion. This ensures that your knowledge base continues to function even if source files are modified or deleted, but you should be aware that deleted data sources with RETAIN policy may still contribute to search results.

## Add data sources
<a name="kb-multimodal-add-data-source"></a>

Add data sources containing your multimodal content to your knowledge base.

**Important**  
For BDA data sources: Only data sources created after the launch of audio/video support will process audio and video files. Existing BDA data sources created before this feature launch will continue to skip audio and video files. To enable audio/video processing for existing knowledge bases, create new data sources.

------
#### [ Console ]

**To add a data source from the console**

1. From your knowledge base details page, choose **Add data source**.

1. Choose **Amazon S3** as your data source type.

1. Provide a name and description for your data source.

1. Configure the Amazon S3 location containing your multimodal files by providing the bucket URI and any inclusion prefixes.

1. Under **Content parsing and chunking**, configure your parsing and chunking methods:
**Note**  
Text embedding models limit retrieval to text-only content, but you can enable multimodal retrieval via text by selecting either Amazon Bedrock Data Automation (for audio, video, and images) or Foundation Model as parsers (for images).

   Choose from three parsing strategies:
   + **Bedrock default parser:** Recommended for text-only parsing. This parser ignores multimodal content and is commonly used with multimodal embedding models.
   + **Bedrock Data Automation as parser:** Enables parsing and storing multimodal content as text, supporting PDFs, images, audio, and video files.
   + **Foundation model as parser:** Provides advanced parsing for images and structured documents, supporting PDFs, images, tables, and visually rich documents.

1. Choose **Add data source** to create the data source.

------
#### [ CLI ]

**To add a data source using the AWS CLI**
+ Create a data source for your multimodal content. Send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request:

  ```
  aws bedrock-agent create-data-source \
  --knowledge-base-id <knowledge-base-id> \
  --cli-input-json file://ds-multimodal.json
  ```

  For Nova Multimodal Embeddings (no special parsing configuration needed), use this `ds-multimodal.json` content:

  ```
  {
      "dataSourceConfiguration": {
          "type": "S3",
          "s3Configuration": {
              "bucketArn": "arn:aws:s3:::<data-source-bucket>",
              "inclusionPrefixes": ["<folder-path>"]
          }
      },
      "name": "multimodal_data_source",
      "description": "Data source with multimodal content",
      "dataDeletionPolicy": "RETAIN"
  }
  ```

  For BDA parsing approach, use this configuration:

  ```
  {
      "dataSourceConfiguration": {
          "type": "S3",
          "s3Configuration": {
              "bucketArn": "arn:aws:s3:::<data-source-bucket>",
              "inclusionPrefixes": ["<folder-path>"]
          }
      },
      "name": "multimodal_data_source_bda",
      "description": "Data source with BDA multimodal parsing",
      "dataDeletionPolicy": "RETAIN",
      "vectorIngestionConfiguration": {
          "parsingConfiguration": {
              "bedrockDataAutomationConfiguration": {
                  "parsingModality": "MULTIMODAL"
              }
          }
      }
  }
  ```

------

## Start an ingestion job
<a name="kb-multimodal-start-ingestion"></a>

After adding your data sources, start an ingestion job to process and index your multimodal content.

------
#### [ Console ]

**To start ingestion from the console**

1. From your data source details page, choose **Sync**.

1. Monitor the sync status on the data source page. Ingestion may take several minutes depending on the size and number of your multimodal files.

1. Once sync completes successfully, your multimodal content is ready for querying.

------
#### [ CLI ]

**To start ingestion using the AWS CLI**

1. Start an ingestion job. Send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) request:

   ```
   aws bedrock-agent start-ingestion-job \
   --knowledge-base-id <knowledge-base-id> \
   --data-source-id <data-source-id>
   ```

   Replace the placeholders with:
   + `<knowledge-base-id>` - ID from knowledge base creation
   + `<data-source-id>` - ID from data source creation

1. Monitor the ingestion job status using [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html).

------

## Resyncing after data source deletion
<a name="kb-multimodal-resync-after-deletion"></a>

If you delete a data source and want to remove its content from the knowledge base, you must explicitly resync the knowledge base:

**To remove deleted data source content**

1. Delete the data source using the console or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteDataSource.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteDataSource.html) API.

1. Start a new ingestion job on any remaining data sources to update the vector database and remove content from the deleted data source.

1. Verify that queries no longer return results from the deleted data source.

**Note**  
Without resyncing, content from deleted data sources will continue to appear in search results even though the data source no longer exists.