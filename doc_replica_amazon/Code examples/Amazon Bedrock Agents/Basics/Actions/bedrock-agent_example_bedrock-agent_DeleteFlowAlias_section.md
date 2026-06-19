

# Use `DeleteFlowAlias` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeleteFlowAlias_section"></a>

The following code example shows how to use `DeleteFlowAlias`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete an alias for an Amazon Bedrock flow.  

```
def delete_flow_alias(client, flow_id, flow_alias_id):
    """
    Deletes an Amazon Bedrock flow alias.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        dict: The response from the call to DetectFLowAlias
    """
    try:

        logger.info("Deleting flow alias %s for flow: %s.", flow_alias_id, flow_id)

        # Delete the flow alias.
        response = client.delete_flow_alias(
            aliasIdentifier=flow_alias_id,
            flowIdentifier=flow_id
        )

        logging.info("Successfully deleted flow version for %s.", flow_id)
        return response

    except ClientError as e:
        logging.exception("Client error deleting flow version: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected deleting flow version: %s", str(e))
        raise
```
+  For API details, see [DeleteFlowAlias](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeleteFlowAlias) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.