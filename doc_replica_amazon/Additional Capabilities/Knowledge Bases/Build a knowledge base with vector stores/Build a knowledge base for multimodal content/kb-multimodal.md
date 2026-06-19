

# Build a knowledge base for multimodal content
<a name="kb-multimodal"></a>

Amazon Bedrock Knowledge Bases supports multimodal content including images, audio, and video files. You can search using images as queries, retrieve visually similar content, and process multimedia files alongside traditional text documents. This capability enables you to extract insights from diverse data types—standalone images, audio recordings, and video files stored across your organization.

Amazon Bedrock Knowledge Bases enable you to index and retrieve information from text, visual, and audio content. Organizations can now search product catalogs using images, find specific moments in training videos, and retrieve relevant segments from customer support call recordings.

**Regional availability**  
Multimodal processing approaches have different regional availability. For detailed information, see [Regional availability](kb-multimodal-choose-approach.md#kb-multimodal-processing-regions).

## Features and capabilities
<a name="kb-multimodal-features"></a>

Multimodal knowledge bases provide the following key capabilities:

**Image-based queries**  
Submit images as search queries to find visually similar content when using Nova Multimodal Embeddings. Supports product matching, visual similarity search, and image retrieval.

**Audio content retrieval**  
Search audio files using text queries. Retrieve specific segments from recordings with timestamp references. Audio transcription enables text-based search across spoken content including meetings, calls, and podcasts.

**Video segment extraction**  
Locate specific moments within video files using text queries. Retrieve video segments with precise timestamps.

**Cross-modal search**  
Search across different data types including text documents, images, audio, and video. Retrieve relevant content regardless of original format.

**Source references with timestamps**  
Retrieval results include references to original files with temporal metadata for audio and video. Enables precise navigation to relevant segments within multimedia content.

**Flexible processing options**  
Choose between native multimodal embeddings for visual similarity or text conversion for speech-based content. Configure processing approach based on content characteristics and application requirements.

## How it works
<a name="kb-multimodal-how-it-works"></a>

Multimodal knowledge bases process and retrieve content through a multi-stage pipeline that handles different data types appropriately:

****Ingestion and processing****

1. **Data source connection:** Connect your knowledge base to Amazon S3 buckets or custom data sources containing text documents, images, audio files, and video files.

1. **File type detection:** The system identifies each file type by its extension and routes it to the appropriate processing pipeline.

1. **Content processing:** Depending on your configuration, files are processed using one of two approaches:
   + **Nova Multimodal Embeddings:** Preserves native format for visual and audio similarity matching. Images, audio, and video are embedded directly without conversion to text.
   + **Bedrock Data Automation (BDA):** Converts multimedia to text representations. Audio is transcribed using Automatic Speech Recognition (ASR), video is processed to extract scene summaries and transcripts, and images undergo OCR and visual content extraction.

1. **Embedding generation:** Processed content is converted to vector embeddings using your selected embedding model. These embeddings capture semantic meaning and enable similarity-based retrieval.

1. **Vector storage:** Embeddings are stored in your configured vector database along with metadata including file references, timestamps (for audio and video), and content type information.

1. **Multimodal storage (optional):** If configured, original multimedia files are copied to a dedicated multimodal storage destination for reliable retrieval, ensuring availability even if source files are modified or deleted.

****Query and retrieval****

1. **Query processing:** User queries (text or image) are converted to embeddings using the same embedding model used during ingestion.

1. **Similarity search:** The query embedding is compared against stored embeddings in the vector database to identify the most relevant content.

1. **Result retrieval:** The system returns matching content with metadata including:
   + Source URI (original file location)
   + Timestamp metadata (for audio and video segments)
   + Content type and modality information

1. **Response generation (optional):** For `RetrieveAndGenerate` requests, retrieved content is passed to a foundation model to generate contextually relevant text responses. This is supported when using BDA processing or when the knowledge base contains text content.

**Important**  
The system returns references to complete files with timestamp metadata for audio and video content. Your application must extract and play specific segments based on the provided start and end timestamps. The AWS Management Console handles this automatically.

**Topics**
+ [Features and capabilities](#kb-multimodal-features)
+ [How it works](#kb-multimodal-how-it-works)
+ [Choosing your multimodal processing approach](kb-multimodal-choose-approach.md)
+ [Prerequisites for multimodal knowledge bases](kb-multimodal-prerequisites.md)
+ [Create a knowledge base for multimodal content](kb-multimodal-create.md)
+ [Adding data sources and starting ingestion](kb-multimodal-add-data-source-and-ingest.md)
+ [Testing and querying multimodal knowledge bases](kb-multimodal-test-and-query.md)
+ [Troubleshooting multimodal knowledge bases](kb-multimodal-troubleshooting.md)