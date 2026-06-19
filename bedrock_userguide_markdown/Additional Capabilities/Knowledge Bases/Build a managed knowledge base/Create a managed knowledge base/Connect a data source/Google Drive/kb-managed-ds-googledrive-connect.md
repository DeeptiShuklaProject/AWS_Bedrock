

# Connect a Google Drive data source
<a name="kb-managed-ds-googledrive-connect"></a>

After you set up authentication and store your credentials in an AWS Secrets Manager secret, create the Google Drive data source in your knowledge base. This page describes how to create the data source with the AWS Management Console or the API, followed by a reference for the connector parameters you can configure.

**Note**  
Complete authentication setup first. See [Set up service account authentication for Google Drive](kb-managed-googledrive-service-account-setup.md) (recommended) or [Set up OAuth 2.0 authentication for Google Drive](kb-managed-googledrive-oauth2-setup.md). You need the secret ARN.

## Create the data source
<a name="kb-managed-ds-googledrive-create"></a>

------
#### [ Console ]

**To connect Google Drive to your managed knowledge base**

1. Under **Data source**, provide a name for your data source.

1. Select **Google Drive** from the data source dropdown.

1. Under **Authentication**, select **Google service account** or **OAuth 2.0 authentication**.

1. Select or create an AWS Secrets Manager secret to store your credentials.

1. (Optional, service account only) To enable document-level access control, select **Control document access with ACLs**. This option cannot be changed after creation. For details, see [Document-level access controls](kb-managed-ds-googledrive-acl.md).

1. (Optional) Expand **Sync scope** to choose which drives to crawl (My Drive, Shared with me, Shared drives).

1. (Optional) Expand **Shared drives** to add shared drive IDs to include or exclude.

1. (Optional, OAuth 2.0 only) Expand **Specific folders and files** to add folder or file IDs to include.

1. (Optional) Expand **Mime types regex pattern** to include or exclude specific MIME types.

1. (Optional) Expand **Date based entity syncing** to specify date filters.

------
#### [ API ]

To create a Google Drive data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. The following AWS Command Line Interface example creates a data source that uses service account authentication. To use OAuth 2.0, change `authType` to `OAUTH2`. To enable document-level access control, set `aclEnabled` to `true`. For a description of each field, see the connector parameters reference that follows.

```
aws bedrock-agent create-data-source \
 --name "{{GoogleDrive-connector}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://googledrive-managed-connector.json
```

The `googledrive-managed-connector.json` file contains the following:

```
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "connectorParameters": {
            "type": "GOOGLEDRIVE",
            "version": "1",
            "aclEnabled": false,
            "connectionConfiguration": {
                "secretArn": "{{arn:aws:secretsmanager:us-west-2:123456789012:secret:bedrock-google-drive-sa-creds}}",
                "authType": "SERVICE_ACCOUNT"
            },
            "dataEntityConfiguration": {
                "crawlMyDrive": true,
                "crawlSharedWithMe": true,
                "crawlSharedDrives": false
            },
            "filterConfiguration": {
                "inclusionMimeTypes": ["application/pdf"]
            }
        }
    }
}
```

For managed knowledge bases, `CreateDataSource` is asynchronous: the data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

------

## Connector parameters
<a name="kb-managed-config-googledrive"></a>

The data source configuration uses the following connector parameters. To connect to Google Drive, specify `GOOGLEDRIVE` as the connector type in `connectorParameters`. For the fields that wrap `connectorParameters` (such as `deletionProtectionConfiguration` and `mediaExtractionConfiguration`), see [Connect a data source](kb-managed-connect-ds.md).

**Set `aclEnabled` explicitly**  
If you omit `aclEnabled`, the default depends on `authType`: `SERVICE_ACCOUNT` defaults to `true`, and `OAUTH2` defaults to `false`. Because ACL configuration is permanent after the data source is created, set `aclEnabled` explicitly so the data source has the access-control behavior you intend. For details, see [Document-level access controls](kb-managed-ds-googledrive-acl.md).


**connectionConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| secretArn | Yes | The ARN of the AWS Secrets Manager secret containing your Google Drive credentials. | 
| authType | Yes | The authentication type: SERVICE\_ACCOUNT (recommended) or OAUTH2. See [Authentication methods](kb-managed-ds-googledrive.md#kb-managed-googledrive-auth-methods). | 


**dataEntityConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| crawlMyDrive | No | Whether to crawl the authenticated user's personal drive. | 
| crawlSharedWithMe | No | Whether to crawl files shared with the authenticated user. | 
| crawlSharedDrives | No | Whether to crawl shared drives. | 


**filterConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| inclusionSharedDriveIds | No | Shared drive IDs to include. | 
| exclusionSharedDriveIds | No | Shared drive IDs to exclude. | 
| inclusionMimeTypes | No | MIME types to include. | 
| exclusionMimeTypes | No | MIME types to exclude. | 
| inclusionFolderIds | No | Folder IDs to include. Available only with OAUTH2 authentication. | 
| inclusionFileIds | No | File IDs to include. Available only with OAUTH2 authentication. | 
| inclusionSharedFolderIds | No | Shared folder IDs to include. Available only with OAUTH2 authentication. | 
| inclusionSharedFileIds | No | Shared file IDs to include. Available only with OAUTH2 authentication. | 
| modifiedDateBefore | No | Only include content modified before this date (ISO 8601). | 
| modifiedDateAfter | No | Only include content modified after this date (ISO 8601). If modifiedDateBefore is earlier than modifiedDateAfter, no content matches the window. | 
| maxFileSizeInMegaBytes | No | Maximum size, in megabytes, of any single file the connector ingests. Provide as a numeric string (for example, "500"). Defaults to "500". | 


**aclEnabled (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| aclEnabled | No | Whether document-level access control is enabled. Set to true to enable, or false to disable. If you omit this field, the default depends on authType: SERVICE\_ACCOUNT defaults to true; OAUTH2 defaults to false. ACL requires SERVICE\_ACCOUNT authentication. You cannot change this setting after you create the data source. For details, see [Document-level access controls](kb-managed-ds-googledrive-acl.md). | 

## Change the authentication method
<a name="kb-managed-ds-googledrive-change-auth"></a>

You can change a data source's authentication method (for example, from OAuth 2.0 to service account) by updating the data source with the new `authType` and a secret that contains the matching credentials, using the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console. The document-level access control setting is fixed when you create a data source, so to add or remove ACLs you must create a new data source.

## Next steps
<a name="kb-managed-ds-googledrive-connect-next"></a>

After you create the data source, sync it to ingest content into your knowledge base. For details, see [Sync a data source](kb-managed-sync.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-googledrive-acl.md).