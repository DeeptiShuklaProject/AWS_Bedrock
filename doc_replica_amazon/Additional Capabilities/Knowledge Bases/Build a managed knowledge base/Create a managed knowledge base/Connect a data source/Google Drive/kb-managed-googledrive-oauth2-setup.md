

# Set up OAuth 2.0 authentication for Google Drive
<a name="kb-managed-googledrive-oauth2-setup"></a>

OAuth 2.0 authentication (`OAUTH2`) authenticates with an OAuth 2.0 client ID and secret together with a refresh token that you obtain from a single Google user's sign-in. The connector accesses only the content that user can access — their own drive, files shared with them, and any shared drives they belong to.

**Important**  
OAuth 2.0 does not support document-level access control (ACLs). To filter query results by user permissions, use service account authentication. See [Set up service account authentication for Google Drive](kb-managed-googledrive-service-account-setup.md).

## Step 1: Enable the Google Drive API
<a name="kb-managed-googledrive-oauth2-step1"></a>

1. Open the [Google Cloud console](https://console.cloud.google.com/) and select or create a project.

1. In the navigation menu, choose **APIs & Services**, then **Library**.

1. Search for **Google Drive API** and choose **Enable**.

## Step 2: Create OAuth 2.0 credentials
<a name="kb-managed-googledrive-oauth2-step2"></a>

1. In the navigation menu, choose **APIs & Services**, then **Credentials**.

1. If prompted, configure the **OAuth consent screen** first. Select **Internal** if your Google Workspace administrator allows it; otherwise **External**. Add a name, support email, and the `https://www.googleapis.com/auth/drive.readonly` scope.

1. On the **Credentials** page, choose **Create Credentials**, then **OAuth client ID**.

1. For **Application type**, choose **Web application**.

1. Under **Authorized redirect URIs**, add `https://developers.google.com/oauthplayground` so you can obtain a refresh token in Step 3.

1. Choose **Create**. Copy the **Client ID** and **Client secret**.

## Step 3: Obtain a refresh token
<a name="kb-managed-googledrive-oauth2-step3"></a>

Use the OAuth 2.0 Playground to obtain a refresh token for the Google user whose access the connector should use. The user must have access to all the Drive content you want to crawl.

1. Open the [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/).

1. Choose the gear icon (**OAuth 2.0 configuration**), select **Use your own OAuth credentials**, and enter the client ID and client secret from Step 2.

1. In **Step 1: Select & authorize APIs**, enter `https://www.googleapis.com/auth/drive.readonly` in the **Input your own scopes** field, and choose **Authorize APIs**.

1. Sign in as the Google user whose access the connector should use, and grant the requested permissions.

1. In **Step 2: Exchange authorization code for tokens**, choose **Exchange authorization code for tokens**. Copy the **Refresh token** from the response.

## Step 4: Create the Secrets Manager secret
<a name="kb-managed-googledrive-oauth2-step4"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs:

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
  --name {{bedrock-google-drive-oauth2-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
If the refresh token is revoked or expires, syncs fail with an authentication error. Refresh tokens can be revoked by the user, by your Google Workspace administrator, or after extended inactivity. Re-run the OAuth 2.0 Playground flow to obtain a new refresh token, and update the secret.

## Next steps
<a name="kb-managed-googledrive-oauth2-next"></a>

After you store the secret, create the data source with `authType` set to `OAUTH2`. See [Connect a Google Drive data source](kb-managed-ds-googledrive-connect.md).