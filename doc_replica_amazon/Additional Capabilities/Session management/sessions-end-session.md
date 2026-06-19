

# End a session when the user ends the conversation
<a name="sessions-end-session"></a>

When the conversations are finished and any agent tasks are completed, end the session with the [EndSession](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_EndSession.html) API operation. After you end a session, you can still access its content but you can’t add to it or restart it. 

The following example code shows how to end a session with the AWS SDK for Python (Boto3).

```
def end_session(session_identifier):
try:
    client.end_session(
        sessionIdentifier=session_identifier
    )
    print("session ended")
except ClientError as e:
    print(f"Error: {e}")
```