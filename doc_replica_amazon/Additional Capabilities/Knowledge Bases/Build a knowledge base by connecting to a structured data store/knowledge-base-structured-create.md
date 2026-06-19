

# Create a knowledge base by connecting to a structured data store
<a name="knowledge-base-structured-create"></a>

To connect a knowledge base to a structured data store, you specify the following components:
+ 

**Query engine configuration**  
The configuration for the compute service that will execute the generated SQL querries. The query engine is used to convert natural language user queries into SQL queries that can be used to extract data from your data store. You can choose Amazon Redshift as your query engine. When choosing this configuration, you must specify:
  + The compute connnection metadata such as the cluster ID or the workgroup ARN depending on the chosen query engine.
  + The authentication method for using the query engine, which can be using an IAM service role with the appropriate permissions, a query engine database user, or an AWS Secrets Manager secret that is linked to your database credentials.
+ 

**Storage configuration**  
The configuration for the data store containing your data. You can connect to Amazon Redshift Provisioned or Amazon Redshift Serverless and use Amazon Redshift or AWS Glue Data Catalog as your data store.
+ 

**(Optional) Query configurations**  
You can use optional query configurations for improving the accuracy of SQL generation:
  + **Maximum query time** – The amount of time after which the query times out.
  + **Descriptions** – Provides metadata or supplementary information about tables or columns. You can include descriptions of the tables or columns, usage notes, or any additional attributes. The descriptions you add can improve SQL query generation by providing extra context and information about the structure of the tables or columns.
  + **Inclusions and Exclusions** – Specifies a set of tables or columns to be included or excluded for SQL generation. This field is crucial if you want to limit the scope of SQL queries to a defined subset of available tables or columns. This option can help optimize the generation process by reducing unnecessary table or column references.

    If you specify inclusions, all other tables and columns are ignored. If you specify exclusions, the tables and columns you specify are ignored.
**Note**  
Inclusions and exclusions aren't a substitute for guardrails and is only intended for improving model accuracy.
  + **Curated queries** – A set of predefined question and answer examples. Questions are written as natural language queries (NLQ) and answers are the corresponding SQL query. These examples help the SQL generation process by providing examples of the kinds of queries that should be generated. They serve as reference points to improve the accuracy and relevance of generative SQL outputs.

Expand the section that corresponds to your use case:

## Use the console
<a name="knowledge-base-structured-create-console"></a>

To connect to a structured data store using the AWS Management Console, do the following:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Knowledge bases**.

1. In the **Knowledge bases** section, choose **Create** and then select **Knowledge base with structured data store**.

1. Set up the following details for the knowledge base:

   1. (Optional) Change the default name and provide a description for your knowledge base.

   1. Select the query engine to use for retrieving data from your data store.

   1. Choose an IAM service role with the proper permissions to create and manage this knowledge base. You can let Amazon Bedrock create the service role or choose a custom role that you have created. For more information about creating a custom role, see [Set up your query engine and permissions for creating a knowledge base with structured data store](knowledge-base-prereq-structured.md).

   1. (Optional) Add tags to associate with your knowledge base. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

   1. Choose **Next**.

1. Configure your query engine:

   1. Select the service in which you created a cluster or workgroup. Then choose the cluster or workgroup to use.

   1. Select the authentication method and provide the necessary fields.

   1. Select the data store in which to store your metadata. Then, choose or enter the name of the database.

   1. (Optional) Modify the query configurations as necessary. Refer to the beginning of this topic for more information about different configurations.

   1. Choose **Next**.

1. Review your knowledge base configurations and edit any sections as necessary. Confirm to create your knowledge base.

## Use the API
<a name="knowledge-base-structured-create-api"></a>

To connect to a structured data store using the Amazon Bedrock API, send a [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) with the following general request body:

```
{
    "name": "string",
    "roleArn": "string",
    "knowledgeBaseConfiguration": {
        "type": "SQL",
        "sqlKnowledgeBaseConfiguration": [SqlKnowledgeBaseConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_SqlKnowledgeBaseConfiguration.html)
    },
    "description": "string",
    "clientToken": "string",
    "tags": {
        "string": "string"
    }
}
```

The following fields are required.


****  

| Field | Basic description | 
| --- | --- | 
| Name | A name for the knowledge base | 
| roleArn | A [knowledge base service role](kb-permissions.md) with the proper permissions. You can use the console to automatically create a service role with the proper permissions. | 
| knowledgeBaseConfiguration | Contains configurations for the knowledge base. For a structured database, specify SQL as the type and include the sqlKnowledgeBaseConfiguration field. | 

The following fields are optional.


****  

| Field | Use | 
| --- | --- | 
| description | To include a description for the knowledge base. | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 
| tags | To associate tags with the flow. For more information, see [Tagging Amazon Bedrock resources](tagging.md). | 

The `SQLKnowledgeBaseConfiguration` depends on the query engine that you use. For Amazon Redshift, specify the `type` field as `REDSHIFT` and include the `redshiftConfiguration` field, which maps to a [RedshiftConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftConfiguration.html). For the [RedshiftConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftConfiguration.html), you configure the following fields:

### queryEngineConfiguration
<a name="w2aac32c12c27c15b9b3c17b1"></a>

You can configure the following types of query engine:

#### Amazon Redshift Provisioned
<a name="w2aac32c12c27c15b9b3c17b1b5b1"></a>

If your Amazon Redshift databases are provisioned on dedicated compute nodes, the value of the `queryEngineConfiguration` field should be a [RedshiftQueryEngineConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftQueryEngineConfiguration.html) in the following format:

```
{
    "type": "PROVISIONED",
    "provisionedConfiguration": {
        "clusterIdentifier": "string",
        "authConfiguration": [RedshiftProvisionedAuthConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftProvisionedAuthConfiguration.html)
    },
}
```

Specify the ID of the cluster in the `clusterIdentifier` field. The [RedshiftProvisionedAuthConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftProvisionedAuthConfiguration.html) depends on the type of authorization you're using. Select the tab that matches your authorization method:

------
#### [ IAM role ]

If you authorize with your IAM role, you need to specify only `IAM` as the type in the [RedshiftProvisionedAuthConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftProvisionedAuthConfiguration.html) with no additional fields.

```
{
    "type": "IAM"
}
```

------
#### [ Temporary credentials user name ]

If you authorize with the database user name, specify the `type` as `USERNAME` and specify the user name in the `databaseUser` field in the `RedshiftProvisionedAuthConfig`:

```
{
    "type": "USERNAME",
    "databaseUser": "string"
}
```

------
#### [ AWS Secrets Manager ]

If you authorize with AWS Secrets Manager, specify the `type` as `USERNAME_PASSWORD` and specify the ARN of the secret in the `usernamePasswordSecretArn` field in the `RedshiftProvisionedAuthConfig`:

```
{
    "type": "USERNAME_PASSWORD",
    "usernamePasswordSecretArn": "string"
}
```

------

#### Amazon Redshift Serverless
<a name="w2aac32c12c27c15b9b3c17b1b5b3"></a>

If you're using Amazon Redshift Serverless, the value of the `queryConfiguration`field should be a [RedshiftQueryEngineConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftQueryEngineConfiguration.html) in the following format:

```
{
    "type": "SERVERLESS",
    "serverlessConfiguration": {
        "workgroupArn": "string",
        "authConfiguration": 
    }
}
```

Specify the ARN of your workgroup in the `workgroupArn` field. The [RedshiftServerlessAuthConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftServerlessAuthConfiguration.html) depends on the type of authorization you're using. Select the tab that matches your authorization method:

------
#### [ IAM role ]

If you authorize with your IAM role, you need to specify only `IAM` as the type in the `RedshiftServerlessAuthConfiguration` with no additional fields.

```
{
    "type": "IAM"
}
```

------
#### [ AWS Secrets Manager ]

If you authorize with AWS Secrets Manager, specify the `type` as `USERNAME_PASSWORD` and specify the ARN of the secret in the `usernamePasswordSecretArn` field in the `RedshiftServerlessAuthConfiguration`:

```
{
    "type": "USERNAME_PASSWORD",
    "usernamePasswordSecretArn": "string"
}
```

------

### storageConfigurations
<a name="w2aac32c12c27c15b9b3c17b3"></a>

This field maps to an array containing a single [RedshiftQueryEngineStorageConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_RedshiftQueryEngineStorageConfiguration.html), whose format depends on where your data is stored.

#### AWS Glue Data Catalog
<a name="w2aac32c12c27c15b9b3c17b3b5b1"></a>

If your data is stored in AWS Glue Data Catalog, the `RedshiftQueryEngineStorageConfiguration` should be in the following format:

```
{
    "type": "AWS_DATA_CATALOG",
    "awsDataCatalogConfiguration": {
        "tableNames": ["string"]
    }
}
```

Add the name of each table that you want to connect your knowledge base to in the array that `tableNames` maps to.

**Note**  
Enter table names in the pattern described in [Cross-database queries](https://docs.aws.amazon.com/redshift/latest/dg/cross-database-overview.html) (`${databaseName}.${tableName}`). You can include all tables by specifying `${databaseName.*}`.

#### Amazon Redshift databases
<a name="w2aac32c12c27c15b9b3c17b3b5b3"></a>

If your data is stored in an Amazon Redshift database, the `RedshiftQueryEngineStorageConfiguration` should be in the following format:

```
{
    "type": "string",
    "redshiftConfiguration": {
        "databaseName": "string"
    }
}
```

Specify the name of your Amazon Redshift database in the `databaseName` field.

**Note**  
Enter table names in the pattern described in [Cross-database queries](https://docs.aws.amazon.com/redshift/latest/dg/cross-database-overview.html) (`${databaseName}.${tableName}`). You can include all tables by specifying `${databaseName.*}`.

If your database is mounted through Amazon SageMaker AI Lakehouse, the database name is in the format {{${db}@${schema}}}.

### queryGenerationConfiguration
<a name="w2aac32c12c27c15b9b3c17b5"></a>

This field maps to the following [QueryGenerationConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationConfiguration.html) that you can use to configure how your data is queried:

```
{
    "executionTimeoutSeconds": number,
    "generationContext": {
        "tables": [
            {
                "name": "string",
                "description": "string",
                "inclusion": "string",
                "columns": [
                    {
                        "name": "string",
                        "description": "string",
                        "inclusion": "string"
                    },
                    ...
                ]
            },
            ...
        ],
        "curatedQueries": [
            {
                "naturalLanguage": "string",
                "sql": "string"
            },
            ...
        ]
    }
}
```

If you want the query to time out, specify the timeout duration in seconds in the `executionTimeoutSeconds` field.

The `generationContext` field maps to a [QueryGenerationContext](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationContext.html) object in which you can configure as many of the following options as you need.

**Important**  
If you include a generation context, the query engine makes a best effort attempt to apply it when generating SQL. The generation context is non-deterministic and is only intended for improving model accuracy. To ensure accuracy, verify the generated SQL queries.

For information about generation contexts that you can include, expand the following sections:

#### Add descriptions for tables or columns in the database
<a name="w2aac32c12c27c15b9b3c17b5c15b1"></a>

To improve the accuracy of SQL generation for querying the database, you can provide a description for the table or column that provides more context than a short table or column name. You can do the following:
+ To add a description for a table, include a [QueryGenerationTable](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationTable.html) object in the `tables` array. In that object, specify the name of the table in the `name` field and a description in the `description` field, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "description": "Description for Table A"
  }
  ```
+ To add a description for a column, include a [QueryGenerationTable](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationTable.html) object in the `tables` array. In that object, specify the name of the table in the `name` field and include the `columns` field, which maps to an array of [QueryGenerationColumn](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationColumn.html). In a `QueryGenerationColumn` object, include the name of the column in the `name` field and a description in the `description` field, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "columns": [
          {
              "name": "Column A",
              "description": "Description for Column A"
          }
      ]
  }
  ```
+ You can add a description for both a table and a column in it, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "description": "Description for Table A",
      "columns": [
          {
              "name": "columnA",
              "description": "Description for Column A"
          }
      ]
  }
  ```
**Note**  
Enter table and column names in the pattern described in [Cross-database queries](https://docs.aws.amazon.com/redshift/latest/dg/cross-database-overview.html). If your database is in AWS Glue Data Catalog, the format is `awsdatacatalog.gluedatabase.table`.

#### Include or exclude tables or columns in the database
<a name="w2aac32c12c27c15b9b3c17b5c15b3"></a>

You can suggest tables or columns to include or exclude when generating SQL by using the `inclusion` field in the [QueryGenerationTable](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationTable.html) and [QueryGenerationColumn](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationColumn.html) objects. You can specify one of the following values in the `inclusion` field:
+ INCLUDE – Only the tables or columns that you specify are included as context when generating SQL.
+ EXCLUDE – The tables or columns that you specify are excluded as context when generating SQL.

You can specify whether to include or exclude tables or columns in the following ways:
+ To include or exclude a table, include a [QueryGenerationTable](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationTable.html) object in the `tables` array. In that object, specify the name of the table in the `name` field and whether to include or exclude it in the `inclusion` field, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "inclusion": "EXCLUDE"
  }
  ```

  The query engine doesn't add `Table A` in the additional context for generating SQL.
+ To include or exclude a column, include a [QueryGenerationTable](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationTable.html) object in the `tables` array. In that object, specify the name of the table in the `name` field and include the `columns` field, which maps to an array of [QueryGenerationColumn](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationColumn.html). In a `QueryGenerationColumn` object, include the name of the column in the `name` field and whether to include or exclude it in the `inclusion` field, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "columns": [
          {
              "name": "database.schema.tableA.columnA",
              "inclusion": "EXCLUDE"
          }
      ]
  }
  ```

  The SQL generation ignores `Column A` in `Table A` in the context when generating SQL.
+ You can combine tables and columns when specifying inclusions or exclusions, as in the following example:

  ```
  {
      "name": "database.schema.tableA",
      "inclusion": "INCLUDE",
      "columns": [
          {
              "name": "database.schema.tableA.columnA",
              "inclusion": "EXCLUDE"
          }
      ]
  }
  ```

  SQL generation includes `Table A`, but excludes `Column A` within it when adding context for generating SQL.

**Important**  
Table and column exclusions aren't substitutes for guardrails. These table and column inclusions and exclusions are used as additional context for model to consider when generating SQL.

#### Give the query engine example mappings of natural language to SQL queries
<a name="w2aac32c12c27c15b9b3c17b5c15b5"></a>

To improve a query engine's accuracy in converting user queries into SQL queries, you can provide it examples in the `curatedQueries` field in the [QueryGenerationContext](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_QueryGenerationContext.html) object, which maps to an array of [CuratedQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CuratedQuery.html) objects. Each object contains the following fields:
+ naturalLanguage – An example of a query in natural language.
+ sql – The SQL query that corresponds to the natural language query.