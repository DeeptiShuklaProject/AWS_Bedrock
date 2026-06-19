

# Testing and querying multimodal knowledge bases
<a name="kb-multimodal-test-and-query"></a>

After ingesting your multimodal content, you can test and query your knowledge base using the console or API. The available query types depend on your chosen processing approach.

------
#### [ Console ]

**To test your knowledge base from the console**

1. From your knowledge base details page, scroll to the **Test knowledge base** section.

1. Choose your query type:
   + **Standard retrieval only:** Query and retrieve information from data sources in a single Knowledge Base.
   + **Retrieval and response generation:** Query a single Knowledge Base and generate responses based on the retrieved results by using a foundation model.
**Note**  
If you have multimodal content, you must use the BDA parser for retrieval and response generation.

1. Configure additional options as needed:
   + **Source chunks:** Specify the maximum number of source chunks to return
   + **Search Type:** Select search type to customize querying strategy
   + **Metadata filters:** Apply filters to narrow search results
   + **Guardrails:** Select an existing guardrail or create a new one

1. Enter a text query or upload an image (Nova Multimodal Embeddings only) to search your multimodal content. Use the attachment button to upload images for visual similarity search.

1. Review the results, which include:
   + Retrieved content chunks with relevance scores
   + Source file references and timestamps (for audio/video)
   + Metadata including file types and processing information
   + For multimedia content, playback controls with automatic segment positioning based on retrieved timestamps

------
#### [ API ]

The following examples show how to use the Amazon Bedrock Agent Runtime API to query your multimodal knowledge base programmatically:

**Text query example**  
Search using text input:

```
aws bedrock-agent-runtime retrieve \
--knowledge-base-id <knowledge-base-id> \
--retrieval-query text="robot automation in manufacturing"
```

**Image query example (Nova Multimodal Embeddings only)**  
Search using an uploaded image:

```
{
    "knowledgeBaseId": "<knowledge-base-id>",
    "retrievalQuery": {
        "imageQuery": {
            "inlineContent": {
                "mimeType": "image/jpeg",
                "data": "<base64-encoded-image>"
            }
        }
    }
}
```

------

## Supported query types
<a name="kb-multimodal-query-types"></a>

**Text queries**  
Supported with both Nova Multimodal Embeddings and BDA approaches. Search using natural language text to find relevant content across all media types.

**Image queries**  
Only supported with Nova Multimodal Embeddings. Upload images to find visually similar content in your knowledge base.

## Understanding response metadata
<a name="kb-multimodal-response-metadata"></a>

Multimodal query responses include additional metadata for multimedia content:

**Source attribution**  
Original file location (sourceUri) and multimodal storage location (supplementalUri) for reliable access

**Temporal metadata**  
Start and end timestamps for audio and video segments, enabling precise navigation to relevant content

**Content type information**  
File format, processing method, and modality indicators to help applications handle different content types appropriately

**Vector database metadata structure**  
When multimodal content is processed and stored, the following metadata structure is used in the vector database:
+ **text field:** For multimedia files processed with Nova Multimodal Embeddings, this field contains an empty string since the content is embedded as native multimedia rather than text
+ **metadata field:** Contains structured information including source details and related content references:

  ```
  {
    "source": {
      "sourceType": "S3",
      "s3Location": {
        "uri": "s3://source-bucket/path/to/file.mp4"
      }
    },
    "relatedContent": [{
      "type": "S3",
      "s3Location": {
        "uri": "s3://multimodal-storage-bucket/processed/file.mp4"
      }
    }]
  }
  ```
+ **Auto-created fields:** Additional fields for filtering and identification:
  + `x-amz-bedrock-kb-source-uri`: Original source URI for filtering operations
  + `x-amz-bedrock-kb-data-source-id`: Data source identifier for tracking content origin
  + `x-amz-bedrock-kb-chunk-start-time-in-millis`: Start timestamp in milliseconds for audio and video segments
  + `x-amz-bedrock-kb-chunk-end-time-in-millis`: End timestamp in milliseconds for audio and video segments
  + `x-amz-bedrock-kb-source-file-mime-type`: MIME type of the source file
  + `x-amz-bedrock-kb-source-file-modality`: Modality of the source file (TEXT, IMAGE, AUDIO, VIDEO)

**Important**  
Applications must use the provided timestamps to extract and play specific segments from audio and video files. The knowledge base returns references to complete files, not pre-segmented clips.