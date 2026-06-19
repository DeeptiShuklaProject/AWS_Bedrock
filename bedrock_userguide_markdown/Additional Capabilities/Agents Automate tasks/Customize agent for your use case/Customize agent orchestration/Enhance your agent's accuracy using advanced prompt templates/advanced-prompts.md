

# Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock
<a name="advanced-prompts"></a>

After creation, an agent is configured with the following four default **base prompt templates**, which outline how the agent constructs prompts to send to the foundation model at each step of the agent sequence. For details about what each step encompasses, see [Runtime process](agents-how.md#agents-rt).
+ Pre-processing
+ Orchestration
+ Knowledge base response generation
+ Post-processing (disabled by default)
+ Memory Summarization
+ Routing Classifier

Prompt templates define how the agent does the following:
+ Processes user input text and output prompts from foundation models (FMs)
+ Orchestrates between the FM, action groups, and knowledge bases
+ Formats and returns responses to the user

By using advanced prompts, you can enhance your agent's accuracy through modifying these prompt templates to provide detailed configurations. You can also provide hand-curated examples for *few-shot prompting*, in which you improve model performance by providing labeled examples for a specific task.

Select a topic to learn more about advanced prompts.

**Topics**
+ [Advanced prompts terminology](#advanced-prompts-terminology)
+ [Advanced prompt templates](advanced-prompts-templates.md)
+ [Configure advanced prompts](configure-advanced-prompts.md)
+ [Use placeholder variables in Amazon Bedrock agent prompt templates](prompt-placeholders.md)
+ [Write a custom parser Lambda function in Amazon Bedrock Agents](lambda-parser.md)

## Advanced prompts terminology
<a name="advanced-prompts-terminology"></a>

The following terminology is helpful in understanding how advanced prompts work.
+ **Session** – A group of [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) requests made to the same agent with the same session ID. When you make an `InvokeAgent` request, you can reuse a `sessionId` that was returned from the response of a previous call to continue the same session with an agent. As long as the `idleSessionTTLInSeconds` time in the [Agent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) configuration hasn't expired, you maintain the same session with the agent.
+ **Turn** – A single `InvokeAgent` call. A session consists of one or more turns.
+ **Iteration** – A sequence of the following actions:

  1. (Required) A call to the foundation model

  1. (Optional) An action group invocation

  1. (Optional) A knowledge base invocation

  1. (Optional) A response to the user asking for more information

  An action might be skipped, depending on the configuration of the agent or the agent's requirement at that moment. A turn consists of one or more iterations.
+ **Prompt** – A prompt consists of the instructions to the agent, context, and text input. The text input can come from a user or from the output of another step in the agent sequence. The prompt is provided to the foundation model to determine the next step that the agent takes in responding to user input
+ **Base prompt template** – The structural elements that make up a prompt. The template consists of placeholders that are filled in with user input, the agent configuration, and context at runtime to create a prompt for the foundation model to process when the agent reaches that step. For more information about these placeholders, see [Use placeholder variables in Amazon Bedrock agent prompt templates](prompt-placeholders.md). With advanced prompts, you can edit these templates.
+ **Payload referencing** – A prompt compression feature that is used with multi-agent collaboration and is enabled for the primary agent by default. It helps reduce output tokens used by primary agent to communicate with the sub-agent or the end-user thus helping in reducing cost. It also reduces the size of conversation history if there were repeated payloads in the prompt. 