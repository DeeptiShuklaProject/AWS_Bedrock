

# Use `ListFlowAliases` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_ListFlowAliases_section"></a>

The following code example shows how to use `ListFlowAliases`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
List the aliases for an Amazon Bedrock flow.  

```
def list_flow_aliases(client, flow_id):
    """
    Lists the aliases of an Amazon Bedrock flow.

    Args:
        client: bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        dict: The response from ListFlowAliases.
    """
    try:

        finished = False

        logger.info("Listing flow aliases for flow: %s.", flow_id)

        print(f"Aliases for flow: {flow_id}")

        response = client.list_flow_aliases(
            flowIdentifier=flow_id,
            maxResults=10)

        while finished is False:

            for alias in response['flowAliasSummaries']:
                print(f"Alias Name: {alias['name']}")
                print(f"ID: {alias['id']}")
                print(f"Description: {alias.get('description', 'No description')}\n") 

                if 'nextToken' in response:
                    next_token = response['nextToken']
                    response = client.list_flow_aliases(maxResults=10,
                                                nextToken=next_token)
                else:
                    finished = True

        logging.info("Successfully listed flow aliases for flow %s.",
                flow_id)
        
        return response

    except ClientError as e:
        logging.exception("Client error listing flow aliases: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error listing flow aliases: %s", str(e))
        raise
```
+  For API details, see [ListFlowAliases](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/ListFlowAliases) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.