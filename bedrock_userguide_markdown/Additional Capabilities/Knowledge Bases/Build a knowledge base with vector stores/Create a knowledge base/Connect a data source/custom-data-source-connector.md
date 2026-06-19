

# Connect your knowledge base to a custom data source
<a name="custom-data-source-connector"></a>

Instead of choosing a supported data source service, you can connect to a custom data source for the following advantages:
+ Flexibility and control over the data types that you want your knowledge base to have access to.
+ The ability to use the `KnowledgeBaseDocuments` API operations to directly ingest or delete documents without the need to sync changes.
+ The ability to view documents in your data source directly through the Amazon Bedrock console or API.
+ The ability to upload documents into the data source directly in the AWS Management Console or to add them inline.
+ The ability to add metadata directly to each document for when adding or updating a document in the data source. For more information on how to use metadata for filtering when retrieving information from a data source, see the **Metadata and filtering** tab in [Configure and customize queries and response generation](kb-test-config.md).

**Multimodal content support**  
Custom data sources support multimodal content including images, audio, and video files up to 10MB base64 encoded. For comprehensive guidance on working with multimodal content, see [Build a knowledge base for multimodal content](kb-multimodal.md).

To connect a knowledge base to a custom data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Specify the `knowledgeBaseId` of the knowledge base to connect to, give a `name` to the data source, and specify the `type` field in the `dataSourceConfiguration` as `CUSTOM`. The following shows a minimal example to create this data source:

```
PUT /knowledgebases/{{KB12345678}}/datasources/ HTTP/1.1
Content-type: application/json

{
    "name": "MyCustomDataSource",
    "dataSourceConfiguration": {
        "type": "CUSTOM"
    }
}
```

You can include any of the following optional fields to configure the data source:


****  

| Field | Use case | 
| --- | --- | 
| description | To provide a description for the data source. | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 
| serverSideEncryptionConfiguration | To specify a custom KMS key for transient data storage while converting your data into embeddings. For more information, see [Encryption of transient data storage during data ingestion](encryption-kb.md#encryption-kb-ingestion) | 
| dataDeletionPolicy | To configure what to do with the vector embeddings for your data source in your vector store, if you delete the data source. Specify RETAIN to retain the data in the vector store or the default option of DELETE to delete them. | 
| vectorIngestionConfiguration | To configure options for ingestion of the data source. See below for more information. | 

The `vectorIngestionConfiguration` field maps to a [VectorIngestionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorIngestionConfiguration.html) object containing the following fields:
+ chunkingConfiguration – To configure the strategy to use for chunking the documents in the data source. For more information about chunking strategies, see [How content chunking works for knowledge bases](kb-chunking.md).
+ parsingConfiguration – To configure the strategy to use for parsing the data source. For more information about parsing options, see [Parsing options for your data source](kb-advanced-parsing.md).
+ customTransformationConfiguration – To customize how the data is transformed and to apply a Lambda function for greater customization. For more information about how to customize chunking of your data and processing of your metadata with a Lambda function, see [Use a custom transformation Lambda function to define how your data is ingested](kb-custom-transformation.md).

After setting up your custom data source, you can add documents into it and directly ingest them into the knowledge base. Unlike other data sources, you don't need to sync a custom data source. To learn how to ingest documents directly, see [Ingest changes directly into a knowledge base](kb-direct-ingestion.md).