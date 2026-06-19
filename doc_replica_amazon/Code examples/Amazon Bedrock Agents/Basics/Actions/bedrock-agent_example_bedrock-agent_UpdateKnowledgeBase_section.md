

# Use `UpdateKnowledgeBase` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_UpdateKnowledgeBase_section"></a>

The following code example shows how to use `UpdateKnowledgeBase`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Update an Amazon Bedrock knowledge base.  

```
def update_knowledge_base(bedrock_agent_client, knowledge_base_id, name=None, description=None, role_arn=None):
    """
    Updates an existing knowledge base.

    Args:
        bedrock_agent_client: The Boto3 Bedrock Agent client.
        knowledge_base_id (str): The ID of the knowledge base to update.
        name (str, optional): The new name for the knowledge base.
        description (str, optional): The new description for the knowledge base.
        role_arn (str, optional): The new IAM role ARN for the knowledge base.

    Returns:
        dict: The details of the updated knowledge base.
    """
    try:
        kwargs = {
            "knowledgeBaseId": knowledge_base_id,
            "knowledgeBaseConfiguration": {
                "type": "VECTOR",
                "vectorKnowledgeBaseConfiguration": {
                    "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
                }
            }
        }
        
        if name:
            kwargs["name"] = name
        if description:
            kwargs["description"] = description
        if role_arn:
            kwargs["roleArn"] = role_arn
            
        response = bedrock_agent_client.update_knowledge_base(**kwargs)
        
        logger.info("Updated knowledge base: %s", knowledge_base_id)
        return response["knowledgeBase"]
    
    except ClientError as err:
        logger.error(
            "Couldn't update knowledge base %s. Here's why: %s: %s",
            knowledge_base_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
```
+  For API details, see [UpdateKnowledgeBase](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/UpdateKnowledgeBase) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.