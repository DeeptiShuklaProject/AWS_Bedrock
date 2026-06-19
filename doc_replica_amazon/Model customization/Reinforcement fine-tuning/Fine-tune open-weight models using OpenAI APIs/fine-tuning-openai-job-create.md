

# Create and manage fine-tuning jobs for open-weight models using OpenAI APIs
<a name="fine-tuning-openai-job-create"></a>

The OpenAI-compatible fine-tuning job APIs allow you to create, monitor, and manage fine-tuning jobs. This page highlights using these APIs for reinforcement fine-tuning. For complete API details, see the [OpenAI Fine-tuning documentation](https://platform.openai.com/docs/api-reference/fine-tuning).

## Create fine-tuning job
<a name="fine-tuning-openai-create-job"></a>

Creates a fine-tuning job that begins the process of creating a new model from a given dataset. For complete API details, see the [OpenAI Create fine-tuning jobs documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/methods/create).

### Examples
<a name="fine-tuning-openai-create-job-examples"></a>

To create a fine-tuning job with RFT method, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Create fine-tuning job with RFT method
job_response = client.fine_tuning.jobs.create(
    model=MODEL_ID,
    training_file=training_file_id,
    # Suffix field is not supported so commenting for now.
    # suffix="rft-example",  # Optional: suffix for fine-tuned model name
    extra_body={
        "method": {
            "type": "reinforcement", 
            "reinforcement": {
                "grader": {
                    "type": "lambda",
                    "lambda": {
                        "function": "arn:aws:lambda:us-west-2:123456789012:function:my-reward-function"  # Replace with your Lambda ARN
                    }
                },
                "hyperparameters": {
                    "n_epochs": 1,  # Number of training epochs
                    "batch_size": 4,  # Batch size
                    "learning_rate_multiplier": 1.0  # Learning rate multiplier
                }
            }
        }
    }
)

# Store job ID for next steps
job_id = job_response.id
print({job_id})
```

------
#### [ HTTP request ]

Make a POST request to `/v1/fine_tuning/jobs`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "file-abc123",
    "model": "gpt-4o-mini",
    "method": {
      "type": "reinforcement",
      "reinforcement": {
        "grader": {
          "type": "lambda",
          "lambda": {
            "function": "arn:aws:lambda:us-west-2:123456789012:function:my-grader"
          }
        },
        "hyperparameters": {
          "n_epochs": 1,
          "batch_size": 4,
          "learning_rate_multiplier": 1.0
        }
      }
    }
  }'
```

------

## List fine-tuning events
<a name="fine-tuning-openai-list-events"></a>

Lists events for a fine-tuning job. Fine-tuning events provide detailed information about the progress of your job, including training metrics, checkpoint creation, and error messages. For complete API details, see the [OpenAI List fine-tuning events documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/methods/list_events).

### Examples
<a name="fine-tuning-openai-list-events-examples"></a>

To list fine-tuning events, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# List fine-tuning events
events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id="ftjob-abc123",
    limit=50
)

for event in events.data:
    print(f"[{event.created_at}] {event.level}: {event.message}")
    if event.data:
        print(f"  Metrics: {event.data}")
```

------
#### [ HTTP request ]

Make a GET request to `/v1/fine_tuning/jobs/{fine_tuning_job_id}/events`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123/events?limit=50
```

------

Events include information such as:
+ Training started and completed messages
+ Checkpoint creation notifications
+ Training metrics (loss, accuracy) at each step
+ Error messages if the job fails

To paginate through all events, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Paginate through all events
all_events = []
after = None

while True:
    events = client.fine_tuning.jobs.list_events(
        fine_tuning_job_id="ftjob-abc123",
        limit=100,
        after=after
    )
    
    all_events.extend(events.data)
    
    if not events.has_more:
        break
    
    after = events.data[-1].id
```

------
#### [ HTTP request ]

Make multiple GET requests with the `after` parameter:

```
# First request
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123/events?limit=100

# Subsequent requests with 'after' parameter
curl "https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123/events?limit=100&after=ft-event-abc123"
```

------

## Retrieve fine-tuning job
<a name="fine-tuning-openai-retrieve-job"></a>

Get detailed information about a fine-tuning job. For complete API details, see the [OpenAI Retrieve fine-tuning job documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/methods/retrieve).

### Examples
<a name="fine-tuning-openai-retrieve-job-examples"></a>

To retrieve specific job details, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Retrieve specific job details
job_details = client.fine_tuning.jobs.retrieve(job_id)

# Print raw response
print(json.dumps(job_details.model_dump(), indent=2))
```

------
#### [ HTTP request ]

Make a GET request to `/v1/fine_tuning/jobs/{fine_tuning_job_id}`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

## List fine-tuning jobs
<a name="fine-tuning-openai-list-jobs"></a>

Lists your organization's fine-tuning jobs with pagination support. For complete API details, see the [OpenAI List fine-tuning jobs documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/methods/list).

### Examples
<a name="fine-tuning-openai-list-jobs-examples"></a>

To list fine-tuning jobs with limit and pagination, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# List fine-tuning jobs with limit and pagination
response = client.fine_tuning.jobs.list(
    limit=20  # Maximum number of jobs to return
)

# Print raw response
print(json.dumps(response.model_dump(), indent=2))
```

------
#### [ HTTP request ]

Make a GET request to `/v1/fine_tuning/jobs`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs?limit=20 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

## Cancel fine-tuning job
<a name="fine-tuning-openai-cancel-job"></a>

Cancels a fine-tuning job that is in progress. Once cancelled, the job cannot be resumed. For complete API details, see the [OpenAI Cancel fine-tuning job documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/methods/cancel).

### Examples
<a name="fine-tuning-openai-cancel-job-examples"></a>

To cancel a fine-tuning job, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Cancel fine-tuning job
cancel_response = client.fine_tuning.jobs.cancel("ftjob-abc123")

print(f"Job ID: {cancel_response.id}")
print(f"Status: {cancel_response.status}")  # Should be "cancelled"
```

------
#### [ HTTP request ]

Make a POST request to `/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel`:

```
curl -X POST https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123/cancel \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

## List fine-tuning checkpoints
<a name="fine-tuning-openai-list-checkpoints"></a>

Lists checkpoints for a fine-tuning job. Checkpoints are intermediate model snapshots created during fine-tuning that can be used for inference to evaluate performance at different training stages. For more information, see the [OpenAI List fine-tuning checkpoints documentation](https://developers.openai.com/api/reference/resources/fine_tuning/subresources/jobs/subresources/checkpoints/methods/list).

### Examples
<a name="fine-tuning-openai-list-checkpoints-examples"></a>

To list checkpoints for a fine-tuning job, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# List checkpoints for a fine-tuning job
checkpoints = client.fine_tuning.jobs.checkpoints.list(
    fine_tuning_job_id="ftjob-abc123",
    limit=10
)

for checkpoint in checkpoints.data:
    print(f"Checkpoint ID: {checkpoint.id}")
    print(f"Step: {checkpoint.step_number}")
    print(f"Model: {checkpoint.fine_tuned_model_checkpoint}")
    print(f"Metrics: {checkpoint.metrics}")
    print("---")
```

------
#### [ HTTP request ]

Make a GET request to `/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/fine_tuning/jobs/ftjob-abc123/checkpoints?limit=10
```

------

Each checkpoint includes:
+ **Checkpoint ID** – Unique identifier for the checkpoint
+ **Step number** – Training step at which the checkpoint was created
+ **Model checkpoint** – Model identifier that can be used for inference
+ **Metrics** – Validation loss and accuracy at this checkpoint

To use a checkpoint model for inference, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Test inference with a checkpoint
response = client.chat.completions.create(
    model=checkpoint.fine_tuned_model_checkpoint,
    messages=[{"role": "user", "content": "What is AI?"}],
    max_tokens=100
)

print(response.choices[0].message.content)
```

------
#### [ HTTP request ]

Make a POST request to `/v1/chat/completions`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ft:gpt-4o-mini:openai:custom:7p4lURel:ckpt-step-1000",
    "messages": [{"role": "user", "content": "What is AI?"}],
    "max_tokens": 100
  }'
```

------

## Run inference with fine-tuned model
<a name="fine-tuning-openai-inference"></a>

Once your fine-tuning job is complete, you can use the fine-tuned model for inference through the Responses API or Chat Completions API. For complete API details, see [Inference using Responses API](bedrock-mantle.md).

### Responses API
<a name="fine-tuning-openai-responses-api"></a>

Use the Responses API for single-turn text generation with your fine-tuned model:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Get the fine-tuned model ID
job_details = client.fine_tuning.jobs.retrieve("ftjob-abc123")

if job_details.status == 'succeeded' and job_details.fine_tuned_model:
    fine_tuned_model = job_details.fine_tuned_model
    print(f"Using fine-tuned model: {fine_tuned_model}")
    
    # Run inference with Responses API
    response = client.completions.create(
        model=fine_tuned_model,
        prompt="What is the capital of France?",
        max_tokens=100,
        temperature=0.7
    )
    
    print(f"Response: {response.choices[0].text}")
else:
    print(f"Job status: {job_details.status}")
    print("Job must be in 'succeeded' status to run inference")
```

------
#### [ HTTP request ]

Make a POST request to `/v1/completions`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "ft:gpt-4o-mini:openai:custom-model:7p4lURel",
    "prompt": "What is the capital of France?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

------

### Chat Completions API
<a name="fine-tuning-openai-inference-examples"></a>

Use the Chat Completions API for conversational interactions with your fine-tuned model:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Get the fine-tuned model ID
job_details = client.fine_tuning.jobs.retrieve("ftjob-abc123")

if job_details.status == 'succeeded' and job_details.fine_tuned_model:
    fine_tuned_model = job_details.fine_tuned_model
    print(f"Using fine-tuned model: {fine_tuned_model}")
    
    # Run inference
    inference_response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
        max_tokens=100
    )
    
    print(f"Response: {inference_response.choices[0].message.content}")
else:
    print(f"Job status: {job_details.status}")
    print("Job must be in 'succeeded' status to run inference")
```

------
#### [ HTTP request ]

Make a POST request to `/v1/chat/completions`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "ft:gpt-4o-mini:openai:custom-model:7p4lURel",
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "max_tokens": 100
  }'
```

------