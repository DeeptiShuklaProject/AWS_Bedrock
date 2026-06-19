

# Set up OAuth 2.0 authentication for OneDrive
<a name="kb-managed-onedrive-oauth2-setup"></a>

OAuth 2.0 authentication (`OAUTH2`) authenticates with an application client ID and secret together with a delegated **refresh token**. The connector uses the refresh token to obtain access tokens that crawl content in the signed-in user's delegated context. The data source covers OneDrive content that user can access — their own drive, plus any drives shared with them or where they have SharePoint admin access. Drives the signed-in user cannot access are silently skipped.

**Important**  
We recommend [Set up Microsoft Entra App ID authentication for OneDrive](kb-managed-onedrive-entra-setup.md) for most data sources. OAuth 2.0 authentication has the following limitations:  
It crawls only OneDrive content the signed-in user can access (their own drive, plus any drives shared with them or where they have SharePoint admin access). Drives the user cannot access are silently skipped. To crawl every user's OneDrive in your tenant uniformly, use Microsoft Entra App ID authentication.
It requires a refresh token, which you obtain through a one-time user sign-in (Step 4).
Refresh tokens have a finite Microsoft-side lifetime. When the refresh token expires or is revoked, syncs fail until you obtain a new one and update the secret.
It does not support document-level access control (ACLs). To filter query results by user permissions, use Microsoft Entra App ID authentication.

## Prerequisites
<a name="kb-managed-onedrive-oauth2-prereqs"></a>
+ Microsoft Entra ID administrator access to register an application, grant admin consent, and create a client secret.
+ A Microsoft 365 user account that has access to the OneDrive content you want to crawl. You sign in as this user once to obtain the refresh token.
+ Your Microsoft 365 tenant ID.

## Step 1: Register the application in Microsoft Entra ID
<a name="kb-managed-onedrive-oauth2-step1"></a>

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

1. In the left navigation, expand **Entra ID** and choose **App registrations**.

1. Choose **New registration**.

1. For **Name**, enter a descriptive name, such as `bedrock-onedrive-oauth2`.

1. For **Supported account types**, select **Accounts in this organizational directory only (Single tenant)**.

1. Under **Redirect URI**, select **Web** as the platform and enter `http://localhost:53672/callback`. You use this redirect URI when you obtain a refresh token in Step 4. You can use any free localhost port; if you change the port here, use the same port in Step 4.

1. Choose **Register**.

1. On the application **Overview** page, record the **Application (client) ID** and the **Directory (tenant) ID**.

## Step 2: Add API permissions and grant admin consent
<a name="kb-managed-onedrive-oauth2-step2"></a>

OAuth 2.0 authentication uses a delegated sign-in, so the application needs **delegated** permissions — not application permissions.

1. In your app registration, choose **API permissions**, then **Add a permission**.

1. Choose **Microsoft Graph**, then **Delegated permissions**.

1. Select the following delegated permissions, then choose **Add permissions**:
   + `Files.Read.All` — read the files the user can access.
   + `Sites.Read.All` — read the OneDrive sites the user can access.
   + `User.Read.All` — identify the user.
   + `offline_access` — required so the sign-in returns a refresh token.

1. On the **API permissions** page, choose **Grant admin consent for [your organization]** and confirm.

## Step 3: Create a client secret
<a name="kb-managed-onedrive-oauth2-step3"></a>

1. In your app registration, choose **Certificates & secrets**, then **Client secrets**, then **New client secret**.

1. Enter a description, choose an expiration, and choose **Add**.

1. Record the secret **Value** immediately — it is shown only once. Record the **Value**, not the **Secret ID**.

## Step 4: Obtain a refresh token
<a name="kb-managed-onedrive-oauth2-step4"></a>

The connector needs a refresh token, which you obtain through a one-time user sign-in. The procedure below uses the OAuth 2.0 authorization code flow with a localhost redirect, which works for users with multi-factor authentication (MFA). For non-MFA service accounts, a simpler alternative is provided at the end.

**Authorization code flow (recommended)**

1. **Build the sign-in URL.** Replace the placeholders with your tenant ID and the application (client) ID from Step 1. If you used a different localhost port in Step 1, update the `redirect_uri` to match.

   ```
   https://login.microsoftonline.com/{{TENANT_ID}}/oauth2/v2.0/authorize?client_id={{CLIENT_ID}}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A53672%2Fcallback&response_mode=query&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default%20offline_access
   ```

1. **Sign in.** Open the URL in a browser and sign in as the Microsoft 365 user whose access you want the connector to use. Complete any MFA challenge.

   The browser then redirects to the localhost URL, which does not load (this is expected because nothing is listening on that port). The browser address bar now contains the redirect URI followed by a `code` parameter, for example: `http://localhost:53672/callback?code=0.AXoA...&session_state=...`.

1. **Copy the authorization code.** From the address bar, copy the value of the `code` parameter (everything between `code=` and the next `&`). The code is valid for a few minutes; complete Step 4 immediately.

1. **Exchange the code for a refresh token.** Replace the placeholders with your tenant ID, application (client) ID, the client secret from Step 3, and the authorization code you just copied.

   ```
   curl -s -X POST \
     "https://login.microsoftonline.com/{{TENANT_ID}}/oauth2/v2.0/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code" \
     -d "client_id={{CLIENT_ID}}" \
     -d "client_secret={{CLIENT_SECRET}}" \
     -d "code={{AUTHORIZATION_CODE}}" \
     -d "redirect_uri=http://localhost:53672/callback" \
     -d "scope=https://graph.microsoft.com/.default offline_access"
   ```

   The response includes a `refresh_token`. Record it for Step 5.

**Resource owner password credentials (alternative for non-MFA service accounts)**

If your account does not require MFA and is not subject to Conditional Access policies that enforce interactive sign-in, you can skip the browser flow and exchange the user's credentials for a refresh token directly. Replace the placeholders with your values, including the user's UPN and password.

```
curl -s -X POST \
  "https://login.microsoftonline.com/{{TENANT_ID}}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id={{CLIENT_ID}}" \
  -d "client_secret={{CLIENT_SECRET}}" \
  -d "username={{USER_UPN}}" \
  -d "password={{USER_PASSWORD}}" \
  -d "scope=https://graph.microsoft.com/.default offline_access"
```

The response includes a `refresh_token`. Record it for Step 5. This flow does not work for accounts with MFA enforced; use the authorization code flow above instead.

## Step 5: Create the Secrets Manager secret
<a name="kb-managed-onedrive-oauth2-step5"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs:
+ `clientId` — the application (client) ID from Step 1.
+ `clientSecret` — the client secret value from Step 3.
+ `refreshToken` — the refresh token from Step 4.

```
{
    "clientId": "{{your-client-id}}",
    "clientSecret": "{{your-client-secret}}",
    "refreshToken": "{{your-refresh-token}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-onedrive-oauth2-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
The `OAUTH2` connector reads the refresh token once from your secret and reuses it for every sync — it does not save the rotated value Microsoft returns. Plan to mint a new refresh token (Step 4) and update the `refreshToken` field in your secret before your existing one expires. If you do not update the secret in time, syncs fail with a token-refresh error until you do.

## Next steps
<a name="kb-managed-onedrive-oauth2-next"></a>

After you store the secret, create the data source with `authType` set to `OAUTH2`. You do not provide a certificate for this method. See [Connect a OneDrive data source](kb-managed-ds-onedrive-connect.md).