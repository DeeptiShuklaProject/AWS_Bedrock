

# Understanding intelligent prompt routing in Amazon Bedrock
<a name="prompt-routing"></a>

Amazon Bedrock intelligent prompt routing provides a single serverless endpoint to efficiently route requests between different foundational models within the same model family. It can dynamically predict the response quality of each model for each request, and then route the request to the model with the best response quality. This helps to optimize for both response quality and cost.

**Topics**
+ [Supported Regions and models for intelligent prompt routing](#prompt-routing-support)
+ [Benefits](#prompt-routing-benefits)
+ [Default and configured prompt routers](#prompt-routing-types)
+ [Considerations and limitations](#prompt-routing-limitations)
+ [Prompt router criteria and fallback model](#prompt-router-criteria)
+ [How intelligent prompt routing works](#prompt-routing-works)
+ [How to use intelligent prompt routing](#prompt-routing-use)

## Supported Regions and models for intelligent prompt routing
<a name="prompt-routing-support"></a>

Intelligent prompt routing can be used with different types of models. The following list describes support for different types of Amazon Bedrock models:
+ **Single-region model support** – Lists regions that support sending inference requests to a foundation model in one AWS Region. For a full table of models available across Amazon Bedrock, see [Supported foundation models in Amazon Bedrock](models-supported.md).
+ **Cross-region inference profile support** – Lists regions that support using a cross-region inference profile, which support sending inference requests to a foundation model in multiple AWS regions within a geographical area. An inference profile has a prefix preceding the model ID that indicates its geographical area (for example, `us.`, `apac`). For more information for available inference profiles across Amazon Bedrock, see [Supported Regions and models for inference profiles](inference-profiles-support.md).

The following table shows models supported for intelligent prompt routing:


| Provider | Model | Model ID | Single-region model support | Cross-region inference profile support | 
| --- | --- | --- | --- | --- | 
| Amazon | Nova Lite | amazon.nova-lite-v1:0 | us-east-1<br />us-gov-west-1 | ap-northeast-1<br />ap-northeast-2<br />ap-south-1<br />ap-southeast-2<br />eu-central-1<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-east-2<br />us-west-2 | 
| Amazon | Nova Pro | amazon.nova-pro-v1:0 | us-east-1<br />us-gov-west-1 | ap-northeast-1<br />ap-northeast-2<br />ap-south-1<br />ap-southeast-2<br />eu-central-1<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-east-2<br />us-west-2 | 
| Anthropic | Claude 3 Haiku | anthropic.claude-3-haiku-20240307-v1:0 | ap-northeast-1<br />ap-northeast-2<br />ap-south-1<br />ap-southeast-2<br />eu-central-1<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-gov-west-1<br />us-west-2 | ap-northeast-1<br />ap-northeast-2<br />ap-south-1<br />ap-southeast-2<br />eu-central-1<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-east-2<br />us-gov-east-1<br />us-west-2 | 
| Anthropic | Claude 3.5 Haiku | anthropic.claude-3-5-haiku-20241022-v1:0 | us-west-2 | us-east-1<br />us-east-2<br />us-west-2 | 
| Anthropic | Claude 3.5 Sonnet | anthropic.claude-3-5-sonnet-20240620-v1:0 | ap-northeast-1<br />ap-northeast-2<br />eu-central-1<br />us-east-1<br />us-gov-west-1<br />us-west-2 | ap-northeast-1<br />ap-northeast-2<br />ap-south-1<br />ap-southeast-2<br />eu-central-1<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-east-2<br />us-gov-east-1<br />us-west-2 | 
| Anthropic | Claude 3.5 Sonnet v2 | anthropic.claude-3-5-sonnet-20241022-v2:0 | ap-southeast-2<br />us-west-2 | ap-northeast-1<br />ap-south-1<br />ap-southeast-2<br />eu-west-3<br />us-east-1<br />us-east-2<br />us-west-2 | 
| Meta | Llama 3.1 70B Instruct | meta.llama3-1-70b-instruct-v1:0 | us-west-2 | us-east-1<br />us-east-2<br />us-west-2 | 
| Meta | Llama 3.1 8B Instruct | meta.llama3-1-8b-instruct-v1:0 | us-west-2 | us-east-1<br />us-east-2<br />us-west-2 | 
| Meta | Llama 3.2 11B Instruct | meta.llama3-2-11b-instruct-v1:0 | N/A | us-east-1<br />us-east-2<br />us-west-2 | 
| Meta | Llama 3.2 90B Instruct | meta.llama3-2-90b-instruct-v1:0 | N/A | us-east-1<br />us-east-2<br />us-west-2 | 
| Meta | Llama 3.3 70B Instruct | meta.llama3-3-70b-instruct-v1:0 | us-east-2 | us-east-1<br />us-east-2<br />us-west-2 | 

## Benefits
<a name="prompt-routing-benefits"></a>
+ **Optimized Response Quality and Cost:** Routes prompts to different foundational models to achieve the best response quality at the lowest cost.
+ **Simplified Management:** Eliminates the need for complex orchestration logic.
+ **Future-Proof:** Incorporates new models as they become available.

## Default and configured prompt routers
<a name="prompt-routing-types"></a>

When using intelligent prompt routing, you can either use the default prompt routers provided by Amazon Bedrock, or configure your own prompt routers.

Default prompt routers are pre-configured routing systems provided by Amazon Bedrock. These routers come with predefined settings and are designed to work out-of-the-box with specific foundational models. They provide a straightforward, ready-to-use solution without needing to configure any routing settings. When starting with intelligent prompt routing, we recommend that you experiment using the default routers provided by Amazon Bedrock. During preview, you can choose to use select models in the Anthropic and Meta families.

Configured prompt routers enable you to define your own routing configurations tailored to specific needs and preferences. They are more suitable when you require more control over how to route your requests and which models to use. Configured routers enable optimization based on response quality metrics and use cases. After you've experimented with default routers, you can configure your own routers that are suitable to your applications, evaluate the response quality in the playground, and use for production applications if it meets the requirements.

## Considerations and limitations
<a name="prompt-routing-limitations"></a>

The following are considerations and limitations for intelligent prompt routing in Amazon Bedrock.
+ Intelligent prompt routing is only optimized for English prompts.
+ Intelligent prompt routing can’t adjust routing decisions or responses based on application-specific performance data.
+ Intelligent prompt routing might not always provide the most optimal routing for unique or specialized use cases. How effective the routing is depends on the initial training data.

## Prompt router criteria and fallback model
<a name="prompt-router-criteria"></a>

When configuring your prompt routers, you can specify the routing criteria, which is used to determine which model to select for processing a request based on the response quality difference. Use this criteria to determine how much closer the responses of the fallback model should be to the responses of the other models.

### Fallback models
<a name="prompt-router-criteria-fallback"></a>

Choose a fallback model that works well for your requests. This model serves as a reliable baseline. You can then choose another model to either improve accuracy or reduce costs compared to the fallback model. The fallback model acts as an anchor, and the routing criteria determines when to switch to the other model based on the response quality difference.

### Response quality difference
<a name="prompt-router-criteria-respquality"></a>

The response quality difference measures the disparity between the responses of the fallback model and the other models. A smaller value indicates that the responses are similar. A higher value indicates a significant difference in the responses between the fallback model and the other models.

For example, a response quality difference of 10% means that, say the response quality of the fallback model, Claude Haiku3, is 10%, then the router will switch to another model, say Claude Sonnet3, only if its responses are 10% better than Claude Haiku3's responses.

## How intelligent prompt routing works
<a name="prompt-routing-works"></a>

1. 

**Model selection and router configuration**

   Choose the family of models you want to use for your application. If you're using default prompt routers, you can choose from models in the Anthropic or Meta families. If you're using configured prompt routers, you can choose from additional models and configure the routing criteria. For more information, see [How to use intelligent prompt routing](#prompt-routing-use).

1. 

**Incoming request analysis**

   For each incoming request, the system analyzes the prompt to understand its content and context.

1. 

**Response quality prediction**

   Amazon Bedrock predicts the response quality of each specified model in the chosen family based on the prompt. If you configured your prompt router, it takes into account the routing criteria, which is the response quality difference, and routes requests to your specified fallback model if the criteria is not met.

1. 

**Model selection and request forwarding**

   Based on the response quality prediction, Amazon Bedrock dynamically chooses the model that offers the best combination of response quality and cost for the specific request. The request is then forwarded to the chosen model for processing.

1. 

**Response handling**

   The response from the chosen model is retrieved and returned to the user. The response includes information about the model that was used to process the request.

## How to use intelligent prompt routing
<a name="prompt-routing-use"></a>

To get started with intelligent prompt routing, use the Amazon Bedrock console, AWS CLI, or AWS SDK.

**Note**  
To best use intelligent prompt routing, you should regularly review performance to take advantage of new models. To optimize your usage, monitor the available performance and cost metrics.

The following sections show you how to use this feature from the console and the CLI. After you configure your prompt router, Amazon Bedrock will perform the steps described in [How intelligent prompt routing works](#prompt-routing-works) to generate a response from one of the models in the chosen router.

------
#### [ console ]

To use intelligent prompt routing from the AWS Management Console:

1. Go to the [Prompt Routers](https://console.aws.amazon.com/bedrock/home?region=us-east-1#/prompt-routers) hub in the Amazon Bedrock console. Use your AWS credentials to log in to the console.

1. Choose the model family that you want to use. If you're using the feature for the first time, you can experiment with the default prompt routers. During the preview, you can choose from models in the Anthropic or Meta families. You can then open the playground and experiment with your prompts.
**Note**  
You must choose exactly two models within the same family.

1. After you've experimented with the default routers, you can configure your router. You must provide a unique name for your router and an optional description.

1. Define the routing rules for routing the prompts to different models. Specify the models for routing, the routing criteria, and a fallback model to be used in case the routing criteria is not met.

1. You can now open the playground and try different prompts to monitor the performance of your prompt router. By analyzing how prompts are being routed and the performance of each model, you can adjust the routing criteria and models as needed to optimize for performance and cost.

------
#### [ API ]

To use intelligent prompt routing using the AWS CLI:

1. After you've experimented with default prompt routers, you can create a router that can handle intelligent prompt routing using the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreatePromptRouter.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreatePromptRouter.html) API or the [https://docs.aws.amazon.com/cli/latest/reference/bedrock/create-prompt-router.html](https://docs.aws.amazon.com/cli/latest/reference/bedrock/create-prompt-router.html) CLI command.

   The following command shows an example of creating the prompt router, where:
   + {{<router-name>}} is a unique name for your router.
   + {{<region>}} is the AWS Region where you want to create the router.
   + {{<modelA>}} and {{<modelB>}} are the models to choose from for routing. For example, `anthropic.claude-sonnet-4-5-20250929-v1:0`.

   ```
   aws bedrock create-prompt-router \
       --prompt-router-name {{<router-name>}} \
       --models '[{"modelArn": "arn:aws:bedrock:{{<region>}}::foundation-model/{{<modelA>}}"}]' \ 
       --fallback-model '[{"modelArn": "arn:aws:bedrock:{{<region>}}::foundation-model/{{<modelB>}}"}]' \ 
       --routing-criteria '{"responseQualityDifference": 0.5}'
   ```

1. Send your prompts to the intelligent prompt router using the AWS CLI. The router will predict the response quality of each model and route the request to the model with the best response quality.

1. Review the response to your request. It will contain information about the model that was used and the routing criteria.

1. As you work with prompt routers, you can also use these additional API operations:
   + [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetPromptRouter.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetPromptRouter.html)
   + [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListPromptRouters.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListPromptRouters.html)
   + [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeletePromptRouter.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeletePromptRouter.html)

------