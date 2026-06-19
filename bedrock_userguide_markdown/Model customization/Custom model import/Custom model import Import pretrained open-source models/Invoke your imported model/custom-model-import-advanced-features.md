

# Advanced API features for imported models
<a name="custom-model-import-advanced-features"></a>

This page provides detailed examples of advanced features available for models imported after November 11, 2025. These capabilities include structured outputs for controlled generation, enhanced vision support for multi-image processing, log probabilities for confidence insights, and tool calling for GPT-OSS models.

## Structured Outputs
<a name="structured-outputs"></a>

Structured outputs enable controlled generation following specific formats, schemas, or patterns. This feature ensures that the model's response adheres to predefined constraints, making it ideal for applications requiring consistent data formats, API integrations, or automated processing pipelines.

Structured outputs on Custom Model Import are supported via two parameters:
+ `response_format` - Supports `json_object` and `json_schema` types
+ `structured_outputs` - Supports `json`, `regex`, `choice`, and `grammar` types

**Note**  
When using structured outputs on Custom Model Import, customers should expect performance trade-offs due to constraint validation during generation. Simple constraints like `choice` and `json_object` have minimal impact, while complex constraints like `json_schema` and `grammar` can significantly increase latency and reduce throughput. For optimal performance, use simpler constraint types when possible and keep schemas flat rather than deeply nested.

The following examples demonstrate structured outputs support across different API formats. The Pydantic model definition is:

```
from pydantic import BaseModel
from enum import Enum

class CarType(str, Enum):
    sedan = "sedan"
    suv = "SUV"
    truck = "Truck"
    coupe = "Coupe"

class CarDescription(BaseModel):
    brand: str
    model: str
    car_type: CarType
```

------
#### [ BedrockCompletion ]

BedrockCompletion supports structured outputs using the `response_format` parameter with `json_object` and `json_schema` types only.

**Example: JSON Schema**

```
payload = {
    "prompt": "Generate a JSON with the brand, model and car_type of the most iconic car from the 90's",
    "response_format": {
        "type": "json_schema",
        "json_schema": CarDescription.model_json_schema()
    }
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response:

```
{
    "generation": "{\n    \"brand\": \"Ferrari\",\n    \"model\": \"F40\",\n    \"car_type\": \"SUV\"\n  }",
    "prompt_token_count": 22,
    "generation_token_count": 30,
    "stop_reason": "stop",
    "logprobs": null
}
```

------
#### [ OpenAICompletion ]

OpenAICompletion supports both `response_format` (json\_object, json\_schema) and `structured_outputs` (json, regex, choice, grammar) parameters. Use `max_tokens` instead of `max_gen_len` to route requests to OpenAICompletion.

**Example: Structured Outputs - Choice**

```
payload = {
    "prompt": "Classify the sentiment of this sentence. Amazon Bedrock CMI is Amazing!",
    "max_tokens": 10,
    "structured_outputs": {
        "choice": ["positive", "negative"]
    }
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response:

```
{
    "id": "cmpl-01f94c4652d24870bbb4d5418a01c384",
    "object": "text_completion",
    "choices": [
        {
            "index": 0,
            "text": "positive",
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 17,
        "completion_tokens": 4
    }
}
```

------
#### [ OpenAIChatCompletion ]

OpenAIChatCompletion supports both `response_format` (json\_object, json\_schema) and `structured_outputs` (json, regex, choice, grammar) parameters.

**Example: Response Format - JSON Schema**

```
payload = {
    "messages": [
        {"role": "user", "content": "Generate a JSON with the brand, model and car_type of the most iconic car from the 90's"}
    ],
    "max_tokens": 100,
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "car-description",
            "schema": CarDescription.model_json_schema()
        }
    }
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response:

```
{
    "id": "chatcmpl-cae5a43b0a924b8eb434510cbf978a19",
    "object": "chat.completion",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "{\"brand\": \"Dodge\", \"model\": \"Viper\", \"car_type\": \"Coupe\"}"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 56,
        "completion_tokens": 23
    }
}
```

------

## Vision Support
<a name="vision-support"></a>

Vision capabilities enable processing of images alongside text inputs, with enhanced multi-image support for complex visual analysis tasks. Custom Model Import now supports up to 3 images per request, enhanced from previous single-image limitation.

**Supported API:** OpenAIChatCompletion only. All models imported after November 11, 2025 will default to this API for vision capabilities.

**Image Requirements:**
+ Base64 encoding required - Image URLs will cause request failures
+ Maximum 3 images per request
+ High resolution images significantly increase processing time and memory usage

**Warning**  
High resolution images significantly increase processing time, memory usage, and may cause timeout errors. Multiple high-resolution images compound performance impact exponentially. For optimal performance, resize images appropriately and use lower detail levels when possible.

------
#### [ OpenAIChatCompletion ]

**Example: Multi-Image Processing**

```
import json
import boto3
import base64

client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Load and encode images
with open('/path/to/car_image_1.jpg', 'rb') as f:
    image_data_1 = base64.b64encode(f.read()).decode('utf-8')

with open('/path/to/car_image_2.jpg', 'rb') as f:
    image_data_2 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that can analyze images."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Spot the difference between the two images?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data_1}"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data_2}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300,
    "temperature": 0.5
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response:

```
{
    "id": "chatcmpl-ccae8a67e62f4014a9ffcbedfff96f44",
    "object": "chat.completion",
    "created": 1763167018,
    "model": "667387627229-g6vkuhd609s4",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "There are no differences between the two images provided. They appear to be identical.",
                "refusal": null,
                "annotations": null,
                "audio": null,
                "function_call": null,
                "tool_calls": [],
                "reasoning_content": null
            },
            "logprobs": null,
            "finish_reason": "stop",
            "stop_reason": null,
            "token_ids": null
        }
    ],
    "service_tier": null,
    "system_fingerprint": null,
    "usage": {
        "prompt_tokens": 2795,
        "total_tokens": 2812,
        "completion_tokens": 17,
        "prompt_tokens_details": null
    },
    "prompt_logprobs": null,
    "prompt_token_ids": null,
    "kv_transfer_params": null
}
```

------

## Log Probabilities
<a name="log-probabilities"></a>

Log probabilities represent the likelihood of each token in a sequence, calculated as log(p) where p is the probability of a token at any position given its previous token in the context. Since log probs are additive, sequence probability equals the sum of individual token log probs, making them useful for ranking generations by average per-token scores. Custom Model Import will always return the raw logprob values for requested tokens.

Key applications include classification tasks where log probs enable custom confidence thresholds, retrieval Q&A systems that use confidence scores to reduce hallucinations, autocomplete suggestions based on token likelihood, and perplexity calculations for comparing model performance across prompts. Log probs also provide token-level analysis capabilities, allowing developers to examine alternative tokens the model considered.

**Note**  
Logprobs are not cached. For a request requiring prompt logprobs, the system will ignore the prefix cache and recompute the prefill of full prompt to generate the logprobs. This presents an obvious performance tradeoff when using logprobs.

Log probability support varies by API format:
+ BedrockCompletion - Output tokens only
+ OpenAICompletion - Prompt and output tokens
+ OpenAIChatCompletion - Prompt and output tokens

------
#### [ BedrockCompletion ]

BedrockCompletion only supports output token logprobs. This will return top 1 logprob for each output token.

```
payload = {
    "prompt": "How is the rainbow formed?",
    "max_gen_len": 10,
    "temperature": 0.5,
    "return_logprobs": True
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response (truncated):

```
{
    "generation": " A rainbow is formed when sunlight passes through water dro",
    "prompt_token_count": 7,
    "generation_token_count": 10,
    "stop_reason": "length",
    "logprobs": [
        {
            "362": -2.1413702964782715
        },
        {
            "48713": -0.8180374503135681
        },
        {
            "374": -0.09657637774944305
        },
        ...
    ]
}
```

------
#### [ OpenAIChatCompletion ]

OpenAIChatCompletion supports both prompt and output token logprobs. You can set `top_logprobs=N` and `prompt_logprobs=N` where N is an integer representing log probabilities for the N most likely tokens at each position.

```
payload = {
    "messages": [
        {
            "role": "user",
            "content": "How is the rainbow formed?"
        }
    ],
    "max_tokens": 10,
    "temperature": 0.5,
    "logprobs": True,
    "top_logprobs": 1,
    "prompt_logprobs": 1
}

response = client.invoke_model(
    modelId='your-model-arn',
    body=json.dumps(payload),
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response['body'].read())
```

Example response (truncated):

```
{
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "A rainbow is formed..."
            },
            "logprobs": {
                "content": [
                    {
                        "token": "A",
                        "logprob": -0.07903262227773666,
                        "bytes": [65],
                        "top_logprobs": [
                            {
                                "token": "A",
                                "logprob": -0.07903262227773666,
                                "bytes": [65]
                            }
                        ]
                    },
                    {
                        "token": " rainbow",
                        "logprob": -0.20187227427959442,
                        "bytes": [32, 114, 97, 105, 110, 98, 111, 119],
                        "top_logprobs": [...]
                    },
                    ...
                ]
            },
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 41,
        "completion_tokens": 10,
        "total_tokens": 51
    }
}
```

------