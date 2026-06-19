

# Use `ListPrompts` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_ListPrompts_section"></a>

The following code example shows how to use `ListPrompts`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
List Amazon Bedrock managed prompts.  

```
def list_prompts(client, max_results=10):
    """
    Lists Amazon Bedrock managed prompts.

    Args:
        client: Amazon Bedrock Agent boto3 client.
        max_results (int): Maximum number of results to return per page.

    Returns:
        list: A list of prompt summaries.
    """
    try:
        logger.info("Listing prompts:")
        
        # Create a paginator for the list_prompts operation
        paginator = client.get_paginator('list_prompts')
        
        # Create the pagination parameters
        pagination_config = {
            'maxResults': max_results
        }
        
        # Initialize an empty list to store all prompts
        all_prompts = []
        
        # Iterate through all pages
        for page in paginator.paginate(**pagination_config):
            all_prompts.extend(page.get('promptSummaries', []))
            
        logger.info("Successfully listed %s prompts.", len(all_prompts))
        return all_prompts
        
    except ClientError as e:
        logger.exception("Client error listing prompts: %s", str(e))
        raise
    except Exception as e:
        logger.exception("Unexpected error listing prompts: %s", str(e))
        raise
```
+  For API details, see [ListPrompts](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/ListPrompts) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.