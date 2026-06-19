

# Model lifecycle
<a name="model-lifecycle"></a>

Amazon Bedrock is continuously working to bring the latest versions of foundation models that have better capabilities, accuracy, and safety. As we launch new model versions, you can test them with the Amazon Bedrock console or API, and migrate your applications to benefit from the latest model versions. 

A model offered on Amazon Bedrock can be in one of these states: ** Active**, **Legacy**, or ** End-of-Life (EOL)**. You can see the status of offered models in the console and in the tables below. Additionally, when you make a [GetFoundationModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html) or [ListFoundationModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) call, the state of the model will be shown in the `modelLifecycle` field in the response. Once a model launches on Amazon Bedrock, it will remain on Amazon Bedrock for at least 12 months before the EOL date. 

**Note**  
Model lifecycle dates on this page are specific to Amazon Bedrock and may differ from dates published by model providers (such as Anthropic or Cohere). For Amazon Bedrock usage, only the dates on this page apply.

## Active versions
<a name="active-versions"></a>

**Active** — The model provider is actively working on this version. In most cases, model providers sunset a model after newer versions become available. For a list of currently active models and their supported regions, see [Regional availability](models-region-compatibility.md). For model specific details, see [Model cards](model-cards.md).

## Legacy and end-of-life (EOL) models
<a name="versions-for-legacy-and-eol"></a>

**Legacy** — We will notify you when a model provider moves a model to the Legacy state. **A model will be in the Legacy state for at least 6 months before the EOL date**. While you can continue to use a Legacy model during this period, you should plan to transition to an Active model before the EOL date. New customers can't use Legacy models and existing customers may lose access to Legacy models after 15 days of inactivity. 

**For models with EOL dates after February 1, 2026: ** After a minimum of 3 months in the Legacy state, a model will enter the public extended access portion of the Legacy period. During this public extended access period, active users of a Legacy model can continue to use it until the EOL date (for a minimum of 3 months), but you should expect higher pricing, which will be set by the model provider. When the model first enters the Legacy state, we will notify you of the provider's chosen date to transition a model to public extended access (which will be at least 3 months from notification) and pricing changes (if any). We will also notify you before any further pricing changes during the public extended access period. 

You can't create a new [Provisioned Throughput](prov-throughput.md) for models in the Legacy state.

**EOL** — After the EOL date, a model will be marked EOL in the console and in the following table. On, or soon after the EOL date, the model is no longer available for use in all AWS Regions and requests made to this version will fail, unless there is a private arrangement between you and the provider for continued access. You will need to migrate to the latest model by updating your application code before the EOL date. Migration will not happen automatically.

The following table shows models that are currently in the Legacy state or are pending end-of-life (EOL) on Amazon Bedrock. This table does not include Active models or models that have already passed their EOL date.



- **AI21 Labs**
  - **Model name:** Jamba 1.5 Large
  - **Model ID:** ai21.jamba-1-5-large-v1:0
  - **Regions:** us-east-1
  - **Legacy date:** May 26, 2026
  - **EOL date:** November 26, 2026
  - **Public extended access start date:** August 26, 2026

- **AI21 Labs**
  - **Model name:** Jamba 1.5 Mini
  - **Model ID:** ai21.jamba-1-5-mini-v1:0
  - **Regions:** us-east-1
  - **Legacy date:** May 26, 2026
  - **EOL date:** November 26, 2026
  - **Public extended access start date:** August 26, 2026

- **Amazon**
  - **Model name:** Nova Canvas
  - **Model ID:** amazon.nova-canvas-v1:0
  - **Regions:** ap-northeast-1, eu-west-1, us-east-1
  - **Legacy date:** March 30, 2026
  - **EOL date:** September 30, 2026
  - **Public extended access start date:** —

- **Amazon**
  - **Model name:** Nova Reel
  - **Model ID:** amazon.nova-reel-v1:0
  - **Regions:** ap-northeast-1, eu-west-1, us-east-1
  - **Legacy date:** March 30, 2026
  - **EOL date:** September 30, 2026
  - **Public extended access start date:** —

- **Amazon**
  - **Model name:** Nova Reel
  - **Model ID:** amazon.nova-reel-v1:1
  - **Regions:** us-east-1
  - **Legacy date:** March 30, 2026
  - **EOL date:** September 30, 2026
  - **Public extended access start date:** —

- **Amazon**
  - **Model name:** Nova Premier
  - **Model ID:** amazon.nova-premier-v1:0
  - **Regions:** us-east-1, us-east-2, us-west-2
  - **Legacy date:** March 13, 2026
  - **EOL date:** September 14, 2026
  - **Public extended access start date:** —

- **Amazon**
  - **Model name:** Nova Sonic
  - **Model ID:** amazon.nova-sonic-v1:0
  - **Regions:** ap-northeast-1, eu-north-1, us-east-1
  - **Legacy date:** March 13, 2026
  - **EOL date:** September 14, 2026
  - **Public extended access start date:** —

- **Amazon**
  - **Model name:** Titan Image Generator G1 v2
  - **Model ID:** amazon.titan-image-generator-v2:0
  - **Regions:** us-east-1, us-west-2
  - **Legacy date:** December 30, 2025
  - **EOL date:** June 30, 2026
  - **Public extended access start date:** —

- **Anthropic**
  - **Model name:** Claude Sonnet 4
  - **Model ID:** anthropic.claude-sonnet-4-20250514-v1:0
  - **Regions:** ap-northeast-1, eu-central-1, eu-north-1, eu-south-1, eu-south-2, eu-west-1, eu-west-3, us-east-1, us-east-2, us-west-1, us-west-2, ap-east-2, ap-northeast-2, ap-northeast-3, ap-south-1, ap-south-2, me-central-1, ap-southeast-1, ap-southeast-2, ap-southeast-3, ap-southeast-4, ap-southeast-5, ap-southeast-7, il-central-1
  - **Legacy date:** April 14, 2026
  - **EOL date:** October 14, 2026
  - **Public extended access start date:** July 14, 2026

- **Anthropic**
  - **Model name:** Claude 3 Haiku
  - **Model ID:** anthropic.claude-3-haiku-20240307-v1:0
  - **Regions:** ap-northeast-1, ap-southeast-2, eu-central-1, eu-west-1, eu-west-2, eu-west-3, us-east-1, us-east-2, us-west-2 / **Legacy date:** March 10, 2026 / **EOL date:** September 10, 2026 / **Public extended access start date:** June 10, 2026
  - **Regions:** us-gov-east-1, us-gov-west-1 / **Legacy date:** March 10, 2026 / **EOL date:** September 10, 2026 / **Public extended access start date:** June 10, 2026

- **Anthropic**
  - **Model name:** Claude 3 Sonnet
  - **Model ID:** anthropic.claude-3-sonnet-20240229-v1:0
  - **Regions:** eu-west-1, eu-west-3, us-east-1, us-west-2 / **Legacy date:** January 30, 2026 / **EOL date:** July 30, 2026 / **Public extended access start date:** —
  - **Regions:** ap-northeast-1, ap-northeast-2, ap-southeast-2 / **Legacy date:** January 30, 2026 / **EOL date:** July 30, 2026 / **Public extended access start date:** April 30, 2026

- **Anthropic**
  - **Model name:** Claude 3.5 Sonnet
  - **Model ID:** anthropic.claude-3-5-sonnet-20240620-v1:0
  - **Regions:** ap-northeast-1, ap-southeast-2 / **Legacy date:** January 30, 2026 / **EOL date:** July 30, 2026 / **Public extended access start date:** April 30, 2026
  - **Regions:** eu-central-2 / **Legacy date:** August 25, 2025 / **EOL date:** June 1, 2026 / **Public extended access start date:** December 1, 2025
  - **Regions:** us-gov-east-1, us-gov-west-1 / **Legacy date:** January 30, 2026 / **EOL date:** July 30, 2026 / **Public extended access start date:** April 30, 2026

- **Anthropic**
  - **Model name:** Claude 3.5 Sonnet v2
  - **Model ID:** anthropic.claude-3-5-sonnet-20241022-v2:0
  - **Regions:** ap-northeast-1, ap-northeast-3, ap-south-2, ap-southeast-2
  - **Legacy date:** January 30, 2026
  - **EOL date:** July 30, 2026
  - **Public extended access start date:** April 30, 2026

- **Anthropic**
  - **Model name:** Claude 3.7 Sonnet
  - **Model ID:** anthropic.claude-3-7-sonnet-20250219-v1:0
  - **Regions:** us-gov-east-1, us-gov-west-1
  - **Legacy date:** January 30, 2026
  - **EOL date:** July 30, 2026
  - **Public extended access start date:** April 30, 2026

- **Anthropic**
  - **Model name:** Claude 3.5 Haiku
  - **Model ID:** anthropic.claude-3-5-haiku-20241022-v1:0
  - **Regions:** us-east-1, us-east-2, us-west-2
  - **Legacy date:** December 19, 2025
  - **EOL date:** June 19, 2026
  - **Public extended access start date:** March 19, 2026

- **Anthropic**
  - **Model name:** Claude Opus 4
  - **Model ID:** anthropic.claude-opus-4-20250514-v1:0
  - **Regions:** us-east-1, us-east-2, us-west-2
  - **Legacy date:** October 1, 2025
  - **EOL date:** May 31, 2026
  - **Public extended access start date:** March 1, 2026

- **Cohere**
  - **Model name:** Command R
  - **Model ID:** cohere.command-r-v1:0
  - **Regions:** us-east-1, us-west-2
  - **Legacy date:** February 19, 2026
  - **EOL date:** August 19, 2026
  - **Public extended access start date:** May 19, 2026

- **Cohere**
  - **Model name:** Command R\+
  - **Model ID:** cohere.command-r-plus-v1:0
  - **Regions:** us-east-1, us-west-2
  - **Legacy date:** February 19, 2026
  - **EOL date:** August 19, 2026
  - **Public extended access start date:** May 19, 2026

- **Meta**
  - **Model name:** Llama 3.1 405B Instruct
  - **Model ID:** meta.llama3-1-405b-instruct-v1:0
  - **Regions:** us-east-2, us-west-2
  - **Legacy date:** January 7, 2026
  - **EOL date:** July 7, 2026
  - **Public extended access start date:** April 7, 2026

- **Meta**
  - **Model name:** Llama 3.2 11B Instruct
  - **Model ID:** meta.llama3-2-11b-instruct-v1:0
  - **Regions:** us-east-1, us-east-2, us-west-2
  - **Legacy date:** January 7, 2026
  - **EOL date:** July 7, 2026
  - **Public extended access start date:** April 7, 2026

- **Meta**
  - **Model name:** Llama 3.2 1B Instruct
  - **Model ID:** meta.llama3-2-1b-instruct-v1:0
  - **Regions:** eu-central-1, eu-west-1, eu-west-3, us-east-1, us-east-2, us-west-2
  - **Legacy date:** January 7, 2026
  - **EOL date:** July 7, 2026
  - **Public extended access start date:** April 7, 2026

- **Meta**
  - **Model name:** Llama 3.2 3B Instruct
  - **Model ID:** meta.llama3-2-3b-instruct-v1:0
  - **Regions:** eu-central-1, eu-west-1, eu-west-3, us-east-1, us-east-2, us-west-2
  - **Legacy date:** January 7, 2026
  - **EOL date:** July 7, 2026
  - **Public extended access start date:** April 7, 2026

- **Meta**
  - **Model name:** Llama 3.2 90B Instruct
  - **Model ID:** meta.llama3-2-90b-instruct-v1:0
  - **Regions:** us-east-1, us-east-2, us-west-2
  - **Legacy date:** January 7, 2026
  - **EOL date:** July 7, 2026
  - **Public extended access start date:** April 7, 2026



The public extended access date indicates when a Legacy model enters the public extended access portion of the Legacy period. During this phase, pricing may increase as set by the model provider. The model remains available until its EOL date.

**Customized Models and Lifecycle Behavior**

When a foundation model transitions to the Legacy state, customization capabilities become restricted. If you previously fine-tuned or customized the model before it entered the Legacy state, you may:
+ Create a new custom model deployment for on-demand inference.
+ Continue using any existing on-demand deployments or any existing Provisioned Throughput (PT) endpoints, provided they were created before the model entered Legacy state.

However, once the model is in Legacy state, you cannot create new fine-tuning jobs on that model. You cannot create new Provisioned Throughput (PT) endpoints. New customers cannot start using the legacy model and existing customers may lose access after 15 days of inactivity.

Because Legacy models are scheduled for retirement, customers are strongly encouraged to begin transitioning workloads and customized deployments to an Active model as soon as the Legacy announcement is made, and complete migration before the model's End-of-Life (EOL) date.