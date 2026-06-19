

# Use `CreateKnowledgeBase` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreateKnowledgeBase_section"></a>

The following code example shows how to use `CreateKnowledgeBase`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create an Amazon Bedrock knowledge base.  

```
def create_knowledge_base(bedrock_agent_client, name, role_arn, description=None):
    """
    Creates a new knowledge base.

    Args:
        bedrock_agent_client: The Boto3 Bedrock Agent client.
        name (str): The name of the knowledge base.
        role_arn (str): The ARN of the IAM role that the knowledge base assumes to access resources.
        description (str, optional): A description of the knowledge base.

    Returns:
        dict: The details of the created knowledge base.
    """
    try:
        kwargs = {
            "name": name,
            "roleArn": role_arn,
            "knowledgeBaseConfiguration": {
                "type": "VECTOR",
                "vectorKnowledgeBaseConfiguration": {
                    "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
                }
            },
            "storageConfiguration": {
                "type": "OPENSEARCH_SERVERLESS",
                # Note: You will need to create an OpenSearch Serverless collection first and replace this ARN
                # with your actual collection ARN from the OpenSearch console. If you use the console instead,
                # you can use the quick-create flow to have Knowledge Bases create the collection for you.
                "opensearchServerlessConfiguration": {
                    "collectionArn": "arn:aws:aoss:us-east-1::123456789012:collection/abcdefgh12345678defgh",
                        "fieldMapping": {
                        "metadataField": "metadata",
                        "textField": "text",
                        "vectorField": "vector"
                        },
                    "vectorIndexName": "test-uuid"
                    },
                },
            "clientToken": "test-client-token-" + str(uuid.uuid4())
        }
        
        if description:
            kwargs["description"] = description
            
        response = bedrock_agent_client.create_knowledge_base(**kwargs)
        
        logger.info("Created knowledge base with ID: %s", response["knowledgeBase"]["knowledgeBaseId"])
        return response["knowledgeBase"]
    
    except ClientError as err:
        logger.error(
            "Couldn't create knowledge base. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
```
+  For API details, see [CreateKnowledgeBase](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreateKnowledgeBase) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.