

# Connect a OneDrive data source
<a name="kb-managed-ds-onedrive-connect"></a>

After you set up authentication and store your credentials in an AWS Secrets Manager secret, create the OneDrive data source in your knowledge base. This page describes how to create the data source with the AWS Management Console or the API, followed by a reference for the connector parameters you can configure.

**Note**  
Complete authentication setup first. See [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md) (recommended) or [Set up OAuth 2.0 authentication for OneDrive](kb-managed-onedrive-oauth2-setup.md). You need the secret ARN, your tenant ID, and (for document-level access control) the Amazon S3 location of your certificate.

## Create the data source
<a name="kb-managed-ds-onedrive-create"></a>

------
#### [ Console ]

**To connect OneDrive to your managed knowledge base**

1. Under **Data source**, provide a name for your data source.

1. Select **OneDrive** from the data source dropdown.

1. Under **Source**, enter your **OneDrive Tenant ID**.

1. Under **Authentication**, select **Microsoft Entra ID App** or **OAuth 2.0 authentication**.

1. Select or create an AWS Secrets Manager secret to store your credentials.

1. (Optional) To enable document-level access control, select **Control document access with ACLs** and provide the **Certificate path** — the Amazon S3 path to your `.p12` certificate file. This option is available only with Microsoft Entra ID App authentication and cannot be changed after creation. For details, see [Document-level access controls](kb-managed-ds-onedrive-acl.md).

1. (Optional) Expand **Sync scope** to choose which content to crawl. With Microsoft Entra ID App authentication, only personal drives can be crawled.

1. (Optional) Expand **User emails** to add specific emails of users whose data you want to include or exclude.

1. (Optional) Expand **File path filters** to include or exclude specific files and folders.

1. (Optional) Expand **Mime types regex pattern** to add regex patterns to include or exclude specific MIME types.

1. (Optional) Expand **Date based entity syncing** to specify date filters.

------
#### [ API ]

To create a OneDrive data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. The following AWS Command Line Interface example creates a data source that uses Microsoft Entra App ID authentication. To enable document-level access control, set `aclEnabled` to `true` and add a `certificateS3Path` to `connectionConfiguration`. For a description of each field, see the connector parameters reference that follows.

```
aws bedrock-agent create-data-source \
 --name "{{OneDrive-connector}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://onedrive-managed-connector.json
```

The `onedrive-managed-connector.json` file contains the following:

```
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "connectorParameters": {
            "type": "ONEDRIVE",
            "version": "1",
            "aclEnabled": false,
            "connectionConfiguration": {
                "secretArn": "{{arn:aws:secretsmanager:us-west-2:123456789012:secret:bedrock-onedrive-creds}}",
                "tenantId": "{{12345678-1234-1234-1234-123456789012}}",
                "authType": "ENTRA_APP_ID"
            },
            "dataEntityConfiguration": {
                "crawlPersonalDrives": true
            }
        }
    }
}
```

To enable document-level access control, set `aclEnabled` to `true` and add `certificateS3Path` to `connectionConfiguration`:

```
{
    "type": "ONEDRIVE",
    "version": "1",
    "aclEnabled": true,
    "connectionConfiguration": {
        "secretArn": "{{arn:aws:secretsmanager:us-west-2:123456789012:secret:bedrock-onedrive-creds}}",
        "tenantId": "{{12345678-1234-1234-1234-123456789012}}",
        "authType": "ENTRA_APP_ID",
        "certificateS3Path": {
            "s3BucketName": "{{your-certificate-bucket}}",
            "s3KeyName": "{{certs/certificate.p12}}"
        }
    },
    "dataEntityConfiguration": {
        "crawlPersonalDrives": true
    }
}
```

For an `OAUTH2` data source, set `authType` to `OAUTH2` and omit `certificateS3Path`.

For managed knowledge bases, `CreateDataSource` is asynchronous: the data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

------

## Connector parameters
<a name="kb-managed-config-onedrive"></a>

The data source configuration uses the following connector parameters. To connect to OneDrive, specify `ONEDRIVE` as the connector type in `connectorParameters`. For the fields that wrap `connectorParameters` (such as `deletionProtectionConfiguration` and `mediaExtractionConfiguration`), see [Connect a data source](kb-managed-connect-ds.md).


**connectionConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| secretArn | Yes | The ARN of the AWS Secrets Manager secret containing your OneDrive credentials. | 
| tenantId | Yes | The Microsoft Entra (Azure AD) tenant ID. | 
| authType | Yes | The authentication type: ENTRA\_APP\_ID (recommended) or OAUTH2. See [Authentication methods](kb-managed-ds-onedrive.md#kb-managed-onedrive-auth-methods). | 
| certificateS3Path | Conditional | Required when aclEnabled is true (Microsoft Entra App ID authentication). Contains s3BucketName and s3KeyName for the .p12 certificate file in Amazon S3. Not used for content-only crawling or with OAUTH2. | 


**dataEntityConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| crawlPersonalDrives | No | Whether to crawl users' personal drives. | 
| crawlSharedWithMe | No | Whether to crawl files shared with the signed-in user. Supported only with OAUTH2 authentication. Microsoft Entra App ID (application-only) authentication cannot crawl shared files. | 

**Note**  
OneNote notebooks are not currently supported.


**filterConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| inclusionUserEmailAddresses | No | User email addresses whose drives to include. | 
| exclusionUserEmailAddresses | No | User email addresses whose drives to exclude. | 
| userFilterPath | No | An Amazon S3 URL pointing to a file that lists the users to include or exclude. | 
| inclusionDriveItems | No | Drive item paths to include. | 
| exclusionDriveItems | No | Drive item paths to exclude. | 
| includeMimeTypes | No | MIME types to include. | 
| excludeMimeTypes | No | MIME types to exclude. | 
| absoluteDateBefore | No | Only include content modified before this date (ISO 8601). | 
| absoluteDateAfter | No | Only include content modified after this date (ISO 8601). | 

**Note**  
With `OAUTH2` authentication the connector crawls in the signed-in user's delegated context. The user-based filters (`inclusionUserEmailAddresses`, `exclusionUserEmailAddresses`, `userFilterPath`) determine which users' drives the connector attempts; drives the signed-in user cannot access are silently skipped. To crawl every user's OneDrive in your tenant regardless of permissions, use `ENTRA_APP_ID` authentication.


**aclEnabled (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| aclEnabled | No | Set to true to enable document-level access control. Requires ENTRA\_APP\_ID authentication and a certificateS3Path in connectionConfiguration. You cannot change this setting after you create the data source. For details, see [Document-level access controls](kb-managed-ds-onedrive-acl.md). | 

## Change the authentication method
<a name="kb-managed-ds-onedrive-change-auth"></a>

You can change a data source's authentication method (for example, from OAuth 2.0 to Microsoft Entra App ID) by updating the data source with the new `authType` and credentials, using the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console. The document-level access control setting is fixed when you create a data source, so to add or remove ACLs you must create a new data source.

## Next steps
<a name="kb-managed-ds-onedrive-connect-next"></a>

After you create the data source, sync it to ingest content into your knowledge base. For details, see [Sync a data source](kb-managed-sync.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-onedrive-acl.md).