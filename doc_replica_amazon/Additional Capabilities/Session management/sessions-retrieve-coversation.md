

# Retrieve conversation history and context from a session
<a name="sessions-retrieve-coversation"></a>

Use the [GetSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetSession.html), [ListInvocations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_ListInvocations.html), and [GetInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetInvocationStep.html) API operations to retrieve session details, details for the interaction state at different checkpoints, and summary information for all invocations.

The following example code shows how to get text and image data for a checkpoint with the AWS SDK for Python (Boto3) and the [GetInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GetInvocationStep.html) API operation.

```
def get_invocation_step(invocation_identifier, session_identifier, invocation_step_identifier):
try:
    response = client.get_invocation_step(
        sessionIdentifier=session_identifier,
        invocationIdentifier=invocation_identifier,
        invocationStepId=invocation_step_identifier
    )  ["invocationStep"]["payload"]["contentBlocks"]
    print(response)
except ClientError as e:
    print(f"Error: {e}")
```