# Nishu @Work

Welcome to your personal notes workspace! 

You can add, edit, or organize your custom notes as markdown (`.md`) files inside the `doc_replica_notes/` folder on your disk.

---

## 1. Live Model Parameter Configurator
Adjust the temperature and top-p values below to see how the generated request payload dynamically changes.

```widget:model-param-tester
{
  "modelId": "anthropic.claude-3-sonnet",
  "temperature": 0.7,
  "topP": 0.9
}
```

---

## 2. Interactive Python Code Console
Test python code snippet execution locally. Try modifying the print statement below and clicking "Run Snippet":

```widget:code-playground
import sys
print(f"Hello from Python {sys.version}!")
print("Local files in notes directory:")
import os
print(os.listdir("."))
```

---

## 3. Local Bedrock API Playground
Run actual requests to Amazon Bedrock models using your local AWS profile credentials:

```widget:api-playground
{
  "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
  "prompt": "List 3 features of Amazon Bedrock.",
  "temperature": 0.5,
  "maxTokens": 300
}
```
