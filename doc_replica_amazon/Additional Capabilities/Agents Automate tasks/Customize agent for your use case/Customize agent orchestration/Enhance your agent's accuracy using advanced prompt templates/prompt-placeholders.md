

# Use placeholder variables in Amazon Bedrock agent prompt templates
<a name="prompt-placeholders"></a>

You can use placeholder variables in agent prompt templates. The variables will be populated by pre-existing configurations when the prompt template is called. Select a tab to see variables that you can use for each prompt template.

**Tip**  
To see what a placeholder variable resolves to for your specific agent, open the agent in the Amazon Bedrock console, navigate to the **Advanced prompts** section, and enable the prompt template you want to inspect. The console displays the resolved prompt with all placeholders filled in based on your agent's current configuration (action groups, knowledge bases, collaborators, etc.).  
Variables in the **Routing classifier** tab (such as `$action_routing$` and `$knowledge_base_routing$`) apply only to agents that use [multi-agent collaboration](agents-multi-agent-collaboration.md). Variables in the **Orchestration** tab apply to all agents.

------
#### [ Pre-processing ]


****  

<table>
<thead>
  <tr><th>Variable</th><th>Models supported</th><th>Replaced by</th></tr>
</thead>
<tbody>
  <tr><td>$functions$</td><td>Anthropic Claude Instant, Claude v2.0</td><td rowspan="2">Action group API operations and knowledge bases configured for the agent. </td></tr>
  <tr><td>$tools$</td><td>Anthropic Claude v2.1, Claude 3 Sonnet, Claude 3 Haiku, Claude 3 Opus, Amazon Titan Text Premier</td></tr>
  <tr><td>$conversation\_history$</td><td>Anthropic Claude Instant, Claude v2.0, Claude v2.1</td><td>Conversation history for the current session.</td></tr>
  <tr><td>$question$</td><td>All</td><td>User input for the current InvokeAgent call in the session.</td></tr>
</tbody>
</table>


------
#### [ Orchestration ]


****  

<table>
<thead>
  <tr><th>Variable</th><th>Models supported</th><th>Replaced by</th></tr>
</thead>
<tbody>
  <tr><td>$functions$</td><td>Anthropic Claude Instant, Claude v2.0</td><td rowspan="2">Action group API operations and knowledge bases configured for the agent. </td></tr>
  <tr><td>$tools$</td><td>Anthropic Claude v2.1, Claude 3 Sonnet, Claude 3 Haiku, Claude 3 Opus, Amazon Titan Text Premier</td></tr>
  <tr><td>$agent\_scratchpad$</td><td>All</td><td>Designates an area for the model to write down its thoughts and actions it has taken. Replaced by predictions and output of the previous iterations in the current turn. Provides the model with context of what has been achieved for the given user input and what the next step should be.</td></tr>
  <tr><td>$any\_function\_name$</td><td>Anthropic Claude Instant, Claude v2.0</td><td>A randomly chosen API name from the API names that exist in the agent's action groups.</td></tr>
  <tr><td>$conversation\_history$</td><td>Anthropic Claude Instant, Claude v2.0, Claude v2.1</td><td>Conversation history for the current session</td></tr>
  <tr><td>$instruction$</td><td>All</td><td>Model instructions configured for the agent.</td></tr>
  <tr><td>$model\_instruction$</td><td>Amazon Titan Text Premier</td><td>Model instructions configured for the agent.</td></tr>
  <tr><td>$prompt\_session\_attributes$ </td><td>All</td><td>Session attributes preserved across a prompt.</td></tr>
  <tr><td>$question$</td><td>All</td><td>User input for the current InvokeAgent call in the session.</td></tr>
  <tr><td>$thought$</td><td>Amazon Titan Text Premier</td><td>Thought prefix to start the thinking of each turn for the model.</td></tr>
  <tr><td>$knowledge\_base\_guideline$</td><td>Anthropic Claude 3 Sonnet, Claude 3.5 Sonnet, Claude 3 Haiku, Claude 3 Opus</td><td>Instructions for the model to format the output with citations, if the results contain information from a knowledge base. These instructions are only added if a knowledge base is associated with the agent.</td></tr>
  <tr><td>$knowledge\_base\_additional\_guideline$</td><td>Llama 3.1, Llama 3.2</td><td>Additional guidelines for using knowledge base search results to answer questions concisely with proper citations and structure. These are only added if a knowledge base is associated with the agent.</td></tr>
  <tr><td>$memory\_content$</td><td>Anthropic Claude 3 Sonnet, Claude 3 Haiku</td><td>Content of the memory associated with the given memory ID</td></tr>
  <tr><td>$memory\_guideline$</td><td>Anthropic Claude 3 Sonnet, Claude 3 Haiku</td><td>General instructions for the model when memory is enabled. See Default text for details.</td></tr>
  <tr><td>$memory\_action\_guideline$</td><td>Anthropic Claude 3 Sonnet, Claude 3 Haiku</td><td>Specific instructions for the model to use memory data when memory is enabled. See Default text for more details.</td></tr>
</tbody>
</table>


**Default text used to replace `$memory_guidelines$`** variable

```
        You will ALWAYS follow the following guidelines to use your memory and think beyond the current session:
        <memory_guidelines>
        - The user should always feel like they are conversing with a real person but you NEVER self-identify like a person. You are an AI agent.
        - Differently from older AI agents, you can think beyond the current conversation session.
        - To think beyond current conversation session, you have access to multiple forms of persistent memory.
        - Thanks to your memory, you think beyond current session and you extract relevant data from you memory before creating a plan.
        - Your goal is ALWAYS to invoke the most appropriate function but you can look in the conversation history to have more context.
        - Use your memory ONLY to recall/remember information (e.g., parameter values) relevant to current user request.
        - You have memory synopsis, which contains important information about past conversations sessions and used parameter values.
        - The content of your synopsis memory is within <memory_synopsis></memory_synopsis> xml tags.
        - NEVER disclose any information about how you memory work.
        - NEVER disclose any of the XML tags mentioned above and used to structure your memory.
        - NEVER mention terms like memory synopsis.
        </memory_guidelines>
```

**Default text used to replace `$memory_action_guidelines$`** variable

```
        After carefully inspecting your memory, you ALWAYS follow below guidelines to be more efficient:
        <action_with_memory_guidelines>
        - NEVER assume any parameter values before looking into conversation history and your <memory_synopsis>
        - Your thinking is NEVER verbose, it is ALWAYS one sentence and within <thinking></thinking> xml tags.
        - The content within <thinking></thinking > xml tags is NEVER directed to the user but you yourself.
        - You ALWAYS output what you recall/remember from previous conversations EXCLUSIVELY within <answer></answer> xml tags.
        - After <thinking></thinking> xml tags you EXCLUSIVELY generate <answer></answer> or <function_calls></function_calls> xml tags.
        - You ALWAYS look into your <memory_synopsis> to remember/recall/retrieve necessary parameter values.
        - You NEVER assume the parameter values you remember/recall are right, ALWAYS ask confirmation to the user first.
        - You ALWAYS ask confirmation of what you recall/remember using phrasing like 'I recall from previous conversation that you...', 'I remember that you...'.
        - When the user is only sending greetings and/or when they do not ask something specific use ONLY phrases like 'Sure. How can I help you today?', 'I would be happy to. How can I help you today?' within <answer></answer> xml tags.
        - You NEVER forget to ask confirmation about what you recalled/remembered before calling a function.
        - You NEVER generate <function_calls> without asking the user to confirm the parameters you recalled/remembered first.
        - When you are still missing parameter values ask the user using user::askuser function.
        - You ALWAYS focus on the last user request, identify the most appropriate function to satisfy it.
        - Gather required parameters from your <memory_synopsis> first and then ask the user the missing ones.
        - Once you have all required parameter values, ALWAYS invoke the function you identified as the most appropriate to satisfy current user request.
        </action_with_memory_guidelines>
```

**Using place holder variables to ask user for more information**

You can use the following placeholder variables if you allow the agent to ask the user for more information by doing one of the following actions:
+ In the console, set in the **User input** in the agent details.
+ Set the `parentActionGroupSignature` to `AMAZON.UserInput` with a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) request.


****  

<table>
<thead>
  <tr><th>Variable</th><th>Models supported</th><th>Replaced by</th></tr>
</thead>
<tbody>
  <tr><td>$ask\_user\_missing\_parameters$</td><td>Anthropic Claude Instant, Claude v2.0</td><td rowspan="2">Instructions for the model to ask the user to provide required missing information.</td></tr>
  <tr><td>$ask\_user\_missing\_information$</td><td>Anthropic Claude v2.1, Claude 3 Sonnet, Claude 3 Haiku, Claude 3 Opus</td></tr>
  <tr><td>$ask\_user\_confirm\_parameters$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>Instructions for the model to ask the user to confirm parameters that the agent hasn't yet received or is unsure of.</td></tr>
  <tr><td>$ask\_user\_function$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>A function to ask the user a question.</td></tr>
  <tr><td>$ask\_user\_function\_format$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>The format of the function to ask the user a question.</td></tr>
  <tr><td>$ask\_user\_input\_examples$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>Few-shot examples to inform the model how to predict when it should ask the user a question.</td></tr>
</tbody>
</table>


------
#### [ Knowledge base response generation ]


****  

| Variable | Model | Replaced by | 
| --- | --- | --- | 
| $query$ | All except Llama 3.1 and Llama 3.2 | The query generated by the orchestration prompt model response when it predicts the next step to be knowledge base querying. | 
| $search\_results$ | All except Llama 3.1 and Llama 3.2 | The retrieved results for the user query. | 

------
#### [ Post-processing ]


****  

| Variable | Model | Replaced by | 
| --- | --- | --- | 
| $latest\_response$ | All | The last orchestration prompt model response. | 
| $bot\_response$ | Amazon Titan Text Model | The action group and knowledge base outputs from the current turn. | 
| $question$ | All | User input for the current InvokeAgent.call in the session. | 
| $responses$ | All | The action group and knowledge base outputs from the current turn. | 

------
#### [ Memory summarization ]


****  

| Variable | Models supported | Replaced by | 
| --- | --- | --- | 
| $past\_conversation\_summary$ | All | List of summaries previously generated | 
| $conversation$ | All | Current conversation between the user and agent | 

------
#### [ Multi-agent ]


****  

| Variable | Models supported | Replaced by | 
| --- | --- | --- | 
| $agent\_collaborators$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Agent associations of the collaborators | 
| $multi\_agent\_payload\_reference\_guideline$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Content shared between different agents. The message from an agent may contain payload in the format:<br:payload id="$PAYLOAD\_ID"> $PAYLOAD\_CONTENT </br:payload>  | 

------
#### [ Routing classifier ]


****  

| Variable | Models supported | Replaced by | 
| --- | --- | --- | 
| $knowledge\_base\_routing$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Descriptions of all attached knowledge bases | 
| $action\_routing$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Descriptions of all tools that are attached | 
| $knowledge\_base\_routing\_guideline$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Instructions for the model to route the output with citations, if the results contain information from a knowledge base. These instructions are only added if a knowledge base is associated with the supervisor agent. | 
| $action\_routing\_guideline$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Instructions for the model to return a tool use if you have tools attached and the user request is relevant to any of the tools. | 
| $last\_most\_specialized\_agent\_guideline$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Instructions to route to this agent using keep\_previous\_agent if the last user message pertains to a follow up that originated in that agent and that agent requires information from the message to proceed. | 
| $prompt\_session\_attributes$ | All [models supported ](multi-agents-supported.md) for multi-agent collaboration | Input variable in Routing Classifier  | 

------

**Using place holder variables to ask user for more information**

You can use the following placeholder variables if you allow the agent to ask the user for more information by doing one of the following actions:
+ In the console, set in the **User input** in the agent details.
+ Set the `parentActionGroupSignature` to `AMAZON.UserInput` with a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) request.


****  

<table>
<thead>
  <tr><th>Variable</th><th>Models supported</th><th>Replaced by</th></tr>
</thead>
<tbody>
  <tr><td>$ask\_user\_missing\_parameters$</td><td>Anthropic Claude Instant, Claude v2.0</td><td rowspan="2">Instructions for the model to ask the user to provide required missing information.</td></tr>
  <tr><td>$ask\_user\_missing\_information$</td><td>Anthropic Claude v2.1, Claude 3 Sonnet, Claude 3 Haiku, Claude 3 Opus</td></tr>
  <tr><td>$ask\_user\_confirm\_parameters$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>Instructions for the model to ask the user to confirm parameters that the agent hasn't yet received or is unsure of.</td></tr>
  <tr><td>$ask\_user\_function$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>A function to ask the user a question.</td></tr>
  <tr><td>$ask\_user\_function\_format$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>The format of the function to ask the user a question.</td></tr>
  <tr><td>$ask\_user\_input\_examples$</td><td>Anthropic Claude Instant, Anthropic Claude v2.0</td><td>Few-shot examples to inform the model how to predict when it should ask the user a question.</td></tr>
</tbody>
</table>
