

# Custom
<a name="kb-managed-ds-custom"></a>

Instead of choosing a supported data source service, you can connect to a custom data source for the following advantages:
+ Flexibility and control over the data types that you want your knowledge base to have access to.
+ The ability to use the `KnowledgeBaseDocuments` API operations to directly ingest or delete documents without the need to sync changes.
+ The ability to view documents in your data source directly through the Amazon Bedrock console or API.
+ The ability to upload documents into the data source directly in the AWS Management Console or to add them inline.

To connect a knowledge base to a custom data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. Specify the `knowledgeBaseId` of the knowledge base to connect to, give a `name` to the data source, and set the `type` field in the `dataSourceConfiguration` to `MANAGED_KNOWLEDGE_BASE_CONNECTOR`. Define the connector itself in `managedKnowledgeBaseConnectorConfiguration.connectorParameters`, setting its `type` to `CUSTOM`. The following shows a minimal example to create this data source:

```
PUT /knowledgebases/{{KB12345678}}/datasources/ HTTP/1.1
Content-type: application/json

{
    "name": "MyCustomDataSource",
    "dataSourceConfiguration": {
        "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
        "managedKnowledgeBaseConnectorConfiguration": {
            "connectorParameters": {
                "type": "CUSTOM",
                "version": "1",
                "aclEnabled": false
            }
        }
    }
}
```

Set `aclEnabled` to `true` in `connectorParameters` to enable document-level access control. For details, see [Document-level access controls](kb-managed-ds-custom-acl.md).

After setting up your custom data source, you can add documents into it and directly ingest them into the knowledge base. Unlike other data sources, you don't need to sync a custom data source. To learn how to ingest documents directly, see [Ingest changes directly into a knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-direct-ingestion.html).