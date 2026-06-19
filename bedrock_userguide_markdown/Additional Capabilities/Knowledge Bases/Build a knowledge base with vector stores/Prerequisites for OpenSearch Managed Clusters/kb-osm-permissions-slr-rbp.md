

# Configuring resource-based policies for OpenSearch Managed clusters
<a name="kb-osm-permissions-slr-rbp"></a>

When creating your knowledge base, you can either create your own custom role or let Amazon Bedrock create one for you. How you configure the permissions depend on whether you're creating a new role or using an existing role. If you already have an existing IAM role, you must ensure that your domain's access policy does not prevent the roles in your account from performing the necessary OpenSearch API actions.

If you are choosing to let Amazon Bedrock Knowledge Bases create the IAM role for you, you must ensure that your domain's access policy grants the permissions to perform the required OpenSearch API actions by the roles in your account. If your domain has a restrictive access policy, it can prevent your role from performing these actions. Following shows an example of a restrictive resource-based policy.

In this case, you can either:
+ Create your knowledge base using an existing IAM role that your OpenSearch domain can grant access to this role for performing the necessary operations.
+ Alternatively, you can let Amazon Bedrock create a new role for you. In this case, you must ensure that the domain's access policy must grant the permissions to perform the necessary OpenSearch API actions by the roles in your account.

The following sections show a sample IAM policy that grants the necessary permissions and how you can update the domain's access policy so that it grants permissions to perform the necessary OpenSearch API operations.

**Topics**
+ [Sample IAM identity-based and resource-based policies](#kb-osm-permissions-iam)
+ [Creating the Amazon Bedrock Knowledge Bases service role](#kb-osm-permissions-slr)
+ [Updating the resource-based policies](#kb-osm-permissions-console-rbp)

## Sample IAM identity-based and resource-based policies
<a name="kb-osm-permissions-iam"></a>

This section provides a sample identity policy and a resource-based policy that you can configure for your OpenSearch domain when integrating with Amazon Bedrock Knowledge Bases. You must grant Amazon Bedrock permissions to perform these actions on the index that you provide your Knowledge Base.


****  

| Action | Resource | Description | 
| --- | --- | --- | 
| es:ESHttpPost | arn:{{<partition>}}:es:{{<region>}}:{{<accountId>}}:domain/{{<domainName>}}/{{<indexName>}} | For inserting information to the index | 
| es:ESHttpGet |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/kb-osm-permissions-slr-rbp.html)  | For searching information from the index. This action is configured at both the at both the domain/index level and the domain/index/\* level. At the domain/index level, it can get high level details about the index, such as the engine type. To retrieve details stored within the index, permissions are required at the domain/index/\* level. | 
| es:ESHttpHead |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/kb-osm-permissions-slr-rbp.html)  | For getting information from the index. This action is configured at both the at both the domain/index level and the domain/index/\* level, in case information needs to be obtained at a higher level, such as whether a particular index exists. | 
| es:ESHttpDelete | arn:{{<partition>}}:es:{{<region>}}:{{<accountId>}}:domain/{{<domainName>}}/{{<indexName>}} | For deleting information to the index | 
| es:DescribeDomain | arn:{{<partition>}}:es:{{<region>}}:{{<accountId>}}:domain/{{<domainName>}} | For performing validations on the domain, such as the engine version used. | 

### Sample identity-based policy
<a name="kb-osm-permissions-idpolicy"></a>

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "OpenSearchIndexAccess",
            "Effect": "Allow",
            "Action": [
                "es:ESHttpGet",
                "es:ESHttpPost",
                "es:ESHttpPut",
                "es:ESHttpDelete"
            ],
            "Resource": [
                "arn:aws:{{es:us-east-1}}:{{123456789012}}:domain/{{domainName}}/{{indexName}}/*"
            ]
        },
        {
            "Sid": "OpenSearchIndexGetAccess",
            "Effect": "Allow",
            "Action": [
                "es:ESHttpGet",
                "es:ESHttpHead"
            ],
            "Resource": [
            "arn:aws:{{es:us-east-1}}:{{123456789012}}:domain/{{domainName}}/{{indexName}}"
            ]
        },
        {
            "Sid": "OpenSearchDomainValidation",
            "Effect": "Allow",
            "Action": [
                "es:DescribeDomain"
            ],
            "Resource": [
            "arn:aws:{{es:us-east-1}}:{{123456789012}}:domain/{{domainName}}"
            ]
        }
    ]
}
```

------

### Sample resource-based policy
<a name="kb-osm-permissions-rbp"></a>

**Note**  
Make sure that the service role has been created for it to be used in the resource-based policy.

## Creating the Amazon Bedrock Knowledge Bases service role
<a name="kb-osm-permissions-slr"></a>

When you create the knowledge base, you can choose the option to create and use a new service role. This section walks you through creating the Amazon Bedrock Knowledge Bases service role. By mapping the resource-based policies and the fine-grained access policies to this role, it will grant Amazon Bedrock the permissions to make requests to the OpenSearch domain.

**To specify the Amazon Bedrock Knowledge Bases service role:**

1. In the Amazon Bedrock console, go to [Knowledge Bases](https://console.aws.amazon.com/bedrock/home#/knowledge-bases).

1. Choose **Create** and then choose **Knowledge base with vector store**.

1. Choose **Create and use a new service role**. You can either use the default, or provide a custom role name, and Amazon Bedrock will automatically create the Knowledge Base service role for you.

1. Continue going through the console to configure your data source and parsing and chunking strategies.

1. Choose an Embeddings model and then, under **Choose an existing vector store**, choose **Amazon OpenSearch Managed Cluster**.

**Important**  
Before you proceed to create the knowledge base, complete the following steps to configure the resource-based policies and fine-grained access policies. For detailed steps on creating the knowledge base, see [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](knowledge-base-create.md).

## Updating the resource-based policies
<a name="kb-osm-permissions-console-rbp"></a>

If your OpenSearch domain has a restrictive access policy, you can follow the instructions on this page to update the resource-based policy. These permissions allow Knowledge Bases to make use of the index that you provide, and to retrieve the OpenSearch domain definition to perform the required validation on the domain.

**To configure the resource-based policies from the AWS Management Console**

1. Go to the [Amazon OpenSearch Service console](https://console.aws.amazon.com/aos/home?region=us-east-1#opensearch/dashboard).

1. Go to the domain that you had created, and then go to **Security Configurations** where the resource-based policy is configured.

1. Edit the policy in the **JSON** tab and then update the policy similar to the [Sample resource-based policy](#kb-osm-permissions-rbp).

1. You can now go back to the Amazon Bedrock console and provide the details for your OpenSearch domain and index as described in [Knowledge base setup for Managed Clusters](knowledge-base-setup.md#knowledge-base-setup-osm).