

# Automate tasks in your application using AI agents
<a name="agents"></a>

Amazon Bedrock Agents offers you the ability to build and configure autonomous agents in your application. An agent helps your end-users complete actions based on organization data and user input. Agents orchestrate interactions between foundation models (FMs), data sources, software applications, and user conversations. In addition, agents automatically call APIs to take actions and invoke knowledge bases to supplement information for these actions. By integrating agents, you can accelerate your development effort to deliver generative artificial intelligence (generative AI) applications.

With agents, you can automate tasks for your customers and answer questions for them. For example, you can create an agent that helps customers process insurance claims or an agent that helps customers make travel reservations. You don't have to provision capacity, manage infrastructure, or write custom code. Amazon Bedrock manages prompt engineering, memory, monitoring, encryption, user permissions, and API invocation.

Agents perform the following tasks:
+ Extend foundation models to understand user requests and break down the tasks that the agent must perform into smaller steps.
+ Collect additional information from a user through natural conversation.
+ Take actions to fulfill a customer's request by making API calls to your company systems.
+ Augment performance and accuracy by querying data sources. 

To use an agent, you perform the following steps:

1. (Optional) Create a knowledge base to store your private data in that database. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md).

1. Configure an agent for your use case and add at least one of the following components:
   + At least one action group that the agent can perform. To learn how to define the action group and how it's handled by the agent, see [Use action groups to define actions for your agent to perform](agents-action-create.md).
   + Associate a knowledge base with the agent to augment the agent's performance. For more information, see [Augment response generation for your agent with knowledge base](agents-kb-add.md).

1. (Optional) To customize the agent's behavior to your specific use-case, modify prompt templates for the pre-processing, orchestration, knowledge base response generation, and post-processing steps that the agent performs. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md).

1. Test your agent in the Amazon Bedrock console or through API calls to the `TSTALIASID`. Modify the configurations as necessary. Use traces to examine your agent's reasoning process at each step of its orchestration. For more information, see [Test and troubleshoot agent behavior](agents-test.md) and [Track agent's step-by-step reasoning process using trace](trace-events.md).

1. When you have sufficiently modified your agent and it's ready to be deployed to your application, create an alias to point to a version of your agent. For more information, see [Deploy and use an Amazon Bedrock agent in your application](agents-deploy.md).

1. Set up your application to make API calls to your agent alias.

1. Iterate on your agent and create more versions and aliases as necessary.