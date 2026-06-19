

# Embed v4
<a name="model-card-cohere-embed-v4"></a>

## ![Three overlapping circles in dark green, coral, and purple colors forming a logo or icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/models/cohere.png) Cohere — Embed v4
<a name="model-card-cohere-embed-v4-header"></a>

## Model Details
<a name="model-card-cohere-embed-v4-details"></a>

Embed v4 is Cohere's unified multimodal embedding model that processes text, images, and mixed content in a single model for search and RAG. For more information about model development and performance, see the [model/service card](https://docs.cohere.com/docs/cohere-embed).
+ **Model launch date:** Apr 15, 2025
+ **Model EOL date:** N/A
+ **End User License Agreements and Terms of Use:** [View](https://aws.amazon.com/legal/bedrock/third-party-models/)
+ **Model lifecycle:** Active
+ **Context window:** 128K tokens
+ **Marketplace product ID:** `prod-ft3cj5gst3spo`


| **Input Modalities** | **Output Modalities** | **[APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html)** | **[Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)** | 
| --- | --- | --- | --- | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Audio | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Embedding | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Responses | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) bedrock-runtime | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Image | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Chat Completions | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) bedrock-mantle | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Speech | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Invoke |  | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) Text | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Text | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Converse |  | 
| ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) Video |  |  | 

## Capabilities and Features
<a name="model-card-cohere-embed-v4-capabilities"></a>

***Bedrock Features***

**Features supported using `bedrock-runtime` endpoint**


| **Supported** | **Not Supported** | 
| --- | --- | 
|  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-cohere-embed-v4.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-cohere-embed-v4.html)  | 

## Pricing
<a name="model-card-cohere-embed-v4-pricing"></a>

For pricing, please refer to the [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) page.

## Programmatic Access
<a name="model-card-cohere-embed-v4-programmatic-access"></a>

Use the following model IDs and endpoint URLs to access this model programmatically. For more information about the available APIs and endpoints, see [APIs supported](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html) and [Endpoints supported](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html).


| **Endpoint** | **Model ID** | **In-Region endpoint URL** | **Geo inference ID** | **Global inference ID** | 
| --- | --- | --- | --- | --- | 
| bedrock-runtime | cohere.embed-v4:0 | https://bedrock-runtime.{region}.amazonaws.com | `us.cohere.embed-v4:0`<br />`eu.cohere.embed-v4:0` | global.cohere.embed-v4:0 | 

*For example, if region is us-east-1 (N. Virginia), then the bedrock-runtime endpoint URL will be "https://bedrock-runtime.us-east-1.amazonaws.com" and for bedrock-mantle will be "https://bedrock-mantle.us-east-1.api.aws/v1".*

## Service Tiers
<a name="model-card-cohere-embed-v4-tiers"></a>

Amazon Bedrock offers multiple service tiers to match your workload requirements. **Standard** provides pay-per-token access with no commitment. **Priority** offers higher throughput with a time-based commitment. **Flex** provides lower-cost access for flexible, non-time-sensitive workloads. **Reserved** provides dedicated throughput with a term commitment for predictable workloads. For more information, see [service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html).


| **Standard** | **Priority** | **Flex** | **Reserved** | 
| --- | --- | --- | --- | 
| ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Regional Availability
<a name="model-card-cohere-embed-v4-regional-availability"></a>

***Regional availability at a glance***

Bedrock offers three inference options: **In-Region** keeps requests within a single Region for strict compliance, **Geo Cross-Region** routes across Regions within a geography (US, EU, etc.) for higher throughput while respecting data residency, and **Global Cross-Region** routes anywhere worldwide for maximum throughput when there are no residency constraints. Refer to the [Regional availability](models-region-compatibility.md) page for more details.


| **Region** | **In-Region** | **Geo** | **Global** | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Red circle with white X icon indicating error, cancel, or close action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![Green circle with white checkmark icon.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

***Geo inference details***

**Geo: US**

Geo Inference ID: `us.cohere.embed-v4:0`


| **Source Region** | **Destination Regions** | 
| --- | --- | 
| us-east-1 (N. Virginia) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-east-2 (Ohio) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 
| us-west-1 (N. California) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-1 (N. California), us-west-2 (Oregon) | 
| us-west-2 (Oregon) | us-east-1 (N. Virginia), us-east-2 (Ohio), us-west-2 (Oregon) | 

**Geo: EU**

Geo Inference ID: `eu.cohere.embed-v4:0`


| **Source Region** | **Destination Regions** | 
| --- | --- | 
| eu-central-1 (Frankfurt) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-central-2 (Zurich) | eu-central-1 (Frankfurt), eu-central-2 (Zurich), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-north-1 (Stockholm) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-south-1 (Milan) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-south-2 (Spain) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-west-1 (Ireland) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 
| eu-west-2 (London) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-2 (London), eu-west-3 (Paris) | 
| eu-west-3 (Paris) | eu-central-1 (Frankfurt), eu-north-1 (Stockholm), eu-south-1 (Milan), eu-south-2 (Spain), eu-west-1 (Ireland), eu-west-3 (Paris) | 

***Global inference details***


| **Global Inference ID** | **Americas** | **EMEA** | **Asia Pacific** | 
| --- | --- | --- | --- | 
| global.cohere.embed-v4:0 |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-cohere-embed-v4.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-cohere-embed-v4.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/model-card-cohere-embed-v4.html)  | 

## Quotas and Limits
<a name="model-card-cohere-embed-v4-quotas"></a>

Your AWS account has default quotas to maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock. The default quotas assigned to an account might be updated depending on regional factors, payment history, fraudulent usage, and/or approval of a quota [increase request](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-increase.html). For more details, please refer to [Quotas for Amazon Bedrock](quotas.md) documentation and see the [limits](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) for the model.

## Sample Code
<a name="model-card-cohere-embed-v4-sample-code"></a>

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
    modelId='cohere.embed-v4:0',
    body=json.dumps({
            'texts': ['What are the different services that you offer?'],
            'input_type': 'search_document',
            'embedding_types': ['float']
    })
)
print(json.loads(response['body'].read()))
```

------