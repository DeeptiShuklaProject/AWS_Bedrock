

# View and interpret results
<a name="advanced-prompt-optimization-results"></a>

## Output location
<a name="advanced-prompt-optimization-results-location"></a>

After a job completes, results are written to your output S3 path:

`{{output-s3-uri}}/{{job-id}}/advanced_prompt_optimization_results.jsonl`

The job ID is the last segment of the job ARN.

## Console results page
<a name="advanced-prompt-optimization-results-console"></a>

**Warning**  
If you move the results files away from the output S3 location after the job is complete, the console results page will not render.

## Output format
<a name="advanced-prompt-optimization-results-format"></a>

The output file is JSONL with per-template results. Each line contains:
+ `promptTemplateId`: correlates to your input templateId
+ `promptOptimizationResults`: array with one entry per target model, each containing:
  + `modelId`: the target model
  + `status`: optimization status for this model
  + `optimizedPromptTemplate`: the rewritten prompt template
  + Evaluation scores per sample
  + Latency (time to first token, or TTFT)
  + Cost estimates

## Reading results programmatically
<a name="advanced-prompt-optimization-results-code"></a>

```
import boto3
import json

s3 = boto3.client('s3', region_name='us-west-2')

# Job ID is the last segment of the job ARN
job_id = job_arn.split('/')[-1]
output_key = f'output/{job_id}/advanced_prompt_optimization_results.jsonl'

response = s3.get_object(Bucket='my-bucket', Key=output_key)
content = response['Body'].read().decode('utf-8')

for line in content.strip().split('\n'):
    result = json.loads(line)
    print(f"Template: {result['promptTemplateId']}")
    for opt in result.get('promptOptimizationResults', []):
        print(f"  Model: {opt['modelId']}")
        print(f"  Status: {opt['status']}")
        print(f"  Optimized: {opt['optimizedPromptTemplate'][:100]}...")
```

## Interpreting scores
<a name="advanced-prompt-optimization-results-scores"></a>

Scores are normalized; higher is better. The service normalizes all evaluation scores regardless of the original grading scale you defined in your evaluation method.

You can always see the raw LLM-as-a-judge output in your S3 bucket and on the console results page in the detailed results tab. Due to the nature of merging custom LLMJ prompts with the service-provided default prompt, the numerical score may not exactly match the discrete steps in your custom LLMJ rubric. If you want binary evaluation results or exact matching, it may be better to use a Lambda evaluator.