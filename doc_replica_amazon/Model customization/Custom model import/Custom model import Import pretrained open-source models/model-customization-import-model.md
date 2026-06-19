

# Use Custom model import to import a customized open-source model into Amazon Bedrock
<a name="model-customization-import-model"></a>

You can create a custom model in Amazon Bedrock by using the Amazon Bedrock Custom Model Import feature to import Foundation Models that you have customized in other environments, such as Amazon SageMaker AI. For example, you might have a model that you have created in Amazon SageMaker AI that has proprietary model weights. You can now import that model into Amazon Bedrock and then use Amazon Bedrock features to make inference calls to the model. 

You can use a model that you import with on demand throughput. Use the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) operations to make inference calls to the model. For more information, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md).

Custom model import is supported in the following regions:
+ eu-central-1
+ us-east-1
+ us-east-2
+ us-west-2

**Note**  
Make sure that your import and use of the models in Amazon Bedrock complies with the terms or licenses applicable to the models.  
You can't use Custom Model Import with the following Amazon Bedrock features.  
Batch inference
CloudFormation

With Custom Model Import you can create a custom model that supports the following patterns.
+ **Fine-tuned model** — You can customize the model weights using proprietary data, but retain the configuration of the base model. 
+ **Adaptation** You can customize the model to your domain for use cases where the model doesn't generalize well. Domain adaptation modifies a model to generalize for a target domain and deal with discrepancies across domains, such as a financial industry wanting to create a model which generalizes well on pricing. Another example is language adaptation. For example you could customize a model to generate responses in Portuguese or Tamil. Most often, this involves changes to the vocabulary of the model that you are using.
+ **Pretrained from scratch** — In addition to customizing the weights and vocabulary of the model, you can also change model configuration parameters such as the number of attention heads, hidden layers, or context length.

For information regarding pricing for custom model import, select the Custom Model Import tab in the Model pricing details section of [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).

**Topics**
+ [Supported architectures](#model-customization-import-model-architecture)
+ [Import a model source from Amazon S3](#model-customization-import-model-source)
+ [Prerequisites for importing custom model](custom-model-import-prereq.md)
+ [Submit a model import job](model-customization-import-model-job.md)
+ [Invoke your imported model](invoke-imported-model.md)
+ [Handling Custom Chat Templates and Tokenizers](custom-chat-templates-tokenizers.md)
+ [Calculate the cost of running a custom model](import-model-calculate-cost.md)
+ [Code samples for custom model import](custom-model-import-code-samples.md)

## Supported architectures
<a name="model-customization-import-model-architecture"></a>

The model you import must be in one of the following architectures.
+ **Mistral** — A decoder-only Transformer based architecture with Sliding Window Attention (SWA) and options for Grouped Query Attention (GQA). For more information, see [https://huggingface.co/docs/transformers/en/model_doc/mistral](https://huggingface.co/docs/transformers/en/model_doc/mistral) in the Hugging Face documentation. 
+ **Mixtral** — A decoder-only transformer model with sparse Mixture of Experts (MoE) models. For more information, see [Mixtral](https://huggingface.co/docs/transformers/en/model_doc/mixtral) in the Hugging Face documentation. 
+  **Flan ** — An enhanced version of the T5 architecture, an encoder-decoder based transformer model. For more information, see [https://huggingface.co/docs/transformers/model_doc/flan-t5](https://huggingface.co/docs/transformers/model_doc/flan-t5) in the Hugging Face documentation. 
+ **Llama 2, Llama3, Llama3.1, Llama3.2, Llama 3.3, and Mllama** — An improved version of Llama with Grouped Query Attention (GQA). For more information, see [https://huggingface.co/blog/llama2](https://huggingface.co/blog/llama2), [https://huggingface.co/blog/llama3 ](https://huggingface.co/blog/llama3 ), [https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct#model-information](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct#model-information), [https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct), [https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct), and [https://huggingface.co/docs/transformers/main/en/model_doc/mllama](https://huggingface.co/docs/transformers/main/en/model_doc/mllama) in the Hugging Face documentation.
+ **GPTBigCode** — An optimized version of GPT-2 with Multi-Query action. For more information, see [GPTBigCode](https://huggingface.co/docs/transformers/en/model_doc/gpt_bigcode) in the Hugging Face documentation.
+ **Qwen2, Qwen2.5, Qwen2-VL, Qwen2.5-VL, Qwen3** — An LLM family with comprehensive multimodal perception and high speed vision encoding. Any model using the Qwen2, Qwen2-VL, and Qwen2.5-VL architectures can be imported. For Qwen3 architecture, only Qwen3ForCausalLM and Qwen3MoeForCausalLM are supported. Converse is also not supported for Qwen3 models. For more information, see [Qwen2](https://huggingface.co/collections/Qwen/qwen2-6659360b33528ced941e557f), [Qwen2.5](https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e), [Qwen2-VL](https://huggingface.co/collections/Qwen/qwen2-vl-66cee7455501d7126940800d), [Qwen2.5-VL](https://huggingface.co/collections/Qwen/qwen25-vl-6795ffac22b334a837c0f9a5), and [Qwen3](https://huggingface.co/docs/transformers/en/model_doc/qwen3) in the Hugging Face documentation.
+ **GPT-OSS** — OpenAI based GPT-OSS architecture. Amazon Bedrock supports both 20B and 120B based custom models. GPT-OSS model architecture is only supported in the US East (N. Virginia) region.

**Note**  
The size of the imported model weights must be less than 100GB for multimodal models and 200GB for text models.
The maximum positional embeddings or the maximum context length supported by the model should be less than 128K.
Amazon Bedrock supports transformer version 4.51.3. Ensure that you are using transformer version 4.51.3 when you fine tune your model.
Custom Model Import does not support embedding models.

## Import a model source from Amazon S3
<a name="model-customization-import-model-source"></a>

You import a model into Amazon Bedrock by creating a model import job in the Amazon Bedrock console or API. In the job you specify the Amazon S3 URI for the source of the model files. During model training, the import job automatically detects your model's architecture.

You need to supply the model files in the Hugging Face weights format. You can create the files by using the Hugging Face transformer library. To create model files for a Llama model, see [convert\_llama\_weights\_to\_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py). To create the files for a Mistral AI model, see [convert\_mistral\_weights\_to\_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/mistral/convert_mistral_weights_to_hf.py).

To import the model from Amazon S3, you minimally need the following files that the Hugging Face transformer library creates.
+ **.safetensor** — the model weights in *Safetensor* format. Safetensors is a format created by Hugging Face that stores a model weights as tensors. You must store the tensors for your model in a file with the extension `.safetensors`. For more information, see [Safetensors](https://huggingface.co/docs/safetensors/en/index). For information about converting model weights to Safetensor format, see [Convert weights to safetensors](https://huggingface.co/docs/safetensors/en/convert-weights).
+ **config.json** — For examples, see [LlamaConfig](https://huggingface.co/docs/transformers/model_doc/llama2#transformers.LlamaConfig) and [MistralConfig](https://huggingface.co/docs/transformers/model_doc/mistral#transformers.MistralConfig).
**Note**  
Amazon Bedrock overrides llama3 `rope_scaling` value with the following values:  
`original_max_position_embeddings=8192`
`high_freq_factor=4`
`low_freq_factor=1`
`factor=8`
+ **tokenizer\_config.json** For an example, see [LlamaTokenizer](https://huggingface.co/docs/transformers/model_doc/llama2#transformers.LlamaTokenizer).
+ **tokenizer.json **
+ **tokenizer.model** 

### Supported tokenizers
<a name="tokenizers"></a>

Amazon Bedrock Custom Model Import supports the following tokenizers. You can use these tokenizers with any model.
+ T5Tokenizer
+ T5TokenizerFast
+ LlamaTokenizer
+ LlamaTokenizerFast
+ CodeLlamaTokenizer
+ CodeLlamaTokenizerFast
+ GPT2Tokenizer
+ GPT2TokenizerFast
+ GPTNeoXTokenizer
+ GPTNeoXTokenizerFast
+ PreTrainedTokenizer
+ PreTrainedTokenizerFast
+ Qwen2Tokenizer
+ Qwen2TokenizerFast