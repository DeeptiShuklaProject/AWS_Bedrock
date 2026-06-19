

# Create an Amazon Bedrock knowledge base with an Amazon Kendra GenAI index
<a name="knowledge-base-kendra-genai-index-create"></a>

 For more information about using an Amazon Kendra GenAI index, see [ Amazon Kendra GenAI index](https://docs.aws.amazon.com/kendra/latest/dg/hiw-index-types.html#kendra-gen-ai-index) in the *Amazon Kendra Developer Guide*.

You can create an Amazon Bedrock knowledge base with an Amazon Kendra GenAI index using either the Amazon Bedrock console or the Amazon Bedrock API. Choose the tab for your preferred method, and then follow the steps:

**Note**  
You can't create a knowledge base with a root user. Before you begin, log in with an AWS Identity and Access Management (IAM) user.

**Important**  
To create a knowledge base with an Amazon Kendra GenAI index using the API, you must have an existing index. With the API, you can't create an index while creating a knowledge base. If you want to create an index while creating a knowledge base, then you must use the console.

------
#### [ Console ]

**To create a knowledge base with an Amazon Kendra GenAI index**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, choose **Create**.

1. Choose **Knowledge Base with Kendra GenAI index**.

1. (Optional) Under **Knowledge base details**, change the default name and provide a description for your knowledge base.

1. Under **IAM permissions**, choose an IAM role that provides Amazon Bedrock permissions to access other required AWS services. You can either have Amazon Bedrock create the service role for you, or you can choose a [custom role that you've created](kb-permissions.md).

1. Choose to **Create and use a new service role** or **use an existing service role**.

1. Choose to **create a new Amazon Kendra GenAI index** or use an **existing one Amazon Kendra GenAI index**.

1. (Optional) Under **Additional configurations**, do any of the following:
   + Configure an AWS Key Management Service (AWS KMS) customer managed key to encrypt your knowledge base.
   + Add tags to your knowledge base. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

   

   

1. Choose **Create knowledge base**. While Amazon Bedrock is creating the knowledge base, you should see the status **In progress**. You must wait for creation to finish before you can add and sync a data source.

1. After Amazon Bedrock finishes creating the knowledge base, to configure a data source, follow the instructions in [Connect a data source to your knowledge base](data-source-connectors.md).

------
#### [ API ]

**To create a knowledge base with an Amazon Kendra GenAI index**

To create a knowledge base, send a [ CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request (see link for request and response formats and field details) with an Agents for [Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).
+ In the `roleArn` field, provide the Amazon Resource Name (ARN) of an IAM role that has permissions to create an Amazon Bedrock knowledge base.
+ To use a model that's supported for knowledge bases, you must [enable model access](model-access.md). Note your model's ARN, which is required to convert your data into vector embeddings. Copy the model (resource) ID for your chosen model for knowledge bases. Then, construct the model ARN using the model ID by following the ARN examples provided in [Resource types defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-resources-for-iam-policies) in the *Service Authorization Reference*. Refer to the examples for your model resource type.

  In the `embeddingModelArn` field, in the `knowledgeBaseConfiguration` object, provide the ARN of the vector embeddings model that you want to use. For more information, see [Supported models and Regions for Amazon Bedrock knowledge bases](knowledge-base-supported.md).
+ To create a knowledge base with an Amazon Kendra GenAI index, provide the ARN of your Amazon Kendra GenAI index 
+ After you create a knowledge base, create a data source that contains the documents or content for your knowledge base. Note that you can't create a data source using Amazon Bedrock API operations. You must do so with either the Amazon Bedrock console or the Amazon Kendra [ CreateDataSource](https://docs.aws.amazon.com/kendra/latest/APIReference/API_CreateDataSource.html) API operation. For more information about choosing a data source, and for API connection configuration examples, see [Connect a data source to your knowledge base](data-source-connectors.md).

------