

# Optimize a prompt
<a name="prompt-management-optimize"></a>

Amazon Bedrock offers simple prompt optimization, which performs a fast, heuristic rewrite of a single short prompt for one model. It works best for prompts of approximately 1k tokens or less. You can choose the model that you want to optimize the prompt for and then generate a revised prompt. Simple optimization does not use evaluation data or support multiple models. For evaluation-driven optimization where your evaluation steers the prompt rewriting across multiple models, see [Advanced Prompt Optimization](https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompt-optimization-how.html).

After you submit a prompt for simple optimization, Amazon Bedrock analyzes the components of the prompt. If the analysis is successful, it then rewrites the prompt. You can then copy and use the text of the optimized prompt. 

**Note**  
For best results, we recommend optimizing prompts in English.

**Topics**
+ [Supported Regions and models for prompt optimization](#prompt-management-optimize-supported)
+ [Submit a prompt for optimization](#prompt-management-optimize-submit)

## Supported Regions and models for prompt optimization
<a name="prompt-management-optimize-supported"></a>

The following table shows model support for prompt optimization:


| Provider | Model | Model ID | Single-region model support | 
| --- | --- | --- | --- | 
| Amazon | Nova Lite | amazon.nova-lite-v1:0 | ap-southeast-2<br />eu-west-2<br />us-east-1 | 
| Amazon | Nova Micro | amazon.nova-micro-v1:0 | ap-southeast-2<br />eu-west-2<br />us-east-1 | 
| Amazon | Nova Premier | amazon.nova-premier-v1:0 |  | 
| Amazon | Nova Pro | amazon.nova-pro-v1:0 | ap-southeast-2<br />eu-west-2<br />us-east-1 | 
| Anthropic | Claude 3 Haiku | anthropic.claude-3-haiku-20240307-v1:0 | ap-south-1<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3 Opus | anthropic.claude-3-opus-20240229-v1:0 |  | 
| Anthropic | Claude 3 Sonnet | anthropic.claude-3-sonnet-20240229-v1:0 | ap-south-1<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3.5 Haiku | anthropic.claude-3-5-haiku-20241022-v1:0 | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet | anthropic.claude-3-5-sonnet-20240620-v1:0 | eu-central-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3.5 Sonnet v2 | anthropic.claude-3-5-sonnet-20241022-v2:0 | ap-southeast-2<br />us-west-2 | 
| Anthropic | Claude 3.7 Sonnet | anthropic.claude-3-7-sonnet-20250219-v1:0 | eu-west-2 | 
| Anthropic | Claude Opus 4 | anthropic.claude-opus-4-20250514-v1:0 |  | 
| Anthropic | Claude Sonnet 4 | anthropic.claude-sonnet-4-20250514-v1:0 |  | 
| DeepSeek | DeepSeek-R1 | deepseek.r1-v1:0 |  | 
| Meta | Llama 3 70B Instruct | meta.llama3-70b-instruct-v1:0 | ap-south-1<br />ca-central-1<br />eu-west-2<br />us-east-1<br />us-west-2 | 
| Meta | Llama 3.1 70B Instruct | meta.llama3-1-70b-instruct-v1:0 | us-west-2 | 
| Meta | Llama 3.2 11B Instruct | meta.llama3-2-11b-instruct-v1:0 |  | 
| Meta | Llama 3.3 70B Instruct | meta.llama3-3-70b-instruct-v1:0 |  | 
| Meta | Llama 4 Maverick 17B Instruct | meta.llama4-maverick-17b-instruct-v1:0 |  | 
| Meta | Llama 4 Scout 17B Instruct | meta.llama4-scout-17b-instruct-v1:0 |  | 
| Mistral AI | Mistral Large (24.02) | mistral.mistral-large-2402-v1:0 | ap-south-1<br />ap-southeast-2<br />ca-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Mistral AI | Mistral Large (24.07) | mistral.mistral-large-2407-v1:0 | us-west-2 | 

## Submit a prompt for optimization
<a name="prompt-management-optimize-submit"></a>

To learn how to optimize a prompt, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

You can optimize a prompt through using a playground or Prompt management in the AWS Management Console. You must select a model before you can optimize a prompt. The prompt is optimized for the model that you choose.

**To optimize a prompt in a playground**

1. To learn how to write a prompt in an Amazon Bedrock playground, follow the steps at [Generate responses in the console using playgrounds](playgrounds.md).

1. After you write a prompt and select a model, choose the wand icon (![Sparkle icon representing cleaning or refreshing functionality.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/wand.png)). The **Optimize prompt** dialog box opens, and Amazon Bedrock begins optimizing your prompt.

1. When Amazon Bedrock finishes analyzing and optimizing your prompt, you can compare your original prompt side by side with the optimized prompt in the dialog box.

1. To replace your prompt with the optimized prompt in the playground, choose **Use optimized prompt**. To keep your original prompt, choose **Cancel**.

1. To submit the prompt and generate a response, choose **Run**.

**To optimize a prompt in Prompt management**

1. To learn how to write a prompt using Prompt management, follow the steps at [Create a prompt using Prompt management](prompt-management-create.md).

1. After you write a prompt and select a model, choose **(![Sparkle icon representing cleaning or refreshing functionality.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/wand.png)) Optimize** at the top of the **Prompt** box.

1. When Amazon Bedrock finishes analyzing and optimizing your prompt, your optimized prompt is displayed as a variant side by side with the original prompt.

1. To use the optimized prompt instead of your original one, select **Replace original prompt**. To keep your original prompt, choose **Exit comparison** and choose to save the original prompt.
**Note**  
If you have 3 prompts in the comparison view and try to optimize another prompt, you are asked to override and replace either the original prompt or one of the variants.

1. To submit the prompt and generate a response, choose **Run**.

------
#### [ API ]

To optimize a prompt, send an [OptimizePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OptimizePrompt.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). Provide the prompt to optimize in the `input` object and specify the model to optimize for in the `targetModelId` field.

The response stream returns the following events:

1. [analyzePromptEvent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AnalyzePromptEvent.html) – Appears when the prompt is finished being analyzed. Contains a message describing the analysis of the prompt.

1. [optimizedPromptEvent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_OptimizedPromptEvent.html) – Appears when the prompt has finished being rewritten. Contains the optimized prompt.

Run the following code sample to optimize a prompt:

```
import boto3

# Set values here
TARGET_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0" # Model to optimize for. For model IDs, see https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
PROMPT = "Please summarize this text: " # Prompt to optimize

def get_input(prompt):
    return {
        "textPrompt": {
            "text": prompt
        }
    }
 
def handle_response_stream(response):
    try:
        event_stream = response['optimizedPrompt']
        for event in event_stream:
            if 'optimizedPromptEvent' in event:
                print("========================== OPTIMIZED PROMPT ======================\n")
                optimized_prompt = event['optimizedPromptEvent']
                print(optimized_prompt)
            else:
                print("========================= ANALYZE PROMPT =======================\n")
                analyze_prompt = event['analyzePromptEvent']
                print(analyze_prompt)
    except Exception as e:
        raise e
 
 
if __name__ == '__main__':
    client = boto3.client('bedrock-agent-runtime')
    try:
        response = client.optimize_prompt(
            input=get_input(PROMPT),
            targetModelId=TARGET_MODEL_ID
        )
        print("Request ID:", response.get("ResponseMetadata").get("RequestId"))
        print("========================== INPUT PROMPT ======================\n")
        print(PROMPT)
        handle_response_stream(response)
    except Exception as e:
        raise e
```

------