

# Create a service role for Amazon Bedrock Knowledge Bases
<a name="kb-permissions"></a>

To use a custom role for a knowledge base instead of the one Amazon Bedrock automatically creates, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). Include only the necessary permissions for your own security.

**Note**  
A policy cannot be shared between multiple roles when the service role is used.
+ Trust relationship
+ Access to the Amazon Bedrock base models
+ Access to the data source for where you store your data
+ (If you create a vector database in Amazon OpenSearch Service) Access to your OpenSearch Service collection
+ (If you create a vector database in Amazon Aurora) Access to your Aurora cluster
+ (If you create a vector database in Pinecone or Redis Enterprise Cloud) Permissions for AWS Secrets Manager to authenticate your Pinecone or Redis Enterprise Cloud account
+ (Optional) If you encrypt any of the following resources with a KMS key, permissions to decrypt the key (see [Encryption of knowledge base resources](encryption-kb.md)).
  + Your knowledge base
  + Data sources for your knowledge base
  + Your vector database in Amazon OpenSearch Service
  + The secret for your third-party vector database in AWS Secrets Manager
  + A data ingestion job

**Topics**
+ [Trust relationship](#kb-permissions-trust)
+ [Permissions to access Amazon Bedrock models](#kb-permissions-access-models)
+ [Permissions to access your data sources](#kb-permissions-access-ds)
+ [Permissions to decrypt your AWS KMS key for encrypted data sources in Amazon S3](#kb-permissions-kms-datasource)
+ [Permissions to chat with your document](#kb-permissions-chatdoc)
+ [Permissions for multimodal content](#kb-permissions-multimodal)
+ [Permissions to access your Amazon Kendra GenAI index](#kb-permissions-kendra)
+ [Permissions to access your vector database in Amazon OpenSearch Serverless](#kb-permissions-oss)
+ [Permissions to access your vector database in OpenSearch Managed Clusters](#kb-permissions-osm)
+ [Permissions to access your Amazon Aurora database cluster](#kb-permissions-rds)
+ [Permissions to access your vector database in Amazon Neptune Analytics](#kb-permissions-neptune)
+ [Permissions to access your vector store in Amazon S3 Vectors](#kb-permissions-s3vectors)
+ [Permissions to access a vector database configured with an AWS Secrets Manager secret](#kb-permissions-secret)
+ [Permissions for AWS to manage a AWS KMS key for transient data storage during data ingestion](#kb-permissions-kms-ingestion)
+ [Permissions for AWS to manage a data sources from another user's AWS account.](#kb-permissions-otherds)

## Trust relationship
<a name="kb-permissions-trust"></a>

The following policy allows Amazon Bedrock to assume this role and create and manage knowledge bases. The following shows an example policy you can use. You can restrict the scope of the permission by using one or more global condition context keys. For more information, see [AWS global condition context keys.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) Set the `aws:SourceAccount` value to your account ID. Use the `ArnEquals` or `ArnLike` condition to restrict the scope to specific knowledge bases.

**Note**  
As a best practice for security purposes, replace the {{\*}} with specific knowledge base IDs after you have created them.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "{{123456789012}}"
                },
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{*}}"
                }
            }
        }
    ]
}
```

------

## Permissions to access Amazon Bedrock models
<a name="kb-permissions-access-models"></a>

Attach the following policy to provide permissions for the role to use Amazon Bedrock models to embed your source data.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:ListFoundationModels",
                "bedrock:ListCustomModels"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/amazon.titan-embed-text-v1",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/cohere.embed-english-v3",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/cohere.embed-multilingual-v3"
            ]
        }
    ]
}
```

------

## Permissions to access your data sources
<a name="kb-permissions-access-ds"></a>

Select from the following data sources to attach the necessary permissions for the role.

**Topics**
+ [Permissions to access your Amazon S3 data source](#kb-permissions-access-s3)
+ [Permissions to access your Confluence data source](#kb-permissions-access-confluence)
+ [Permissions to access your Microsoft SharePoint data source](#kb-permissions-access-sharepoint)
+ [Permissions to access your Salesforce data source](#kb-permissions-access-salesforce)
+ [Permissions to access your Web Crawler data source](#kb-permissions-access-webcrawler)
+ [Permissions to access your Microsoft OneDrive data source](#kb-permissions-access-onedrive)
+ [Permissions to access your Google Drive data source](#kb-permissions-access-googledrive)

### Permissions to access your Amazon S3 data source
<a name="kb-permissions-access-s3"></a>

If your data source is Amazon S3, attach the following policy to provide permissions for the role to access the S3 bucket that you will connect to as your data source.

If you encrypted the data source with a AWS KMS key, attach permissions to decrypt the key to the role by following the steps at [Permissions to decrypt your AWS KMS key for your data sources in Amazon S3](encryption-kb.md#encryption-kb-ds).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "S3ListBucketStatement",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        },
        {
            "Sid": "S3GetObjectStatement",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{123456789012}}"
                }
            }
        }
    ]
}
```

------

### Permissions to access your Confluence data source
<a name="kb-permissions-access-confluence"></a>

**Note**  
Confluence data source connector is in preview release and is subject to change.

Attach the following policy to provide permissions for the role to access Confluence.

**Note**  
`secretsmanager:PutSecretValue` is only necessary if you use OAuth 2.0 authentication with a refresh token.  
Confluence OAuth2.0 **access** token has a default expiry time of 60 minutes. If this token expires while your data source is syncing (sync job), Amazon Bedrock will use the provided **refresh** token to regenerate this token. This regeneration refreshes both the access and refresh tokens. To keep the tokens updated from the current sync job to the next sync job, Amazon Bedrock requires write/put permissions for your secret credentials.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue",
                "secretsmanager:PutSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Permissions to access your Microsoft SharePoint data source
<a name="kb-permissions-access-sharepoint"></a>

**Note**  
SharePoint data source connector is in preview release and is subject to change.

Attach the following policy to provide permissions for the role to access SharePoint.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Permissions to access your Salesforce data source
<a name="kb-permissions-access-salesforce"></a>

**Note**  
Salesforce data source connector is in preview release and is subject to change.

Attach the following policy to provide permissions for the role to access Salesforce.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Permissions to access your Web Crawler data source
<a name="kb-permissions-access-webcrawler"></a>

Attach the following policy to provide permissions for the role to access websites through the Web Crawler. If your website requires authentication, include permissions to access the AWS Secrets Manager secret that stores your credentials.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Permissions to access your Microsoft OneDrive data source
<a name="kb-permissions-access-onedrive"></a>

Attach the following policy to provide permissions for the role to access Microsoft OneDrive.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Permissions to access your Google Drive data source
<a name="kb-permissions-access-googledrive"></a>

Attach the following policy to provide permissions for the role to access Google Drive.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{SecretId}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{KeyId}}"
            ],
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "secretsmanager.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

## Permissions to decrypt your AWS KMS key for encrypted data sources in Amazon S3
<a name="kb-permissions-kms-datasource"></a>

If you encrypted your data sources in Amazon S3 with a AWS KMS key, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow Amazon Bedrock to decrypt your key. Replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the key belongs. Replace {{${KeyId}}} with the ID of your AWS KMS key.

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "kms:Decrypt"
        ],
        "Resource": [
            "arn:aws:kms:{{${Region}}}:{{${AccountId}}}:key/{{${KeyId}}}"
        ],
        "Condition": {
            "StringEquals": {
                "kms:ViaService": [
                    "s3.{{${Region}}}.amazonaws.com"
                ]
            }
        }
    }]
}
```

## Permissions to chat with your document
<a name="kb-permissions-chatdoc"></a>

Attach the following policy to provide permissions for the role to use Amazon Bedrock models to chat with your document:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
			"Effect": "Allow",
			"Action": [
				"bedrock:RetrieveAndGenerate"
			],
			"Resource": "*"
		}
    ]
}
```

------

If you only want to grant a user access to chat with your document (and not to `RetrieveAndGenerate` on all Knowledge Bases), use the following policy:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
			"Effect": "Allow",
			"Action": [
				"bedrock:RetrieveAndGenerate"
			],
			"Resource": "*"
		},
        {
			"Effect": "Deny",
			"Action": [
				"bedrock:Retrieve"
			],
			"Resource": "*"
		}
    ]
}
```

------

If you want both chat with your document and use `RetrieveAndGenerate` on a specific Knowledge Base, provide a {{${KnowledgeBaseArn}}}, and use the following policy:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/$KnowledgeBaseId"
        }
    ]
}
```

------

## Permissions for multimodal content
<a name="kb-permissions-multimodal"></a>

When working with multimodal content (images, audio, video), additional permissions are required depending on your processing approach.

### Nova Multimodal Embeddings permissions
<a name="kb-permissions-multimodal-mme"></a>

When using Nova Multimodal Embeddings, attach the following policy to provide permissions for asynchronous model invocation:

```
{
    "Sid": "BedrockInvokeModelStatement",
    "Effect": "Allow",
    "Action": ["bedrock:InvokeModel"],
    "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-*-multimodal-embeddings-*",
        "arn:aws:bedrock:us-east-1::async-invoke/*"
    ],
    "Condition": {
        "StringEquals": {
            "aws:ResourceAccount": ""
        }
    }
},
{
    "Sid": "BedrockGetAsyncInvokeStatement",
    "Effect": "Allow",
    "Action": ["bedrock:GetAsyncInvoke"],
    "Resource": ["arn:aws:bedrock:us-east-1::async-invoke/*"],
    "Condition": {
        "StringEquals": {
            "aws:ResourceAccount": ""
        }
    }
}
```

### Bedrock Data Automation (BDA) permissions
<a name="kb-permissions-multimodal-bda"></a>

When using BDA to process multimodal content, attach the following policy:

```
{
    "Sid": "BDAInvokeStatement",
    "Effect": "Allow",
    "Action": ["bedrock:InvokeDataAutomationAsync"],
    "Resource": [
        "arn:aws:bedrock:us-east-1:aws:data-automation-project/public-rag-default",
        "arn:aws:bedrock:us-east-1::data-automation-profile/*"
    ]
},
{
    "Sid": "BDAGetStatement",
    "Effect": "Allow",
    "Action": ["bedrock:GetDataAutomationStatus"],
    "Resource": "arn:aws:bedrock:us-east-1::data-automation-invocation/*"
}
```

If you use customer-managed AWS KMS keys with BDA, also attach the following policy. Replace {{account-id}}, {{region}}, and {{key-id}} with your specific values:

```
{
    "Sid": "KmsPermissionStatementForBDA",
    "Effect": "Allow",
    "Action": [
        "kms:GenerateDataKey",
        "kms:Decrypt",
        "kms:DescribeKey",
        "kms:CreateGrant"
    ],
    "Resource": ["arn:aws:kms:{{region}}:{{account-id}}:key/{{key-id}}"],
    "Condition": {
        "StringEquals": {
            "aws:ResourceAccount": "{{account-id}}",
            "kms:ViaService": "bedrock.{{region}}.amazonaws.com"
        }
    }
}
```

## Permissions to access your Amazon Kendra GenAI index
<a name="kb-permissions-kendra"></a>

If you created an Amazon Kendra GenAI index for your knowledge base, then attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the index. In the policy, replace {{${Partition}}}, {{${Region}}}, {{${AccountId}}}, and {{${IndexId}}} with the values for your index. You can allow access to multiple indexes by adding them to the `Resource` list. To allow access to every index in your AWS account, replace {{${IndexId}}} with a wildcard (\*).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kendra:Retrieve",
                "kendra:DescribeIndex"
            ],
            "Resource": "arn:aws:kendra:{{us-east-1}}:{{123456789012}}:index/{{${IndexId}}}" 
        }
    ]
}
```

------

## Permissions to access your vector database in Amazon OpenSearch Serverless
<a name="kb-permissions-oss"></a>

If you created a vector database in OpenSearch Serverless for your knowledge base, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the collection. Replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the database belongs. Input the ID of your Amazon OpenSearch Service collection in {{${CollectionId}}}. You can allow access to multiple collections by adding them to the `Resource` list.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "aoss:APIAccessAll"
            ],
            "Resource": [
                "arn:aws:aoss:{{us-east-1}}:{{123456789012}}:collection/{{${CollectionId}}}"
            ]
        }
    ]
}
```

------

## Permissions to access your vector database in OpenSearch Managed Clusters
<a name="kb-permissions-osm"></a>

If you created a vector database in OpenSearch Managed Cluster for your knowledge base, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the domain. Replace {{<region>}} and {{<accountId>}} with the Region and account ID to which the database belongs. You can allow access to multiple domains by adding them to the `Resource` list. For more information about configuring permissions, see [Prerequisites and permissions required for using OpenSearch Managed Clusters with Amazon Bedrock Knowledge BasesOverview of permissions configuration](kb-osm-permissions-prereq.md).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",       
            "Action": [
                "es:ESHttpGet", 
                "es:ESHttpPost", 
                "es:ESHttpPut", 
                "es:ESHttpDelete" 
            ],
            "Resource": [
                "arn:aws:es:{{us-east-1}}:{{123456789012}}:domain/{{domainName}}/{{indexName}}"
            ]       
        }, 
        {
            "Effect": "Allow",
            "Action": [
                "es:DescribeDomain" 
            ],
            "Resource": [
                "arn:aws:es:{{us-east-1}}:{{123456789012}}:domain/{{domainName}}"
            ]       
        }
    ]
}
```

------

## Permissions to access your Amazon Aurora database cluster
<a name="kb-permissions-rds"></a>

**Note**  
The Amazon Aurora cluster must reside in the same AWS account as the one where the knowledge base is created for Amazon Bedrock.

If you created a database (DB) cluster in Amazon Aurora for your knowledge base, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the DB cluster and to provide read and write permissions on it. Replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the DB cluster belongs. Input the ID of your Amazon Aurora database cluster in {{${DbClusterId}}}. You can allow access to multiple DB clusters by adding them to the `Resource` list.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "{{RdsDescribeStatementID}}",
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBClusters"
            ],
            "Resource": [
                "arn:aws:rds:{{us-east-1}}:{{123456789012}}:cluster:{{${DbClusterId}}}"
            ]
        },
        {
            "Sid": "DataAPIStatementID",
            "Effect": "Allow",
            "Action": [
                "rds-data:BatchExecuteStatement",
                "rds-data:ExecuteStatement"
            ],
            "Resource": [
                "arn:aws:rds:{{us-east-1}}:{{123456789012}}:cluster:{{${DbClusterId}}}"
            ]
        }
    ]
}
```

------

## Permissions to access your vector database in Amazon Neptune Analytics
<a name="kb-permissions-neptune"></a>

If you created an Amazon Neptune Analytics graph for your knowledge base, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the graph. In the policy, replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the database belongs. Replace {{${GraphId}}} with the values for your graph database.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "NeptuneAnalyticsAccess",
            "Effect": "Allow",
            "Action": [
                "neptune-graph:GetGraph",
                "neptune-graph:ReadDataViaQuery",
                "neptune-graph:WriteDataViaQuery",
                "neptune-graph:DeleteDataViaQuery"
            ],
            "Resource": [
                "arn:aws:neptune-graph:{{us-east-1}}:{{123456789012}}:graph/{{${GraphId}}}"
            ]
        }
    ]
}
```

------

## Permissions to access your vector store in Amazon S3 Vectors
<a name="kb-permissions-s3vectors"></a>

If you choose to use Amazon S3 Vectors for your knowledge base, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow access to the vector index.

In the policy, replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the vector index belongs. Replace {{${BucketName}}} with the name of your S3 vector bucket and {{${IndexName}}} with the name of your vector index. For more information about Amazon S3 Vectors, see [Setting up to use Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-setting-up.html).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "S3VectorBucketReadAndWritePermission",
            "Effect": "Allow",
            "Action": [
                "s3vectors:PutVectors",
                "s3vectors:GetVectors",
                "s3vectors:DeleteVectors",
                "s3vectors:QueryVectors",
                "s3vectors:GetIndex"
            ],
            "Resource": "arn:aws:s3vectors:{{us-east-1}}:{{123456789012}}:bucket/{{${BucketName}}}/index/{{${IndexName}}}"
        }
    ]
}
```

------

## Permissions to access a vector database configured with an AWS Secrets Manager secret
<a name="kb-permissions-secret"></a>

If your vector database is configured with an AWS Secrets Manager secret, attach the following policy to your Amazon Bedrock Knowledge Bases service role to allow AWS Secrets Manager to authenticate your account to access the database. Replace {{${Region}}} and {{${AccountId}}} with the Region and account ID to which the database belongs. Replace {{${SecretId}}} with the ID of your secret.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:{{us-east-1}}:{{123456789012}}:secret:{{${SecretId}}}"
            ]
        }
    ]
}
```

------

If you encrypted your secret with a AWS KMS key, attach permissions to decrypt the key to the role by following the steps at [Permissions to decrypt an AWS Secrets Manager secret for the vector store containing your knowledge base](encryption-kb.md#encryption-kb-3p).

## Permissions for AWS to manage a AWS KMS key for transient data storage during data ingestion
<a name="kb-permissions-kms-ingestion"></a>

To allow the creation of a AWS KMS key for transient data storage in the process of ingesting your data source, attach the following policy to your Amazon Bedrock Knowledge Bases service role. Replace the {{${Region}}}, {{${AccountId}}}, and {{${KeyId}}} with the appropriate values.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{${KeyId}}}"
            ]
        }
    ]
}
```

------

## Permissions for AWS to manage a data sources from another user's AWS account.
<a name="kb-permissions-otherds"></a>

To allow the access to another user's AWS account, you must create a role that allows cross-account access to a Amazon S3 bucket in another user's account. Replace the {{${BucketName}}}, {{${BucketOwnerAccountId}}}, and {{${BucketNameAndPrefix}}} with the appropriate values.

**Permissions Required on Knowledge Base role**

The knowledge base role that is provided during knowledge base creation `createKnowledgeBase` requires the following Amazon S3 permissions.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "S3ListBucketStatement",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::amzn-s3-demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "123456789012"
                }
            }
        },
        {
            "Sid": "S3GetObjectStatement",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::amzn-s3-demo-bucket/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "123456789012"
                }
            }
        }
    ]
}
```

------

If the Amazon S3 bucket is encrypted using a AWS KMS key, the following also needs to be added to the knowledge base role. Replace the {{${BucketOwnerAccountId}}} and {{${Region}}} with the appropriate values.

```
{
        "Sid": "KmsDecryptStatement",
        "Effect": "Allow",
        "Action": [
            "kms:Decrypt"
        ],
        "Resource": [
            "arn:aws:kms:{{${Region}}}:{{${BucketOwnerAccountId}}}:key/{{${KeyId}}}"
        ],
        "Condition": {
        "StringEquals": {
            "kms:ViaService": [
                "s3.{{${Region}}}.amazonaws.com"
            ]
        }
        }
    }
```

**Permissions required on a cross-account Amazon S3 bucket policy**

The bucket in the other account requires the following Amazon S3 bucket policy. Replace the {{${KbRoleArn}}}, {{${BucketName}}}, and {{${BucketNameAndPrefix}}} with the appropriate values. 

------
#### [ JSON ]

****  

```
{
   "Version":"2012-10-17",		 	 	 
   "Statement": [
      {
         "Sid": "ListBucket",
         "Effect": "Allow",
         "Principal": {
            "AWS": "{{123456789012}}"
         },
         "Action": [
            "s3:ListBucket"
         ],
         "Resource": [
            "arn:aws:s3:::{{amzn-s3-demo-bucket}}"
         ]
      },
      {
         "Sid": "GetObject",
         "Effect": "Allow",
         "Principal": {
            "AWS": "{{123456789012}}"
         },
         "Action": [
            "s3:GetObject"
         ],
         "Resource": [
            "arn:aws:s3:::{{amzn-s3-demo-bucket}}/*"
         ]
      }
   ]
}
```

------

**Permissions required on cross-account AWS KMS key policy**

If the cross-account Amazon S3 bucket is encrypted using a AWS KMS key in that account, the policy of the AWS KMS key requires the following policy. Replace the {{${KbRoleArn}}} and {{${KmsKeyArn}}} with the appropriate values.

```
{
    "Sid": "Example policy",
    "Effect": "Allow",
    "Principal": {
        "AWS": [
            "{{${KbRoleArn}}}"
        ]
    },
    "Action": [
        "kms:Decrypt"
    ],
    "Resource": "{{${KmsKeyArn}}}"
}
```