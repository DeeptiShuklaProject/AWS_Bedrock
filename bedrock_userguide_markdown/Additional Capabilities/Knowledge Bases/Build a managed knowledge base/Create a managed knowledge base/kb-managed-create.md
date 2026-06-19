

# Create a managed knowledge base
<a name="kb-managed-create"></a>

When you create a managed knowledge base, Amazon Bedrock AgentCore manages the storage, indexing, and retrieval infrastructure for you. By default, a service-managed embedding model is used and no model selection or configuration is required. You can optionally provide your own Bedrock embedding model instead. You can also optionally provide a KMS key for encryption of the managed vector store.

After you create the knowledge base, connect it to a data source and start ingestion. For details on connecting a data source, see [Connect a data source](kb-managed-connect-ds.md). To sync a data source, use the `StartIngestionJob` API. For details, see [Sync your data with your Amazon Bedrock knowledge base](kb-data-source-sync-ingest.md).

To learn how to create a managed knowledge base, choose the tab for your preferred method:

------
#### [ Console ]

**To create a managed knowledge base**

1. Sign in to the AWS Management Console and navigate to Amazon Bedrock AgentCore > **Built-in tools** > **Knowledge Base**.

1. Choose **Create Managed Knowledge Base**.

1. (Optional) Expand **Additional configurations** of **Knowledge Base details** section to configure the following:
   + Add a description.
   + Choose an embedding model type:
     + **Managed** (default): A service-managed embedding model is used. No model selection or configuration is required.
     + **Custom**: Select a Bedrock embedding model. Choose the model to open the model selector, which shows available providers (Amazon, Cohere) and models.
   + Configure IAM permissions: choose **Create and use a new service role** (recommended) or select an existing role.
   + Configure AWS KMS encryption for the managed vector store (AWS managed key by default, or select a custom KMS key).

1. Under **Data source**, provide a data source name.

1. Select your data source type from the dropdown: Amazon S3, Confluence, Custom, Google Drive, OneDrive, SharePoint, or Web Crawler.

1. Configure the data source connection settings for your selected data source type.

1. (Optional) Expand **Content parsing and chunking** to configure the following:
   + Parsing strategy is set to **Managed parser** by default.
   + Select a text chunking strategy from the dropdown:
     + **Default chunking** (recommended): Splits text into fixed-size chunks.
     + **Fixed-size chunking**: Splits text into your set approximate token size.
     + **No chunking**: For pre-processed or pre-split documents.

1. (Optional) Expand **Advanced configurations** to configure advanced indexing. Under **Content indexing**, the default indexes text-based content from common documents. Enable advanced indexing for additional modalities:
   + **Visual content in documents**: Processes embedded visuals in .pdf, .docx, .ppt, .pptx files.
   + **Audio files**: Processes .mp3, .wav, .m4a, .flac, .ogg files.
   + **Video files**: Processes .mp4, .mov, .m4v files.

   Optionally set a maximum file size (MB) and configure the document deletion safeguard.

1. (Optional) Configure log delivery to send knowledge base ingestion logs to a destination such as CloudWatch Logs, Amazon S3, or Firehose.

1. Choose **Create Knowledge Base**.

1. Wait for the knowledge base and data source to be created (2–5 minutes). If you create a managed knowledge base with a customer managed key, the creation may take longer.

------
#### [ API ]

The following is an example of creating a managed knowledge base and configuring your data source using the API with the AWS CLI or supported SDK, such as Python. After you call [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html), you call [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) to create your data source with your connection information in `dataSourceConfiguration`.

To learn about customizations that you can apply to ingestion by including the optional `vectorIngestionConfiguration` field, see [Customize ingestion for a data source](kb-managed-customize-ingestion.md).

**AWS Command Line Interface**

**Step 1: Create the knowledge base**

With a managed embedding model (default):

```
aws bedrock-agent create-knowledge-base \
 --name "{{my-managed-kb}}" \
 --role-arn "{{arn:aws:iam::123456789012:role/BedrockKBRole}}" \
 --description "{{My managed knowledge base}}" \
 --knowledge-base-configuration file://kb-config.json

kb-config.json
{
    "type": "MANAGED",
    "managedKnowledgeBaseConfiguration": {
        "embeddingModelType": "MANAGED"
    }
}
```

With a custom embedding model (customer-provided Bedrock model):

```
aws bedrock-agent create-knowledge-base \
 --name "{{my-custom-embed-kb}}" \
 --role-arn "{{arn:aws:iam::123456789012:role/BedrockKBRole}}" \
 --description "{{My managed knowledge base with custom embedding}}" \
 --knowledge-base-configuration file://kb-config.json

kb-config.json
{
    "type": "MANAGED",
    "managedKnowledgeBaseConfiguration": {
        "embeddingModelType": "CUSTOM",
        "embeddingModelArn": "{{arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v2:0}}",
        "embeddingModelConfiguration": {
            "bedrockEmbeddingModelConfiguration": {
                "dimensions": 1024
            }
        }
    }
}
```

**Note**  
When `embeddingModelType` is omitted, it defaults to `MANAGED`. When using `MANAGED`, you must not specify `embeddingModelArn` or `embeddingModelConfiguration`. When using `CUSTOM`, both fields are required.

**Step 2: Create a data source**

```
aws bedrock-agent create-data-source \
 --name "{{S3-connector}}" \
 --description "{{S3 data source connector for Amazon Bedrock to use content in S3}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://bedrock-s3-managed-connector-configuration.json \
 --data-deletion-policy "DELETE" \
 --vector-ingestion-configuration '{"parsingConfiguration":{"parsingStrategy":"SMART_PARSING"}}'

bedrock-s3-managed-connector-configuration.json
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "mediaExtractionConfiguration": {
            "imageExtractionConfiguration": {
                "imageExtractionStatus": "ENABLED"
            }
        },
        "connectorParameters": {
            "type": "S3",
            "version": "1",
            "connectionConfiguration": {
                "bucketName": "{{your-test-s3-bucket}}",
                "bucketOwnerAccountId": "{{123456789012}}"
            },
            "deletionProtectionConfiguration": {
                "enableDeletionProtection": false
            }
        }
    }
}
```

------

## Embedding model options
<a name="kb-managed-embedding-models"></a>

Managed knowledge bases support two embedding model types:
+ **Managed embedding** (default) – A service-managed embedding model is used automatically. You don't need to select a model, configure dimensions, or manage Bedrock service limits for embedding. The service handles model selection, hosting, and scaling transparently.
+ **Custom embedding** – You provide your own Bedrock embedding model ARN. When using a custom embedding model, you must specify the model dimensions (1024) and float32 embedding data type. The following Bedrock embedding models are supported:
  + Amazon Titan Text Embeddings V2
  + Cohere Embed English v3
  + Cohere Embed Multilingual v3
  + Cohere Embed v4
  + Amazon Nova Multimodal Embeddings

**Note**  
You cannot change the embedding model type after creating the knowledge base. To switch between managed and custom embedding, you must create a new knowledge base.

**Important**  
If you create a knowledge base with a custom embedding model, the managed reranker is not available for that knowledge base. To use the managed reranker, create your knowledge base with the default managed embedding model.

## Supported data source connectors
<a name="kb-managed-connectors"></a>

Managed knowledge bases support the following data source connectors:
+ Amazon S3
+ Confluence
+ Microsoft SharePoint
+ Google Drive
+ Microsoft OneDrive
+ Web Crawler
+ Custom connector

For information about configuring data source connectors, see [Connect a data source](kb-managed-connect-ds.md).