

# Use `CreatePrompt` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreatePrompt_section"></a>

The following code example shows how to use `CreatePrompt`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a managed prompt](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockPrompts_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create an Amazon Bedrock managed prompt.  

```
def create_prompt(client, prompt_name, prompt_description, prompt_template, model_id=None):
    """
    Creates an Amazon Bedrock managed prompt.

    Args:
    client: Amazon Bedrock Agent boto3 client.
    prompt_name (str): The name for the new prompt.
    prompt_description (str): The description for the new prompt.
    prompt_template (str): The template for the prompt.
    model_id (str, optional): The model ID to associate with the prompt.

    Returns:
        dict: The response from CreatePrompt.
    """
    try:
        logger.info("Creating prompt: %s.", prompt_name)
        
        # Create a variant with the template
        variant = {
            "name": "default",
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "text": prompt_template,
                    "inputVariables": []
                }
            }
        }
        
        # Extract input variables from the template
        # Look for patterns like {{variable_name}}

        variables = re.findall(r'{{(.*?)}}', prompt_template)
        for var in variables:
            variant["templateConfiguration"]["text"]["inputVariables"].append({"name": var.strip()})
        
        # Add model ID if provided
        if model_id:
            variant["modelId"] = model_id
        
        # Create the prompt with the variant
        create_params = {
            'name': prompt_name,
            'description': prompt_description,
            'variants': [variant]
        }
            
        response = client.create_prompt(**create_params)

        logger.info("Successfully created prompt: %s. ID: %s",
                    prompt_name,
                    response['id'])

        return response

    except ClientError as e:
        logger.exception("Client error creating prompt: %s", str(e))
        raise

    except Exception as e:
        logger.exception("Unexpected error creating prompt: %s", str(e))
        raise
```
+  For API details, see [CreatePrompt](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreatePrompt) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.