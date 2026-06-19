

# Nova Premier
<a name="model-card-amazon-nova-premier"></a>

## ![Amazon logo with curved arrow from A to Z forming a smile.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/models/nova2pro.png) Amazon — Nova Premier
<a name="model-card-amazon-nova-premier-header"></a>

## Model Details
<a name="model-card-amazon-nova-premier-details"></a>

Nova Premier is Amazon's multimodal model for complex reasoning, agentic workflows, and model distillation. For more information about model development and performance, see the [model/service card](https://docs.aws.amazon.com/ai/responsible-ai/nova-micro-lite-pro/overview.html).
+ **Model launch date:** Oct 31, 2025
+ **Model EOL date:** September 14, 2026
+ **End User License Agreements and Terms of Use:** [View](https://aws.amazon.com/legal/bedrock/third-party-models/)
+ **Model lifecycle:** Legacy
+ **Context window:** 1M tokens
+ **Max output tokens:** 25K
+ **Reasoning:** Supported
+ **Knowledge cutoff:** Oct 2024


| **Input Modalities** | **Output Modalities** | **[APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html)** | **[Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)** | 
| --- | --- | --- | --- | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Audio | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Embedding | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Responses | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) bedrock-runtime | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Chat Completions | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) bedrock-mantle | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Invoke |  | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Converse |  | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Video | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video |  |  | 

## Capabilities and Features
<a name="model-card-amazon-nova-premier-capabilities"></a>

***Bedrock Features***

**Features supported using `bedrock-runtime` endpoint**


| **Supported** | **Not Supported** | 
| --- | --- | 
|  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-premier.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-premier.html)  | 

**Prompt caching using `bedrock-runtime` endpoint**

For more information, see [Prompt caching for faster model inference](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html).


| **Prompt caching supported** | **Min tokens per cache checkpoint** | **Max cache checkpoints per request** | **Supported TTL** | **Fields that accept prompt cache checkpoints** | 
| --- | --- | --- | --- | --- | 
| Yes | 1K\* | 4 | 5 minutes | system and messages | 

*\* Amazon Nova models support a maximum of 20K tokens for prompt caching. Prompt caching is primarily for text prompts.*

## Pricing
<a name="model-card-amazon-nova-premier-pricing"></a>

For pricing, please refer to the [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) page.

## Programmatic Access
<a name="model-card-amazon-nova-premier-programmatic-access"></a>

Use the following model IDs and endpoint URLs to access this model programmatically. For more information about the available APIs and endpoints, see [APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html) and [Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html).


| **Endpoint** | **Model ID** | **In-Region endpoint URL** | **Geo inference ID** | **Global inference ID** | 
| --- | --- | --- | --- | --- | 
| bedrock-runtime | amazon.nova-premier-v1:0 | https://bedrock-runtime.{region}.amazonaws.com | us.amazon.nova-premier-v1:0 | Not supported | 

*For example, if region is us-east-1 (N. Virginia), then the bedrock-runtime endpoint URL will be "https://bedrock-runtime.us-east-1.amazonaws.com" and for bedrock-mantle will be "https://bedrock-mantle.us-east-1.api.aws/v1".*

## Service Tiers
<a name="model-card-amazon-nova-premier-tiers"></a>

Amazon Bedrock offers multiple service tiers to match your workload requirements. **Standard** provides pay-per-token access with no commitment. **Priority** offers higher throughput with a time-based commitment. **Flex** provides lower-cost access for flexible, non-time-sensitive workloads. **Reserved** provides dedicated throughput with a term commitment for predictable workloads. For more information, see [service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html).


| **Standard** | **Priority** | **Flex** | **Reserved** | 
| --- | --- | --- | --- | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Regional Availability
<a name="model-card-amazon-nova-premier-regional-availability"></a>

***Regional availability at a glance***

Bedrock offers three inference options: **In-Region** keeps requests within a single Region for strict compliance, **Geo Cross-Region** routes across Regions within a geography (US, EU, etc.) for higher throughput while respecting data residency, and **Global Cross-Region** routes anywhere worldwide for maximum throughput when there are no residency constraints. Refer to the [Regional availability](models-region-compatibility.md) page for more details.


| **Region** | **In-Region** | **Geo** | **Global** | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

***Geo inference details***

**Geo: US**

Geo Inference ID: `us.amazon.nova-premier-v1:0`


| **Source Region** | **Destination Regions** | 
| --- | --- | 
| us-east-1 (N. Virginia) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-east-2 (Ohio) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-west-2 (Oregon) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 

## Quotas and Limits
<a name="model-card-amazon-nova-premier-quotas"></a>

Your AWS account has default quotas to maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock. The default quotas assigned to an account might be updated depending on regional factors, payment history, fraudulent usage, and/or approval of a quota [increase request](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-increase.html). For more details, please refer to [Quotas for Amazon Bedrock](quotas.md) documentation and see the [limits](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) for the model.

## Sample Code
<a name="model-card-amazon-nova-premier-sample-code"></a>

**Step 1 - AWS Account:** If you have an AWS account already, skip this step. If you are new to AWS, sign up for an [AWS account](https://portal.aws.amazon.com/billing/signup).

**Step 2 - API key:** Go to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/home#/api-keys/long-term/create) and generate a long-term API key.

**Step 3 - Get the SDK:** To use this getting started guide, you must have Python already installed. Then install the relevant software depending on the APIs you are using.

```
pip install boto3
```

**Step 4 - Set environment variables:** Configure your environment to use the API key for authentication.

```
AWS_BEARER_TOKEN_BEDROCK="<provide your Bedrock API key>"
```

**Step 5 - Run your first inference request:** Save the file as `bedrock-first-request.py`

------
#### [ Invoke API ]

```
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')
response = client.invoke_model(
    modelId='amazon.nova-premier-v1:0',
    body=json.dumps({
            'messages': [{
                'role': 'user',
                'content': [{'text': 'Can you explain the features of Amazon Bedrock?'}]
            }],
            'inferenceConfig': {
                'maxTokens': 1024
            }
    })
)
print(json.loads(response['body'].read()))
```

------
#### [ Converse API ]

```
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')
response = client.converse(
    modelId='amazon.nova-premier-v1:0',
    messages=[
        {
            'role': 'user',
            'content': [{'text': 'Can you explain the features of Amazon Bedrock?'}]
        }
    ]
)
print(response)
```

------