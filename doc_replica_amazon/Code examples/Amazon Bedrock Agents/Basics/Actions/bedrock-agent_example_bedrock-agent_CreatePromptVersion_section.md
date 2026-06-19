

# Use `CreatePromptVersion` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreatePromptVersion_section"></a>

The following code example shows how to use `CreatePromptVersion`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a managed prompt](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockPrompts_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create a version of an Amazon Bedrock managed prompt.  

```
def create_prompt_version(client, prompt_id, description=None):
    """
    Creates a version of an Amazon Bedrock managed prompt.

    Args:
    client: Amazon Bedrock Agent boto3 client.
    prompt_id (str): The identifier of the prompt to create a version for.
    description (str, optional): A description for the version.

    Returns:
        dict: The response from CreatePromptVersion.
    """
    try:
        logger.info("Creating version for prompt ID: %s.", prompt_id)
        
        create_params = {
            'promptIdentifier': prompt_id
        }
        
        if description:
            create_params['description'] = description
            
        response = client.create_prompt_version(**create_params)

        logger.info("Successfully created prompt version: %s", response['version'])
        logger.info("Prompt version ARN: %s", response['arn'])

        return response


    except ClientError as e:
        logger.exception("Client error creating prompt version: %s", str(e))
        raise

    except Exception as e:
        logger.exception("Unexpected error creating prompt version: %s", str(e))
        raise
```
+  For API details, see [CreatePromptVersion](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreatePromptVersion) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.