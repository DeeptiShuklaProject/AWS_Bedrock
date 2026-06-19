

# ACL-aware retrieval on managed knowledge bases
<a name="kb-test-retrieve-acl"></a>

When ACL awareness is enabled on a managed knowledge base data source, you filter query results by passing a user context in your [Retrieve](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) request. Bedrock Managed Knowledge Base returns only the documents that the supplied user is permitted to access. For an overview of how ACL awareness works, the identity model, connector support, and your responsibilities when enabling it, see [Access Control Lists awareness enablement](kb-managed-acl.md).

**Important**  
ACL awareness provides ACL-aware filtering, not authorization. Bedrock Managed Knowledge Base does not authenticate end users — your application must authenticate users and pass verified identity context. For details, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## Using userContext in Retrieve requests
<a name="kb-test-retrieve-acl-api"></a>

To perform ACL-aware retrieval, include the `userContext` field in your [Retrieve](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) request. The `userContext` specifies the user's identity. The `userId` is always the user's universal email address associated with the underlying data source.

```
{
    "knowledgeBaseId": "{{your-knowledge-base-id}}",
    "retrievalQuery": {
        "text": "{{your query}}"
    },
    "userContext": {
        "userId": "{{user@example.com}}"
    }
}
```

If you do not provide `userContext` in a Retrieve request, ACL-enabled data sources return zero results. Non-ACL data sources in the same knowledge base return results normally.

## Retrieval behavior with ACLs
<a name="kb-test-retrieve-acl-behavior"></a>

When ACL awareness is enabled, the following behaviors apply:
+ **User context required for ACL-enabled data sources** — If you do not provide user context in a Retrieve request, ACL-enabled data sources return zero results. Non-ACL data sources in the same knowledge base return results normally.
+ **Missing ACL metadata means inaccessible** — If a document in an ACL-enabled data source has no ACL (for example, the connector failed to extract permissions or the document is public), that document is not returned to any user. Missing permissions are treated as restricted, not public.
+ **Mixed data sources** — You can have both ACL-enabled and non-ACL data sources in the same knowledge base. Documents from non-ACL data sources are returned to all users regardless of user context.
+ **Partial results** — When real-time ACL verification denies access to some documents, the response may contain fewer results than the requested `maxResults`. Bedrock Managed Knowledge Base does not backfill with additional documents. Your application should handle responses with fewer results than requested.
+ **Deny overrides allow** — If a user appears in both an allow list and a deny list for a document, access is denied.

**Note**  
Third-party identity provider credentials are cached for up to 1 hour. Access may continue until the cache refreshes.  
Changes to access control permissions are eventually consistent. Updates typically take effect within a few minutes.

## Troubleshooting
<a name="kb-test-retrieve-acl-troubleshooting"></a>

If ACL-aware retrieval returns no results or unexpected results, the cause is usually connector-specific — permissions, credentials, or ACL configuration. See the troubleshooting guidance for your connector:
+ [SharePoint](kb-managed-ds-sharepoint-acl.md#kb-managed-ds-sharepoint-acl-troubleshooting)
+ [OneDrive](kb-managed-ds-onedrive-acl.md#kb-managed-ds-onedrive-acl-troubleshooting)
+ [Google Drive](kb-managed-ds-googledrive-acl.md#kb-managed-ds-googledrive-acl-troubleshooting)
+ [Confluence](kb-managed-ds-confluence-acl.md#kb-managed-ds-confluence-acl-troubleshooting)
+ [Amazon S3](kb-managed-ds-s3-acl.md#kb-managed-ds-s3-acl-troubleshooting)
+ [Custom](kb-managed-ds-custom-acl.md#kb-managed-ds-custom-acl-troubleshooting)