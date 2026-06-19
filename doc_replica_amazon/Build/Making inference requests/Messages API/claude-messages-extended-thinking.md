

# Extended thinking
<a name="claude-messages-extended-thinking"></a>

**See also**  
[Thinking encryption](claude-messages-thinking-encryption.md) – encrypted-thinking and redaction behavior specific to Claude 3.7 Sonnet.
[Differences in thinking across model versions](claude-messages-thinking-differences.md) – differences in how Claude 3.7 Sonnet and Claude 4 models return thinking output.

Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer. Whenever you enable Claude’s thinking mode, you will need to set a budget for the maximum number of tokens that Claude can use for its internal reasoning process.

The supported models are as follows:


| Model | Model ID | 
| --- | --- | 
| Claude Opus 4.5 | `anthropic.claude-opus-4-5-20251101-v1:0` | 
| Claude Opus 4 | `anthropic.claude-opus-4-20250514-v1:0` | 
| Claude Sonnet 4 | `anthropic.claude-sonnet-4-20250514-v1:0` | 
| Claude Sonnet 4.5 | `anthropic.claude-sonnet-4-5-20250929-v1:0` | 
| Claude Sonnet 4.6 | `anthropic.claude-sonnet-4-6` | 
| Claude Opus 4.6 | `anthropic.claude-opus-4-6-v1` | 
| Claude Haiku 4.5 | `anthropic.claude-haiku-4-5-20251001-v1:0` | 
| Claude 3.7 Sonnet | `anthropic.claude-3-7-sonnet-20250219-v1:0` | 

**Note**  
Claude Mythos 5 and Claude Fable 5 do not support extended thinking. Requests with `thinking.type: "enabled"` or `thinking.type: "disabled"` will return a 400 error. These models use adaptive thinking exclusively. See [Adaptive thinking](claude-messages-adaptive-thinking.md) for details.  
**Migration from extended thinking:**  
Replace `{"type": "enabled", "budget_tokens": N}` with `{"type": "adaptive"}` and use `output_config.effort` to control thinking depth.
Remove `{"type": "disabled"}` — omitting the thinking parameter entirely gives you adaptive thinking by default.

**Note**  
API behavior differs between Claude 3.7 and Claude 4 models. For more information, see [Differences in thinking across model versions](claude-messages-thinking-differences.md).

**Topics**
+ [Best practices and considerations for extended thinking](#claude-messages-extended-thinking-bps)
+ [How extended thinking works](#claude-messages-how-extended-thinking-works)
+ [How to use extended thinking](#claude-messages-use-extended-thinking)
+ [Extended thinking with tool use](#claude-messages-extended-thinking-tool-use)
+ [Thinking block clearing (beta)](#claude-messages-thinking-block-clearing)
+ [Extended thinking with prompt caching](#claude-messages-extended-thinking-prompt-caching)
+ [Understanding thinking block caching behavior](#claude-messages-extended-thinking-caching-behavior)
+ [Max tokens and context window size with extended thinking](#claude-messages-extended-thinking-max-tokens)
+ [Extended thinking token cost considerations](#claude-messages-extended-thinking-cost)

## Best practices and considerations for extended thinking
<a name="claude-messages-extended-thinking-bps"></a>

Usage guidelines
+ **Task selection**: Use extended thinking for particularly complex tasks that benefit from step-by-step reasoning like math, coding, and analysis.
+ **Context handling**: You do not need to remove previous thinking blocks yourself. The Anthropic API automatically ignores thinking blocks from previous turns and they are not included when calculating context usage.
+ **Prompt engineering**: Review Anthropic's [extended thinking prompting tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips) if you want to maximize Claude's thinking capabilities.

Performance considerations
+ **Response times**: Be prepared for potentially longer response times due to the additional processing required for the reasoning process. Factor in that generating thinking blocks might increase the overall response time.
+ **Streaming requirements**: Streaming is required when `max_tokens` is greater than 21,333. When streaming, be prepared to handle both `thinking` and `text` content blocks as they arrive.

Feature compatibility
+ Thinking isn't compatible with `temperature`, `top_p`, or `top_k` modifications or [forced tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#forcing-tool-use).
+ You cannot pre-fill responses when thinking is enabled.
+ Changes to the thinking budget invalidate cached prompt prefixes that include messages. However, cached system prompts and tool definitions will continue to work when thinking parameters change.

Working with thinking budgets
+ **Budget optimizations**: The minimum budget is 1,024 tokens. Anthropic suggests starting at the minimum and increasing the thinking budget incrementally to find the optimal range for your use case. Larger token counts might allow for more comprehensive and nuanced reasoning, but there can also be diminishing returns depending on the task. The thinking budget is a target rather than a strict limit - actual token usage may vary based on the task.
+ **Minimum and optimal settings**: The minimum budget is 1,024 tokens. We suggest starting at the minimum and increasing the thinking budget incrementally to find the optimal range for Claude to perform well for your use case. Higher token counts might allow you to achieve more comprehensive and nuanced reasoning, but there might also be diminishing returns depending on the task. The thinking budget is a target rather than a strict limit - actual token usage can vary based on the task.
+ **Experimentation**: The model might perform differently at different max thinking budget settings. Increasing the max thinking budget can make the model think better or harder, at the tradeoff of increased latency. For critical tasks, consider testing different budget settings to find the optimal balance between quality and performance.
+ **Large budgets**: For thinking budgets above 32K, we recommend using batch processing to avoid networking issues. Requests pushing the model to think above 32K tokens causes long running requests that might result in system timeouts and open connection limits. Please note that `max_tokens` limits vary among Claude models. For more information, see [Max tokens and context window size with extended thinking](#claude-messages-extended-thinking-max-tokens).
+ **Token usage tracking**: Monitor thinking token usage to optimize costs and performance.

## How extended thinking works
<a name="claude-messages-how-extended-thinking-works"></a>

When extended thinking is turned on, Claude creates `thinking` content blocks where it outputs its internal reasoning. Claude incorporates insights from this reasoning before crafting a final response. The API response will include `thinking` content blocks, followed by `text` content blocks.

Here’s an example of the default response format:

```
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "text", 
      "text": "Based on my analysis..."
    }
  ]
}
```

For more information about the response format of extended thinking, see Anthropic’s Messages API [Request and Response](model-parameters-anthropic-claude-messages-request-response.md).

## How to use extended thinking
<a name="claude-messages-use-extended-thinking"></a>

To turn on extended thinking, add a `thinking` object, with the `thinking` parameter set to enabled and the `budget_tokens` set to a specified token budget for extended thinking.

The `budget_tokens` parameter determines the maximum number of tokens Claude is allowed to use for its internal reasoning process. In Claude 4 models, this limit applies to full thinking tokens, and not to the summarized output. Larger budgets can improve response quality by enabling more thorough analysis for complex problems, although Claude might not use the entire budget allocated, especially at ranges above 32K.

The value of `budget_tokens` must be set to a value less than `max_tokens`. However, when using [Interleaved thinking (beta)](#claude-messages-extended-thinking-tool-use-interleaved) with tools, you can exceed this limit because the token limit becomes your entire context window (200K tokens).

### Summarized thinking
<a name="claude-messages-use-extended-thinking-summarized"></a>

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude’s full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse.

Here are some important considerations for summarized thinking:
+ You’re charged for the full thinking tokens generated by the original request, not the summary tokens.
+ The billed output token count will not match the count of tokens you see in the response.
+ The prompt provided to the summarizer model is subject to change.
+ The first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes.

**Note**  
Claude 3.7 Sonnet still returns the full thinking output.

### Streaming thinking
<a name="claude-messages-use-extended-thinking-streaming"></a>

You can stream extended thinking responses using server-sent events (SSE). When streaming is enabled for extended thinking, you receive thinking content via `thinking_delta` events. Streamed events are not guaranteed to return at a constant rate. There can be delays between streaming events. For more documentation on streaming via the Messages API, see [Streaming messages](https://docs.anthropic.com/en/docs/build-with-claude/streaming).

Here’s how to handle streaming with thinking using **InvokeModelWithResponseStream**:

```
{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 10000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 4000
    },
    "messages": [
        {
            "role": "user",
            "content": "What is 27 * 453?"
        }
    ]
}
```

Response:

```
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-3-7-sonnet-20250219", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "Let me solve this step by step:\n\n1. First break down 27 * 453"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n2. 453 = 400 + 50 + 3"}}

// Additional thinking deltas...

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "27 * 453 = 12,231"}}

// Additional text deltas...

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

**About streaming behavior with thinking**  
When using streaming with thinking enabled, you might notice that text sometimes arrives in larger chunks alternating with smaller, token-by-token delivery. This is expected behavior, especially for thinking content. The streaming system needs to process content in batches for optimal performance, which can result in this delivery pattern.

## Extended thinking with tool use
<a name="claude-messages-extended-thinking-tool-use"></a>

Extended thinking can be used alongside [Anthropic Claude tool use](model-parameters-anthropic-claude-messages-tool-use.md) allowing Claude to reason through tool selection and results processing. When using extended thinking with tool use, be aware of the following limitations:
+ **Tool choice limitation**: Tool use with thinking only supports `tool_choice: auto` (default) or `tool_choice: none`. It does not support forced tool use (`any` or specifying a specific tool).
+ **Preserving thinking blocks**: During tool use, you must pass thinking blocks back to the API for the last assistant message. Include the complete unmodified block back to the API to maintain reasoning continuity.

Here is how context window management works with tools:

```
{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 10000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 4000
    },
  "tools": [
  {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string"
        }
      },
      "required": [
        "location"
      ]
    }
  }
],
    "messages": [
        {
            "role": "user",
            "content": "What's the weather in Paris?"
        }
    ]
}
```

The first response is the following:

```
{
    "content": [
        {
            "type": "thinking",
            "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
            "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5TILnCrrUXoKiiNBZW9P+nr8XSj1zuZzAl4egiCCpQNvfyUuFFJP5CncdYZEQPPmLxYsNrcs...."
        },
        {
            "type": "text",
            "text": "I can help you get the current weather information for Paris. Let me check that for you"
        },
        {
            "type": "tool_use",
            "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
            "name": "get_weather",
            "input": {
                "location": "Paris"
            }
        }
    ]
}
```

Continuing the conversation with tool use will generate another response. Notice that the `thinking_block` is passed in as well as the `tool_use_block`. If this is not passed in, an error occurs.

```
{
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 10000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 4000
  },
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather for a location",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string"
          }
        },
        "required": [
          "location"
        ]
      }
    }
  ],
      "messages": [
        {
          "role": "user",
          "content": "What's the weather in Paris?"
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "thinking",
              "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`…",
              "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5TILnCrrUXoKiiNBZW9P+nr8XSj1zuZzAl4egiCCpQNvfyUuFFJP5CncdYZEQPPmLxY",
            },
            {
              "type": "tool_use",
              "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
              "name": "get_weather",
              "input": {
                "location": "Paris"
              }
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "tool_result",
              "tool_use_id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
              "content": "Current temperature: 88°F"
            }
          ]
        }
      ]
    }
```

The API response will now only include text

```
{
  "content": [
    {
      "type": "text",
      "text": "Currently in Paris, the temperature is 88°F (31°C)"
    }
  ]
}
```

### Preserve thinking blocks
<a name="claude-messages-extended-thinking-tool-use-thinking-blocks"></a>

During tool use, you must pass thinking blocks back to the API, and you must include the complete unmodified block back to the API. This is critical for maintaining the model’s reasoning flow and conversation integrity.

**Tip**  
While you can omit `thinking` blocks from prior `assistant` role turns, we suggest always passing back all thinking blocks to the API for any multi-turn conversation. The API will do the following:  
Automatically filter the provided thinking blocks
Use the relevant thinking blocks necessary to preserve the model’s reasoning
Only bill for the input tokens for the blocks shown to Claude

When Claude invokes tools, it is pausing its construction of a response to await external information. When tool results are returned, Claude will continue building that existing response. This necessitates preserving thinking blocks during tool use, for the following reasons:
+ **Reasoning continuity**: The thinking blocks capture Claude’s step-by-step reasoning that led to tool requests. When you post tool results, including the original thinking ensures Claude can continue its reasoning from where it left oﬀ.
+ **Context maintenance**: While tool results appear as user messages in the API structure, they’re part of a continuous reasoning flow. Preserving thinking blocks maintains this conceptual flow across multiple API calls.

**Important**  
When providing thinking blocks, the entire sequence of consecutive thinking blocks must match the outputs generated by the model during the original request; you cannot rearrange or modify the sequence of these blocks.

### Interleaved thinking (beta)
<a name="claude-messages-extended-thinking-tool-use-interleaved"></a>

**Warning**  
Interleaved thinking is made available to you as a ‘Beta Service’ as defined in the AWS Service Terms. It is subject to your Agreement with AWS and the AWS Service Terms, and the applicable model EULA.

Claude 4 models support interleaved thinking, a feature that enables Claude to think between tool calls and run more sophisticated reasoning after receiving tool results. This allows for more complex agentic interactions where Claude can do the following:
+ Reason about the results of a tool call before deciding what to do next
+ Chain multiple tool calls with reasoning steps in between
+ Make more nuanced decisions based on intermediate results

To enable interleaved thinking, add the beta header `interleaved-thinking-2025-05-14` to your API request.

**Note**  
With interleaved thinking, the `budget_tokens` can exceed the `max_tokens` parameter because it represents the total budget across all thinking blocks within one assistant turn.

## Thinking block clearing (beta)
<a name="claude-messages-thinking-block-clearing"></a>

**Warning**  
Thinking block clearing is made available as a "Beta Service" as defined in the AWS Service Terms.

**Note**  
This feature is currently supported on Claude Sonnet 4/4.5, Claude Haiku 4.5, and Claude Opus 4/4.1/4.5.

Thinking block clearing is an Anthropic Claude model capability (in beta). With this feature, Claude can automatically clear older thinking blocks from previous turns. To use Thinking block clearing, you need to add `context-management-2025-06-27` to the list of beta headers on the anthropic\_beta request parameter. You will also need to specify the use of `clear_thinking_20251015` and choose from the following configuration options.

These are the available controls for the `clear_thinking_20251015` context management strategy. All are optional or have defaults:


| **Configuration Option** | **Description** | 
| --- | --- | 
| `keep`<br />default: 1 thinking turn | Defines how many recent assistant turns with thinking blocks to preserve. Use `{"type": "thinking_turns", "value": N}` where N must be > 0 to keep the last N turns, or `{"type": "all"}` to keep all thinking blocks. | 

------
#### [ Request ]

```
{
      "anthropic_version": "bedrock-2023-05-31",
      "max_tokens": 10000,
      "anthropic_beta": [
        "context-management-2025-06-27"
      ],
      "thinking": {
        "type": "enabled",
        "budget_tokens": 4000
      },
      "tools": [
        {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string"
              }
            },
            "required": [
              "location"
            ]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "What's the weather in Paris?"
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "thinking",
              "thinking": "The user is asking for the weather in Paris. I have access to a get_weather function that takes a location as a parameter. I have all the information I need to make this call - the location is \"Paris\".\n\nLet me call the get_weather function with \"Paris\" as the location.",
              "signature": "ErgDCkgIChABGAIqQC/Ccv8GC+5VfcMEiq78XmpU2Ef2cT+96pHKMedKcRNuPz1x0kFlo5HBpW0r1NcQFVQUPuj6PDmP7jdHY7GsrUwSDKNBMogjaM7wYkwfPhoMswjlmfF09JLjZfFlIjB03NkghGOxLbr3VCQHIY0lMaV9UBvt7ZwTpJKzlz+mulBysfvAmDfcnvdJ/6CZre4qnQJsTZaiXdEgASwPIc5jOExBguerrtYSWVC/oPjSi7KZM8PfhP/SPXupyLi8hwYxeqomqkeG7AQhD+3487ecerZJcpJSOSsf0I1OaMpmQEE/b7ehnvTV/A4nLhxIjP4msyIBW+dVwHNFRFlpJLBHUJvN99b4run6YmqBSf4y9TyNMfOr+FtfxedGE0HfJMBd4FHXmUFyW5y91jAHMWqwNxDgacaKkFCAMaqce5rm0ShOxXn1uwDUAS3jeRP26Pynihq8fw5DQwlqOpo7vvXtqb5jjiCmqfOe6un5xeIdhhbzWddhEk1Vmtg7I817pM4MZjVaeQN02drPs8QgDxihnP6ZooGhd6FCBP2X3Ymdlj5zMlbVHxmSkA4wcNtg4IAYAQ=="
            },
            {
              "type": "tool_use",
              "id": "toolu_bdrk_01U7emCvL5v5z5GT7PDr2vzc",
              "name": "get_weather",
              "input": {
                "location": "Paris"
              }
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "tool_result",
              "tool_use_id": "toolu_bdrk_01U7emCvL5v5z5GT7PDr2vzc",
              "content": "Current temperature: 88°F"
            }
          ]
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "clear_thinking_20251015",
            "keep": {
              "type": "thinking_turns",
              "value": 1
            }
          }
        ]
      }
    }
```

------
#### [ Response ]

```
{
      "model": "claude-haiku-4-5-20251001",
      "id": "msg_bdrk_01KyTbyFbdG2kzPwWMJY1kum",
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The current weather in Paris is **88°F** (approximately 31°C). It's quite warm! If you need more detailed information like humidity, wind conditions, or a forecast, please let me know."
        }
      ],
      "stop_reason": "end_turn",
      "stop_sequence": null,
      "usage": {
        "input_tokens": 736,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation": {
          "ephemeral_5m_input_tokens": 0,
          "ephemeral_1h_input_tokens": 0
        },
        "output_tokens": 47
      },
      "context_management": {
        "applied_edits": [...]
      }
    }
```

------

## Extended thinking with prompt caching
<a name="claude-messages-extended-thinking-prompt-caching"></a>

[Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) with thinking has several important considerations:

**Thinking block context removal**
+ Thinking blocks from previous turns are removed from context, which can affect cache breakpoints.
+ When continuing conversations with tool use, thinking blocks are cached and count as input tokens when read from cache. This creates a tradeoff where thinking blocks don't consume context window space visually, but they will still count towards your input token usage when cached.
+ If thinking becomes disabled, requests will fail if you pass thinking content in the current tool use turn. In other contexts, thinking content passed to the API is simply ignored.

**Cache invalidation patterns**
+ Changes to thinking parameters (such as enabling, disabling, or altering the budget allocation) invalidate message cache breakpoints.
+ [Interleaved thinking (beta)](#claude-messages-extended-thinking-tool-use-interleaved) amplifies cache invalidation, as thinking blocks can occur between multiple tool calls.
+ System prompts and tools remain cached despite thinking parameter changes or block removal.

**Note**  
While thinking blocks are removed for caching and context calculations, they must be preserved when continuing conversations with tool use, especially with interleaved thinking.

## Understanding thinking block caching behavior
<a name="claude-messages-extended-thinking-caching-behavior"></a>

When using extended thinking with tool use, thinking blocks exhibit specific caching behavior that affects token counting. The following sequence demonstrates how this works.

1. Caching only occurs when you make a subsequent request that includes tool results.

1. When the subsequent request is made, the previous conversation history (including thinking blocks) can be cached.

1. These cached thinking blocks count as input tokens in your usage metrics when they are read from the cache.

1. When a non-tool-result user block is included, all previous thinking blocks are ignored and stripped from context.

Here is a detailed example flow:

Request 1:

```
User: "What's the weather in Paris?"
```

Response 1:

```
[thinking_block 1] + [tool_use block 1]
```

Request 2:

```
User: "What's the weather in Paris?",
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
```

Response 2:

```
[thinking_block 2] + [text block 2]
```

Request 2 writes a cache of the request content (not the response). The cache includes the original user message, the first thinking block, tool use block, and the tool result.

Request 3:

```
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```

Because a non-tool-result user block was included, all previous thinking blocks are ignored. This request will be processed the same as the following request:

Request 3 Alternate:

```
User: ["What's the weather in Paris?"]
Assistant: [tool_use block 1]
User: [tool_result_1, cache=True]
Assistant: [text block 2]
User: [Text response, cache=True]
```

This behavior is consistent whether using regular thinking or interleaved thinking.

## Max tokens and context window size with extended thinking
<a name="claude-messages-extended-thinking-max-tokens"></a>

In older Claude models (before Claude 3.7 Sonnet), if the sum of prompt tokens and max\_tokens exceeded the model’s context window, the system would automatically adjust max\_tokens to fit within the context limit. This meant you could set a large max\_tokens value and the system would silently reduce it as needed. With Claude 3.7 and 4 models, `max_tokens` (which includes your thinking budget when thinking is enabled) is enforced as a strict limit. The system now returns a validation error if prompt tokens \+ max\_tokens exceeds the context window size.

### The context window with extended thinking
<a name="claude-messages-extended-thinking-max-tokens-calculate"></a>

When calculating context window usage with thinking enabled, there are some considerations to be aware of:
+ Thinking blocks from previous turns are removed and not counted towards your context window.
+ Current turn thinking counts towards your `max_tokens` limit for that turn.

The eﬀective context window is calculated as: context window = (current input tokens - previous thinking tokens) \+ (thinking tokens \+ encrypted thinking tokens \+ text output tokens).

### Managing tokens with extended thinking and tool use
<a name="claude-messages-extended-thinking-max-tokens-manage-tool"></a>

When using extended thinking with tool use, thinking blocks must be explicitly preserved and returned with the tool results. The effective context window calculation for extended thinking with tool use becomes the following:

`context window = (current input tokens + previous thinking tokens + tool use tokens) + (thinking tokens + encrypted thinking tokens + text output tokens)`

### Managing tokens with extended thinking
<a name="claude-messages-extended-thinking-max-tokens-manage"></a>

Given the context window and `max_tokens` behavior with extended thinking Claude 3.7 and 4 models, you might need to perform one of the following actions:
+ More actively monitor and manage your token usage.
+ Adjust `max_tokens` values as your prompt length changes.
+ Be aware that previous thinking blocks don’t accumulate in your context window. This change has been made to provide more predictable and transparent behavior, especially as maximum token limits have increased significantly.

## Extended thinking token cost considerations
<a name="claude-messages-extended-thinking-cost"></a>

The thinking process incurs charges for the following:
+ Tokens used during thinking (output tokens)
+ Thinking blocks from the last assistant turn included in subsequent requests (input tokens)
+ Standard text output tokens

**Tip**  
When extended thinking is enabled, a specialized 28 or 29 token system prompt is automatically included to support this feature.

The `budget_tokens` parameter determines the maximum number of tokens Claude is allowed to use for its internal reasoning process. Larger budgets can improve response quality by enabling more thorough analysis for complex problems, although Claude may not use the entire budget allocated, especially at ranges above 32K.

With interleaved thinking, the `budget_tokens` can exceed the `max_tokens` parameter as it represents the total budget across all thinking blocks within one assistant turn.

When using summarized thinking, keep the following information in mind:
+ **Input tokens**: Tokens in your original request
+ **Output tokens (billed)**: The original thinking tokens that Claude generated internally
+ **Output tokens (visible)**: The summarized thinking tokens you see in the response
+ **No charge**: Tokens used to generate the summary
+ The `summary_status` field can indicate if token limits aﬀected summarization
+ The billed output token count will not match the visible token count in the response. You are billed for the full thinking process, not the summary you see.