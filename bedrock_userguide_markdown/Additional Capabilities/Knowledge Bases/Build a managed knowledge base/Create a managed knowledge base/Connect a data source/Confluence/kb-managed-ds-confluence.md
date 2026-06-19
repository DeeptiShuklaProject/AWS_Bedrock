

# Confluence
<a name="kb-managed-ds-confluence"></a>

Atlassian Confluence is a collaborative work-management tool for sharing, storing, and working on documents and pages. You can connect your Confluence Cloud instance as a data source for your managed knowledge base to crawl pages, blog posts, and their attachments. Only Confluence Cloud (SaaS) is supported; Confluence Server and Data Center are not.

## Supported features
<a name="kb-managed-supported-features-confluence"></a>
+ Crawl pages, blog posts, and their attachments across spaces
+ Automatic detection of common document fields (such as title, author, and created or modified dates)
+ Inclusion content filters for spaces, pages, and blogs
+ Inclusion or exclusion content filters for MIME types
+ Incremental content syncs for added, updated, and deleted content
+ Basic and OAuth 2.0 authentication
+ Document-level access control (ACLs), with Basic authentication and Atlassian organization admin credentials

## Authentication methods
<a name="kb-managed-confluence-auth-methods"></a>

A Confluence data source supports two authentication methods. Choose one before you begin, because it determines the credentials you create and whether you can use document-level access control. We recommend Basic authentication for new data sources.


**Confluence authentication methods**  

| Method | How it authenticates | When to use | Setup | 
| --- | --- | --- | --- | 
| Basic (BASIC) — recommended | The connector signs in with the email address and an Atlassian API token of a Confluence user. | Most data sources, and any data source that uses document-level access control. ACLs additionally require Atlassian organization admin credentials in the same secret. | [Set up Basic authentication](kb-managed-confluence-basic-setup.md) | 
| OAuth 2.0 (OAUTH2) | The connector authenticates as an Atlassian OAuth 2.0 (3LO) app, using an app key, app secret, access token, and refresh token. The access token is renewed automatically with the refresh token. | Use when you want a registered Atlassian app instead of an individual user account. Not supported with document-level access control. | [Set up OAuth 2.0 authentication](kb-managed-confluence-oauth2-setup.md) | 

## Prerequisites
<a name="kb-managed-prereqs-confluence"></a>

**In Confluence, make sure you**:
+ Note your Confluence Cloud instance URL (for example, {{https://example.atlassian.net}}). The URL is the base URL ending with `.atlassian.net`.

**In your AWS account, make sure you**:
+ Store your authentication credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note the Amazon Resource Name (ARN) of the secret.
+ For the exact key-value pairs to store in the secret, see the setup page for your authentication method: [Set up Basic authentication for Confluence](kb-managed-confluence-basic-setup.md) or [Set up OAuth 2.0 authentication for Confluence](kb-managed-confluence-oauth2-setup.md).
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## How to set up a Confluence data source
<a name="kb-managed-confluence-workflow"></a>

Setting up a Confluence data source involves the following steps:

1. **Set up authentication.** Follow the page for your chosen method to create the credentials in Confluence and store them in AWS: [Set up Basic authentication for Confluence](kb-managed-confluence-basic-setup.md) or [Set up OAuth 2.0 authentication for Confluence](kb-managed-confluence-oauth2-setup.md).

1. **Connect the data source.** Create the Confluence data source in the knowledge base using the AWS Management Console or the API. See [Connect a Confluence data source](kb-managed-ds-confluence-connect.md).

1. **(Optional) Enable document-level access control.** Filter query results by each user's Confluence permissions. Requires Basic authentication with Atlassian organization admin credentials. See [Document-level access controls](kb-managed-ds-confluence-acl.md).