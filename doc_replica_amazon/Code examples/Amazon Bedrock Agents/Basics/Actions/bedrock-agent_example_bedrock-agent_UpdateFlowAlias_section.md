

# Use `UpdateFlowAlias` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_UpdateFlowAlias_section"></a>

The following code example shows how to use `UpdateFlowAlias`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Update an alias for an Amazon Bedrock flow.  

```
def update_flow_alias(client, flow_id, alias_id, flow_version, name, description):
    """
    Updates an alias for an Amazon Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        str: The response from UpdateFlowAlias.
    """

    try:
        logger.info("Updating flow alias %s for flow: %s.", alias_id, flow_id)

        response = client.update_flow_alias(
            aliasIdentifier=alias_id,
            flowIdentifier=flow_id,
            name=name,
            description=description,
            routingConfiguration=[
                {
                    "flowVersion": flow_version
                }
            ]
        )
        logger.info("Successfully updated flow alias %s for %s.", alias_id, flow_id)

        return response

    except ClientError as e:
        logging.exception("Client error updating alias %s for flow: %s - %s",
                alias_id, flow_id, str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error updating alias %s for flow : %s - %s",
                alias_id, flow_id, str(e))
        raise
```
+  For API details, see [UpdateFlowAlias](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/UpdateFlowAlias) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.