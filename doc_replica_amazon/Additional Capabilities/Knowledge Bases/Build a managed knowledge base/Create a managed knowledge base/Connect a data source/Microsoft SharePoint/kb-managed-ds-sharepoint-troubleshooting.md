

# Troubleshoot a SharePoint data source
<a name="kb-managed-ds-sharepoint-troubleshooting"></a>

Use this page to diagnose common issues with SharePoint authentication, data source creation, and syncing. For issues specific to document-level access control, see the troubleshooting table in [Document-level access controls](kb-managed-ds-sharepoint-acl.md).

## Data source creation and connection errors
<a name="kb-managed-ds-sharepoint-troubleshooting-create"></a>


**Creation and connection errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| The data source fails immediately with an error that connectionConfiguration.certificateS3Path must not be null. | The authType is ENTRA\_ID\_APP\_ONLY but no certificate path was provided. This auth type always requires a certificate, even when ACLs are disabled. | Add certificateS3Path to connectionConfiguration, pointing to your .p12 certificate in Amazon S3. See [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md). | 
| Invalid tenant ID. | The tenant ID is malformed or does not match your Microsoft Entra tenant. | Copy the Directory (tenant) ID from the application Overview page in the Microsoft Entra admin center. | 
| Invalid client ID, or the application cannot be found. | The clientId in the secret is incorrect, or the app registration does not exist. | Copy the Application (client) ID from the application Overview page and update the secret. | 
| Unable to connect to SharePoint. | One or more credentials are incorrect, or the application is missing required permissions or admin consent. | Verify the secret values, confirm the application permissions, and grant admin consent. See [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md). | 
| The knowledge base service role cannot read the certificate. | The service role is missing s3:GetObject on the certificate object, or the object is encrypted with a customer managed key the role cannot use. | Grant s3:GetObject on the certificate, and if the object uses a customer managed KMS key, grant kms:Decrypt on that key. See [Step 8: Grant the service role access to the certificate](kb-managed-sharepoint-entra-setup.md#kb-managed-sharepoint-entra-step8). | 

## Certificate errors (Microsoft Entra ID App-Only)
<a name="kb-managed-ds-sharepoint-troubleshooting-cert"></a>


**Certificate errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Certificate password or token-minting errors during sync. | The .p12 password does not match the certificatePassword in the secret. | Set certificatePassword to the password used to create the .p12 file, or recreate the bundle with a known password. | 
| Authentication worked before and now all syncs fail. | The certificate expired, or admin consent was revoked. | Generate a new certificate, upload the public certificate to the Entra app registration, replace the .p12 in Amazon S3, and re-grant admin consent. | 
| Sync fails with an error that the certificate could not be loaded as X.509 or PKCS\#12 (for example, "Invalid certificate format — failed to load as X.509 or PKCS12"). | Amazon Bedrock could not read the certificate in Amazon S3 with the credentials provided. Common reasons include a missing or blank certificatePassword in the secret, a certificateS3Path that points to the wrong object (for example, a .cer/PEM file or a leftover object), or a certificate that no longer matches the secret. This is more likely after reconfiguring a data source or switching authentication methods. | Confirm the secret referenced by the data source includes a certificatePassword that matches your .p12 bundle, and that certificateS3Path points to that .p12. If you reconfigured the data source, verify the certificate and secret still correspond, then sync again. | 

## Rotate the certificate
<a name="kb-managed-ds-sharepoint-rotate-cert"></a>

Rotate the certificate before it expires. An expired certificate causes all syncs to fail. To rotate without interrupting access, upload the new certificate as a separate object and switch the data source to it, so the existing certificate keeps working until you cut over.

1. Generate a new certificate and PKCS\#12 (`.p12`) bundle, as described in [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md).

1. In your Entra app registration, under **Certificates & secrets**, upload the new public certificate. Leave the existing certificate in place — an app registration can hold multiple certificates.

1. Upload the new `.p12` bundle to Amazon S3 under a **new object key** (do not overwrite the existing certificate object). Confirm your knowledge base service role can read the new object.

1. Update the data source so that `certificateS3Path` points to the new object, and update the `certificatePassword` in your AWS Secrets Manager secret to match the new bundle. Use the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console.

1. Start a sync and confirm it completes successfully with the new certificate.

1. After the sync succeeds, remove the old certificate from the Entra app registration and delete the old `.p12` object from Amazon S3.

## OAuth 2.0 authentication errors
<a name="kb-managed-ds-sharepoint-troubleshooting-oauth2"></a>


**OAuth 2.0 errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Sync fails with a message that the REST API token request failed with status 400. | The account requires MFA or Conditional Access, which the resource-owner password credentials flow cannot satisfy; or the secret is missing the userName or password field. | Confirm the secret includes clientId, clientSecret, userName, and password. If the account enforces MFA or Conditional Access, switch to [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md). | 
| Sync fails after the account password changed. | The stored password is no longer valid. | Update the password field in the secret. | 

## Sync errors
<a name="kb-managed-ds-sharepoint-troubleshooting-sync"></a>


**Sync errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| The sync completes but no documents are indexed. | The application cannot access the configured sites. With Sites.Selected, per-site permissions might not be granted. | Verify the application permissions and admin consent. If you use Sites.Selected, confirm a per-site grant for each site. See [Step 5 (Sites.Selected only): Grant per-site access](kb-managed-sharepoint-entra-setup.md#kb-managed-sharepoint-entra-step5). | 
| A newly added site is not crawled (Sites.Selected). | Per-site grants are not retroactive, so the new site has no grant. | Grant the connector application access to the new site, then sync again. | 
| Specific paths return no results. | The path was entered as a browser URL, or the item was moved or renamed in SharePoint. | Use the SharePoint path (not the browser URL), and verify the item still exists at that path. | 

## Document-level access control issues
<a name="kb-managed-ds-sharepoint-troubleshooting-acl"></a>

ACL misconfigurations do not produce explicit errors during retrieval. Instead, queries return fewer or zero results. For ACL-specific symptoms, verification steps, and fixes, see [Document-level access controls](kb-managed-ds-sharepoint-acl.md).