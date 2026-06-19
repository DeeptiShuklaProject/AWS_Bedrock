

# Create a prompt dataset for a model evaluation job that uses a model as judge
<a name="model-evaluation-prompt-datasets-judge"></a>

To create a model evaluation job that uses a model as judge you must specify a prompt dataset. This prompt dataset uses the same format as automatic model evaluation jobs and is used during inference with the models you select to evaluate.

If you want to evaluate non-Amazon Bedrock models using responses that you've already generated, include them in the prompt dataset as described in [Prepare a dataset for an evaluation job using your own inference response data](#model-evaluation-prompt-datasets-judge-byoir). When you provide your own inference response data, Amazon Bedrock skips the model-invoke step and performs the evaluation job with the data you provide.

Custom prompt datasets must be stored in Amazon S3, and use the JSON line format and `.jsonl` file extension. Each line must be a valid JSON object. There can be up to 1000 prompts in your dataset per evaluation job.

CORS configuration is not required for LLM-as-a-judge evaluation jobs. For human-based evaluation jobs, CORS is required on the S3 output bucket. To learn more, see [Required Cross Origin Resource Sharing (CORS) permissions on S3 buckets](model-evaluation-security-cors.md). 

## Prepare a dataset for an evaluation job where Amazon Bedrock invokes models for you
<a name="model-evaluation-prompt-datasets-judge-invoke"></a>

To run an evaluation job where Amazon Bedrock invokes the models for you, create a prompt dataset containing the following key-value pairs:
+ `prompt` – the prompt you want the models to respond to.
+ `referenceResponse` – (optional) the ground truth response.
+ `category`– (optional) generates evaluation scores reported for each category. 

**Note**  
If you choose to supply a ground truth response (`referenceResponse)`, Amazon Bedrock will use this parameter when calculating the **Completeness** (`Builtin.Completeness`) and **Correctness** (`Builtin.Correctness`) metrics. You can also use these metrics without supplying a ground truth response. To see the judge prompts for both of these scenarios, refer to the section for your chosen judge model in [Built-in metric evaluator prompts for model-as-a-judge evaluation jobs](model-evaluation-type-judge-prompt.md).

The following is an example custom dataset that contains 6 inputs and uses the JSON line format.

```
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
{"prompt":"{{Provide the prompt you want the model to use during inference}}","category":"{{(Optional) Specify an optional category}}","referenceResponse":"{{(Optional) Specify a ground truth response}}."}
```

The following example is a single entry expanded for clarity. In your actual prompt dataset each line must be a valid JSON object.

```
{
  "prompt": "What is high intensity interval training?",
  "category": "Fitness",
  "referenceResponse": "High-Intensity Interval Training (HIIT) is a cardiovascular exercise approach that involves short, intense bursts of exercise followed by brief recovery or rest periods."
}
```

## Prepare a dataset for an evaluation job using your own inference response data
<a name="model-evaluation-prompt-datasets-judge-byoir"></a>

To run an evaluation job using responses you've already generated, create a prompt dataset containing the following key-value pairs:
+ `prompt` – the prompt your models used to generate the responses.
+ `referenceResponse` – (optional) the ground truth response.
+ `category`– (optional) generates evaluation scores reported for each category. 
+ `modelResponses` – the response from your own inference that you want Amazon Bedrock to evaluate. Evaluation jobs that use a model as a judge support only one model response for each prompt, defined using the following keys:
  + `response` – a string containing the response from your model inference.
  + `modelIdentifier` – a string identifying the model that generated the response. You may use only one unique `modelIdentifier` in an evaluation job, and each prompt in your dataset must use this identifier.

**Note**  
If you choose to supply a ground truth response (`referenceResponse)`, Amazon Bedrock will use this parameter when calculating the **Completeness** (`Builtin.Completeness`) and **Correctness** (`Builtin.Correctness`) metrics. You can also use these metrics without supplying a ground truth response. To see the judge prompts for both of these scenarios, refer to the section for your chosen judge model in [Built-in metric evaluator prompts for model-as-a-judge evaluation jobs](model-evaluation-type-judge-prompt.md).

The following is a custom example dataset with 6 inputs in JSON line format.

```
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
{"prompt":{{"The prompt you used to generate the model response"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your model generated"}},"modelIdentifier":{{"A string identifying your model"}}}]}
```

The following example shows a single entry in a prompt dataset expanded for clarity.

```
{
    "prompt": "What is high intensity interval training?",
    "referenceResponse": "High-Intensity Interval Training (HIIT) is a cardiovascular exercise approach that involves short, intense bursts of exercise followed by brief recovery or rest periods.",
    "category": "Fitness",
     "modelResponses": [
        {
            "response": "High intensity interval training (HIIT) is a workout strategy that alternates between short bursts of intense, maximum-effort exercise and brief recovery periods, designed to maximize calorie burn and improve cardiovascular fitness.",
            "modelIdentifier": "my_model"
        }
    ]
}
```