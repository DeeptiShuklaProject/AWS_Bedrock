

# Create a knowledge base for multimodal content
<a name="kb-multimodal-create"></a>

You can create multimodal knowledge bases using either the console or API. Choose your approach based on your multimodal processing needs.

**Important**  
Multimodal support is only available when creating a knowledge base with unstructured data sources. Structured data sources do not support multimodal content processing.

------
#### [ Console ]

**To create a multimodal knowledge base from the console**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, choose **Create**, and then choose **Knowledge Base with vector store**.

1. (Optional) Under **Knowledge Base details**, change the default name and provide a description for your knowledge base.

1. Under **IAM permissions**, choose an IAM role that provides Amazon Bedrock permissions to access other required AWS services. You can either have Amazon Bedrock create the service role for you, or you can choose to use your own custom role. For multimodal permissions, see [Permissions for multimodal content](kb-permissions.md#kb-permissions-multimodal).

1. Choose **Amazon S3** as your data source and choose **Next** to configure your data source.
**Note**  
You can add up to 5 Amazon S3 data sources during knowledge base creation. Additional data sources can be added after the knowledge base is created.

1. Provide the **S3 URI** of the bucket containing your multimodal content and configure an inclusion prefix if needed. The inclusion prefix is a folder path that can be used to limit what content gets ingested.

1. Under **Chunking and parsing configurations**, choose your parsing strategy:
   + **Bedrock default parser:** Recommended for text-only content processing. This parser processes common text formats while ignoring multimodal files. Supports text documents including Word, Excel, HTML, Markdown, TXT, and CSV files.
   + **Bedrock Data Automation (BDA):** Converts multimodal content to searchable text representations. Processes PDFs, images, audio, and video files to extract text, generate descriptions for visual content, and create transcriptions for audio and video content.
   + **Foundation model parser:** Provides advanced parsing capabilities for complex document structures. Processes PDFs, images, structured documents, tables, and visually rich content to extract text and generate descriptions for visual elements.

1. Choose **Next** and select your embedding model and multimodal processing approach. 
   + **Amazon Nova Multimodal Embeddings V1.0:** Choose **Amazon Nova embedding V1.0** for direct visual and audio similarity searches. Configure audio and video chunk duration (1-30 seconds, default 5 seconds) to control how content is segmented.
**Note**  
Audio and video chunking parameters are configured at the embedding model level, not at the data source level. A validation exception occurs if you provide this configuration for non-multimodal embedding models. Configure audio and video chunk duration (default: 5 seconds, range: 1-30 seconds) to control how content is segmented. Shorter chunks enable precise content retrieval while longer chunks preserve more semantic context.
**Important**  
Amazon Nova embedding v1.0 has limited support for searching speech content in audio/video data. If you need to support speech, use Bedrock Data Automation as a parser.
   + **Text embeddings with BDA:** Choose a text embedding model (such as Titan Text Embeddings v2) when using BDA processing. Text embedding models limit retrieval to text-only content, but you can enable multimodal retrieval by selecting either Amazon Bedrock Data Automation or Foundation Model as parsers.
**Note**  
If you use BDA parser with Nova Multimodal Embeddings, Amazon Bedrock Knowledge Bases will go with BDA parsing first. In this case, the embedding model will not generate native multimodal embeddings for images, audio, and video as BDA converts these to text representations.

1. If using Nova Multimodal Embeddings, configure the **Multimodal storage destination** by specifying an Amazon S3 bucket where processed files will be stored for retrieval. Knowledge Bases will store images parsed into a single Amazon S3 bucket with a folder created .bda for easy access.
**Lifecycle policy recommendation**  
When using Nova Multimodal Embeddings, Amazon Bedrock stores transient data in your multimodal storage destination and attempts to delete it after processing is completed. We recommend applying a lifecycle policy on the transient data path to ensure proper cleanup. For detailed instructions, see [Managing transient data with Amazon S3 lifecycle policies](kb-multimodal-troubleshooting.md#kb-multimodal-lifecycle-policy).

1. In the **Vector database** section, choose your vector store method and configure the appropriate dimensions based on your selected embedding model.

1. Choose **Next** and review the details of your knowledge base configuration, then choose **Create knowledge base**.

------
#### [ CLI ]

**To create a multimodal knowledge base using the AWS CLI**
+ Create a knowledge base with Nova Multimodal Embeddings. Send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request:

  ```
  aws bedrock-agent create-knowledge-base \
  --cli-input-json file://kb-nova-mme.json
  ```

  Contents of `kb-nova-mme.json` (replace the placeholder values with your specific configuration):

  ```
  {
      "knowledgeBaseConfiguration": {
          "vectorKnowledgeBaseConfiguration": {
              "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-2-multimodal-embeddings-v1:0",
              "supplementalDataStorageConfiguration": {
                  "storageLocations": [
                      {
                          "type": "S3",
                          "s3Location": {
                              "uri": "s3://<multimodal-storage-bucket>/"
                          }
                      }
                  ]
              }
          },
          "type": "VECTOR"
      },
      "storageConfiguration": {
          "opensearchServerlessConfiguration": {
              "collectionArn": "arn:aws:aoss:us-east-1:<account-id>:collection/<collection-id>",
              "vectorIndexName": "<index-name>",
              "fieldMapping": {
                  "vectorField": "<vector-field>",
                  "textField": "<text-field>",
                  "metadataField": "<metadata-field>"
              }
          },
          "type": "OPENSEARCH_SERVERLESS"
      },
      "name": "<knowledge-base-name>",
      "description": "Multimodal knowledge base with Nova Multimodal Embeddings"
  }
  ```

  Replace the following placeholders:
  + `<multimodal-storage-bucket>` - S3 bucket for storing multimodal files
  + `<account-id>` - Your AWS account ID
  + `<collection-id>` - OpenSearch Serverless collection ID
  + `<index-name>` - Vector index name in your OpenSearch collection (configured with appropriate dimensions for your chosen embedding model)
  + `<vector-field>` - Field name for storing embeddings
  + `<text-field>` - Field name for storing text content
  + `<metadata-field>` - Field name for storing metadata

------