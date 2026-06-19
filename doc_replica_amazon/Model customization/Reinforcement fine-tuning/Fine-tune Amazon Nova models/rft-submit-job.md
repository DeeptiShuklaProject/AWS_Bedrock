

# Create and manage fine-tuning jobs for Amazon Nova models
<a name="rft-submit-job"></a>

You can create a reinforcement fine-tuning (RFT) job using the Amazon Bedrock console or API. The RFT job can take a few hours depending on the size of your training data, number of epochs, and complexity of your reward functions.

## Prerequisites
<a name="rft-prerequisites"></a>
+ Create an IAM service role with the required permissions. For comprehensive security and permissions information including RFT-specific permissions, see [Access and security for Amazon Nova models](rft-access-security.md).
+ (Optional) Encrypt input and output data, your RFT job, or inference requests made to custom models. For more information, see [ Encryption of custom models](https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-custom-job.html).

## Create your RFT job
<a name="rft-submit-job-how-to"></a>

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

To submit an RFT job in the console, carry out the following steps:

1. Open the Amazon Bedrock console and navigate to **Custom models** under **Tune**.

1. Choose **Create**, then **Create reinforcement fine-tuning job**.

1. In the **Model details** section, choose **Amazon Nova 2 Lite** as your base model.

1. In the **Customization details** section, enter the customization name.

1. In the **Training data** section, choose your data source. Either select from your available invocation logs stored in Amazon S3, or select the Amazon S3 location of your training dataset file, or upload a file directly from your device.
**Note**  
Your training dataset should be in the OpenAI Chat Completions data format. If you provide invocation logs in the Amazon Bedrock invoke or converse format, Amazon Bedrock automatically converts them to the Chat Completions format.

1. In the **Reward function** section, set up your reward mechanism:
   + **Model as judge (RLAIF)** - Select a Bedrock hosted base model as judge and configure the instructions for evaluation. Use this for subjective tasks like content moderation.
**Note**  
The console's **Model as judge** option automatically converts your configuration into a Lambda function during training.
   + **Custom code (RLVR)** - Create custom reward functions using Python code executed through Lambda functions. Use this for objective tasks like code generation.

   For more information, see [Setting up reward functions for Amazon Nova models](reward-functions.md).

1. (Optional) In the **Hyperparameters** section, adjust training parameters or use default values.

1. In the **Output data** section, enter the Amazon S3 location where Amazon Bedrock should save job outputs.

1. In the **Role configuration** section, either choose an existing role from the dropdown list or enter a name for the service role to create.

1. (Optional) In the **Additional configuration** section, configure the validation data by pointing to an Amazon S3 bucket, KMS encryption settings, and job and model tags.

1. Choose **Create reinforcement fine-tuning job** to begin the job.

------
#### [ API ]

Send a CreateModelCustomizationJob request with `customizationType` set to `REINFORCEMENT_FINE_TUNING`.

**Required fields:** `roleArn`, `baseModelIdentifier`, `customModelName`, `jobName`, `trainingDataConfig`, `outputDataConfig`, `rftConfig`

**Example request:**

```
{
    "roleArn": "arn:aws:iam::{{123456789012}}:role/{{BedrockRFTRole}}",
    "baseModelIdentifier": "amazon.nova-2.0",
    "customModelName": "{{my-rft-model}}",
    "jobName": "{{my-rft-job}}",
    "customizationType": "REINFORCEMENT_FINE_TUNING",
    "trainingDataConfig": {
        "s3Uri": "s3://{{my-bucket}}/{{training-data.jsonl}}"
    },
    "customizationConfig": {
        "rftConfig" : {
            "graderConfig": {
                "lambdaGrader": {
                    "lambdaArn": "arn:aws:lambda:{{us-east-1}}:{{123456789012}}:function:{{function-name}}"
                }
            },
            "hyperParameters": {
                "batchSize": 64,
                "epochCount": 2,
                "evalInterval": 10,
                "inferenceMaxTokens": 8192,
                "learningRate": 0.00001,
                "maxPromptLength": 4096,
                "reasoningEffort": "high",
                "trainingSamplePerPrompt": 4
            }
        }
    },
    "outputDataConfig": {
        "s3Uri": "s3://{{my-bucket}}/{{rft-output/}}"
    }
}
```

**Python API sample request:**

```
import boto3

bedrock = boto3.client(service_name='bedrock')
    
# Set parameters
customizationType = "REINFORCEMENT_FINE_TUNING"
baseModelIdentifier = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-2-lite-v1:0:256k"
roleArn = "${your-customization-role-arn}"
jobName = "MyFineTuningJob"
customModelName = "MyCustomModel"

customizationConfig = {
    'rftConfig' : {
        'graderConfig': {
            'lambdaGrader': {
                'lambdaArn': 'arn:aws:lambda:us-east-1:123456789012:function:function-name'
            }
        },
        'hyperParameters': {
            'batchSize': 64,
            'epochCount': 2,
            'evalInterval': 10,
            'inferenceMaxTokens': 8192,
            'learningRate':0.00001,
            'maxPromptLength': 4096,
            'reasoningEffort': 'high',
            'trainingSamplePerPrompt':4
        }
    }
}

trainingDataConfig = {"s3Uri": "s3://${training-bucket}/myInputData/train.jsonl"}
outputDataConfig = {"s3Uri": "s3://${output-bucket}/myOutputData"}

# Create job
response_ft = bedrock.create_model_customization_job(
    jobName=jobName, 
    customModelName=customModelName,
    roleArn=roleArn,
    baseModelIdentifier=baseModelIdentifier,
    customizationConfig=customizationConfig,
    trainingDataConfig=trainingDataConfig,
    outputDataConfig=outputDataConfig,
    customizationType=customizationType
)

jobArn = response_ft['jobArn']
```

------

## Monitor your RFT training job
<a name="rft-monitor-job"></a>

Amazon Bedrock provides real-time monitoring with visual graphs and metrics during RFT training. These metrics help you understand whether the model converges properly and if the reward function effectively guides the learning process.

### Job status tracking
<a name="rft-job-status"></a>

You can monitor your RFT job status through the validation and training phases in the Amazon Bedrock console.

**Completion indicators:**
+ Job status changes to **Completed** when training completes successfully
+ Custom model ARN becomes available for deployment
+ Training metrics reach convergence thresholds

### Real-time training metrics
<a name="rft-real-time-metrics"></a>

Amazon Bedrock provides real-time monitoring during RFT training with visual graphs displaying training and validation metrics.

#### Core training metrics
<a name="rft-core-metrics"></a>
+ **Training loss** - Measures how well the model is learning from the training data
+ **Training reward statistics** - Shows reward scores assigned by your reward functions
+ **Reward margin** - Measures the difference between good and bad response rewards
+ **Accuracy on training and validation sets** - Shows model performance on both the training and held-out data

**Detailed metric categories**
+ **Reward metrics** – `critic/rewards/mean`, `critic/rewards/max`, `critic/rewards/min` (reward distribution), and `val-score/rewards/mean@1` (validation rewards)
+ **Model behavior** – `actor/entropy` (policy variation; higher equals more exploratory)
+ **Training health** – `actor/pg_loss` (policy gradient loss), `actor/pg_clipfrac` (frequency of clipped updates), and `actor/grad_norm` (gradient magnitude)
+ **Response characteristics** – `prompt_length/mean`, `prompt_length/max`, `prompt_length/min` (input token statistics), `response_length/mean`, `response_length/max`, `response_length/min` (output token statistics), and `response/aborted_ratio` (incomplete generation rate; 0 equals all completed)
+ **Performance** – `perf/throughput` (training throughput), `perf/time_per_step` (time per training step), and `timing_per_token_ms/*` (per-token processing times)
+ **Resource usage** – `perf/max_memory_allocated_gb`, `perf/max_memory_reserved_gb` (GPU memory), and `perf/cpu_memory_used_gb` (CPU memory)

#### Training progress visualization
<a name="rft-progress-visualization"></a>

The console displays interactive graphs that update in real-time as your RFT job progresses. These visualizations can help you:
+ Track convergence toward optimal performance
+ Identify potential training issues early
+ Determine optimal stopping points
+ Compare performance across different epochs

## Set up inference
<a name="rft-setup-inference"></a>

After job completion, deploy the RFT model for on-demand inference or use Provisioned Throughput for consistent performance. For setting up inference, see [Set up inference for a custom model](model-customization-use.md).

Use **Test in Playground** to evaluate and compare responses with the base model. For evaluating your completed RFT model, see [Evaluate your RFT model](rft-evaluate-model.md).