

# Prerequisites for creating Amazon Bedrock Agents
<a name="agents-prereq"></a>

Ensure that your IAM role has the [necessary permissions](security_iam_id-based-policy-examples-agent.md#iam-agents-ex-all) to perform actions related to Amazon Bedrock Agents.

Before creating an agent, review the following prerequisites and determine which ones you need to fulfill:

1. You must set up at least one of the following for your agent:
   + [Action group](agents-action-create.md) – Defines actions that the agent can help end users perform. Each action group includes the parameters that the agent must elicit from the end-user. You can also define the APIs that can be called, how to handle the action, and how to return the response. To see the quota for action groups in an agent, refer to the **Action groups per Agent** quota in [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) in the AWS General Reference. You can skip this prerequisite if you plan to have no action groups for your agent.
   + [Knowledge base](knowledge-base.md) – Provides a repository of information that the agent can query to answer customer queries and improve its generated responses. Associating at least one knowledge base can help improve responses to customer queries by using private data sources. To see the quota for knowledge bases attached to an agent, refer to the **Associated knowledge bases per Agent** quota in [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) in the AWS General Reference. You can skip this prerequisite if you plan to have no knowledge bases associated with your agent.

1. (Optional) [Create a custom AWS Identity and Access Management (IAM) [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) for your agent with the proper permissions](agents-permissions.md). You can skip this prerequisite if you plan to use the AWS Management Console to automatically create a service role for you.

1. (Optional) Create a [guardrail](guardrails.md) to implement safeguards for your agent and to prevent unwanted behavior from model responses and user messages. You can then associate it with your agent.

1. (Optional) Purchase [Provisioned Throughput](prov-throughput.md) to increase the number and rate of tokens that your agent can process in a given time frame. You can then associate it with an alias of your agent when you [create a version of your agent and associate an alias with it](agents-deploy.md).