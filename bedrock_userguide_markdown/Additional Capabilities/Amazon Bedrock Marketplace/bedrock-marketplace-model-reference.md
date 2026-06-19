

# Model compatibility
<a name="bedrock-marketplace-model-reference"></a>

All models can use the `InvokeModel` operation. Some models can use the `Converse` operation. 

For Amazon Bedrock marketplace models, use the [ ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html) API to use Amazon Bedrock Guardrails.

The following table shows the available models and whether they can use the `Converse` operation:


| Name | Converse API Supported | Streaming Supported | 
| --- | --- | --- | 
| Arcee Lite | Yes | Yes | 
| Arcee Nova | Yes | Yes | 
| Arcee SuperNova | Yes | Yes | 
| Arcee Virtuoso Small | Yes | Yes | 
| Aya 101 | No | Yes | 
| Bart Large CNN samsum | No | No | 
| Bloom 1b1 | No | Yes | 
| Bloom 1b7 | No | Yes | 
| Bloom 3B | No | Yes | 
| Bloom 560m | No | Yes | 
| Bloom 7B1 | No | Yes | 
| Bloomz 1b1 | No | Yes | 
| Bloomz 1b7 | No | Yes | 
| BloomZ 3B FP16 | No | Yes | 
| BloomZ 7B1 FP16 | No | Yes | 
| Bria 2.2HD Commercial | No | No | 
| Bria 2.3 Commercial  | No | No | 
| Bria 2.3 Fast Commercial  | No | No | 
| CyberAgentLM3-22B-Chat (CALM3-22B-Chat) | Yes | Yes | 
| DBRX Base | No | Yes | 
| DBRX Instruct | Yes | Yes | 
| DeepSeek-R1-Distill-Llama-70B | No | Yes | 
| DeepSeek-R1-Distill-Llama-8B | No | Yes | 
| DeepSeek-R1-Distill-Qwen-32B | No | Yes | 
| DeepSeek-R1-Distill-Qwen-14B | No | Yes | 
| DeepSeek-R1-Distill-Qwen-7B | No | Yes | 
| DeepSeek-R1-Distill-Qwen-1.5B | No | Yes | 
| DeepSeek-R1 | No | Yes | 
| Distilbart CNN 12-6 | No | No | 
| Distilbart CNN 6-6 | No | No | 
| Distilbart xsum 12-3 | No | No | 
| DistilGPT 2 | No | Yes | 
| Dolly V2 12b BF16 | No | Yes | 
| Dolly V2 3b BF16 | No | Yes | 
| Dolly V2 7b BF16 | No | Yes | 
| Dolphin 2.2.1 Mistral 7B | Yes | Yes | 
| Dolphin 2.5 Mixtral 8 7B | Yes | Yes | 
| EleutherAI GPT Neo 1.3B | No | Yes | 
| EleutherAI GPT Neo 2.7B | No | Yes | 
| ESM3-open | No | No | 
| EXAONE\_v3.0 7.8B Instruct | Yes | No | 
| Falcon 40B BF16 | No | Yes | 
| Falcon Lite | No | Yes | 
| Falcon Lite 2 | No | Yes | 
| Falcon RW 1B | No | Yes | 
| Falcon3 1B Instruct | Yes | Yes | 
| Falcon3 3B Base  | No | Yes | 
| Falcon3 3B Instruct | Yes | Yes | 
| Falcon3 7B Base | No | Yes | 
| Falcon3 7B Instruct | Yes | Yes | 
| Falcon3 10B Base  | No | Yes | 
| Falcon3 10B Instruct | Yes | Yes | 
| Flan-T5 Base | No | Yes | 
| Flan-T5 Base Model Fine-tuned on the Samsum Dataset | No | Yes | 
| Flan-T5 Large | No | Yes | 
| Flan-T5 Small | No | Yes | 
| Gemma 2 27B | No | Yes | 
| Gemma 2 27B Instruct | Yes | Yes | 
| Gemma 2 2B | No | Yes | 
| Gemma 2 2B Instruct | Yes | Yes | 
| Gemma 2 9B | No | Yes | 
| Gemma 2 9B Instruct | Yes | Yes | 
| Gemma 2B | No | Yes | 
| Gemma 2B Instruct | Yes | Yes | 
| Gemma 7B | No | Yes | 
| Gemma 7B Instruct | Yes | Yes | 
| GPT 2 | No | Yes | 
| GPT NeoX 20B FP16 | No | Yes | 
| GPT-2 XL | No | Yes | 
| GPT-J 6B | No | Yes | 
| GPT-Neo 1.3B | No | Yes | 
| GPT-Neo 125M | No | Yes | 
| GPT-NEO 2.7B | No | Yes | 
| Granite 3.0 2B Instruct | Yes | Yes | 
| Granite 3.0 8B Instruct | Yes | Yes | 
| Gretel Navigator Tabular | Yes | Yes | 
| IBM Granite 20B Code Instruct - 8K | Yes | Yes | 
| IBM Granite 34B Code Instruct - 8K | Yes | Yes | 
| IBM Granite 3B Code Instruct - 128K | Yes | Yes | 
| IBM Granite 8B Code Instruct - 128K | Yes | Yes | 
| KARAKURI LM 8x7b instruct | No | Yes | 
| Liquid | Yes | Yes | 
| Llama 3.1 SuperNova Lite | Yes | Yes | 
| Llama Spark | Yes | Yes | 
| Llama-3-Varco-Offsetbias-8B | No | Yes | 
| Llama3 8B SEA-Lion v2.1 Instruct | Yes | Yes | 
| MARS6 | No | No | 
| Medical LLM - Medium | No | No | 
| Medical LLM - Small | No | No | 
| Medical Text Translation (EN-ES) | No | No | 
| Mistral 7B OpenOrca AWQ | Yes | Yes | 
| Mistral 7B OpenOrca GPTQ | Yes | Yes | 
| Mistral 7B SFT Alpha | Yes | Yes | 
| Mistral 7B SFT Beta | Yes | Yes | 
| Mistral Lite | Yes | Yes | 
| Mistral Nemo Base 2407 | No | Yes | 
| Mistral Nemo Instruct 2407 | Yes | Yes | 
| Mistral Trix V1 | No | Yes | 
| MPT 7B BF16 | No | Yes | 
| MPT 7B Instruct BF16 | No | Yes | 
| MPT 7B StoryWriter-65k\+ BF16 | No | Yes | 
| Multilingual GPT | No | Yes | 
| NVIDIA Nemotron-4 15B NIM Microservice | Yes | No | 
| Open Hermes 2 Mistral 7B | Yes | Yes | 
| Phi-2 | No | Yes | 
| Phi-3-Mini-128K-Instruct | Yes | Yes | 
| Phi-3-Mini-4K-Instruct | Yes | Yes | 
| Phi-3.5-mini-instruct | Yes | Yes | 
| Pixtral 12B 2409 | Yes | Yes | 
| PLaMo API | No | Yes | 
| Snowflake Arctic Instruct Vllm | Yes | Yes | 
| Solar Mini Chat | Yes | Yes | 
| Solar Mini Chat - Quant | Yes | Yes | 
| Solar Mini Chat ja | Yes | Yes | 
| Solar Mini Chat ja - Quant | Yes | Yes | 
| Solar Pro | Yes | Yes | 
| Solar Pro (Quantized) | Yes | Yes | 
| Stable Diffusion 3.5 Large | No | No | 
| Stockmark-LLM-13b | No | No | 
| Text Summarization | No | No | 
| VARCO LLM KO/EN-13B-IST | Yes | No | 
| Whisper Large V3 Turbo | No | Yes | 
| Widn Llama3-Tower Vesuvius | Yes | Yes | 
| Widn Tower Anthill | Yes | Yes | 
| Widn Tower Sugarloaf | Yes | Yes | 
| Writer Palmyra Small | No | Yes | 
| Writer Palmyra-Fin-70B-32K | Yes | Yes | 
| Writer Palmyra-Med-70B-32K | Yes | Yes | 
| YARN Mistral 7B 128k | No | Yes | 
| Yi-1.5-34B | No | Yes | 
| Yi-1.5-34B-Chat | Yes | Yes | 
| Yi-1.5-6B | No | Yes | 
| Yi-1.5-6B-Chat | Yes | Yes | 
| Yi-1.5-9B | No | Yes | 
| Yi-1.5-9B-Chat | Yes | Yes | 
| Zephyr 7B Alpha | No | Yes | 
| Zephyr 7B Beta | No | Yes | 
| Zephyr 7B Gemma | No | Yes | 