

# GPT-5.4
<a name="model-card-openai-gpt-54"></a>

## ![Icon showing a circular pattern with interwoven curved segments forming a pinwheel design.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/models/openai.png) OpenAI — GPT-5.4
<a name="model-card-openai-gpt-54-header"></a>

## Model Details
<a name="model-card-openai-gpt-54-details"></a>

GPT-5.4 brings frontier reasoning, coding, computer use, long-context workflows, and tool use to Amazon Bedrock. It helps developers build AI applications and production workflows that can interpret context, interact with tools, operate software environments, and verify outputs across multiple steps. GPT-5.4 is well suited for professional workflows that require reliable reasoning and action across complex business systems. For more information about model development and performance, see the [model/service card](https://deploymentsafety.openai.com/gpt-5-4-thinking/gpt-5-4-thinking.pdf).
+ **Model launch date:** June 1, 2026
+ **Model EOL date:** N/A
+ **End User License Agreements and Terms of Use:** [View](https://aws.amazon.com/legal/bedrock/third-party-models/)
+ **Model lifecycle:** Active
+ **Context window:** 272K tokens
+ **Max output tokens:** N/A


| **Input Modalities** | **Output Modalities** | **[APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html)** | **[Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)** | 
| --- | --- | --- | --- | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Audio | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Embedding | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Responses | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) bedrock-runtime | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Chat Completions | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) bedrock-mantle | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Invoke |  | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Converse |  | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video |  |  | 

**Note**  
This model is available on the `openai/v1/responses` path on the `bedrock-mantle` endpoint. This is different from the `v1/responses` path used by other models on the responses endpoint.

## Capabilities and Features
<a name="model-card-openai-gpt-54-capabilities"></a>

***Bedrock Features***

**Features supported using `bedrock-mantle` endpoint**


| **Supported** | **Not Supported** | 
| --- | --- | 
|  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html)  | — | 

## Pricing
<a name="model-card-openai-gpt-54-pricing"></a>

For pricing, please refer to the [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) page.

## Programmatic Access
<a name="model-card-openai-gpt-54-programmatic-access"></a>

Use the following model IDs and endpoint URLs to access this model programmatically. For more information about the available APIs and endpoints, see [APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html) and [Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html).


| **Endpoint** | **Model ID** | **In-Region endpoint URL** | **Geo inference ID** | **Global inference ID** | 
| --- | --- | --- | --- | --- | 
| bedrock-mantle | openai.gpt-5.4 | https://bedrock-mantle.{region}.api.aws/openai/v1 | Not supported | Not supported | 

*For example, if region is us-east-2 (Ohio), then the bedrock-mantle endpoint URL will be "https://bedrock-mantle.us-east-2.api.aws/openai/v1".*

## Service Tiers
<a name="model-card-openai-gpt-54-tiers"></a>

Amazon Bedrock offers multiple service tiers to match your workload requirements. **Standard** provides pay-per-token access with no commitment. **Priority** offers higher throughput with a time-based commitment. **Flex** provides lower-cost access for flexible, non-time-sensitive workloads. **Reserved** provides dedicated throughput with a term commitment for predictable workloads. For more information, see [service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html).


| **Standard** | **Priority** | **Flex** | **Reserved** | 
| --- | --- | --- | --- | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Regional Availability
<a name="model-card-openai-gpt-54-regional-availability"></a>

***Regional availability at a glance***

Bedrock offers three inference options: **In-Region** keeps requests within a single Region for strict compliance, **Geo Cross-Region** routes across Regions within a geography (US, EU, etc.) for higher throughput while respecting data residency, and **Global Cross-Region** routes anywhere worldwide for maximum throughput when there are no residency constraints. Refer to the [Regional availability](models-region-compatibility.md) page for more details.


| **Region** | **In-Region** | **Geo** | **Global** | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Quotas and Limits
<a name="model-card-openai-gpt-54-quotas"></a>

Your AWS account has default quotas to maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock. The default quotas assigned to an account might be updated depending on regional factors, payment history, fraudulent usage, and/or approval of a quota [increase request](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-increase.html). For more details, please refer to [Quotas for Amazon Bedrock](quotas.md) documentation and see the [limits](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) for the model.

## Sample Code
<a name="model-card-openai-gpt-54-sample-code"></a>

**Step 1 - AWS Account:** If you have an AWS account already, skip this step. If you are new to AWS, sign up for an [AWS account](https://portal.aws.amazon.com/billing/signup).

**Step 2 - API key:** Go to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/home#/api-keys/long-term/create) and generate a long-term API key.

**Step 3 - Get the SDK:** To use this getting started guide, you must have Python already installed. Then install the relevant software depending on the APIs you are using.

------
#### [ Responses API ]

```
pip install openai
```

------

**Step 4 - Set environment variables:** Configure your environment to use the API key for authentication.

------
#### [ Responses API ]

```
OPENAI_API_KEY="<provide your Bedrock API key>"
OPENAI_BASE_URL="https://bedrock-mantle.us-west-2.api.aws/openai/v1"
```

------

**Step 5 - Run your first inference request:** Save the file as `bedrock-first-request.py`

------
#### [ Responses API ]

```
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="openai.gpt-5.4",
    input="Can you explain the features of Amazon Bedrock?"
)
print(response)
```

------