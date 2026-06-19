

# Microsoft SharePoint
<a name="kb-managed-ds-sharepoint"></a>

Microsoft SharePoint is a collaborative web-based service for working on documents, web pages, web sites, lists, and more. You can connect your SharePoint Online instance as a data source for your managed knowledge base to crawl files and pages from one or more SharePoint sites.

## Supported features
<a name="kb-managed-supported-features-sharepoint"></a>
+ Crawl files and pages from multiple SharePoint sites
+ Automatic detection of common document fields (such as title, author, and created or modified dates)
+ Inclusion content filters using item paths and date ranges
+ Incremental content syncs for added, updated, and deleted content
+ Microsoft Entra ID App-Only and OAuth 2.0 authentication
+ Document-level access control (ACLs), with Microsoft Entra ID App-Only authentication

## Authentication methods
<a name="kb-managed-sharepoint-auth-methods"></a>

A SharePoint data source supports two authentication methods. Choose one before you begin, because it determines the credentials you create and whether you can use document-level access control. We recommend Microsoft Entra ID App-Only authentication for new data sources.


**SharePoint authentication methods**  

| Method | How it authenticates | When to use | Setup | 
| --- | --- | --- | --- | 
| Microsoft Entra ID App-Only (ENTRA\_ID\_APP\_ONLY) — recommended | A Microsoft Entra application authenticates with a certificate. No user credentials and no interactive sign-in. | Most data sources, and any data source that uses document-level access control. | [Set up Entra ID App-Only authentication](kb-managed-sharepoint-entra-setup.md) | 
| OAuth 2.0 (OAUTH2\_APP) | An application client ID and secret, plus the user name and password of a Microsoft 365 user account that has access to the sites you want to crawl (the resource-owner password credentials, or ROPC, flow). | Use only if you cannot use Microsoft Entra ID App-Only authentication. The account must not require MFA or Conditional Access. Not supported with document-level access control. | [Set up OAuth 2.0 authentication](kb-managed-sharepoint-oauth2-setup.md) | 

**Important**  
The `OAUTH2_APP` method signs in with a user name and password, so it cannot complete a multi-factor authentication (MFA) challenge or satisfy a Conditional Access policy that requires one. If the account enforces MFA or Conditional Access, authentication fails and the data source cannot sync. Use Microsoft Entra ID App-Only authentication unless you have a specific reason to use `OAUTH2_APP`.

## Prerequisites
<a name="kb-managed-prereqs-sharepoint"></a>

**In Microsoft SharePoint, make sure you**:
+ Note the URLs of the SharePoint sites you want to crawl. Each URL is a crawl entry point and must start with `https://` and point to a site, team site, or personal site — the path must begin with `/sites/`, `/teams/`, or `/personal/` followed by the site name (for example, {{https://yourdomain.sharepoint.com/sites/mysite}}). Standard `*.sharepoint.com` domains and custom (vanity) domains are both supported. Within each site, the connector crawls files and pages; you can narrow the crawl to specific items with item path filters when you connect the data source.
+ Copy your Microsoft 365 tenant ID. You can find your tenant ID in the Properties of your Microsoft Entra portal. For details, see [Find your Microsoft 365 tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id) on the Microsoft Learn website.

**In your AWS account, make sure you**:
+ Store your authentication credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note the Amazon Resource Name (ARN) of the secret.
+ For the exact key-value pairs to store in the secret, see the setup page for your authentication method: [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md) or [Set up OAuth 2.0 authentication for SharePoint](kb-managed-sharepoint-oauth2-setup.md).
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## How to set up a SharePoint data source
<a name="kb-managed-sharepoint-workflow"></a>

Setting up a SharePoint data source involves the following steps:

1. **Set up authentication.** Follow the page for your chosen method to register a Microsoft Entra application, configure permissions, and store your credentials in AWS: [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md) or [Set up OAuth 2.0 authentication for SharePoint](kb-managed-sharepoint-oauth2-setup.md).

1. **Connect the data source.** Create the SharePoint data source in the knowledge base using the AWS Management Console or the API. See [Connect a SharePoint data source](kb-managed-ds-sharepoint-connect.md).

1. **(Optional) Enable document-level access control.** Filter query results by each user's SharePoint permissions. See [Document-level access controls](kb-managed-ds-sharepoint-acl.md).

If you run into problems during setup or syncing, see [Troubleshoot a SharePoint data source](kb-managed-ds-sharepoint-troubleshooting.md).