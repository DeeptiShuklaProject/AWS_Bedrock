

# Customize agent orchestration strategy
<a name="orch-strategy"></a>

An orchestration strategy defines how an agent accomplishes a task. When an agent is given a task it has to develop a plan and execute that plan. The orchestration strategy defines the process of creating the plan and executing the plan which results in the final answer. The orchestration strategy generally relies on the prompts sent to the model to create the plan and give the appropriate actions to solve the user’s request. By default, agents use the orchestration strategy defined in the base default prompt templates. The default orchestration strategy is ReAct or Reason and Action which makes use of the foundation model’s tool use patterns where applicable. You can customize the orchestration strategy for your agent by creating an AWS Lambda function where you can add your own orchestration logic for your specific use case. 

Choose the orchestration strategy for your agent:
+ **Use advanced prompts** — Modify the base prompt templates to customize your agent's behavior by overriding the logic with your own configurations using advanced prompts templates. To use advanced prompts, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md). 
+ **Use custom orchestration** — Build Amazon Bedrock Agents that can implement complex orchestration workflows, verification steps, or multi-step processes that is specific to your use case. To use custom orchestration, see [Customize your Amazon Bedrock Agent's behavior with custom orchestration](agents-custom-orchestration.md).