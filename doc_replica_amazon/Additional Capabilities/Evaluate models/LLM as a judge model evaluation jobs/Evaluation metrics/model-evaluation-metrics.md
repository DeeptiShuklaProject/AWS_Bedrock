

# Use metrics to understand model performance
<a name="model-evaluation-metrics"></a>

When you run a judge-based model evaluation job, the evaluator model you select uses a set of metrics to characterize the performance of the models being evaluated. Amazon Bedrock provides a number of built-in metrics you can choose from, or you can define your own metrics.

The following table lists the built-in metrics available in Amazon Bedrock for evaluation jobs that use an LLM as a judge. To learn more about using custom metrics, see [Create a prompt for a custom metric](model-evaluation-custom-metrics-prompt-formats.md) and [Create a model evaluation job using custom metrics](model-evaluation-custom-metrics-create-job.md).


| Metric | Description | 
| --- | --- | 
| Correctness (Builtin.Correctness) | Measures if the model's response to the prompt is correct. Note that if you supply a reference response (ground truth) as part of your [prompt dataset](model-evaluation-prompt-datasets-judge.md), the evaluator model considers this when scoring the response. | 
| Completeness (Builtin.Completeness) | Measures how well the model's response answers every question in the prompt. Note that if you supply a reference response (ground truth) as part of your [prompt dataset](model-evaluation-prompt-datasets-judge.md), the evaluator model considers this when scoring the response. | 
| Faithfulness (Builtin.Faithfulness) | Identifies whether the response contains information not found in the prompt to measure how faithful the response is to the available context. | 
| Helpfulness (Builtin.Helpfulness) | Measures how helpful the model's response is. The evaluation uses factors including whether the response follows provided instructions, whether the response is sensible and coherent, and whether the response anticipates implicit needs and expectations. | 
| Logical coherence (Builtin.Coherence) | Measures how coherent the response is by identifying logical gaps, inconsistencies, and contradictions in a model's response to a prompt. | 
| Relevance (Builtin.Relevance) | Measures how relevant the answer is to the prompt. | 
| Following instructions (Builtin.FollowingInstructions) | Measures how well the model's response respects the exact directions found in the prompt. | 
| Professional style and tone (Builtin.ProfessionalStyleAndTone) | Measures how appropriate the response's style, formatting, and tone is for a professional setting. | 
| Harmfulness (Builtin.Harmfulness) | Evaluates whether the response contains harmful content. | 
| Stereotyping (Builtin.Stereotyping) | Evaluates whether content in the response contains stereotypes of any kind (either positive or negative). | 
| Refusal (Builtin.Refusal) | Determines if the response directly declines to answer the prompt or rejects the request by providing reasons. | 