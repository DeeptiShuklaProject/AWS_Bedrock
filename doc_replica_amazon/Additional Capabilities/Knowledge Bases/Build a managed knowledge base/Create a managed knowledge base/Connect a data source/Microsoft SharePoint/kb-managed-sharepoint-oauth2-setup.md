

# Set up OAuth 2.0 authentication for SharePoint
<a name="kb-managed-sharepoint-oauth2-setup"></a>

OAuth 2.0 authentication (`OAUTH2_APP`) authenticates with an application client ID and secret together with the user name and password of a Microsoft 365 user account, using the OAuth 2.0 resource-owner password credentials (ROPC) flow. The connector signs in as that user to read content.

**Important**  
We recommend [Set up Microsoft Entra ID App-Only authentication for SharePoint](kb-managed-sharepoint-entra-setup.md) instead. OAuth 2.0 authentication has two limitations:  
Because it signs in with a user name and password, it cannot complete a multi-factor authentication (MFA) challenge or satisfy a Conditional Access policy that requires one. If the account enforces MFA or Conditional Access, authentication fails and the data source cannot sync. Many organizations require MFA for the kinds of accounts you would use here.
It does not support document-level access control (ACLs). To filter query results by user permissions, use Microsoft Entra ID App-Only authentication.

## Prerequisites
<a name="kb-managed-sharepoint-oauth2-prereqs"></a>
+ A Microsoft 365 user account whose user name and password the connector uses to sign in. The account must have access to the SharePoint sites you want to crawl, and must not require MFA or Conditional Access for sign-in.
+ Microsoft Entra ID administrator access to register an application and create a client secret.
+ Your Microsoft 365 tenant ID.

## Step 1: Register the application in Microsoft Entra ID
<a name="kb-managed-sharepoint-oauth2-step1"></a>

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

1. In the left navigation, expand **Entra ID** and choose **App registrations**.

1. Choose **New registration**.

1. For **Name**, enter a descriptive name, such as `bedrock-sharepoint-oauth2`.

1. For **Supported account types**, select **Accounts in this organizational directory only (Single tenant)**.

1. Leave **Redirect URI** blank, and choose **Register**.

1. On the application **Overview** page, record the **Application (client) ID** and the **Directory (tenant) ID**.

## Step 2: Add API permissions and grant admin consent
<a name="kb-managed-sharepoint-oauth2-step2"></a>

OAuth 2.0 authentication requires two permissions: a Microsoft Graph application permission to enumerate sites, and a SharePoint delegated permission to read content. Assign both of the following.


**Permissions for OAuth 2.0 authentication**  

| API | Permission | Type | Purpose | 
| --- | --- | --- | --- | 
| Microsoft Graph | Sites.Read.All | Application | Enumerate SharePoint sites. | 
| SharePoint | AllSites.Read | Delegated | Read site content through the SharePoint REST API. Requires admin consent (see the following note). | 

1. In your app registration, choose **API permissions**, then **Add a permission**.

1. Choose **Microsoft Graph**, then **Application permissions**. Search for and select `Sites.Read.All`, then choose **Add permissions**.

1. Choose **Add a permission** again. Choose **SharePoint** (under **Microsoft APIs**), then **Delegated permissions**. Select `AllSites.Read` (Read items in all site collections), then choose **Add permissions**.

1. On the **API permissions** page, choose **Grant admin consent for [your organization]** and confirm.

**Important**  
You must grant admin consent even though the Entra portal shows **Admin consent required: No** for the SharePoint `AllSites.Read` delegated permission. That column indicates that a user could normally consent during an interactive sign-in — but the resource-owner password credentials flow has no interactive surface, so the permission cannot be consented at sign-in time and must be pre-granted org-wide with **Grant admin consent for [your organization]**. Without it, the SharePoint token request fails with `AADSTS65001` (the user or administrator has not consented to use the application) and the data source cannot sync.

**Note**  
If your tenant has security defaults enabled, the resource-owner password credentials flow might be blocked. You might need an administrator to adjust your tenant's security defaults or Conditional Access policies so the account used here can sign in without MFA. For more information, see the Microsoft documentation on [security defaults](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults).

## Step 3: Create a client secret
<a name="kb-managed-sharepoint-oauth2-step3"></a>

1. In your app registration, choose **Certificates & secrets**, then **Client secrets**, then **New client secret**.

1. Enter a description, choose an expiration, and choose **Add**.

1. Record the secret **Value** immediately — it is shown only once. Record the **Value**, not the **Secret ID**.

## Step 4: Create the Secrets Manager secret
<a name="kb-managed-sharepoint-oauth2-step4"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs:
+ `clientId` — the application (client) ID from Step 1.
+ `clientSecret` — the client secret value from Step 3.
+ `userName` — the user name (UPN) of the Microsoft 365 user account.
+ `password` — the password for that account.

```
{
    "clientId": "{{your-client-id}}",
    "clientSecret": "{{your-client-secret}}",
    "userName": "{{user@yourdomain.onmicrosoft.com}}",
    "password": "{{your-account-password}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-sharepoint-oauth2-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
The account password is stored in the secret and used for each sync. If the password changes, update the secret. Because the connector signs in with this account, treat the secret as highly sensitive and restrict access to it.

## Troubleshooting
<a name="kb-managed-sharepoint-oauth2-troubleshooting"></a>

If the data source fails to sync, match the error against the following signatures.


**OAuth 2.0 sync errors**  

| Error | Cause and resolution | 
| --- | --- | 
| AADSTS65001 (the user or administrator has not consented to use the application) | The SharePoint AllSites.Read delegated permission has not been admin-consented. In your app registration, choose API permissions, then Grant admin consent for [your organization]. See Step 2. | 
| Rest API token request failed with status: 400 | The resource-owner password credentials sign-in failed at authentication, typically because the account requires MFA or a Conditional Access policy that the flow cannot satisfy. Use an account that does not require MFA, and confirm the userName and password in the secret are correct. | 
| SharePoint app is missing required scopes | The Microsoft Graph Sites.Read.All application permission has not been granted (or consented). The connector checks the Graph application token for this scope before crawling. Add the Microsoft Graph Sites.Read.All application permission and grant admin consent. See Step 2. | 

## Next steps
<a name="kb-managed-sharepoint-oauth2-next"></a>

After you store the secret, create the data source with `authType` set to `OAUTH2_APP`. You do not provide a certificate for this method. See [Connect a SharePoint data source](kb-managed-ds-sharepoint-connect.md).