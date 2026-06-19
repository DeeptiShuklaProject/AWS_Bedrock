

# Data encryption
<a name="data-encryption"></a>

Amazon Bedrock uses encryption to protect data at rest and data in transit.

**Encryption in transit**

Within AWS, all inter-network data in transit supports TLS 1.2 encryption.

Requests to the Amazon Bedrock API and console are made over a secure (SSL) connection. You pass AWS Identity and Access Management (IAM) roles to Amazon Bedrock to provide permissions to access resources on your behalf for training and deployment. 

**Encryption at rest**

Amazon Bedrock provides [Encryption of custom models](encryption-custom-job.md) at rest.

## Key management
<a name="key-management"></a>

Use the AWS Key Management Service to manage the keys that you use to encrypt your resources. For more information, see [AWS Key Management Service concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys). You can encrypt the following resources with a KMS key.
+ Through Amazon Bedrock
  + Model customization jobs and their output custom models – During job creation in the console or by specifying the `customModelKmsKeyId` field in the [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) API call.
  + Agents – During agent creation in the console or by specifying the `customerEncryptionKeyArn` field in the [CreateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) API call.
  + Data source ingestion jobs for knowledge bases – During knowledge base creation in the console or by specifying the `kmsKeyArn` field in the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) or [UpdateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateDataSource.html) API call.
  + Vector stores in Amazon OpenSearch Service – During vector store creation. For more information, see [Creating, listing, and deleting Amazon OpenSearch Service collections](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html) and [Encryption of data at rest for Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html).
  + Model evaluations jobs – When you create a model evaluation job in console or by specify a key ARN in ` customerEncryptionKeyId` in the [CreateEvaluationJob ](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateEvaluationJob.html) API call.
+ Through Amazon S3 – For more information, see [Using server-side encryption with AWS KMS keys (SSE-KMS).](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)
  + Training, validation, and output data for model customization
  + Data sources for knowledge bases
+ Through AWS Secrets Manager – For more information, see [Secret encryption and decryption in AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html)
  + Vector stores for third-party models

After you encrypt a resource, you can find the ARN of the KMS key by selecting a resource and viewing its **Details** in the console or by using the following `Get` API calls.
+ [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html)
+ [GetAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgent.html)
+ [GetIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetIngestionJob.html)