

# Optimize model inference for latency
<a name="latency-optimized-inference"></a>

**Note**  
The Latency Optimized Inference feature is in preview release for Amazon Bedrock and is subject to change.

Latency-optimized inference for foundation models in Amazon Bedrock delivers faster response times and improved responsiveness for AI applications. The optimized versions of [https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html), [Anthropic's Claude 3.5 Haiku model](https://aws.amazon.com/bedrock/claude/) and [Meta's Llama 3.1 405B and 70B models](https://aws.amazon.com/bedrock/llama/) offer significantly reduced latency without compromising accuracy. 

Accessing the latency optimization capability requires no additional setup or model fine-tuning, allowing for immediate enhancement of existing applications with faster response times. You can set the “Latency” parameter to “optimized” while calling the Amazon Bedrock runtime API. If you select "standard" as your invocation option, your requests will be served by standard inference. By default all requests are routed to through "standard".

```
"performanceConfig" : {
    "latency" : "standard | optimized" 
}
```

Once you reach the usage quota for latency optimization for a model, we will attempt to serve the request with Standard latency. In such cases, the request will be charged at Standard latency rates. The latency configuration for a served request is visible in API response and AWS CloudTrail logs. You can also view metrics for latency optimized requests in Amazon CloudWatch logs under "model-id\+latency-optimized".

Latency optimized inference is available for Meta’s Llama 3.1 70B and 405B, as well as Anthropic’s Claude 3.5 Haiku in the US East (Ohio) and US West (Oregon) Regions via [cross-Region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html).

Latency optimized inference is available for Amazon Nova Pro in the US East (N. Virginia), US East (Ohio), and US West (Oregon) Regions via [cross-Region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html).

For more information about pricing, visit the [pricing page](https://aws.amazon.com/bedrock/pricing/).

**Note**  
 Latency optimized inference for Llama 3.1 405B currently supports requests with total input and output token count up to 11K. For larger token count requests, we will fall back to the standard mode. 

The following table shows the inference profiles that support latency optimization:


| Provider | Model | Model ID | Cross-region inference profile support | 
| --- | --- | --- | --- | 
| Amazon | Nova Pro | amazon.nova-pro-v1:0 | us-east-1<br />us-east-2 | 
| Anthropic | Claude 3.5 Haiku | anthropic.claude-3-5-haiku-20241022-v1:0 | us-east-2<br />us-west-2 | 
| Meta | Llama 3.1 405B Instruct | meta.llama3-1-405b-instruct-v1:0 | us-east-2 | 
| Meta | Llama 3.1 70B Instruct | meta.llama3-1-70b-instruct-v1:0 | us-east-2<br />us-west-2 | 

For more information about inference profiles, see [Supported Regions and models for inference profiles](inference-profiles-support.md).