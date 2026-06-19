

# Prerequisites
<a name="kb-managed-prereqs"></a>

Amazon Bedrock managed knowledge bases require data and AWS Identity and Access Management permissions to access your data and perform actions. By default, managed knowledge bases use service-managed embedding and reranking models, so no Bedrock model access is required for those. If you provide your own embedding or reranking models, you also need access to those Bedrock models.

Before you can create a managed knowledge base, you must fulfill the following prerequisites. For general permissions requirements, see [Set up permissions for a user or role to create and manage knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-prereq-permissions-general.html)

1. Make sure your data is in a [supported data source connector](kb-managed-connect-ds.md).

1. Ensure that the IAM role used to create the knowledge base has the `iam:PassRole` permission to pass the service role to Amazon Bedrock. Add the following statement to the role's policy:

   ```
   {
       "Sid": "IAMPassRole",
       "Effect": "Allow",
       "Action": "iam:PassRole",
       "Resource": "arn:aws:iam::{{account-id}}:role/{{BedrockKBRole}}",
       "Condition": {
           "StringEquals": {
               "iam:PassedToService": "bedrock.amazonaws.com"
           }
       }
   }
   ```

1. (Optional) Create a custom AWS Identity and Access Management (IAM) [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) with the proper permissions by following the instructions at [Create a service role for managed Amazon Bedrock Knowledge Bases](kb-managed-permissions.md). You can use the AWS Management Console to automatically create a service role for you.

1. (Optional) If you plan to use a custom embedding model (`embeddingModelType: CUSTOM`) instead of the default managed embedding model, request access to the Bedrock embedding model in the Regions that you'll use by following the steps at [Request access to models](model-access.md). This is not required when using managed embedding.

1. (Optional) If you plan to use a custom reranking model (`rerankingModelType: CUSTOM`) instead of the default managed reranking model, request access to the Bedrock reranking model in the Regions that you'll use by following the steps at [Request access to models](model-access.md). This is not required when using managed reranking.

1. (Optional) If you plan to connect to your knowledge base through AgentCore Gateway, see [Connect to your knowledge base through AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-gateway-target.html) in Test your knowledge base with queries and responses.

1. (Optional) To encrypt data storage in your managed knowledge base with a custom KMS key, specify `ServerSideEncryptionConfiguration` during knowledge base creation. You also need to add the required KMS permissions to the service role. For more information, see [Encryption of data storage in fully managed knowledge base](encryption-kb.md#encryption-kb-managed-ingestion).

   ```
   "ManagedKnowledgeBaseConfiguration": {
       "ServerSideEncryptionConfiguration": {
           "KmsKeyArn": "arn:aws:kms:us-west-2:123456789012:key/6d2dc333-1294-40bb-840a-c86e46ddc8b7"
       }
   }
   ```