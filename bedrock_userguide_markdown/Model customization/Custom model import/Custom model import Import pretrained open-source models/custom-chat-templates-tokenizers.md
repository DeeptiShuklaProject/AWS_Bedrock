

# Handling Custom Chat Templates and Tokenizers
<a name="custom-chat-templates-tokenizers"></a>

Custom chat templates and tokenizers are essential components for properly formatting conversational inputs and managing token generation in your imported models. Custom Model Import supports importing models with custom chat templates that define how multi-turn conversations are structured and tokenized.

## Importing Models with Custom Chat Templates
<a name="import-chat-template"></a>

When importing a model with custom chat templates, ensure that you follow the best practices outlined in the main Custom Model Import documentation, including bringing in model weights in safe tensors format and providing all necessary configuration files.

### Chat Template Format Requirements
<a name="chat-template-format-requirements"></a>

If your model uses a custom chat template and you want to use that template with Amazon Bedrock, you must include the chat template file in one of the following formats:
+ **`chat_template.jinja`** — A Jinja2-based template file that defines how messages are formatted.
+ **`chat_template.json`** — A JSON file containing the chat template as a string value.
+ **`tokenizer_config.json` with embedded chat template** — Alternatively, you can include the chat template directly within your `tokenizer_config.json` file as a `chat_template` field. For an example, see the [Hermes-2-Pro tokenizer\_config.json](https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B/blob/main/tokenizer_config.json#L2059) on Hugging Face.

Custom Model Import will automatically process these files and include them in the correct directories during the import process.

#### Chat Template Precedence
<a name="chat-template-precedence"></a>

If you provide multiple chat template sources, Amazon Bedrock applies the following precedence rules:

1. **Separate chat template files take precedence** — If you include both a separate chat template file (`chat_template.jinja` or `chat_template.json`) AND a `chat_template` field in your `tokenizer_config.json`, the separate file will be used and the embedded template in `tokenizer_config.json` will be ignored.

1. **Embedded template as fallback** — If you do not provide a separate chat template file, Amazon Bedrock will use the `chat_template` field from your `tokenizer_config.json` if present.

**Warning**  
**Choose one approach:** To avoid confusion and ensure predictable behavior, we strongly recommend using only ONE of these approaches:  
**Option 1:** Provide separate chat template files (`chat_template.jinja` or `chat_template.json`) without including a `chat_template` field in your `tokenizer_config.json`.
**Option 2:** Include the `chat_template` field directly in your `tokenizer_config.json` and do not provide separate template files.
If you have custom tool templates or complex chat template configurations, we recommend using Option 2 (embedding the template in `tokenizer_config.json`) as it allows you to define multiple named templates (such as "default" and "tool\_use") within a single configuration file.

**Note**  
The chat template file must follow the Hugging Face format and naming conventions. Ensure that your template is compatible with the Transformers library.

#### Chat Template Format Examples
<a name="chat-template-examples"></a>

Here are examples of the two supported chat template formats:

------
#### [ Jinja Format (chat\_template.jinja) ]

A simplified example of a Jinja2-based chat template:

```
{% for message in messages %}
{% if loop.first and message['role'] != 'system' %}
<|im_start|>system
You are a helpful assistant.<|im_end|>
{% endif %}
<|im_start|>{{ message['role'] }}
{{ message['content'] }}<|im_end|>
{% endfor %}
{% if add_generation_prompt %}
<|im_start|>assistant
{% endif %}
```

For a complete example, see the [GPT-OSS chat template](https://huggingface.co/openai/gpt-oss-20b/blob/main/chat_template.jinja) on Hugging Face.

------
#### [ JSON Format (chat\_template.json) ]

A simplified example of a JSON-based chat template with vision support:

```
{
    "chat_template": "{% for message in messages %}{% if loop.first and message['role'] != 'system' %}<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n{% endif %}<|im_start|>{{ message['role'] }}\n{% if message['content'] is string %}{{ message['content'] }}<|im_end|>\n{% else %}{% for content in message['content'] %}{% if content['type'] == 'image' %}<|vision_start|><|image_pad|><|vision_end|>{% elif 'text' in content %}{{ content['text'] }}{% endif %}{% endfor %}<|im_end|>\n{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant\n{% endif %}"
}
```

For a complete example with multimodal support, see the [Qwen2-VL chat template](https://huggingface.co/Qwen/Qwen2-VL-72B-Instruct/blob/main/chat_template.json) on Hugging Face.

------

**Important**  
Ensure that your chat template file follows the exact naming convention (`chat_template.jinja` or `chat_template.json`) and format shown in the examples above. Incorrectly formatted templates may cause import or inference failures.

## Invoking Models with Custom Chat Templates
<a name="invoke-custom-chat-templates"></a>

Once you have imported a model with a custom chat template, you have two options for invoking the model with properly formatted conversational inputs:

### Using OpenAI ChatCompletion API with Messages
<a name="chatcompletion-api-approach"></a>

If you are providing inputs in the messages schema format, you should use the **OpenAI ChatCompletion API**. When you use this API format with a model that has an uploaded chat template (`chat_template.jinja` or `chat_template.json`), Amazon Bedrock will automatically convert your input messages into the correct format using the chat template.

This is the recommended approach as it provides the most seamless integration and allows Amazon Bedrock to handle the chat template application automatically.

**Example: Using OpenAI ChatCompletion API with custom chat template**

```
import json
import boto3

# Initialize Bedrock Runtime client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Define the model ARN for your imported model with custom chat template
model_id = 'arn:aws:bedrock:us-east-1:123456789012:imported-model/your-model-id'

# Prepare the request payload using messages format
payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ],
    "max_tokens": 150,
    "temperature": 0.7
}

# Invoke the model
response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

# Parse and display the response
response_body = json.loads(response['body'].read())
print(json.dumps(response_body, indent=2))
```

In this example, Amazon Bedrock will automatically apply your custom chat template to the messages array, converting it into the appropriate format for your model.

### Manual Tokenization Approach
<a name="manual-tokenization-approach"></a>

Alternatively, if you prefer to have full control over the chat template application and tokenization process, you can manually apply the chat template to your conversation and then use the **Completion API** (not ChatCompletion) with the pre-formatted text.

This approach is useful when you need to customize the template application logic or when working with specialized tokenization requirements.

#### Step 1: Apply Chat Template Locally
<a name="apply-chat-template-locally"></a>

Use the following code snippet to load your custom chat template and apply it to a conversation locally:

```
from transformers import AutoTokenizer

# Configuration paths - update these with your actual paths
TOKENIZER_PATH = ""  # Path to tokenizer directory

# Load tokenizer with updated chat template
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

# Test chat template with sample conversation
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"},
]

# Apply chat template and display formatted output to make sure chat template works as expected
formatted_chat = tokenizer.apply_chat_template(chat_history, tokenize=False)
print(formatted_chat)
```

This code demonstrates how to:

1. Load your tokenizer configuration from the model files

1. Add the custom chat template to the tokenizer configuration

1. Apply the chat template to a conversation history

1. Generate the formatted text that can be sent to the model

#### Step 2: Invoke with Completion API
<a name="invoke-with-completion-api"></a>

After applying the chat template locally, use the formatted text with the Completion API:

```
import json
import boto3

# Initialize Bedrock Runtime client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Define the model ARN for your imported model
model_id = 'arn:aws:bedrock:us-east-1:123456789012:imported-model/your-model-id'

# Use the formatted_chat output from Step 1 as the prompt
payload = {
    "prompt": formatted_chat,
    "max_tokens": 150,
    "temperature": 0.7
}

# Invoke the model using Completion format (not ChatCompletion)
response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

# Parse and display the response
response_body = json.loads(response['body'].read())
print(json.dumps(response_body, indent=2))
```

**Warning**  
**Always use `max_tokens` parameter:** When using the Completion API with custom model imports, always use the `max_tokens` parameter to ensure OpenAI completion schema compatibility. This avoids any translation confusion and ensures consistent behavior across different SDK implementations. Do not use model-specific parameter names like `max_gen_len` or similar variants.

**Important**  
When using the manual tokenization approach, you must use the **Completion API** format (with `prompt` field), not the ChatCompletion API format (with `messages` field). The ChatCompletion API expects raw messages and will attempt to apply the chat template again, resulting in incorrect formatting.

### Best Practices
<a name="chat-template-best-practices"></a>
+ **Use ChatCompletion API when possible** — The OpenAI ChatCompletion API with messages format provides the most seamless experience and allows Amazon Bedrock to handle chat template application automatically.
+ **Validate your chat template** — Before importing your model, test your chat template locally using the Transformers library to ensure it produces the expected output format.
+ **Include all special tokens** — Ensure your chat template includes all necessary special tokens (such as beginning-of-sequence, end-of-sequence, and role markers) that your model expects.
+ **Test with multi-turn conversations** — Validate that your chat template correctly handles multi-turn conversations with alternating user and assistant messages.
+ **Consider vision support** — If your model supports multimodal inputs, ensure your chat template includes logic for handling image and video content markers.

**Warning**  
Incorrectly formatted chat templates can result in poor model performance, unexpected outputs, or inference failures. Always test your chat template thoroughly before deploying to production.