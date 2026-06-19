

# Access Control Lists awareness enablement
<a name="kb-managed-acl"></a>

Bedrock Managed Knowledge Base supports *ACL-aware retrieval* — the ability to filter query results based on document-level access control lists (ACLs) crawled from your connected data sources. When ACL awareness is enabled on a data source, Bedrock Managed Knowledge Base ingests the permissions (allowed users, denied users, allowed groups, denied groups) alongside document content. At query time, you supply a user context and Bedrock Managed Knowledge Base returns only the documents that user is permitted to access. For the request syntax used to pass user context at retrieval time, see [ACL-aware retrieval on managed knowledge bases](kb-test-retrieve-acl.md).

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides *ACL-aware filtering*, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

## How ACL-aware retrieval works
<a name="kb-managed-acl-how-it-works"></a>

ACL-aware retrieval operates in two stages:
+ **Pre-retrieval filtering** — During ingestion, Bedrock Managed Knowledge Base crawls document permissions from the data source. At query time, Bedrock Managed Knowledge Base uses the user context you provide to filter the search results, returning only documents where the user (or their groups) appears in the allow list and does not appear in the deny list.
+ **Real-time ACL verification** — For connectors that support it (SharePoint, OneDrive, Google Drive, Confluence), Bedrock Managed Knowledge Base makes a real-time call to the data source to verify that the user still has access to each returned document. This catches permission changes that occurred between syncs. S3 and Custom connectors do not support real-time verification because their ACL metadata is provided by the customer through configuration files rather than crawled from a live permission system.

Both stages use the same evaluation logic: if a user appears in both an allow list and a deny list for a document, access is denied. Deny always overrides allow.

## Identity model
<a name="kb-managed-acl-identity"></a>

Bedrock Managed Knowledge Base uses *email* as the universal user identifier for ACL matching. The user is *always* identified by their universal email — the email you pass in the user context must exactly match the email associated with the user in each connected data source. There is no alias resolution or cross-identity-provider mapping. Groups, by contrast, are identified by however the source connector represents them — a group name, a group ID, or another identifier — and are matched against the group memberships crawled from that data source.

Group memberships are resolved from the data source. During ingestion, Bedrock Managed Knowledge Base crawls group memberships from each data source and stores them internally. At query time, Bedrock Managed Knowledge Base resolves which groups a user belongs to based on this crawled data automatically.

**Note**  
Group memberships are as fresh as the last sync. Permission changes between syncs are not reflected until the next ingestion job completes. For connectors that support real-time ACL verification, this check catches permission changes that occurred since the last sync.

## Connector support matrix
<a name="kb-managed-acl-connector-support"></a>

Not all connectors support ACL awareness. The following table shows which connectors support pre-retrieval filtering and real-time ACL verification.


**ACL support by connector**  

| Connector | Pre-retrieval filter | Real-time ACL | Notes | 
| --- | --- | --- | --- | 
| [SharePoint](kb-managed-ds-sharepoint-acl.md) | Supported | Supported | Uses application-level permissions (2LO). Requires ENTRA\_ID\_APP\_ONLY auth type. | 
| [OneDrive](kb-managed-ds-onedrive-acl.md) | Supported | Supported | Uses application-level permissions (2LO). Requires ENTRA\_APP\_ID auth type. | 
| [Google Drive](kb-managed-ds-googledrive-acl.md) | Supported | Supported | Uses domain-wide delegation (2LO). Requires SERVICE\_ACCOUNT auth type. | 
| [Confluence](kb-managed-ds-confluence-acl.md) | Supported | Supported | Uses admin API token for real-time checks. Requires BASIC auth type. | 
| [Amazon S3](kb-managed-ds-s3-acl.md) | Supported | Not supported | ACLs defined via a customer-provided ACL configuration file in Amazon S3. No real-time verification because the customer-provided metadata file is the source of truth. | 
| [Custom](kb-managed-ds-custom-acl.md) | Supported | Not supported | ACLs defined via customer-provided metadata. No real-time verification because the customer-provided metadata is the source of truth. | 
| Web Crawler | Not supported | N/A | Web content has no permission model. ACL awareness cannot be enabled for this connector. | 

For connector-specific ACL configuration details, see:
+ [ACL awareness for SharePoint](kb-managed-ds-sharepoint-acl.md)
+ [ACL awareness for OneDrive](kb-managed-ds-onedrive-acl.md)
+ [ACL awareness for Google Drive](kb-managed-ds-googledrive-acl.md)
+ [ACL awareness for Confluence](kb-managed-ds-confluence-acl.md)
+ [ACL awareness for Amazon S3](kb-managed-ds-s3-acl.md)
+ [ACL awareness for Custom](kb-managed-ds-custom-acl.md)

## Failure behavior
<a name="kb-managed-acl-failure"></a>

ACL-aware retrieval fails closed. If any part of the ACL evaluation pipeline encounters an error — group resolution failure, real-time verification timeout, or internal service error — Bedrock Managed Knowledge Base does not return the affected documents. A transient failure never results in documents being returned to unauthorized users.

When an ACL failure occurs, the response may contain zero results or fewer results than expected. Error responses indicate an ACL resolution failure so you can distinguish it from a query that genuinely matched no documents.

## Your responsibilities
<a name="kb-managed-acl-responsibilities"></a>

Because Bedrock Managed Knowledge Base provides ACL-aware filtering and not a complete authorization solution, you are responsible for the following:
+ **Authenticating end users** — You must authenticate users in your application before passing their identity to Bedrock Managed Knowledge Base. Bedrock Managed Knowledge Base does not verify that the user context you provide is authentic.
+ **Consistent email identity** — The email address you pass must match the email used in each connected data source. If emails differ across systems, ACL matching fails silently and the user receives no results from that data source.
+ **Email lifecycle management** — If an email address is reassigned to a different person (for example, after an employee departure), you must detect this before passing the identity to Bedrock Managed Knowledge Base. Real-time ACL verification acts as a safety net for connectors that support it, but is not a substitute for proper identity lifecycle management.