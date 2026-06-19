

# Connect a SharePoint data source
<a name="kb-managed-ds-sharepoint-connect"></a>

After you set up authentication and store your credentials in an AWS Secrets Manager secret, create the SharePoint data source in your knowledge base. This page describes how to create the data source with the AWS Management Console or the API, followed by a reference for the connector parameters you can configure.

**Note**  
Complete authentication setup first. See [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md) (recommended) or [Set up OAuth 2.0 authentication for SharePoint](kb-managed-sharepoint-oauth2-setup.md). You need the secret ARN, your tenant ID, and (for Microsoft Entra ID App-Only authentication) the Amazon S3 location of your certificate.

## Create the data source
<a name="kb-managed-ds-sharepoint-create"></a>

------
#### [ Console ]

**To connect SharePoint to your managed knowledge base**

1. Under **Data source**, provide a name for your data source.

1. Select **SharePoint** from the data source dropdown.

1. Under **Source**, enter your **Site URLs**. Each URL must start with `https://` and point to a site, team site, or personal site (for example, `https://contoso.sharepoint.com/sites/engineering`). You can add up to 100 URLs.

1. Under **Authentication**, select **Microsoft Entra ID App-Only** or **OAuth 2.0 authentication**.

1. Select or create an AWS Secrets Manager secret to store your credentials.

1. Enter your **Tenant ID**.

1. If you selected Microsoft Entra ID App-Only authentication, provide the **Certificate path** — the Amazon S3 path to your `.p12` certificate file.

1. (Optional) To enable document-level access control, select **Control document access with ACLs**. This option is available only with Microsoft Entra ID App-Only authentication and cannot be changed after creation. For details, see [Document-level access controls](kb-managed-ds-sharepoint-acl.md).

1. (Optional) Expand **Sync scope** to configure which content to crawl (files, pages).

1. (Optional) Expand **Date based entity syncing** to specify date filters.

1. (Optional) Expand **Item path pattern** to add specific paths to filter the items to be crawled.

------
#### [ API ]

To create a SharePoint data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. The following AWS Command Line Interface example creates a data source that uses Microsoft Entra ID App-Only authentication. To enable document-level access control, set `aclEnabled` to `true`. For a description of each field, see the connector parameters reference that follows.

```
aws bedrock-agent create-data-source \
 --name "{{SharePoint-connector}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://sharepoint-managed-connector.json
```

The `sharepoint-managed-connector.json` file contains the following:

```
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "connectorParameters": {
            "type": "SHAREPOINT",
            "version": "1",
            "aclEnabled": false,
            "connectionConfiguration": {
                "secretArn": "{{arn:aws:secretsmanager:us-west-2:123456789012:secret:bedrock-sharepoint-creds}}",
                "tenantId": "{{12345678-1234-1234-1234-123456789012}}",
                "authType": "ENTRA_ID_APP_ONLY",
                "certificateS3Path": {
                    "s3BucketName": "{{your-certificate-bucket}}",
                    "s3KeyName": "{{certs/certificate.p12}}"
                }
            },
            "dataEntityConfiguration": {
                "crawlFiles": true,
                "crawlPages": true,
                "siteUrls": [
                    "{{https://contoso.sharepoint.com/sites/engineering}}"
                ]
            }
        }
    }
}
```

For an `OAUTH2_APP` data source, set `authType` to `OAUTH2_APP` and omit `certificateS3Path`.

For managed knowledge bases, `CreateDataSource` is asynchronous: the data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

------

## Connector parameters
<a name="kb-managed-config-sharepoint"></a>

The data source configuration uses the following connector parameters. To connect to SharePoint, specify `SHAREPOINT` as the connector type in `connectorParameters`. For the fields that wrap `connectorParameters` (such as `deletionProtectionConfiguration` and `mediaExtractionConfiguration`), see [Connect a data source](kb-managed-connect-ds.md).


**connectionConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| secretArn | Yes | The ARN of the AWS Secrets Manager secret containing your SharePoint credentials. | 
| tenantId | Yes | The Microsoft Entra (Azure AD) tenant ID. | 
| authType | Yes | The authentication type: ENTRA\_ID\_APP\_ONLY (recommended) or OAUTH2\_APP. See [Authentication methods](kb-managed-ds-sharepoint.md#kb-managed-sharepoint-auth-methods). | 
| certificateS3Path | Conditional | Required for ENTRA\_ID\_APP\_ONLY authentication, even when ACLs are disabled. Contains s3BucketName and s3KeyName for the certificate file in Amazon S3. Not used with OAUTH2\_APP. | 


**dataEntityConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| siteUrls | Yes | List of SharePoint site URLs to crawl. Each URL is a crawl entry point and must start with https:// and point to a site, team site, or personal site — the path must begin with /sites/, /teams/, or /personal/ followed by the site name (for example, https://contoso.sharepoint.com/sites/engineering). Standard \*.sharepoint.com domains and custom (vanity) domains are both supported. Within each site, the connector crawls files and pages (see crawlFiles and crawlPages); to target specific items, use inclusionItemPaths. | 
| crawlFiles | No | Whether to crawl files. Defaults to true. | 
| crawlPages | No | Whether to crawl pages. Defaults to true. | 


**filterConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| modifiedDateBefore | No | Only include content modified before this date (ISO 8601). | 
| modifiedDateAfter | No | Only include content modified after this date (ISO 8601). | 
| inclusionItemPaths | No | Specific item paths to include. When you provide inclusionItemPaths, the connector crawls those items and does not validate siteUrls. | 


**aclEnabled (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| aclEnabled | No | Set to true to enable document-level access control. Requires ENTRA\_ID\_APP\_ONLY authentication. You cannot change this setting after you create the data source. For details, see [Document-level access controls](kb-managed-ds-sharepoint-acl.md). | 

## Change the authentication method
<a name="kb-managed-ds-sharepoint-change-auth"></a>

You can change a data source's authentication method (for example, from OAuth 2.0 to Microsoft Entra ID App-Only) by updating the data source with the new `authType` and credentials, using the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console. The document-level access control setting is fixed when you create a data source, so to add or remove ACLs you must create a new data source.

## Next steps
<a name="kb-managed-ds-sharepoint-connect-next"></a>

After you create the data source, sync it to ingest content into your knowledge base. For details, see [Sync a data source](kb-managed-sync.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-sharepoint-acl.md).