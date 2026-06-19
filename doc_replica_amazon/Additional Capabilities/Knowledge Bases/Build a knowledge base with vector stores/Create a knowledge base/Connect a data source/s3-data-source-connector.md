

# Connect to Amazon S3 for your knowledge base
<a name="s3-data-source-connector"></a>

Amazon S3 is an object storage service that stores data as objects within buckets. You can connect to your Amazon S3 bucket for your Amazon Bedrock knowledge base by using either the [AWS Management Console for Amazon Bedrock](https://console.aws.amazon.com/bedrock/home) or the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) API (see Amazon Bedrock [supported SDKs and AWS CLI](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)).

**Multimodal content support**  
Amazon S3 data sources support multimodal content including images, audio, and video files. For comprehensive guidance on working with multimodal content, see [Build a knowledge base for multimodal content](kb-multimodal.md).

You can upload a small batch of files to an Amazon S3 bucket using the Amazon S3 console or API. You can alternatively use [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html) to upload multiple files to S3 continuously, and transfer files on a schedule from on-premises, edge, other cloud, or AWS storage.

Currently only General Purpose S3 buckets are supported.

There are limits to how many files and MB per file that can be crawled. See [Quotas for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html).

**Topics**
+ [Supported features](#supported-features-s3-connector)
+ [Prerequisites](#prerequisites-s3-connector)
+ [Connection configuration](#configuration-s3-connector)

## Supported features
<a name="supported-features-s3-connector"></a>
+ Document metadata fields
+ Inclusion prefixes
+ Incremental content syncs for added, updated, deleted content

## Prerequisites
<a name="prerequisites-s3-connector"></a>

**In Amazon S3, make sure you**:
+ Note the Amazon S3 bucket URI, Amazon Resource Name (ARN), and the AWS account ID for the owner of the bucket. You can find the URI and ARN in the properties section in the Amazon S3 console. Your bucket must be in the same Region as your Amazon Bedrock knowledge base. You must have permission to access the bucket.

**In your AWS account, make sure you**:
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions for this data source to add to your knowledge base IAM role, see [Permissions to access data sources](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html#kb-permissions-access-ds).

**Note**  
If you use the console, the IAM role with all the required permissions can be created for you as part of the steps for creating a knowledge base. After you have configured your data source and other configurations, the IAM role with all the required permissions are applied to your specific knowledge base.

## Connection configuration
<a name="configuration-s3-connector"></a>

To connect to your Amazon S3 bucket, you must provide the necessary configuration information so that Amazon Bedrock can access and crawl your data. You must also follow the [Prerequisites](#prerequisites-s3-connector).

An example of a configuration for this data source is included in this section.

For more information about inclusion filters, document metadata fields, incremental syncing, and how these work, select the following:

### Document metadata fields
<a name="ds-s3-metadata-fields"></a>

You can include a separate file that specifies the document metadata fields/attributes for each file in your Amazon S3 data source and whether to include them in the embeddings when indexing the data source into the vector store. For example, you can create a file in the following format, name it {{fileName.extension.metadata.json}} and upload it to your S3 bucket.

```
{
  "metadataAttributes": {
    "company": {
      "value": {
        "type": "STRING",
        "stringValue": "BioPharm Innovations"
      },
      "includeForEmbedding": true
    },
    "created_date": {
      "value": {
        "type": "NUMBER",
        "numberValue": 20221205
      },
      "includeForEmbedding": true
    },
    "author": {
      "value": {
        "type": "STRING",
        "stringValue": "Lisa Thompson"
      },
      "includeForEmbedding": true
    },
    "origin": {
      "value": {
        "type": "STRING",
        "stringValue": "Overview"
      },
      "includeForEmbedding": true
    }
  }
}
```

The metadata file must use the same name as its associated source document file, with `.metadata.json` appended onto the end of the file name. The metadata file must be stored in the same folder or location as the source file in your Amazon S3 bucket. The file must not exceed the limit of 10 KB. For information on the supported attribute/field data types and the filtering operators you can apply to your metadata fields, see [Metadata and filtering](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html).

The `includeForEmbedding` field controls whether a metadata attribute is included when embedding the chunk:
+ `includeForEmbedding: false` – Only the chunk text is embedded and turned into a vector during ingestion. The metadata is still stored and available for filtering, but does not influence semantic search results.
+ `includeForEmbedding: true` – The metadata key-value pair is concatenated to the chunk text before embedding (for example, `key1: value1\n\nchunk text`). This means the metadata information is included in the embedding vector, so queries mentioning the metadata key or value will contribute to the similarity score and boost search relevance. The metadata key-value pair is not included in the chunk text returned in results, ensuring that results contain only the raw content from source files.

You can also use a simplified format for metadata attributes when you don't need to control embedding behavior:

```
{
    "metadataAttributes": {
        "tag": "value"
    }
}
```

With the simplified format, the metadata is stored for filtering but is not included in the embedding (equivalent to `includeForEmbedding: false`).

### Inclusion prefixes
<a name="ds-s3-inclusion-exclusion"></a>

You can specify an inclusion prefix, which is an Amazon S3 path prefix, where you can use an S3 file or a folder instead of the entire bucket to create the S3 data source connector.

### Incremental syncing
<a name="ds-s3-incremental-sync"></a>

The data source connector crawls new, modified, and deleted content each time your data source syncs with your knowledge base. Amazon Bedrock can use your data source’s mechanism for tracking content changes and crawl content that changed since the last sync. When you sync your data source with your knowledge base for the first time, all content is crawled by default.

To sync your data source with your knowledge base, use the [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) API or select your knowledge base in the console and select **Sync** within the data source overview section.

**Important**  
All data that you sync from your data source becomes available to anyone with `bedrock:Retrieve` permissions to retrieve the data. This can also include any data with controlled data source permissions. For more information, see [Knowledge base permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).

------
#### [ Console ]

**To connect an Amazon S3 bucket to your knowledge base**

1. Follow the steps at [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md) and choose **Amazon S3** as the data source.

1. Provide a name for the data source.

1. Specify whether the Amazon S3 bucket is in your current AWS account or another AWS account. Your bucket must be in the same Region as the knowledge base.

1. (Optional) If the Amazon S3 bucket is encrypted with a KMS key, include the key. For more information, see [Permissions to decrypt your AWS KMS key for your data sources in Amazon S3](encryption-kb.md#encryption-kb-ds).

1. (Optional) In the **Content parsing and chunking** section, you can customize how to parse and chunk your data. Refer to the following resources to learn more about these customizations:
   + For more information about parsing options, see [Parsing options for your data source](kb-advanced-parsing.md).
   + For more information about chunking strategies, see [How content chunking works for knowledge bases](kb-chunking.md).
**Warning**  
You can't change the chunking strategy after connecting to the data source.
   + For more information about how to customize chunking of your data and processing of your metadata with a Lambda function, see [Use a custom transformation Lambda function to define how your data is ingested](kb-custom-transformation.md).

1. In the **Advanced settings** section, you can optionally configure the following:
   + **KMS key for transient data storage.** – You can encrypt the transient data while converting your data into embeddings with the default AWS managed key or your own KMS key. For more information, see [Encryption of transient data storage during data ingestion](encryption-kb.md#encryption-kb-ingestion).
   + **Data deletion policy** – You can delete the vector embeddings for your data source that are stored in the vector store by default, or choose to retain the vector store data.

1. Continue to choose an embeddings model and vector store. To see the remaining steps, return to [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md) and continue from the step after connecting your data source.

------
#### [ API ]

The following is an example of a configuration for connecting to Amazon S3 for your Amazon Bedrock knowledge base. You configure your data source using the API with the AWS CLI or supported SDK, such as Python. After you call [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html), you call [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) to create your data source with your connection information in `dataSourceConfiguration`.

To learn about customizations that you can apply to ingestion by including the optional `vectorIngestionConfiguration` field, see [Customize ingestion for a data source](kb-data-source-customize-ingestion.md).

**AWS Command Line Interface**

```
aws bedrock-agent create-data-source \
 --name "S3-connector" \
 --description "S3 data source connector for Amazon Bedrock to use content in S3" \
 --knowledge-base-id "your-knowledge-base-id" \
 --data-source-configuration file://s3-bedrock-connector-configuration.json \
 --data-deletion-policy "DELETE" \
 --vector-ingestion-configuration '{"chunkingConfiguration":{"chunkingStrategy":"FIXED_SIZE","fixedSizeChunkingConfiguration":{"maxTokens":100,"overlapPercentage":10}}}'
                    
s3-bedrock-connector-configuration.json
{
    "s3Configuration": {
	    "bucketArn": "arn:aws:s3:::bucket-name",
	    "bucketOwnerAccountId": "000000000000",
	    "inclusionPrefixes": [
	        "documents/"
	    ]
    },
    "type": "S3"	
}
```

------