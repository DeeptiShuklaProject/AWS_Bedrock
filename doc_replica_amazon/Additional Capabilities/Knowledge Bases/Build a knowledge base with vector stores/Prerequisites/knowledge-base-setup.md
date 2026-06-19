

# Prerequisites for using a vector store you created for a knowledge base
<a name="knowledge-base-setup"></a>

To store the vector embeddings that your documents are converted to, you use a vector store. Amazon Bedrock Knowledge Bases supports a quick-create flow for some of the vector stores, so if you prefer for Amazon Bedrock to automatically create a vector index for you in one of those vector stores, skip this prerequisite and proceed to [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md).

If you want to store binary vector embeddings instead of the standard floating-point (float32) vector embeddings, then you must use a vector store that supports binary vectors.

**Note**  
Amazon OpenSearch Serverless and Amazon OpenSearch Managed clusters are the only vector stores that support storing binary vectors.

You can set up your own supported vector store to index the vector embeddings representation of your data. You create fields for the following data:
+ A field for the vectors generated from the text in your data source by the embeddings model that you choose.
+ A field for the text chunks extracted from the files in your data source.
+ Fields for source files metadata that Amazon Bedrock manages.
+ (If you use an Amazon Aurora database and want to set up [filtering on metadata](kb-test-config.md)) Fields for metadata that you associate with your source files. If you plan to set up filtering in other vector stores, you don't have to set up these fields for filtering.

You can encrypt third-party vector stores with a KMS key. For more information, see [Encryption of knowledge base resources](https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html).

Select the tab corresponding to the vector store service that you will use to create your vector index.

**Note**  
Your choice of embeddings model and vector dimensions can affect the available vector store choices. If you are not able to use your preferred vector store, choose compatible options the embeddings model and vector dimensions.

------
#### [ Amazon OpenSearch Serverless ]

1. To configure permissions and create a vector search collection in Amazon OpenSearch Serverless in the AWS Management Console, follow steps 1 and 2 at [Working with vector search collections](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vector-search.html) in the Amazon OpenSearch Service Developer Guide. Note the following considerations while setting up your collection:

   1. Give the collection a name and description of your choice.

   1. To make your collection private, select **Standard create** for the **Security** section. Then, in the **Network access settings** section, select **VPC** as the **Access type** and choose a VPC endpoint. For more information about setting up a VPC endpoint for an Amazon OpenSearch Serverless collection, see [Access Amazon OpenSearch Serverless using an interface endpoint (AWS PrivateLink)](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vpc.html) in the Amazon OpenSearch Service Developer Guide.

1. Once the collection is created, take note of the **Collection ARN** for when you create the knowledge base.

1. In the left navigation pane, select **Collections** under **Serverless**. Then select your vector search collection.

1. Select the **Indexes** tab. Then choose **Create vector index**.

1. In the **Vector index details** section, enter a name for your index in the **Vector index name** field.

1. In the **Vector fields** section, choose **Add vector field**. Amazon Bedrock stores the vector embeddings for your data source in this field. Provide the following configurations:
   + **Vector field name** – Provide a name for the field (for example, **embeddings**).
   + **Engine** – The vector engine used for search. Select **faiss**.
   + **Dimensions** – The number of dimensions in the vector. Refer to the following table to determine how many dimensions the vector should contain:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
   + **Distance metric** – The metric used to measure the similarity between vectors. We recommend using **Euclidean** for floating-point vector embeddings.

1. Expand the **Metadata management** section and add two fields to configure the vector index to store additional metadata that a knowledge base can retrieve with vectors. The following table describes the fields and the values to specify for each field:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)

1. Take note of the names you choose for the vector index name, vector field name, and metadata management mapping field names for when you create your knowledge base. Then choose **Create**.

After the vector index is created, you can proceed to [create your knowledge base](knowledge-base-create.md). The following table summarizes where you will enter each piece of information that you took note of.


| Field | Corresponding field in knowledge base setup (Console) | Corresponding field in knowledge base setup (API) | Description | 
| --- | --- | --- | --- | 
| Collection ARN | Collection ARN | collectionARN | The Amazon Resource Name (ARN) of the vector search collection. | 
| Vector index name | Vector index name | vectorIndexName | The name of the vector index. | 
| Vector field name | Vector field | vectorField | The name of the field in which to store vector embeddings for your data sources. | 
| Metadata management (first mapping field) | Text field | textField | The name of the field in which to store the raw text from your data sources. | 
| Metadata management (second mapping field) | Bedrock-managed metadata field | metadataField | The name of the field in which to store metadata that Amazon Bedrock manages.  | 

For more detailed documentation on setting up a vector store in Amazon OpenSearch Serverless, see [Working with vector search collections](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vector-search.html) in the Amazon OpenSearch Service Developer Guide.

------
#### [ Amazon OpenSearch Service Managed Clusters ]

**Important**  
Before using any domain resources in OpenSearch Managed clusters, you need to configure certain IAM access permissions and policies. For more information, see [Prerequisites and permissions required for using OpenSearch Managed Clusters with Amazon Bedrock Knowledge BasesOverview of permissions configuration](kb-osm-permissions-prereq.md).
If you encounter data ingestion failures, it might indicate insufficient OpenSearch domain capacity. To resolve this issue, increase your domain's capacity by provisioning higher IOPS and by increasing the throughput settings. For more information, see [Operational best practices for Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/bp.html).

1. To create a domain and vector index in OpenSearch Cluster in the AWS Management Console, follow the steps described in [Creating and managing OpenSearch Service domains](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html) in the *Amazon OpenSearch Service Developer Guide*.

   Note the following considerations while setting up your domain:

   1. Give the domain a name of your choice.

   1. We recommend that you use the **Easy create** option to get started quickly with creating your domain.
**Note**  
This option gives you a domain with a low throughput. If you have larger workloads that require a higher throughput, choose the **Standard Create** option. You can adjust the capacity later as required. With this option, you can start with the lowest capacity, which can then be modified later as needed.

   1. For Network, you must choose **Public access**. OpenSearch domains that are behind a VPC are not supported for your Knowledge Base.

   1. For **Version**, if you're using binary vector embeddings, Amazon Bedrock Knowledge Bases requires an Engine version of 2.16 or later. In addition, a version of 2.13 or higher is required to create a k-nn index. For more information, see [K-NN Search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html) in the *Amazon OpenSearch Service developer guide*.

   1. We recommend that you use the **Dual-stack mode**.

   1. We recommend that you enable **Fine-grained access control** to protect the data in your domain, and further control the permissions that grants your Knowledge base service role access to the OpenSearch domain and make requests.

   1. Leave all other settings to their default values and choose **Create** to create your domain.

1. Once the domain is created, choose it to take note of the **Domain ARN** and **Domain endpoint** for when you create the knowledge base.

1. After you've created the domain, you can create a vector index by running the following commands on an OpenSearch dashboard or using curl commands. For more information, see the [OpenSearch documentation](https://opensearch.org/docs/latest/search-plugins/knn/knn-index/).

   When running the command:
   + Provide a name for the vector field (for example, **embeddings**).
   + Make sure that the vector used for search is **faiss**. **nmslib** is not supported.
   + For the number of dimensions in the vector, refer to the following table to determine how many dimensions the vector should contain:
**Note**  
The Titan V2 Embeddings - Text model supports multiple dimensions. It can also be 256 or 512.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
   + You can add two fields to configure the vector index to store additional metadata that a knowledge base can retrieve with vectors. The following table describes the fields and the values to specify for each of them.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)

   ```
   PUT /{{<index-name>}}
   {
       "settings": {
           "index": {
               "knn": true
           }
       },
       "mappings": {
           "properties": {
               "{{<vector-name>}}": {
                   "type": "knn_vector",
                   "dimension": {{<embedding-dimension>}},
                   "data_type": "binary",          # Only needed for binary embeddings
                   "space_type": "l2" | "hamming", # Use l2 for float embeddings and hamming for binary embeddings
                   "method": {
                       "name": "hnsw",
                       "engine": "faiss",
                       "parameters": {
                           "ef_construction": 128,
                           "m": 24
                       }
                   }
               },
   
               "AMAZON_BEDROCK_METADATA": {
                   "type": "text",
                   "index": "false"
               },
               "AMAZON_BEDROCK_TEXT_CHUNK": {
                   "type": "text",
                   "index": "true"            
               }
           }
       }
   }
   ```
**Custom metadata fields for filtering**  
If you plan to use [metadata filtering](kb-test-config.md) with custom metadata fields, you must define those fields with a `keyword` type or as a `text` type with a `keyword` subfield. For example:  

   ```
   "my_custom_field": {
       "type": "text",
       "fields": {
           "keyword": {
               "type": "keyword"
           }
       }
   }
   ```
Without this structure, filtering queries on custom metadata fields will fail with a "Rewrite first" error.

1. Take note of the domain ARN and endpoint, and the names you choose for the vector index name, vector field name, and metadata management mapping field names for when you create your knowledge base.

After the vector index is created, you can proceed to [create your knowledge base](knowledge-base-create.md). The following table summarizes where you will enter each piece of information that you took note of.


| Field | Corresponding field in knowledge base setup (Console) | Corresponding field in knowledge base setup (API) | Description | 
| --- | --- | --- | --- | 
| Domain ARN | Domain ARN | domainARN | The Amazon Resource Name (ARN) of the OpenSearch domain. | 
| Domain endpoint | Domain endpoint | domainEndpoint | The endpoint to connect to the OpenSearch domain. | 
| Vector index name | Vector index name | vectorIndexName | The name of the vector index. | 
| Vector field name | Vector field | vectorField | The name of the field in which to store vector embeddings for your data sources. | 
| Metadata management (first mapping field) | Text field | textField | The name of the field in which to store the raw text from your data sources. | 
| Metadata management (second mapping field) | Bedrock-managed metadata field | metadataField | The name of the field in which to store metadata that Amazon Bedrock manages.  | 

------
#### [ Amazon S3 Vectors ]

Amazon S3 Vectors provides cost-effective vector storage in Amazon S3 that can be used to store and query vector data. It provides durable and elastic storage of large vector datasets with sub-second query performance. Amazon S3 Vectors is best suited for infrequent query workloads, and can help reduce costs when used in retrieval augmented generation (RAG) and semantic search applications.

Amazon S3 Vectors introduces S3 vector buckets, which contain vector indexes that you can query based on semantic meaning and similarity. It can be used to deliver sub-second query response times and reduce costs while storing, accessing, and querying vector data at scale without provisioning any infrastructure. Inside a vector bucket, you can organize your vector data within vector indexes. Your vector bucket can have multiple vector indexes. For more information, see [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) in the *Amazon S3 User Guide*.

**Note**  
You can create a knowledge base for Amazon S3 Vectors in all AWS Regions where both Amazon Bedrock and Amazon S3 Vectors are available. For information about regional availability of Amazon S3 Vectors, see [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) in the *Amazon S3 User Guide*.
When using very high token counts with hierarchical chunking in Amazon Bedrock Knowledge Bases, you can exceed the maximum metadata size limits as parent-child chunk relationships and hierarchical context are stored as non-filterable metadata in Amazon S3 Vectors. For more information about metadata size limits per vector, see [Limitations and restrictions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-limitations.html) in the *Amazon S3 User Guide*. For information about chunking strategies, see [How content chunking works for knowledge bases](kb-chunking.md).
<a name="metadata-support"></a>
**Metadata support**  
You can attach metadata as key-value pairs to each vector. By default, metadata is filterable and can be used in similarity search queries to filter by conditions such as dates, categories, or user preferences.

You can also configure metadata to be non-filterable when creating the vector index. Amazon S3 vector indexes support string, boolean, and number types.

When using Amazon S3 Vectors with Amazon Bedrock Knowledge Bases, you can attach up to 1 KB of custom metadata (including both filterable and non-filterable metadata) and 35 metadata keys per vector. For more information about metadata size limits per vector, see [Limitations and restrictions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-limitations.html) in the *Amazon S3 User Guide*.

If the metadata exceeds these limits, the ingestion job will throw an exception when populating the vector index. For more information, see [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) in the *Amazon S3 User Guide*.

**Required permissions**  
Make sure that your IAM policy allows Amazon Bedrock to access your vector index in S3 vector bucket. For more information about the required permissions, see [Create a service role for Amazon Bedrock Knowledge Bases](kb-permissions.md).

**Create S3 vector bucket and index**  
To use Amazon S3 Vectors with your knowledge base, you need to create an S3 vector bucket and a vector index. You can create a vector bucket and index using the Amazon S3 console, AWS CLI, or AWS SDK. For detailed instructions, see [Create a vector index](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-index-create.html) in the *Amazon S3 User Guide*.

Note the following considerations when creating your vector bucket and index in the [Amazon S3 console](https://console.aws.amazon.com/s3/vector-buckets#).

1. When creating your S3 vector bucket, take note of the following considerations.
   + Provide a unique **Vector bucket name**.
   + (Optional) Amazon S3 will automatically encrypt the data using the default **Server-side encryption with Amazon S3 managed keys (SSE-S3)**. You can choose whether to use this default encryption, or the **Server-side encryption with AWS Key Management Service keys (SSE-KMS)** instead.
**Note**  
The encryption type can't be changed once the vector bucket has been created.

     For step-by-step instructions, see [Encryption with AWS KMS keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bucket-encryption.html).

1. Once you've created the S3 vector bucket, take note of the **Amazon Resource Name (ARN)** of the vector bucket for when you create the knowledge base.

1. Choose the vector bucket that you created and then create a vector index. When creating the vector index, take note of the following considerations.
   + **Vector index name** – Provide a name for the field (for example, **embeddings**).
   + **Dimension** – The number of dimensions in the vector. The dimensions must be a value between 1 and 4096. Refer to the following table to determine how many dimensions the vector should contain based on your selection of the embeddings model:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
   + 
**Note**  
Amazon S3 Vectors only support floating-point embeddings. Binary embeddings are not supported.

     **Distance metric** – The metric used to measure the similarity between vectors. You can use **Cosine** or **Euclidean**.

1. Expand the **Additional settings** and provide any non-filterable metadata in the **Non-filterable metadata** field.

   You can configure up to a maximum of 10 non-filterable metadata keys. Choose **Add key** and then add `AMAZON_BEDROCK_TEXT` and `AMAZON_BEDROCK_METADATA` as keys.

1. Under **Encryption**, choose **Specify encryption type**. You have the option to **Use bucket settings for encryption** or override the encryption settings for the vector index. If you override the bucket-level settings, you have the option to specify encryption type for the vector index as **Server-side encryption with AWS Key Management Service keys (SSE-KMS)** or the default **Server-side encryption with Amazon S3 managed keys (SSE-S3)**. For more information about setting encryption configuration for vector indexes, see [Data protection and encryption in Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-data-encryption.html).

1. Under **Tags (Optional)**, you can add tags as key-value pairs to help track and organize vector index costs using AWS Billing and Cost Management. Enter a **Key** and a **Value**. To add another tag, choose **Add Tag**. You can enter up to 50 tags for a vector index. For more information see [Using tags with Amazon S3 vector indexes](https://docs.aws.amazon.com/console/s3/vector-index-create-with-tag).

1. Create the vector index and take note of the **Amazon Resource Name (ARN)** of the vector index for when you create the knowledge base.

**Create knowledge base for S3 vector bucket**  
After you've gathered this information, you can proceed to [create your knowledge base](knowledge-base-create.md). When creating your knowledge base with S3 vector bucket, you'll need to provide the ARN of the vector bucket and the vector index. The vector index will store the embeddings that's generated from your data sources. The following table summarizes where you will enter each piece of information:


| Field | Corresponding field in knowledge base setup (Console) | Corresponding field in knowledge base setup (API) | Description | 
| --- | --- | --- | --- | 
| Vector bucket ARN | S3 vector bucket ARN | vectorBucketArn | The Amazon Resource Name (ARN) of your S3 vector bucket. | 
| Vector index ARN | S3 vector index ARN | vectorIndexARN | The Amazon Resource Name (ARN) of the vector index for your S3 vector bucket. | 

------
#### [ Amazon Aurora (RDS) ]

1. Create an Amazon Aurora database (DB) cluster, schema, and table by following the steps at [Using Aurora PostgreSQL as a knowledge base](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html). When you create the table, configure it with the following columns and data types. You can use column names of your liking instead of the ones listed in the following table. Take note of the column names you choose so that you can provide them during knowledge base setup.

   You must provide these fields before creating the knowledge base. They connot be updated once the knowledge base has been created.
**Important**  
The Aurora cluster must reside in the same AWS account as the one where the knowledge base is created for Amazon Bedrock.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)

1. You must create an index on the columns vector and text for your text and embeddings fields. If you're using the custom metadata field, you must also create a GIN index on this column. GIN indexes can be used to efficiently search for key-value pairs in jsonb documents for metadata filtering. For more information, see [jsonb indexing](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING) in the *PostgreSQL documentation*.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
**Note**  
For improving hybrid search accuracy and latency with English content, consider using the 'english' dictionary instead of 'simple':  

   ```
   CREATE INDEX ON bedrock_integration.bedrock_kb USING gin (to_tsvector('english', chunks));
   ```
**Note**  
If you use metadata filtering with your knowledge base, we recommend enabling HNSW iterative index scans (requires pgvector 0.8.0 or later). Without iterative scans, selective metadata filters can return fewer results than expected because filtering is applied after the HNSW index scan. Iterative scans automatically scan more of the index until enough filtered results are found.  

   ```
   ALTER DATABASE {{your_database}} SET hnsw.iterative_scan = 'relaxed_order';
   ALTER DATABASE {{your_database}} SET hnsw.max_scan_tuples = 20000;
   ```
These settings persist at the database level but only take effect for new sessions. If you are using the RDS Data API, allow a few minutes for connection pool sessions to recycle before the settings take effect.

1. (Optional) If you [added metadata to your files for filtering](kb-test-config.md), we recommend that you provide the column name in the custom metadata field to store all your metadata in a single column. During [data ingestion](kb-data-source-sync-ingest.md), this column will be populated with all the information in the metadata files from your data sources. If you choose to provide this field, you must create a GIN index on this column.
**Note**  
If you frequently use range filters over numerical metadata, then to optimize performance, create an index for the specific key. For example, if you use filters such as `"lessThan": { "key": "year", "value": 1989 }`, create an expression index on the `year` key. For more information, see [Indexes on expressions](https://www.postgresql.org/docs/current/indexes-expressional.html) in the *PostgreSQL documentation*.  

   ```
   CREATE INDEX ON your_table ((custom_metadata->>'year')::double precision
   ```

   Alternatively, if you don't provide this field name, you can create a column for each metadata attribute in your files and specify the data type (text, number, or boolean). For example, if the attribute `genre` exists in your data source, you would add a column named `genre` and specify `text` as the data type. During [data ingestion](kb-data-source-sync-ingest.md), these separate columns will be populated with the corresponding attribute values.

1. Configure an AWS Secrets Manager secret for your Aurora DB cluster by following the steps at [Password management with Amazon Aurora and AWS Secrets Manager](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html).

1. Take note of the following information after you create your DB cluster and set up the secret.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)

------
#### [ Neptune Analytics graphs (GraphRAG) ]

1. To create a graph and vector store in Neptune Analytics in the AWS Management Console, follow the steps described in [Vector indexing in Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/vector-index.html) in the *Neptune Analytics User Guide*.
**Note**  
To use Neptune GraphRAG, create an empty Neptune Analytics graph with a vector search index. The vector search index can only be created when the graph is created. When you create a [Neptune Analytics graph in the console](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/create-graph-using-console.html), you specify the index dimension under **Vector search settings** near the end of the process.

   Note the following considerations while creating the graph:

   1. Give the graph a name of your choice.

   1. Under **Data source**, choose **Create empty graph**, and specify the number of m-NCUs to be allocated. Each m-NCU has around one GiB of memory capacity and corresponding compute and networking.
**Note**  
The capacity of your graph can be modified later. We recommend that you start with the smallest instance and later choose a different instance, if needed.

   1. You can leave the default network connectivity settings. Amazon Bedrock will create a networking connection to the Neptune Analytics graph that you associate the knowledge base with. You do not have to configure public connectivity or private endpoints for your graph.

   1. Under **Vector search settings**, choose **Use vector dimension** and specify the number of dimensions in each vector.
**Note**  
The number of dimensions in each vector must match the vector dimensions in the embeddings model. Refer to the following table to determine how many dimensions the vector should contain:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)

   1. Leave all other settings to their default and create the graph.

1. Once the graph is created, choose it to take note of the **Resource ARN** and **Vector dimensions** for when you create the knowledge base. When choosing the embeddings model in Amazon Bedrock, make sure that you choose a model with the same dimensions as the **Vector dimensions** you configured on your Neptune Analytics graph.

After the vector index is created, you can proceed to [create your knowledge base](knowledge-base-create.md). The following table summarizes where you will enter each piece of information that you took note of.


| Field | Corresponding field in knowledge base setup (Console) | Corresponding field in knowledge base setup (API) | Description | 
| --- | --- | --- | --- | 
| Graph ARN | Neptune Analytics Graph ARN | graphARN | The Amazon Resource Name (ARN) of the Neptune Analytics graph. | 
| Metadata management (first mapping field) | Text field name | textField | The name of the field in which to store the raw text from your data sources. You can provide any value for this field, for example, text. | 
| Metadata management (second mapping field) | Bedrock-managed metadata field | metadataField | The name of the field in which to store metadata that Amazon Bedrock manages. You can provide any value for this field, for example, metadata. | 

------
#### [ Pinecone ]

**Note**  
If you use Pinecone, you agree to authorize AWS to access the designated third-party source on your behalf to provide vector store services to you. You're responsible for complying with any third-party terms applicable to use and and transfer of data from the third-party service.

For detailed documentation on setting up a vector store in Pinecone, see [Pinecone as a knowledge base for Amazon Bedrock](https://docs.pinecone.io/docs/amazon-bedrock).

While you set up the vector store, take note of the following information, which you will fill out when you create a knowledge base:
+ **Endpoint URL** – The endpoint URL for your index management page.
+ **Credentials secret ARN** – The Amazon Resource Name (ARN) of the secret that you created in AWS Secrets Manager that contains the username and password for a database user.
+ **(Optional) Customer-managed KMS key for your Credentials secret ARN** – if you encrypted your credentials secret ARN, provide the KMS key so that Amazon Bedrock can decrypt it. 
+ **Name Space** – (Optional) The namespace to be used to write new data to your database. For more information, see [Using namespaces](https://docs.pinecone.io/docs/namespaces).

There are additional configurations that you must provide when creating a Pinecone index:
+ **Text field name** – The name of the field which Amazon Bedrock should store the raw chunk text in.
+ **Metadata field name** – The name of the field which Amazon Bedrock should store source attribution metadata in.

To access your Pinecone index, you must provide your Pinecone API key to Amazon Bedrock through the AWS Secrets Manager.

**To set up a secret for your Pinecone configuration**

1. Follow the steps at [Create an AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html), setting the key as `apiKey` and the value as the API key to access your Pinecone index.

1. To find your API key, open your [Pinecone console](https://app.pinecone.io/) and select **API Keys**.

1. After you create the secret, take note of the ARN of the KMS key.

1. Attach permissions to your service role to decrypt the ARN of the KMS key by following the steps in [Permissions to decrypt an AWS Secrets Manager secret for the vector store containing your knowledge base](encryption-kb.md#encryption-kb-3p).

1. Later, when you create your knowledge base, enter the ARN in the **Credentials secret ARN** field.

------
#### [ Redis Enterprise Cloud ]

**Note**  
If you use Redis Enterprise Cloud, you agree to authorize AWS to access the designated third-party source on your behalf to provide vector store services to you. You're responsible for complying with any third-party terms applicable to use and transfer of data from the third-party service.

For detailed documentation on setting up a vector store in Redis Enterprise Cloud, see [Integrating Redis Enterprise Cloud with Amazon Bedrock](https://docs.redis.com/latest/rc/cloud-integrations/aws-marketplace/aws-bedrock/).

While you set up the vector store, take note of the following information, which you will fill out when you create a knowledge base:
+ **Endpoint URL** – The public endpoint URL for your database.
+ **Vector index name** – The name of the vector index for your database.
+ **Vector field** – The name of the field where the vector embeddings will be stored. Refer to the following table to determine how many dimensions the vector should contain.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
+ **Text field** – The name of the field where the Amazon Bedrock stores the chunks of raw text.
+ **Bedrock-managed metadata field** – The name of the field where Amazon Bedrock stores metadata related to your knowledge base.

To access your Redis Enterprise Cloud cluster, you must provide your Redis Enterprise Cloud security configuration to Amazon Bedrock through the AWS Secrets Manager.

**To set up a secret for your Redis Enterprise Cloud configuration**

1. Enable TLS to use your database with Amazon Bedrock by following the steps at [Transport Layer Security (TLS)](https://docs.redis.com/latest/rc/security/database-security/tls-ssl/).

1. Follow the steps at [Create an AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html). Set up the following keys with the appropriate values from your Redis Enterprise Cloud configuration in the secret:
   + `username` – The username to access your Redis Enterprise Cloud database. To find your username, look under the **Security** section of your database in the [Redis Console](http://app.redislabs.com/).
   + `password` – The password to access your Redis Enterprise Cloud database. To find your password, look under the **Security** section of your database in the [Redis Console](http://app.redislabs.com/).
   + `serverCertificate` – The content of the certificate from the Redis Cloud Certificate authority. Download the server certificate from the Redis Admin Console by following the steps at [Download certificates](https://docs.redis.com/latest/rc/security/database-security/tls-ssl/#download-certificates).
   + `clientPrivateKey` – The private key of the certificate from the Redis Cloud Certificate authority. Download the server certificate from the Redis Admin Console by following the steps at [Download certificates](https://docs.redis.com/latest/rc/security/database-security/tls-ssl/#download-certificates).
   + `clientCertificate` – The public key of the certificate from the Redis Cloud Certificate authority. Download the server certificate from the Redis Admin Console by following the steps at [Download certificates](https://docs.redis.com/latest/rc/security/database-security/tls-ssl/#download-certificates).

1. After you create the secret, take note of its ARN. Later, when you create your knowledge base, enter the ARN in the **Credentials secret ARN** field.

------
#### [ MongoDB Atlas ]

**Note**  
If you use MongoDB Atlas, you agree to authorize AWS to access the designated third-party source on your behalf to provide vector store services to you. You're responsible for complying with any third-party terms applicable to use and and transfer of data from the third-party service.

For detailed documentation on setting up a vector store in MongoDB Atlas, see [Launch a Fully Managed RAG Workflow With MongoDB Atlas and Amazon Bedrock](https://www.mongodb.com/developer/products/atlas/rag-workflow-with-atlas-amazon-bedrock/).

When you set up the vector store, note the following information which you will add when you create a knowledge base:
+ **Endpoint URL** – The endpoint URL of your MongoDB Atlas cluster.
+ **Database name** – The name of the database in your MongoDB Atlas cluster.
+ **Collection name** – The name of the collection in your database.
+ **Credentials secret ARN** – The Amazon Resource Name (ARN) of the secret that you created in AWS Secrets Manager that contains the username and password for a database user in your MongoDB Atlas cluster. The secret must contain keys named `username` and `password`.
+ **(Optional) Customer-managed KMS key for your Credentials secret ARN** – if you encrypted your credentials secret ARN, provide the KMS key so that Amazon Bedrock can decrypt it. 

There are additional configurations for **Field mapping** that you must provide when creating a MongoDB Atlas index:
+ **Vector index name** – The name of the MongoDB Atlas Vector Search Index on your collection.
+ **Vector field name** – The name of the field which Amazon Bedrock should store vector embeddings in.
+ **Text field name** – The name of the field which Amazon Bedrock should store the raw chunk text in.
+ **Metadata field name** – The name of the field which Amazon Bedrock should store source attribution metadata in.
+ **(Optional) Text search index name** – The name of the MongoDB Atlas Search index on your collection.

**Important**  
If you plan to use metadata filtering with your MongoDB Atlas knowledge base, you must manually configure filters in your vector index. Metadata filtering doesn't work by default and requires additional setup in your MongoDB Atlas vector index configuration.

(Optional) To have Amazon Bedrock connect to your MongoDB Atlas cluster over AWS PrivateLink, see [ RAG workflow with MongoDB Atlas using Amazon Bedrock](https://www.mongodb.com/developer/products/atlas/rag-workflow-with-atlas-amazon-bedrock/).

------