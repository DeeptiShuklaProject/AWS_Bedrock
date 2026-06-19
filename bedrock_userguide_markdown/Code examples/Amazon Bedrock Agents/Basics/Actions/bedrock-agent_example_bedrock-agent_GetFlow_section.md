

# Use `GetFlow` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_GetFlow_section"></a>

The following code example shows how to use `GetFlow`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Get an Amazon Bedrock flow.  

```
def get_flow(client, flow_id):
    """
    Gets an Amazon Bedrock flow.

    Args:
    client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow that you want to get.

    Returns:
        dict: The response from the GetFlow operation.
    """
    try:

        logger.info("Getting flow ID: %s.",
                    flow_id)

        # Call GetFlow operation.
        response = client.get_flow(
            flowIdentifier=flow_id
        )

        logger.info("Retrieved flow ID: %s. Name: %s", flow_id,
                    response['name'])

        return response

    except ClientError as e:
        logger.exception("Client error getting flow: %s", {str(e)})
        raise

    except Exception as e:
        logger.exception("Unexepcted error getting flow: %s", {str(e)})
        raise
```
+  For API details, see [GetFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/GetFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.