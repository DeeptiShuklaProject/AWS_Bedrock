

# Configure an Amazon Bedrock Agent to complete tasks with computer use tools
<a name="agents-computer-use"></a>

Computer use is an Anthropic Claude model capability (in beta) available with Anthropic Claude 3.7 Sonnet and Claude 3.5 Sonnet v2 only.

**Warning**  
Computer use feature is made available to you as a ‘Beta Service’ as defined in the AWS Service Terms. It is subject to your Agreement with AWS and the AWS Service Terms, and the applicable model EULA. Computer use poses unique risks that are distinct from standard API features or chat interfaces. These risks are heightened when using a computer use tool to interact with the Internet. To minimize risks, consider taking precautions such as:  
Operate computer use functionality in a dedicated Virtual Machine or container with minimal privileges to prevent direct system attacks or accidents.
To prevent information theft, avoid giving the computer use API access to sensitive accounts or data.
Limiting the computer use API’s internet access to required domains to reduce exposure to malicious content.
To ensure proper oversight, keep a human in the loop for sensitive tasks (such as making decisions that could have meaningful real-world consequences) and for anything requiring affirmative consent (such as accepting cookies, executing financial transactions, or agreeing to terms of service).
Any content that you enable Claude to see or access can potentially override instructions or cause Claude to make mistakes or perform unintended actions. Taking proper precautions, such as isolating Claude from sensitive surfaces, is essential — including to avoid risks related to prompt injection. Before enabling or requesting permissions necessary to enable computer use features in your own products, please inform end users of any relevant risks, and obtain their consent as appropriate. 

With computer use, an Amazon Bedrock Agent can use Claude to automate tasks through basic GUI actions and run linux commands that you implement. For example, when enabled your agent can take screen captures, create and edit text files, or run linux commands. Claude helps the agent predict which tools and tool actions to use, and the agent uses your tool implementation to complete the task. To enable computer use for an agent, you create an action group for the agent and specify a computer use tool. For more information about the workflow, see [Workflow](#agent-computer-use-workflow).

Your agent can use the following Anthropic-defined tools:
+ Computer – Actions include using the mouse and keyboard, and taking screen shots
+ TextEditor – Actions include viewing, creating and editing files.
+ Bash – Actions include running commands in a Bash shell.

For more information about computer use tools, including implementation examples and tool descriptions, see [Computer use (beta)](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) in the Anthropic documentation.

**Topics**
+ [Guardrail considerations](#agent-computer-use-guardrails)
+ [Workflow](#agent-computer-use-workflow)
+ [Specify the computer use tools for the agent in an action group](agent-computer-use-create-action-group.md)
+ [Handle computer use tool requests from agents in conversations](agent-computer-use-handle-tools.md)

## Guardrail considerations
<a name="agent-computer-use-guardrails"></a>

The following are guardrail considerations for computer use tools and agents:
+ We recommend that you implement safeguards for your application by associating a guardrail with your agent. For more information, see [Implement safeguards for your application by associating a guardrail with your agent](agents-guardrail.md). 
+ Due to limitations for image guardrails, if your application outputs text from images, use the [ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html) API to restrict this content before outputting it. For more information about guardrails in Amazon Bedrock, see [Detect and filter harmful content by using Amazon Bedrock Guardrails](guardrails.md).

## Workflow
<a name="agent-computer-use-workflow"></a>

To use computer use tools with your Amazon Bedrock Agents, you do the following:

1.  Create an action group and specify a computer use tool. You specify the tools available to the agent in the [CreateAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [UpdateAgentActionGroup](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) API operation. For inline agents, you specify the tool in the [InvokeInlineAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html) API operation. 

1. Implement the computer use functions in your application. For example tool implementations, see [anthropic-quickstarts/computer-use-demo/tools](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools) in the [anthropic-quickstarts](https://github.com/anthropics/anthropic-quickstarts) GitHub repository. 

1. Handle computer use tool requests from agents in conversations. After you use the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) API operation, extract the tool and action choice from the response, and then execute your implementation of the tool action. 