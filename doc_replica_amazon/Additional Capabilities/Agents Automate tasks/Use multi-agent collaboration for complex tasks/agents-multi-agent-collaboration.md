

# Use multi-agent collaboration with Amazon Bedrock Agents
<a name="agents-multi-agent-collaboration"></a>

Multi-agent collaboration enables multiple Amazon Bedrock Agents to collaboratively plan and solve complex tasks. With multi-agent collaboration, you can quickly assemble a team of agents that can break down tasks, assign specific tasks to domain specialist sub-agents, work in parallel, and use each other's strengths, which leads to more efficient problem-solving. Multi-agent provides a centralized mechanism for planning, orchestration , and user interaction for your generative AI applications. 

With multi-agent approach, you can quickly designate an Amazon Bedrock Agent as the supervisor and then associate one or more collaborator agents with the supervisor. You can use this hierarchical collaboration model to synchronously respond to prompts and queries from users in real-time. As your hierarchical model matures, you can add additional collaborator agents to augment its capabilities. 

**Important**  
Before you can enable multi-agent collaboration, you must first save the surpervisor agent. After the supervisor agent has been saved, you can update the agent and associate additional collaborator agents to it.

The supervisor agent uses the instructions you provide to understand the structure and role of each collaborator agent. To ensure that the team performs well, you must clearly designate the role and responsibilities of the supervisor agent and every collaborator agent on the team and minimize overlapping responsibilities. You can describe each agent’s role and responsibilities using natural language. For example, you could use multi-agent collaboration to create an online mortgage assistant. Each Amazon Bedrock agent can be configured to carry out one of the following tasks:
+ **Supervisor agent** – Takes questions from the user, checks if the question is about the existing mortgage, new mortgage, or it is a general question and routes the question to the appropriate collaborator agent.
+ **Collaborator agent 1** – Responsible for handling existing mortgages
+ **Collaborator agent 2** – Responsible for handling new mortgage applications and for answering questions related to new mortgages.
+ **Collaborator agent 3** – Responsible for handling general questions. 

 Each agent on the team, including the supervisor agent, is optimized for a specific use case, has all the capabilities of Amazon Bedrock Agents, including access to tools, action groups, knowledge bases, and guardrails. When you invoke the supervisor agent, it automatically creates and executes a plan across a set of collaborator agents and routes relevant requests and tasks to the appropriate collaborator agent. 