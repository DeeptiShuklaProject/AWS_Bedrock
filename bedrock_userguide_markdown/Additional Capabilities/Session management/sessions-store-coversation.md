

# Store conversation history and context in a session
<a name="sessions-store-coversation"></a>

After you create a session, use the [CreateInvocation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_CreateInvocation.html) API to create a grouping of interactions within the session. For each grouping, use the [PutInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PutInvocationStep.html) API operations to store state checkpoints, including text and images, for each interaction.

How you organize invocation steps within invocations depends on your use case. For example, if you have an agent that helps customers make travel reservations, your invocation and invocation steps might be as follows:
+ The invocation might serve as the grouping for the text from a conversation an agent has with a customer checking room availability at a specific hotel for different nights.
+ Each invocation step might be each message between the agent and the user, and each step the agent takes to retrieve the availability.

In your [PutInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PutInvocationStep.html) API, you can import images associated with the conversation.
+ You can include up to 20 images. Each image's size, height, and width must be no more than 3.75 MB, 8000 px, and 8000 px, respectively.
+ You can import the following types of images:
  + PNG
  + JPEG
  + GIF
  + WEBP

**Topics**
+ [CreateInvocation example](#session-create-invocation)
+ [PutInvocationSteps example](#session-put-invocation-step)

## CreateInvocation example
<a name="session-create-invocation"></a>

The following code example shows how to add an invocation to an active session with the AWS SDK for Python (Boto3). For the `sessionIdentifier`, you can specify either the session's sessionId or its Amazon Resource Name (ARN). For more information about the API, see [CreateInvocation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_CreateInvocation.html). 

```
def create_invocation(session_identifier):
try:
    invocationId = client.create_invocation(
        sessionIdentifier=session_identifier,
        description="User asking about weather in Seattle",
        invocationId="12345abc-1234-abcd-1234-abcdef123456"
    )["invocationId"]
    print("invocation created")
    return invocationId
except ClientError as e:
    print(f"Error: {e}")
```

## PutInvocationSteps example
<a name="session-put-invocation-step"></a>

The following code example shows how to add an invocation step to an active session with the AWS SDK for Python (Boto3). The code adds text and an image in from the working directory. For the `sessionIdentifier`, you can specify either the session's sessionId or its Amazon Resource Name (ARN). For the invocation identifier, specify the unique identifier (in UUID format) of the invocation to add the invocation step to. For more information about the API, see [PutInvocationStep](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_PutInvocationStep.html). 

```
def put_invocation_step(invocation_identifier, session_identifier):
with open('weather.png', 'rb') as image_file:
    weather_image = image_file.read()

try:
    client.put_invocation_step(
        sessionIdentifier=session_identifier,
        invocationIdentifier=invocation_identifier,
        invocationStepId="12345abc-1234-abcd-1234-abcdef123456",
        invocationStepTime="2023-08-08T12:00:00Z",
        payload={
            'contentBlocks': [
                {
                    'text': 'What\'s the weather in Seattle?',

                },
                {
                    'image': {
                        'format': 'png',
                        'source': {'bytes': weather_image}
                    }
                }

            ]
        }
    )
    print("invocation step created")
except ClientError as e:
    print(f"Error: {e}")
```