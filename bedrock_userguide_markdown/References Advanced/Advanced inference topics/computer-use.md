

# Use computer use tools to automate GUI tasks with Amazon Bedrock models
<a name="computer-use"></a>

Computer use is an Anthropic Claude tool family (in beta) for automating graphical user interface (GUI) tasks. The model returns `tool_use` actions such as `screenshot`, `left_click`, `type`, and `scroll` in JSON. Your application executes those actions on a desktop or container and returns the resulting screenshot to Claude on the next turn.

For the underlying tool protocol, the full list of actions, and prompt-engineering guidance, see [Computer use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) in the Anthropic documentation. This page covers the Amazon Bedrock-specific usage on top of that protocol.

**Warning**  
Computer use is made available to you as a "Beta Service" as defined in the AWS Service Terms. It is subject to your Agreement with AWS, the AWS Service Terms, and the applicable model EULA. The Computer Use API poses unique risks distinct from standard API features or chat interfaces. These risks are heightened when using the Computer Use API to interact with the Internet. To minimize risks, consider taking precautions such as:  
Operate computer use functionality in a dedicated Virtual Machine or container with minimal privileges to prevent direct system attacks or accidents.
To prevent information theft, avoid giving the Computer Use API access to sensitive accounts or data.
Limit the computer use API's internet access to required domains to reduce exposure to malicious content.
To ensure proper oversight, keep a human in the loop for sensitive tasks (such as making decisions that could have meaningful real-world consequences) and for anything requiring affirmative consent (such as accepting cookies, executing financial transactions, or agreeing to terms of service).
Any content that you enable Claude to see or access can potentially override instructions or cause Claude to make mistakes or perform unintended actions. Taking proper precautions, such as isolating Claude from sensitive surfaces, is essential — including to avoid risks related to prompt injection. Before enabling or requesting permissions necessary to enable computer use features in your own products, please inform end users of any relevant risks, and obtain their consent as appropriate.

**Topics**
+ [Use computer use on Amazon Bedrock](#computer-use-bedrock-specifics)
+ [Example request](#computer-use-example-code)

## Use computer use on Amazon Bedrock
<a name="computer-use-bedrock-specifics"></a>

Computer use is supported on both the `bedrock-runtime` and `bedrock-mantle` endpoints. To find which models support computer use on each endpoint, see the *Capabilities and Features* table in each [](model-cards.md). Submitting a request to a model that doesn't support computer use, or pairing a tool type with an unsupported model, returns a `400 invalid_request_error`.

To enable computer use on a request, include both:
+ An `anthropic_beta` entry naming a computer-use beta version (for example, `"anthropic_beta": ["computer-use-2025-11-24"]` in the request body for `bedrock-runtime`, or the `anthropic-beta: computer-use-2025-11-24` HTTP header for `bedrock-mantle`).
+ One or more Anthropic pre-defined tool entries in the `tools` array, with a `type` field that matches the beta version (for example, `computer_20251124`, `bash_20250124`, or `text_editor_20250124`).

For the beta-version-to-tool-type pairings, additional Anthropic-defined tools (bash and text editor), and the full request and response field documentation, see [Computer use (Beta)](model-parameters-anthropic-claude-messages-tool-use.md#model-parameters-anthropic-claude-messages-computer-use).

## Example request
<a name="computer-use-example-code"></a>

The following Python example sends a Messages API request through the `bedrock-runtime` endpoint with the computer use tool. Replace the `modelId` with one that supports computer use (see [](model-cards.md)).

```
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="us.anthropic.claude-opus-4-7",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "anthropic_beta": ["computer-use-2025-11-24"],
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Take a screenshot of the desktop."}
        ],
        "tools": [
            {
                "type": "computer_20251124",
                "name": "computer",
                "display_width_px": 1024,
                "display_height_px": 768,
            }
        ],
    }),
)

result = json.loads(response["body"].read())
print(result["stop_reason"])  # "tool_use" when the model issues a computer action
print(result["content"])      # contains the tool_use block describing the action
```

For the equivalent `bedrock-mantle` Messages API request shape, see [Inference using Anthropic Messages API](inference-messages-api.md).