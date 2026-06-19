

# Create a prompt for a custom metric
<a name="kb-evaluation-custom-metrics-prompt-formats"></a>

With RAG evaluation jobs, you can create your own metrics to better characterize model performance for your particular business case. You can define up to 10 custom metrics for each evaluation job.

To create your own custom evaluation metric, you need to supply the following:
+ A prompt containing detailed instructions for the judge model to use
+ The evaluator model you want to use for your custom metrics

You can also specify a scoring system (output schema) that the evaluator model can use to rate the RAG system's outputs.

The following sections describe how to create a prompt for your evaluator model when using custom metrics, including best practices. They also define the schema to use if you create your metric using a JSON file.

To learn how to create an evaluation job with a custom metric using your prompt, see [Creating a retrieve-only RAG evaluation job using custom metrics](knowledge-base-evaluation-create-ro-custom.md) and [Creating a retrieve-and-generate RAG evaluation job using custom metrics](knowledge-base-evaluation-create-randg-custom.md).

## Prompt construction and best practices
<a name="kb-evaluation-custom-metrics-prompt-formats-create"></a>

When creating a prompt for a custom metric, you should structure the prompt with the following elements:

1. **Role definition** (optional) – instructs the evaluator model to adopt a specific identity or role

1. **Task description** – provides detailed instructions about the evaluation task

1. **Criterion and rubric** (optional) – provides detailed scoring guidelines and rubrics for the evaluation

1. **Input variables** – defines the variables to be evaluated such as the prompt and response

Include these elements in your prompt in the order given in the list. The following sections describe each of these elements in more detail.

### Role definition
<a name="kb-evaluation-custom-metrics-prompt-formats-role"></a>

Supplying a role definition is optional, but providing one can help frame the evaluation. For example, if you're creating a metric to evaluate the prose style of a RAG system's final outputs, you could consider using a role like "writing tutor". Roles like "factual accuracy checker" or "subject matter expert" might also be appropriate depending on the goals of your evaluation.

If you choose to include a role definition, it should be the first section of your prompt. The following shows an example role definition.

**Example role definition**  

```
You are a professional editor who is familiar with the requirements of commonly-used style manuals.
```

### Task definition
<a name="kb-evaluation-custom-metrics-prompt-formats-task"></a>

The task definition is the most important section of your prompt and defines the task you want your evaluator model to carry out. Your task definition should provide detailed instructions about the evaluation task (we recommend a minimum of 15 words), and be specific about what aspects to focus on and how to structure the evaluation.

Your task definition should come directly after your role definition, if you choose to include one.

For more general guidance about how to structure prompts for LLMs, see [Design a prompt](design-a-prompt.md).

The following example shows a task definition for a metric that focuses on the adherence of RAG system responses to a particular style guide.

**Example task definition**  

```
You are provided a prompt and a response from a RAG system.
The prompt asks the RAG system to follow the Chicago Manual of Style when generating its responses. 
Your task is to assess how closely the text in the response adheres to the style guide.
Focus in particular on grammar, prose style, and citation requirements.
```

### Criterion and rubric
<a name="kb-evaluation-custom-metrics-prompt-formats-rubric"></a>

This section is optional, and can be used to define multiple evaluation rubrics or provide detailed scoring guidelines for the metric. This section should be added between the task definition and input variables. The following examples show an evaluation rubric and scoring guidelines for the task given in the example task definition provided. You can include either or both of these types of information in this section of your prompt.

**Example evaluation rubric**  

```
When evaluating the response quality, consider the following:
- Grammar: Does the grammar in the response follow the requirements of the style guide
- Style consistency: Does the response maintain consistent capitalization, punctuation, and paragraph formatting
- Citations: Does the response use the correct citation style for in-text citations and endnotes
```

**Example scoring guidelines**  

```
Please rate the quality of the response on the following scale:
- Poor: Response includes errors in citation, grammar, or usage
- Acceptable: Response includes only minor formatting errors
- Good: Response meets all requirements of the style guide
```

When you create an evaluation job that uses an LLM as a judge, either in the AWS Management Console or using the AWS CLI or one of the AWS SDKs, you can specify an output schema for Amazon Bedrock to rate the responses from your generator model. Ensure that any definitions you specify for the output schema are consistent with the scoring guidelines you define in the prompt. For example, in the preceding example, you would specify the definitions for your output schema as 'Poor', 'Acceptable', and 'Good'. For more guidance on defining output schemas, see [Specifying an output schema (rating scale)](#kb-evaluation-custom-metrics-prompt-formats-schema).

### Input variables
<a name="kb-evaluation-custom-metrics-prompt-formats-variables"></a>

The final section of your prompt specifies the variables that the evaluator model needs to perform the evaluation. Note that you must specify the input variables last; if you provide further instructions in your prompt after the input variables, the evaluator model may not evaluate your metrics correctly.

The minimum input variables you need to specify depend on the type of evaluation job you are creating; for a retrieve-only job, you must provide `{{context}}`, and for a retrieve-and-generate job, you must provide `{{prediction}}`. In both cases, we recommend that you also include the prompt provided to the generator model (`{{prompt}}`). The following table defines the variables you can use in your prompt, and how they correspond to properties in your [prompt dataset](model-evaluation-prompt-datasets-judge.md).


| Input variable | Definition | Required (retrieve only) | Required (retrieve and generate) | Prompt dataset property | 
| --- | --- | --- | --- | --- | 
| {{prompt}} | The prompt provided to the RAG system | No | No | "prompt" | 
| {{prediction}} | The response provided by the response generator model (only available for retrieve-and-generate jobs) | No | Yes | "output" -> "text" (only applicable to jobs where you provide your own inference data) | 
| {{ground\_truth}} | A reference answer for the prompt | No | No | "referenceResponses" -> "content" -> "text" | 
| {{context}} | RAG passages received for generating the response | Yes | No | "retrievalResults" -> "content" -> "text" | 
| {{reference\_contexts}} | Ground truth passages you would expect to be retrieved | No | No | referenceContexts -> "content" -> "text" | 

The following example illustrates how to specify input variables in a prompt.

**Example input variable definition**  

```
Here is the actual task:
Prompt: {{prompt}}
Response: {{prediction}}
```

For completeness, the whole prompt for this use case is provided in the following example. A complete prompt can have a maximum length of 5,000 characters.

**Example custom metric prompt**  

```
You are a professional editor who is familiar with the requirements of commonly-used style manuals.
					
You are provided a prompt and a response from a RAG system.
The prompt asks the RAG system to follow the Chicago manual of style when generating its responses. 
Your task is to assess how closely the text in the response adheres to the style guide.
Focus in particular on grammar, prose style, and citation requirements.

When evaluating the response quality, consider the following:
- Grammar: Does the grammar in the response follow the requirements of the style guide
- Style consistency: Does the response maintain consistent capitalization, punctuation, and paragraph formatting
- Citations: Does the response use the correct citation style for in-text citations and endnotes

Please rate the quality of the response on the following scale:
- Poor: Response includes errors in citation, grammar, or usage
- Acceptable: Response includes only minor formatting errors
- Good: Response meets all requirements of the style guide

Here is the actual task:
Prompt: {{prompt}}
Response: {{prediction}}
```

## Specifying an output schema (rating scale)
<a name="kb-evaluation-custom-metrics-prompt-formats-schema"></a>

In addition to the evaluation guidelines in your prompt, when you create an evaluation job with a custom metric, you can define a rating scale for the metric by specifying an output schema. This schema consists of scale values and their corresponding definitions. The values for the scale can be either numerical values or strings, but not a mixture of both.

We strongly recommend that you define a rating scale. If you don't, Amazon Bedrock may not be able to properly parse the outputs of your evaluator model to display your results graphically in the console, or to compute average score calculations. You can define a rating scale when you create a metric either using the console, or by using the `ratingScale` property if you create your metric using an AWS SDK or the AWS CLI. 

 When you define a rating scale, Amazon Bedrock adds structured output instructions to your evaluator model prompt. Because the format for structured output differs between evaluator models, it's important that you define the rating scale separately, and don't include it as part of your main prompt. If you create your metric and define a rating scale in the console, you can see the final prompt including the structured output instructions in the **preview** text area. 

When providing the definition for each scale value, be sure that the definitions you use in your output schema definition exactly match how you have defined your scoring guidelines in the prompt. These definitions should have a maximum of five words and are limited to 100 characters. Avoid using articles ('a' and 'the') in the definition. You can use the explanatory text in your prompt to provide the evaluator model with a more detailed definition of how to rate responses.

The following table illustrates how you might describe the scoring guidelines in the prompt, and how you should define the corresponding scale definition in the output schema.


| Prompt scoring guideline | Schema scale value | Schema scale definition | 
| --- | --- | --- | 
| - Poor: The response fails to meet the basic requirements of the prompt and contains significant errors and omissions | 0 | Poor | 
| - Good: The response adequately meets the basic requirements of the prompt but may contain minor errors or omissions | 1 | Good | 
| - Excellent: The response fully meets the prompt with comprehensive, accurate, and valuable information | 2 | Excellent | 

This example uses integer values for the scale, but you can also use strings.

To learn how to specify the schema when you create an evaluation job, see [Create a model evaluation job using custom metrics](model-evaluation-custom-metrics-create-job.md).

## Creating a JSON file to create a custom metric
<a name="kb-evaluation-custom-metrics-prompt-formats-json"></a>

When you create an evaluation job that uses custom metrics in the console, you have the option to upload a JSON file from your local machine that defines your metric. If you choose to use a JSON file to create a custom metric using the console, you can't define a rating scale using the text areas in the console UI, so you must include it in your JSON definition. We recommend that you always define a rating scale when creating custom metrics.

The following examples show JSON file formats for creating a custom metric with either a numerical or a string rating scale, or with no rating scale. In each case, add your complete prompt as a string in the `"instructions"` property.

When you create an evaluation job with one or more custom metrics, Amazon Bedrock stores your metric definitions as JSON files in the output S3 bucket you specify. You can access these files by navigating to `s3://{{S3-output-bucket-name}}/{{job-name}}/{{job-uuid}}/custom_metrics`.

------
#### [ Definition with numerical scale ]

```
{
    "customMetricDefinition": {
        "metricName": {{"my_custom_metric"}},
        "instructions": {{"Your complete custom metric prompt including at least one {{input variable}}"}},
        "ratingScale": [
            {
                "definition": {{"first rating definition"}},
                "value": {
                    "floatValue": {{3}}
                }
            },
            {
                "definition": {{"second rating definition"}},
                "value": {
                    "floatValue": {{2}}
                }
            },
            {
                "definition": {{"third rating definition"}},
                "value": {
                    "floatValue": {{1}}
                }
            }
        ]
    }
}
```

------
#### [ Definition with string scale ]

```
{
    "customMetricDefinition": {
        "metricName": {{"my_custom_metric"}},
        "instructions": {{"Your complete custom metric prompt including at least one {{input variable}}"}},
        "ratingScale": [
            {
                "definition": {{"first rating definition"}},
                "value": {
                    "stringValue": {{"first value"}}
                }
            },
            {
                "definition": {{"second rating definition"}},
                "value": {
                    "stringValue": {{"second value"}}
                }
            },
            {
                "definition": {{"third rating definition"}},
                "value": {
                    "stringValue": {{"third value"}}
                }
            }
        ]
    }
}
```

------
#### [ Definition with no scale ]

```
{
    "customMetricDefinition": {
        "metricName": {{"my_custom_metric"}},
        "instructions": {{"Your complete custom metric prompt including at least one {{input variable}}"}}
    }
}
```

------