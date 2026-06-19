

# Permissions for reranking in Amazon Bedrock
<a name="rerank-prereq"></a>

A user requires the following permissions to use reranking:
+ Access to the reranking models that they plan to use. For more information, see [Request access to models](model-access.md). For third-party models (such as Cohere Rerank), your IAM role also needs `aws-marketplace:ViewSubscriptions` and `aws-marketplace:Subscribe` permissions. For more information, see [Use product ID condition keys to control access](model-access-product-ids.md).
+ Permissions for their role and, if they plan to use reranking in a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) workflow, permissions for the Amazon Bedrock Knowledge Bases service role that has a [trust relationship](kb-permissions.md#kb-permissions-trust) with their role.
**Tip**  
To configure the required permissions quickly, you can do the following:  
Attach the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) AWS managed policy to the user role. For more information about attaching a policy to an IAM role, see [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html).
Use the Amazon Bedrock console to create an Amazon Bedrock Knowledge Bases service role when [creating a knowledge base](knowledge-base-create.md). If you already have an Amazon Bedrock Knowledge Bases service role that the console created for you, you can use the console to update it when [retrieving sources](kb-test-retrieve.md) in the console.
**Important**  
When you use reranking in a `Retrieve` workflow with an Amazon Bedrock Knowledge Bases service role, note the following:  
If you manually edit the AWS Identity and Access Management (IAM) policy that Amazon Bedrock created for your knowledge base service role, then you might encounter errors when trying to update the permissions in the AWS Management Console. To resolve this issue, in the IAM console, delete the policy version that you created manually. Then, refresh the reranker page in the Amazon Bedrock console and retry.
If you use a custom role, then Amazon Bedrock can't update the knowledge base service role on your behalf. Verify that the permissions are properly configured for the service role.

  For a summary of use cases and the permissions needed for them, refer to the following table:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/rerank-prereq.html)

For example permissions policies that you can attach to an IAM role, expand the section that corresponds to your use case:

## Permissions policy for using a reranking model independently
<a name="rerank-permissions-rerank"></a>

To use [Rerank](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Rerank.html) directly with a list of sources, the user role needs permissions to use both the `bedrock:Rerank` and `bedrock:InvokeModel` actions. Similarly, to prevent usage of a reranking model, you must deny permissions for both actions. To allow the user role to use a reranking model independently, you can attach the following policy to the role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RerankSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:Rerank"
            ],
            "Resource": "*"
        },
        {
            "Sid": "InvokeModelSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:{{bedrock:us-east-1}}::foundation-model/{{model-id}}"
            ]
        }
    ]
}
```

------

In the preceding policy, for the `bedrock:InvokeModel` action, you scope the permissions to the models that you want to allow the role to use for reranking. To allow access to all models, use a wildcard ({{\*}}) in the `Resource` field.

## Permissions policies for using a reranking model in a Retrieve workflow
<a name="rerank-permissions-retrieve"></a>

To use reranking while retrieving data from a knowledge base, you must set up the following permissions:

**For the user role**

The user role needs permissions to use the `bedrock:Retrieve` action. To allow the user role to retrieve data from a knowledge base, you can attach the following policy to the role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RetrieveSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{KnowledgeBaseId}}"
            ]
        }
    ]
}
```

------

In the preceding policy, for the `bedrock:Retrieve` action, you scope the permissions to the knowledge bases from which you want to allow the role to retrieve information. To allow access to all knowledge bases, you can use a wildcard ({{\*}}) in the `Resource` field.

**For the service role**

The [Amazon Bedrock Knowledge Bases service role](kb-permissions.md) that the user uses needs permissions to use the `bedrock:Rerank` and `bedrock:InvokeModel` actions. You can use the Amazon Bedrock console to configure permissions for your service role automatically when you choose a reranking model when you [configure knowledge base retrieval](kb-test-retrieve.md). Otherwise, to allow the service role to rerank sources during retrieval, you can attach the following policy:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RerankSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:Rerank"
            ],
            "Resource": "*"
        },
        {
            "Sid": "InvokeModelSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{RerankModelId}}"
        }
    ]
}
```

------

In the preceding policy, for the `bedrock:InvokeModel` action, you scope the permissions to the models that you want to allow the role to use for reranking. To allow access to all models, you can use a wildcard (\*) in the `Resource` field.

## Permissions policy for using a reranking model in a RetrieveAndGenerate workflow
<a name="rerank-permissions-retrieve-and-generate"></a>

To use a reranker model when retrieving data from a knowledge base and subsequently generating responses based on the retrieved results, the user role needs permissions to use the `bedrock:RetrieveAndGenerate`, `bedrock:Rerank`, and `bedrock:InvokeModel` actions. To allow reranking of sources during retrieval, and to allow generation of responses based on the results, you can attach the following policy to the user role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "RerankRetrieveAndGenerateSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:Rerank",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": "*"
        },
        {
            "Sid": "InvokeModelSid",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{RerankModelId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{GenerationModelId}}}"
            ]
        }
    ]
}
```

------

In the preceding policy, for the `bedrock:InvokeModel` operation, you scope the permissions to the models that you want to allow the role to use for reranking, and to the models that you want to allow the role to use for generating responses. To allow access to all models, you can use a wildcard ({{\*}}) in the `Resource` field.

To further restrict permissions, you can omit actions, or you can specify resources and condition keys by which to filter permissions. For more information about actions, resources, and condition keys, see the following topics in the *Service Authorization Reference*:
+ [Actions defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) – Learn about actions, the resource types that you can scope them to in the `Resource` field, and the condition keys that you can filter permissions on in the `Condition` field.
+ [Resource types defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-resources-for-iam-policies) – Learn about the resource types in Amazon Bedrock.
+ [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) – Learn about the condition keys in Amazon Bedrock.