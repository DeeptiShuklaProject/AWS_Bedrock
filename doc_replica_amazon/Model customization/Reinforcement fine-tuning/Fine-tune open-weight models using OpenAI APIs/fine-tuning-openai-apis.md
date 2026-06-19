

# Fine-tune open-weight models using OpenAI-compatible APIs
<a name="fine-tuning-openai-apis"></a>

Amazon Bedrock provides OpenAI compatible API endpoints for fine-tuning foundation models. These endpoints allow you to use familiar OpenAI SDKs and tools to create, monitor, and manage fine-tuning jobs with Amazon Bedrock models. This page highlights using these APIs for reinforcement fine-tuning.

## Key capabilities
<a name="fine-tuning-openai-key-capabilities"></a>
+ **Upload training files** – Use the Files API to upload and manage training data for fine-tuning jobs
+ **Create fine-tuning jobs** – Start fine-tuning jobs with custom training data and reward functions
+ **List and retrieve jobs** – View all fine-tuning jobs and get detailed information about specific jobs
+ **Monitor job events** – Track fine-tuning progress through detailed event logs
+ **Access checkpoints** – Retrieve intermediate model checkpoints created during training
+ **Immediate inference** – After fine-tuning completes, use the resulting fine-tuned model for on-demand inference through Amazon Bedrock's OpenAI-compatible APIs (Responses/chat completions API) without additional deployment steps
+ **Easy migration** – Compatible with existing OpenAI SDK codebases

## Reinforcement fine-tuning workflow for open-weight models
<a name="fine-tuning-openai-workflow"></a>

Before fine-tuning, ensure you have the pre-requisites as Amazon Bedrock needs specific permissions to create and manage the fine-tuning process. For comprehensive security and permissions information, see [Access and security for open-weight models](rft-open-weight-access-security.md).

Run reinforcement fine-tuning for open-weight models in 5 steps:

1. **Upload Training Dataset** – Use the Files API to upload prompts in required format (e.g., JSONL) with purpose "fine-tune" as the reinforcement fine-tuning training dataset. For more information, see [Prepare data for open-weight models](rft-prepare-data-open-weight.md).

1. **Configure Reward Function** – Define a grader to score model responses based on correctness, structure, tone, or other objectives using Lambda functions. For more information, see [Setting up reward functions for open-weight models](reward-functions-open-weight.md).

1. **Create Fine-tuning Job** – Launch the reinforcement fine-tuning job using the OpenAI-compatible API by specifying base model, dataset, reward function, and other optional settings such as hyperparameters. For more information, see [Create fine-tuning job](fine-tuning-openai-job-create.md#fine-tuning-openai-create-job).

1. **Monitor Training Progress** – Track job status, events, and training metrics using the fine-tuning jobs APIs. For more information, see [List fine-tuning events](fine-tuning-openai-job-create.md#fine-tuning-openai-list-events). Access intermediate model checkpoints to evaluate performance at different training stages, see [List fine-tuning checkpoints](fine-tuning-openai-job-create.md#fine-tuning-openai-list-checkpoints).

1. **Run Inference** – Use the fine-tuned model ID directly for inference through Amazon Bedrock's OpenAI-compatible Responses or Chat Completions APIs. For more information, see [Run inference with fine-tuned model](fine-tuning-openai-job-create.md#fine-tuning-openai-inference).

## Supported regions and endpoints
<a name="fine-tuning-openai-supported-regions"></a>

The following table shows the foundation models and regions that support OpenAI compatible fine-tuning APIs:


**Supported models and regions for OpenAI compatible fine-tuning APIs**  

| Provider | Model | Model ID | Region name | Region | Endpoint | 
| --- | --- | --- | --- | --- | --- | 
| OpenAI | Gpt-oss-20B | openai.gpt-oss-20b | US West (Oregon) | us-west-2 | bedrock-mantle.us-west-2.api.aws | 
| Qwen | Qwen3 32B | qwen.qwen3-32b | US West (Oregon) | us-west-2 | bedrock-mantle.us-west-2.api.aws | 