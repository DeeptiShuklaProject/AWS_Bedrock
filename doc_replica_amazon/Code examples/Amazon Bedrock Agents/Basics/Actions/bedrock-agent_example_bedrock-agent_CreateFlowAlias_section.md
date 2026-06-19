

# Use `CreateFlowAlias` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreateFlowAlias_section"></a>

The following code example shows how to use `CreateFlowAlias`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create an alias for an Amazon Bedrock flow.  

```
def create_flow_alias(client, flow_id, flow_version, name, description):
    """
    Creates an alias for an Amazon Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        str: The ID for the flow alias.
    """

    try:
        logger.info("Creating flow alias for flow: %s.", flow_id)

        response = client.create_flow_alias(
            flowIdentifier=flow_id,
            name=name,
            description=description,
            routingConfiguration=[
                {
                    "flowVersion": flow_version
                }
            ]
        )
        logger.info("Successfully created flow alias for %s.", flow_id)

        return response['id']

    except ClientError as e:
        logging.exception("Client error creating alias for flow: %s - %s",
                flow_id, str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error creating alias for flow : %s - %s",
                flow_id, str(e))
        raise
```
+  For API details, see [CreateFlowAlias](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreateFlowAlias) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.