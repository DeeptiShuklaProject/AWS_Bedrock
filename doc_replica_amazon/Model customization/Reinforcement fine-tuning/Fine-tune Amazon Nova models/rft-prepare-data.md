

# Prepare data for Amazon Nova models
<a name="rft-prepare-data"></a>

When you fine-tune an Amazon Nova model with reinforcement fine-tuning, you can bring your own prompts or use existing Amazon Bedrock API invocation logs as training data.

## Training data requirements and sources
<a name="rft-data-source-options"></a>

You can provide training data through one of the following options:

**Note**  
We only support the OpenAI chat completion format.

### Option 1: Provide your own prompts
<a name="w2aac17c25c17c15b5b7b1"></a>

Collect your prompts and store them in `.jsonl` file format. You can upload custom datasets in JSONL format or select existing datasets from Amazon S3. Each record in the JSONL must use the OpenAI chat completion format in the following structure:
+ `messages`: In this field, include the user, system or assistant role containing the input prompt provided to the model.
+ `reference_answer`: In this field, it should contain the expected output or evaluation criteria that your reward function uses to score the model's response. It is not limitedto structured outputs—it can contain any format that helps your reward function evaluate quality.
+ [Optional] You can add fields used by grader Lambda for grading.

**Requirements:**
+ JSONL format with prompts in OpenAI chat completion format (one prompt per line)
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

### Option 2: Use invocation logs
<a name="w2aac17c25c17c15b5b7b3"></a>

When you create a reinforcement fine-tuning job, you can have Amazon Bedrock use existing invocation logs from your S3 bucket as training data. For Amazon Bedrock, an invocation log is a detailed record of model invocations.

You can use customer-side stored Invoke/Converse API invocation logs from Amazon S3 for training.

**Requirements:**
+ API logging must be enabled for your Amazon Bedrock usage
+ Logs must be in a supported format (Amazon Bedrock Invoke/Converse API)
+ A minimum of 100 prompt examples

To use invocation logs for reinforcement fine-tuning, set the model invocation logging on, use one of the model invocation operations, and make sure that you've set up an Amazon S3 bucket as the destination for the logs. For more information about setting up the invocation logs, see [Monitor model invocation using CloudWatch Logs and Amazon S3](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html).

Before you can start the reinforcement fine-tuning job with invocation logs from an S3 bucket as input, you must provide Amazon Bedrock permissions to access the logs from an S3 Bucket. For more information, see [Model customization access and security](custom-model-job-access-security.md).

You can optionally add request metadata to the prompt-response pairs in the invocation log using one of the model invocation operations and then later use it to filter the logs. Amazon Bedrock can use the filtered logs to fine-tune the model.

#### Add request metadata to prompts and responses in your invocation logs
<a name="rft-request-metadata"></a>

With invocation logs, you can identify the training dataset prompts that you want Amazon Bedrock to use for reinforcement fine-tuning using request metadata attached to invocation logs. 

The following is an example of an invocation log from an `InvokeModel` call with the `requestMetadata`:

```
{
"schemaType": "ModelInvocationLog",
    "schemaVersion": "1.0",
    "timestamp": "2024-09-11T17:16:18Z",
    "accountId": "XXXXX",
    "identity": {
"arn": "arn:aws:sts::XXXXXXX:assumed-role/Admin/XXXXXX"
    },
    "region": "us-east-1",
    "requestId": "7ee514f3-9eff-467c-af75-8fd564ce58e5",
    "operation": "InvokeModel",
    "modelId": "meta.llama3-1-405b-instruct-v1:0",
    "input": {
"inputContentType": "application/json",
        "inputBodyJson": {
"prompt": "story of two dogs",
            "max_tokens_to_sample": 300
        },
        "inputTokenCount": 13
    },
    "output": {
"outputContentType": "application/json",
        "outputBodyJson": {
"type": "completion",
            "completion": " Here is a story about two dogs:\n\nRex and Charlie were best friends who lived next door to each other. Every morning, their owners would let them out into the backyard to play. Rex was a golden retriever with long, shaggy fur. He loved to run and chase sticks. Charlie was a corgi with short legs and a big smile. He was happy just sniffing the grass and rolling around. \n\nThe two dogs spent every day playing together. Rex would grab a stick and bring it over to Charlie, wagging his tail excitedly. Charlie would take the other end of the stick in his mouth and they'd have a friendly game of tug-of-war. After tiring themselves out, they'd flop down in the warm sunshine for a nap. \n\nAt lunchtime, their owners would call them in for food. Rex would gobble up his kibble hungrily while Charlie ate his at a more leisurely pace. After lunch, it was right back outside for more playtime. The afternoon sunbeams would light up their fur as they chased each other around the yard. \n\nWhen it started getting late, their owners called them in for the night. Rex and Charlie would head inside, tired but happy after another fun day of play. After slurping up fresh water from their bowls, they'd curl up on their beds, Rex's fluffy golden tail tucked over his nose and little",
            "stop_reason": "max_tokens",
            "stop": null
        },
        "outputTokenCount": 300
    },
    "requestMetadata": {
"project": "CustomerService",
        "intent": "ComplaintResolution",
        "priority": "High"
    }
}
```

You can specify the invocation log as your input data source when you start a reinforcement fine-tuning job. You can start a reinforcement fine-tuning job through the Amazon Bedrock console, using the API, AWS CLI, or SDK.

##### Requirements for providing request metadata
<a name="rft-metadata-requirements"></a>

The request metadata must meet the following requirements:
+ Provided in the JSON `key:value` format.
+ Key and value pair must be a string of 256 characters maximum.
+ Provide a maximum of 16 key-value pairs.

##### Using request metadata filters
<a name="rft-metadata-filters"></a>

Once invocation logs with request metadata are available, you can apply filters based on the request metadata to selectively choose which prompts to include for fine-tuning the model. For example, you might want to include only those with `"project": "CustomerService"` and `"priority": "High"` request metadata.

To filter the logs using multiple request metadata, use a single Boolean operator `AND` or `OR`. You cannot combine these operators. For single request metadata filtering, use the `Equals` or `Not Equals` operator.

## Characteristics of effective training data
<a name="rft-data-characteristics"></a>

Effective RFT training data requires three key characteristics:
+ **Clarity and consistency** – Use clear, unambiguous prompts with consistent formatting. Avoid contradictory labels, ambiguous instructions, or conflicting reference answers that mislead training.
+ **Diversity** – Include varied input formats, edge cases, and difficulty levels that reflect production usage patterns across different user types and scenarios.
+ **Efficient reward functions** – Design functions that execute quickly (seconds, not minutes), parallelize with AWS Lambda, and return consistent scores for cost-effective training.

## Additional properties
<a name="rft-additional-properties"></a>

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