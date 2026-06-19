

# Use `DeleteAgentAlias` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_DeleteAgentAlias_section"></a>

The following code example shows how to use `DeleteAgentAlias`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke an agent](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockAgents_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Delete an agent alias.  

```
    def delete_agent_alias(self, agent_id, agent_alias_id):
        """
        Deletes an alias of an Amazon Bedrock agent.

        :param agent_id: The unique identifier of the agent that the alias belongs to.
        :param agent_alias_id: The unique identifier of the alias to delete.
        :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
        """

        try:
            response = self.client.delete_agent_alias(
                agentId=agent_id, agentAliasId=agent_alias_id
            )
        except ClientError as e:
            logger.error(f"Couldn't delete agent alias. {e}")
            raise
        else:
            return response
```
+  For API details, see [DeleteAgentAlias](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/DeleteAgentAlias) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.