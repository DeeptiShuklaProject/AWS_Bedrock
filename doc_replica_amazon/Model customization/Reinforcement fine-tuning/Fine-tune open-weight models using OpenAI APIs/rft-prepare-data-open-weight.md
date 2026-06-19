

# Prepare data for open-weight models
<a name="rft-prepare-data-open-weight"></a>

When you fine-tune open-weight models with reinforcement fine-tuning using OpenAI-compatible APIs, provide training data by bringing your own prompts in JSONL format with the purpose `fine-tune`.

## Training data format and requirements
<a name="rft-data-format-open-weight"></a>

Training data must follow the OpenAI chat completions format with 100-20K examples. Each training example contains:
+ `messages`: In this field, include the user, system or assistant role containing the input prompt provided to the model.
+ `reference_answer`: In this field, it should contain the expected output or evaluation criteria that your reward function uses to score the model's response. It is not limitedto structured outputs—it can contain any format that helps your reward function evaluate quality.
+ [Optional] You can add fields used by grader Lambda for grading.

**Requirements:**
+ JSONL format with prompts in OpenAI chat completion format (one prompt per line)
+ Purpose must be set to `fine-tune`
+ A minimum of 100 records in training dataset
+ Amazon Bedrock automatically validates training dataset format

------
#### [ Example: General question-answering ]

```
{
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant"
                },
                {
                    role": "user", 
                    "content": "What is machine learning?"}
            ],
            "reference_answer": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed."
            }
```

------
#### [ Example: Math problem ]

```
{
  "id": "sample-001",
  "messages": [
    {
      "role": "system",
      "content": "You are a math tutor"
    },
    {
      "role": "user",
      "content": "Solve: 2x + 5 = 13"
    }
  ],
  "reference_answer": {
    "solution": "x = 4",
    "steps": ["2x = 13 - 5", "2x = 8", "x = 4"]
  }
}
```

------

## Files API
<a name="fine-tuning-openai-files-api"></a>

You can use OpenAI-compatible files api to upload your training data for fine-tuning jobs. Files are stored securely in Amazon Bedrock, and are used when creating fine-tuning jobs. For complete API details, see the [OpenAI Files documentation](https://platform.openai.com/docs/api-reference/files).

### Upload training file
<a name="fine-tuning-openai-upload-file"></a>

To upload a training file, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Upload training file
with open(TRAINING_FILE_PATH, 'rb') as f:
    file_response = client.files.create(
        file=f,
        purpose='fine-tune'
    )

# Store file ID for next steps
training_file_id = file_response.id
print(f"✅ Training file uploaded successfully: {training_file_id}")
```

------
#### [ HTTP request ]

Make a POST request to `/v1/files`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@training_data.jsonl"
```

------

### Retrieve file details
<a name="fine-tuning-openai-retrieve-file"></a>

To retrieve details about a specific file, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Retrieve file details
file_details = client.files.retrieve(training_file_id)

# Print raw response
print(json.dumps(file_details.model_dump(), indent=2))
```

------
#### [ HTTP request ]

Make a GET request to `/v1/files/{file_id}`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/files/file-abc123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

### List files
<a name="fine-tuning-openai-list-files"></a>

To list uploaded files, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# List files
files_response = client.files.list(purpose='fine-tune')

# Print raw response
print(json.dumps(files_response.model_dump(), indent=2))
```

------
#### [ HTTP request ]

Make a GET request to `/v1/files`:

```
curl https://bedrock-mantle.us-west-2.api.aws/v1/files?purpose=fine-tune \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

### Delete file
<a name="fine-tuning-openai-delete-file"></a>

To delete a file, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

```
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables
from openai import OpenAI
client = OpenAI()

# Delete file
delete_response = client.files.delete(training_file_id)
```

------
#### [ HTTP request ]

Make a DELETE request to `/v1/files/{file_id}`:

```
curl -X DELETE https://bedrock-mantle.us-west-2.api.aws/v1/files/file-abc123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

## Characteristics of effective training data
<a name="rft-data-characteristics-open-weight"></a>

Effective RFT training data requires three key characteristics:
+ **Clarity and consistency** – Use clear, unambiguous prompts with consistent formatting. Avoid contradictory labels, ambiguous instructions, or conflicting reference answers that mislead training.
+ **Diversity** – Include varied input formats, edge cases, and difficulty levels that reflect production usage patterns across different user types and scenarios.
+ **Efficient reward functions** – Design functions that execute quickly (seconds, not minutes), parallelize with AWS Lambda, and return consistent scores for cost-effective training.

## Additional properties
<a name="rft-additional-properties-open-weight"></a>

The RFT data format supports custom fields beyond the core schema requirements (`messages` and `reference_answer`). This flexibility allows you to add any additional data your reward function needs for proper evaluation.

**Note**  
You don't need to configure this in your recipe. The data format inherently supports additional fields. Simply include them in your training data JSON, and they will be passed to your reward function in the `metadata` field.

**Common additional properties**
+ `task_id` – Unique identifier for tracking
+ `difficulty_level` – Problem complexity indicator
+ `domain` – Subject area or category
+ `expected_reasoning_steps` – Number of steps in solution

These additional fields are passed to your reward function during evaluation, enabling sophisticated scoring logic tailored to your specific use case.

**Examples with additional properties**

------
#### [ Chemistry problem ]

```
{
  "id": "chem-001",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful chemistry assistant"
    },
    {
      "role": "user",
      "content": "Predict hydrogen bond donors and acceptors for this SMILES: CCN(CC)CCC(=O)c1sc(N)nc1C"
    }
  ],
  "reference_answer": {
    "donor_bond_counts": 2,
    "acceptor_bond_counts": 4
  }
}
```

The `reference_answer` field contains the expected output or evaluation criteria that your reward function uses to score the model's response. It is not limited to structured outputs—it can contain any format that helps your reward function evaluate quality.

------
#### [ Math problem with metadata ]

```
{
  "messages": [
    {
      "role": "system",
      "content": "You are a math tutor"
    },
    {
      "role": "user",
      "content": "Solve: 2x + 5 = 13"
    }
  ],
  "reference_answer": {
    "solution": "x = 4",
    "steps": ["2x = 13 - 5", "2x = 8", "x = 4"]
  },
  "task_id": "algebra_001",
  "difficulty_level": "easy",
  "domain": "algebra",
  "expected_reasoning_steps": 3
}
```

------