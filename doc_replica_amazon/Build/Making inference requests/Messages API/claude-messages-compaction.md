

# Compaction
<a name="claude-messages-compaction"></a>

**Tip**  
Server-side compaction is recommended for managing context in long-running conversations and agentic workflows as it handles context management automatically with minimal integration work.

**Note**  
Compaction is currently in beta. Include the beta header `compact-2026-01-12` in your API requests to use this feature. Compaction is currently not supported by the Converse API, however it is supported with [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html).

Compaction extends the effective context length for long-running conversations and tasks by automatically summarizing older context when approaching the context window limit. This is ideal for:
+ Chat-based, multi-turn conversations where you want users to use one chat for a long period of time
+ Task-oriented prompts that require a lot of follow-up work (often tool use) that may exceed the 200K context window

Compaction is supported on the following models:


| Model | Model ID | 
| --- | --- | 
| Claude Sonnet 4.6 | `anthropic.claude-sonnet-4-6` | 
| Claude Opus 4.6 | `anthropic.claude-opus-4-6-v1` | 

**Note**  
The top-level `input_tokens` and `output_tokens` in the `usage` field do not include compaction iteration usage, and reflect the sum of all non-compaction iterations. To calculate the total tokens consumed and billed for a request, sum across all entries in the `usage.iterations` array.  
If you previously relied on `usage.input_tokens` and `usage.output_tokens` for cost tracking or auditing, you will need to update your tracking logic to aggregate across `usage.iterations` when compaction is enabled. The `iterations` array is only present when a new compaction is triggered during the request. Re-applying a previous `compaction` block incurs no additional compaction cost, and the top-level usage fields remain accurate in that case.

## How compaction works
<a name="claude-messages-compaction-how-it-works"></a>

When compaction is enabled, Claude automatically summarizes your conversation when it approaches the configured token threshold. The API:

1. Detects when input tokens exceed your specified trigger threshold.

1. Generates a summary of the current conversation.

1. Creates a `compaction` block containing the summary.

1. Continues the response with the compacted context.

On subsequent requests, append the response to your messages. The API automatically drops all message blocks before the `compaction` block, continuing the conversation from the summary.

## Basic usage
<a name="claude-messages-compaction-basic-usage"></a>

Enable compaction by adding the `compact_20260112` strategy to `context_management.edits` in your Messages API request.

------
#### [ CLI ]

```
aws bedrock-runtime invoke-model \
    --model-id "us.anthropic.claude-opus-4-6-v1" \
    --body '{
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["compact-2026-01-12"],
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Help me build a website"
            }
        ],
        "context_management": {
            "edits": [
                {
                    "type": "compact_20260112"
                }
            ]
        }
    }' \
    --cli-binary-format raw-in-base64-out \
    /tmp/response.json

echo "Response:"
cat /tmp/response.json | jq '.content[] | {type, text: .text[0:500]}'
```

------
#### [ Python ]

```
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

messages = [{"role": "user", "content": "Help me build a website"}]

response = bedrock_runtime.invoke_model(
    modelId="us.anthropic.claude-opus-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["compact-2026-01-12"],
        "max_tokens": 4096,
        "messages": messages,
        "context_management": {
            "edits": [
                {
                    "type": "compact_20260112"
                }
            ]
        }
    })
)

response_body = json.loads(response["body"].read())

# Append the response (including any compaction block) to continue the conversation
messages.append({"role": "assistant", "content": response_body["content"]})

for block in response_body["content"]:
    if block.get("type") == "compaction":
        print(f"[COMPACTION]: {block['content'][:200]}...")
    elif block.get("type") == "text":
        print(f"[RESPONSE]: {block['text']}")
```

------
#### [ TypeScript ]

```
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

async function main() {
    const client = new BedrockRuntimeClient({});

    const messages: Array<{role: string, content: string | object[]}> = [
        { role: "user", content: "Help me build a website" }
    ];

    const command = new InvokeModelCommand({
        modelId: "us.anthropic.claude-opus-4-6-v1",
        body: JSON.stringify({
            anthropic_version: "bedrock-2023-05-31",
            anthropic_beta: ["compact-2026-01-12"],
            max_tokens: 4096,
            messages,
            context_management: {
                edits: [
                    {
                        type: "compact_20260112"
                    }
                ]
            }
        })
    });

    const response = await client.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));

    // Append response to continue conversation
    messages.push({ role: "assistant", content: responseBody.content });

    for (const block of responseBody.content) {
        if (block.type === "compaction") {
            console.log(`[COMPACTION]: ${block.content.substring(0, 200)}...`);
        } else if (block.type === "text") {
            console.log(`[RESPONSE]: ${block.text}`);
        }
    }
}

main().catch(console.error);
```

------

## Parameters
<a name="claude-messages-compaction-parameters"></a>


| Parameter | Type | Default | Description | 
| --- | --- | --- | --- | 
| type | string | Required | Must be "compact\_20260112" | 
| trigger | object | 150,000 tokens | When to trigger compaction. Must be at least 50,000 tokens. | 
| pause\_after\_compaction | boolean | false | Whether to pause after generating the compaction summary | 
| instructions | string | null | Custom summarization prompt. Completely replaces the default prompt when provided. | 

## Trigger configuration
<a name="claude-messages-compaction-trigger"></a>

Configure when compaction triggers using the `trigger` parameter:

```
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

response = bedrock_runtime.invoke_model(
    modelId="us.anthropic.claude-opus-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["compact-2026-01-12"],
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Help me build a website"}],
        "context_management": {
            "edits": [
                {
                    "type": "compact_20260112",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 100000
                    }
                }
            ]
        }
    })
)

response_body = json.loads(response["body"].read())
print(response_body["content"][-1]["text"])
```

## Custom summarization instructions
<a name="claude-messages-compaction-custom-instructions"></a>

By default, compaction uses the following summarization prompt:

```
You have written a partial transcript for the initial task above. Please write a summary of the transcript. The purpose of this summary is to provide continuity so you can continue to make progress towards solving the task in a future context, where the raw history above may not be accessible and will be replaced with this summary. Write down anything that would be helpful, including the state, next steps, learnings etc. You must wrap your summary in a <summary></summary> block.
```

You can provide custom instructions via the `instructions` parameter to replace this prompt entirely. Custom instructions don't supplement the default; they completely replace it:

```
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

response = bedrock_runtime.invoke_model(
    modelId="us.anthropic.claude-opus-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["compact-2026-01-12"],
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Help me build a website"}],
        "context_management": {
            "edits": [
                {
                    "type": "compact_20260112",
                    "instructions": "Focus on preserving code snippets, variable names, and technical decisions."
                }
            ]
        }
    })
)

response_body = json.loads(response["body"].read())
print(response_body["content"][-1]["text"])
```

## Pausing after compaction
<a name="claude-messages-compaction-pause"></a>

Use `pause_after_compaction` to pause the API after generating the compaction summary. This allows you to add additional content blocks (such as preserving recent messages or specific instruction-oriented messages) before the API continues with the response.

When enabled, the API returns a message with the `compaction` stop reason after generating the compaction block:

```
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

messages = [{"role": "user", "content": "Help me build a website"}]

response = bedrock_runtime.invoke_model(
    modelId="us.anthropic.claude-opus-4-6-v1",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["compact-2026-01-12"],
        "max_tokens": 4096,
        "messages": messages,
        "context_management": {
            "edits": [
                {
                    "type": "compact_20260112",
                    "pause_after_compaction": True
                }
            ]
        }
    })
)

response_body = json.loads(response["body"].read())

# Check if compaction triggered a pause
if response_body.get("stop_reason") == "compaction":
    # Response contains only the compaction block
    messages.append({"role": "assistant", "content": response_body["content"]})

    # Continue the request
    response = bedrock_runtime.invoke_model(
        modelId="us.anthropic.claude-opus-4-6-v1",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "anthropic_beta": ["compact-2026-01-12"],
            "max_tokens": 4096,
            "messages": messages,
            "context_management": {
                "edits": [{"type": "compact_20260112"}]
            }
        })
    )
    response_body = json.loads(response["body"].read())

print(response_body["content"][-1]["text"])
```

## Working with compaction blocks
<a name="claude-messages-compaction-blocks"></a>

When compaction is triggered, the API returns a `compaction` block at the start of the assistant response.

A long-running conversation may result in multiple compactions. The last compaction block reflects the final state of the prompt, replacing content before it with the generated summary.

```
{
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation: The user requested help building a web scraper..."
    },
    {
      "type": "text",
      "text": "Based on our conversation so far..."
    }
  ]
}
```

## Streaming
<a name="claude-messages-compaction-streaming"></a>

When streaming responses with compaction enabled, you'll receive a `content_block_start` event when compaction begins. The compaction block streams differently from text blocks. You'll receive a `content_block_start` event, followed by a single `content_block_delta` with the complete summary content (no intermediate streaming), and then a `content_block_stop` event.

## Prompt caching
<a name="claude-messages-compaction-prompt-caching"></a>

You may add a `cache_control` breakpoint on compaction blocks, which caches the full system prompt along with the summarized content. The original compacted content is ignored. Note that when compaction is triggered, it can result in a cache miss on the subsequent request.

```
{
    "role": "assistant",
    "content": [
        {
            "type": "compaction",
            "content": "[summary text]",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "Based on our conversation..."
        }
    ]
}
```

## Understanding usage
<a name="claude-messages-compaction-usage"></a>

Compaction requires an additional sampling step, which contributes to rate limits and billing. The API returns detailed usage information in the response:

```
{
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 1234,
    "iterations": [
      {
        "type": "compaction",
        "input_tokens": 180000,
        "output_tokens": 3500
      },
      {
        "type": "message",
        "input_tokens": 23000,
        "output_tokens": 1000
      }
    ]
  }
}
```

The `iterations` array shows usage for each sampling iteration. When compaction occurs, you'll see a `compaction` iteration followed by the main `message` iteration. The final iteration's token counts reflect the effective context size after compaction.