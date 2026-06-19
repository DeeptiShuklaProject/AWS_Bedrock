

# Connect a data source
<a name="kb-managed-connect-ds"></a>

After finishing the configurations for your knowledge base, you connect a supported data source to the knowledge base.

Amazon Bedrock managed knowledge bases support connecting to unstructured data sources. Select a topic to learn how to connect to that type of data source:

**Note**  
For managed knowledge bases, the `CreateDataSource` operation is asynchronous. The data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

To learn how to connect to a data source using the Amazon Bedrock console, select the topic that corresponds to your data source type at the bottom of this page:

To connect to a data source using the Amazon Bedrock API, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt).

**Required fields:**


****  

| Field | Description | 
| --- | --- | 
| knowledgeBaseId | The ID of the knowledge base. | 
| name | A name for the data source. | 
| dataSourceConfiguration | Specify the data source type in the type field and include the corresponding configuration. For more details about connector-specific configurations, select the topic for the connector from the topics at the bottom of this page. | 

Within `dataSourceConfiguration`, you must specify the following:
+ `type` – Must be `MANAGED_KNOWLEDGE_BASE_CONNECTOR`.
+ `managedKnowledgeBaseConnectorConfiguration` – Configuration for the connector. Contains the following fields:
  + `connectorParameters` (required) – Contains a `type` field that specifies the connector type and a required `version` field set to `1`. Supported type values are `S3`, `ONEDRIVE`, `CONFLUENCE`, `SHAREPOINT`, `WEB_CRAWLER`, and `GOOGLE_DRIVE`. The remaining fields in `connectorParameters` differ by connector type — refer to each data connector page for more details.
  + `deletionProtectionConfiguration` (optional) – A safeguard against accidental bulk deletion of indexed content. Contains `deletionProtectionStatus` (`ENABLED` or `DISABLED`) and, when enabled, an optional `deletionProtectionThreshold` (0–100, defaults to 15). The threshold is the maximum percentage of documents that a sync job can delete from your index. If a sync would delete more than this percentage, the sync skips its delete phase, leaving your indexed documents in place. Not supported for the Custom connector.
  + `mediaExtractionConfiguration` (optional) – Configuration for extracting media (images, audio, video) from data source files.

**Optional fields:**


****  

| Field | Description | 
| --- | --- | 
| description | Provide a description for the data source. | 
| vectorIngestionConfiguration | Contains configurations for customizing the ingestion process. For more information, see [Customize ingestion for a data source](kb-managed-customize-ingestion.md). | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 

The following example shows a `CreateDataSource` request with an S3 connector:

```
{
    "knowledgeBaseId": "{{your-knowledge-base-id}}",
    "name": "{{my-s3-data-source}}",
    "description": "{{S3 data source for my managed knowledge base}}",
    "dataSourceConfiguration": {
        "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
        "managedKnowledgeBaseConnectorConfiguration": {
            "mediaExtractionConfiguration": {
                "imageExtractionConfiguration": {
                    "imageExtractionStatus": "ENABLED"
                }
            },
            "deletionProtectionConfiguration": {
                "deletionProtectionStatus": "ENABLED",
                "deletionProtectionThreshold": 15
            },
            "connectorParameters": {
                "type": "S3",
                "version": "1",
                "connectionConfiguration": {
                    "bucketName": "{{my-bucket-name}}",
                    "bucketOwnerAccountId": "{{123456789012}}"
                },
                "filterConfiguration": {
                    "maxFileSizeInMegaBytes": "50"
                }
            }
        }
    }
}
```

To learn more about a specific connector and its configuration, select a topic below.

**Topics**
+ [Amazon S3](kb-managed-ds-s3.md)
+ [Confluence](kb-managed-ds-confluence.md)
+ [Custom](kb-managed-ds-custom.md)
+ [Google Drive](kb-managed-ds-googledrive.md)
+ [Microsoft OneDrive](kb-managed-ds-onedrive.md)
+ [Microsoft SharePoint](kb-managed-ds-sharepoint.md)
+ [Web Crawler](kb-managed-ds-webcrawler.md)