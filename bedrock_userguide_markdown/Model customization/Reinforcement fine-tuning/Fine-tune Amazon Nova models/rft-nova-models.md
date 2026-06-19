

# Fine-tune Amazon Nova models with reinforcement fine-tuning
<a name="rft-nova-models"></a>

Before fine-tuning, ensure you have the pre-requisites as Amazon Bedrock needs specific permissions to create and manage the fine-tuning process. For comprehensive security and permissions information, see [Access and security for Amazon Nova models](rft-access-security.md).

Run reinforcement fine-tuning for Amazon Nova models in 5 steps:

1. **Provide Training Dataset** – Upload prompts in required format (e.g., JSONL) as the reinforcement fine-tuning training dataset. For more information, see [Prepare data for Amazon Nova models](rft-prepare-data.md).

1. **Configure Reward Function (grader)** – Define a grader to score model responses based on correctness, structure, tone, or other objectives. The reward function can be executed using Lambda to compute objective scores. You can also choose a model as a judge (via console) and grade responses based on criteria and principles you configure (the console converts these into Lambda functions automatically). For more information, see [Setting up reward functions for Amazon Nova models](reward-functions.md).

1. **Submit reinforcement fine-tuning Job** – Launch the reinforcement fine-tuning job by specifying base model, dataset, reward function, and other optional settings such as hyperparameters. For more information, see [Create and manage fine-tuning jobs for Amazon Nova models](rft-submit-job.md).

1. **Monitor Training** – Track job status, reward metrics, and training progress until completion. For more information, see [Monitor your RFT training job](rft-submit-job.md#rft-monitor-job).

1. **Use Fine-Tuned Model** – After job completion, deploy the resulting RFT model with one click for on-demand inference. You can also use Provisioned Throughput for mission-critical workloads that require consistent performance. See [Set up inference for a custom model](model-customization-use.md). Use **Test in Playground** to evaluate and compare responses with the base model.

**Important**  
You can provide a maximum of 20K prompts to Amazon Bedrock for reinforcement fine-tuning the model.

## Supported Nova models
<a name="rft-nova-supported-models"></a>

The following table shows the Amazon Nova models that you can customize with reinforcement fine-tuning:

**Note**  
For information about additional supported models including open-weight models, see [Fine-tune open-weight models using OpenAI-compatible APIs](fine-tuning-openai-apis.md).


**Supported models for reinforcement fine-tuning**  

| Provider | Model | Model ID | Single-region model support | 
| --- | --- | --- | --- | 
| Amazon | Nova 2 Lite | amazon.nova-2-lite-v1:0:256k | us-east-1 | 