

# Set up your query engine and permissions for creating a knowledge base with structured data store
<a name="knowledge-base-prereq-structured"></a>

This topic describes the permissions that you need when connecting your knowledge base to a structured data store. If you plan to connect an Amazon Bedrock knowledge base to a structured data store, you need to fulfill the prerequisites. For general permissions requirements to be fulfilled, see [Set up permissions for a user or role to create and manage knowledge bases](knowledge-base-prereq-permissions-general.md).

**Important**  
Executing arbitrary SQL queries can be a security risk for any Text-to-SQL application. We recommend that you take precautions as needed, such as using restricted roles, read-only databases, and sandboxing.

Amazon Bedrock Knowledge Bases uses Amazon Redshift as the query engine for querying your data store. A query engine accesses metadata from a structured data store and uses the metadata to help generate SQL queries. Amazon Redshift is a data warehouse service that uses SQL to analyze structured data across data warehouses, databases, and data lakes.

## Create Amazon Redshift query engine
<a name="kb-query-engine-setup-create"></a>

You can use Amazon Redshift Serverless or Amazon Redshift Provisioned depending on your use case, and connect to workgroups or clusters for your data warehouse. The underlying data that the Amazon Redshift engine can query can be data natively stored in Amazon Redshift clusters, or data located under the default AWS Glue Data Catalog (such as in Amazon S3 among others).

If you've already created a query engine, you can skip this prerequisite. Otherwise, perform the following steps to set up your Amazon Redshift provisioned or Amazon Redshift Serverless query engine:

**To set up a query engine in Amazon Redshift provisioned**

1. Follow the procedure in [Step 1: Create a sample Amazon Redshift cluster](https://docs.aws.amazon.com/redshift/latest/gsg/new-user.html#rs-gsg-launch-sample-cluster) in the Amazon Redshift Getting Started Guide.

1. Note the cluster ID.

1. (Optional) For more information about Amazon Redshift provisioned clusters, see [Amazon Redshift provisioned clusters](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html) in the Amazon Redshift Management Guide.

**To set up a query engine in Amazon Redshift Serverless**

1. Follow only the setup procedure in [Creating a data warehouse with Amazon Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html#serverless-console-resource-creation) in the Amazon Redshift Getting Started Guide and configure it with default settings.

1. Note the workgroup ARN.

1. (Optional) For more information about Amazon Redshift Serverless workgroups, see [Workgroups and namespaces](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-workgroup-namespace.html) in the Amazon Redshift Management Guide.

## Configure Amazon Redshift query engine permissions
<a name="kb-query-engine-setup-redshift-permissions"></a>

Depending on the Amazon Redshift query engine that you choose, you can configure certain permissions. The permissions that you configure depend on the authentication method. The following table shows the authentication methods that can be used for different query engines:


****  

| Authentication method | Amazon Redshift Provisioned | Amazon Redshift Serverless | 
| --- | --- | --- | 
| IAM | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | 
| Database username | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png)No | 
| AWS Secrets Manager | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | 

Amazon Bedrock Knowledge Bases uses a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) to connect knowledge bases to structured data stores, retrieve data from these data stores, and generate SQL queries based on user queries and the structure of the data stores.

**Note**  
If you plan to use the AWS Management Console to create a knowledge base, you can skip this prerequisite. The console will create an Amazon Bedrock Knowledge Bases service role with the proper permissions.

To create a custom IAM service role with the proper permissions, follow the steps at [Create a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) and attach the trust relationship defined in [Trust relationship](kb-permissions.md#kb-permissions-trust).

Then, add permissions for your knowledge base to access your Amazon Redshift query engine and databases. Expand the section that applies to your use case:

### Your query engine is Amazon Redshift provisioned
<a name="w2aac32c12c27c13c11c15b1"></a>

Attach the following policy to your custom service role to allow it to access your data and generate queries using it:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RedshiftDataAPIStatementPermissions",
            "Effect": "Allow",
            "Action": [
                "redshift-data:GetStatementResult",
                "redshift-data:DescribeStatement",
                "redshift-data:CancelStatement"
            ],
            "Resource": [
                "*"
            ],
            "Condition": {
                "StringEquals": {
                    "redshift-data:statement-owner-iam-userid": "{{${aws:userid}}}"
                }
            }
        },
        {
            "Sid": "RedshiftDataAPIExecutePermissions",
            "Effect": "Allow",
            "Action": [
                "redshift-data:ExecuteStatement"
            ],
            "Resource": [
                "arn:aws:redshift:{{us-east-1}}:{{123456789012}}:cluster:{{${Cluster}}}"
            ]
        },
        {
            "Sid": "SqlWorkbenchAccess",
            "Effect": "Allow",
            "Action": [
                "sqlworkbench:GetSqlRecommendations",
                "sqlworkbench:PutSqlGenerationContext",
                "sqlworkbench:GetSqlGenerationContext",
                "sqlworkbench:DeleteSqlGenerationContext"
            ],
            "Resource": "*"
        },
        {
            "Sid": "GenerateQueryAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:GenerateQuery"
            ],
            "Resource": "*"
        }
    ]
}
```

------

You also need to add permissions to allow your service role to authenticate to the query engine. Expand a section to see the permissions for that method.

------
#### [ IAM ]

To allow your service role to authenticate to your Amazon Redshift provisioned query engine with IAM, attach the following policy to your custom service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "GetCredentialsWithFederatedIAMCredentials",
            "Effect": "Allow",
            "Action": "redshift:GetClusterCredentialsWithIAM",
            "Resource": [
                "arn:aws:redshift:{{us-east-1}}:{{123456789012}}:dbname:{{Cluster}}/{{database}}"
            ]
        }
    ]
}
```

------

------
#### [ Database user ]

To authenticate as an Amazon Redshift database user, attach the following policy to the service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "GetCredentialsWithClusterCredentials",
            "Effect": "Allow",
            "Action": [
                "redshift:GetClusterCredentials"
            ],
            "Resource": [
                "arn:aws:redshift:{{us-east-1}}:{{123456789012}}:dbuser:{{${cluster}}}/{{${dbuser}}}",
                "arn:aws:redshift:{{us-east-1}}:{{123456789012}}:dbname:{{${cluster}}}/{{${database}}}"
            ]
        }
    ]
}
```

------

------
#### [ AWS Secrets Manager ]

To allow your service role to authenticate to your Amazon Redshift provisioned query engine with an AWS Secrets Manager secret, do the following:
+ Attach the following policy to the role:

  ```
  {
      "Version": "2012-10-17",		 	 	 
      "Statement": [
          {
              "Sid": "GetSecretPermissions",
              "Effect": "Allow",
              "Action": [
                  "secretsmanager:GetSecretValue"
              ],
              "Resource": [
                  "arn:aws:secretsmanager:{{${region}}}:{{${account}}}:secret:{{${secretName}}}"
              ]
          }
      ]
  }
  ```

------

### Your query engine is Amazon Redshift Serverless
<a name="w2aac32c12c27c13c11c15b3"></a>

The permissions to attach depend on your authentication method. Expand a section to see the permissions for a method.

------
#### [ IAM ]

To allow your service role to authenticate to your Amazon Redshift serverless query engine with IAM, attach the following policy to your custom service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RedshiftServerlessGetCredentials",
            "Effect": "Allow",
            "Action": "redshift-serverless:GetCredentials",
            "Resource": [
                "arn:aws:redshift-serverless:{{us-east-1}}:{{123456789012}}:workgroup/{{WorkgroupId}}"
            ]
        }
    ]
}
```

------

------
#### [ AWS Secrets Manager ]

To allow your service role to authenticate to your Amazon Redshift provisioned query engine with an AWS Secrets Manager secret, do the following:
+ Attach the following policy to the role:

  ```
  {
      "Version": "2012-10-17",		 	 	 
      "Statement": [
          {
              "Sid": "GetSecretPermissions",
              "Effect": "Allow",
              "Action": [
                  "secretsmanager:GetSecretValue"
              ],
              "Resource": [
                  "arn:aws:secretsmanager:{{${region}}}:{{${account}}}:secret:{{${secretName}}}"
              ]
          }
      ]
  }
  ```

------

## Allow knowledge base service role to access your data store
<a name="knowledge-base-prereq-structured-db-access"></a>

Make sure your data is stored in one of the following [supported structured data stores](knowledge-base-structured-create.md):
+ Amazon Redshift
+ AWS Glue Data Catalog (AWS Lake Formation)

The following table summarizes the authentication methods available for the query engine, depending on your data store:


****  

| Authentication method | Amazon Redshift | AWS Glue Data Catalog (AWS Lake Formation) | 
| --- | --- | --- | 
| IAM | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | 
| Database username | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png)No | 
| AWS Secrets Manager | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png)Yes | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png)No | 

To learn how to set up permissions for your Amazon Bedrock Knowledge Bases service role to access your data store and generate queries based on it, expand the section that corresponds to the service that your data store is in:

### Amazon Redshift
<a name="w2aac32c12c27c13c13c13b1"></a>

To grant your Amazon Bedrock Knowledge Bases service role access to your Amazon Redshift database, use the [Amazon Redshift query editor v2](https://docs.aws.amazon.com/redshift/latest/mgmt/query-editor-v2.html) and run the following SQL commands:

1. (If you authenticate with IAM and a user wasn't already created for your database) Run the following command, which uses [CREATE USER](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html) to create a database user and allow it to authenticate through IAM, replacing {{${service-role}}} with the name of the custom Amazon Bedrock Knowledge Bases service role you created:

   ```
   CREATE USER "IAMR:{{${service-role}}}" WITH PASSWORD DISABLE;
   ```
**Important**  
If you use the Amazon Bedrock Knowledge Bases service role created for you in the console and then [sync your data store](kb-data-source-structured-sync-ingest.md) before you do this step, the user will be created for you, but the sync will fail because the user hasn't been granted permissions to access your data store. You must carry out the following step before syncing.

1. Grant an identity permissions to retrieve information from your database by running the [GRANT](https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html) command.

------
#### [ IAM ]

   ```
   GRANT SELECT ON ALL TABLES IN SCHEMA {{${schemaName}}} TO "IAMR:{{${serviceRole}}}";
   ```

------
#### [ Database user ]

   ```
   GRANT SELECT ON ALL TABLES IN SCHEMA {{${schemaName}}} TO "{{${dbUser}}}";
   ```

------
#### [ AWS Secrets Manager username ]

   ```
   GRANT SELECT ON ALL TABLES IN SCHEMA {{${schemaName}}} TO "{{${secretsUsername}}}";
   ```

------
**Important**  
Don't grant `CREATE`, `UPDATE`, or `DELETE` access. Granting these actions can lead to unintended modification of your data.

   For finer-grained control on the tables that can be accessed, you can replace `ALL TABLES` specific table names with the following notation: {{${schemaName}}}{{${tableName}}}. For more information about this notation, see the **Query objects** section at [Cross-database queries](https://docs.aws.amazon.com/redshift/latest/dg/cross-database-overview.html).

------
#### [ IAM ]

   ```
   GRANT SELECT ON {{${schemaName}}}.{{${tableName}}} TO "IAMR:{{${serviceRole}}}";
   ```

------
#### [ Database user ]

   ```
   GRANT SELECT ON {{${schemaName}}}.{{${tableName}}} TO "{{${dbUser}}}";
   ```

------
#### [ AWS Secrets Manager username ]

   ```
   GRANT SELECT ON {{${schemaName}}}.{{${tableName}}} TO "{{${secretsUsername}}}";
   ```

------

1. If you created a new schema in the Redshift database, run the following command to grant an identity permissions against the new schema.

   ```
   GRANT USAGE ON SCHEMA ${schemaName} TO "IAMR:${serviceRole}";
   ```

### AWS Glue Data Catalog
<a name="w2aac32c12c27c13c13c13b3"></a>

To grant your Amazon Bedrock Knowledge Bases service role access to your AWS Glue Data Catalog data store, use the [Amazon Redshift query editor v2](https://docs.aws.amazon.com/redshift/latest/mgmt/query-editor-v2.html) and run the following SQL commands:

1. Run the following command, which uses [CREATE USER](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html) to create a database user and allow it to authenticate through IAM, replacing {{${service-role}}} with the name of the custom Amazon Bedrock Knowledge Bases service role you created:

   ```
   CREATE USER "IAMR:{{${service-role}}}" WITH PASSWORD DISABLE;
   ```
**Important**  
If you use the Amazon Bedrock Knowledge Bases service role created for you in the console and then [sync your data store](kb-data-source-structured-sync-ingest.md) before you do this step, the user will be created for you, but the sync will fail because the user hasn't been granted permissions to access your data store. You must carry out the following step before syncing.

1. Grant the service role permissions to retrieve information from your database by running the following [GRANT](https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html) command:

   ```
   GRANT USAGE ON DATABASE awsdatacatalog TO "IAMR:{{${serviceRole}}}";
   ```
**Important**  
Don't grant `CREATE`, `UPDATE`, or `DELETE` access. Granting these actions can lead to unintended modification of your data.

1. To allow access to your AWS Glue Data Catalog databases, attach the following permissions to the service role:

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "VisualEditor0",
               "Effect": "Allow",
               "Action": [
                   "glue:GetDatabases",
                   "glue:GetDatabase",
                   "glue:GetTables",
                   "glue:GetTable",
                   "glue:GetPartitions",
                   "glue:GetPartition",
                   "glue:SearchTables"
               ],
               "Resource": [
                   "arn:aws:glue:{{us-east-1}}:{{123456789012}}:table/{{${DatabaseName}}}/{{${TableName}}}",
                   "arn:aws:glue:{{us-east-1}}:{{123456789012}}:database/{{${DatabaseName}}}",
                   "arn:aws:glue:{{us-east-1}}:{{123456789012}}:catalog"
               ]
           }
       ]
   }
   ```

------

1. Grant permissions to your service role through AWS Lake Formation (to learn more about Lake Formation and its relationship with Amazon Redshift, see [Data sources for Redshift](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-source.html)) by doing the following:
**Important**  
You must also add the `lakeformation:GetDataAccess` action to your Amazon Bedrock Knowledge Bases service role's IAM policy. Without this permission, queries to the knowledge base will fail with an authorization error. Add the following statement to the service role policy:  

   ```
   {
       "Effect": "Allow",
       "Action": "lakeformation:GetDataAccess",
       "Resource": "*"
   }
   ```

   1. Sign in to the AWS Management Console, and open the Lake Formation console at [https://console.aws.amazon.com/lakeformation/](https://console.aws.amazon.com/lakeformation/).

   1. Select **Data permissions** from the left navigation pane.

   1. Grant permissions to the service role you're using for Amazon Bedrock Knowledge Bases.

   1. Grant **Describe** and **Select** permissions for your databases and tables.

1. Depending on the data source you use in AWS Glue Data Catalog, you might need to add permissions to access that data source (for more information, see [AWS Glue dependency on other AWS services](https://docs.aws.amazon.com/glue/latest/dg/dependency-on-other-services.html)). For example, if your data source is in an Amazon S3 location, you'll need to add the following statement to the policy above.

   ```
   {
       "Sid": "Statement1",
       "Effect": "Allow",
       "Action": [
           "s3:ListBucket",
           "s3:GetObject"
       ],
       "Resource": [
           "arn:aws:s3:::{{${BucketName}}}",
           "arn:aws:s3:::{{${BucketName}}}/*"
       ]
   }
   ```

1. (Optional) If you use AWS KMS to encrypt the data in Amazon S3 or AWS Glue Data Catalog, then you need to add permissions to the role to decrypt the data on the KMS key.

   ```
   {
       "Action": [
           "kms:Decrypt"
       ],
       "Resource": [
           "arn:aws:kms:${Region}:${Account}:key/{KmsId}",
           "arn:aws:kms:${Region}:${Account}:key/{KmsId}"
       ],
       "Effect": "Allow"
   }
   ```