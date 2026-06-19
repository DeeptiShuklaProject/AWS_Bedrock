

# Customize agent for your use case
<a name="agents-customize"></a>

After you have set up your agent, you can further customize its behavior with the following features:
+ **Advanced prompts** let you modify prompt templates to determine the prompt that is sent to the agent at each step of runtime.
+ **Session state** is a field that contains attributes that you can define during build-time when sending a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) request or that you can send at runtime with an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request. You can use these attributes to provide and manage context in a conversation between users and the agent.
+ Amazon Bedrock Agents offers options to choose different flows that can optimize on latency for simpler use cases in which agents have a single knowledge base. To learn more, refer to the performance optimization topic.

Select a topic to learn more about that feature.

**Topics**
+ [Customize agent orchestration strategy](orch-strategy.md)
+ [Control agent session context](agents-session-state.md)
+ [Optimize performance for Amazon Bedrock agents using a single knowledge base](agents-optimize-performance.md)
+ [Working with models not yet optimized for Amazon Bedrock Agents](working-with-models-not-yet-optimized.md)

**Note**  
The agent instructions will not be honored if your agent has only one knowledge base, uses default prompts, has no action group, and user input is disabled.