

# Connect to Confluence for your knowledge base
<a name="confluence-data-source-connector"></a>

Atlassian Confluence is a collaborative work-management tool designed for sharing, storing, and working on project planning, software development, and product management. You can connect to your Confluence instance for your Amazon Bedrock knowledge base by using either the [AWS Management Console for Amazon Bedrock](https://console.aws.amazon.com/bedrock/home) or the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) API (see Amazon Bedrock [supported SDKs and AWS CLI](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)).

**Note**  
Confluence data source connector is in preview release and is subject to change.  
Confluence data sources don't support multimodal data, such as tables, charts, diagrams, or other images..

Amazon Bedrock supports connecting to Confluence Cloud instances. Currently, only Amazon OpenSearch Serverless vector store is available to use with this data source.

There are limits to how many files and MB per file that can be crawled. See [Quotas for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html).

**Topics**
+ [Supported features](#supported-features-confluence-connector)
+ [Prerequisites](#prerequisites-confluence-connector)
+ [Connection configuration](#configuration-confluence-connector)

## Supported features
<a name="supported-features-confluence-connector"></a>
+ Auto detection of main document fields
+ Inclusion/exclusion content filters
+ Incremental content syncs for added, updated, deleted content
+ OAuth 2.0 authentication, authentication with Confluence API token

## Prerequisites
<a name="prerequisites-confluence-connector"></a>

**In Confluence, make sure you**:
+ Take note of your Confluence instance URL. For example, for Confluence Cloud, {{https://example.atlassian.net}}. The URL for Confluence Cloud must be the base URL, ending with {{.atlassian.net}}.
+ Configure basic authentication credentials containing a username (email of admin account) and password (Confluence API token) to allow Amazon Bedrock to connect to your Confluence Cloud instance. For information about how to create a Confluence API token, see [Manage API tokens for your Atlassian account](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/#Create-an-API-token) on the Atlassian website.
+ (Optional) Configure an OAuth 2.0 application with credentials of an app key, app secret, access token, and refresh token. For more information, see [OAuth 2.0 apps](https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/) on the Atlassian website.
+ Certain read permissions or scopes must be enabled for your OAuth 2.0 app to connect to Confluence.

  Confluence API:
  + offline\_access
  + read:content:confluence – View detailed contents 
  + read:content-details:confluence – View content details 
  + read:space-details:confluence – View space details
  + read:audit-log:confluence – View audit records 
  + read:page:confluence – View pages 
  + read:attachment:confluence – View and download content attachments 
  + read:blogpost:confluence – View blogposts 
  + read:custom-content:confluence – View custom content 
  + read:comment:confluence – View comments 
  + read:template:confluence – View content templates 
  + read:label:confluence – View labels 
  + read:watcher:confluence – View content watchers 
  + read:relation:confluence – View entity relationships 
  + read:user:confluence – View user details 
  + read:configuration:confluence – View Confluence settings 
  + read:space:confluence – View space details 
  + read:space.property:confluence – View space properties 
  + read:user.property:confluence – View user properties 
  + read:space.setting:confluence – View space settings 
  + read:analytics.content:confluence – View analytics for content
  + read:content.property:confluence – View content properties
  + read:content.metadata:confluence – View content summaries 
  + read:inlinetask:confluence – View tasks 
  + read:task:confluence – View tasks 
  + read:whiteboard:confluence – View whiteboards 
  + read:app-data:confluence – Read app data 
  + read:folder:confluence - View folders
  + read:embed:confluence - View Smart Link data

**In your AWS account, make sure you**:
+ Store your authentication credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note the Amazon Resource Name (ARN) of the secret. Follow the **Connection configuration** instructions on this page to include the key-values pairs that must be included in your secret.
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions for this data source to add to your knowledge base IAM role, see [Permissions to access data sources](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html#kb-permissions-access-ds).

**Note**  
If you use the console, you can go to AWS Secrets Manager to add your secret or use an existing secret as part of the data source configuration step. The IAM role with all the required permissions can be created for you as part of the console steps for creating a knowledge base. After you have configured your data source and other configurations, the IAM role with all the required permissions are applied to your specific knowledge base.  
We recommend that you regularly refresh or rotate your credentials and secret. Provide only the necessary access level for your own security. We do not recommend that you re-use credentials and secrets across data sources.

## Connection configuration
<a name="configuration-confluence-connector"></a>

To connect to your Confluence instance, you must provide the necessary configuration information so that Amazon Bedrock can access and crawl your data. You must also follow the [Prerequisites](#prerequisites-confluence-connector).

An example of a configuration for this data source is included in this section.

For more information about auto detection of document fields, inclusion/exclusion filters, incremental syncing, secret authentication credentials, and how these work, select the following:

### Auto detection of main document fields
<a name="ds-confluence-document-fields"></a>

The data source connector automatically detects and crawls all of the main metadata fields of your documents or content. For example, the data source connector can crawl the document body equivalent of your documents, the document title, the document creation or modification date, or other core fields that might apply to your documents.

**Important**  
If your content includes sensitive information, then Amazon Bedrock could respond using sensitive information.

You can apply filtering operators to metadata fields to help you further improve the relevancy of responses. For example, document "epoch\_modification\_time" or the number of seconds that’s passed January 1 1970 for when the document was last updated. You can filter on the most recent data, where "epoch\_modification\_time" is *greater than* a certain number. For more information on the filtering operators you can apply to your metadata fields, see [Metadata and filtering](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html).

### Inclusion/exclusion filters
<a name="ds-confluence-inclusion-exclusion"></a>

You can include or exclude crawling certain content. For example, you can specify an exclusion prefix/regular expression pattern to skip crawling any file that contains “private” in the file name. You could also specify an inclusion prefix/regular expression pattern to include certain content entities or content types. If you specify an inclusion and exclusion filter and both match a document, the exclusion filter takes precedence and the document isn’t crawled.

An example of a regular expression pattern to exclude or filter out PDF files that contain "private" in the file name: *".\*private.\*\\\\.pdf"*

You can apply inclusion/exclusion filters on the following content types:
+ `Space`: Unique space key
+ `Page`: Main page title
+ `Blog`: Main blog title
+ `Comment`: Comments that belong to a certain page or blog. Specify {{Re: Page/Blog Title}}
+ `Attachment`: Attachment file name with its extension

### Incremental syncing
<a name="ds-confluence-incremental-sync"></a>

The data source connector crawls new, modified, and deleted content each time your data source syncs with your knowledge base. Amazon Bedrock can use your data source’s mechanism for tracking content changes and crawl content that changed since the last sync. When you sync your data source with your knowledge base for the first time, all content is crawled by default.

To sync your data source with your knowledge base, use the [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) API or select your knowledge base in the console and select **Sync** within the data source overview section.

**Important**  
All data that you sync from your data source becomes available to anyone with `bedrock:Retrieve` permissions to retrieve the data. This can also include any data with controlled data source permissions. For more information, see [Knowledge base permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).

### Secret authentication credentials
<a name="ds-confluence-secret-auth-credentials"></a>

(If using basic authentication) Your secret authentication credentials in AWS Secrets Manager should include these key-value pairs:
+ `username`: {{admin user email address of Atlassian account}}
+ `password`: {{Confluence API token}}

(If using OAuth 2.0 authentication) Your secret authentication credentials in AWS Secrets Manager should include these key-value pairs:
+ `confluenceAppKey`: {{app key}}
+ `confluenceAppSecret`: {{app secret}}
+ `confluenceAccessToken`: {{app access token}}
+ `confluenceRefreshToken`: {{app refresh token}}

**Note**  
Confluence OAuth2.0 **access** token has a default expiry time of 60 minutes. If this token expires while your data source is syncing (sync job), Amazon Bedrock will use the provided **refresh** token to regenerate this token. This regeneration refreshes both the access and refresh tokens. To keep the tokens updated from the current sync job to the next sync job, Amazon Bedrock requires write/put permissions for your secret credentials as part of your knowledge base IAM role.

**Note**  
Your secret in AWS Secrets Manager must use the same Region of your knowledge base.

------
#### [ Console ]

**Connect a Confluence instance to your knowledge base**

1. Follow the steps at [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md) and choose **Confluence** as the data source.

1. Provide a name and optional description for the data source.

1. Provide your Confluence instance URL. For example, for Confluence Cloud, {{https://example.atlassian.net}}. The URL for Confluence Cloud must be the base URL, ending with {{.atlassian.net}}.

1. In the **Advanced settings** section, you can optionally configure the following:
   + **KMS key for transient data storage.** – You can encrypt the transient data while converting your data into embeddings with the default AWS managed key or your own KMS key. For more information, see [Encryption of transient data storage during data ingestion](encryption-kb.md#encryption-kb-ingestion).
   + **Data deletion policy** – You can delete the vector embeddings for your data source that are stored in the vector store by default, or choose to retain the vector store data.

1. Provide the authentication information to connect to your Confluence instance:
   + For basic authentication, go to AWS Secrets Manager to add your secret authentication credentials or use an existing Amazon Resource Name (ARN) for the secret you created. Your secret must contain the admin user email address of the Atlassian account as the username and a Confluence API token in place of a password. For information about how to create a Confluence API token, see [Manage API tokens for your Atlassian account](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/#Create-an-API-token) on the Atlassian website.
   + For OAuth 2.0 authentication, go to AWS Secrets Manager to add your secret authentication credentials or use an existing Amazon Resource Name (ARN) for the secret you created. Your secret must contain the Confluence app key, app secret, access token, and refresh token. For more information, see [OAuth 2.0 apps](https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/) on the Atlassian website.

1. (Optional) In the **Content parsing and chunking** section, you can customize how to parse and chunk your data. Refer to the following resources to learn more about these customizations:
   + For more information about parsing options, see [Parsing options for your data source](kb-advanced-parsing.md).
   + For more information about chunking strategies, see [How content chunking works for knowledge bases](kb-chunking.md).
**Warning**  
You can't change the chunking strategy after connecting to the data source.
   + For more information about how to customize chunking of your data and processing of your metadata with a Lambda function, see [Use a custom transformation Lambda function to define how your data is ingested](kb-custom-transformation.md).

1. Choose to use filters/regular expressions patterns to include or exclude certain content. All standard content is crawled otherwise.

1. Continue to choose an embeddings model and vector store. To see the remaining steps, return to [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md) and continue from the step after connecting your data source.

------
#### [ API ]

The following is an example of a configuration for connecting to Confluence Cloud for your Amazon Bedrock knowledge base. You configure your data source using the API with the AWS CLI or supported SDK, such as Python. After you call [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html), you call [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) to create your data source with your connection information in `dataSourceConfiguration`.

To learn about customizations that you can apply to ingestion by including the optional `vectorIngestionConfiguration` field, see [Customize ingestion for a data source](kb-data-source-customize-ingestion.md).

**AWS Command Line Interface**

```
aws bedrock create-data-source \
 --name "Confluence Cloud/SaaS connector" \
 --description "Confluence Cloud/SaaS data source connector for Amazon Bedrock to use content in Confluence" \
 --knowledge-base-id "your-knowledge-base-id" \
 --data-source-configuration file://confluence-bedrock-connector-configuration.json \
 --data-deletion-policy "DELETE" \
 --vector-ingestion-configuration '{"chunkingConfiguration":[{"chunkingStrategy":"FIXED_SIZE","fixedSizeChunkingConfiguration":[{"maxTokens":"100","overlapPercentage":"10"}]}]}'

confluence-bedrock-connector-configuration.json
{
    "confluenceConfiguration": {
        "sourceConfiguration": {
            "hostUrl": "https://example.atlassian.net",
            "hostType": "SAAS",
            "authType": "OAUTH2_CLIENT_CREDENTIALS",
            "credentialsSecretArn": "arn:aws::secretsmanager:your-region:secret:AmazonBedrock-Confluence"
        },
        "crawlerConfiguration": {
            "filterConfiguration": {
                "type": "PATTERN",
                "patternObjectFilter": {
                    "filters": [
                        {
                            "objectType": "Attachment",
                            "inclusionFilters": [
                                ".*\\.pdf"
                            ],
                            "exclusionFilters": [
                                ".*private.*\\.pdf"
                            ]
                        }
                    ]
                }
            }
        }
    },
    "type": "CONFLUENCE"
}
```

------