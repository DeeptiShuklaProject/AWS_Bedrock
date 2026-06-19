

# Use `PrepareAgent` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_PrepareAgent_section"></a>

The following code example shows how to use `PrepareAgent`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke an agent](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockAgents_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Prepare an agent for internal testing.  

```
    def prepare_agent(self, agent_id):
        """
        Creates a DRAFT version of the agent that can be used for internal testing.

        :param agent_id: The unique identifier of the agent to prepare.
        :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
        """
        try:
            prepared_agent_details = self.client.prepare_agent(agentId=agent_id)
        except ClientError as e:
            logger.error(f"Couldn't prepare agent. {e}")
            raise
        else:
            return prepared_agent_details
```
+  For API details, see [PrepareAgent](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/PrepareAgent) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.