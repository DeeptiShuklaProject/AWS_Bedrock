

# Use `DeletePrompt` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeletePrompt_section"></a>

The following code example shows how to use `DeletePrompt`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a managed prompt](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockPrompts_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete an Amazon Bedrock managed prompt.  

```
def delete_prompt(client, prompt_id):
    """
    Deletes an Amazon Bedrock managed prompt.

    Args:
    client: Amazon Bedrock Agent boto3 client.
    prompt_id (str): The identifier of the prompt that you want to delete.

    Returns:
        dict: The response from the DeletePrompt operation.
    """
    try:
        logger.info("Deleting prompt ID: %s.", prompt_id)

        response = client.delete_prompt(
            promptIdentifier=prompt_id
        )

        logger.info("Finished deleting prompt ID: %s", prompt_id)

        return response

    except ClientError as e:
        logger.exception("Client error deleting prompt: %s", str(e))
        raise

    except Exception as e:
        logger.exception("Unexpected error deleting prompt: %s", str(e))
        raise
```
+  For API details, see [DeletePrompt](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeletePrompt) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.