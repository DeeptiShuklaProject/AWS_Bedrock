

# Create and manage optimization jobs
<a name="advanced-prompt-optimization-jobs"></a>

## Create a job (console)
<a name="advanced-prompt-optimization-jobs-console"></a>

**To create a job using the console**

1. Give your advanced prompt optimization job a name.

1. Select your target models (up to 5 per job). If you are migrating to a new model, select your current model as a baseline. Then select up to 4 other models you want to migrate to. If you are not changing models, just select your current model.

1. Upload your JSONL input file from Amazon S3 or from your computer. Make sure you follow the [Prepare your input dataset](advanced-prompt-optimization-input.md).

1. For each prompt template, select your evaluation method. You can choose between steering criteria, LLM-as-a-judge, Lambda function, or leave blank for the system default.

1. Select your output location in S3 for your raw results to be saved after the job.

1. (Optional) Add a job description or a custom KMS key for encryption.

1. Create the optimization.

**Note**  
If you move the results files away from the output S3 location after the job is complete, the console results page will not render.

## Create a job (Python SDK)
<a name="advanced-prompt-optimization-jobs-create-api"></a>

Replace the Region, S3 bucket location, model ID, and other fields as necessary for your use case.

```
import boto3
import json

client = boto3.client('bedrock', region_name='us-west-2')

response = client.create_advanced_prompt_optimization_job(
    jobName='my-optimization-job',
    modelConfigurations=[
        {'modelId': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'}
    ],
    inputConfig={
        's3Uri': 's3://my-bucket/input/dataset.jsonl'
    },
    outputConfig={
        's3Uri': 's3://my-bucket/output/'
    }
)

job_arn = response['jobArn']
print(f'Job created: {job_arn}')
```

## Create a job (AWS CLI)
<a name="advanced-prompt-optimization-jobs-create-cli"></a>

Replace the Region, S3 bucket location, model ID, and other fields as necessary for your use case.

```
JOB_ARN=$(aws bedrock create-advanced-prompt-optimization-job \
    --job-name "my-optimization-job" \
    --model-configurations '[{"modelId": "us.anthropic.claude-sonnet-4-5-20250929-v1:0"}]' \
    --input-config '{"s3Uri": "s3://my-bucket/input/dataset.jsonl"}' \
    --output-config '{"s3Uri": "s3://my-bucket/output/"}' \
    --region us-west-2 \
    --query 'jobArn' --output text)
```

## Check job status
<a name="advanced-prompt-optimization-jobs-status"></a>

```
response = client.get_advanced_prompt_optimization_job(
    jobIdentifier=job_arn
)

print(f"Status: {response['jobStatus']}")
if response.get('failureMessage'):
    print(f"Failure: {response['failureMessage']}")
```

```
aws bedrock get-advanced-prompt-optimization-job \
    --job-identifier "$JOB_ARN" \
    --region us-west-2
```

## List jobs
<a name="advanced-prompt-optimization-jobs-list"></a>

```
response = client.list_advanced_prompt_optimization_jobs(
    maxResults=10
)

for job in response['advancedPromptOptimizationJobSummaries']:
    print(f"{job['jobName']} | {job['jobStatus']} | {job['jobArn']}")
```

```
aws bedrock list-advanced-prompt-optimization-jobs \
    --max-results 10 \
    --region us-west-2
```

## Stop a job
<a name="advanced-prompt-optimization-jobs-stop"></a>

```
client.stop_advanced_prompt_optimization_job(
    jobIdentifier=job_arn
)
print('Job stop requested')
```

```
aws bedrock stop-advanced-prompt-optimization-job \
    --job-identifier "$JOB_ARN" \
    --region us-west-2
```

## Batch delete jobs
<a name="advanced-prompt-optimization-jobs-delete"></a>

```
response = client.batch_delete_advanced_prompt_optimization_jobs(
    jobIdentifiers=[job_arn]
)

for result in response['results']:
    print(f"{result['jobIdentifier']}: {result['status']}")
```

```
aws bedrock batch-delete-advanced-prompt-optimization-jobs \
    --job-identifiers "$JOB_ARN" \
    --region us-west-2
```