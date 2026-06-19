

# Create a prompt using Prompt management
<a name="prompt-management-create"></a>

When you create a prompt, you have the following options:
+ Write the prompt message that serves as input for an FM to generate an output.
+ Use double curly braces to include variables (as in {{{{variable}}}}) in the prompt message that can be filled in when you call the prompt.
+ Choose a model with which to invoke the prompt or, if you plan to use the prompt with an agent, leave it unspecified. If you choose a model, you can also modify the inference configurations to use. To see inference parameters for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md).

All prompts support the following base inference parameters:
+ **maxTokens** – The maximum number of tokens to allow in the generated response. 
+ **stopSequences** – A list of stop sequences. A stop sequence is a sequence of characters that causes the model to stop generating the response. 
+ **temperature** – The likelihood of the model selecting higher-probability options while generating a response. 
+ **topP** – The percentage of most-likely candidates that the model considers for the next token.

If a model supports additional inference parameters, you can specify them as *additional fields* for your prompt. You supply the additional fields in a JSON object. The following example shows how to set `top_k`, which is available in Anthropic Claude models, but isn't a base inference parameter. 

```
{
    "top_k": 200
}
```

For information about model inference parameters, see [Inference request parameters and response fields for foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html).

Setting a base inference parameter as an additional field doesn't override the value that you set in the console.

If the model that you choose for the prompt supports the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API (for more information, see [Inference using Converse API](conversation-inference.md)), you can include the following when constructing the prompt:
+ A system prompt to provide instructions or context to the model.
+ Previous prompts (user messages) and model responses (assistant messages) as conversational history for the model to consider when generating a response for the final user message.
+ (If supported by the model) [Tools](tool-use.md) for the model to use when generating the response.
+ (If supported by the model) Use [Prompt caching](prompt-caching.md) to reduce costs by caching large or frequently used prompts. Depending on the model, you can cache system instructions, tools, and messages (user and assistant). Prompt caching creates a cache checkpoint for the prompt if your total prompt prefix meets the minimum number of tokens that the model requires. When a changed variable is encountered in a prompt, prompt caching creates a new cache checkpoint (if the number of input tokens reaches the minimum that the model requires).

To learn how to create a prompt using Prompt management, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To create a prompt**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane. Then, choose **Create prompt**.

1. Provide a name for the prompt and an optional description.

1. To encrypt your prompt with a customer managed key, select **Customize encryption settings (advanced)** in the **KMS key selection** section. If you omit this field, your prompt will be encrypted with an AWS managed key. For more information, see [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html).

1. Choose **Create prompt**. Your prompt is created and you'll be taken to the **Prompt builder** for your newly created prompt, where you can configure your prompt.

1. You can continue to the following procedure to configure your prompt or return to the prompt builder later.

**To configure your prompt**

1. If you're not already in the prompt builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Prompt management** from the left navigation pane. Then, choose a prompt in the **Prompts** section.

   1. In the **Prompt draft** section, choose **Edit in prompt builder**.

1. Use the **Prompt** pane to construct the prompt. Enter the prompt in the last **User message** box. If the model supports the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API or the [AnthropicClaude Messages API](model-parameters-anthropic-claude-messages.md), you can also include a **System prompt** and previous **User messages** and **Assistant messages** for context.

   When you write a prompt, you can include variables in double curly braces (as in {{{{variable}}}}). Each variable that you include appears in the **Test variables** section.

1. (Optional) You can modify your prompt in the following ways:
   + In the **Configurations** pane, do the following:

     1. Choose a **Generative AI resource** for running inference.
**Note**  
If you choose an agent, you can only test the prompt in the console. To learn how to test a prompt with an agent in the API, see [Test a prompt using Prompt management](prompt-management-test.md).

     1. In **Inference parameters** set the inference parameters that you want to use. 

     1. If the model supports [reasoning](inference-reasoning.md), turn on **Reasoning** to include the model's reasoning in its response. In **Reasoning tokens**, you can configure the number of reasoning tokens that the model can use. 

     1. In **Additional model request fields**, choose **Configure** to specify additional inference parameters, beyond those in **Inference parameters**. 

     1. If the model that you choose supports tools, choose **Configure tools** to use tools with the prompt.

     1. If the model that you choose supports [prompt caching](prompt-caching.md), choose one of the following options (availability varies by model):
        + **None** – No prompt caching is done.
        + **Tools** – Only tools in the prompt are cached.
        + **Tools, system instructions** – Tools and system instructions in the prompt are cached.
        + **Tools, system instructions, and messages** – Tools, system instructions, and messages (user and assistant) in the prompt are cached.
   + To compare different variants of your prompt, choose **Compare variants**. You can do the following on the comparison page:
     + To add a variant, choose the plus sign. You can add up to three variants.
     + After you specify the details of a variant, you can specify any **Test variables** and choose **Run** to test the output of the variant.
     + To delete a variant, choose the three dots and select **Remove from compare**.
     + To replace the working draft and leave the comparison mode, choose **Save as draft**. All the other variants will be deleted.
     + To leave the comparison mode, choose **Exit compare mode**.

1. You have the following options when you're finished configuring the prompt:
   + To save your prompt, choose **Save draft**. For more information about the draft version, see [Deploy a prompt to your application using versions in Prompt management](prompt-management-deploy.md).
   + To delete your prompt, choose **Delete**. For more information, see [Delete a prompt in Prompt management](prompt-management-delete.md).
   + To create a version of your prompt, choose **Create version**. For more information about prompt versioning, see [Deploy a prompt to your application using versions in Prompt management](prompt-management-deploy.md).

------
#### [ API ]

To create a prompt, send a [CreatePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreatePrompt.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

The following fields are required:


****  

| Field | Brief description | 
| --- | --- | 
| name | A name for the prompt. | 
| variants | A list of different configurations for the prompt (see below). | 
| defaultVariant | The name of the default variant. | 

Each variant in the `variants` list is a [PromptVariant](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptVariant.html) object of the following general structure:

```
{
        "name": "string",
        # modelId or genAiResource (see below)
        "templateType": "TEXT",
        "templateConfiguration": # see below,
        "inferenceConfiguration": {
            "text": {
                "maxTokens": int,
                "stopSequences": ["string", ...],
                "temperature": float,
                "topP": float
            }
        },
        "additionalModelRequestFields": {
            "key": "value",
            ...
        },
        "metadata": [
            {
                "key": "string",
                "value": "string"
            },
            ...
        ]
}
```

Fill in the fields as follows:
+ name – Enter a name for the variant.
+ Include one of these fields, depending on the model invocation resource to use:
  + modelId – To specify a [foundation model](models-supported.md) or [inference profile](cross-region-inference.md) to use with the prompt, enter its ARN or ID.
  + genAiResource – To specify an [agent](agents.md), enter its ID or ARN. The value of the `genAiResource` is a JSON object of the following format:

    ```
    {
        "genAiResource": {
        "agent": {
            "agentIdentifier": "string"
        }   
    }
    ```
**Note**  
If you include the `genAiResource` field, you can only test the prompt in the console. To test a prompt with an agent in the API, you must enter the text of the prompt directly into the `inputText` field of the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request.
+ templateType – Enter `TEXT` or `CHAT`. `CHAT` is only compatible with models that support the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API. If you want to use prompt caching, you must use the `CHAT` template type.
+ templateConfiguration – The value depends on the template type that you specified:
  + If you specified `TEXT` as the template type, the value should be a [TextPromptTemplateConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_TextPromptTemplateConfiguration.html.html) JSON object.
  + If you specified `CHAT` as the template type, the value should be a [ChatPromptTemplateConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ChatPromptTemplateConfiguration.html.html) JSON object.
+ inferenceConfiguration – The `text` field maps to a [PromptModelInferenceConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptModelInferenceConfiguration.html.html). This field contains inference parameters that are common to all models. To learn more about inference parameters, see [Influence response generation with inference parameters](inference-parameters.md).
+ additionalModelRequestFields – Use this field to specify inference parameters that are specific to the model that you're running inference with. To learn more about model-specific inference parameters, see [Inference request parameters and response fields for foundation models](model-parameters.md).
+ metadata – Metadata to associate with the prompt variant. You can append key-value pairs to the array to tag the prompt variant with metadata.

The following fields are optional:


****  

| Field | Use case | 
| --- | --- | 
| description | To provide a description for the prompt. | 
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 
| tags | To associate tags with the flow. For more information, see [Tagging Amazon Bedrock resources](tagging.md). | 

The response creates a `DRAFT` version and returns an ID and ARN that you can use as a prompt identifier for other prompt-related API requests.

------