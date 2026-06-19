

# Anthropic Claude tool use
<a name="model-parameters-anthropic-claude-messages-tool-use"></a>

**Warning**  
Several functions below are offered in beta as indicated. These features are made available to you as a "Beta Service" as defined in the AWS Service Terms. It is subject to your Agreement with AWS and the AWS Service Terms, and the applicable model EULA.

With Anthropic Claude models, you can specify a tool that the model can use to answer a message. For example, you could specify a tool that gets the most popular song on a radio station. If the user passes the message *What's the most popular song on WZPZ?*, the model determines that the tool you specified can help answer the question. In its response, the model requests that you run the tool on its behalf. You then run the tool and pass the tool result to the model, which then generates a response for the original message. For more information, see [Tool use (function calling)](https://docs.anthropic.com/en/docs/tool-use) in the Anthropic Claude documentation.

**Tip**  
We recommend that you use the Converse API for integrating tool use into your application. For more information, see [Use a tool to complete an Amazon Bedrock model response](tool-use.md). 

**Important**  
Claude Sonnet 4.5 now preserves intentional formatting in tool call string parameters. Previously, trailing newlines in string parameters were sometimes incorrectly stripped. This fix ensures that tools requiring precise formatting (like text editors) receive parameters exactly as intended. This is a behind-the-scenes improvement with no API changes required. However, tools with string parameters may now receive values with trailing newlines that were previously stripped.

**Note**  
Claude Sonnet 4.5 includes automatic optimizations to improve model performance. These optimizations may add small amounts of tokens to requests, but you are not billed for these system-added tokens.

You specify the tools that you want to make available to a model in the `tools` field. The following example is for a tool that gets the most popular songs on a radio station. 

```
[
    {
        "name": "top_song",
        "description": "Get the most popular song played on a radio station.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sign": {
                    "type": "string",
                    "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ and WKRP."
                }
            },
            "required": [
                "sign"
            ]
        }
    }
]
```

When the model needs a tool to generate a response to a message, it returns information about the requested tool, and the input to the tool, in the message `content` field. It also sets the stop reason for the response to `tool_use`.

```
{
    "id": "msg_bdrk_01USsY5m3XRUF4FCppHP8KBx",
    "type": "message",
    "role": "assistant",
    "model": "claude-3-sonnet-20240229",
    "stop_sequence": null,
    "usage": {
        "input_tokens": 375,
        "output_tokens": 36
    },
    "content": [
        {
            "type": "tool_use",
            "id": "toolu_bdrk_01SnXQc6YVWD8Dom5jz7KhHy",
            "name": "top_song",
            "input": {
                "sign": "WZPZ"
            }
        }
    ],
    "stop_reason": "tool_use"
}
```

In your code, you call the tool on the tools behalf. You then pass the tool result (`tool_result`) in a user message to the model.

```
{
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_bdrk_01SnXQc6YVWD8Dom5jz7KhHy",
            "content": "Elemental Hotel"
        }
    ]
}
```

In its response, the model uses the tool result to generate a response for the original message.

```
{
    "id": "msg_bdrk_012AaqvTiKuUSc6WadhUkDLP",
    "type": "message",
    "role": "assistant",
    "model": "claude-3-sonnet-20240229",
    "content": [
        {
            "type": "text",
            "text": "According to the tool, the most popular song played on radio station WZPZ is \"Elemental Hotel\"."
        }
    ],
    "stop_reason": "end_turn"
}
```

## Fine-grained tool streaming
<a name="model-parameters-anthropic-claude-messages-fine-grained-tool-streaming"></a>

Fine-grained tool streaming is an Anthropic Claude model capability available with Claude Sonnet 4.5, Claude Haiku 4.5, Claude Sonnet 4, and Claude Opus 4. With fine-grained tool streaming, Claude developers can stream tool use parameters without buffering or JSON validation, reducing the latency to begin receiving large parameters.

**Note**  
When using fine-grained tool streaming, you may potentially receive invalid or partial JSON inputs. Please make sure to account for these edge cases in your code.

To use this feature, simply add the header `fine-grained-tool-streaming-2025-05-14` to a tool use request.

Here’s an example of how to specify the fine-grained tool streaming header:

```
{
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 1024,
  "anthropic_beta": ["fine-grained-tool-streaming-2025-05-14"],
  "messages": [
    {
      "role": "user",
      "content": "Can you write a long poem and make a file called poem.txt?"
    }
  ],
  "tools": [
    {
      "name": "make_file",
      "description": "Write text to a file",
      "input_schema": {
        "type": "object",
        "properties": {
          "filename": {
            "type": "string",
            "description": "The filename to write text to"
          },
          "lines_of_text": {
            "type": "array",
            "description": "An array of lines of text to write to the file"
          }
        },
        "required": [
          "filename",
          "lines_of_text"
        ]
      }
    }
  ]
}
```

In this example, fine-grained tool streaming enables Claude to stream the lines of a long poem into the tool call `make_file` without buffering to validate if the `lines_of_text` parameter is valid JSON. This means you can see the parameter stream as it arrives, without having to wait for the entire parameter to buffer and validate.

With fine-grained tool streaming, tool use chunks start streaming faster, and are often longer and contain fewer word breaks. This is due to differences in chunking behavior.

For example, without fine-grained streaming (15s delay):

```
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
```

With fine-grained streaming (3s delay):

```
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
```

**Note**  
Because fine-grained streaming sends parameters without buffering or JSON validation, there is no guarantee that the resulting stream will complete in a valid JSON string. Particularly, if the stop reason `max_tokens` is reached, the stream may end midway through a parameter and may be incomplete. You will generally have to write specific support to handle when `max_tokens` is reached.

## Computer use (Beta)
<a name="model-parameters-anthropic-claude-messages-computer-use"></a>

Computer use is an Anthropic Claude tool family (in beta) for automating graphical user interface (GUI) tasks. For an overview, the Amazon Bedrock-specific request shape, and an end-to-end example, see [Use computer use tools to automate GUI tasks with Amazon Bedrock models](computer-use.md). To find which models support computer use on each endpoint, see the *Capabilities and Features* table in each [](model-cards.md).

To enable computer use on a request, set `anthropic_beta` to a computer-use version and include a tool entry whose `type` matches that version. The valid pairings are:


| Beta header | Computer tool type | 
| --- | --- | 
| computer-use-2025-11-24 | computer\_20251124 | 
| computer-use-2025-01-24 | computer\_20250124 | 
| computer-use-2024-10-22 | computer\_20241022 | 

Each tool type works only with a specific subset of models. Submitting a tool type that a model does not support returns a `400 invalid_request_error` with a message such as `'claude-opus-4-7' does not support tool types: computer_20241022`. Confirm support in the model's *Capabilities and Features* table before sending requests.

For the underlying tool protocol, the full action vocabulary, and prompt-engineering guidance, see [Computer use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) in the Anthropic documentation.

## Anthropic defined tools
<a name="model-parameters-anthropic-anthropic-defined-tools"></a>

Anthropic provides a set of pre-defined tools that Claude models can use to interact with computers. When specifying an Anthropic-defined tool, the `description` and `tool_schema` fields are not necessary or allowed. The model does not execute these tools automatically; you must run each requested action and return a `tool_result` to Claude. To find which of these tools each model accepts, see the *Capabilities and Features* table in the model's [](model-cards.md); submitting a tool type that a model does not support returns a `400 invalid_request_error`.


| Tool | Notes | 
| --- | --- | 
|  <pre>{ <br />    "type": "computer_20251124", <br />    "name": "computer" <br />}</pre>  | Latest computer-use tool. Use with `"anthropic_beta": ["computer-use-2025-11-24"]`. | 
|  <pre>{ <br />    "type": "computer_20250124", <br />    "name": "computer" <br />}</pre>  | Use with `"anthropic_beta": ["computer-use-2025-01-24"]`. | 
|  <pre>{ <br />    "type": "computer_20241022", <br />    "name": "computer" <br />}</pre>  | Legacy. Use with `"anthropic_beta": ["computer-use-2024-10-22"]`. | 
|  <pre>{ <br />    "type": "text_editor_20250124", <br />    "name": "str_replace_based_edit_tool" <br />}</pre>  | Update to the existing `str_replace_editor` tool. Use with `"anthropic_beta": ["computer-use-2025-01-24"]` or `["computer-use-2025-11-24"]`. | 
|  <pre>{ <br />    "type": "text_editor_20241022", <br />    "name": "str_replace_editor" <br />}</pre>  | Legacy. Use with `"anthropic_beta": ["computer-use-2024-10-22"]`. | 
|  <pre>{ <br />    "type": "bash_20250124", <br />    "name": "bash" <br />}</pre>  | Use with `"anthropic_beta": ["computer-use-2025-01-24"]` or `["computer-use-2025-11-24"]`. | 
|  <pre>{ <br />    "type": "bash_20241022", <br />    "name": "bash" <br />}</pre>  | Legacy. Use with `"anthropic_beta": ["computer-use-2024-10-22"]`. | 

The `type` field identifies the tool and its parameters for validation purposes; the `name` field is the tool name exposed to the model.

If you want to prompt the model to use one of these tools, you can explicitly refer the tool by the `name` field. The `name` field must be unique within the tool list; you cannot define a tool with the same `name` as an Anthropic-defined tool in the same API call.

## Automatic tool call clearing (Beta)
<a name="model-parameters-anthropic-claude-automatic-tool-call-clearing"></a>

**Warning**  
Automatic tool call clearing is made available as a "Beta Service" as defined in the AWS Service Terms.

**Note**  
This feature is currently supported on Claude Sonnet 4/4.5, Claude Haiku 4.5, and Claude Opus 4/4.1/4.5.

Automatic tool call clearing is an Anthropic Claude model capability (in beta). With this feature, Claude can automatically clear old tool use results as you approach token limits, allowing for more efficient context management in multi-turn tool use scenarios. To use tool use clearing, you need to add `context-management-2025-06-27` to the list of beta headers on the anthropic\_beta request parameter. You will also need to specify the use of `clear_tool_uses_20250919` and choose from the following configuration options.

These are the available controls for the `clear_tool_uses_20250919` context management strategy. All are optional or have defaults:


| **Configuration Option** | **Description** | 
| --- | --- | 
| `trigger`<br />default: 100,000 input tokens | Defines when the context editing strategy activates. Once the prompt exceeds this threshold, clearing will begin. You can specify this value in either input\_tokens or tool\_uses. | 
| `keep`<br />default: 3 tool uses | Defines how many recent tool use/result pairs to keep after clearing occurs. The API removes the oldest tool interactions first, preserving the most recent ones. Helpful when the model needs access to recent tool interactions to continue the conversation effectively. | 
| `clear_at_least` (optional) | Ensures a minimum number of tokens are cleared each time the strategy activates. If the API can't clear at least the specified amount, the strategy will not be applied. This is useful for determining whether context clearing is worth breaking your prompt cache for. | 
| `exclude_tools` (optional) | List of tool names whose tool uses and results should never be cleared. Useful for preserving important context. | 
| `clear_tool_inputs` (optional, default False) | Controls whether the tool call parameters are cleared along with the tool results. By default, only the tool results are cleared while keeping Claude's original tool calls visible, so Claude can see what operations were performed even after the results are removed. | 

**Note**  
Tool clearing will invalidate your cache if your prefixes contain your tools.

**Important**  
The Anthropic `web_search_20250305` server tool is not supported on Amazon Bedrock.

------
#### [ Request ]

```
from anthropic import AnthropicBedrock

client = AnthropicBedrock()

response = client.beta.messages.create(
    betas=["context-management-2025-06-27"],
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a simple command line calculator app using Python"
       }
    ],
    tools=[
        {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 10000
        }
    ],
    extra_body={
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                # The below parameters are OPTIONAL:
                    # Trigger clearing when threshold is exceeded
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    # Number of tool uses to keep after clearing
                    "keep": {
                        "type": "tool_uses",
                        "value": 3
                    },
                    # Optional: Clear at least this many tokens
                    "clear_at_least": {
                        "type": "input_tokens",
                        "value": 5000
                    },
                    # Exclude these tools uses from being cleared
                    "exclude_tools": ["str_replace_based_edit_tool"]
                }
            ]
       }
    }
 )
```

------
#### [ Response ]

```
{
    "id": "msg_123",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "tool_use",
            "id": "toolu_456",
            "name": "data_analyzer",
            "input": {
                "data": "sample data"
            }
        }
    ],
    "context_management": {
        "applied_edits": [
            {
                "type": "clear_tool_uses_20250919",
                "cleared_tool_uses": 8,  # Number of tool use/result pairs that were cleared
                "cleared_input_tokens": 50000  # Total number of input tokens removed from the prompt
            }
        ]
    }
    "stop_reason": "tool_use",
    "usage": {
        "input_tokens": 150,
        "output_tokens": 50
    }
}
```

------
#### [ Streaming Response ]

```
data: {"type": "message_start", "message": {"id": "msg_123", "type": "message", "role": "assistant"}}

data: {"type": "content_block_start", "index": 0, "content_block": {"type": "tool_use", "id": "toolu_456", "name": "data_analyzer", "input": {}}}

data: {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": "{\"data\": \"sample"}}

data: {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": " data\"}"}}

data: {"type": "content_block_stop", "index": 0}

data: {"type": "message_delta", "delta": {"stop_reason": "tool_use"}}

data: {"type": "message_stop"}

{
  "type": "message_delta",
  "delta": {
    "stop_reason": "end_turn",
    "stop_sequence": null,
  },
  "usage": {
    "output_tokens": 1024
  },
  "context_management": {
    "applied_edits": [...],
  }
}
```

------

**Note**  
Bedrock does not currently support `clear_tool_uses_20250919` context management on the CountTokens API.

## Memory Tool (Beta)
<a name="model-parameters-anthropic-claude-memory-tool"></a>

**Warning**  
Memory Tool is made available as a "Beta Service" as defined in the AWS Service Terms.

Claude Sonnet 4.5 includes a new memory tool. This tool provides you a way to manage memory across conversations. With this feature, you can allow Claude to retrieve information outside the context window by providing access to a local directory. This feature is available in beta. To use this feature, you must include `context-management-2025-06-27` in the `anthropic_beta` parameter.

Tool definition:

```
{
  "type": "memory_20250818",
  "name": "memory"
}
```

Example Request:

```
{
    "max_tokens": 2048,
    "anthropic_version": "bedrock-2023-05-31",
    "anthropic_beta": ["context-management-2025-06-27"],
    "tools": [{
        "type": "memory_20250818",
        "name": "memory"
    }],
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": "Remember that my favorite color is blue and I work at Amazon?"}]
        }
    ]
}
```

Example Response:

```
{
    "id": "msg_vrtx_014mQ5ficCRB6PEa5k5sKqHd",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-4-20250514",
    "content": [
        {
            "type": "text",
            "text": "I'll start by checking your memory directory and then record this important information about you."
        },
        {
            "type": "tool_use",
            "id": "toolu_vrtx_01EU1UrCDigyPMRntr3VYvUB",
            "name": "memory",
            "input": {
                "command": "view",
                "path": "/memories"
            }
        }
    ],
    "stop_reason": "tool_use",
    "stop_sequence": null,
    "usage": {
        "input_tokens": 1403,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "output_tokens": 87
    },
    "context_management": {
        "applied_edits": []
    }
}
```

## Cost considerations for tool use
<a name="model-parameters-anthropic-claude-tool-use-cost"></a>

Tool use requests are priced based on the following factors:

1. The total number of input tokens sent to the model (including in the tools parameter).

1. The number of output tokens generated.

Tools are priced the same as all other Claude API requests, but do include additional tokens per request. The additional tokens from tool use come from the following:
+ The `tools` parameter in the API requests. For example, tool names, descriptions, and schemas.
+ Any `tool_use` content blocks in API requests and responses.
+ Any `tool_result` content blocks in API requests.

When you use tools, the Anthropic models automatically include a special system prompt that enables tool use. The number of tool use tokens required for each model is listed in the following table. This table excludes the additional tokens described previously. Note that this table assumes at least one tool is provided. If no tools are provided, then a tool choice of none uses 0 additional system prompt tokens.


| Model | Tool choice | Tool use system prompt token count | 
| --- | --- | --- | 
| Claude Opus 4.5<br />Claude Opus 4.1<br />Claude Opus 4<br />Claude Sonnet 4.5<br />Claude Haiku 4.5<br />Claude Sonnet 4<br />Claude 3.7 Sonnet<br />Claude 3.5 Sonnet v2 | auto or none | 346 | 
| Claude Opus 4.5<br />Claude Opus 4.1<br />Claude Opus 4<br />Claude Sonnet 4.5<br />Claude Haiku 4.5<br />Claude Sonnet 4<br />Claude 3.7 Sonnet<br />Claude 3.5 Sonnet v2 | any or tool | 313 | 
| Claude 3.5 Sonnet | auto or none | 294 | 
| Claude 3.5 Sonnet | any or tool | 261 | 
| Claude 3 Opus | auto or none | 530 | 
| Claude 3 Opus | any or tool | 281 | 
| Claude 3 Sonnet | auto or none | 159 | 
| Claude 3 Sonnet | any or tool | 235 | 
| Claude 3 Haiku | auto or none | 264 | 
| Claude 3 Haiku | any or tool | 340 | 

## Tool search tool (beta)
<a name="model-parameters-anthropic-claude-tool-search-tool"></a>

Tool Search Tool allows Claude to work with hundreds or even thousands of tools without loading all their definitions into the context window upfront. Instead of declaring all tools immediately, you can mark them with `defer_loading: true`, and Claude finds and loads only the tools it needs through the tool search mechanism.

To access this feature, you must include `tool-search-tool-2025-10-19` in the `anthropic_beta` parameter. Note that this feature is currently only available via the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) APIs.

Tool definition:

```
{
    "type": "tool_search_tool_regex",
    "name": "tool_search_tool_regex"
}
```

Request example:

```
{
    "anthropic_version": "bedrock-2023-05-31",
    "anthropic_beta": [
        "tool-search-tool-2025-10-19"
    ],
    "max_tokens": 4096,
    "tools": [{
            "type": "tool_search_tool_regex",
            "name": "tool_search_tool_regex"
        },
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            },
            "defer_loading": true
        },
        {
            "name": "search_files",
            "description": "Search through files in the workspace",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "file_types": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["query"]
            },
            "defer_loading": true
        }
    ],
    "messages": [{
        "role": "user",
        "content": "What's the weather in Seattle?"
    }]
}
```

Response example

```
{
    "role": "assistant",
    "content": [{
            "type": "text",
            "text": "I'll search for the appropriate tools to help with this task."
        },
        {
            "type": "server_tool_use",
            "id": "srvtoolu_01ABC123",
            "name": "tool_search_tool_regex",
            "input": {
                "pattern": "weather"
            }
        },
        {
            "type": "tool_search_tool_result",
            "tool_use_id": "srvtoolu_01ABC123",
            "content": {
                "type": "tool_search_tool_search_result",
                "tool_references": [{
                    "type": "tool_reference",
                    "tool_name": "get_weather"
                }]
            }
        },
        {
            "type": "text",
            "text": "Now I can check the weather."
        },
        {
            "type": "tool_use",
            "id": "toolu_01XYZ789",
            "name": "get_weather",
            "input": {
                "location": "Seattle",
                "unit": "fahrenheit"
            }
        }
    ],
    "stop_reason": "tool_use"
}
```

Streaming example

```
# Event 1: content_block_start(with complete server_tool_use block) {
    "type": "content_block_start",
    "index": 0,
    "content_block": {
        "type": "server_tool_use",
        "id": "srvtoolu_01ABC123",
        "name": "tool_search_tool_regex"
    }
}

# Event 2: content_block_delta(input JSON streamed) {
    "type": "content_block_delta",
    "index": 0,
    "delta": {
        "type": "input_json_delta",
        "partial_json": "{\"regex\": \".*weather.*\"}"
    }
}

# Event 3: content_block_stop(tool_use complete) {
    "type": "content_block_stop",
    "index": 0
}

# Event 4: content_block_start(COMPLETE result in single chunk) {
    "type": "content_block_start",
    "index": 1,
    "content_block": {
        "type": "tool_search_tool_result",
        "tool_use_id": "srvtoolu_01ABC123",
        "content": {
            "type": "tool_search_tool_search_result",
            "tool_references": [{
                "type": "tool_reference",
                "tool_name": "get_weather"
            }]
        }
    }
}

# Event 5: content_block_stop(result complete) {
    "type": "content_block_stop",
    "index": 1
}
```

**Custom tool search tools**  
You can implement custom tool search tools (for example, using embeddings) by defining a tool that returns `tool_reference` blocks. The custom tool must have `defer_loading: false` while other tools should have `defer_loading: true`. When you define your own Tool Search Tool, it should return a tool result containing `tool_reference` content blocks that point to the tools you want Claude to use.

The expected customer-defined Tool Search Tool result response format:

```
{
    "type": "tool_result",
    "tool_use_id": "toolu_01ABC123",
    "content": [{
            "type": "tool_reference",
            "tool_name": "get_weather"
        },
        {
            "type": "tool_reference",
            "tool_name": "weather_forecast"
        }
    ]
}
```

The `tool_name` must match a tool defined in the request with `defer_loading: true`. Claude will then have access to those tools' full schemas.

**Custom search tools - Detailed example**  
You can implement custom tool search tools (for example, using embeddings or semantic search) by defining a tool that returns `tool_reference` blocks. This enables sophisticated tool discovery mechanisms beyond regex matching.

Request example with custom TST:

```
{
    "model": "claude-sonnet-4-5-20250929",
    "anthropic_version": "bedrock-2023-05-31",
    "anthropic_beta": ["tool-search-tool-2025-10-19"],
    "max_tokens": 4096,
    "tools": [{
            "name": "semantic_tool_search",
            "description": "Search for available tools using semantic similarity. Returns the most relevant tools for the given query.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language description of what kind of tool is needed"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of tools to return (default: 5)"
                    }
                },
                "required": ["query"]
            },
            "defer_loading": false
        },
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            },
            "defer_loading": true
        },
        {
            "name": "search_flights",
            "description": "Search for available flights between locations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string"
                    },
                    "destination": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    }
                },
                "required": ["origin", "destination", "date"]
            },
            "defer_loading": true
        }
    ],
    "messages": [{
        "role": "user",
        "content": "What's the weather forecast in Seattle for the next 3 days?"
    }]
}
```

Claude's response (calling custom TST):

```
{
    "role": "assistant",
    "content": [{
            "type": "text",
            "text": "I'll search for the appropriate tools to help with weather information."
        },
        {
            "type": "tool_use",
            "id": "toolu_01ABC123",
            "name": "semantic_tool_search",
            "input": {
                "query": "weather forecast multiple days",
                "top_k": 3
            }
        }
    ],
    "stop_reason": "tool_use"
}
```

**Customer-provided tool result**  
After performing semantic search on the tool library, the customer returns matching tool references:

```
{
    "role": "user",
    "content": [{
        "type": "tool_search_tool_result",
        "tool_use_id": "toolu_01ABC123",
        "content": {
            "type": "tool_search_tool_search_result",
            "tool_references": [{
                "type": "tool_reference",
                "tool_name": "get_weather"
            }]
        }
    }]
}
```

Claude's follow-up (using discovered tool)

```
{
    "role": "assistant",
    "content": [{
            "type": "text",
            "text": "I found the forecast tool. Let me get the weather forecast for Seattle."
        },
        {
            "type": "tool_use",
            "id": "toolu_01DEF456",
            "name": "get_weather",
            "input": {
                "location": "Seattle, WA"
            }
        }
    ],
    "stop_reason": "tool_use"
}
```

**Error handling**
+ Setting `defer_loading: true` for all tools (including the Tool Search Tool) will throw a 400 error.
+ Passing a `tool_reference` without a corresponding tool definition will throw a 400 error

## Tool use examples (beta)
<a name="model-parameters-anthropic-claude-tool-use-examples"></a>

Claude Opus 4.5 supports user-provided examples in tool definitions to increase Claude's tool use performance. You can provide examples as full function calls, formatted exactly as real LLM outputs would be, without needing translation into another format. To use this feature, you must include `tool-examples-2025-10-29` in the `anthropic_beta` parameter.

Tool definition example:

```
{
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    },
    "input_examples": [{
            "location": "San Francisco, CA",
            "unit": "fahrenheit"
        },
        {
            "location": "Tokyo, Japan",
            "unit": "celsius"
        },
        {
            "location": "New York, NY"
        }
    ]
}
```

**Validation rules**
+ Schema conformance: Each example in `input_examples` must be valid according to the tool's `input_schema`.
  + Required fields must be present in at least one example.
  + Field types must match the schema.
  + Enum values must be from the allowed set.
  + If validation fails, return a 400 error with details about which example failed validation.
+ Array requirements: `input_examples` must be an array (can be empty).
  + Empty array `[]` is valid and equivalent to omitting the field.
  + Single example must still be wrapped in an array: `[{...}]`
  + Length limit: start with a limit of 20 examples per tool definition.

Error examples:

```
// Invalid: Example doesn't match schema (missing required field)
{
    "type": "invalid_request_error",
    "message": "Tool 'get_weather' input_examples[0] is invalid: Missing required property 'location'"
}

// Invalid: Example has wrong type for field
{
    "type": "invalid_request_error",
    "message": "Tool 'search_products' input_examples[1] is invalid: Property 'filters.price_range.min' must be a number, got string"
}

// Invalid: input_examples on server-side tool
{
    "type": "invalid_request_error",
    "message": "input_examples is not supported for server-side tool"
}
```