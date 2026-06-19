

# Endpoint availability
<a name="models-endpoint-availability"></a>

Amazon Bedrock supports two endpoints: bedrock-runtime and bedrock-mantle. Please refer to the [Endpoints supported by Amazon Bedrock](endpoints.md) to learn more about how to choose between the two endpoints.


| **Endpoint** | **Supported APIs** | **Description** | 
| --- | --- | --- | 
| bedrock-mantle.{region}.api.aws | [Responses API](bedrock-mantle.md) / [Chat Completions API](bedrock-mantle.md) / [Messages API](model-parameters-anthropic-claude-messages.md) | Region-specific endpoints for making inference requests for models hosted in Amazon Bedrock using the OpenAI-compatible endpoints and the Anthropic Messages API. | 
| bedrock-runtime.{region}.amazonaws.com | [InvokeModel](inference-invoke.md) / [Converse](conversation-inference.md) / [Chat Completions](inference-chat-completions.md) / [Messages API](model-parameters-anthropic-claude-messages.md) | Region-specific endpoints for making inference requests for models hosted in Amazon Bedrock using the InvokeModel/Converse/Chat Completions/Messages APIs. Read more on Amazon Bedrock Runtime APIs [here](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html). | 

The following tables show which Amazon Bedrock endpoints support each model, organized by provider.

## AI21 Labs
<a name="model-endpoints-ai21-labs"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Jamba 1.5 Large](model-card-ai21-labs-jamba-1-5-large.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Jamba 1.5 Mini](model-card-ai21-labs-jamba-1-5-mini.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Amazon
<a name="model-endpoints-amazon"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Amazon Nova Multimodal Embeddings](model-card-amazon-amazon-nova-multimodal-embeddings.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova 2 Lite](model-card-amazon-nova-2-lite.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova 2 Sonic](model-card-amazon-nova-2-sonic.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Canvas](model-card-amazon-nova-canvas.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Lite](model-card-amazon-nova-lite.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Micro](model-card-amazon-nova-micro.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Premier](model-card-amazon-nova-premier.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Pro](model-card-amazon-nova-pro.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Reel](model-card-amazon-nova-reel.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Nova Sonic](model-card-amazon-nova-sonic.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Titan Embeddings G1 - Text](model-card-amazon-titan-embeddings-g1---text.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Titan Image Generator G1 v2](model-card-amazon-titan-image-generator-g1-v2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Titan Multimodal Embeddings G1](model-card-amazon-titan-multimodal-embeddings-g1.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Titan Text Embeddings V2](model-card-amazon-titan-text-embeddings-v2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Titan Embeddings G1 - Text v2](model-card-amazon-titan-text-embeddings-v2-2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Anthropic
<a name="model-endpoints-anthropic"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Claude Mythos 5](model-card-anthropic-claude-mythos-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude Fable 5](model-card-anthropic-claude-fable-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude Mythos Preview](model-card-anthropic-claude-mythos-preview.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude 3 Haiku](model-card-anthropic-claude-3-haiku.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude 3.5 Haiku](model-card-anthropic-claude-3-5-haiku.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Haiku 4.5](model-card-anthropic-claude-haiku-4-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude Opus 4.1](model-card-anthropic-claude-opus-4-1.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Opus 4.5](model-card-anthropic-claude-opus-4-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Opus 4.6](model-card-anthropic-claude-opus-4-6.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Opus 4.7](model-card-anthropic-claude-opus-4-7.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude Opus 4.8](model-card-anthropic-claude-opus-4-8.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Claude Sonnet 4](model-card-anthropic-claude-sonnet-4.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Sonnet 4.5](model-card-anthropic-claude-sonnet-4-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Claude Sonnet 4.6](model-card-anthropic-claude-sonnet-4-6.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Cohere
<a name="model-endpoints-cohere"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Command R](model-card-cohere-command-r.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Command R\+](model-card-cohere-command-r-plus.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Embed English](model-card-cohere-embed-english.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Embed Multilingual](model-card-cohere-embed-multilingual.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Embed v4](model-card-cohere-embed-v4.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Rerank 3.5](model-card-cohere-rerank-3-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## DeepSeek
<a name="model-endpoints-deepseek"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [DeepSeek V3.2](model-card-deepseek-deepseek-v3-2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [DeepSeek-R1](model-card-deepseek-deepseek-r1.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [DeepSeek-V3.1](model-card-deepseek-deepseek-v3-1.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Google
<a name="model-endpoints-google"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Gemma 3 12B IT](model-card-google-gemma-3-12b-it.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Gemma 3 27B PT](model-card-google-gemma-3-27b-pt.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Gemma 3 4B IT](model-card-google-gemma-3-4b-it.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Meta
<a name="model-endpoints-meta"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Llama 3 70B Instruct](model-card-meta-llama-3-70b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3 8B Instruct](model-card-meta-llama-3-8b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.1 405B Instruct](model-card-meta-llama-3-1-405b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.1 70B Instruct](model-card-meta-llama-3-1-70b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.1 8B Instruct](model-card-meta-llama-3-1-8b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.2 11B Instruct](model-card-meta-llama-3-2-11b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.2 1B Instruct](model-card-meta-llama-3-2-1b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.2 3B Instruct](model-card-meta-llama-3-2-3b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.2 90B Instruct](model-card-meta-llama-3-2-90b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 3.3 70B Instruct](model-card-meta-llama-3-3-70b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 4 Maverick 17B Instruct](model-card-meta-llama-4-maverick-17b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Llama 4 Scout 17B Instruct](model-card-meta-llama-4-scout-17b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## MiniMax
<a name="model-endpoints-minimax"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [MiniMax M2](model-card-minimax-minimax-m2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [MiniMax M2.1](model-card-minimax-minimax-m2-1.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [MiniMax M2.5](model-card-minimax-minimax-m2-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Mistral AI
<a name="model-endpoints-mistral-ai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Devstral 2 123B](model-card-mistral-ai-devstral-2-123b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Magistral Small 2509](model-card-mistral-ai-magistral-small-2509.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Ministral 14B 3.0](model-card-mistral-ai-ministral-14b-3-0.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Ministral 3 8B](model-card-mistral-ai-ministral-3-8b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Ministral 3B](model-card-mistral-ai-ministral-3b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Mistral 7B Instruct](model-card-mistral-ai-mistral-7b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Mistral Large](model-card-mistral-ai-mistral-large.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Mistral Large 3](model-card-mistral-ai-mistral-large-3.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Mistral Small](model-card-mistral-ai-mistral-small.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Mixtral 8x7B Instruct](model-card-mistral-ai-mixtral-8x7b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Pixtral Large](model-card-mistral-ai-pixtral-large.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Voxtral Mini 3B 2507](model-card-mistral-ai-voxtral-mini-3b-2507.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Voxtral Small 24B 2507](model-card-mistral-ai-voxtral-small-24b-2507.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Moonshot AI
<a name="model-endpoints-moonshot-ai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Kimi K2 Thinking](model-card-moonshot-ai-kimi-k2-thinking.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Kimi K2.5](model-card-moonshot-ai-kimi-k2-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## NVIDIA
<a name="model-endpoints-nvidia"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [NVIDIA Nemotron Nano 9B v2](model-card-nvidia-nvidia-nemotron-nano-9b-v2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [NVIDIA Nemotron Nano 12B v2 VL BF16](model-card-nvidia-nvidia-nemotron-nano-12b-v2-vl-bf16.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Nemotron Nano 3 30B](model-card-nvidia-nemotron-nano-3-30b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [NVIDIA Nemotron 3 Super 120B](model-card-nvidia-nemotron-super-3-120b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## OpenAI
<a name="model-endpoints-openai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [GPT-5.5](model-card-openai-gpt-55.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [GPT-5.4](model-card-openai-gpt-54.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [GPT OSS Safeguard 120B](model-card-openai-gpt-oss-safeguard-120b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [GPT OSS Safeguard 20B](model-card-openai-gpt-oss-safeguard-20b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [gpt-oss-120b](model-card-openai-gpt-oss-120b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [gpt-oss-20b](model-card-openai-gpt-oss-20b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Qwen
<a name="model-endpoints-qwen"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Qwen3 235B A22B 2507](model-card-qwen-qwen3-235b-a22b-2507.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3 32B](model-card-qwen-qwen3-32b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3 Coder 480B A35B Instruct](model-card-qwen-qwen3-coder-480b-a35b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3 Coder Next](model-card-qwen-qwen3-coder-next.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3 Next 80B A3B](model-card-qwen-qwen3-next-80b-a3b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3 VL 235B A22B](model-card-qwen-qwen3-vl-235b-a22b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Qwen3-Coder-30B-A3B-Instruct](model-card-qwen-qwen3-coder-30b-a3b-instruct.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Stability AI
<a name="model-endpoints-stability-ai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Stable Image Conservative Upscale](model-card-stability-ai-stable-image-conservative-upscale.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Control Sketch](model-card-stability-ai-stable-image-control-sketch.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Control Structure](model-card-stability-ai-stable-image-control-structure.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Creative Upscale](model-card-stability-ai-stable-image-creative-upscale.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Erase Object](model-card-stability-ai-stable-image-erase-object.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Fast Upscale](model-card-stability-ai-stable-image-fast-upscale.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Inpaint](model-card-stability-ai-stable-image-inpaint.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Outpaint](model-card-stability-ai-stable-image-outpaint.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Remove Background](model-card-stability-ai-stable-image-remove-background.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Search and Recolor](model-card-stability-ai-stable-image-search-and-recolor.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Search and Replace](model-card-stability-ai-stable-image-search-and-replace.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Style Guide](model-card-stability-ai-stable-image-style-guide.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Stable Image Style Transfer](model-card-stability-ai-stable-image-style-transfer.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## TwelveLabs
<a name="model-endpoints-twelvelabs"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Marengo Embed 3.0](model-card-twelvelabs-marengo-embed-3-0.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Marengo Embed v2.7](model-card-twelvelabs-marengo-embed-v2-7.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Pegasus v1.2](model-card-twelvelabs-pegasus-v1-2.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Writer
<a name="model-endpoints-writer"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Palmyra Vision 7B](model-card-writer-palmyra-vision-7b.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [Palmyra X4](model-card-writer-palmyra-x4.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| [Palmyra X5](model-card-writer-palmyra-x5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## xAI
<a name="model-endpoints-xai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [Grok 4.3](model-card-xai-grok-4-3.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Z.AI
<a name="model-endpoints-z.ai"></a>


| Model name | `bedrock-runtime` | `bedrock-mantle` | 
| --- | --- | --- | 
| [GLM 4.7](model-card-zai-glm-4-7.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [GLM 4.7 Flash](model-card-zai-glm-4-7-flash.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| [GLM 5](model-card-zai-glm-5.md) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 