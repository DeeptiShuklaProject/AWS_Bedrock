

# Use `ListKnowledgeBases` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_ListKnowledgeBases_section"></a>

The following code example shows how to use `ListKnowledgeBases`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
List Amazon Bedrock knowledge Bases.  

```
def list_knowledge_bases(bedrock_agent_client, max_results=None):
    """
    Lists the knowledge bases in your AWS account.

    Args:
        bedrock_agent_client: The Boto3 Bedrock Agent client.
        max_results (int, optional): The maximum number of knowledge bases to return.

    Returns:
        list: A list of knowledge base details.
    """
    try:
        kwargs = {}
        if max_results is not None:
            kwargs["maxResults"] = max_results

        # Initialize an empty list to store all knowledge bases
        all_knowledge_bases = []
        
        # Use paginator to handle pagination automatically
        paginator = bedrock_agent_client.get_paginator('list_knowledge_bases')
        page_iterator = paginator.paginate(**kwargs)
        
        # Iterate through each page of results
        for page in page_iterator:
            all_knowledge_bases.extend(page.get('knowledgeBaseSummaries', []))
            
        logger.info("Found %s knowledge bases.", len(all_knowledge_bases))
        return all_knowledge_bases
    except ClientError as err:
        logger.error(
            "Couldn't list knowledge bases. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
```
+  For API details, see [ListKnowledgeBases](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/ListKnowledgeBases) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.