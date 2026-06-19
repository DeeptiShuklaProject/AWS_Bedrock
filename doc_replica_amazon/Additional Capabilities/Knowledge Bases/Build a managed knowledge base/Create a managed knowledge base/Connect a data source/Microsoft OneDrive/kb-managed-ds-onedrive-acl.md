

# Document-level access controls
<a name="kb-managed-ds-onedrive-acl"></a>

OneDrive data sources optionally support document-level access control. When enabled, Bedrock Managed Knowledge Base syncs access control lists (ACLs) from OneDrive during each crawl and verifies each user's permissions at query time, so users only see results from documents they are authorized to access in OneDrive. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide. Therefore, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

## How it works
<a name="kb-managed-ds-onedrive-acl-how"></a>

When a user queries a knowledge base that uses an ACL-enabled OneDrive data source, Bedrock Managed Knowledge Base enforces access controls in two stages:
+ **Pre-retrieval filtering** — Bedrock Managed Knowledge Base applies the access control lists that were synced from OneDrive during the last crawl, returning only candidate documents the user (or their groups) is permitted to access.
+ **Real-time verification** — Bedrock Managed Knowledge Base verifies the candidate documents in real time by checking the querying user's current access in OneDrive. Only documents the user is currently authorized to access are included in the response.

This two-stage approach provides document-level access control that stays current even when OneDrive permissions change between syncs.

## What is crawled
<a name="kb-managed-ds-onedrive-acl-crawl"></a>

When ACLs are enabled, Bedrock Managed Knowledge Base crawls file-level sharing permissions and security group assignments from OneDrive. Nested (transitive) group memberships are also resolved.

At query time you pass the user's email address (not a group). Bedrock Managed Knowledge Base resolves that user's group memberships from the data it crawled and applies them when filtering results. For more information about the identity model, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## Prerequisites for ACL awareness
<a name="kb-managed-ds-onedrive-acl-prereqs"></a>

ACL-enabled OneDrive uses two different Microsoft APIs, each with its own application-permission set on your Microsoft Entra application: the crawl uses the Microsoft Graph API, and real-time verification uses the SharePoint REST API (OneDrive for Business is backed by SharePoint). Configure the permissions for both APIs, with admin consent, before you enable ACL awareness.
+ `User.Read.All` and `GroupMember.Read.All` on Microsoft Graph (for identity crawling).
+ `Sites.FullControl.All` on SharePoint (for document access verification). `Sites.Read.All` is not sufficient — read-only access cannot perform the effective-permission check that real-time verification requires.

**Important**  
The crawl uses the Microsoft Graph API and real-time verification uses the SharePoint REST API — different resources with different application permissions. The Microsoft Graph identity-crawling permissions are necessary but not sufficient: real-time verification additionally requires the SharePoint `Sites.FullControl.All` permission with admin consent. Granting only the Microsoft Graph permissions is the most common cause of an ACL-enabled OneDrive data source returning no results even when the user has access.

For the full setup procedure, including the certificate, see [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md).

## Enable ACL awareness
<a name="kb-managed-ds-onedrive-acl-enable"></a>

To enable ACL awareness for a OneDrive data source, set `aclEnabled` to `true` in the `connectorParameters` and use the `ENTRA_APP_ID` auth type. This auth type uses application permissions that allow Bedrock Managed Knowledge Base to crawl identity information and verify document access at query time.

**Important**  
ACL configuration is permanent. You cannot enable ACLs on a data source created without ACL support, and you cannot disable ACLs once enabled.

When ACLs are enabled for OneDrive, you must include a `certificateS3Path` in the `connectionConfiguration` pointing to a PKCS\#12 (`.p12`) certificate file in Amazon S3. This certificate is used for real-time ACL verification against the SharePoint REST API. The `certificateS3Path` is not required when ACLs are disabled.

```
"connectorParameters": {
    "type": "ONEDRIVE",
    "version": "1",
    "aclEnabled": true,
    "connectionConfiguration": {
        "tenantId": "{{your-tenant-id}}",
        "authType": "ENTRA_APP_ID",
        "secretArn": "{{arn:aws:secretsmanager:region:account-id:secret:secret-name}}",
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

**Note**  
The `certificatePassword` field in the secret is optional. If you omit it, Bedrock Managed Knowledge Base opens the PKCS\#12 (`.p12`) file using your application's client ID as the password, so the certificate must have been created with that password. We recommend that you always set an explicit, high-entropy `certificatePassword` to protect the certificate's private key at rest.

**Note**  
The `OAUTH2` auth type is not supported for ACL-enabled OneDrive data sources. You must use `ENTRA_APP_ID`.

## Real-time access verification
<a name="kb-managed-ds-onedrive-acl-realtime"></a>

Bedrock Managed Knowledge Base verifies each candidate document in real time entirely server-side, using application credentials — there is no end-user sign-in or delegated consent. Because OneDrive for Business is backed by SharePoint, Bedrock Managed Knowledge Base checks the querying user's effective permissions against the SharePoint REST API for your tenant's OneDrive host.

OneDrive real-time verification uses a two-credential model, and both credentials are required:
+ The client ID and client secret in your AWS Secrets Manager secret mint a Microsoft Graph token that is used to resolve your tenant's OneDrive host (the `-my.sharepoint.com` host).
+ The certificate from `certificateS3Path` mints the SharePoint REST token used for the permission check itself. The certificate is the authoritative credential for real-time verification — a client-secret token alone cannot perform the check.

**Important**  
The application must hold the SharePoint `Sites.FullControl.All` permission with admin consent; `Sites.Read.All` is not sufficient because the effective-permission check requires manage/full-control rights. Without the correct permission, real-time verification cannot evaluate effective permissions and fails closed, denying every document for every query — even when the user has access and the crawl and pre-retrieval filtering succeeded. See [Prerequisites for ACL awareness](#kb-managed-ds-onedrive-acl-prereqs).

**Note**  
After you grant or consent to the SharePoint application permission, allow up to one hour for the change to take effect for users checked before the change, because the application access credentials are cached. To confirm the change sooner, test with a different user who has not yet been queried.

## Verify your configuration
<a name="kb-managed-ds-onedrive-acl-verify"></a>

You can validate your Entra application permissions independently of a retrieve request. Perform each of the following checks:

1. **Microsoft Graph (crawl)**:
   + Acquire an application token with scope `https://graph.microsoft.com/.default`.
   + Decode the token and confirm the `roles` claim includes the required Microsoft Graph permissions (`User.Read.All`, `GroupMember.Read.All`, and `Files.Read.All`).
   + Call `GET https://graph.microsoft.com/v1.0/users/{user}/drive/root/children` and confirm it lists the user's drive items.

1. **SharePoint REST (real-time verification)**:
   + Acquire a token using the certificate client assertion with scope `https://{tenant}-my.sharepoint.com/.default`.
   + Confirm the token's `roles` claim includes the SharePoint `Sites.FullControl.All` permission. A `roles: null` value means the permission or admin consent is missing.
   + Call `GET https://{tenant}-my.sharepoint.com/_api/web` and confirm it succeeds (HTTP 200). A failed or unauthorized response means the SharePoint permission or admin consent is missing, which causes all documents to be denied.

**Note**  
After you fix the permission, the SharePoint call succeeds immediately at the token level, but an end-to-end retrieve for an already-tested user can still lag by the cache TTL described in [Real-time access verification](#kb-managed-ds-onedrive-acl-realtime). Do not conclude the fix failed based on a cached user.

## Troubleshooting
<a name="kb-managed-ds-onedrive-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the verification checks above to diagnose these issues.


**ACL-enabled OneDrive symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results, but the user has access in OneDrive. | Microsoft Graph permissions are present, but the SharePoint application permission or admin consent is missing, so the SharePoint REST call is rejected and every document is denied. | Grant the SharePoint Sites.FullControl.All permission with admin consent. Because these application credentials are cached, allow up to one hour for the change to take effect, or test with a not-yet-queried user to confirm sooner. | 
| A user's access was changed in OneDrive, but the new result is not reflected immediately. | Per-user access results are eventually consistent between the data source and Bedrock Managed Knowledge Base (typically within about two minutes), so a recent access change may not be reflected immediately. | After the data source reflects the change, wait about two minutes and retry. | 
| All users are denied after previously working. | The certificate expired, or admin consent was revoked. | Renew the certificate in the Entra app registration and in Amazon S3, and re-grant admin consent. | 
| Crawl or sync fails although the configuration looks correct. | A required Microsoft Graph application permission is missing. | Grant Files.Read.All, Sites.Read.All, User.Read.All, and GroupMember.Read.All. | 
| Certificate password or token-minting errors. | The .p12 password does not match certificatePassword. | Set certificatePassword to the password used to create the .p12 file. | 