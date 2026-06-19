

# Troubleshoot a OneDrive data source
<a name="kb-managed-ds-onedrive-troubleshooting"></a>

Use this page to diagnose common issues with OneDrive authentication, data source creation, and syncing. For issues specific to document-level access control, see the troubleshooting table in [Document-level access controls](kb-managed-ds-onedrive-acl.md).

## Data source creation and connection errors
<a name="kb-managed-ds-onedrive-troubleshooting-create"></a>


**Creation and connection errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| The data source fails to create with an error that certificateS3Path must not be null. | aclEnabled is true but no certificate path was provided. Document-level access control requires a certificate. | Add certificateS3Path to connectionConfiguration, pointing to your .p12 certificate in Amazon S3. See [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md). | 
| Invalid tenant ID. | The tenant ID is malformed or does not match your Microsoft Entra tenant. | Copy the Directory (tenant) ID from the application Overview page in the Microsoft Entra admin center. | 
| Invalid client ID, or the application cannot be found. | The clientId in the secret is incorrect, or the app registration does not exist. | Copy the Application (client) ID from the application Overview page and update the secret. | 
| Unable to connect to OneDrive. | One or more credentials are incorrect, or the application is missing required permissions or admin consent. | Verify the secret values, confirm the application permissions, and grant admin consent. See [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md). | 
| The knowledge base service role cannot read the certificate. | The service role is missing s3:GetObject on the certificate object, or the object is encrypted with a customer managed key the role cannot use. | Grant s3:GetObject on the certificate, and if the object uses a customer managed KMS key, grant kms:Decrypt on that key. See [Step 8 (ACLs only): Grant the service role access to the certificate](kb-managed-onedrive-entra-setup.md#kb-managed-onedrive-entra-step8). | 

## Certificate errors (document-level access control)
<a name="kb-managed-ds-onedrive-troubleshooting-cert"></a>


**Certificate errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Certificate password or token-minting errors during real-time access verification. | The .p12 password does not match the certificatePassword in the secret. | Set certificatePassword to the password used to create the .p12 file, or recreate the bundle with a known password. | 
| Access verification worked before and now all queries return zero results. | The certificate expired, or admin consent was revoked. | Generate a new certificate, upload the public certificate to the Entra app registration, replace the .p12 in Amazon S3, and re-grant admin consent. See [Rotate the certificate](#kb-managed-ds-onedrive-rotate-cert). | 
| An error that the certificate could not be loaded as PKCS\#12 (for example, "Invalid certificate format"). | The certificateS3Path points to the wrong object (for example, a .cer/PEM file), or the certificatePassword in the secret does not match the bundle. Document-level access control requires the .p12 format. | Confirm certificateS3Path points to your .p12 bundle and that certificatePassword matches it. | 

## Rotate the certificate
<a name="kb-managed-ds-onedrive-rotate-cert"></a>

If you use document-level access control, rotate the certificate before it expires. An expired certificate causes real-time access verification to fail closed, so queries return zero results. To rotate without interrupting access, upload the new certificate as a separate object and switch the data source to it, so the existing certificate keeps working until you cut over.

1. Generate a new certificate and PKCS\#12 (`.p12`) bundle, as described in [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md).

1. In your Entra app registration, under **Certificates & secrets**, upload the new public certificate. Leave the existing certificate in place — an app registration can hold multiple certificates.

1. Upload the new `.p12` bundle to Amazon S3 under a **new object key** (do not overwrite the existing certificate object). Confirm your knowledge base service role can read the new object.

1. Update the data source so that `certificateS3Path` points to the new object, and update the `certificatePassword` in your AWS Secrets Manager secret to match the new bundle. Use the [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) operation or the AWS Management Console.

1. Confirm that retrieval with an authorized user returns results, which shows the new certificate works for real-time verification.

1. After you confirm the new certificate works, remove the old certificate from the Entra app registration and delete the old `.p12` object from Amazon S3.

## OAuth 2.0 authentication errors
<a name="kb-managed-ds-onedrive-troubleshooting-oauth2"></a>


**OAuth 2.0 errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Sync fails with a message that the OAuth 2.0 access token could not be refreshed. | The secret is missing the refreshToken field, or the refresh token expired or was revoked. | Confirm the secret includes clientId, clientSecret, and refreshToken. If the token expired or was revoked, obtain a new one and update the secret. See [Step 4: Obtain a refresh token](kb-managed-onedrive-oauth2-setup.md#kb-managed-onedrive-oauth2-step4). | 
| You want to crawl files shared with the user or OneNote notebooks, but they are not indexed. | The data source uses Microsoft Entra App ID (application-only) authentication, which cannot access shared files or OneNote notebooks. | Use OAUTH2 authentication and enable the corresponding sync scope. See [Set up OAuth 2.0 authentication for OneDrive](kb-managed-onedrive-oauth2-setup.md). | 

## Sync errors
<a name="kb-managed-ds-onedrive-troubleshooting-sync"></a>


**Sync errors**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| The sync completes but no documents are indexed. | The application cannot access the configured users' drives, or the inclusion or exclusion filters exclude all content. | Verify the application permissions and admin consent, and review your user email and drive item filters. | 
| A specific user's content is not crawled. | The user is excluded by a filter, or the user has no accessible content. | Check the inclusionUserEmailAddresses and exclusionUserEmailAddresses filters and confirm the user has content in their drive. | 

## Document-level access control issues
<a name="kb-managed-ds-onedrive-troubleshooting-acl"></a>

ACL misconfigurations do not produce explicit errors during retrieval. Instead, queries return fewer or zero results. For ACL-specific symptoms, verification steps, and fixes, see [Document-level access controls](kb-managed-ds-onedrive-acl.md).