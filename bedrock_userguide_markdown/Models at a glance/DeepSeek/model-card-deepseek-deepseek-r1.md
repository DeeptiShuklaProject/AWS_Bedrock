

# DeepSeek-R1
<a name="model-card-deepseek-deepseek-r1"></a>

## ![Blue icon showing a stylized whale with containers, representing Docker or container services.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/models/deepseek.png) DeepSeek — DeepSeek-R1
<a name="model-card-deepseek-deepseek-r1-header"></a>

## Model Details
<a name="model-card-deepseek-deepseek-r1-details"></a>

DeepSeek-R1 is DeepSeek's reasoning model that uses chain-of-thought to solve complex math, coding, and logic problems. For more information about model development and performance, see the [model/service card](https://api-docs.deepseek.com/news/news250120).
+ **Model launch date:** Jan 20, 2025
+ **Model EOL date:** No sooner than 3/10/2026
+ **End User License Agreements and Terms of Use:** [View](https://huggingface.co/deepseek-ai/DeepSeek-R1/blob/main/LICENSE)
+ **Model lifecycle:** Active
+ **Context window:** 128K tokens
+ **Max output tokens:** 8K
+ **Reasoning:** Supported
+ **Knowledge cutoff:** Jan 2025


| **Input Modalities** | **Output Modalities** | **[APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html)** | **[Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)** | 
| --- | --- | --- | --- | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Audio | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Embedding | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Responses | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) bedrock-runtime | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Chat Completions | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) bedrock-mantle | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Invoke |  | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Converse |  | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video |  |  | 

## Capabilities and Features
<a name="model-card-deepseek-deepseek-r1-capabilities"></a>

***Bedrock Features***

**Features supported using `bedrock-runtime` endpoint**


| **Supported** | **Not Supported** | 
| --- | --- | 
|  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-deepseek-deepseek-r1.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-deepseek-deepseek-r1.html)  | 

## Pricing
<a name="model-card-deepseek-deepseek-r1-pricing"></a>

For pricing, please refer to the [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) page.

## Programmatic Access
<a name="model-card-deepseek-deepseek-r1-programmatic-access"></a>

Use the following model IDs and endpoint URLs to access this model programmatically. For more information about the available APIs and endpoints, see [APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html) and [Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html).


| **Endpoint** | **Model ID** | **In-Region endpoint URL** | **Geo inference ID** | **Global inference ID** | 
| --- | --- | --- | --- | --- | 
| bedrock-runtime | deepseek.r1-v1:0 | https://bedrock-runtime.{region}.amazonaws.com | us.deepseek.r1-v1:0 | Not supported | 

*For example, if region is us-east-1 (N. Virginia), then the bedrock-runtime endpoint URL will be "https://bedrock-runtime.us-east-1.amazonaws.com" and for bedrock-mantle will be "https://bedrock-mantle.us-east-1.api.aws/v1".*

## Service Tiers
<a name="model-card-deepseek-deepseek-r1-tiers"></a>

Amazon Bedrock offers multiple service tiers to match your workload requirements. **Standard** provides pay-per-token access with no commitment. **Priority** offers higher throughput with a time-based commitment. **Flex** provides lower-cost access for flexible, non-time-sensitive workloads. **Reserved** provides dedicated throughput with a term commitment for predictable workloads. For more information, see [service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html).


| **Standard** | **Priority** | **Flex** | **Reserved** | 
| --- | --- | --- | --- | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Regional Availability
<a name="model-card-deepseek-deepseek-r1-regional-availability"></a>

***Regional availability at a glance***

Bedrock offers three inference options: **In-Region** keeps requests within a single Region for strict compliance, **Geo Cross-Region** routes across Regions within a geography (US, EU, etc.) for higher throughput while respecting data residency, and **Global Cross-Region** routes anywhere worldwide for maximum throughput when there are no residency constraints. Refer to the [Regional availability](models-region-compatibility.md) page for more details.


| **Region** | **In-Region** | **Geo** | **Global** | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

***Geo inference details***

**Geo: US**

Geo Inference ID: `us.deepseek.r1-v1:0`


| **Source Region** | **Destination Regions** | 
| --- | --- | 
| us-east-1 (N. Virginia) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-east-2 (Ohio) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-west-2 (Oregon) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 

## Quotas and Limits
<a name="model-card-deepseek-deepseek-r1-quotas"></a>

Your AWS account has default quotas to maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock. The default quotas assigned to an account might be updated depending on regional factors, payment history, fraudulent usage, and/or approval of a quota [increase request](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-increase.html). For more details, please refer to [Quotas for Amazon Bedrock](quotas.md) documentation and see the [limits](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) for the model.

## Sample Code
<a name="model-card-deepseek-deepseek-r1-sample-code"></a>

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
    modelId='deepseek.r1-v1:0',
    body=json.dumps({
            'messages': [{ 'role': 'user', 'content': 'Can you explain the features of Amazon Bedrock?'}],
            'max_tokens': 1024
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
    modelId='deepseek.r1-v1:0',
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