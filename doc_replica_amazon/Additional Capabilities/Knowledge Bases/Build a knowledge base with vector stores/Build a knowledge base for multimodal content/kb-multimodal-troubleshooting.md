

# Troubleshooting multimodal knowledge bases
<a name="kb-multimodal-troubleshooting"></a>

This section provides guidance for resolving common issues encountered when working with multimodal knowledge bases. The troubleshooting information is organized by general limitations, common error scenarios with their causes and solutions, and performance optimization recommendations. Use this information to diagnose and resolve issues during setup, ingestion, or querying of your multimodal content.

## General limitations
<a name="kb-multimodal-general-limitations"></a>

Be aware of these current limitations when working with multimodal knowledge bases:
+ **File size limits:** Maximum 1.5 GB per video file, 1 GB per audio file (Nova Multimodal Embeddings), or 1.5 GB per file (BDA)
+ **Files per ingestion job:** Maximum 15,000 files per job (Nova Multimodal Embeddings) or 1,000 files per job (BDA)
+ **Query limits:** Maximum of one image per query
+ **Data source restrictions:** Only Amazon S3 and custom data sources support multimodal content
+ **BDA chunking limitations:** When using Bedrock Data Automation with fixed size chunking, overlap percentage settings are not applied to audio and video content
+ **BDA concurrent job limits:** Default limit of 20 concurrent BDA jobs. For large-scale processing, consider requesting a service quota increase
+ **Reranker model limitations:** Reranker models are not supported for multimodal content
+ **Summarization limitations:** Summarization of retrieval responses containing non-text content is not supported
+ **Query input limitations:** Input containing both text and image is not currently supported. You can use either text or image queries, but not both simultaneously.
+ **Guardrail image content filters:** When using image queries with a guardrail that has image content filters configured, the input image will be evaluated against the guardrail and may be blocked if it violates the configured filter thresholds
+ **Input and type mismatch:** By default, the input is assumed to be text when the type is not specified. When using modalities other than text, you must specify the correct type

## Common errors and solutions
<a name="kb-multimodal-common-errors"></a>

If you encounter issues with your multimodal knowledge base, review these common scenarios:

**4xx error when using image queries**  
**Cause:** Attempting to use image queries with text-only embedding models or BDA-processed knowledge bases.  
**Solution:** Choose Amazon Nova Multimodal Embeddings when creating your knowledge base for image query support.

**RAG returns 4xx error with multimodal content**  
**Cause:** Using `RetrieveAndGenerate` with knowledge base containing only multimodal content and Amazon Nova Multimodal Embeddings model.  
**Solution:** Use BDA parser for RAG functionality, or ensure that your knowledge base contains text content.

**Multimodal storage destination required error**  
**Cause:** Using Nova Multimodal Embeddings without configuring a multimodal storage destination.  
**Solution:** Specify a multimodal storage destination when using Nova Multimodal Embeddings.

**Data source and multimodal storage use same S3 bucket**  
**Cause:** Configuring your data source and multimodal storage destination to use the same Amazon S3 bucket without proper inclusion prefixes.  
**Solution:** Either use separate buckets for data source and multimodal storage, or configure inclusion prefixes to prevent re-ingesting extracted media files.

**Inclusion prefix cannot start with "aws/"**  
**Cause:** Using an inclusion prefix that starts with "aws/" when your data source and multimodal storage destination share the same Amazon S3 bucket.  
**Solution:** Specify a different inclusion prefix. The "aws/" path is reserved for extracted media storage and cannot be used as an inclusion prefix to avoid re-ingesting processed content.

**BDA ingestion skips multimodal content**  
**Cause:** Knowledge base was created without a multimodal storage destination, then BDA data source was added with multimodal content.  
**Solution:** Re-create the knowledge base with a multimodal storage destination configured to enable BDA processing of audio, video, and image files.

**Knowledge base created without multimodal embedding model**  
**Cause:** Knowledge base was created with a text-only embedding model, limiting multimodal capabilities.  
**Solution:** Create a new knowledge base with Nova Multimodal Embeddings to enable native multimodal processing and image-based queries.

## Managing transient data with Amazon S3 lifecycle policies
<a name="kb-multimodal-lifecycle-policy"></a>

When using Nova Multimodal Embeddings, Amazon Bedrock stores transient data in your multimodal storage destination and attempts to delete it after processing is completed. We recommend applying a lifecycle policy on the transient data path to ensure that it is properly expired.

------
#### [ Console ]

**To create a lifecycle rule using the console**

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3).

1. Navigate to the multimodal storage destination you've configured for your Knowledge Base.

1. Choose the **Management** tab and select **Create lifecycle rule**.

1. For **Lifecycle rule name**, enter **Transient Data Deletion**.

1. Under **Filter type**, choose **Limit the scope of this rule using one or more filters**.

1. For **Prefix**, enter the transient data path for your knowledge base and data source.

   Replace the placeholder values in the following prefix with your actual identifiers:

   ```
   aws/bedrock/knowledge_bases/{{knowledge-base-id}}/{{data-source-id}}/transient_data
   ```
**Important**  
Do not apply lifecycle policies to the entire bucket or to the "aws/" prefix, as this will delete your multimodal content and cause retrieval failures. Only use the specific transient data path shown above.

1. Under **Lifecycle rule actions**, select **Expire current versions of objects**.

1. For **Days after object creation**, enter **1**.

1. Choose **Create rule**.

------
#### [ AWS CLI ]

**To create a lifecycle rule using the AWS CLI**

1. Create a JSON file named `lifecycle-policy.json` with the following content.

   Replace the placeholder values with your actual identifiers:
   + {{knowledge-base-id}} - Your knowledge base identifier
   + {{data-source-id}} - Your data source identifier

   ```
   {
       "Rules": [
           {
               "ID": "TransientDataDeletion",
               "Status": "Enabled",
               "Filter": {
                   "Prefix": "aws/bedrock/knowledge_bases/{{knowledge-base-id}}/{{data-source-id}}/transient_data"
               },
               "Expiration": {
                   "Days": 1
               }
           }
       ]
   }
   ```

1. Apply the lifecycle policy to your bucket. Replace {{your-multimodal-storage-bucket}} with your actual bucket name:

   ```
   aws s3api put-bucket-lifecycle-configuration \
       --bucket {{your-multimodal-storage-bucket}} \
       --lifecycle-configuration file://lifecycle-policy.json
   ```

1. Verify the lifecycle policy was applied:

   ```
   aws s3api get-bucket-lifecycle-configuration \
       --bucket {{your-multimodal-storage-bucket}}
   ```

------

For more information about Amazon S3 lifecycle policies, see [Managing the lifecycle of objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) in the *Amazon S3 User Guide*.

## Performance considerations
<a name="kb-multimodal-performance-considerations"></a>

For optimal performance with your multimodal knowledge base, consider these factors:
+ **Processing time:** BDA processing takes longer due to content conversion
+ **Query latency:** Image queries may have higher latency than text queries
+ **Chunking duration:** Longer audio/video chunk durations increase processing time but may improve accuracy