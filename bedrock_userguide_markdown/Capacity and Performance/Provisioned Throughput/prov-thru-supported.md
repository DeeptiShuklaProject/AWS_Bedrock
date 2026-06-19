

# Supported Region and models for Provisioned Throughput
<a name="prov-thru-supported"></a>

If you purchase Provisioned Throughput through the Amazon Bedrock API, you must specify a contextual variant of Amazon Bedrock FMs for the model ID.

**Note**  
Provisioned Throughput is supported in AWS GovCloud (US-West) only for custom models with a no-commitment purchase. Use the ID of a custom model when purchasing Provisioned Throughput for it.

The following table shows the models for which you can purchase Provisioned Throughput, the model ID to use when purchasing Provisioned Throughput, and the AWS Regions in which you can purchase Provisioned Throughput for the model.


| Provider | Model | Model ID | Single-region model support | 
| --- | --- | --- | --- | 
| Amazon | Nova 2 Lite | amazon.nova-2-lite-v1:0:256k | us-east-1 | 
| Amazon | Nova Canvas | amazon.nova-canvas-v1:0 | us-east-1 | 
| Amazon | Nova Lite | amazon.nova-lite-v1:0:24k | us-east-1 | 
| Amazon | Nova Lite | amazon.nova-lite-v1:0:300k | us-east-1 | 
| Amazon | Nova Micro | amazon.nova-micro-v1:0:128k | us-east-1 | 
| Amazon | Nova Micro | amazon.nova-micro-v1:0:24k | us-east-1 | 
| Amazon | Nova Pro | amazon.nova-pro-v1:0:24k | us-east-1 | 
| Amazon | Nova Pro | amazon.nova-pro-v1:0:300k | us-east-1 | 
| Amazon | Titan Embeddings G1 - Text | amazon.titan-embed-text-v1:2:8k | us-east-1<br />us-west-2 | 
| Amazon | Titan Image Generator G1 v2 | amazon.titan-image-generator-v2:0 | us-east-1<br />us-west-2 | 
| Amazon | Titan Multimodal Embeddings G1 | amazon.titan-embed-image-v1:0 | ap-south-1<br />ap-southeast-2<br />ca-central-1<br />eu-central-1<br />eu-west-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude | anthropic.claude-v2:0:100k | us-east-1<br />us-west-2 | 
| Anthropic | Claude | anthropic.claude-v2:0:18k | us-east-1<br />us-west-2 | 
| Anthropic | Claude | anthropic.claude-v2:1:18k | eu-central-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude | anthropic.claude-v2:1:200k | eu-central-1<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3 Haiku | anthropic.claude-3-haiku-20240307-v1:0:200k | ap-southeast-2<br />eu-west-3<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3 Haiku | anthropic.claude-3-haiku-20240307-v1:0:48k | ap-south-1<br />ap-southeast-2<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3 Sonnet | anthropic.claude-3-sonnet-20240229-v1:0:200k | ap-southeast-2<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3 Sonnet | anthropic.claude-3-sonnet-20240229-v1:0:28k | ap-south-1<br />ap-southeast-2<br />eu-west-1<br />eu-west-3<br />us-east-1<br />us-west-2 | 
| Anthropic | Claude 3.5 Sonnet | anthropic.claude-3-5-sonnet-20240620-v1:0:18k | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet | anthropic.claude-3-5-sonnet-20240620-v1:0:200k | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet | anthropic.claude-3-5-sonnet-20240620-v1:0:51k | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet v2 | anthropic.claude-3-5-sonnet-20241022-v2:0:18k | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet v2 | anthropic.claude-3-5-sonnet-20241022-v2:0:200k | us-west-2 | 
| Anthropic | Claude 3.5 Sonnet v2 | anthropic.claude-3-5-sonnet-20241022-v2:0:51k | us-west-2 | 
| Anthropic | Claude Instant | anthropic.claude-instant-v1:2:100k | us-east-1<br />us-west-2 | 
| Cohere | Embed English | cohere.embed-english-v3:0:512 | ca-central-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Cohere | Embed Multilingual | cohere.embed-multilingual-v3:0:512 | ca-central-1<br />eu-west-2<br />eu-west-3<br />sa-east-1<br />us-east-1<br />us-west-2 | 
| Meta | Llama 3.1 70B Instruct | meta.llama3-1-70b-instruct-v1:0:128k | us-west-2 | 
| Meta | Llama 3.1 8B Instruct | meta.llama3-1-8b-instruct-v1:0:128k | us-west-2 | 
| Meta | Llama 3.2 11B Instruct | meta.llama3-2-11b-instruct-v1:0:128k | us-west-2 | 
| Meta | Llama 3.2 1B Instruct | meta.llama3-2-1b-instruct-v1:0:128k | us-west-2 | 
| Meta | Llama 3.2 3B Instruct | meta.llama3-2-3b-instruct-v1:0:128k | us-west-2 | 
| Meta | Llama 3.2 90B Instruct | meta.llama3-2-90b-instruct-v1:0:128k | us-west-2 | 

**Note**  
The following models don't support no-commitment purchases for the base model:  
Titan Image Generator G1 V1
Titan Image Generator G1 V2