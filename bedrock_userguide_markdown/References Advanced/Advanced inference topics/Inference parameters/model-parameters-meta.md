

# Meta Llama models
<a name="model-parameters-meta"></a>

This section describes the request parameters and response fields for Meta Llama models. Use this information to make inference calls to Meta Llama models with the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. This section also includes Python code examples that shows how to call Meta Llama models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md). Some models also work with the [Converse API](conversation-inference.md). To check if a specific Meta Llama model supports a feature, see [models at a glance](model-cards.md). For more code examples, see [Code examples for Amazon Bedrock using AWS SDKs](service_code_examples.md).

Foundation models in Amazon Bedrock support input and output modalities, which vary from model to model. To check the modalities that Meta Llama models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which Amazon Bedrock features the Meta Llama models support, see [Supported foundation models in Amazon Bedrock](models-supported.md). To check which AWS Regions that Meta Llama models are available in, see [Supported foundation models in Amazon Bedrock](models-supported.md).

When you make inference calls with Meta Llama models, you include a prompt for the model. For general information about creating prompts for the models that Amazon Bedrock supports, see [Prompt engineering concepts](prompt-engineering-guidelines.md). For Meta Llama specific prompt information, see the [Meta Llama prompt engineering guide](https://ai.meta.com/llama/get-started/#prompting).

**Note**  
Llama 3.2 Instruct and Llama 3.3 Instruct models use geofencing. This means that these models cannot be used outside the AWS Regions available for these models listed in the Regions table.

This section provides information for using the following models from Meta.
+ Llama 3 Instruct
+ Llama 3.1 Instruct
+ Llama 3.2 Instruct
+ Llama 3.3 Instruct
+ Llama 4 Instruct

**Topics**
+ [Request and response](#model-parameters-meta-request-response)
+ [Example code](#api-inference-examples-meta-llama)

## Request and response
<a name="model-parameters-meta-request-response"></a>

The request body is passed in the `body` field of a request to [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html).

**Note**  
You can't use the [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) (streaming) operations with Llama 4 Instruct.

------
#### [ Request ]

The Llama 3 Instruct, Llama 3.1 Instruct, Llama 3.2 Instruct, and Llama 4 Instruct models have the following inference parameters: 

```
{
    "prompt": string,
    "temperature": float,
    "top_p": float,
    "max_gen_len": int
}
```

NOTE: Llama 3.2 and later models adds `images` to the request structure, which is a list of strings. Example: `images: Optional[List[str]]` 

The following are required parameters:
+  **prompt** – (Required) The prompt that you want to pass to the model. For optimal results, format the conversation with the following template.

  ```
  <|begin_of_text|><|start_header_id|>user<|end_header_id|>
  
  What can you help me with?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
  ```

  **Example template with system prompt**

  The following is an example prompt that includes a system prompt.

  ```
  <|begin_of_text|><|start_header_id|>system<|end_header_id|>
  
  You are a helpful AI assistant for travel tips and recommendations<|eot_id|><|start_header_id|>user<|end_header_id|>
  
  What can you help me with?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
  ```

  **Multi-turn conversation example**

  The following is an example prompt of a multi-turn conversation.

  ```
  <|begin_of_text|><|start_header_id|>user<|end_header_id|>
  
  What is the capital of France?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
  
  The capital of France is Paris!<|eot_id|><|start_header_id|>user<|end_header_id|>
  
  What is the weather like in Paris?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
  ```

  **Example template with system prompt**

  For more information, see [Meta Llama 3](https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3).

The following are optional parameters:
+ **temperature** – Use a lower value to decrease randomness in the response.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html)
+ **top\_p** – Use a lower value to ignore less probable options. Set to 1.0 to disable.    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html)
+ **max\_gen\_len** – Specify the maximum number of tokens to use in the generated response. The model truncates the response once the generated text exceeds `max_gen_len`.     
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html)

------
#### [ Response ]

The Llama 3 Instruct models return the following fields for a text completion inference call. 

```
{
    "generation": "\n\n{{<response>}}",
    "prompt_token_count": int,
    "generation_token_count": int,
    "stop_reason" : string
}
```

More information about each field is provided below.
+ **generation** – The generated text.
+ **prompt\_token\_count** – The number of tokens in the prompt.
+ **generation\_token\_count** – The number of tokens in the generated text.
+ **stop\_reason** – The reason why the response stopped generating text. Possible values are:
  + **stop** – The model has finished generating text for the input prompt.
  + **length** – The length of the tokens for the generated text exceeds the value of `max_gen_len` in the call to `InvokeModel` (`InvokeModelWithResponseStream`, if you are streaming output). The response is truncated to `max_gen_len` tokens. Consider increasing the value of `max_gen_len` and trying again.

------

## Example code
<a name="api-inference-examples-meta-llama"></a>

This example shows how to call the *Llama 3 Instruct* model.

```
# Use the native inference API to send a text message to Meta Llama 3.

import boto3
import json

from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID, e.g., Llama 3 70b Instruct.
model_id = "meta.llama3-70b-instruct-v1:0"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Embed the prompt in Llama 3's instruction format.
formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

# Format the request payload using the model's native structure.
native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.5,
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["generation"]
print(response_text)
```

This example shows how to control the generation length using Llama 3 Instruct models. For detailed responses or summaries, adjust `max\_gen\_len` and include specific instructions in your prompt.