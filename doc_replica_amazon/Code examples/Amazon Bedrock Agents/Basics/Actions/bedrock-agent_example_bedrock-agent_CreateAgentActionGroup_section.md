

# Use `CreateAgentActionGroup` with an AWS SDK
<a name="bedrock-agent_example_bedrock-agent_CreateAgentActionGroup_section"></a>

The following code example shows how to use `CreateAgentActionGroup`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code example: 
+  [Create and invoke an agent](bedrock-agent_example_bedrock-agent_GettingStartedWithBedrockAgents_section.md) 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent#code-examples). 
Create an agent action group.  

```
    def create_agent_action_group(
            self, name, description, agent_id, agent_version, function_arn, api_schema
    ):
        """
        Creates an action group for an agent. An action group defines a set of actions that an
        agent should carry out for the customer.

        :param name: The name to give the action group.
        :param description: The description of the action group.
        :param agent_id: The unique identifier of the agent for which to create the action group.
        :param agent_version: The version of the agent for which to create the action group.
        :param function_arn: The ARN of the Lambda function containing the business logic that is
                             carried out upon invoking the action.
        :param api_schema: Contains the OpenAPI schema for the action group.
        :return: Details about the action group that was created.
        """
        try:
            response = self.client.create_agent_action_group(
                actionGroupName=name,
                description=description,
                agentId=agent_id,
                agentVersion=agent_version,
                actionGroupExecutor={"lambda": function_arn},
                apiSchema={"payload": api_schema},
            )
            agent_action_group = response["agentActionGroup"]
        except ClientError as e:
            logger.error(f"Error: Couldn't create agent action group. Here's why: {e}")
            raise
        else:
            return agent_action_group
```
+  For API details, see [CreateAgentActionGroup](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-2023-12-12/CreateAgentActionGroup) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.