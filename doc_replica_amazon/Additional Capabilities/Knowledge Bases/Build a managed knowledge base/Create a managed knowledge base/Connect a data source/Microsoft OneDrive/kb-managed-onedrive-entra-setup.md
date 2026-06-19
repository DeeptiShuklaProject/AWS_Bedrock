

# Set up Microsoft Entra App ID authentication for OneDrive
<a name="kb-managed-onedrive-entra-setup"></a>

Microsoft Entra App ID authentication (`ENTRA_APP_ID`) is the recommended authentication method for a OneDrive data source. The connector crawls content with the OAuth 2.0 client-credentials (application-only) flow, using your application's client ID and secret — no user sign-in is involved. This is the only authentication method that supports document-level access control (ACLs). For a comparison with the alternative `OAUTH2` method, see [Authentication methods](kb-managed-ds-onedrive.md#kb-managed-onedrive-auth-methods).

**Note**  
A certificate is required only when you enable document-level access control. For content-only crawling, the client ID and secret are the only credentials the connector needs. This differs from a SharePoint data source, where Microsoft Entra ID App-Only authentication always requires a certificate.

**Administrative access required**  
This setup requires a Microsoft Entra ID administrator (Global Administrator or Privileged Role Administrator) to register the application, configure permissions, and grant admin consent. The **Setup steps and roles** table below identifies the access required for each step.

## Setup steps and roles
<a name="kb-managed-onedrive-entra-roles"></a>

This procedure involves both a Microsoft Entra ID administrator and an AWS administrator. Depending on how responsibilities are divided in your organization, one person or several people might complete these steps. The certificate steps (Steps 4–6 and 8) apply only when you enable document-level access control. Use the following table to identify the access each step requires.


**Setup steps and the access each one requires**  

| Step | What you do | Access needed | 
| --- | --- | --- | 
| 1. Register the application | Create the Entra app registration and record its client and tenant IDs. | Microsoft Entra ID administrator (Global Administrator or Privileged Role Administrator) | 
| 2. Add permissions and grant consent | Assign the application permissions for your configuration and grant admin consent. | Microsoft Entra ID administrator | 
| 3. Create a client secret | Create a client secret for the application and record its value. | Microsoft Entra ID administrator | 
| 4. Generate the certificate (ACLs only) | Create a self-signed certificate and a PKCS\#12 (.p12) bundle with OpenSSL. | Anyone with a local terminal (OpenSSL required) | 
| 5. Upload the public certificate to Entra (ACLs only) | Add the public certificate to the app registration's keys. | Microsoft Entra ID administrator | 
| 6. Upload the certificate to Amazon S3 (ACLs only) | Store the .p12 bundle in an Amazon S3 bucket. | AWS administrator (Amazon S3) | 
| 7. Create the secret | Store the credentials in an AWS Secrets Manager secret. | AWS administrator (Secrets Manager) | 
| 8. Grant the service role access to the certificate (ACLs only) | Add Amazon S3 read permissions to your knowledge base service role. | AWS administrator (IAM) | 

## Permissions reference
<a name="kb-managed-onedrive-entra-permissions"></a>

Assign the application permissions that match your configuration. All permissions are **application** permissions (not delegated), and every one requires admin consent. For content-only crawling, the connector authenticates only to **Microsoft Graph**. When document-level access control is enabled, the connector additionally authenticates to the **SharePoint** REST API to verify access at query time, because OneDrive for Business is backed by SharePoint.

**Important**  
When you add these permissions in the Entra portal, choose the **Application permissions** tab, not **Delegated permissions**. Application-only authentication uses application permissions.

Select the tab for your configuration to see the exact permissions to assign.

------
#### [ Content only (no ACLs) ]


**Content only**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Files.Read.All | Read the files in users' drives. | 
| Microsoft Graph | Sites.Read.All | Read the OneDrive sites that back users' drives. | 
| Microsoft Graph | User.Read.All | Enumerate the users whose drives you crawl. | 

------
#### [ With ACLs ]


**With ACLs**  

| API | Permission | Purpose | 
| --- | --- | --- | 
| Microsoft Graph | Files.Read.All | Read the files in users' drives. | 
| Microsoft Graph | Sites.Read.All | Read the OneDrive sites that back users' drives. | 
| Microsoft Graph | User.Read.All | Enumerate users and resolve them for document-level ACLs. | 
| Microsoft Graph | GroupMember.Read.All | Resolve group membership for document-level ACLs. | 
| SharePoint | Sites.FullControl.All | Verify each user's access to a document at query time. Sites.Read.All is not sufficient for this check. | 

------

**Note**  
The SharePoint `Sites.FullControl.All` permission grants the connector application broad access across the sites in your tenant. Grant it only to this application, and protect the application's credentials accordingly.

## Values you collect during setup
<a name="kb-managed-onedrive-entra-values"></a>

You create or collect the following values as you work through the steps. You use them when you create the data source. For details, see [Connect a OneDrive data source](kb-managed-ds-onedrive-connect.md).


**Values reference**  

| Value | Created in | Used for | 
| --- | --- | --- | 
| Application (client) ID | Step 1 | The secret (clientId). | 
| Directory (tenant) ID | Step 1 | The data source tenantId. | 
| Client secret value | Step 3 | The secret (clientSecret). | 
| Certificate — PKCS\#12 bundle (.p12) and its password (ACLs only) | Step 4 | The bundle (certificate plus private key) is uploaded to Amazon S3 (Step 6); the password is stored in the secret (certificatePassword). | 
| Certificate — public certificate (.cer) (ACLs only) | Step 4 | The public half of the same certificate, uploaded to the Entra app registration (Step 5). | 
| Amazon S3 bucket name and key (ACLs only) | Step 6 | The data source certificateS3Path. | 
| Secret ARN | Step 7 | The data source secretArn. | 

## Step 1: Register the application in Microsoft Entra ID
<a name="kb-managed-onedrive-entra-step1"></a>

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

1. In the left navigation, expand **Entra ID** and choose **App registrations**.

1. Choose **New registration**.

1. For **Name**, enter a descriptive name, such as `bedrock-onedrive-connector`.

1. For **Supported account types**, select **Accounts in this organizational directory only (Single tenant)**.

1. Leave **Redirect URI** blank. A redirect URI is not required because the application uses the client-credentials flow, not an interactive sign-in flow.

1. Choose **Register**.

1. On the application **Overview** page, record the **Application (client) ID** and the **Directory (tenant) ID**. You need both later.

## Step 2: Add API permissions and grant admin consent
<a name="kb-managed-onedrive-entra-step2"></a>

Add the permissions for your configuration from [Permissions reference](#kb-managed-onedrive-entra-permissions).

1. In your app registration, choose **API permissions**, then **Add a permission**.

1. Choose **Microsoft Graph**, then **Application permissions**. Search for and select each Microsoft Graph permission for your configuration, then choose **Add permissions**.

1. If you are enabling document-level access control, choose **Add a permission** again. Choose **SharePoint** (under **Microsoft APIs**), then **Application permissions**. Select `Sites.FullControl.All`, then choose **Add permissions**.

1. On the **API permissions** page, choose **Grant admin consent for [your organization]** and confirm. Without admin consent, the application cannot access OneDrive data.

## Step 3: Create a client secret
<a name="kb-managed-onedrive-entra-step3"></a>

OneDrive crawling uses the application's client ID and secret, so a client secret is required for both content-only and ACL-enabled data sources. When document-level access control is enabled, the connector uses the client secret to obtain a Microsoft Graph token that resolves your tenant's OneDrive host, and the certificate (from Step 4) to obtain the SharePoint token used for the access check.

1. In your app registration, choose **Certificates & secrets**, then **Client secrets**, then **New client secret**.

1. Enter a description, choose an expiration, and choose **Add**.

1. Record the secret **Value** immediately — it is shown only once. Record the **Value**, not the **Secret ID**.

## Step 4 (ACLs only): Generate the authentication certificate
<a name="kb-managed-onedrive-entra-step4"></a>

**Note**  
This step and Steps 5, 6, and 8 apply only if you enable document-level access control. For content-only crawling, skip to [Step 7: Create the Secrets Manager secret](#kb-managed-onedrive-entra-step7).

Generate a self-signed certificate and package it as a PKCS\#12 (`.p12`) bundle. The bundle contains both the certificate and its private key, protected by a password. You upload the public certificate to Entra (Step 5) and the `.p12` bundle to Amazon S3 (Step 6). Select the tab for your operating system to see the commands.

**Note**  
Amazon Bedrock reads the private key from the `.p12` bundle to sign authentication assertions, so the bundle must be password-protected. Choose a strong, random password — you store it in the secret as `certificatePassword` in Step 7.

------
#### [ Linux or macOS (OpenSSL) ]

**Generate a private key and self-signed certificate**

```
openssl req -x509 -newkey rsa:2048 -keyout private_key.pem -out certificate.cer \
    -days 365 -nodes \
    -subj "/CN={{bedrock-onedrive-connector}}"
```

**Package the certificate and key as a PKCS\#12 (`.p12`) bundle**

Enter a strong export password when prompted. Record it for Step 7.

```
openssl pkcs12 -export -out certificate.p12 \
    -inkey private_key.pem -in certificate.cer
```

You now have three files: the private key (`private_key.pem`), the public certificate (`certificate.cer`), and the bundle (`certificate.p12`). You upload the public certificate to Entra in Step 5 and the `.p12` bundle to Amazon S3 in Step 6.

------
#### [ Windows (PowerShell) ]

**Generate a self-signed certificate**

The following PowerShell commands generate a 2048-bit RSA self-signed certificate with a one-year validity period and store it in the current user's certificate store. Replace {{your-password}} with a strong, random password — you store it in the secret as `certificatePassword` in Step 7.

```
$cert = New-SelfSignedCertificate `
    -Subject "CN={{bedrock-onedrive-connector}}" `
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

You now have two files: the public certificate (`certificate.cer`) and the bundle (`certificate.p12`). You upload the public certificate to Entra in Step 5 and the `.p12` bundle to Amazon S3 in Step 6.

------

**Important**  
Store the `.p12` bundle in Amazon S3 (not the `.pem` or `.cer` file). The bundle contains the private key that Amazon Bedrock uses to authenticate to SharePoint for access verification, so store it securely. Document-level access control requires the `.p12` format.

**Note**  
The certificate is valid for one year by default. An expired certificate causes all syncs to fail, so rotate the certificate before it expires. To change the validity period, adjust the `-days` option (OpenSSL) or the `-NotAfter` argument (PowerShell). For the rotation steps, see [Rotate the certificate](kb-managed-ds-onedrive-troubleshooting.md#kb-managed-ds-onedrive-rotate-cert).

## Step 5 (ACLs only): Upload the public certificate to Entra
<a name="kb-managed-onedrive-entra-step5"></a>

1. In your app registration, choose **Certificates & secrets**, then the **Certificates** tab.

1. Choose **Upload certificate** and select the `certificate.cer` file you generated in Step 4 (the public certificate only — never upload the `.p12` bundle or the private key to Entra).

1. Choose **Add**.

## Step 6 (ACLs only): Upload the certificate to Amazon S3
<a name="kb-managed-onedrive-entra-step6"></a>

Upload the `.p12` bundle from Step 4 to an Amazon S3 bucket in the same AWS Region as your knowledge base. Record the bucket name and key — you use them as the data source `certificateS3Path`.

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
<a name="kb-managed-onedrive-entra-step7"></a>

Store the credentials in an AWS Secrets Manager secret. For Microsoft Entra App ID authentication, include the following key-value pairs:
+ `clientId` (required) — the application (client) ID from Step 1.
+ `clientSecret` (required) — the client secret value from Step 3.
+ `certificatePassword` (document-level access control only, recommended) — the password you set on the `.p12` bundle in Step 4. See the note that follows.

**Content only (no document-level access control)**

```
{
    "clientId": "{{your-client-id}}",
    "clientSecret": "{{your-client-secret}}"
}
```

**With document-level access control**

```
{
    "clientId": "{{your-client-id}}",
    "clientSecret": "{{your-client-secret}}",
    "certificatePassword": "{{your-certificate-password}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-onedrive-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
When document-level access control is enabled, set `certificatePassword` to the password you used when you created the `.p12` bundle in Step 4. If you omit this field, Amazon Bedrock opens the bundle using your application's client ID as the password, so the bundle must have been created with the client ID as its password. We recommend that you always set an explicit, high-entropy password instead.

## Step 8 (ACLs only): Grant the service role access to the certificate
<a name="kb-managed-onedrive-entra-step8"></a>

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

The upload command in [Step 6 (ACLs only): Upload the certificate to Amazon S3](#kb-managed-onedrive-entra-step6) uses Amazon S3-managed encryption (`AES256`), which needs no additional permissions. If instead you encrypt the certificate object with Amazon S3 server-side encryption using a customer managed KMS key (SSE-KMS), the service role also needs `kms:Decrypt` permission on that key, and the key's policy must allow the role to use it. Objects encrypted with the AWS managed `aws/s3` key do not require this additional grant.

```
{
    "Sid": "KmsDecryptCertificate",
    "Effect": "Allow",
    "Action": ["kms:Decrypt"],
    "Resource": ["arn:aws:kms:{{us-west-2}}:{{123456789012}}:key/{{your-key-id}}"]
}
```

For the complete set of knowledge base service role permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## Next steps
<a name="kb-managed-onedrive-entra-next"></a>

You now have the credentials you need to create the data source: the secret ARN, your tenant ID, and (for document-level access control) the Amazon S3 location of the certificate. To create the OneDrive data source with the AWS Management Console or the API, see [Connect a OneDrive data source](kb-managed-ds-onedrive-connect.md).