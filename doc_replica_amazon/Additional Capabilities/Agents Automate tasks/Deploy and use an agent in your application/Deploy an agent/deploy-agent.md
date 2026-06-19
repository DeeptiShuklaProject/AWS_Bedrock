

# Deploy an agent
<a name="deploy-agent"></a>

When you first create an Amazon Bedrock agent, you have a working draft version (`DRAFT`) and a test alias (`TSTALIASID`) that points to the working draft version. When you make changes to your agent, the changes apply to the working draft. You iterate on your working draft until you're satisfied with the behavior of your agent. Then, you can set up your agent for deployment and integration into your application by creating *aliases* of your agent.

**Aliases and Versions**

To deploy your agent, you must create an *alias*. During alias creation, Amazon Bedrock creates a version of your agent automatically. The alias points to this newly created version. Alternatively, you can point the alias to a previously created version of your agent. Then, you configure your application to make API calls to that alias.

A *version* is a snapshot that preserves the resource as it exists at the time it was created. You can continue to modify the working draft and create new versions of your agent as necessary. Amazon Bedrock creates versions in numerical order, starting from 1. You can create a new version in the following ways:
+ Create a new alias and choose to create a new version to associate with it.
+ Update an existing alias to point to a new version. You can do this by using the [UpdateAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentAlias.html) operation or by editing the alias in the console. If you omit the `routingConfiguration`, Amazon Bedrock automatically creates a new version and associates it with the alias.

Versions are immutable because they act as a snapshot of your agent at the time you created it. To make updates to an agent in production, you must create a new version and set up your application to make calls to the alias that points to that version.

With aliases, you can switch efficiently between different versions of your agent without requiring the application to keep track of the version. For example, you can change an alias to point to a previous version of your agent if there are changes that you need to revert quickly.

## Pausing a deployed agent
<a name="agent-pause"></a>

You might need to temporarily pause the running of an agent. For example, during maintenance, updates, or when addressing performance issues. To pause an agent, you use the alias for the agent with the [UpdateAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentAlias.html) operation. To pause an agent, set the `aliasInvocationState` field to `REJECT_INVOCATIONS`. To start the agent running again, set `aliasInvocationState` to `ACCEPT_INVOCATIONS`. You don't need to make any IAM policy modifications to pause the agent.

To check if an agent is currently paused, call [GetAgentAlias](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgentAlias.html) and check the `aliasInvocationState` field. You can also check the `aliasInvocationState` field for an alias in the response from [ListAgentAliases](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentAliases.html). 

**Topics**
+ [Pausing a deployed agent](#agent-pause)
+ [Create an alias for your agent](deploy-agent-proc.md)
+ [View information about versions of agents in Amazon Bedrock](agents-version-view.md)
+ [Delete a version of an agent in Amazon Bedrock](agents-version-delete.md)
+ [View information about aliases of agents in Amazon Bedrock](agents-alias-view.md)
+ [Edit an alias of an agent in Amazon Bedrock](agents-alias-edit.md)
+ [Delete an alias of an agent in Amazon Bedrock](agents-alias-delete.md)