

# Connect a data source to your knowledge base
<a name="data-source-connectors"></a>

After finishing the configurations for your knowledge base, you connect a supported data source to the knowledge base.

Amazon Bedrock Knowledge Bases supports connecting to unstructured data sources or to structured data stores through a query engine. Select a topic to learn how to connect to that type of data source:

**Multimodal content support**  
Multimodal content (images, audio, and video files) is only supported with Amazon S3 and custom data sources. Other data source types will skip multimodal files during ingestion. For comprehensive guidance on working with multimodal content, see [Build a knowledge base for multimodal content](kb-multimodal.md).

To learn how to connect to a data source using the Amazon Bedrock console, select the topic that corresponds to your data source type at the bottom of this page:

To connect to a data source using the Amazon Bedrock API, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt).

The following fields are required:


****  

| Field | Basic description | 
| --- | --- | 
| knowledgeBaseId | The ID of the knowledge base. | 
| name | A name for the knowledge base. | 
| dataSourceConfiguration | Specify the data source service or type in the type field and include the corresponding field. For more details about service-specific configurations, select the topic for the service from the topics at the bottom of this page. | 

The following fields are optional:


****  

| Field | Use case | 
| --- | --- | 
| description | To provide a description for the data source. | 
| vectorIngestionConfiguration | Contains configurations for customizing the ingestion process. For more information, see [Customize ingestion for a data source](kb-data-source-customize-ingestion.md). | 
| dataDeletionPolicy | To specify whether to RETAIN the vector embeddings in the vector store or to DELETE them. | 
| serverSideEncryptionConfiguration | To encrypt transient data during data syncing with a customer managed key, specify its ARN in the kmsKeyArn field. | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 

Select a topic to learn more about a service and configuring it.

**Topics**
+ [Connect to Amazon S3 for your knowledge base](s3-data-source-connector.md)
+ [Connect to Confluence for your knowledge base](confluence-data-source-connector.md)
+ [Connect to Microsoft SharePoint for your knowledge base](sharepoint-data-source-connector.md)
+ [Connect to Salesforce for your knowledge base](salesforce-data-source-connector.md)
+ [Crawl web pages for your knowledge base](webcrawl-data-source-connector.md)
+ [Connect your knowledge base to a custom data source](custom-data-source-connector.md)