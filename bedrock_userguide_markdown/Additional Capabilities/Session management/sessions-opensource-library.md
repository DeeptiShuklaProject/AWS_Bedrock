

# Store and retrieve conversation history and context with the BedrockSessionSaver LangGraph library
<a name="sessions-opensource-library"></a>

Instead of directly using the Amazon Bedrock session management APIs, you can store and retrieve conversation history and context in LangGraph with the `BedrockSessionSaver` library. This is a custom implementation of the LangGraph CheckpointSaver. It uses the Amazon Bedrock APIs with a LangGraph-based interface. For more information, see [langgraph-checkpoint-aws](https://github.com/langchain-ai/langchain-aws/tree/main/libs/langgraph-checkpoint-aws) in the [LangChain](https://github.com/langchain-ai) GitHub repository.

The following code sample shows how to use the BedrockSessionSaver LangGraph library to track state as a user interacts with Claude. To use this code sample:
+ Install the required dependencies:
  + boto3
  + langgraph
  + langgraph-checkpoint-aws
  + langchain-core
+ Make sure you have access to the Claude 3.5 Sonnet v2 model in your account. Or you can modify the code to use a different model.
+ Replace `REGION` with your region:
  + This Region for your runtime client and the BedrockSessionSaver must match. 
  + It must support Claude 3.5 Sonnet v2 (or the model you are using).

```
import boto3
from typing import Dict, TypedDict, Annotated, Sequence, Union
from langgraph.graph import StateGraph, END
from langgraph_checkpoint_aws.saver import BedrockSessionSaver
from langchain_core.messages import HumanMessage, AIMessage
import json


# Define state structure
class State(TypedDict):
    messages: Sequence[Union[HumanMessage, AIMessage]]
    current_question: str


# Function to get response from Claude
def get_response(messages):
    bedrock = boto3.client('bedrock-runtime', region_name="us-west-2")
    prompt = "\n".join([f"{'Human' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
                        for m in messages])

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "temperature": 0.7
        })
    )

    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']


# Node function to process user question
def process_question(state: State) -> Dict:
    messages = list(state["messages"])
    messages.append(HumanMessage(content=state["current_question"]))

    # Get response from Claude
    response = get_response(messages)
    messages.append(AIMessage(content=response))

    # Print assistant's response
    print("\nAssistant:", response)

    # Get next user input
    next_question = input("\nYou: ").strip()

    return {
        "messages": messages,
        "current_question": next_question
    }


# Node function to check if conversation should continue
def should_continue(state: State) -> bool:
    # Check if the last message was from the user and contains 'quit'
    if state["current_question"].lower() == 'quit':
        return False
    return True


# Create the graph
def create_graph(session_saver):
    # Initialize state graph
    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("process_question", process_question)

    # Add conditional edges
    workflow.add_conditional_edges(
        "process_question",
        should_continue,
        {
            True: "process_question",
            False: END
        }
    )

    # Set entry point
    workflow.set_entry_point("process_question")

    return workflow.compile(session_saver)


def main():
    # Create a runtime client
    agent_run_time_client = boto3.client("bedrock-agent-runtime",
                                         region_name="{{REGION}}")
            
    # Initialize Bedrock session saver. The Region must match the Region used for the agent_run_time_client.
    session_saver = BedrockSessionSaver(region_name="{{REGION}}")

    # Create graph
    graph = create_graph(session_saver)

    # Create session
    session_id = agent_run_time_client.create_session()["sessionId"]
    print("Session started. Type 'quit' to end.")

    # Configure graph
    config = {"configurable": {"thread_id": session_id}}

    # Initial state
    state = {
        "messages": [],
        "current_question": "Hello! How can I help you today? (Type 'quit' to end)"
    }

    # Print initial greeting
    print(f"\nAssistant: {state['current_question']}")

    state["current_question"] = input("\nYou: ").strip()

    # Process the question through the graph
    graph.invoke(state, config)
    print("\nSession contents:")
    for i in graph.get_state_history(config, limit=3):
        print(i)


if __name__ == "__main__":
    main()
```