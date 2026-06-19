

# Document-level access controls
<a name="kb-managed-ds-googledrive-acl"></a>

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

Google Drive data sources optionally support document-level access control. When enabled, Bedrock Managed Knowledge Base syncs access control lists (ACLs) from Google Drive during each crawl and verifies each user's permissions at query time, so users only see results from documents they are authorized to access in Google Drive. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## How it works
<a name="kb-managed-ds-googledrive-acl-how"></a>

When a user queries a knowledge base that uses an ACL-enabled Google Drive data source, Bedrock Managed Knowledge Base enforces access controls in two stages:
+ **Pre-retrieval filtering** — Bedrock Managed Knowledge Base applies the access control lists that were synced from Google Drive during the last crawl, returning only candidate documents the user (or their groups) is permitted to access.
+ **Real-time verification** — Bedrock Managed Knowledge Base verifies the candidate documents in real time by checking the querying user's current access in Google Drive. Only documents the user is currently authorized to access are included in the response.

This two-stage approach provides document-level access control that stays current even when Google Drive permissions change between syncs.

## What is crawled
<a name="kb-managed-ds-googledrive-acl-crawl"></a>

When ACLs are enabled, Bedrock Managed Knowledge Base crawls file-level sharing permissions from Google Drive, including:
+ Direct user shares (individual file permissions)
+ Google Groups memberships
+ Shared drive memberships

## Enable ACL awareness
<a name="kb-managed-ds-googledrive-acl-enable"></a>

To enable ACL awareness for a Google Drive data source, set `aclEnabled` to `true` in the `connectorParameters` and use the `SERVICE_ACCOUNT` auth type. The service account must have domain-wide delegation enabled in your Google Workspace admin console.

**Important**  
ACL configuration is permanent. You cannot enable ACLs on a data source created without ACL support, and you cannot disable ACLs once enabled.

The AWS Secrets Manager secret must include `adminAccountEmail`, `clientEmail`, and `privateKey`. For step-by-step instructions to create the service account, configure domain-wide delegation, and obtain these values, see [Set up service account authentication for Google Drive](kb-managed-googledrive-service-account-setup.md).

```
"connectorParameters": {
    "type": "GOOGLEDRIVE",
    "version": "1",
    "aclEnabled": true,
    "connectionConfiguration": {
        "authType": "SERVICE_ACCOUNT",
        "secretArn": "{{arn:aws:secretsmanager:region:account-id:secret:secret-name}}"
    },
    "dataEntityConfiguration": {
        "crawlMyDrive": true,
        "crawlSharedWithMe": false,
        "crawlSharedDrives": false
    }
}
```

**Note**  
The `OAUTH2` auth type is not supported for ACL-enabled Google Drive data sources. You must use `SERVICE_ACCOUNT` with domain-wide delegation.

## Real-time access verification
<a name="kb-managed-ds-googledrive-acl-realtime"></a>

Bedrock Managed Knowledge Base uses the service account's domain-wide delegation to verify document access in real time against the Google Drive API, confirming the querying user still has access to each candidate document.

## Verify your configuration
<a name="kb-managed-ds-googledrive-acl-verify"></a>

You can validate your service account configuration independently of a retrieve request. Perform each of the following checks:

1. **Domain-wide delegation**:
   + In the Google Workspace Admin console, confirm the service account client ID is authorized for the required scopes (Google Drive read-only and the Admin SDK directory/group read scopes).

1. **Drive access (crawl and verification)**:
   + Using the service account (`clientEmail` and `privateKey`) impersonating `adminAccountEmail`, call the Google Drive API to list a user's files and confirm it succeeds.

1. **Group resolution**:
   + Call the Admin SDK Directory API to list a user's group memberships and confirm it returns the expected groups.

## Troubleshooting
<a name="kb-managed-ds-googledrive-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the verification checks above to diagnose these issues.


**ACL-enabled Google Drive symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results, but the user has access in Google Drive. | Domain-wide delegation is not configured, or the service account is missing required scopes, so access cannot be verified. | Authorize the service account client ID for the required Drive and Admin SDK scopes in the Google Workspace Admin console. | 
| Group-based access is not honored. | The Admin SDK directory/group read scope is missing from the delegation. | Add the Admin SDK group read scope to the service account's domain-wide delegation. | 
| Crawl or sync fails. | The clientEmail/privateKey is invalid, or adminAccountEmail is not a Workspace admin. | Verify the service account credentials and that adminAccountEmail is a Workspace administrator. | 
| All users are denied after previously working. | The service account key was rotated or revoked. | Update the privateKey in the secret. | 