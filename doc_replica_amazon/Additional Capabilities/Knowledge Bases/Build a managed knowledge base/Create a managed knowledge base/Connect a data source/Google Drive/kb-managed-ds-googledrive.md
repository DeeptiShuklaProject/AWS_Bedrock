

# Google Drive
<a name="kb-managed-ds-googledrive"></a>

Google Drive is a cloud-based file storage and collaboration service. You can connect Google Drive as a data source for your managed knowledge base to crawl personal drives, shared drives, and files shared with the authenticated identity.

## Supported features
<a name="kb-managed-supported-features-googledrive"></a>
+ Crawl personal drives, shared drives, and files shared with the authenticated identity
+ Automatic detection of common document fields (such as title, author, and created or modified dates)
+ Inclusion and exclusion content filters by shared drive IDs and MIME types
+ Granular inclusion of specific folders and files (with OAuth 2.0 authentication only)
+ Date-based filtering for content modified before or after a specific date
+ Incremental content syncs for added, updated, and deleted content
+ Service account and OAuth 2.0 authentication
+ Document-level access control (ACLs), with service account authentication

## Authentication methods
<a name="kb-managed-googledrive-auth-methods"></a>

A Google Drive data source supports two authentication methods. Choose one before you begin, because it determines the credentials you create, what content the connector can crawl, and whether you can use document-level access control. We recommend service account authentication for new data sources.


**Google Drive authentication methods**  

| Method | How it authenticates | When to use | Setup | 
| --- | --- | --- | --- | 
| Service account (SERVICE\_ACCOUNT) — recommended | A Google Cloud service account with domain-wide delegation authenticates with a private key, then impersonates a Google Workspace admin user to access Drive content for any user in your domain. | Most data sources, and any data source that uses document-level access control. Requires a Google Workspace administrator to set up. | [Set up service account authentication](kb-managed-googledrive-service-account-setup.md) | 
| OAuth 2.0 (OAUTH2) | An OAuth 2.0 client ID and secret together with a delegated refresh token that you obtain from a single Google user's sign-in. The connector accesses only the content that user can access. | Use when a single Google user has access to all the Drive content you want to crawl, or when you cannot configure domain-wide delegation. Granular folder and file ID filters are available only with this method. Not supported with document-level access control. | [Set up OAuth 2.0 authentication](kb-managed-googledrive-oauth2-setup.md) | 

**Important**  
Service account authentication requires Google Workspace administrator access. If your organization restricts third-party app access in Google Workspace, your administrator might also need to allow OAuth 2.0 access on your behalf for the OAuth 2.0 method.

## Prerequisites
<a name="kb-managed-prereqs-googledrive"></a>

**In Google Workspace and Google Cloud, make sure you**:
+ Have access to a Google Cloud project where you can enable APIs and create credentials.
+ Have a Google Workspace account with an email domain that matches the content you want to crawl. For service account authentication, you also need administrator access to the Google Workspace.

**In your AWS account, make sure you**:
+ Store your authentication credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note the Amazon Resource Name (ARN) of the secret.
+ For the exact key-value pairs to store in the secret, see the setup page for your authentication method: [Set up service account authentication for Google Drive](kb-managed-googledrive-service-account-setup.md) or [Set up OAuth 2.0 authentication for Google Drive](kb-managed-googledrive-oauth2-setup.md).
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## How to set up a Google Drive data source
<a name="kb-managed-googledrive-workflow"></a>

Setting up a Google Drive data source involves the following steps:

1. **Set up authentication.** Follow the page for your chosen method to configure Google Cloud and Google Workspace, generate credentials, and store them in AWS: [Set up service account authentication for Google Drive](kb-managed-googledrive-service-account-setup.md) or [Set up OAuth 2.0 authentication for Google Drive](kb-managed-googledrive-oauth2-setup.md).

1. **Connect the data source.** Create the Google Drive data source in the knowledge base using the AWS Management Console or the API. See [Connect a Google Drive data source](kb-managed-ds-googledrive-connect.md).

1. **(Optional) Enable document-level access control.** Filter query results by each user's Google Drive permissions. Requires service account authentication. See [Document-level access controls](kb-managed-ds-googledrive-acl.md).