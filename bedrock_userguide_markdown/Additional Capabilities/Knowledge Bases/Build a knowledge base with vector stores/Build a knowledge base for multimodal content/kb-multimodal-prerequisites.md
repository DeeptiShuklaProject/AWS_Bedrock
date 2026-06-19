

# Prerequisites for multimodal knowledge bases
<a name="kb-multimodal-prerequisites"></a>

Amazon Bedrock multimodal knowledge bases require additional setup beyond standard knowledge bases to process images, audio, and video content. The specific prerequisites depend on your chosen processing approach and storage configuration.

Before you can create a multimodal knowledge base, you must fulfill the following prerequisites:

**Topics**
+ [Prerequisites](#kb-multimodal-prerequisites)
+ [Permissions for multimodal content](#kb-multimodal-prerequisites-permissions)

## Prerequisites
<a name="kb-multimodal-prerequisites"></a>

1. Make sure your data is in a [supported data source connector](data-source-connectors.md). Multimodal content is only supported with Amazon S3 and custom data sources.

1. (Optional) [Set up your own supported vector store](knowledge-base-setup.md). You can skip this step if you plan to use the AWS Management Console to automatically create a vector store for you.

1. Create a custom AWS Identity and Access Management (IAM) [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) with the proper permissions for multimodal processing. See [Permissions for multimodal content](#kb-multimodal-prerequisites-permissions) for details.
**Note**  
If you're using the console, Amazon Bedrock Knowledge Bases will automatically configure the permissions for you.

1. (Optional) Set up extra security configurations by following the steps at [Encryption of knowledge base resources](encryption-kb.md).

1. If you plan to use the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) API operation with BDA-processed content, request access to the models that you'll use in the Regions that you'll use them in by following the steps at [Request access to models](model-access.md).

## Permissions for multimodal content
<a name="kb-multimodal-prerequisites-permissions"></a>

Multimodal knowledge bases require additional permissions beyond standard knowledge base permissions. The specific permissions depend on your chosen processing approach and storage configuration.

You must configure the following permissions based on your multimodal processing approach:
+ **Nova Multimodal Embeddings permissions:** Required when using Nova Multimodal Embeddings for direct visual and audio similarity searches. Includes permissions for asynchronous model invocation and multimodal storage access.
+ **Bedrock Data Automation (BDA) permissions:** Required when using BDA to convert multimodal content to text representations. Includes permissions for data automation invocation and status monitoring.
+ **Customer-managed KMS key permissions:** Required when using customer-managed encryption keys with BDA processing. Includes permissions for key operations and grant creation.
+ **Multimodal storage permissions:** Required when configuring a multimodal storage destination. Includes standard S3 permissions for the storage bucket.

For detailed IAM policies and step-by-step permission configuration, see [Permissions for multimodal content](kb-permissions.md#kb-permissions-multimodal).

### Storage requirements
<a name="kb-multimodal-storage-requirements"></a>

**Nova Multimodal Embeddings**  
**Required:** You must configure a multimodal storage destination. This destination stores copies of your multimedia files for retrieval and ensures availability even if source files are modified or deleted.

**Bedrock Data Automation (BDA)**  
**Optional:** You can configure a multimodal storage bucket for additional reliability, and also to retrieve the file at runtime. However, it's not required since BDA converts content to text.  
If you select BDA parser without configuring a multimodal storage bucket, only text parsing will be available. To use multimodal parsing capabilities with BDA (processing images, audio, and video), you must configure a multimodal storage destination.

**Multimodal storage destination configuration**  
When configuring your multimodal storage destination, consider the following:
+ **Use separate buckets (recommended):** Configure different Amazon S3 buckets for your data source and multimodal storage destination. This provides the simplest setup and avoids potential conflicts.
+ **If using the same bucket:** You must specify an inclusion prefix for your data source that limits which content is ingested. This prevents re-ingesting extracted media files.
+ **Avoid "aws/" prefix:** When using the same bucket for both data source and multimodal storage destination, do not use inclusion prefixes starting with "aws/" as this path is reserved for extracted media storage.