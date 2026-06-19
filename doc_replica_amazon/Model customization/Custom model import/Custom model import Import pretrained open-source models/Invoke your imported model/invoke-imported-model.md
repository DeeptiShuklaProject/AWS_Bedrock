

# Invoke your imported model
<a name="invoke-imported-model"></a>

The model import job can take several minutes to import your model after you send [CreateModelImportJob](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_CreateModelImportJob.html) request. You can check the status of your import job in the console or by calling the [GetModelImportJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelImportJob.html) operation and checking the `Status` field in the response. The import job is complete if the Status for the model is **Complete**. 

After your imported model is available in Amazon Bedrock, you can use the model with on demand throughput by sending [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) requests to make inference calls to the model. For more information, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md).

To interface with your imported model using the messages format, you can call the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) operations. For more information, see [Using the Converse APIUsing the Converse API (moved)](conversation-inference-call.md).

**Note**  
Converse API is not supported for Qwen2.5, Qwen2-VL, Qwen2.5-VL, and GPT-OSS models.

## Enhanced API Support: Multiple API Formats
<a name="enhanced-api-support"></a>

Starting November 17, 2025, Amazon Bedrock Custom Model Import supports comprehensive OpenAI-compatible API formats, providing flexibility in how you integrate and deploy your custom models. All models imported after November 11, 2025, will automatically benefit from these enhanced capabilities with no additional configuration required.

Custom Model Import now supports three API formats:
+ **BedrockCompletion (Text)** - Compatible with current Bedrock workflows
+ **OpenAICompletion (Text)** - OpenAI Completions Schema compatibility
+ **OpenAIChatCompletion (Text and Images)** - Full conversational Schema compatibility

These enhanced capabilities include structured outputs for enforcing JSON schemas and patterns, enhanced vision support with multi-image processing, log probabilities for model confidence insights, and tool calling capabilities for GPT-OSS models.

For detailed API reference documentation, see the official OpenAI documentation:
+ Completion: [OpenAI Completions API](https://platform.openai.com/docs/api-reference/completions)
+ ChatCompletion: [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat)

### API Format Examples
<a name="api-format-examples"></a>

The following examples demonstrate how to use each of the four supported API formats with your imported models.

------
#### [ BedrockCompletion ]

**BedrockCompletion** format is compatible with current Bedrock workflows and supports text-based inference requests.

Example request:

```
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

payload = {
    "prompt": "How is the rainbow formed?",
    "max_gen_len": 100,
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
    "generation": " – A scientific explanation\nA rainbow is a beautiful natural phenomenon that occurs when sunlight passes through water droplets in the air. It is formed through a process called refraction, which is the bending of light as it passes from one medium to another.\nHere's a step-by-step explanation of how a rainbow is formed:\n1. Sunlight enters the Earth's atmosphere: The first step in forming a rainbow is for sunlight to enter the Earth's atmosphere. This sunlight is made up of a spectrum of",
    "prompt_token_count": 7,
    "generation_token_count": 100,
    "stop_reason": "length",
    "logprobs": null
}
```

BedrockCompletion supports structured outputs using `response_format` parameter with `json_object` and `json_schema` types.

------
#### [ OpenAICompletion ]

**OpenAICompletion** format provides OpenAI Completions Schema compatibility. To use this format, include the `max_tokens` parameter instead of `max_gen_len`.

Example request:

```
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

payload = {
    "prompt": "How is the rainbow formed?",
    "max_tokens": 100,
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
    "id": "cmpl-b09d5810bd64428f8a853be71c31f912",
    "object": "text_completion",
    "created": 1763166682,
    "choices": [
        {
            "index": 0,
            "text": " The formation of a rainbow is a complex process that involves the interaction of sunlight with water droplets in the air. Here's a simplified explanation: 1. Sunlight enters the Earth's atmosphere and is refracted, or bent, as it passes through the air. 2. When sunlight encounters a water droplet, such as a cloud, mist, or fog, it is refracted again and split into its individual colors, a process known as dispersion. 3. The refracted and",
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 7,
        "total_tokens": 107,
        "completion_tokens": 100
    }
}
```

OpenAICompletion supports full structured outputs capabilities including `json`, `regex`, `choice`, and `grammar` constraints using the `structured_outputs` parameter.

------
#### [ OpenAIChatCompletion ]

**OpenAIChatCompletion** format provides full conversational Schema compatibility and supports both text and image inputs.

Example request:

```
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

payload = {
    "messages": [
        {
            "role": "user",
            "content": "How is the rainbow formed?"
        }
    ],
    "max_tokens": 100,
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
    "id": "chatcmpl-1d84ce1d3d61418e8c6d1973f87173db",
    "object": "chat.completion",
    "created": 1763166683,
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "A rainbow is a beautiful natural phenomenon that occurs when sunlight passes through water droplets in the air. The process of forming a rainbow involves several steps:\n\n1. **Sunlight**: The first requirement for a rainbow is sunlight. The sun should be shining brightly, but not directly overhead.\n2. **Water droplets**: The second requirement is water droplets in the air..."
            },
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 41,
        "completion_tokens": 100,
        "total_tokens": 141
    }
}
```

OpenAIChatCompletion supports structured outputs using both `response_format` and `structured_outputs` parameters. For vision capabilities, include images in the content array with base64-encoded image data.

**Note**  
To use ChatCompletion format, the chat template needs to be part of the `tokenizer_config.json`. Custom Model Import will not apply any default chat templates to the request.

------

You'll need the model ARN to make inference calls to your newly imported model. After the successful completion of the import job and after your imported model is active, you can get the model ARN of your imported model in the console or by sending a [ListImportedModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListImportedModels.html) request. 

When you invoke your imported model using `InvokeModel` or `InvokeModelWithStream`, your request is served within 5 minutes or you might get `ModelNotReadyException`. To understand the ModelNotReadyException, follow the steps in this next section for handling ModelNotreadyException. 

## Frequently Asked Questions
<a name="api-format-faq"></a>

**Q: What API format should I use?**

A: For maximum compatibility with various SDKs, we recommend using OpenAICompletion or OpenAIChatCompletion formats as they provide OpenAI-compatible schemas that are widely supported across different tools and libraries.

**Q: Does GPT-OSS on Amazon Bedrock Custom Model Import support the Converse API?**

A: No. GPT-OSS based custom model import models do not support the Converse API or ConverseStream API. You must use the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) API with OpenAI-compatible schemas when working with GPT-OSS based custom models.

**Q: What models support tool calling?**

A: GPT-OSS based custom models support tool calling capabilities. Tool calling enables function calling for complex workflows.

**Q: What about models imported before November 11, 2025?**

A: Models imported before November 11, 2025, continue to work as is with their existing API formats and capabilities.

**Q: What about `generation_config.json` for OpenAI-based models?**

A: It is critical that you include the correct `generation_config.json` file when importing OpenAI-based models such as GPT-OSS. You must use the updated configuration file (updated August 13, 2024) available at [https://huggingface.co/openai/gpt-oss-20b/blob/main/generation\_config.json](https://huggingface.co/openai/gpt-oss-20b/blob/main/generation_config.json). The updated configuration includes three end-of-sequence token IDs (`[200002, 199999, 200012]`), whereas older versions only included two tokens (`[200002, 199999]`). Using an outdated `generation_config.json` file will cause runtime errors during model invocation. This file is essential for proper model behavior and must be included with your OpenAI-based model imports.

## Handling ModelNotReadyException
<a name="handle-model-not-ready-exception"></a>

Amazon Bedrock Custom Model Import optimizes the hardware use by removing the models that are not active. If you try to invoke a model that has been removed, you'll get a `ModelNotReadyException`. After the model is removed and you invoke the model for the first time, Custom Model Import starts to restore the model. The restoration time depends on the on-demand fleet size and the model size.

If your `InvokeModel` or `InvokeModelWithStream` request returns `ModelNotReadyException`, follow the steps to handle the exception.

1. 

**Configure retries**

   By default, the request is automatically retried with exponential backoff. You can configure the maximum number of retries.

   The following example shows how to configure the retry. Replace {{${region-name}}}, {{${model-arn}}}, and {{10}} with your Region, model ARN, and maximum attempts.

   ```
   import json
   import boto3
   from botocore.config import Config
   
   
   REGION_NAME = {{${region-name}}}
   MODEL_ID= '{{${model-arn}}}'
   
   config = Config(
       retries={
           'total_max_attempts': {{10}}, //customizable
           'mode': 'standard'
       }
   )
   message = "Hello"
   
   
   session = boto3.session.Session()
   br_runtime = session.client(service_name = 'bedrock-runtime', 
                                    region_name=REGION_NAME, 
                                    config=config)
       
   try:
       invoke_response = br_runtime.invoke_model(modelId=MODEL_ID, 
                                               body=json.dumps({'prompt': message}), 
                                               accept="application/json", 
                                               contentType="application/json")
       invoke_response["body"] = json.loads(invoke_response["body"].read().decode("utf-8"))
       print(json.dumps(invoke_response, indent=4))
   except Exception as e:
       print(e)
       print(e.__repr__())
   ```

1. 

**Monitor response codes during retry attempts**

   Each retry attempt starts model restoration process. The restoration time depends on the availability of the on-demand fleet and the model size. Monitor the response codes while the restoration process is going on. 

   If the retries are consistently failing, continue with the next steps.

1. 

**Verify model was successfully imported**

   You can verify if the model was successfully imported by checking the status of your import job in the console or by calling the [GetModelImportJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelImportJob.html) operation. Check the `Status` field in the response. The import job is successful if the Status for the model is **Complete**. 

1. 

**Contact Support for further investigation**

   Open a ticket with Support For more information, see [Creating support cases](https://docs.aws.amazon.com//awssupport/latest/user/case-management.html).

   Include relevant details such as model ID and timestamps in the support ticket.