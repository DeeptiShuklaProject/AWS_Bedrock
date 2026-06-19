

# Set up Basic authentication for Confluence
<a name="kb-managed-confluence-basic-setup"></a>

Basic authentication (`BASIC`) is the recommended authentication method for a Confluence data source. The connector signs in with the email address of a Confluence user and an Atlassian API token (used in place of a password). It is the only authentication method that supports document-level access control (ACLs); ACLs also require Atlassian organization admin credentials in the same secret.

## Step 1: Generate an Atlassian API token
<a name="kb-managed-confluence-basic-step1"></a>

Use the Confluence user account whose access you want the connector to use. The account must have access to all the spaces, pages, and blog posts you want to crawl.

1. Sign in to [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens) with the Confluence user account.

1. Choose **Create API token**, enter a label, and choose **Create**.

1. Copy the API token immediately and store it securely. The token is shown only once.

For more information, see [Manage API tokens for your Atlassian account](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/#Create-an-API-token) on the Atlassian website.

## Step 2: (For ACLs) Get Atlassian organization admin credentials
<a name="kb-managed-confluence-basic-step2"></a>

Skip this step if you do not plan to enable document-level access control.

Document-level access control requires Atlassian organization admin credentials in addition to the user-level API token. Admin credentials let Amazon Bedrock resolve user and group memberships from your organization, regardless of individual email visibility settings. The admin credentials are different from the user API token and must come from an Atlassian organization administrator.

You need three values:


**Atlassian organization admin values**  

| Value | How to obtain it | 
| --- | --- | 
| adminApiKey | An Atlassian organization API key with the read:directories:admin and read:workspaces:admin scopes. Generate it at admin.atlassian.com under Settings → API keys (org admin only). | 
| organizationId | The UUID of your Atlassian organization. Sign in to admin.atlassian.com and copy the ID from the URL: admin.atlassian.com/o/{{{orgId}}}. | 
| directoryId | The UUID of the user directory for your Confluence workspace. Retrieve it with the Atlassian Admin Workspace API (GET /v2/orgs/{{{orgId}}}/workspaces) using the adminApiKey as a bearer token. Use the directoryId from the workspace that corresponds to your Confluence site. | 

## Step 3: Create the Secrets Manager secret
<a name="kb-managed-confluence-basic-step3"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs.

**Without document-level access control**

```
{
    "username": "{{your-confluence-email}}",
    "password": "{{your-atlassian-api-token}}",
    "hostUrl": "{{https://your-instance.atlassian.net}}"
}
```

**With document-level access control**

```
{
    "username": "{{your-confluence-email}}",
    "password": "{{your-atlassian-api-token}}",
    "hostUrl": "{{https://your-instance.atlassian.net}}",
    "adminApiKey": "{{your-atlassian-admin-api-key}}",
    "organizationId": "{{your-org-uuid}}",
    "directoryId": "{{your-directory-uuid}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-confluence-basic-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

## Next steps
<a name="kb-managed-confluence-basic-next"></a>

After you store the secret, create the data source with `authType` set to `BASIC`. See [Connect a Confluence data source](kb-managed-ds-confluence-connect.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-confluence-acl.md).