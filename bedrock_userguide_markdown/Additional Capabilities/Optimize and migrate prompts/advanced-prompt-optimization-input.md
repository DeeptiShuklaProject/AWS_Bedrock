

# Prepare your input dataset
<a name="advanced-prompt-optimization-input"></a>

**Note**  
Fully working examples and notebooks are available in the [Amazon Bedrock Samples GitHub](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/advanced-prompt-optimization).

## File format
<a name="advanced-prompt-optimization-input-format"></a>

The input file uses JSONL format: one JSON object per line. Each line represents one prompt template to optimize and its associated fields. You provide one input file per job.

## Schema reference
<a name="advanced-prompt-optimization-input-schema"></a>

In this prompt dataset, you will also choose the evaluation method to steer the optimization. For more information about choosing an evaluation method, see [Define evaluation methods](advanced-prompt-optimization-evaluation.md).

```
{
    "version": "bedrock-2026-05-14",
    "templateId": "string",
    "promptTemplate": "string",
    "steeringCriteria": ["string"],
    "customEvaluationMetricLabel": "string",
    "customLLMJConfig": {
        "customLLMJPrompt": "string",
        "customLLMJModelId": "string"
    },
    "evaluationMetricLambdaArn": "string",
    "evaluationSamples": [
        {
            "inputVariables": [
                {"variableName1": "string"}
            ],
            "referenceResponse": "string",
            "inputVariablesMultimodal": [
                {
                    "Arbitrary_Name": {
                        "type": "string",
                        "s3Uri": "string"
                    }
                }
            ]
        }
    ]
}
```

### Field descriptions
<a name="advanced-prompt-optimization-input-fields"></a>


| \# | Field | Type | Required | Description | 
| --- | --- | --- | --- | --- | 
| 1 | version | string | Yes | Fixed value: "bedrock-2026-05-14". | 
| 2 | templateId | string | Yes | Unique identifier for this prompt template. Used to correlate input and output. | 
| 3 | promptTemplate | string | Yes | The prompt template to optimize. Use {{variableName}} syntax for variable placeholders. | 
| 4 | steeringCriteria | list of string | No | High-level optimization criteria (for example, ["PROFESSIONAL"]). | 
| 5 | customEvaluationMetricLabel | string | Yes (if customLLMJConfig or evaluationMetricLambdaArn is used) | Name for your evaluation metric. | 
| 6 | customLLMJConfig | object | No | Custom LLM-as-Judge configuration. | 
| 7 | customLLMJConfig.customLLMJPrompt | string | Yes (if customLLMJConfig present) | The judge prompt used to evaluate responses. Use {{prompt}}, {{response}}, {{referenceResponse}} as placeholders. | 
| 8 | customLLMJConfig.customLLMJModelId | string | Yes (if customLLMJConfig present) | Bedrock model ID for the judge model. | 
| 9 | evaluationMetricLambdaArn | string | No | ARN of a Lambda function for custom evaluation. | 
| 10 | evaluationSamples | list | Yes | Evaluation samples with input variables and reference responses. | 
| 11 | evaluationSamples[].inputVariables | list of objects | Yes (if not using inputVariablesMultimodal) | Single-key objects matching {{variableName}} placeholders. At least one of inputVariables or inputVariablesMultimodal must be present per sample. | 
| 12 | evaluationSamples[].referenceResponse | string | No | Optional ground-truth reference response. Recommended for best optimization results. | 
| 13 | evaluationSamples[].inputVariablesMultimodal | list of objects | Yes (if not using inputVariables) | Multimodal file inputs. At least one of inputVariables or inputVariablesMultimodal must be present per sample. | 
| 14 | evaluationSamples[].inputVariablesMultimodal[].Arbitrary\_Name | object | Yes (if multimodal present) | Name your multimodal variable. This is an arbitrary user-chosen name. | 
| 15 | evaluationSamples[].inputVariablesMultimodal[].Arbitrary\_Name.type | string | Yes (if multimodal present) | "IMAGE" or "PDF". IMAGE accepts png and jpeg. | 
| 16 | evaluationSamples[].inputVariablesMultimodal[].Arbitrary\_Name.s3Uri | string | Yes (if multimodal present) | S3 URI path to the multimodal file. | 

## Required fields
<a name="advanced-prompt-optimization-input-required"></a>
+ `version`: fixed value `"bedrock-2026-05-14"`
+ `templateId`: unique string identifier for this prompt template
+ `promptTemplate`: the prompt to optimize, using `{{variableName}}` for placeholders
+ `evaluationSamples`: array of 1 to 100 samples

## Placeholder variables
<a name="advanced-prompt-optimization-input-variables"></a>

Use `{{variableName}}` syntax (double curly brackets) for placeholders in your prompt template. The keys in `inputVariables` must exactly match the placeholder names. Each key must be in its own object in the list. Maximum of 20 text placeholder variables per template. Placeholder variables should not be used to point to an S3 location of a multimodal file. The placeholder variables are for text only. If you have multimodal files, they will be sent to the model in the payload along with the text prompt.

## Evaluation samples
<a name="advanced-prompt-optimization-input-samples"></a>

Provide `inputVariables` as a list of single-key objects: `[{"variable1": "value1"}, {"variable2": "value2"}]`. Do NOT put multiple keys in one object. Optionally provide `referenceResponse` as the ground truth answer for better optimization results. For multimodal inputs, use the `inputVariablesMultimodal` array with `Arbitrary_Name` objects. Multimodal files are sent to the model in the payload along with the text prompt. Supported types are IMAGE (png, jpeg) and PDF, with a maximum of 2 multimodal files per sample. Multimodal inputs (images and PDFs) are sent in the payload to the model along with the prompt but should not be referenced in a double curly bracket `{{placeholder}}` variable.

## Evaluation strategy
<a name="advanced-prompt-optimization-input-strategy"></a>

Pick ONE evaluation method per template, or omit all optional evaluation fields for the system default (which combines accuracy, answer completeness, and a subjective writing style evaluation). We recommend you define your own evaluation method for the best results. You may use different methods across templates in the same job. See [Define evaluation methods](advanced-prompt-optimization-evaluation.md) for details.

## Limits
<a name="advanced-prompt-optimization-input-limits"></a>

For the full list of quotas, see [Supported Regions, models, and quotas](advanced-prompt-optimization-quotas.md). Key limits for input file preparation:
+ Maximum 10 templates per job
+ Maximum 100 evaluation samples per template
+ Maximum 5 models per job
+ Maximum 20 text variables per template
+ Maximum 2 multimodal files per sample
+ Maximum 5 steering criteria per template

## Common mistakes
<a name="advanced-prompt-optimization-input-mistakes"></a>
+ Providing both `steeringCriteria` AND `customLLMJConfig`/`evaluationMetricLambdaArn` = ValidationException
+ Missing `customEvaluationMetricLabel` when using LLMJ or `evaluationMetricLambdaArn` = ValidationException
+ Multiple keys in one `inputVariables` object = silent failure
+ Using single curly brackets like `{variable}` instead of double curly brackets like `{{variable}}`
+ The `inputVariables` keys must match the `{{variableName}}` placeholders in the `promptTemplate`
+ Allowed LLMJ models: anthropic.claude-opus-4-6-v1, anthropic.claude-sonnet-4-5-20250929-v1:0, anthropic.claude-sonnet-4-6

## Use multimodal inputs
<a name="advanced-prompt-optimization-input-multimodal"></a>

**Supported file types:** IMAGE (png, jpeg) and PDF.

**Tip**  
To use GIF or WebP images and include all frames in the optimization, break the images down into individual frames, convert them to png or jpeg, and include them in sequential order in your evaluation samples.

**How to include:** Use the `inputVariablesMultimodal` array with `Arbitrary_Name` objects containing `type` and `s3Uri`.

**Limits:** Maximum 2 multimodal files per evaluation sample. You can mix and match so that you have up to 20 text variables and also 2 multimodal files per evaluation sample record.

**Mixing text and multimodal:** You can have both `inputVariables` (text) and `inputVariablesMultimodal` in the same sample. Double curly bracket `{{placeholders}}` are reserved for plaintext only. You cannot reference multimodal files via placeholders. Placeholder variables should not be used to point to an S3 location of a multimodal file. If you have multimodal files, they will be sent to the model in the payload along with the text prompt.

## Dataset tips
<a name="advanced-prompt-optimization-input-dataset-tips"></a>
+ **Mix easy and hard examples** — match what you see in the real world. All-easy data won't push the prompt to improve; all-hard data leaves nothing to learn from.
+ **Cover the cases you care about** — the system generalizes beyond what it sees, but a representative data distribution helps it generalize better to real-world inputs.
+ **After prompt optimization, test on data the optimizer hasn't seen with a held-out dataset** — confirms the gains are real and not just memorized.

## Examples
<a name="advanced-prompt-optimization-input-examples"></a>

### Example 1: Single template, multiple variables, single evaluation sample, steering criteria
<a name="advanced-prompt-optimization-input-ex1"></a>

```
{
    "version": "bedrock-2026-05-14",
    "templateId": "customer-support-v1",
    "promptTemplate": "You are a customer support agent.\n\nProduct info:\n{{productInfo}}\n\nQuestion:\n{{customerQuestion}}\n\nProvide a helpful response.",
    "steeringCriteria": ["PROFESSIONAL"],
    "evaluationSamples": [{
        "inputVariables": [{"productInfo": "Product: Sony WH-1000XM5. Battery: 30 hours."}, {"customerQuestion": "How long does the battery last?"}],
        "referenceResponse": "The battery lasts up to 30 hours on a single charge."
    }]
}
```

### Example 2: Single template, multiple variables, multiple evaluation samples, steering criteria
<a name="advanced-prompt-optimization-input-ex2"></a>

```
{
    "version": "bedrock-2026-05-14",
    "promptTemplate": "You are a customer support agent for an electronics store.\n\nGiven the following product information:\n{{productInfo}}\n\nAnswer the customer's question:\n{{customerQuestion}}\n\nProvide a helpful, accurate, and concise response.",
    "templateId": "template-support-1",
    "steeringCriteria": ["PROFESSIONAL", "CONCISE"],
    "evaluationSamples": [
        {"inputVariables": [{"productInfo": "Product: Sony WH-1000XM5 Headphones. Price: $349.99. Battery Life: 30 hours. Noise Cancellation: Yes, adaptive. Connectivity: Bluetooth 5.2, 3.5mm jack. Weight: 250g."}, {"customerQuestion": "How long does the battery last and can I use them wired?"}], "referenceResponse": "The Sony WH-1000XM5 headphones have a battery life of up to 30 hours on a single charge. And yes, they do come with a 3.5mm jack, so you can use them in wired mode as well."},
        {"inputVariables": [{"productInfo": "Product: Sony WH-1000XM5 Headphones. Price: $349.99. Battery Life: 30 hours. Noise Cancellation: Yes, adaptive. Connectivity: Bluetooth 5.2, 3.5mm jack. Weight: 250g."}, {"customerQuestion": "Do these have noise cancellation?"}], "referenceResponse": "Yes, the Sony WH-1000XM5 headphones feature adaptive noise cancellation, which automatically adjusts the level of noise cancellation based on your environment."},
        {"inputVariables": [{"productInfo": "Product: Apple MacBook Air M3. Price: $1,099. RAM: 8GB. Storage: 256GB SSD. Display: 13.6-inch Liquid Retina. Battery Life: Up to 18 hours."}, {"customerQuestion": "Is 8GB of RAM enough for video editing?"}], "referenceResponse": "The MacBook Air M3 comes with 8GB of unified memory. It can handle light video editing but you may want more RAM for heavy work."}
    ]
}
```

### Example 3: Two templates, single variable per prompt, multiple samples, steering criteria
<a name="advanced-prompt-optimization-input-ex3"></a>

This example shows two lines in the JSONL file (two prompt templates in one job).

```
{"version": "bedrock-2026-05-14", "promptTemplate": "You are a helpful assistant. Answer the following: {{question}}", "templateId": "template-qa-1", "steeringCriteria": ["ACCURATE"], "evaluationSamples": [{"inputVariables": [{"question": "What is 2+2?"}], "referenceResponse": "4"}, {"inputVariables": [{"question": "What is the largest planet in our solar system?"}], "referenceResponse": "Jupiter is the largest planet in our solar system."}]}
{"version": "bedrock-2026-05-14", "promptTemplate": "Translate the following to French: {{text}}", "templateId": "template-translate-1", "steeringCriteria": ["PRECISE"], "evaluationSamples": [{"inputVariables": [{"text": "Hello, how are you?"}], "referenceResponse": "Bonjour, comment allez-vous?"}, {"inputVariables": [{"text": "Thank you very much."}], "referenceResponse": "Merci beaucoup."}]}
```

### Example 4: Single template, multiple variables, multiple samples, LLM-as-a-judge
<a name="advanced-prompt-optimization-input-ex4"></a>

```
{
    "version": "bedrock-2026-05-14",
    "promptTemplate": "You are a customer support agent for an electronics store.\n\nGiven the following product information:\n{{productInfo}}\n\nAnswer the customer's question:\n{{customerQuestion}}\n\nProvide a helpful, accurate, and concise response.",
    "templateId": "template-llmj-1",
    "customEvaluationMetricLabel": "responseaccuracy",
    "evaluationSamples": [
        {"inputVariables": [{"productInfo": "Product: Sony WH-1000XM5 Headphones. Price: $349.99. Battery Life: 30 hours. Noise Cancellation: Yes, adaptive."}, {"customerQuestion": "How long does the battery last?"}], "referenceResponse": "The Sony WH-1000XM5 headphones have a battery life of up to 30 hours on a single charge."},
        {"inputVariables": [{"productInfo": "Product: Apple MacBook Air M3. Price: $1,099. RAM: 8GB. Storage: 256GB SSD."}, {"customerQuestion": "Is 8GB of RAM enough for video editing?"}], "referenceResponse": "The MacBook Air M3 comes with 8GB of unified memory. It can handle light video editing but you may want more RAM for heavy work."}
    ],
    "customLLMJConfig": {
        "customLLMJPrompt": "Evaluate how accurate the response is to the customer question. Consider whether the response uses only the provided product information and does not hallucinate details. Here is the information you are supposed to evaluate: \n\nPrompt: {{prompt}}\nResponse: {{response}}\n\n \n\n ground truth answer: {{referenceResponse}}. Grading scale: Rate the response on a scale of 1-5. 1 means the answer is full of hallucinations and does not answer the question. 5 means the answer does not hallucinate at all and perfectly answers the question with no extra information. Interpolate the rest of the grading scale",
        "customLLMJModelId": "anthropic.claude-sonnet-4-5-20250929-v1:0"
    }
}
```

### Example 5: Single template, multiple variables, multiple samples, no evaluation method (system default)
<a name="advanced-prompt-optimization-input-ex5"></a>

Since no evaluation or steering is provided, the prompt optimizer will use a built-in generic LLM-as-a-judge that combines accuracy, completeness, and writing style.

```
{
    "version": "bedrock-2026-05-14",
    "promptTemplate": "You are a customer support agent for an electronics store.\n\nGiven the following product information:\n{{productInfo}}\n\nAnswer the customer's question:\n{{customerQuestion}}\n\nProvide a helpful, accurate, and concise response.",
    "templateId": "template-default-llmj-1",
    "evaluationSamples": [
        {"inputVariables": [{"productInfo": "Product: Sony WH-1000XM5 Headphones. Price: $349.99. Battery Life: 30 hours. Noise Cancellation: Yes, adaptive."}, {"customerQuestion": "How long does the battery last?"}], "referenceResponse": "The Sony WH-1000XM5 headphones have a battery life of up to 30 hours on a single charge."},
        {"inputVariables": [{"productInfo": "Product: Apple MacBook Air M3. Price: $1,099. RAM: 8GB. Storage: 256GB SSD."}, {"customerQuestion": "Is 8GB of RAM enough for video editing?"}], "referenceResponse": "The MacBook Air M3 comes with 8GB of unified memory. It can handle light video editing but you may want more RAM for heavy work."}
    ]
}
```

### Example 6: Single template, single variable, multiple samples, Lambda evaluator
<a name="advanced-prompt-optimization-input-ex6"></a>

```
{
    "version": "bedrock-2026-05-14",
    "promptTemplate": "You are a helpful assistant. Answer the following: {{question}}",
    "templateId": "template-byo-1",
    "customEvaluationMetricLabel": "accuracygraderlambda",
    "evaluationSamples": [
        {"inputVariables": [{"question": "What is the capital of France?"}], "referenceResponse": "The capital of France is Paris."},
        {"inputVariables": [{"question": "What is 2+2?"}], "referenceResponse": "4"}
    ],
    "evaluationMetricLambdaArn": "arn:aws:lambda:us-west-2:<YOUR_ACCOUNT_ID>:function:<YOUR_EVAL_FUNCTION>"
}
```

### Example 7: Single template, no text variables, multimodal only, LLM-as-judge
<a name="advanced-prompt-optimization-input-ex7"></a>

This is an acceptable input even with no `{{variables}}` because there is a multimodal input included.

```
{
    "version": "bedrock-2026-05-14",
    "templateId": "multimodal_only_01",
    "promptTemplate": "Does this image contain a dog? Respond yes or no",
    "customEvaluationMetricLabel": "binarydogjudge",
    "customLLMJConfig": {
        "customLLMJPrompt": "Determine if the model response matches the ground truth. Grading scale: 0 if the response does not match the ground truth, 1 if the response matches the ground truth. Here is the input: \n\n input: {{prompt}} \n\n model response: {{response}} \n\n ground truth: {{referenceResponse}}.",
        "customLLMJModelId": "anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    "evaluationSamples": [
        {"inputVariablesMultimodal": [{"dogimage": {"type": "IMAGE", "s3Uri": "s3://my-bucket/images/dog-photo.jpeg"}}], "referenceResponse": "Yes"},
        {"inputVariablesMultimodal": [{"catimage": {"type": "IMAGE", "s3Uri": "s3://my-bucket/images/cat-photo.png"}}], "referenceResponse": "No"}
    ]
}
```

### Example 8: Single template, multiple variables, LLM-as-judge, mixed text and multimodal
<a name="advanced-prompt-optimization-input-ex8"></a>

```
{
    "version": "bedrock-2026-05-14",
    "templateId": "multimodal_with_text_01",
    "promptTemplate": "Given the context in attached documents and the user question, provide a short answer. User question: {{question}}",
    "customEvaluationMetricLabel": "documentinfograder",
    "customLLMJConfig": {
        "customLLMJPrompt": "Evaluate whether the response correctly answers the question using information from the provided document. Score 1-5 where 5 means fully correct and grounded in the source material, and 1 means the answer was completely hallucinated and inaccurate. Here's the information: \n Prompt: {{prompt}}, Model response: {{response}}, ground truth: {{referenceResponse}}",
        "customLLMJModelId": "anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    "evaluationSamples": [
        {
            "inputVariables": [{"question": "What is the total revenue for Q1?"}],
            "inputVariablesMultimodal": [
                {"Q1report": {"type": "PDF", "s3Uri": "s3://my-bucket/docs/quarterly-report.pdf"}},
                {"revenuechart": {"type": "IMAGE", "s3Uri": "s3://my-bucket/images/revenue-chart.png"}}
            ],
            "referenceResponse": "The total revenue for Q1 was $4.2M."
        }
    ]
}
```