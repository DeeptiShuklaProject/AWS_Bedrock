

# Prerequisites and permissions required for using OpenSearch Managed Clusters with Amazon Bedrock Knowledge Bases
<a name="kb-osm-permissions-prereq"></a>

This section shows you how to configure permissions if you're creating your own vector database with Amazon OpenSearch Service Managed Clusters. This configuration must be performed before you create the knowledge base. The steps assume that you've already created a domain and vector index in Amazon OpenSearch Service. For more information, see [Creating and managing OpenSearch Service domains](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html) in the *Amazon OpenSearch Service developer guide*.

## Key considerations
<a name="kb-osm-permissions-prereq-considerations"></a>

Following are some key considerations for using Amazon Bedrock Knowledge Bases with Amazon OpenSearch Service Managed Clusters.
+ Before using any domain resources in OpenSearch Managed clusters, you need to configure certain IAM access permissions and policies. For Knowledge Bases integration with Managed clusters, before you perform the steps in this section, if your domain has a restrictive access policy, you must grant the required IAM access and configure the resource-based policies. We also recommend that you configure fine-grained access control to scope down the permissions.
+ When ingesting the data for your knowledge base, if you encounter failures, it might indicate an insufficient OpenSearch domain capacity to handle the speed of ingestion. To resolve this issue, increase your domain's capacity by provisioning higher IOPS (Input/Output Operations Per Second) and by increasing the throughput settings. Wait for several minutes for the new capacity to be provisioned and then retry the ingestion process. To verify that the issue has been resolved, you can monitor the performance during the retry process. If throttling still persists, you may need to further adjust capacity for improved efficiency. For more information, see [Operational best practices for Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/bp.html).

## Overview of permissions configuration
<a name="kb-osm-permissions-prereq-overview"></a>

For Knowledge Bases integration with managed clusters, you need to configure the following IAM access permissions and resource-based policies. We recommend that you enable fine-grained access policies to further control the user access and the granularity at which it must be scoped down to the property level.

The following steps provide a high-level overview for how to configure permissions.

1. 

**Create and use Knowledge base service role**

   For the permissions that you want to configure, while you can still provide your own custom role, we recommend that you specify the option for Amazon Bedrock Knowledge Bases to create the Knowledge base service role for you.

1. 

**Configure the resource-based policy**

   The OpenSearch domain supports resource-based policies, that determine which principals can access and act on the domain. To use with Knowledge Bases, ensure proper configuration of the resource-based policy for your domain.

1. 

***(Strongly Recommended)* Provide role mapping for fine-grained access control**

   While fine-grained access control is optional, we recommend that you have it enabled for controlling the granularity at which the permissions must be scoped down at the property level.

## Configuring IAM policies
<a name="kb-osm-permissions-iam"></a>

Your domain's access policy must grant the permissions to perform the required OpenSearch API actions by the roles in your account.

If your domain has a restrictive access policy, then it might need to be updated as follows:
+ It should grant access to Amazon Bedrock service and include the required HTTP actions: `GET`, `POST`, `PUT`, and `DELETE`.
+ It must also grant Amazon Bedrock permissions to perform the `es:DescribeDomain` action on your index resource. This allows Amazon Bedrock Knowledge Bases to perform the required validations when configuring a knowledge base.

## (Optional) Fine-grained access control
<a name="kb-osm-permissions-console-fgap"></a>

Fine-grained access control can control the granularity at which the permissions must be scoped down at the property levelYou can configure the fine-grained access policies, to grant the read-write permissions required to the service role created by Knowledge Bases.

To configure fine-grained access control and provide the role mapping:

1. Make sure that the OpenSearch domain that you created has fine-grained access control enabled.

1. Create an OpenSearch UI (Dashboards), if you haven't already. This will be used to configure the role mapping

1. In your OpenSearch Dashboards, create an OpenSearch role and specify the vector index name, and the cluster and index permissions. To add the permissions, you must create permission groups and then add the required permissions that grant access to perform a set of operations including `delete`, `search`, `get`, and `index` for the role.

1. After you've added the required permissions, you must enter the ARN of your Knowledge base service role for the OpenSearch back-end role. Performing this step will complete the mapping between your Knowledge Base Service role and the OpenSearch role, which then grants Amazon Bedrock Knowledge Bases permissions to access the vector index in the OpenSearch domain and perform the required operations.

**Topics**
+ [Key considerations](#kb-osm-permissions-prereq-considerations)
+ [Overview of permissions configuration](#kb-osm-permissions-prereq-overview)
+ [Configuring IAM policies](#kb-osm-permissions-iam)
+ [(Optional) Fine-grained access control](#kb-osm-permissions-console-fgap)
+ [Configuring resource-based policies for OpenSearch Managed clusters](kb-osm-permissions-slr-rbp.md)
+ [Configuring OpenSearch permissions with fine-grained access control](kb-osm-permissions-console-fgap.md)