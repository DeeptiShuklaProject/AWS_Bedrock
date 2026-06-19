

# Use `ListFlowVersions` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_ListFlowVersions_section"></a>

The following code example shows how to use `ListFlowVersions`.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
List the versions of an Amazon Bedrock flow.  

```
def list_flow_versions(client, flow_id):
    """
    Lists the versions of an Amazon Bedrock flow.

    Args:
        client: Amazon bedrock agent boto3 client.
        flow_id (str): The identifier of the flow.

    Returns:
        dict: The response from ListFlowVersions.
    """
    try:

        finished = False

        logger.info("Listing flow versions for flow: %s.", flow_id)

        response = client.list_flow_versions(
            flowIdentifier=flow_id,
            maxResults=10)

        while finished is False:

            print(f"Versions for flow:{flow_id}")
            for version in response['flowVersionSummaries']:
                print(f"Version: {version['version']}")
                print(f"Status: {version['status']}\n")

                if 'nextToken' in response:
                    next_token = response['nextToken']
                    response = client.list_flow_versions(maxResults=10,
                                                nextToken=next_token)
                else:
                    finished = True


        logging.info("Successfully listed flow versions for flow %s.",
                flow_id)
        
        return response

    except ClientError as e:
        logging.exception("Client error listing flow versions: %s", str(e))
        raise
    except Exception as e:
        logging.exception("Unexpected error listing flow versions: %s", str(e))
        raise
```
+  For API details, see [ListFlowVersions](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/ListFlowVersions) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.