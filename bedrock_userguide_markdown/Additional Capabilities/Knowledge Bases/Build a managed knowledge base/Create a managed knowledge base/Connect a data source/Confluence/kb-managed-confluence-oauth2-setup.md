

# Set up OAuth 2.0 authentication for Confluence
<a name="kb-managed-confluence-oauth2-setup"></a>

OAuth 2.0 authentication (`OAUTH2`) authenticates with an Atlassian OAuth 2.0 three-legged (3LO) app. You register an app in the Atlassian developer console, complete a one-time authorization flow to obtain a refresh token, and store the credentials in AWS. At crawl time, Amazon Bedrock uses the refresh token to mint short-lived access tokens automatically.

**Important**  
OAuth 2.0 does not support document-level access control (ACLs). To filter query results by user permissions, use Basic authentication. See [Set up Basic authentication for Confluence](kb-managed-confluence-basic-setup.md).

## Step 1: Register an OAuth 2.0 (3LO) app
<a name="kb-managed-confluence-oauth2-step1"></a>

1. Sign in to the [Atlassian developer console](https://developer.atlassian.com/console/myapps/).

1. Choose **Create**, then **OAuth 2.0 integration**.

1. Enter a name for the app (for example, `bedrock-confluence-connector`) and choose **Create**.

1. On the app's **Permissions** page, add **Confluence API**. Configure the following granular scopes (or the equivalent classic scopes if your app uses them):
   + `read:content:confluence`
   + `read:content-details:confluence`
   + `read:space:confluence`
   + `read:space-details:confluence`
   + `read:user:confluence`
   + `read:attachment:confluence`
   + `read:page:confluence` — required for page enumeration
   + `read:blogpost:confluence` — required if you crawl blog posts
   + `read:custom-content:confluence` — required if your workspace contains custom content

   Add `offline_access` in the **Authorization** — **User identity API** permission. `offline_access` is what causes Atlassian to issue a refresh token.

1. On the **Authorization** page, set the **Callback URL** to a URL you control where you can capture the authorization code in Step 3 (for example, `https://localhost:8080/callback`).

1. On the **Settings** page, copy the **Client ID** and **Secret**. These are the `confluenceAppKey` and `confluenceAppSecret`.

## Step 2: Authorize the app
<a name="kb-managed-confluence-oauth2-step2"></a>

Open the following URL in a browser, replacing the placeholders with your values. Sign in with the Atlassian user whose access the connector should use; the user must have access to the Confluence content you want to crawl.

```
https://auth.atlassian.com/authorize?
audience=api.atlassian.com&
client_id={{your-client-id}}&
scope=read:content:confluence%20read:content-details:confluence%20read:space:confluence%20read:space-details:confluence%20read:user:confluence%20read:attachment:confluence%20read:page:confluence%20read:blogpost:confluence%20read:custom-content:confluence%20offline_access&
redirect_uri={{https://localhost:8080/callback}}&
response_type=code&
prompt=consent
```

Approve the consent prompt. Atlassian redirects to your callback URL with a `code` query parameter. Copy that authorization code.

## Step 3: Exchange the code for tokens
<a name="kb-managed-confluence-oauth2-step3"></a>

Exchange the authorization code for an access token and a refresh token. From a terminal, run:

```
curl -X POST https://auth.atlassian.com/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "authorization_code",
    "client_id": "{{your-client-id}}",
    "client_secret": "{{your-client-secret}}",
    "code": "{{authorization-code-from-step-2}}",
    "redirect_uri": "{{https://localhost:8080/callback}}"
  }'
```

The response contains `access_token` and `refresh_token`. Record both values. The refresh token does not expire as long as it is used regularly.

## Step 4: Create the Secrets Manager secret
<a name="kb-managed-confluence-oauth2-step4"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs:

```
{
    "confluenceAppKey": "{{your-client-id}}",
    "confluenceAppSecret": "{{your-client-secret}}",
    "confluenceAccessToken": "{{your-access-token}}",
    "confluenceRefreshToken": "{{your-refresh-token}}",
    "hostUrl": "{{https://your-instance.atlassian.net}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-confluence-oauth2-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

## Step 5: Grant the service role permission to update the secret
<a name="kb-managed-confluence-oauth2-step5"></a>

Atlassian access tokens expire after 60 minutes. Amazon Bedrock uses the refresh token to mint a new access token and writes the new value back to the same secret. Add `secretsmanager:PutSecretValue` for the secret to your knowledge base service role's permissions policy:

```
{
    "Effect": "Allow",
    "Action": "secretsmanager:PutSecretValue",
    "Resource": "{{arn:aws:secretsmanager:region:account-id:secret:bedrock-confluence-oauth2-creds-*}}"
}
```

Without this permission, the connector cannot persist the rotated access token, and subsequent syncs fail.

## Next steps
<a name="kb-managed-confluence-oauth2-next"></a>

After you store the secret, create the data source with `authType` set to `OAUTH2`. See [Connect a Confluence data source](kb-managed-ds-confluence-connect.md).