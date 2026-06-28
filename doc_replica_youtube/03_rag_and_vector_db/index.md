# Building RAG & Vector Search on AWS Bedrock

A practical project tutorial focusing on ingesting document corpus sources and querying them.

- **Video URL**: [Building RAG on AWS Bedrock (YouTube)](https://www.youtube.com/watch?v=y1slHK9R_Vg) *(Note: Placeholder link. Replace with actual video link once available)*
- **Duration**: ~1 Hour
- **Key Focus**: Ingestion pipelines, Cohere/Titan embedding models, OpenSearch/Pinecone integrations.

---

## Detailed Transcript Bookmarks & Outline

| Timestamp | Topic | Concepts Covered |
|-----------|-------|------------------|
| **0:00** | RAG Architecture | Retrieval-Augmented Generation vs fine-tuning. |
| **0:12** | Vector Embeddings | Choosing Titan Text Embeddings or Cohere Embed models. |
| **0:25** | Ingestion Scripts | Chunking documents recursively and generating vectors. |
| **0:40** | Vector Similarity | Querying vector databases using cosine similarity. |
| **0:52** | Final Generation | Prepending retrieval results to system prompts to answer questions. |

---

## Key Takeaways
1. **Chunking Size**: Adjust chunk sizes (e.g., 512 tokens with 10% overlap) depending on file complexity.
2. **Hybrid Search**: Combining keyword search with vector semantic search delivers the highest retrieval accuracy.
3. **Data Privacy**: Keep vector databases inside VPC limits if documents contain sensitive enterprise data.

---

## Interactive Transcript Timeline

```widget:transcript-timeline
{
  "transcriptPath": "03_rag_and_vector_db/transcript.json"
}
```
