

# Data management and encryption in Amazon Bedrock evaluation job
<a name="evaluation-data-management"></a>

During the model evaluation job, Amazon Bedrock makes a temporary copy of your data and stores it in an AWS-owned Amazon S3 bucket. Amazon Bedrock deletes this data after the job finishes. Amazon Bedrock encrypts this data using a AWS KMS key. You can choose to specify your own AWS KMS key or to use an Amazon Bedrock-owned key to encrypt the data.

When you create a model evaluation job using the either the AWS Management Console, AWS CLI, or a supported AWS SDK you can choose to use an Amazon Bedrock owned KMS key or your own customer managed key. If no customer managed key is specified then an Amazon Bedrock owned key is used by default.

To use a customer managed key, you must add the required IAM actions and resources to the IAM service role's policy. You must also add the required AWS KMS key policy elements.

**Topics**
+ [Required Key policy elements to encrypt your model evaluation job using AWS KMS](model-evaluation-security-kms.md)
+ [AWS Key Management Service support in model evaluation jobs](model-evaluation-security-data.md)
+ [Data encryption for knowledge base evaluation jobs](rag-evaluation-security-data.md)