

# Writer Palmyra X5
<a name="model-parameters-palmyra-x5"></a>

Writer Palmyra X5 includes a suite of enterprise-ready capabilities, including advanced reasoning, tool-calling, LLM delegation, built-in RAG, code generation, structured outputs, multi-modality, and multi-lingual support.

The Writer Palmyra X5 model has the following controls:
+ Provider — Writer
+ Categories — Text generation, code generation, rich text formatting
+ Last version — v1
+ Release date — April 28th, 2025
+ Model ID — `writer.palmyra-x5-v1:0`
+ Modality — Text
+ Max tokens — Input: 1,040,000 tokens, Output: 8192 tokens
+ Language — English, Spanish, French, German, Chinese and multiple other languages
+ Deployment type — Serverless

## Palmyra X5 invocation request body field
<a name="model-parameters-palmyra-x5-request-body"></a>

When you make an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) call using a Writer model, fill the `body` field with a JSON object that conforms to the one below. Enter the prompt in the `text` field in the `text_prompts` object.

```
{
"modelId": "writer.palmyra-x5-v1:0",
"contentType": "application/json",
"accept": "application/json",
"body": "{\"messages\":[{\"role\":\"user\",\"content\":{\"text\":\"Explain quantum computing in simple terms\"}}]}"
}
```

The following table shows the minimum, maximum, and default values for the numerical parameters.


****  

| Parameter | Type | Default | Range/Validation | Description | 
| --- | --- | --- | --- | --- | 
| messages | array | Required | 1-∞ items | Chat history messages | 
| temperature | float | 1.0 | 0.0 ≤ x ≤ 2.0 | Sampling temperature | 
| top\_p | float | 1.0 | 0.0 < x ≤ 1.0 | Nucleus sampling threshold | 
| max\_tokens | int | 16 | 1 ≤ x ≤ 8192 | Maximum tokens to generate | 
| min\_tokens | int | 0 | 0 ≤ x ≤ max\_tokens | Minimum tokens before stopping | 
| stop | array | [] | ≤4 entries | Stop sequences | 
| seed | int | null | Any integer | Random seed | 
| presence\_penalty | float | 0.0 | -2.0 ≤ x ≤ 2.0 | New token presence penalty | 
| frequency\_penalty | float | 0.0 | -2.0 ≤ x ≤ 2.0 | Token frequency penalty | 

## Palmyra X5 invocation response body field
<a name="model-parameters-palmyra-x5-response-body"></a>

The response JSON for Writer Palmyra X5 uses the following format:

```
{
  "id": "chatcmpl-a689a6e150b048ca8814890d3d904d41",
  "object": "chat.completion",
  "created": 1745854231,
  "model": "writer.palmyra-x5-v1:0",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": null,
        "content": "Quantum computing harnesses quantum mechanics to process information in extraordinarily powerful ways. Unlike classical bits, which are 0 or 1, quantum bits (qubits) can exist in multiple states simultaneously through superposition. Qubits also entangle, allowing them to be interconnected in such a way that the state of one (whether it's 0 or 1) can depend on the state of another, no matter the distance between them. This combination of superposition and entanglement enables quantum computers to solve complex problems much faster than classical computers, particularly in areas like cryptography, optimization, and simulations of molecular structures. However, quantum computing is still in its early stages, facing challenges in stability and scalability.",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 43,
    "total_tokens": 186,
    "completion_tokens": 143,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null
}
```