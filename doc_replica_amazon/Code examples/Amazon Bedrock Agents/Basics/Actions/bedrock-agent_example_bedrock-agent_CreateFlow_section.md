

# Use `CreateFlow` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreateFlow_section"></a>

The following code example shows how to use `CreateFlow`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke a flow](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create an Amazon Bedrock flow.  

```
def create_flow(client, flow_name, flow_description, role_arn, flow_def):
    """
    Creates an Amazon Bedrock flow.

    Args:
    client: Amazon Bedrock agent boto3 client.
    flow_name (str): The name for the new flow.
    role_arn (str):  The ARN for the IAM role that use flow uses.
    flow_def (json): The JSON definition of the flow that you want to create.

    Returns:
        dict: The response from CreateFlow.
    """
    try:

        logger.info("Creating flow: %s.", flow_name)

        response = client.create_flow(
            name=flow_name,
            description=flow_description,
            executionRoleArn=role_arn,
            definition=flow_def
        )

        logger.info("Successfully created flow: %s. ID: %s",
                    flow_name,
                    {response['id']})

        return response

    except ClientError as e:
        logger.exception("Client error creating flow: %s", {str(e)})
        raise

    except Exception as e:
        logger.exception("Unexepcted error creating flow: %s", {str(e)})
        raise
```
+  For API details, see [CreateFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreateFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.