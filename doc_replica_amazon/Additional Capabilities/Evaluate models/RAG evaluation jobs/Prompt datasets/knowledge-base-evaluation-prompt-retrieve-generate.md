

# Creating a prompt dataset for retrieve-and-generate RAG evaluation jobs
<a name="knowledge-base-evaluation-prompt-retrieve-generate"></a>

A retrieve-and-generate evaluation jobs require a prompt dataset using JSON lines format. You can have up to 1000 prompts in your dataset

## Prepare a dataset for a retrieve-and-generate evaluation job where Amazon Bedrock invokes your Knowledge Base
<a name="knowledge-base-evaluation-prompt-retrieve-generate-invoke"></a>

To create a retrieve-only evaluation job where Amazon Bedrock invokes your Knowledge Base, your prompt dataset must contain the following key-value pairs:
+ `referenceResponses` – This parent key is used to specify the ground truth response you expect the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) would return. Specify the ground truth in the `text` key. `referenceResponses` is required if you choose the **Context coverage** metric in your evaluation job.
+ `prompt` – This parent key is used to specify the prompt (user query) that you want the model to respond to while the evaluation job is running.

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

## Prepare a dataset for a retrieve-and-generate evaluation job using your own inference response data
<a name="knowledge-base-evaluation-prompt-retrieve-generate-byoir"></a>

To create a retrieve-and-generate evaluation job where you provide your own inference response data, your prompt dataset is a list of conversation turns and contains the following for each turn. You can only evaluate one RAG source per job.
+ `prompt` – The prompt you supplied to your model to generate the results.
+ `referenceResponses` – This parent key is used to specify the ground-truth response you would expect for the final output from your LLM after it has ingested the retrieval results and the input query.
+ `referenceContexts` (optional) – This optional parent key is used to specify the ground truth passages you would expect to be retrieved from the RAG source. You only need to include this key if you want to use it in your own custom evaluation metrics. The built-in metrics Amazon Bedrock provides don't use this property.
+ `output` – the output from your RAG source, comprising the following:
  + `text` – The final output from the LLM in your RAG system.
  + `retrievedPassages` – This parent key is used to specify the content your RAG source retrieved.

Your `output` data must also include the string `knowledgeBaseIdentifier` that defines the RAG source you used to generate the inference responses. You can also include an optional `modelIdentifier` string that identifies the LLM you used. For the `retrievalResults` and `retrievedReferences`, you can supply optional names and metadata.

The following is an example custom dataset that contains 6 inputs and uses the JSON line format.

```
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
{"conversationTurns":[{"prompt":{"content":[{"text":"Provide the prompt you used to generate the response"}]},"referenceResponses":[{"content":[{"text":"A ground truth for the final response generated by the LLM"}]}],"referenceContexts":[{"content":[{"text":"A ground truth for a received passage"}]}],"output":{"text":"The output of the LLM","modelIdentifier":"(Optional) a string identifying your model","knowledgeBaseIdentifier":"A string identifying your RAG source","retrievedPassages":{"retrievalResults":[{"name":"(Optional) a name for your retrieval","content":{"text":"The retrieved content"},"metadata":{"(Optional) a key for your metadata":"(Optional) a value for your metadata"}}]}}}]}
```

The following shows the prompt dataset format expanded for clarity. In your actual prompt dataset each line (a prompt) must be a valid JSON object.

```
{
    "conversationTurns": [
        {
            "prompt": {
                "content": [
                    {
                        "text": "Provide the prompt you used to generate the responses"
                    }
                ]
            },
            "referenceResponses": [
                {
                    "content": [
                        {
                            "text": "A ground truth for the final response generated by the LLM"
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
                "text": "The output of the LLM",
                "modelIdentifier": "(Optional) a string identifying your model",
                "knowledgeBaseIdentifier": "A string identifying your RAG source",
                "retrievedPassages": {
                    "retrievalResults": [
                        {
                            "name": "(Optional) a name for your retrieval",
                            "content": {
                                "text": "The retrieved content"
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