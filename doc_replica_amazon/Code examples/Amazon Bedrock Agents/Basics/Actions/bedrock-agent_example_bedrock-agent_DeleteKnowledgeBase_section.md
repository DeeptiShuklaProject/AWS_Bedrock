

# Use `DeleteKnowledgeBase` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeleteKnowledgeBase_section"></a>

The following code example shows how to use `DeleteKnowledgeBase`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete an Amazon Bedrock knowledge base.  

```
def delete_knowledge_base(bedrock_agent_client, knowledge_base_id):
    """
    Deletes a knowledge base.

    Args:
        bedrock_agent_client: The Boto3 Bedrock Agent client.
        knowledge_base_id (str): The ID of the knowledge base to delete.

    Returns:
        bool: True if the deletion was successful.
    """
    try:
        bedrock_agent_client.delete_knowledge_base(
            knowledgeBaseId=knowledge_base_id
        )
        
        logger.info("Deleted knowledge base: %s", knowledge_base_id)
        return True
    except ClientError as err:
        logger.error(
            "Couldn't delete knowledge base %s. Here's why: %s: %s",
            knowledge_base_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
```
+  For API details, see [DeleteKnowledgeBase](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeleteKnowledgeBase) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.