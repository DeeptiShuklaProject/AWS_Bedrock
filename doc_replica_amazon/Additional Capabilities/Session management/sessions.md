

# Store and retrieve conversation history and context with session management APIs
<a name="sessions"></a>

**Note**  
The session management APIs are in preview and are subject to change.

 The session management APIs enable you to save checkpoints for ongoing conversations in generative AI applications built with open-source frameworks, such as LangGraph and LlamaIndex. You can use the APIs to securely manage state and conversation context across multi-step generative AI workflows. You don’t have to build, maintain, or scale custom back-end solutions for state and context persistence. 

With the session management APIs, you can do the following:
+ Checkpoint workflow stages for iterative testing and human-in-the-loop workflows.
+  Resume conversations and tasks from the point of interruption. 
+ Review session logs to analyze workflow stages and debug failures.

Because sessions are a resource in Amazon Bedrock, you can control access to the session with AWS Identity and Access Management (IAM). By default, Amazon Bedrock uses AWS-managed keys for session encryption, including session metadata, or you can use your own AWS KMS key. For more information, see [Session encryption](sessions-encryption.md).

 You can create and manage Amazon Bedrock sessions with the Amazon Bedrock APIs, or AWS SDKs. For applications built on LangGraph, you can use the `BedrockSessionSaver` class from the `langgraph_checkpoint_aws.saver` library. This is a custom implementation of the LangGraph CheckpointSaver. For more information, see [langgraph-checkpoint-aws](https://github.com/langchain-ai/langchain-aws/tree/main/libs/langgraph-checkpoint-aws) in the [LangChain](https://github.com/langchain-ai) GitHub repository.

**Note**  
You use a session to store state and conversation history for generative AI applications built with open-source frameworks. For Amazon Bedrock Agents, the service automatically manages conversation context and associates them with the agent-specific sessionId you specify in the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) API operation.

**Topics**
+ [Use case example](#sessions-use-case)
+ [Workflow](#sessions-workflow)
+ [Considerations](#sessions-considerations)
+ [Session encryption](sessions-encryption.md)
+ [Create a session to prepare to store conversation history and context](sessions-create.md)
+ [Store conversation history and context in a session](sessions-store-coversation.md)
+ [Retrieve conversation history and context from a session](sessions-retrieve-coversation.md)
+ [End a session when the user ends the conversation](sessions-end-session.md)
+ [Delete a session and all of its data](sessions-delete-session.md)
+ [Store and retrieve conversation history and context with the BedrockSessionSaver LangGraph library](sessions-opensource-library.md)

## Use case example
<a name="sessions-use-case"></a>

You might have an application that uses a LangGraph agent to help customers plan travel itineraries. A user can start a conversation with this agent to create the itinerary for an upcoming trip, adding destinations, preferred hotels, and flight details. 

With session management APIs, the agent can save intermediate states and persistent context across the extended multi-step interaction. The agent could use an Amazon Bedrock session to checkpoint its state after each destination is added, preserving details about the customer's preferences.

If the conversation is interrupted or fails, the agent can resume the session later with context intact, including text and images. This allows the agent continue without requiring the customer to repeat information. Also, in the case of failure, you can investigate the session details to debug the cause.

## Workflow
<a name="sessions-workflow"></a>

The workflow to use the Session Management APIs is as follows. For information about using the BedrockSessionSaver library, see [Manage sessions with BedrockSessionSaver LangGraph library](sessions-opensource-library.md). 
+ **Create a session** – When your end user first starts the conversation, you create a session with the [CreateSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_CreateSession.html) API operation and specify an ID for the session. You use this ID when you store and retrieve the conversation state.
+ **Store conversations and context** – As your end users interact with your generative AI assistant, use the [CreateInvocation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_CreateInvocation.html) API to create a grouping of interactions within the session. For each invocation, use the [PutInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PutInvocationStep.html) API operations to store fine-grained state checkpoints, including text and images, for each interaction.
+ **Retrieve conversation history and context** – Use the [GetSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetSession.html), [ListInvocations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListInvocations.html), and [GetInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetInvocationStep.html) API operations to retrieve session metadata and interaction details.
+ **End the session** – When the session is complete, end the session with the [EndSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_EndSession.html) API operation. After you end a session, you can still access its content but you can’t add to it. To delete the session and it's content, you use the [DeleteSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_DeleteSession.html) API operation.

## Considerations
<a name="sessions-considerations"></a>

Before you create and manage sessions, note the following:
+ You can create and manage sessions with the Amazon Bedrock APIs and AWS SDKs. You can’t use the AWS Management Console to manage sessions.
+ For agent applications built on LangGraph, you can use the `BedrockSessionSaver` class from the `langchain-aws` library. This is a custom implementation of the LangGraph CheckpointSaver. For information about using the BedrockSessionSaver library, see [Manage sessions with BedrockSessionSaver LangGraph library](sessions-opensource-library.md). To view the code directly, see [langgraph-checkpoint-aws](https://github.com/langchain-ai/langchain-aws/tree/main/libs/langgraph-checkpoint-aws) in the [LangChain](https://github.com/langchain-ai) GitHub repository.
+ If you specify a customer managed AWS KMS key when you create a session, the user or role creating the session must have permission to use the key. For more information, [Session encryption](sessions-encryption.md).
+ The Session Management APIs have the following quotas:
  + Number of invocation steps in a session across all invocations – 1000
  + Maximum size of each invocation step – 50 MB
  + IdleSession Timeout – 1 hour
  + Retention period – Session data is automatically deleted after 30 days