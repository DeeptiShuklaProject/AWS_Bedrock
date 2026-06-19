

# Connect a Confluence data source
<a name="kb-managed-ds-confluence-connect"></a>

After you set up authentication and store your credentials in an AWS Secrets Manager secret, create the Confluence data source in your knowledge base. This page describes how to create the data source with the AWS Management Console or the API, followed by a reference for the connector parameters you can configure.

**Note**  
Complete authentication setup first. See [Set up Basic authentication for Confluence](kb-managed-confluence-basic-setup.md) or [Set up OAuth 2.0 authentication for Confluence](kb-managed-confluence-oauth2-setup.md). You need the secret ARN and the Confluence host URL.

## Create the data source
<a name="kb-managed-ds-confluence-create"></a>

------
#### [ Console ]

**To connect Confluence to your managed knowledge base**

1. Under **Data source**, provide a name for your data source.

1. Select **Confluence** from the data source dropdown.

1. Under **Source**, enter your Confluence URL (for example, `https://example.atlassian.net`).

1. Under **Authentication**, select **Basic authentication** or **OAuth 2.0 authentication**.

1. Select or create an AWS Secrets Manager secret to store your credentials.

1. (Optional, Basic auth only) To enable document-level access control, select **Control document access with ACLs**. The secret you select must include `adminApiKey`, `organizationId`, and `directoryId`. This option cannot be changed after creation. For details, see [Document-level access controls](kb-managed-ds-confluence-acl.md).

1. (Optional) Expand **Sync scope** to choose which entity types to crawl (pages, blogs, page attachments, blog attachments, archived spaces, archived pages, personal spaces).

1. (Optional) Expand **Entity URLs** to use URL-based filtering to sync specific Confluence spaces, pages, and blogs.

1. (Optional) Expand **Mime types regex pattern** to include or exclude specific MIME types.

------
#### [ API ]

To create a Confluence data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. The following AWS Command Line Interface example creates a data source that uses Basic authentication. To use OAuth 2.0 instead, change `authType` to `OAUTH2`. To enable document-level access control, set `aclEnabled` to `true`. For a description of each field, see the connector parameters reference that follows.

```
aws bedrock-agent create-data-source \
 --name "{{Confluence-connector}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://confluence-managed-connector.json
```

The `confluence-managed-connector.json` file contains the following:

```
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "connectorParameters": {
            "type": "CONFLUENCE",
            "version": "1",
            "aclEnabled": false,
            "connectionConfiguration": {
                "secretArn": "{{arn:aws:secretsmanager:us-west-2:123456789012:secret:bedrock-confluence-basic-creds}}",
                "type": "SAAS",
                "authType": "BASIC",
                "hostUrl": "{{https://example.atlassian.net}}"
            },
            "dataEntityConfiguration": {
                "crawlPage": true,
                "crawlBlog": true,
                "crawlPageAttachment": true,
                "crawlBlogAttachment": true
            },
            "filterConfiguration": {
                "inclusionSpaceKeys": ["{{ENG}}", "{{DOCS}}"]
            }
        }
    }
}
```

For managed knowledge bases, `CreateDataSource` is asynchronous: the data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

------

## Connector parameters
<a name="kb-managed-config-confluence"></a>

The data source configuration uses the following connector parameters. To connect to Confluence, specify `CONFLUENCE` as the connector type in `connectorParameters`. For the fields that wrap `connectorParameters` (such as `deletionProtectionConfiguration` and `mediaExtractionConfiguration`), see [Connect a data source](kb-managed-connect-ds.md).

**Set `aclEnabled` explicitly**  
If you omit `aclEnabled`, the default depends on `authType`: `BASIC` defaults to `true`, and `OAUTH2` defaults to `false`. Because ACL configuration is permanent after the data source is created, set `aclEnabled` explicitly so the data source has the access-control behavior you intend. For details, see [Document-level access controls](kb-managed-ds-confluence-acl.md).


**connectionConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| secretArn | Yes | The ARN of the AWS Secrets Manager secret containing your Confluence credentials. | 
| type | Yes | The Confluence deployment type. Set to SAAS. Confluence Server and Data Center are not supported. | 
| authType | Yes | The authentication type. Set to BASIC or OAUTH2. See [Authentication methods](kb-managed-ds-confluence.md#kb-managed-confluence-auth-methods). | 
| hostUrl | Yes | The base URL of your Confluence Cloud instance (for example, https://example.atlassian.net). | 


**dataEntityConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| crawlPage | No | Whether to crawl pages. | 
| crawlBlog | No | Whether to crawl blog posts. | 
| crawlPageAttachment | No | Whether to crawl page attachments. Crawled only when crawlPage is also true. | 
| crawlBlogAttachment | No | Whether to crawl blog post attachments. Crawled only when crawlBlog is also true. | 
| crawlArchivedSpace | No | Whether to crawl archived spaces. | 
| crawlArchivedPage | No | Whether to crawl archived pages. | 
| crawlPersonalSpace | No | Whether to crawl personal spaces. | 


**filterConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| inclusionSpaceKeys | No | Space keys to include. | 
| inclusionSpaceUrls | No | Space URLs to include. | 
| inclusionMimeTypes | No | MIME types to include. | 
| exclusionMimeTypes | No | MIME types to exclude. | 
| maxFileSizeInMegaBytes | No | Maximum size, in megabytes, of any single file the connector ingests. Provide as a numeric string (for example, "500"). Defaults to "500". | 


**aclEnabled (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| aclEnabled | No | Whether document-level access control is enabled. Set to true to enable, or false to disable. If you omit this field, the default depends on authType: BASIC defaults to true; OAUTH2 defaults to false. ACL on BASIC requires a secret that includes Atlassian organization admin credentials. You cannot change this setting after you create the data source. For details, see [Document-level access controls](kb-managed-ds-confluence-acl.md). | 

## Change the authentication method
<a name="kb-managed-ds-confluence-change-auth"></a>

You can change a data source's authentication method (for example, from OAuth 2.0 to Basic) by updating the data source with the new `authType` and a secret that contains the matching credentials, using the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console. The document-level access control setting is fixed when you create a data source, so to add or remove ACLs you must create a new data source.

## Next steps
<a name="kb-managed-ds-confluence-connect-next"></a>

After you create the data source, sync it to ingest content into your knowledge base. For details, see [Sync a data source](kb-managed-sync.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-confluence-acl.md).