

# Document-level access controls
<a name="kb-managed-ds-confluence-acl"></a>

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

Confluence data sources optionally support document-level access control. When enabled, Bedrock Managed Knowledge Base syncs access control lists (ACLs) from Confluence during each crawl and verifies each user's permissions at query time, so users only see results from documents they are authorized to access in Confluence. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## How it works
<a name="kb-managed-ds-confluence-acl-how"></a>

When a user queries a knowledge base that uses an ACL-enabled Confluence data source, Bedrock Managed Knowledge Base enforces access controls in two stages:
+ **Pre-retrieval filtering** — Bedrock Managed Knowledge Base applies the access control lists that were synced from Confluence during the last crawl, returning only candidate documents the user (or their groups) is permitted to access.
+ **Real-time verification** — Bedrock Managed Knowledge Base verifies the candidate documents in real time by checking the querying user's current access in Confluence. Only documents the user is currently authorized to access are included in the response.

This two-stage approach provides document-level access control that stays current even when Confluence permissions change between syncs.

## What is crawled
<a name="kb-managed-ds-confluence-acl-crawl"></a>

When ACLs are enabled, Bedrock Managed Knowledge Base crawls the following permission structures from Confluence:
+ **Spaces** — Space permissions apply to all documents in the space by default.
+ **Pages** — Pages can be restricted to specific users and groups. Nested pages inherit restrictions from the parent page.
+ **Blogs** — Blog posts can be restricted to specific users and groups.
+ **Attachments** — Files attached to pages or blog posts inherit the access controls of their parent document.

## Enable ACL awareness
<a name="kb-managed-ds-confluence-acl-enable"></a>

To enable ACL awareness for a Confluence data source, set `aclEnabled` to `true` in the `connectorParameters` and use the `BASIC` auth type. The secret must include Atlassian organization admin credentials in addition to the standard email and API token. These admin credentials are required for identity crawling.

**Important**  
ACL configuration is permanent. You cannot enable ACLs on a data source created without ACL support, and you cannot disable ACLs once enabled.

In addition to the standard `username`, `password` (API token), and `hostUrl` fields, the AWS Secrets Manager secret must include the following organization admin fields. For step-by-step instructions to obtain these values, see [Set up Basic authentication for Confluence](kb-managed-confluence-basic-setup.md).
+ `adminApiKey` — An Atlassian organization API key with the `read:directories:admin` and `read:workspaces:admin` scopes.
+ `organizationId` — The UUID of your Atlassian organization.
+ `directoryId` — The UUID of the user directory for your Confluence workspace.

**Note**  
The `OAUTH2` auth type is not supported for ACL-enabled Confluence data sources. You must use `BASIC` with Atlassian organization admin credentials in the secret.

## Real-time access verification
<a name="kb-managed-ds-confluence-acl-realtime"></a>

Bedrock Managed Knowledge Base verifies each candidate document against Confluence at query time entirely server-side, using the Atlassian Admin API token configured in the secret — there is no end-user sign-in. The admin token checks the querying user's current space, page, and blog restrictions, so access changes made since the last crawl are honored.

## Verify your configuration
<a name="kb-managed-ds-confluence-acl-verify"></a>

You can validate your credentials independently of a retrieve request. Perform each of the following checks:

1. **Confluence content access (crawl)**:
   + Using the `username` and API token (`password`) from the secret, call the Confluence REST API (for example, list spaces) and confirm it returns HTTP 200.

1. **Atlassian Admin API (identity crawling and real-time verification)**:
   + Confirm the `adminApiKey` has the `read:directories:admin` and `read:workspaces:admin` scopes.
   + Using the `adminApiKey`, call the Atlassian admin directory API for your `organizationId` and `directoryId` and confirm it returns your organization's users and groups.

## Troubleshooting
<a name="kb-managed-ds-confluence-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the verification checks above to diagnose these issues.


**ACL-enabled Confluence symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results, but the user has access in Confluence. | The Atlassian Admin API key is missing scopes, or the organizationId/directoryId is wrong, so user and group restrictions cannot be resolved. | Confirm the adminApiKey has read:directories:admin and read:workspaces:admin, and that organizationId and directoryId are correct. | 
| Crawl or sync fails. | The username or API token (password) is invalid. | Verify the BASIC username and API token in the secret. | 
| All users are denied after previously working. | The API token or admin API key expired or was revoked. | Rotate the affected credentials in the secret. | 