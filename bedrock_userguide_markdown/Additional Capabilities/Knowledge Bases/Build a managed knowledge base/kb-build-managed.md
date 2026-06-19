

# Build a managed knowledge base
<a name="kb-build-managed"></a>

**Note**  
For optimized combination of ease-of-use, accuracy and cost, we recommend that you choose Bedrock Managed Knowledge Base.

With a Bedrock Managed Knowledge Base, Amazon Bedrock manages the ingestion, storage, indexing, and retrieval infrastructure for you. You provide your data sources and Amazon Bedrock manages the data ingestion pipeline, datastore setup, and retrieval optimization — including embedding and reranking with service-managed models by default. You can optionally provide your own Bedrock embedding model at creation time or your own reranking model at query time. This simplifies the setup process compared to a Customer-managed Knowledge Base, where you must configure and manage some of the underlying infrastructure.

## Bedrock Managed vs Customer-managed Knowledge Bases
<a name="kb-managed-vs-custom"></a>

The following table summarizes the key differences between Bedrock Managed and Customer-managed Knowledge Bases:


****  

| Feature | Bedrock Managed | Customer-Managed | 
| --- | --- | --- | 
| Agentic retrieval | Supported | Not supported | 
| Data store | Auto-scaling datastore of embeddings, text, metadata and raw files. Managed completely by Bedrock. | Customers choose, provision, scale, and update vector and text datastores | 
| Search type | Agentic and semantic hybrid retrieval optimized for ingested across file types | Choose your own search strategy | 
| Managed Embedding model | Comes with built-in managed model optimized for accuracy and performance at no extra cost | None | 
| Custom Embedding model | Choose any Bedrock embedding model with float32 and 1024 dimensions | Chose any Bedrock embedding model | 
| Managed Reranking | Comes with built-in managed semantic reranker optimized for accuracy and performance at no extra cost | None | 
| Customized Reranking | Choose your reranker models from Bedrock | Choose your reranker models from Bedrock | 
| Connectors | 7 native connectors (S3, SharePoint, Confluence, Web Crawler, Google Drive, OneDrive, Custom) | S3 and Custom | 
| Data parsing | Built-in parser for multi-modal file types | Choose among Default for text, Foundation Model, and Bedrock Data Automation | 
| Chunking | Choose among built-in (default), fixed-size, and hierarchical | Choose among built-in (default), fixed-size, and hierarchical | 
| AgentCore Gateway integration | Supported | Not supported | 
| Infrastructure management | None required | You provision and maintain your vector DB, with direct access to it | 
| Best for | End-to-end managed RAG with native connectors and agentic retrieval | Custom vector DB configurations | 
| Amazon Quick integration | Natively associate as knowledge base within Quick | Customers build their own Integration | 

**Topics**
+ [Bedrock Managed vs Customer-managed Knowledge Bases](#kb-managed-vs-custom)
+ [Prerequisites](kb-managed-prereqs.md)
+ [Create a managed knowledge base](kb-managed-create.md)
+ [Observability for managed knowledge bases](kb-managed-observability.md)
+ [Sync a data source](kb-managed-sync.md)
+ [View data source information for your Amazon Bedrock knowledge base](kb-managed-ds-info.md)
+ [Access Control Lists awareness enablement](kb-managed-acl.md)
+ [Resource policies for managed knowledge bases](kb-managed-cross-account.md)
+ [Amazon Quick integration with managed knowledge bases](kb-managed-byo-fmkb.md)
+ [Connect to your knowledge base through AgentCore Gateway](kb-gateway-target.md)
+ [Supported AWS Regions](kb-managed-regions.md)
+ [Service quotas for managed knowledge bases](kb-managed-quotas.md)