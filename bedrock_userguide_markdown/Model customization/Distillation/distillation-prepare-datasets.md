

# Prepare your training datasets for distillation
<a name="distillation-prepare-datasets"></a>

Before you can begin a model customization job, you need to minimally prepare a training dataset. To prepare input datasets for your custom model, you create `.jsonl` files, each line of which is a JSON object corresponding to a record. The files you create must conform to the format for model distillation and model that you choose. The records in it must also conform to size requirements.

Provide the input data as prompts. Amazon Bedrock uses the input data to generate responses from the teacher model and uses the generated responses to fine-tune the student model. For more information about inputs Amazon Bedrock uses, and for choosing an option that works best for your use case, see [How Amazon Bedrock Model Distillation works](model-distillation.md#how-md-works). There are a couple options for preparing your input dataset.

**Note**  
Amazon Nova models have different requirements for distillation. For more information, see [Distilling Amazon Nova models](https://docs.aws.amazon.com/nova/latest/userguide/customize-distill.html).

## Supported modalities for distillation
<a name="distillation-supported-modalities"></a>

The models listed in [Supported models and Regions for Amazon Bedrock Model Distillation](prequisites-model-distillation.md#model-distillation-supported) support only the text-to-text modality.

## Optimize your input prompts for synthetic data generation
<a name="distillation-data-prep-prompt-optimization"></a>

During model distillation, Amazon Bedrock generates a synthetic dataset that it uses to fine tune your student model for your specific use case. For more information, see [How Amazon Bedrock Model Distillation works](model-distillation.md#how-md-works).

You can optimize the synthetic data generation process by formatting your input prompts for the use case that you want. For example, if your distilled model's use case is retrieval augmented generation (RAG), you would format your prompts differently than if you want the model to focus on agent use cases.

The following are examples for how you can format your input prompts for RAG or agent use cases.

------
#### [ RAG prompt example ]

```
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [
    {
      "text": "You are a financial analyst charged with answering questions about 10K and 10Q SEC filings. Given the context below, answer the following question."
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "text": "<context>\nDocument 1: Multiple legal actions have been filed against us as a result of the October 29, 2018 accident of Lion Air Flight 610 and the March 10, 2019 accident of Ethiopian Airlines Flight 302.\n</context>\n\n<question>Has Boeing reported any materially important ongoing legal battles from FY2022?</question>"
        }
      ]
    }
  ]
}
```

------
#### [ Agent prompt example ]

```
{
    "schemaVersion": "bedrock-conversation-2024",
    "system": [
        {
            "text": 'You are an expert in composing functions. You are given a question and a set of possible functions. Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
                    Here is a list of functions in JSON format that you can invoke.
                    [
                        {
                            "name": "lookup_weather",
                            "description: "Lookup weather to a specific location",
                            "parameters": {
                                "type": "dict",
                                "required": [
                                    "city"
                                ],
                                "properties": {
                                    "location": {
                                        "type": "string",
                                    },
                                    "date": {
                                        "type": "string",
                                    }
                                }
                            }
                        }
                    ]'
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "What's the weather tomorrow?"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
               {
                   "text": "[lookup_weather(location=\"san francisco\", date=\"tomorrow\")]"
               }
            ]
        }
    ]
}
```

------