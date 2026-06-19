

# Use `DeleteFlowVersion` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeleteFlowVersion_section"></a>

The following code example shows how to use `DeleteFlowVersion`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete a version of an Amazon Bedrock flow.  

```
def delete_flow_version(client, flow_id, flow_version):
    """
    Deletes a version of an Amazon Bedrock flow.

    Args:
        client: Amazon Bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        dict: The response from DeleteFlowVersion.
    """
    try:

        logger.info("Deleting flow version %s for flow: %s.",flow_version, flow_id)

        # Call DeleteFlowVersion operation
        response = client.delete_flow_version(
            flowIdentifier=flow_id,
            flowVersion=flow_version
        )

        logging.info("Successfully deleted flow version %s for %s.",
                flow_version,
                flow_id)
        return response

    except ClientError as e:
        logging.exception("Client error deleting flow version: %s ", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected deleting flow version: %s", str(e))
        raise
```
+  For API details, see [DeleteFlowVersion](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeleteFlowVersion) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.