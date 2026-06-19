

# Use `DeleteFlow` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeleteFlow_section"></a>

The following code example shows how to use `DeleteFlow`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete an Amazon Bedrock flow.  

```
def delete_flow(client, flow_id):
    """
    Deletes an Amazon Bedrock flow.

    Args:
    client: Amazon Bedrock agent boto3 client.
    flow_id (str): The identifier of the flow that you want to delete.

    Returns:
        dict: The response from the DeleteFLow operation.
    """
    try:

        logger.info("Deleting flow ID: %s.",
                    flow_id)

        # Call DeleteFlow operation
        response = client.delete_flow(
            flowIdentifier=flow_id,
            skipResourceInUseCheck=True
        )

        logger.info("Finished deleting flow ID: %s", flow_id)

        return response

    except ClientError as e:
        logger.exception("Client error deleting flow: %s", {str(e)})
        raise

    except Exception as e:
        logger.exception("Unexepcted error deleting flow: %s", {str(e)})
        raise
```
+  For API details, see [DeleteFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeleteFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.