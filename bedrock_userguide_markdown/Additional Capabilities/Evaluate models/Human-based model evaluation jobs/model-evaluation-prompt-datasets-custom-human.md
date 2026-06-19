

# Create a custom prompt dataset for a model evaluation job that uses human workers
<a name="model-evaluation-prompt-datasets-custom-human"></a>

To create a model evaluation job that uses human workers you must specify a custom prompt dataset. These prompts are then used during inference with the models you select to evaluate. 

If you want to evaluate non-Amazon Bedrock models using responses that you've already generated, include them in the prompt dataset as described in [Perform an evaluation job using your own inference response data](#model-evaluation-prompt-datasets-custom-human-byoir). When you provide your own inference response data, Amazon Bedrock skips the model-invoke step and performs the evaluation job with the data you provide. 

Custom prompt datasets must be stored in Amazon S3, and use the JSON line format and use the `.jsonl` file extension. Each line must be a valid JSON object. There can be up to 1000 prompts in your dataset per automatic evaluation job.

For human-based evaluation jobs created using the console, you must configure Cross Origin Resource Sharing (CORS) on the S3 output bucket. This is required to display prompts and inference results to human annotators in the annotation portal. To learn more about the required CORS permissions, see [Required Cross Origin Resource Sharing (CORS) permissions on S3 buckets](model-evaluation-security-cors.md). 

## Perform an evaluation job where Amazon Bedrock invokes a model for you
<a name="model-evaluation-prompt-datasets-custom-human-invoke"></a>

To run an evaluation job where Amazon Bedrock invokes the models for you, provide a prompt dataset containing the following key-value pairs:
+ `prompt` – the prompt you want the models to respond to.
+ `referenceResponse` – (optional) a ground truth response that your workers can reference during the evaluation.
+ `category`– (optional) a key that you can use to filter results when reviewing them in the model evaluation report card.

In the worker UI, what you specify for `prompt` and `referenceResponse` are visible to your human workers.

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

## Perform an evaluation job using your own inference response data
<a name="model-evaluation-prompt-datasets-custom-human-byoir"></a>

To run an evaluation job using responses you've already generated, you provide a prompt dataset containing the following key-value pairs:
+ `prompt` – the prompt that your models used to generate the responses.
+ `referenceResponse` – (optional) a ground truth response that your workers can reference during the evaluation.
+ `category`– (optional) a key that you can use to filter results when reviewing them in the model evaluation report card.
+ `modelResponses` – the responses from your own inference that you want to evaluate. You can provide either one or two entries with the following properties in the `modelResponses` list.
  + `response` – a string containing the response from your model inference.
  + `modelIdentifier` – a string identifying the model that generated the responses.

Every line in your prompt dataset must contain the same number of responses (either one or two). Additionally, you must specify the same model identifier or identifiers in each line and may not use more than 2 unique values for `modelIdentifier` in a single dataset.

The following is a custom example dataset with 6 inputs in JSON line format.

```
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
{"prompt":{{"The prompt you used to generate the model responses"}},"referenceResponse":{{"(Optional) a ground truth response"}},"category":{{"(Optional) a category for the prompt"}},"modelResponses":[{"response":{{"The response your first model generated"}},"modelIdentifier":{{"A string identifying your first model"}}},{"response":{{"The response your second model generated"}},"modelIdentifier":{{"A string identifying your second model"}}}]}
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
            "modelIdentifier": "Model1"
        },
        {
            "response": "High-intensity interval training (HIIT) is a cardiovascular exercise strategy that alternates short bursts of intense, anaerobic exercise with less intense recovery periods, designed to maximize calorie burn, improve fitness, and boost metabolic rate.",
            "modelIdentifier": "Model2"
        }
    ]
}
```