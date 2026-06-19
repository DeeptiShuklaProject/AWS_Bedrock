

# Build and modify agents in Amazon Bedrock for your application
<a name="agents-build-modify"></a>

Amazon Bedrock agents automate tasks for your application users by orchestrating interactions between the foundation model, data sources, software applications and user conversations. Agents also automatically call APIs to take actions and invoke knowledge bases to supplement information for these actions. Before you can start using agents for your application, you must first build your agent by creating and then configuring your agent to perform the tasks.

Amazon Bedrock provides you with the following options for building an agent for your use case.

**Create and configure your agent manually**

After you've created your agent, configure the agent by setting up an action group that defines actions that the agent can help end users perform. Action group includes the parameters that the agent must elicit from your application user, APIs that can be called, how to handle the action, and how to return a response. 

You can skip defining an action group for your agent and instead choose to set up knowledge bases that provides a repository of information that agent can query to answer queries from your application users. 

You can manually create, configure, modify, and delete your agent in the console, using the CLI, or using the SDKs. For more information, see [Create and configure agent manually](agents-create.md).

**Configure your agent using conversational builder**

After you’ve created your agent, you can optionally use *Conversational Builder* to configure your agent. Conversational builder is an interactive assistant that is available in the Amazon Bedrock console. Conversational builder helps in configuring an agent for you. With conversational builder, you interact with the assistant using natural language to describe the purpose of your agent and information your agent might require to fulfill the purpose. The agent is built for you using the information you provide. Use conversational builder if you want to quickly configure or modify an agent. You can modify and delete your agent at any time in the console, using the conversational builder. For more information, see [Configure your agent using conversational builder](agents-create-cb.md).

**Configure and invoke an agent dynamically at runtime**

You can configure and invoke an inline Amazon Bedrock agent dynamically at runtime using [InvokeInlineAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html) API. Using an inline agent provides you with flexibility to specify your agent capabilities like foundation models, instructions, action groups, guardrails, and knowledge bases at the same time you invoke your agent. You do not need to pre-define agent capabilities before you can use it. For more information, see [Configure an inline agent at runtime](agents-create-inline.md).

**Use pre-built templates to jumpstart the use of agents for your use case**

Amazon Bedrock provides you with *Agent Blueprints* to jumpstart your use of Amazon Bedrock Agents. Blueprints are a collection of pre-built templates optimized for popular use cases. These templates allows you to quickly experiment with agent-based applications without the need for configurations and lengthy development cycles. Agent Blueprints are open-source templates hosted on [amazon-bedrock-samples](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/agents-and-function-calling/bedrock-agents/agent-blueprint-templates) GitHib repository. The templates come with sample actions, Guardrails, and Knowledge Bases. For more information, see [Introducing Blueprints to simplify agent-based automation on Amazon Bedrock](https://aws.amazon.com/about-aws/whats-new/2024/08/blueprints-agent-based-automation-amazon-bedrock/).

**Topics**
+ [Configure your agent using conversational builder](agents-create-cb.md)
+ [Configure an inline agent at runtime](agents-create-inline.md)
+ [Create and configure agent manually](agents-create.md)
+ [View information about an agent](agents-view.md)
+ [Modify an agent](agents-edit.md)
+ [Delete an agent](agents-delete.md)