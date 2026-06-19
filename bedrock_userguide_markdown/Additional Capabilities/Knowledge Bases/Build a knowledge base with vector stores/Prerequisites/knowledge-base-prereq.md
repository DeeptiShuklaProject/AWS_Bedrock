

# Prerequisites for creating an Amazon Bedrock knowledge basewith a unstructured data source
<a name="knowledge-base-prereq"></a>

Amazon Bedrock knowledge bases require data and models to retrieve and generate responses, a vector store to store the vector representation of the data, and AWS Identity and Access Management permissions to access your data and perform actions.

Before you can create a knowledge base, you must fulfill the following prerequisites. For general permissions requirements, see [Set up permissions for a user or role to create and manage knowledge bases](knowledge-base-prereq-permissions-general.md)

1. Make sure your data is in a [supported data source connector](data-source-connectors.md).

1. (Optional) [Set up your own supported vector store](knowledge-base-setup.md). You can skip this step if you plan to use the AWS Management Console to automatically create a vector store for you.

1. (Optional) Create a custom AWS Identity and Access Management (IAM) [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) with the proper permissions by following the instructions at [Create a service role for Amazon Bedrock Knowledge Bases](kb-permissions.md). You can use the AWS Management Console to automatically create a service role for you.
**Note**  
If you choose to have Amazon Bedrock create a new service role for you, the user or role creating the knowledge base requires `iam:CreateRole` and `iam:CreatePolicy` permissions. If you're creating a knowledge base with Amazon OpenSearch Service (including Amazon OpenSearch Serverless), additional permissions are required, including `aoss:CreateAccessPolicy` and `iam:CreateServiceLinkedRole`.

1. (Optional) Set up extra security configurations by following the steps at [Encryption of knowledge base resources](encryption-kb.md).

1. (Optional) If you plan to use the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) API operation to generate responses based on information retrieved from your knowledge base, request access to the models that you'll use in the Regions that you'll use them in by following the steps at [Request access to models](model-access.md).

**Topics**
+ [Prerequisites for your Amazon Bedrock knowledge base data](knowledge-base-ds.md)
+ [Prerequisites for using a vector store you created for a knowledge base](knowledge-base-setup.md)