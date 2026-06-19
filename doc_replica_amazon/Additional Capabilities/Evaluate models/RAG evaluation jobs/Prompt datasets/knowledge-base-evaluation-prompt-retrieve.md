

# Create a prompt dataset for retrieve-only RAG evaluation jobs
<a name="knowledge-base-evaluation-prompt-retrieve"></a>

A retrieve-only evaluation jobs require a prompt dataset using JSON lines format. You can have up to 1000 prompts in your dataset.

## Prepare a dataset for a retrieve-only evaluation job where Amazon Bedrock invokes your Knowledge Base
<a name="knowledge-base-evaluation-prompt-retrieve-invoke"></a>

To create a retrieve-only evaluation job where Amazon Bedrock invokes your Knowledge Base, your prompt dataset must contain the following key-value pairs:
+ `referenceResponses` – This parent key is used to specify the ground-truth response you would expect an end-to-end RAG system to return. This parameter does not represent the expected passages or chunks you expect to be retrieved from your Knowledge Base. Specify the ground truth in the `text` key. `referenceResponses` is required if you choose the **Context coverage** metric in your evaluation job.
+ `prompt` – This parent key is used to specify the prompt (user query) that you want the RAG system to respond to.

The following is an example custom dataset that contains 6 inputs and uses the JSON line format.

```
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"Provide the prompt you want to use during inference"}}}]},"referenceResponses":[{"content":[{"text":{{"Specify a ground-truth response"}}}]}]}]}
```

The following prompt is expanded for clarity. In your actual prompt dataset each line (a prompt) must be a valid JSON object.

```
{
    "conversationTurns": [
        {
            "prompt": {
                "content": [
                    {
                        "text": "What is the recommended service interval for your product?"
                    }
                ]
            },
            "referenceResponses": [
                {
                    "content": [
                        {
                            "text": "The recommended service interval for our product is two years."
                        }
                    ]
                }
            ]
        }
    ]
}
```

## Prepare a dataset for a retrieve-only evaluation job using your own inference response data
<a name="knowledge-base-evaluation-prompt-retrieve-byoir"></a>

To create a retrieve-only evaluation job where you provide your own inference response data, your prompt dataset must contain the following:
+ `prompt` – this parent key is used to specify the prompt (user query) that you used to generate your inference response data.
+ `referenceResponses` – This parent key is used to specify the ground-truth response you would expect an end-to-end RAG system to return. This parameter does not represent the expected passages or chunks you expect to be retrieved from the knowledge base. Specify the ground truth in the `text` key. `referenceResponses` is required if you choose the **Context coverage** metric in your evaluation job.
+ `referenceContexts` (optional) – This optional parent key is used to specify the ground truth passages you would expect to be retrieved from the RAG source. You only need to include this key if you want to use it in your own custom evaluation metrics. The built-in metrics Amazon Bedrock provides don't use this property.
+ `knowledgeBaseIdentifier` – a customer-defined string identifying the RAG source used to generate the retrieval results.
+ `retrievedResults` – a JSON object with a list of retrieval results. For each result, you can supply an optional `name` and optional `metadata` specified as key-value pairs.

The following is an example custom dataset that contains 6 inputs and uses the JSON line format.

```
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":{{"The prompt you used to generate your response"}}}]},"referenceResponses":[{"content":[{"text":{{"A ground-truth response"}}}]}],"referenceContexts":[{"content":[{"text":{{"A ground truth for a received passage"}}}]}],"output":{"knowledgeBaseIdentifier":{{"A string identifying your RAG source"}},"retrievedResults":{"retrievalResults":[{"name":{{"(Optional) a name for your reference context"}},"content":{"text":{{"The output from your RAG inference"}}},"metadata":{{{"(Optional) a key for your metadata"}}:{{"(Optional) a metadata value"}}}}]}}}]}
```

The following prompt is expanded for clarity. In your actual prompt dataset each line (a prompt) must be a valid JSON object.

```
{
  "conversationTurns": [
    {
      "prompt": {
        "content": [
          {
            "text": "What is the recommended service interval for your product?"
          }
        ]
      },
      "referenceResponses": [
        {
          "content": [
            {
              "text": "The recommended service interval for our product is two years."
            }
          ]
        }
      ],
      "referenceContexts": [
        {
          "content": [
            {
              "text": "A ground truth for a received passage"
            }
          ]
        }
      ],
       "output": {
        "knowledgeBaseIdentifier": "RAG source 1",
        "retrievedResults": {
          "retrievalResults": [
            {
              "name": "(Optional) a name for your retrieval",
              "content": {
                "text": "The recommended service interval for our product is two years."
              },
              "metadata": {
                "(Optional) a key for your metadata": "(Optional) a value for your metadata"
              }
            }
          ]
        }
      }
    }
  ]
}
```