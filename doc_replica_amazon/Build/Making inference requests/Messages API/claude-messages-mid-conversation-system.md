

# Mid-conversation system messages
<a name="claude-messages-mid-conversation-system"></a>

You can append `{"role": "system", ...}` messages to the `messages` array. This adds or updates system instructions partway through a conversation without invalidating the cached prefix.

Previously, system instructions could only be supplied through the top-level `system` parameter. This makes it possible to update instructions without resetting prior context.

This is useful in agentic workflows where the model needs to adapt as a task progresses. Examples include introducing a new constraint mid-task, refreshing authoritative context, or changing tool guidance for later turns.

## Supported models
<a name="claude-messages-mid-conversation-system-supported-models"></a>

This feature is available on Claude Opus 4.8 only. No beta header is required. Requests that include `role: "system"` in `messages[]` on unsupported models return a `400 invalid_request_error`.

## Message fields
<a name="claude-messages-mid-conversation-system-fields"></a>


| **Field** | **Type** | **Description** | 
| --- | --- | --- | 
| role | String | Required. Must be system | 
| content | String or list of text blocks | Required. Use a plain string or content blocks, the same as a user or assistant message. | 
| cache\_control | Object | Optional. Same semantics as the top-level system parameter. | 

## Placement rules
<a name="claude-messages-mid-conversation-system-placement"></a>

A `{"role": "system"}` message in `messages` has the following placement constraints:
+ Cannot be the first entry in `messages`. Use the top-level `system` field for instructions that apply from the very start.
+ Must immediately follow a user message or an assistant message that ends in a server tool use.
+ Must either be the last entry in `messages` or be followed by an assistant turn.
+ Cannot be adjacent to another system message. Consecutive system messages are not allowed.

Requests that violate these placement rules return a `400 invalid_request_error`.

## Content rules
<a name="claude-messages-mid-conversation-system-content-rules"></a>

System-role message content supports text blocks only. Images, documents, tool blocks, and citations are not supported.

Set `content` to either a plain string or content blocks. The instruction applies from that point in the conversation onward. Use the top-level `system` field for instructions that should apply to the entire conversation, and use mid-conversation system messages for instructions that become relevant later.

## Prompt caching
<a name="claude-messages-mid-conversation-system-caching"></a>

Mid-conversation system messages are designed to work with prompt caching. Cache the stable prefix as usual by placing `cache_control` on the last block that remains unchanged across requests. Then append the system message after that breakpoint. Because the new instruction appears after the cached prefix, it does not change the prefix hash, and the cache can still hit.

Once a mid-conversation system message becomes part of the stable history, it can itself be read from cache on subsequent turns. Avoid editing or removing a previously sent mid-conversation system message, because changing earlier messages invalidates the cache from that point forward.

For more information about prompt caching, see [Prompt caching for faster model inference](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html).

## Response behavior
<a name="claude-messages-mid-conversation-system-response"></a>

The response shape is unchanged. System-role messages do not appear in the response content array. The model processes the system instructions but does not echo them back in its response.

## Code example
<a name="claude-messages-mid-conversation-system-example"></a>

The following Python example demonstrates how to use mid-conversation system prompts with Amazon Bedrock:

```
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="us.anthropic.claude-opus-4-8",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": "You are a helpful travel planning assistant.",
        "messages": [
            {"role": "user", "content": "Help me plan a week in Paris."},
            {"role": "assistant", "content": "I'd love to help! What kind of experience are you looking for?"},
            {"role": "user", "content": "I want to see the major sights. What should I do on day one?"},
            {"role": "system", "content": "The user has a budget of $150/day. Only suggest options that fit within this budget. Prioritize free attractions and affordable dining."}
        ]
    })
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])
```