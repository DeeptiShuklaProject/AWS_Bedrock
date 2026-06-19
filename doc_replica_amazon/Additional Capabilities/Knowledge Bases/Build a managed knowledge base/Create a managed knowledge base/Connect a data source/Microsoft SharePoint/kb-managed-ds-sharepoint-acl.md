

# Document-level access controls
<a name="kb-managed-ds-sharepoint-acl"></a>

SharePoint data sources optionally support document-level access control. When enabled, Bedrock Managed Knowledge Base syncs access control lists (ACLs) from SharePoint during each crawl and verifies each user's permissions at query time, so users only see results from documents they are authorized to access in SharePoint. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

## How it works
<a name="kb-managed-ds-sharepoint-acl-how"></a>

When a user queries a knowledge base that uses an ACL-enabled SharePoint data source, Bedrock Managed Knowledge Base enforces access controls in two stages:
+ **Pre-retrieval filtering** — Bedrock Managed Knowledge Base applies the access control lists that were synced from SharePoint during the last crawl, returning only candidate documents the user (or their groups) is permitted to access.
+ **Real-time verification** — Bedrock Managed Knowledge Base verifies the candidate documents in real time by checking the querying user's current access in SharePoint. Only documents the user is currently authorized to access are included in the response.

This two-stage approach provides document-level access control that stays current even when SharePoint permissions change between syncs.

## What is crawled
<a name="kb-managed-ds-sharepoint-acl-crawl"></a>

When ACLs are enabled, Bedrock Managed Knowledge Base crawls the following permission structures from SharePoint:
+ Site-level memberships and role assignments
+ Document library-level permissions
+ Item-level (file and page) permissions, including unique permissions that break inheritance
+ Security group memberships, including Microsoft Entra ID (Azure AD) security groups, mail-enabled security groups, and distribution groups. Nested (transitive) group memberships are also resolved.

At query time you pass the user's email address (not a group). Bedrock Managed Knowledge Base resolves that user's group memberships from the data it crawled and applies them when filtering results. For more information about the identity model, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## Enable ACL awareness
<a name="kb-managed-ds-sharepoint-acl-enable"></a>

To enable ACL awareness for a SharePoint data source, set `aclEnabled` to `true` in the `connectorParameters` and use the `ENTRA_ID_APP_ONLY` auth type. This auth type uses certificate-based application permissions that allow Bedrock Managed Knowledge Base to crawl identity information and verify document access at query time.

**Important**  
ACL configuration is permanent. You cannot enable ACLs on a data source created without ACL support, and you cannot disable ACLs once enabled.

Your Entra ID app registration must have the following application permissions:
+ `User.Read.All` and `GroupMember.Read.All` on Microsoft Graph (for identity crawling)
+ `Sites.FullControl.All` on SharePoint, or `Sites.Selected` with per-site permissions granted (for document access verification)

The `connectionConfiguration` must include a `certificateS3Path` pointing to a PKCS\#12 (.p12) certificate file in Amazon S3.

**Note**  
The `certificatePassword` field in the secret is optional. If you omit it, Bedrock Managed Knowledge Base opens the PKCS\#12 (.p12) file using your application's client ID as the password, so the certificate must have been created with that password. We recommend that you always set an explicit, high-entropy `certificatePassword` to protect the certificate's private key at rest.

```
"connectorParameters": {
    "type": "SHAREPOINT",
    "version": "1",
    "aclEnabled": true,
    "connectionConfiguration": {
        "tenantId": "{{your-tenant-id}}",
        "authType": "ENTRA_ID_APP_ONLY",
        "secretArn": "{{arn:aws:secretsmanager:region:account-id:secret:secret-name}}",
        "certificateS3Path": {
            "s3BucketName": "{{your-certificate-bucket}}",
            "s3KeyName": "{{certs/certificate.p12}}"
        }
    },
    "dataEntityConfiguration": {
        "siteUrls": [
            "{{https://contoso.sharepoint.com/sites/engineering}}"
        ],
        "crawlFiles": true,
        "crawlPages": true
    }
}
```

**Note**  
The `OAUTH2_APP` auth type is not supported for ACL-enabled SharePoint data sources. You must use `ENTRA_ID_APP_ONLY`.

## Real-time access verification
<a name="kb-managed-ds-sharepoint-acl-realtime"></a>

Bedrock Managed Knowledge Base verifies each candidate document against SharePoint at query time using the application's certificate-based permissions (the `ENTRA_ID_APP_ONLY` app registration configured for crawling). Unlike a delegated user sign-in flow, no interactive per-user sign-in or consent is required — verification uses the same app registration and certificate, through the `Sites.FullControl.All` or `Sites.Selected` permission, to confirm the querying user still has access to each document.

## Verify your configuration
<a name="kb-managed-ds-sharepoint-acl-verify"></a>

You can validate your Entra application permissions independently of a retrieve request. Perform each of the following checks:

1. **Microsoft Graph (crawl)**:
   + Acquire an application token with scope `https://graph.microsoft.com/.default` and confirm the `roles` claim includes `User.Read.All` and `GroupMember.Read.All`.
   + Call a Microsoft Graph site endpoint (for example, `GET https://graph.microsoft.com/v1.0/sites/{site}`) and confirm it returns the site.

1. **SharePoint REST (real-time verification)**:
   + Acquire a token using the certificate client assertion with scope `https://{tenant}.sharepoint.com/.default`.
   + Confirm the token's `roles` claim includes the SharePoint `Sites.FullControl.All` (or `Sites.Selected`) permission. A `roles: null` value means the permission or admin consent is missing.
   + Call `GET https://{tenant}.sharepoint.com/_api/web` and confirm it succeeds (HTTP 200). A failed or unauthorized response means the SharePoint permission or admin consent is missing, which causes all documents to be denied.

## Troubleshooting
<a name="kb-managed-ds-sharepoint-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the preceding verification checks to diagnose these issues.


**ACL-enabled SharePoint symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results, but the user has access in SharePoint. | The SharePoint Sites.FullControl.All (or Sites.Selected) permission or admin consent is missing, so the SharePoint REST call is rejected and every document is denied. | Grant the SharePoint Sites.FullControl.All permission (or Sites.Selected with per-site grants) with admin consent. Because these application credentials are cached, allow up to one hour for the change to take effect, or test with a not-yet-queried user to confirm sooner. | 
| A user's access was changed in SharePoint, but the new result is not reflected immediately. | Per-user access results are eventually consistent between the data source and Bedrock Managed Knowledge Base (typically within about two minutes), so a recent access change may not be reflected immediately. | After the data source reflects the change, wait about two minutes and retry. | 
| All users are denied after previously working. | The certificate expired, or admin consent was revoked. | Renew the certificate in the Entra app registration and in Amazon S3, and re-grant admin consent. | 
| Crawl or sync fails although the configuration looks correct. | A required Microsoft Graph application permission is missing. | Grant User.Read.All and GroupMember.Read.All. | 
| Certificate password or token-minting errors. | The .p12 password does not match certificatePassword. | Set certificatePassword to the password used to create the .p12 file. | 