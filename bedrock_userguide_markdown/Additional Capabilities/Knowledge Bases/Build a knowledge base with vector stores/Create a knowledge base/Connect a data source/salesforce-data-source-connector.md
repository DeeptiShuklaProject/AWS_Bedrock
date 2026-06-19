

# Connect to Salesforce for your knowledge base
<a name="salesforce-data-source-connector"></a>

Salesforce is a customer relationship management (CRM) tool for managing support, sales, and marketing teams. You can connect to your Salesforce instance for your Amazon Bedrock knowledge base by using either the [AWS Management Console for Amazon Bedrock](https://console.aws.amazon.com/bedrock/home) or the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) API (see Amazon Bedrock [supported SDKs and AWS CLI](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)).

**Note**  
Salesforce data source connector is in preview release and is subject to change.  
Salesforce data sources don't support multimodal data, such as tables, charts, diagrams, or other images..

Currently, only Amazon OpenSearch Serverless vector store is available to use with this data source.

There are limits to how many files and MB per file that can be crawled. See [Quotas for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html).

**Topics**
+ [Supported features](#supported-features-salesforce-connector)
+ [Prerequisites](#prerequisites-salesforce-connector)
+ [Connection configuration](#configuration-salesforce-connector)

## Supported features
<a name="supported-features-salesforce-connector"></a>
+ Auto detection of main document fields
+ Inclusion/exclusion content filters
+ Incremental content syncs for added, updated, deleted content
+ OAuth 2.0 authentication

## Prerequisites
<a name="prerequisites-salesforce-connector"></a>

**In Salesforce, make sure you**:
+ Take note of your Salesforce instance URL. For example, {{https://company.salesforce.com/}}. The instance must be running a Salesforce Connected App.
+ Create a Salesforce Connected App and configure client credentials. Then, for your selected app, copy the consumer key (client ID) and consumer secret (client secret) from the OAuth settings. For more information, see Salesforce documentation on [Create a Connected App](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5) and [Configure a Connected App for the OAuth 2.0 Client Credentials](https://help.salesforce.com/s/articleView?id=sf.connected_app_client_credentials_setup.htm&type=5).
**Note**  
For Salesforce Connected Apps, under Client Credentials Flow, make sure you search and select the user’s name or alias for your client credentials in the “Run As” field.

**In your AWS account, make sure you**:
+ Store your authentication credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note the Amazon Resource Name (ARN) of the secret. Follow the **Connection configuration** instructions on this page to include the key-values pairs that must be included in your secret.
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions for this data source to add to your knowledge base IAM role, see [Permissions to access data sources](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html#kb-permissions-access-ds).

**Note**  
If you use the console, you can go to AWS Secrets Manager to add your secret or use an existing secret as part of the data source configuration step. The IAM role with all the required permissions can be created for you as part of the console steps for creating a knowledge base. After you have configured your data source and other configurations, the IAM role with all the required permissions are applied to your specific knowledge base.  
We recommend that you regularly refresh or rotate your credentials and secret. Provide only the necessary access level for your own security. We do not recommend that you re-use credentials and secrets across data sources.

## Connection configuration
<a name="configuration-salesforce-connector"></a>

To connect to your Salesforce instance, you must provide the necessary configuration information so that Amazon Bedrock can access and crawl your data. You must also follow the [Prerequisites](#prerequisites-salesforce-connector).

An example of a configuration for this data source is included in this section.

For more information about auto detection of document fields, inclusion/exclusion filters, incremental syncing, secret authentication credentials, and how these work, select the following:

### Auto detection of main document fields
<a name="ds-salesforce-document-fields"></a>

The data source connector automatically detects and crawls all of the main metadata fields of your documents or content. For example, the data source connector can crawl the document body equivalent of your documents, the document title, the document creation or modification date, or other core fields that might apply to your documents.

**Important**  
If your content includes sensitive information, then Amazon Bedrock could respond using sensitive information.

You can apply filtering operators to metadata fields to help you further improve the relevancy of responses. For example, document "epoch\_modification\_time" or the number of seconds that’s passed January 1 1970 for when the document was last updated. You can filter on the most recent data, where "epoch\_modification\_time" is *greater than* a certain number. For more information on the filtering operators you can apply to your metadata fields, see [Metadata and filtering](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html).

### Inclusion/exclusion filters
<a name="ds-salesforce-inclusion-exclusion"></a>

You can include or exclude crawling certain content. For example, you can specify an exclusion prefix/regular expression pattern to skip crawling any file that contains “private” in the file name. You could also specify an inclusion prefix/regular expression pattern to include certain content entities or content types. If you specify an inclusion and exclusion filter and both match a document, the exclusion filter takes precedence and the document isn’t crawled.

An example of a regular expression pattern to exclude or filter out campaigns that contain "private" in the campaign name: *".\*private.\*"*

You can apply inclusion/exclusion filters on the following content types:
+ `Account`: Account number/identifier
+ `Attachment`: Attachment file name with its extension
+ `Campaign`: Campaign name and associated identifiers
+ `ContentVersion`: Document version and associated identifiers
+ `Partner`: Partner information fields including associated identifiers
+ `Pricebook2`: Product/price list name
+ `Case`: Customer inquiry/issue number and other information fields including associated identifiers (please note: can contain personal information, which you can choose to exclude or filter out)
+ `Contact`: Customer information fields (please note: can contain personal information, which you can choose to exclude or filter out)
+ `Contract`: Contract name and associated identifiers
+ `Document`: File name with its extension
+ `Idea`: Idea information fields and associated identifiers
+ `Lead`: Potential new customer information fields (please note: can contain personal information, which you can choose to exclude or filter out)
+ `Opportunity`: Pending sale/deal information fields and associated identifiers
+ `Product2`: Product information fields and associated identifiers
+ `Solution`: Solution name for a customer inquiry/issue and associated identifiers
+ `Task`: Task information fields and associated identifiers
+ `FeedItem`: Identifier of the chatter feed post
+ `FeedComment`: Identifier of the chatter feed post that the comments belong to
+ `Knowledge__kav`: Knowledge Article Title
+ `User`: User alias within your organization
+ `CollaborationGroup`: Chatter group name (unique)

### Incremental syncing
<a name="ds-salesforce-incremental-sync"></a>

The data source connector crawls new, modified, and deleted content each time your data source syncs with your knowledge base. Amazon Bedrock can use your data source’s mechanism for tracking content changes and crawl content that changed since the last sync. When you sync your data source with your knowledge base for the first time, all content is crawled by default.

To sync your data source with your knowledge base, use the [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html) API or select your knowledge base in the console and select **Sync** within the data source overview section.

**Important**  
All data that you sync from your data source becomes available to anyone with `bedrock:Retrieve` permissions to retrieve the data. This can also include any data with controlled data source permissions. For more information, see [Knowledge base permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).

### Secret authentication credentials
<a name="ds-salesforce-secret-auth-credentials"></a>

(For OAuth 2.0 authentication) Your secret authentication credentials in AWS Secrets Manager should include these key-value pairs:
+ `consumerKey`: {{app client ID}}
+ `consumerSecret`: {{app client secret}}
+ `authenticationUrl`: {{Salesforce instance URL or the URL to request the authentication token from}}

**Note**  
Your secret in AWS Secrets Manager must use the same Region of your knowledge base.

------
#### [ Console ]

**Connect a Salesforce instance to your knowledge base**

1. Follow the steps at [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md) and choose **Salesforce** as the data source.

1. Provide a name and optional description for the data source.

1. Provide your Salesforce instance URL. For example, {{https://company.salesforce.com/}}. The instance must be running a Salesforce Connected App.

1. In the **Advanced settings** section, you can optionally configure the following:
   + **KMS key for transient data storage.** – You can encrypt the transient data while converting your data into embeddings with the default AWS managed key or your own KMS key. For more information, see [Encryption of transient data storage during data ingestion](encryption-kb.md#encryption-kb-ingestion).
   + **Data deletion policy** – You can delete the vector embeddings for your data source that are stored in the vector store by default, or choose to retain the vector store data.

1. Provide the authentication information to connect to your Salesforce instance:

   1. For OAuth 2.0 authentication, go to AWS Secrets Manager to add your secret authentication credentials or use an existing Amazon Resource Name (ARN) for the secret you created. Your secret must contain the Salesforce Connected App consumer key (client ID), consumer secret (client secret), and the Salesforce instance URL or the URL to request the authentication token from. For more information, see Salesforce documentation on [Create a Connected App](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5) and [Configure a Connected App for the OAuth 2.0 Client Credentials](https://help.salesforce.com/s/articleView?id=sf.connected_app_client_credentials_setup.htm&type=5).

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

The following is an example of a configuration for connecting to Salesforce for your Amazon Bedrock knowledge base. You configure your data source using the API with the AWS CLI or supported SDK, such as Python. After you call [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html), you call [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) to create your data source with your connection information in `dataSourceConfiguration`.

To learn about customizations that you can apply to ingestion by including the optional `vectorIngestionConfiguration` field, see [Customize ingestion for a data source](kb-data-source-customize-ingestion.md).

**AWS Command Line Interface**

```
aws bedrock create-data-source \
 --name "Salesforce connector" \
 --description "Salesforce data source connector for Amazon Bedrock to use content in Salesforce" \
 --knowledge-base-id "your-knowledge-base-id" \
 --data-source-configuration file://salesforce-bedrock-connector-configuration.json \
 --data-deletion-policy "DELETE" \
 --vector-ingestion-configuration '{"chunkingConfiguration":[{"chunkingStrategy":"FIXED_SIZE","fixedSizeChunkingConfiguration":[{"maxTokens":"100","overlapPercentage":"10"}]}]}'

salesforce-bedrock-connector-configuration.json
{
    "salesforceConfiguration": {
        "sourceConfiguration": {
            "hostUrl": "https://company.salesforce.com/",
            "authType": "OAUTH2_CLIENT_CREDENTIALS",
            "credentialsSecretArn": "arn:aws::secretsmanager:your-region:secret:AmazonBedrock-Salesforce"
        },
        "crawlerConfiguration": {
            "filterConfiguration": {
                "type": "PATTERN",
                "patternObjectFilter": {
                    "filters": [
                        {
                            "objectType": "Campaign",
                            "inclusionFilters": [
                                ".*public.*"
                            ],
                            "exclusionFilters": [
                                ".*private.*"
                            ]
                        }
                    ]
                }
            }
        }
    },
    "type": "SALESFORCE"
}
```

------