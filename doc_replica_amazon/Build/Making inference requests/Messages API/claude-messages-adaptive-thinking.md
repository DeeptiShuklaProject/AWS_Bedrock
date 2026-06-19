

# Adaptive thinking
<a name="claude-messages-adaptive-thinking"></a>

Adaptive thinking is the recommended way to use [Extended thinking](claude-messages-extended-thinking.md) with Claude Opus 4.6. Instead of manually setting a thinking token budget, adaptive thinking lets Claude dynamically decide when and how much to think based on the complexity of each request. Adaptive thinking reliably drives better performance than extended thinking with a fixed `budget_tokens`, and we recommend moving to adaptive thinking to get the most intelligent responses from Claude Opus 4.6. No beta header is required.

The supported models are as follows:


| Model | Model ID | 
| --- | --- | 
| Claude Mythos 5 | `anthropic.claude-mythos-5` | 
| Claude Fable 5 | `anthropic.claude-fable-5` | 
| Claude Opus 4.7 | `anthropic.claude-opus-4-7` | 
| Claude Mythos Preview | `anthropic.claude-mythos-preview` | 
| Claude Opus 4.6 | `anthropic.claude-opus-4-6-v1` | 
| Claude Sonnet 4.6 | `anthropic.claude-sonnet-4-6` | 

**Note**  
Claude Mythos 5, Claude Fable 5, Claude Opus 4.7, and Claude Mythos Preview *only* support adaptive thinking. Manual extended thinking (`thinking.type: "enabled"` with `budget_tokens`) and disabled thinking (`thinking.type: "disabled"`) are not supported on these models and will return a 400 error. Use `thinking.type: "adaptive"` with `output_config.effort` to control thinking behavior.  
`thinking.type: "enabled"` and `budget_tokens` are deprecated on Claude Opus 4.6 and Claude Sonnet 4.6 and will be removed in a future model release. Use `thinking.type: "adaptive"` with the effort parameter instead.  
Older models (Claude Sonnet 4.5, Claude Opus 4.5, etc.) do not support adaptive thinking and require `thinking.type: "enabled"` with `budget_tokens`.

## How adaptive thinking works
<a name="claude-messages-adaptive-thinking-how-it-works"></a>

In adaptive mode, Claude evaluates the complexity of each request and decides whether and how much to think. At the default effort level (`high`), Claude will almost always think. At lower effort levels, Claude may skip thinking for simpler problems.

Adaptive thinking also automatically enables [Interleaved thinking (beta)](claude-messages-extended-thinking.md#claude-messages-extended-thinking-tool-use-interleaved). This means Claude can think between tool calls, making it especially effective for agentic workflows.

Set `thinking.type` to `"adaptive"` in your API request:

------
#### [ CLI ]

```
aws bedrock-runtime invoke-model \
--model-id "us.anthropic.claude-opus-4-6-v1" \
--body '{
"anthropic_version": "bedrock-2023-05-31",
"max_tokens": 16000,
"thinking": {
"type": "adaptive"
},
"messages": [
{
"role": "user",
"content": "Three players A, B, C play a game. Each has a jar with 100 balls numbered 1-100. Simultaneously, each draws one ball. A beats B if As number > Bs number (mod 100, treating 100 as 0 for comparison). Similarly for B vs C and C vs A. The overall winner is determined by majority of pairwise wins (ties broken randomly). Is there a mixed strategy Nash equilibrium where each player draws uniformly? If not, characterize the equilibrium."
}
]
}' \
--cli-binary-format raw-in-base64-out \
output.json && cat output.json | jq '.content[] | {type, thinking: .thinking[0:200], text}'
```

------
#### [ Python ]

```
import boto3
import json

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

response = bedrock_runtime.invoke_model(
    modelId="us.anthropic.claude-opus-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 16000,
        "thinking": {
            "type": "adaptive"
        },
        "messages": [{
            "role": "user",
            "content": "Explain why the sum of two even numbers is always even."
        }]
    })
)

response_body = json.loads(response["body"].read())

for block in response_body["content"]:
    if block["type"] == "thinking":
        print(f"\nThinking: {block['thinking']}")
    elif block["type"] == "text":
        print(f"\nResponse: {block['text']}")
```

------
#### [ TypeScript ]

```
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

async function main() {
    const client = new BedrockRuntimeClient({});

    const command = new InvokeModelCommand({
        modelId: "us.anthropic.claude-opus-4-6-v1",
        body: JSON.stringify({
            anthropic_version: "bedrock-2023-05-31",
            max_tokens: 16000,
            thinking: {
                type: "adaptive"
            },
            messages: [{
                role: "user",
                content: "Explain why the sum of two even numbers is always even."
            }]
        })
    });

    const response = await client.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));

    for (const block of responseBody.content) {
        if (block.type === "thinking") {
            console.log(`\nThinking: ${block.thinking}`);
        } else if (block.type === "text") {
            console.log(`\nResponse: ${block.text}`);
        }
    }
}

main().catch(console.error);
```

------

## Adaptive thinking with the effort parameter
<a name="claude-messages-adaptive-thinking-effort"></a>

You can combine adaptive thinking with the effort parameter to guide how much thinking Claude does. The effort level acts as soft guidance for Claude's thinking allocation:


| Effort level | Thinking behavior | 
| --- | --- | 
| max | Claude always thinks with no constraints on thinking depth. Claude Opus 4.6 only — requests using max on other models will return an error. | 
| high (default) | Claude always thinks. Provides deep reasoning on complex tasks. | 
| medium | Claude uses moderate thinking. May skip thinking for very simple queries. | 
| low | Claude minimizes thinking. Skips thinking for simple tasks where speed matters most. | 

**Important**  
The `effort` parameter must be placed inside a separate `output_config` object in your request body — not inside the `thinking` object. Placing `effort` inside `thinking` will result in a `ValidationException`.

The following example shows how to set the effort level when using the InvokeModel API:

```
{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 16000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "high"
    },
    "messages": [{
        "role": "user",
        "content": "Your prompt here"
    }]
}
```

## Using adaptive thinking with the Converse API
<a name="claude-messages-adaptive-thinking-converse"></a>

When using the [Converse API](conversation-inference.md), pass the `thinking` and `effort` parameters inside `additionalModelRequestFields`. The following example shows adaptive thinking with the default effort level:

```
import boto3, json

bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-2')

response = bedrock_runtime.converse(
    modelId="us.anthropic.claude-opus-4-6-v1",
    messages=[{
        "role": "user",
        "content": [{"text": "Explain why the sum of two even numbers is always even."}]
    }],
    additionalModelRequestFields={
        "thinking": {
            "type": "adaptive"
        }
    }
)

print(json.dumps(response["output"], indent=2, default=str))
```

To specify an effort level, add the `effort` field inside a separate `output_config` object in `additionalModelRequestFields`:

```
response = bedrock_runtime.converse(
    modelId="us.anthropic.claude-opus-4-6-v1",
    messages=[{
        "role": "user",
        "content": [{"text": "What is 2 + 2?"}]
    }],
    additionalModelRequestFields={
        "thinking": {
            "type": "adaptive"
        },
        "output_config": {
            "effort": "low"
        }
    }
)
```

## Prompt caching
<a name="claude-messages-adaptive-thinking-prompt-caching"></a>

Consecutive requests using `adaptive` thinking preserve prompt cache breakpoints. However, switching between `adaptive` and `enabled`/`disabled` thinking modes breaks cache breakpoints for messages. System prompts and tool definitions remain cached regardless of mode changes.

## Tuning thinking behavior
<a name="claude-messages-adaptive-thinking-tuning"></a>

If Claude is thinking more or less often than you'd like, you can add guidance to your system prompt:

```
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality — typically for problems
that require multi-step reasoning. When in doubt, respond directly.
```

**Warning**  
Steering Claude to think less often may reduce quality on tasks that benefit from reasoning. Measure the impact on your specific workloads before deploying prompt-based tuning to production. Consider testing with lower effort levels first.

## Connector text summarization (beta)
<a name="claude-messages-adaptive-thinking-connector-summarization"></a>

On Claude Fable 5, text that the model emits between tool calls (sometimes called "connector text" — for example, "Let me check that file next...") is summarized server-side and returned as a thinking block rather than a plain text content block. The thinking block uses the same shape as any other thinking block (empty text with a signature under the default `omitted` display).

**Customer impact:**
+ **Response shape:** Tool-use responses from Claude Fable 5 may contain additional thinking blocks where previous models emitted plain text between `tool_use` blocks. There is no new content block type. Final assistant answers (after all tool use is complete) are unaffected and remain plain text.
+ **Multi-turn handling:** Pass these thinking blocks back unchanged in multi-turn conversations — the same handling as protected thinking (signature validated on passback; silently stripped if sent to a different model).
+ **Scope:** Connector summarization applies only after a `tool_result` exists in the conversation. Narration before the first tool call in a fresh conversation remains plain text. Short text segments may pass through as plain text without summarization.

This feature is enabled server-side for Claude Fable 5. There is no customer opt-in or opt-out.