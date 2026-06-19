

# How Amazon Bedrock Agents works
<a name="agents-how"></a>


|  | 
| --- |
| *Accelerate agents to production with Amazon Bedrock AgentCore. AgentCore is an agentic platform to build, deploy, and operate highly capable agents securely at scale. For more information, see the [AgentCore developer guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html).* | 

Amazon Bedrock Agents consists of the following two main sets of API operations to help you set up and run an agent:
+ [Build-time API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) to create, configure, and manage your agents and their related resources
+ [Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html) to invoke your agent with user input and to initiate orchestration to carry out a task

## Build-time configuration
<a name="agents-btl"></a>

An agent consists of the following components:
+ **Foundation model** – You choose a foundation model (FM) that the agent invokes to interpret user input and subsequent prompts in its orchestration process. The agent also invokes the FM to generate responses and follow-up steps in its process.
+ **Instructions** – You write instructions that describe what the agent is designed to do. With advanced prompts, you can further customize instructions for the agent at every step of orchestration and include Lambda functions to parse each step's output.
+ At least one of the following:
  + **Action groups** – You define the actions that the agent should perform for the user (through providing the following resources):
    + One of the following schemas to define the parameters that the agent needs to elicit from the user (each action group can use a different schema):
      + An OpenAPI schema to define the API operations that the agent can invoke to perform its tasks. The OpenAPI schema includes the parameters that need to be elicited from the user.
      + A function detail schema to define the parameters that the agent can elicit from the user. These parameters can then be used for further orchestration by the agent, or you can set up how to use them in your own application.
    + (Optional) A Lambda function with the following input and output:
      + Input – The API operation and/or parameters identified during orchestration.
      + Output – The response from the API invocation or the response from the function invocation.
  + **Knowledge bases** – Associate knowledge bases with an agent. The agent queries the knowledge base for extra context to augment response generation and input into steps of the orchestration process.
+ **Prompt templates** – Prompt templates are the basis for creating prompts to be provided to the FM. Amazon Bedrock Agents exposes the default four base prompt templates that are used during the pre-processing, orchestration, knowledge base response generation, and post-processing. You can optionally edit these base prompt templates to customize your agent's behavior at each step of its sequence. You can also turn off steps for troubleshooting purposes or if you decide that a step is unnecessary. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](advanced-prompts.md).

At build-time, all these components are gathered to construct base prompts for the agent to perform orchestration until the user request is completed. With advanced prompts, you can modify these base prompts with additional logic and few-shot examples to improve accuracy for each step of agent invocation. The base prompt templates contain instructions, action descriptions, knowledge base descriptions, and conversation history, all of which you can customize to modify the agent to meet your needs. You then *prepare* your agent, which packages all the components of the agents, including security configurations. Preparing the agent brings it into a state where it can be tested in runtime. The following image shows how build-time API operations construct your agent.

![How build-time APIs construct your agent with action groups and knowledge bases.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/agents/agents-buildtime.png)


An action group consists of an OpenAPI schema and a Lambda function to define what API operations an agent can call and how the agent should handle the requests and responses. The agent synthesizes information from the base prompt templates, instructions provided to it, and any attached action groups and knowledge bases to generate prompts with the model that it uses. The prompts are added to the agent's prompt store.

## Runtime process
<a name="agents-rt"></a>

Runtime is managed by the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) API operation. This operation starts the agent sequence, which consists of the following three main steps.

1. **Pre-processing** – Manages how the agent contextualizes and categorizes user input and can be used to validate input.

1. **Orchestration** – Interprets the user input, invokes action groups and queries knowledge bases, and returns output to the user or as input to continued orchestration. Orchestration consists of the following steps:

   1. The agent interprets the input with a foundation model and generates a *rationale* that lays out the logic for the next step it should take.

   1. The agent predicts which action in an action group it should invoke or which knowledge base it should query.

   1. If the agent predicts that it needs to invoke an action, the agent sends the parameters, determined from the user prompt, to the [Lambda function configured for the action group](agents-lambda.md) or [returns control](agents-returncontrol.md) by sending the parameters in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. If the agent doesn't have enough information to invoke the action, it might do one of the following actions:
      + Query an associated knowledge base (**Knowledge base response generation**) to retrieve additional context and summarize the data to augment its generation.
      + Reprompt the user to gather all the required parameters for the action.

   1. The agent generates an output, known as an *observation*, from invoking an action and/or summarizing results from a knowledge base. The agent uses the observation to augment the base prompt, which is then interpreted with a foundation model. The agent then determines if it needs to reiterate the orchestration process.

   1. This loop continues until the agent returns a response to the user or until it needs to prompt the user for extra information.

   During orchestration, the base prompt template is augmented with the agent instructions, action groups, and knowledge bases that you added to the agent. Then, the augmented base prompt is used to invoke the FM. The FM predicts the best possible steps and trajectory to fulfill the user input. At each iteration of orchestration, the FM predicts the API operation to invoke or the knowledge base to query.

1. **Post-processing** – The agent formats the final response to return to the user. This step is turned off by default.

When you invoke your agent, you can turn on a **trace** at runtime. With the trace, you can track the agent's rationale, actions, queries, and observations at each step of the agent sequence. The trace includes the full prompt sent to the foundation model at each step and the outputs from the foundation model, API responses, and knowledge base queries. You can use the trace to understand the agent's reasoning at each step. For more information, see [Track agent's step-by-step reasoning process using trace](trace-events.md).

As the user session with the agent continues through more `InvokeAgent` requests, the conversation history is preserved. The conversation history continually augments the orchestration base prompt template with context, helping improve the agent's accuracy and performance. The following diagram shows the agent's process during runtime:

![How your agent processes user input at runtime through orchestration and action execution.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/agents/agents-runtime.png)


After receiving user input, the agent fetches augmented prompts from the prompt store and conversation history from the sessions store. If the preprocessing step is enabled, the agent invokes the FM with the preprocessing prompt to validate the user input. In the orchestration step, the agent invokes the FM with the orchestration prompt and parses the response. It then determines action groups and queries knowledge bases as necessary and generates an observation that might trigger a new orchestration prompt. The orchestration stage loops until the observation returns a final response to the user.