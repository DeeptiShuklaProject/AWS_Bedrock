

# Create an Amazon Bedrock knowledge base with Amazon Neptune Analytics graphs
<a name="knowledge-base-build-graphs-build"></a>

GraphRAG is fully integrated into Amazon Bedrock Knowledge Bases and uses Amazon Neptune Analytics for graph and vector storage. You can get started using GraphRAG in your knowledge bases with the AWS Management Console, the AWS CLI, or the AWS SDK.

You do not need any existing graph infrastructure to get started using GraphRAG. Amazon Bedrock Knowledge Bases automatically manages the creation and maintenance of the graphs from Amazon Neptune. The system will automatically create and update a graph by extracting entities, facts, and relationships from documents that you upload to your Amazon S3 bucket. so you can provide relevant responses to your end users, without any prior knowledge in graph modeling. The graph will be stored in Amazon Neptune Analytics.

When you create a knowledge base, you set up or specify the following:
+ General information that defines and identifies the knowledge base.
+ The service role with permissions to the knowledge base.
+ Configurations for the knowledge base, including the embeddings model to use when converting data from the data source, and storage configurations for the service in which to store the embeddings.

**Note**  
You can’t create a knowledge base with a root user. Log in with an IAM user before starting these steps.

The following shows how to create a knowledge base for using Neptune GraphRAG from the console and using the CLI.

------
#### [ Console ]

**To create a knowledge base for Neptune Analytics from the console**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, choose **Create**, and then choose **Knowledge Base with vector store**.

1. (Optional) Under **Knowledge Base details**, change the default name and provide a description for your knowledge base.

1. Under **IAM permissions**, choose an IAM role that provides Amazon Bedrock permissions to access other required AWS services. You can either have Amazon Bedrock create the service role for you, or you can choose to use your own custom role that you've created for Neptune Analytics. For an example, see [Permissions to access your vector database in Amazon Neptune Analytics](kb-permissions.md#kb-permissions-neptune).

1. Make sure to choose **Amazon S3** as your data source and choose **Next** to configure your data source.

1. Provide the **S3 URI** of the file that will be used as the data source to connect your knowledge base to and for integrating with Amazon Neptune Analytics. For additional steps and optional information you can provide, see [Connect a data source to your knowledge base](data-source-connectors.md).

1. In the **Embeddings model** section, choose an embeddings model to convert your data into vector embeddings. Optionally, you can use the **Additional configurations** section to specify the vector dimensions. For embeddings type, we recommend that you use floating-point vector embeddings.
**Note**  
The vector dimensions of the embeddings model must match the vector dimensions that you specified when creating the Neptune Analytics graph.

1. In the **Vector database** section, choose the method for creating the vector store, and then choose **Amazon Neptune Analytics (GraphRAG)** as your vector store to store the embeddings that will be used for the query. To create your vector store, you can use either of the following methods:
   + We recommend that you use the **Quick create a new vector store** method to get started quickly with creating your vector store. Choose **Amazon Neptune Analytics (GraphRAG)** as your vector store. This option doesn't require you to have any existing Neptune Analytics resources. The knowledge base automatically generates and stores document embeddings in Amazon Neptune, along with a graph representation of entities and their relationships derived from the document corpus.
   + Alternatively, if you have already created your Neptune Analytics graph and vector index, you can use the **Choose a vector store you have created** option. Choose **Amazon Neptune Analytics (GraphRAG)** as your vector store, and identify the graph ARN, vector field names, and metadata field names in the vector index. For more information, see [Prerequisites for using a vector store you created for a knowledge base](knowledge-base-setup.md).

1. In the **Model for graph construction** section, choose the foundation model to use for extracting entities and relationships from your documents during ingestion. The required permissions for the selected model are automatically added to the knowledge base service role.
**Note**  
Some models are supported only through cross-Region inference profiles. When you invoke a cross-Region inference profile in Amazon Bedrock, your request and data to be ingested originates from a source Region and is automatically routed to one of the destination Regions defined in that profile, optimizing for performance. The destination Regions for Global cross-Region inference profiles include all commercial Regions. For example, you might specify the `modelArn` for a us-based cross-Region call from the us-west-2 Region using the format `arn:aws:bedrock:us-west-2:{{account-id}}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0`.

   For guidance on how to use inference profiles to select source and destination Regions, see [Supported Regions and models for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html). Your data is stored only in your source Region corresponding to the Amazon Bedrock knowledge base and Amazon Neptune Analytics instance. The destination Region is used for inference only.

1. Choose **Next** and review the details of your knowledge base. You can edit any section before going ahead and creating your knowledge base.
**Note**  
The time it takes to create the knowledge base depends on your specific configurations. When the creation of the knowledge base has completed, the status of the knowledge base changes to either state it is ready or available.  
Once your knowledge base is ready and available, sync your data source for the first time and whenever you want to keep your content up to date. Select your knowledge base in the console and select **Sync** within the data source overview section.

1. Choose **Create knowledge base**. While Amazon Bedrock is creating the knowledge base, you should see the status **In progress**. You must wait for creation to finish before you can sync a data source.

1. After Amazon Bedrock finishes creating the knowledge base, to configure a data source, follow the instructions in [Connect a data source to your knowledge base](data-source-connectors.md).

------
#### [ API ]

**To create a knowledge base for Neptune Analytics using the AWS CLI**

1. First create a data source using the context enrichment configuration. To perform this operation, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for [Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). The following shows an example CLI command.

   ```
   aws bedrock-agent create-data-source \
       --name graph_rag_source \
       --description data_source_for_graph_rag \
       --knowledge-base-id LDBBY2K5AG \
       --cli-input-json "file://input.json"
   ```

   The following code shows the contents of the `input.json` file.

   ```
   {
       "dataSourceConfiguration": { 
           "s3Configuration": { 
               "bucketArn": "arn:aws:s3:::{{<example-graphrag-datasets>}}",
               "bucketOwnerAccountId": {{"<ABCDEFGHIJ>"}},
               "inclusionPrefixes": [ {{<"example-dataset">}} ]
           },
           "type": "S3",
       },
       "VectorIngestionConfiguration": {
           "contextEnrichmentConfiguration":
               "type": "BEDROCK_FOUNDATION_MODEL",
               "bedrockFoundationModelConfiguration": {
                   "modelArn": "arn:aws:bedrock:{{<region>}}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                   "enrichmentStrategyConfiguration": {
                       "method": "CHUNK_ENTITY_EXTRACTION"
               }
           }
       }
   }
   ```

   For the `modelArn` used to build the graph from your documents, you can use Claude 3 Haiku (as shown in the preceding example), Claude Haiku 4.5, and the Amazon Nova family (including Nova 2 and Nova models with text input modality). To see the foundation models available in your Region, see [Supported foundation models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html).
**Note**  
Some models are supported only through cross-Region inference profiles. When you invoke a cross-Region inference profile in Amazon Bedrock, your request and data to be ingested originates from a source Region and is automatically routed to one of the destination Regions defined in that profile, optimizing for performance. The destination Regions for Global cross-Region inference profiles include all commercial Regions. For example, you might specify the `modelArn` for a us-based cross-Region call from the us-west-2 Region using the format `arn:aws:bedrock:us-west-2:{{account-id}}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0`.

   To see the policy requirements for your role to use inference profiles, see [Prerequisites for cross-Region inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html). For guidance on how to use inference profiles to select source and destination Regions, see [Supported Regions and models for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html). Your data is stored only in your source Region corresponding to the Amazon Bedrock knowledge base and Amazon Neptune Analytics instance. The destination Region is used for inference only.

1. To create a knowledge base, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request with an Agents for [Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). The following shows an example CLI command.

   ```
   aws bi create-knowledge-base \
   --name {{<"knowledge-base-graphrag">}} \
   --role-arn arn:aws:iam::{{<accountId>}}:role/{{<BedrockExecutionRoleForKnowledgeBase>}} \
   --cli-input-json "file://input.json"
   ```

   The following shows the contents of the `input.json` file.

   ```
   {
       "storageConfiguration": {
           "type": "NEPTUNE_ANALYTICS"
           "neptuneAnalyticsConfiguration": {
               "graphArn": "arn:aws:neptune-graph:{{<region>}}:{{<>}}:graph/{{<graphID>}}",
               "fieldMapping": {
                   "metadataField": "metadata",
                   "textField": "text"
               },
           }
       },
       "knowledgeBaseConfiguration": {
           "type": "VECTOR",
           "vectorKnowledgeBaseConfiguration": {
               "embeddingModelArn": "arn:aws:bedrock:{{<region>}}::foundation-model/cohere.embed-english-v3"
           }
       }
   }
   ```

1. When your GraphRAG-based application is running, you can continue using the Knowledge Bases API operations to provide end users with more comprehensive, relevant, and explainable responses. The following sections show you how to start ingestion and perform retrieve queries using CLI commands.

------

## Choose and update the graph construction model
<a name="knowledge-base-build-graphs-model"></a>

GraphRAG uses a foundation model during ingestion to extract entities and relationships from your documents. You choose this model when you create a knowledge base or when you configure a data source. Selecting a graph construction model automatically enables contextual enrichment.

**Important**  
Foundation models can reach end-of-life or be deprecated. For example, Claude 3 Haiku has moved to Legacy status. We recommend that you select a currently supported model for graph construction. To check the status of available models, see [Model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html).

When you select a graph construction model, the required permissions are automatically added to the knowledge base service role.

Some models are available only through cross-Region inference profiles.

**Note**  
When using cross-Region inference, data to be ingested originates from a source Region and is routed to a destination Region for inference. Data is stored only in the source Region corresponding to the Amazon Bedrock knowledge base and Amazon Neptune Analytics instance.

**Choose a model during knowledge base creation (console)**

In Step 3 of the Create Knowledge Base workflow (configure data storage and processing ), when you select **Amazon Neptune Analytics (GraphRAG)** as the vector store type, a **Model for graph construction** section appears. Choose **Select model** to pick the model to use for extracting entities and relationships from your documents during ingestion.

**Update the model on an existing data source (console)**

Navigate to the Knowledge Base detail page. In the **Data source** section, select the data source and choose **Edit**. In the edit page, under **Model for graph construction**, choose a new model. Choose **Submit** to save your changes.

**Choose a model during knowledge base creation (API)**

When creating a data source via the `CreateDataSource` API, specify the `modelArn` in the `bedrockFoundationModelConfiguration` within `contextEnrichmentConfiguration`. See the API tab in the creation section above for a full example.

**Update the model on an existing data source (API)**

To update the graph construction model on an existing data source, use the `update-data-source` command. The following example shows how to specify a new model ARN in the `contextEnrichmentConfiguration`.

```
aws bedrock-agent update-data-source \
    --data-source-id {{data-source-id}} \
    --knowledge-base-id {{knowledge-base-id}} \
    --name {{data-source-name}} \
    --data-source-configuration '{"type":"S3","s3Configuration":{"bucketArn":"arn:aws:s3:::{{bucket-name}}"}}' \
    --vector-ingestion-configuration '{"contextEnrichmentConfiguration":{"type":"BEDROCK_FOUNDATION_MODEL","bedrockFoundationModelConfiguration":{"modelArn":"{{model-arn}}","enrichmentStrategyConfiguration":{"method":"CHUNK_ENTITY_EXTRACTION"}}}}' \
    --region {{region}}
```

For example, to use Claude Haiku 4.5 through a US-based cross-Region inference profile from the `us-west-2` Region, specify the `modelArn` in the following format:

```
arn:aws:bedrock:us-west-2:{{account-id}}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0
```

To see the policy requirements for your role to use inference profiles, see [Prerequisites for cross-Region inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html). For guidance on how to use inference profiles to select source and destination Regions, see [Supported Regions and models for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html).

## Sync your data source
<a name="knowledge-base-build-graphs-sync"></a>

After you create your knowledge base, you ingest or sync your data so that the data can be queried. Ingestion extracts the graphical structure and converts the raw data in your data source into vector embeddings, based on the vector embeddings model and configurations that you specified.

The following command shows an example of how to start an ingestion job using the CLI.

```
aws bedrock-agent start-ingestion-job \
--data-source-id {{<"ABCDEFGHIJ">}} \
--knowledge-base-id {{<"EFGHIJKLMN">}}
```

For more information and how to sync your data source using the console and API, see [Sync your data with your Amazon Bedrock knowledge base](kb-data-source-sync-ingest.md).

## Ingest changes into your knowledge base
<a name="knowledge-base-build-graphs-ingest"></a>

When using Amazon S3 as your data source, you can modify your data source and sync the changes in one step. With direct ingestion, you can directly add, update, or delete files in a knowledge base in a single action and your knowledge base can have access to documents without the need to sync. Direct ingestion uses the `KnowledgeBaseDocuments` API operations to index the documents that you submit directly into the vector store set up for the knowledge base. You can also view the documents in your knowledge base directly with these operations, rather than needing to navigate to the connected data source to view them. For more information, see [Ingest changes directly into a knowledge base](kb-direct-ingestion.md).

## Test your knowledge base
<a name="knowledge-base-build-graphs-test"></a>

Now that you've set up your knowledge base, you can test it by sending querues and generating responses.

The following code shows an example CLI command.

```
aws bedrock-agent-runtime retrieve \
--knowledge-base-id {{<"ABCDEFGHIJ">}} \
--retrieval-query="{\"text\": \"What are the top three video games available now?\"}"
```

For more information, see [Query a knowledge base connected to an Amazon Neptune Analytics graph](kb-test-neptune.md).