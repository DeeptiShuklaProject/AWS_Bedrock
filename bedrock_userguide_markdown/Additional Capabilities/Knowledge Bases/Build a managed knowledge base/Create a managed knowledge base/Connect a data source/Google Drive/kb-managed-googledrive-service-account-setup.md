

# Set up service account authentication for Google Drive
<a name="kb-managed-googledrive-service-account-setup"></a>

Service account authentication (`SERVICE_ACCOUNT`) is the recommended method for a Google Drive data source. A Google Cloud service account authenticates with a private key, then impersonates a Google Workspace admin user to crawl Drive content for any user in your domain. This is the only method that supports document-level access control (ACLs).

**Administrative access required**  
This setup requires a Google Workspace administrator to enable APIs, create the service account, configure domain-wide delegation, and create a delegated admin user. The AWS side requires administrator access to AWS Secrets Manager and IAM.

## Step 1: Create a Google Cloud project
<a name="kb-managed-googledrive-sa-step1"></a>

1. Open the [Google Cloud console](https://console.cloud.google.com/).

1. From the project selector at the top of the page, choose **New Project**.

1. Enter a project name, and choose **Create**.

1. After the project is created, switch to it from the project selector.

## Step 2: Enable the required APIs
<a name="kb-managed-googledrive-sa-step2"></a>

1. In the Google Cloud console navigation menu, choose **APIs & Services**, then **Library**.

1. Search for and enable each of the following APIs:
   + **Google Drive API**
   + **Google Drive Activity API**
   + **Admin SDK API**

## Step 3: Create the service account
<a name="kb-managed-googledrive-sa-step3"></a>

1. In the navigation menu, choose **APIs & Services**, then **Credentials**.

1. Choose **Create Credentials**, then **Service account**.

1. Enter a name (for example, `bedrock-google-drive-connector`) and an optional description, and choose **Done**.

1. On the **Credentials** page, choose the service account you just created.

1. On the **Details** tab, copy the **Unique ID**. You use this in Step 5 to grant domain-wide delegation.

## Step 4: Generate a private key
<a name="kb-managed-googledrive-sa-step4"></a>

1. On the service account detail page, choose the **Keys** tab.

1. Choose **Add Key**, then **Create new key**.

1. Select **JSON** and choose **Create**. Your browser downloads a JSON file containing the service account's `client_email` and `private_key`. Store the file securely.

**Note**  
If you receive an error stating that service account key creation is disabled by an organization policy, you must override the `iam.disableServiceAccountKeyCreation` constraint for your project. For details, see [Restricting service account usage](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts) in the Google Cloud documentation.

## Step 5: Configure domain-wide delegation
<a name="kb-managed-googledrive-sa-step5"></a>

Domain-wide delegation lets the service account act on behalf of users in your Google Workspace.

1. Sign in to the [Google Workspace Admin Console](https://admin.google.com/) as a Google Workspace administrator.

1. In the navigation pane, choose **Security**, **Access and data control**, **API controls**.

1. Choose **Manage Domain Wide Delegation**, then **Add new**.

1. For **Client ID**, enter the service account's Unique ID from Step 3.

1. For **OAuth scopes**, enter the following comma-separated values:

   ```
   https://www.googleapis.com/auth/drive.readonly,
   https://www.googleapis.com/auth/drive.metadata.readonly,
   https://www.googleapis.com/auth/admin.directory.user.readonly,
   https://www.googleapis.com/auth/admin.directory.group.readonly,
   https://www.googleapis.com/auth/cloud-platform,
   https://www.googleapis.com/auth/forms.body.readonly
   ```

1. Choose **Authorize**.

## Step 6: Create a delegated admin user
<a name="kb-managed-googledrive-sa-step6"></a>

The service account impersonates a Google Workspace admin user when crawling content. We recommend creating a dedicated admin user for this purpose with the minimum required roles.

1. In the Google Workspace Admin Console, choose **Directory**, then **Users**.

1. Choose **Add new user**, enter a first name, last name, and primary email address, and choose **Add new user**.

1. From the user list, open the user you created.

1. Expand the **Admin roles and privileges** section, and assign the following roles:
   + **Groups Reader**
   + **User Management Admin**
   + **Storage Admin**

1. Choose **Save**. Record this user's email address; you store it in the secret as `adminAccountEmail`.

## Step 7: Create the Secrets Manager secret
<a name="kb-managed-googledrive-sa-step7"></a>

Store the credentials in an AWS Secrets Manager secret with the following key-value pairs. Copy `clientEmail` and `privateKey` from the JSON key file you downloaded in Step 4 (use the `client_email` and `private_key` values).

```
{
    "adminAccountEmail": "{{admin@your-domain.com}}",
    "clientEmail": "{{your-service-account@your-project.iam.gserviceaccount.com}}",
    "privateKey": "{{your-private-key-from-the-json-key-file}}"
}
```

Create the secret with the AWS Command Line Interface:

```
aws secretsmanager create-secret \
  --name {{bedrock-google-drive-sa-creds}} \
  --secret-string file://secret.json
```

Record the secret ARN from the response. You use it as the data source `secretArn`.

**Note**  
The `privateKey` value contains literal `\n` escape sequences from the JSON key file. Keep them as-is when copying the value into the secret.

## Next steps
<a name="kb-managed-googledrive-sa-next"></a>

After you store the secret, create the data source with `authType` set to `SERVICE_ACCOUNT`. See [Connect a Google Drive data source](kb-managed-ds-googledrive-connect.md). To filter query results by user permissions, see [Document-level access controls](kb-managed-ds-googledrive-acl.md).