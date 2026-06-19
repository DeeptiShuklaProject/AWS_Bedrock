

# Fine-tune Amazon Nova models with supervised fine-tuning
<a name="nova-2-sft-data-prep"></a>

Amazon Nova 2.0 SFT data uses the same Converse API format as Amazon Nova 1.0, with the addition of optional reasoning content fields. For complete format specifications, see [ReasoningContentBlock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ReasoningContentBlock.html) and [Converse API schema](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html).

**Supported features:**
+ **Input types** – Text, image, or video in user content blocks
+ **Assistant content** – Text-only responses and reasoning content
+ **Dataset composition** – Must be homogeneous. Choose one of the following: text-only turns, text \+ image turns, or text \+ video turns

**Important**  
You cannot mix images and videos within the same dataset or across different turns.

**Current limitations:**
+ **Tool usage** – Although tool usage is supported in the input format, it is not currently supported by Amazon Nova 2.0 SFT. Adding tool sections might cause your job to fail.
+ **Multimodal reasoning content** – Although the Converse format supports image-based reasoning content, this is not supported by Amazon Nova 2.0 SFT.
+ **Validation sets** – Providing a validation set might be supported through the UI but will not be supported during SFT training.

**Supported media formats:**
+ **Images** – PNG, JPEG, GIF
+ **Videos** – MOV, MKV, MP4

## Data format examples
<a name="nova-2-sft-data-examples"></a>

------
#### [ Text-only ]

This example shows a basic text-only format compatible with Amazon Nova 1.0.

```
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [
    {
      "text": "You are a digital assistant with a friendly personality"
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "text": "What country is right next to Australia?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The closest country is New Zealand"
        }
      ]
    }
  ]
}
```

------
#### [ Text with reasoning ]

This example shows text with optional reasoning content for Amazon Nova 2.0.

```
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [
    {
      "text": "You are a digital assistant with a friendly personality"
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "text": "What country is right next to Australia?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "reasoningContent": {
            "reasoningText": {
              "text": "I need to use my world knowledge of geography to answer this question"
            }
          }
        },
        {
          "text": "The closest country to Australia is New Zealand, located to the southeast across the Tasman Sea."
        }
      ]
    }
  ]
}
```

**Note**  
Currently, only `reasoningText` is supported within `reasoningContent`. Multimodal reasoning content is not yet available.

------
#### [ Image \+ text ]

This example shows how to include image input with text.

```
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [
    {
      "text": "You are a helpful assistant."
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "image": {
            "format": "jpeg",
            "source": {
              "s3Location": {
                "uri": "s3://your-bucket/your-path/your-image.jpg",
                "bucketOwner": "your-aws-account-id"
              }
            }
          }
        },
        {
          "text": "Which country is highlighted in the image?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "reasoningContent": {
            "reasoningText": {
              "text": "I will determine the highlighted country by examining its location on the map and using my geographical knowledge"
            }
          }
        },
        {
          "text": "The highlighted country is New Zealand"
        }
      ]
    }
  ]
}
```

------
#### [ Video \+ text ]

This example shows how to include video input with text.

```
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [
    {
      "text": "You are a helpful assistant."
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "video": {
            "format": "mp4",
            "source": {
              "s3Location": {
                "uri": "s3://your-bucket/your-path/your-video.mp4",
                "bucketOwner": "your-aws-account-id"
              }
            }
          }
        },
        {
          "text": "What is shown in this video?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "reasoningContent": {
            "reasoningText": {
              "text": "I will analyze the video content to identify key elements"
            }
          }
        },
        {
          "text": "The video shows a map with New Zealand highlighted"
        }
      ]
    }
  ]
}
```

------

## Reasoning content
<a name="nova-2-reasoning-modes"></a>

Reasoning content (also called chain-of-thought) captures the model's intermediate thinking steps before generating a final answer. In the `assistant` turn, use the `reasoningContent` field to include these reasoning traces.

**How loss is calculated:**
+ **With reasoning content** – Training loss includes both reasoning tokens and final output tokens
+ **Without reasoning content** – Training loss is calculated only on the final output tokens

**When to enable reasoning mode:** Set `reasoning_enabled: true` in your training configuration when you want the model to generate thinking tokens before producing final outputs or need improved performance on complex reasoning tasks. Set `reasoning_enabled: false` when you're training on straightforward tasks that don't benefit from explicit reasoning steps.

**Note**  
You can enable reasoning mode regardless of whether your training data contains reasoning content. However, including reasoning traces in your training data is recommended so the model can learn from these examples and improve reasoning quality.

**Formatting guidelines:**
+ Use plain text for reasoning content.
+ Avoid markup tags like `<thinking>` and `</thinking>` unless specifically required by your task.
+ Ensure reasoning content is clear and relevant to the problem-solving process.

**Effective reasoning content should include:**
+ Intermediate thoughts and analysis
+ Logical deductions and inference steps
+ Step-by-step problem-solving approaches
+ Explicit connections between steps and conclusions

If your dataset lacks reasoning traces, you can create them using a reasoning-capable model like Nova Premier. Provide your input-output pairs to the model and capture its reasoning process to build a reasoning-augmented dataset.

## Dataset preparation guidelines
<a name="nova-2-dataset-preparation"></a>

The following table provides guidelines for preparing your training dataset.


**Dataset preparation guidelines**  

| Guideline | Description | 
| --- | --- | 
| Size and quality |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/nova-2-sft-data-prep.html)  | 
| Diversity | Include diverse examples that do the following:[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/nova-2-sft-data-prep.html) | 
| Output formatting | Clearly specify the desired output format in assistant responses. Examples include JSON structures, tables, CSV format, or custom formats specific to your application. | 
| Multi-turn conversations |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/nova-2-sft-data-prep.html)  | 
| Quality checklist |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/nova-2-sft-data-prep.html)  | 