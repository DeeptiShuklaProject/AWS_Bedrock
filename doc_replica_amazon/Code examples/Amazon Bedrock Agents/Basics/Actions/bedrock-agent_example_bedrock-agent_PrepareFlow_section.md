

# Use `PrepareFlow` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_PrepareFlow_section"></a>

The following code example shows how to use `PrepareFlow`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Prepare an Amazon Bedrock flow.  

```
def prepare_flow(client, flow_id):
    """
    Prepares an Amazon Bedrock Flow.

    Args:
        client: Amazon Bedrock agent boto3 client.
        flow_id (str): The identifier of the flow that you want to prepare.

    Returns:
        str: The status of the flow preparation
    """
    try:

        # Prepare the flow.
        logger.info("Preparing flow ID: %s",
                    flow_id)

        response = client.prepare_flow(
            flowIdentifier=flow_id
        )

        status = response.get('status')

        while status == "Preparing":
            logger.info("Preparing flow ID: %s. Status %s",
                        flow_id, status)

            sleep(5)
            response = client.get_flow(
                flowIdentifier=flow_id
            )
            status = response.get('status')
            print(f"Flow Status: {status}")

        if status == "Prepared":
            logger.info("Finished preparing flow ID: %s. Status %s",
                        flow_id, status)
        else:
            logger.warning("flow ID: %s not prepared. Status %s",
                           flow_id, status)

        return status

    except ClientError as e:
        logger.exception("Client error preparing flow: %s", {str(e)})
        raise

    except Exception as e:
        logger.exception("Unexepcted error preparing flow: %s", {str(e)})
        raise
```
+  For API details, see [PrepareFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/PrepareFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.