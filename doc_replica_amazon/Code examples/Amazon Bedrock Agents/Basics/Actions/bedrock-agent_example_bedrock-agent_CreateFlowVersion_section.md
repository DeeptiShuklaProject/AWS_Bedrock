

# Use `CreateFlowVersion` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreateFlowVersion_section"></a>

The following code example shows how to use `CreateFlowVersion`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create a version of an Amazon Bedrock flow.  

```
def create_flow_version(client, flow_id, description):
    """
    Creates a version of an Amazon Bedrock flow.

    Args:
        client: Amazon Bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.
        description (str) : A description for the flow.

    Returns:
        str: The version for the flow.
    """
    try:

        logger.info("Creating flow version for flow: %s.", flow_id)

        # Call CreateFlowVersion operation
        response = client.create_flow_version(
            flowIdentifier=flow_id,
            description=description
        )

        logging.info("Successfully created flow version %s for flow %s.",
            response['version'], flow_id)
        
        return response['version']

    except ClientError as e:
        logging.exception("Client error creating flow: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error creating flow : %s", str(e))
        raise
```
+  For API details, see [CreateFlowVersion](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreateFlowVersion) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.