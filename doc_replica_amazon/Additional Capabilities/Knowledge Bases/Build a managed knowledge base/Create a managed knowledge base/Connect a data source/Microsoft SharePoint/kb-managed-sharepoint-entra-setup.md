

# Set up Microsoft Entra ID App-Only authentication for SharePoint
<a name="kb-managed-sharepoint-entra-setup"></a>

Microsoft Entra ID App-Only authentication (`ENTRA_ID_APP_ONLY`) is the recommended authentication method for a SharePoint data source. It uses the OAuth 2.0 client-credentials (application-only) flow: a Microsoft Entra application authenticates with a certificate, so no user sign-in is involved at crawl time or at query time. This is the only authentication method that supports document-level access control (ACLs). For a comparison with the alternative `OAUTH2_APP` method, see [Authentication methods](kb-managed-ds-sharepoint.md#kb-managed-sharepoint-auth-methods).

This setup spans two systems — Microsoft Entra ID and your AWS account — and the certificate is the credential that ties them together. The connector stores the certificate (private key included) as a PKCS\#12 (`.p12`) file in Amazon S3 and uses it to sign authentication assertions to Microsoft; the matching public certificate is uploaded to the Entra application registration so Microsoft can validate those assertions.

**Administrative access required**  
This setup requires a Microsoft Entra ID administrator (Global Administrator or Privileged Role Administrator) to register the application, configure permissions, and grant admin consent. If you use the `Sites.Selected` permission scope, you also need a SharePoint administrator to grant per-site access. The **Setup steps and roles** table below identifies the access required for each step.

## Setup steps and roles
<a name="kb-managed-sharepoint-entra-roles"></a>

This procedure involves both a Microsoft Entra ID administrator and an AWS administrator. Depending on how responsibilities are divided in your organization, one person or several people might complete these steps. Use the following table to identify the access each step requires.


**Setup steps and the access each one requires**  

| Step | What you do | Access needed | 
| --- | --- | --- | 
| 1. Register the application | Create the Entra app registration and record its client and tenant IDs. | Microsoft Entra ID administrator (Global Administrator or Privileged Role Administrator) | 
| 2. Add permissions and grant consent | Assign the application permissions for your configuration and grant admin consent. | Microsoft Entra ID administrator | 
| 3. Generate the certificate | Create a self-signed certificate and a PKCS\#12 (.p12) bundle with OpenSSL. | Anyone with a local terminal (OpenSSL required) | 
| 4. Upload the public certificate to Entra | Add the public certificate to the app registration's keys. | Microsoft Entra ID administrator | 
| 5. Grant per-site access (Sites.Selected only) | Grant the app access to each SharePoint site through the Microsoft Graph API. | Microsoft Entra ID administrator | 
| 6. Upload the certificate to Amazon S3 | Store the .p12 bundle in an Amazon S3 bucket. | AWS administrator (Amazon S3) | 
| 7. Create the secret | Store the credentials in an AWS Secrets Manager secret. | AWS administrator (Secrets Manager) | 
| 8. Grant the service role access to the certificate | Add Amazon S3 read permissions to your knowledge base service role. | AWS administrator (IAM) | 

## Choose your configuration
<a name="kb-managed-sharepoint-entra-choose"></a>

Before you begin, make two decisions. They determine which permissions you assign in Step 2 and how you grant site access.
+ **Document-level access control (ACLs)** — Decide whether the data source filters query results by each user's SharePoint permissions. ACL crawling requires additional Microsoft Graph and SharePoint permissions. You cannot change this setting after you create the data source. For details, see [Document-level access controls](kb-managed-ds-sharepoint-acl.md).
+ **Permission scope** — Decide whether the application can read all SharePoint sites in your tenant (**all sites**, the simplest option) or only sites you explicitly grant (**`Sites.Selected`**, the least-privilege option). With `Sites.Selected` you complete an extra per-site grant in Step 5, and any sites you add later need their own grant.

The combination of these two choices selects one of the permission sets in the following section.

## Permissions reference
<a name="kb-managed-sharepoint-entra-permissions"></a>

Assign the application permissions that match your configuration. All permissions are **application** permissions (not delegated), and every one requires admin consent. The connector authenticates to two Microsoft resources: **Microsoft Graph** (to enumerate sites and, for ACLs, to resolve users and groups) and the **SharePoint** REST API (to read site content and, for ACLs, item-level permissions).

**Important**  
When you add these permissions in the Entra portal, choose the **Application permissions** tab, not **Delegated permissions**. App-only authentication uses application permissions.

Select the tab for your configuration to see the exact Microsoft Graph and SharePoint permissions to assign.

------
#### [ All sites, no ACLs ]


**All sites, content only**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Sites.Read.All | Enumerate and read all SharePoint sites. | 
| SharePoint | Sites.Read.All | Read site content through the SharePoint REST API. | 

------
#### [ All sites, with ACLs ]


**All sites, with ACLs**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Sites.Read.All | Enumerate and read all SharePoint sites. | 
| Microsoft Graph | User.Read.All | Resolve users for document-level ACLs. | 
| Microsoft Graph | GroupMember.Read.All | Resolve group membership for document-level ACLs. | 
| SharePoint | Sites.FullControl.All | Read item-level permissions for ACL crawling and verify access at query time. Sites.Read.All is not sufficient for this check. | 

------
#### [ Sites.Selected, no ACLs ]


**Sites.Selected, content only**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Sites.Selected | Access only the sites you explicitly grant (Microsoft Graph). | 
| SharePoint | Sites.Selected | Access only the sites you explicitly grant (SharePoint REST). Grant the read role per site in Step 5. | 

------
#### [ Sites.Selected, with ACLs ]


**Sites.Selected, with ACLs**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Sites.Selected | Access only the sites you explicitly grant (Microsoft Graph). | 
| Microsoft Graph | User.Read.All | Resolve users for document-level ACLs. | 
| Microsoft Graph | GroupMember.Read.All | Resolve group membership for document-level ACLs. | 
| SharePoint | Sites.Selected | Access only the sites you explicitly grant. Grant the fullcontrol role per site in Step 5 (required to read item-level permissions for ACLs). | 

------

**Note**  
`Sites.FullControl.All` grants broad access to every site in the tenant. If your organization requires least privilege, use `Sites.Selected` and grant per-site access in Step 5.

## Values you collect during setup
<a name="kb-managed-sharepoint-entra-values"></a>

You create or collect the following values as you work through the steps. You use them when you create the data source. For details, see [Connect a SharePoint data source](kb-managed-ds-sharepoint-connect.md).


**Values reference**  

| Value | Created in | Used for | 
| --- | --- | --- | 
| Application (client) ID | Step 1 | The secret (clientId). | 
| Directory (tenant) ID | Step 1 | The data source tenantId. | 
| Certificate — PKCS\#12 bundle (.p12) and its password | Step 3 | The bundle (certificate plus private key) is uploaded to Amazon S3 (Step 6); the password is stored in the secret (certificatePassword). | 
| Certificate — public certificate (.cer) | Step 3 | The public half of the same certificate, uploaded to the Entra app registration (Step 4). | 
| Amazon S3 bucket name and key | Step 6 | The data source certificateS3Path. | 
| Secret ARN | Step 7 | The data source secretArn. | 

## Step 1: Register the application in Microsoft Entra ID
<a name="kb-managed-sharepoint-entra-step1"></a>

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

1. In the left navigation, expand **Entra ID** and choose **App registrations**.

1. Choose **New registration**.

1. For **Name**, enter a descriptive name, such as `bedrock-sharepoint-connector`.

1. For **Supported account types**, select **Accounts in this organizational directory only (Single tenant)**.

1. Leave **Redirect URI** blank. A redirect URI is not required because the application uses the client-credentials flow, not an interactive sign-in flow.

1. Choose **Register**.

1. On the application **Overview** page, record the **Application (client) ID** and the **Directory (tenant) ID**. You need both later.

## Step 2: Add API permissions and grant admin consent
<a name="kb-managed-sharepoint-entra-step2"></a>

Add the permissions for your configuration from [Permissions reference](#kb-managed-sharepoint-entra-permissions).

1. In your app registration, choose **API permissions**, then **Add a permission**.

1. Choose **Microsoft Graph**, then **Application permissions**. Search for and select each Microsoft Graph permission for your configuration, then choose **Add permissions**.

1. Choose **Add a permission** again. Choose **SharePoint** (under **Microsoft APIs**), then **Application permissions**. Select each SharePoint permission for your configuration, then choose **Add permissions**.

1. On the **API permissions** page, choose **Grant admin consent for [your organization]** and confirm. Without admin consent, the application cannot access SharePoint data.

**Note**  
Microsoft Entra ID App-Only authentication uses the certificate (from Step 3) as the credential, so you do not create a client secret for this application.

## Step 3: Generate the authentication certificate
<a name="kb-managed-sharepoint-entra-step3"></a>

Generate a self-signed certificate and package it as a PKCS\#12 (`.p12`) bundle. The bundle contains both the certificate and its private key, protected by a password. You upload the public certificate to Entra (Step 4) and the `.p12` bundle to Amazon S3 (Step 6). Select the tab for your operating system to see the commands.

**Note**  
Amazon Bedrock reads the private key from the `.p12` bundle to sign authentication assertions, so the bundle must be password-protected and stored securely. Choose a strong, random password — you store it in the secret as `certificatePassword` in Step 7.

------
#### [ Linux or macOS (OpenSSL) ]

**Generate a private key and self-signed certificate**

```
openssl req -x509 -newkey rsa:2048 -keyout private_key.pem -out certificate.cer \
    -days 365 -nodes \
    -subj "/CN={{bedrock-sharepoint-connector}}"
```

**Package the certificate and key as a PKCS\#12 (`.p12`) bundle**

Enter a strong export password when prompted. Record it for Step 7.

```
openssl pkcs12 -export -out certificate.p12 \
    -inkey private_key.pem -in certificate.cer
```

You now have three files: the private key (`private_key.pem`), the public certificate (`certificate.cer`), and the bundle (`certificate.p12`). You upload the public certificate to Entra in Step 4 and the `.p12` bundle to Amazon S3 in Step 6.

------
#### [ Windows (PowerShell) ]

**Generate a self-signed certificate**

The following PowerShell commands generate a 2048-bit RSA self-signed certificate with a one-year validity period and store it in the current user's certificate store. Replace {{your-password}} with a strong, random password — you store it in the secret as `certificatePassword` in Step 7.

```
$cert = New-SelfSignedCertificate `
    -Subject "CN={{bedrock-sharepoint-connector}}" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyAlgorithm RSA `
    -KeyLength 2048 `
    -KeyExportPolicy Exportable `
    -NotAfter (Get-Date).AddYears(1)
```

**Export the public certificate**

```
Export-Certificate -Cert $cert -FilePath certificate.cer -Type CERT
```

**Export the PKCS\#12 (`.p12`) bundle**

```
$password = ConvertTo-SecureString -String "{{your-password}}" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath certificate.p12 -Password $password
```

You now have two files: the public certificate (`certificate.cer`) and the bundle (`certificate.p12`). You upload the public certificate to Entra in Step 4 and the `.p12` bundle to Amazon S3 in Step 6.

------

**Important**  
Store the `.p12` bundle in Amazon S3 (not the `.pem` or `.cer` file). The bundle contains the private key that Amazon Bedrock uses to authenticate. Document-level access control (ACLs) requires the `.p12` format. For content-only crawling without ACLs, you can store a PEM-encoded certificate instead; because `.p12` works for every configuration, this guide uses `.p12` throughout.

**Note**  
The certificate is valid for one year by default. An expired certificate causes all syncs to fail, so rotate the certificate before it expires. To change the validity period, adjust the `-days` option (OpenSSL) or the `-NotAfter` argument (PowerShell). For the rotation steps, see [Rotate the certificate](kb-managed-ds-sharepoint-troubleshooting.md#kb-managed-ds-sharepoint-rotate-cert).

## Step 4: Upload the public certificate to Entra
<a name="kb-managed-sharepoint-entra-step4"></a>

1. In your app registration, choose **Certificates & secrets**, then the **Certificates** tab.

1. Choose **Upload certificate** and select the `certificate.cer` file you generated in Step 3 (the public certificate only — never upload the `.p12` bundle or the private key to Entra).

1. Choose **Add**.

## Step 5 (Sites.Selected only): Grant per-site access
<a name="kb-managed-sharepoint-entra-step5"></a>

**Note**  
This step applies only if you chose the `Sites.Selected` permission scope in Step 2. If you used the all-sites scope (`Sites.Read.All` or `Sites.FullControl.All`), skip to [Step 6: Upload the certificate to Amazon S3](#kb-managed-sharepoint-entra-step6).

With `Sites.Selected`, you grant your connector application access to each SharePoint site individually through the Microsoft Graph API. This requires a separate, temporary application that holds `Sites.FullControl.All` and is used only to perform the grants. Amazon Bedrock never sees this temporary application or its credentials.

1. **Create a temporary granter application.** In the Entra admin center, register a second application (for example, `bedrock-sharepoint-granter`) as single-tenant with no redirect URI. Add the Microsoft Graph `Sites.FullControl.All` application permission, grant admin consent, and create a client secret. Record its client ID and secret value.

1. **Get an access token for the granter application.** Replace the placeholders with the granter application's client ID and secret, and your tenant ID.

   ```
   curl -s -X POST \
     "https://login.microsoftonline.com/{{TENANT_ID}}/oauth2/v2.0/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials" \
     -d "client_id={{GRANTER_CLIENT_ID}}" \
     -d "client_secret={{GRANTER_CLIENT_SECRET}}" \
     -d "scope=https://graph.microsoft.com/.default"
   ```

   The response contains an `access_token`. Use it as the bearer token in the next commands.

1. **Resolve each site URL to a site ID.** Use the site's hostname and server-relative path.

   ```
   curl -s \
     "https://graph.microsoft.com/v1.0/sites/{{contoso}}.sharepoint.com:/sites/{{engineering}}" \
     -H "Authorization: Bearer {{ACCESS_TOKEN}}"
   ```

   The `id` field in the response is the site ID.

1. **Grant the connector application access to the site.** Use `read` for content-only crawling or `fullcontrol` for ACL crawling. Replace {{CONNECTOR\_CLIENT\_ID}} with the application (client) ID from Step 1.

   ```
   curl -s -X POST \
     "https://graph.microsoft.com/v1.0/sites/{{SITE_ID}}/permissions" \
     -H "Authorization: Bearer {{ACCESS_TOKEN}}" \
     -H "Content-Type: application/json" \
     -d '{
       "roles": ["{{fullcontrol}}"],
       "grantedToIdentities": [{
         "application": {
           "id": "{{CONNECTOR_CLIENT_ID}}",
           "displayName": "{{bedrock-sharepoint-connector}}"
         }
       }]
     }'
   ```

1. Repeat the resolve-and-grant commands for every site you include in the data source. After you finish, you can delete the temporary granter application; the per-site grants remain in effect.

**Important**  
Per-site grants are not retroactive. If you add a site to the data source later, grant the connector application access to that site before the next sync, or its content is not crawled.

## Step 6: Upload the certificate to Amazon S3
<a name="kb-managed-sharepoint-entra-step6"></a>

Upload the `.p12` bundle from Step 3 to an Amazon S3 bucket in the same AWS Region as your knowledge base. Record the bucket name and key — you use them as the data source `certificateS3Path`.

```
aws s3api put-object \
  --bucket {{your-certificate-bucket}} \
  --key {{certs/certificate.p12}} \
  --body certificate.p12 \
  --server-side-encryption AES256
```

**Note**  
We recommend that you enable server-side encryption on the certificate object and restrict the bucket to the principals that need it. The bundle contains the private key.

## Step 7: Create the Secrets Manager secret
<a name="kb-managed-sharepoint-entra-step7"></a>

Store the credentials in an AWS Secrets Manager secret. For Entra ID App-Only authentication, include the following key-value pairs:
+ `clientId` (required) — the application (client) ID from Step 1.
+ `certificatePassword` (recommended) — the password you set on the `.p12` bundle in Step 3. See the note that follows.

```
{
    "clientId": "{{your-client-id}}",
    "certificatePassword": "{{your-certificate-password}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-sharepoint-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
Set `certificatePassword` to the password you used when you created the `.p12` bundle in Step 3. If you omit this field, Amazon Bedrock opens the bundle using your application's client ID as the password, so the bundle must have been created with the client ID as its password. We recommend that you always set an explicit, high-entropy password instead, and store the private key securely.

**Note**  
**Using a PEM certificate instead.** This guide uses a `.p12` bundle, which works for every configuration. If you crawl content only (no document-level access control), you can use a PEM certificate instead. In that case, upload only the *public* certificate to Amazon S3 (not a `.p12` bundle), and store the private key in the secret as `privateKey` (unencrypted base64-encoded PKCS\#8, with no header lines) in place of `certificatePassword`:  

```
{
    "clientId": "{{your-client-id}}",
    "privateKey": "{{your-base64-pkcs8-private-key}}"
}
```

## Step 8: Grant the service role access to the certificate
<a name="kb-managed-sharepoint-entra-step8"></a>

Your knowledge base service role must be able to read the certificate object from Amazon S3. Add the following statement to the role's permissions policy, replacing the bucket name and key with your values.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ListCertificateBucket",
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": ["arn:aws:s3:::{{your-certificate-bucket}}"],
            "Condition": {
                "StringEquals": { "aws:ResourceAccount": ["{{123456789012}}"] }
            }
        },
        {
            "Sid": "S3GetCertificate",
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": [
                "arn:aws:s3:::{{your-certificate-bucket}}/{{certs/certificate.p12}}",
                "arn:aws:s3:::{{your-certificate-bucket}}/{{certs/certificate.p12}}.metadata.json"
            ],
            "Condition": {
                "StringEquals": { "aws:ResourceAccount": ["{{123456789012}}"] }
            }
        }
    ]
}
```

**Note**  
The policy also allows read access to an optional `.metadata.json` file alongside the certificate. Amazon Bedrock does not require this file; including the permission prevents access errors if one is present.

**If the certificate object is encrypted with an AWS KMS key**

The upload command in [Step 6: Upload the certificate to Amazon S3](#kb-managed-sharepoint-entra-step6) uses Amazon S3-managed encryption (`AES256`), which needs no additional permissions. If instead you encrypt the certificate object with Amazon S3 server-side encryption using a customer managed KMS key (SSE-KMS), the service role also needs `kms:Decrypt` permission on that key, and the key's policy must allow the role to use it. Objects encrypted with the AWS managed `aws/s3` key do not require this additional grant.

```
{
    "Sid": "KmsDecryptCertificate",
    "Effect": "Allow",
    "Action": ["kms:Decrypt"],
    "Resource": ["arn:aws:kms:{{us-west-2}}:{{123456789012}}:key/{{your-key-id}}"]
}
```

Read access requires only `kms:Decrypt`. For more information, see [Using server-side encryption with AWS KMS keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).

For the complete set of knowledge base service role permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## Next steps
<a name="kb-managed-sharepoint-entra-next"></a>

You now have everything you need to create the data source: the secret ARN, your tenant ID, and the Amazon S3 location of the certificate. To create the SharePoint data source with the AWS Management Console or the API, see [Connect a SharePoint data source](kb-managed-ds-sharepoint-connect.md).

**Important**  
For `ENTRA_ID_APP_ONLY` authentication, you must provide `certificateS3Path` when you create the data source, even when ACLs are disabled. A SharePoint data source created with this auth type and no certificate fails.