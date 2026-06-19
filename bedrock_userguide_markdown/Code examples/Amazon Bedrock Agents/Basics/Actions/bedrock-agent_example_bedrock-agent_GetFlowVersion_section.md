

# Use `GetFlowVersion` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_GetFlowVersion_section"></a>

The following code example shows how to use `GetFlowVersion`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Get a version of an Amazon Bedrock flow.  

```
def get_flow_version(client, flow_id, flow_version):
    """
    Gets information about a version of an Amazon Bedrock flow.

    Args:
        client: Amazon Bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.
        flow_version (str): The flow version of the flow.

    Returns:
        dict: The response from the call to GetFlowVersion.
    """
    try:

        logger.info("Deleting flow version for flow: %s.", flow_id)

        # Call GetFlowVersion operation
        response = client.get_flow_version(
            flowIdentifier=flow_id,
            flowVersion=flow_version
        )

        logging.info("Successfully got flow version %s information for flow %s.",
                    flow_version,
                    flow_id)
        
        return response

    except ClientError as e:
        logging.exception("Client error getting flow version: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error getting flow version: %s", str(e))
        raise
```
+  For API details, see [GetFlowVersion](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/GetFlowVersion) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.