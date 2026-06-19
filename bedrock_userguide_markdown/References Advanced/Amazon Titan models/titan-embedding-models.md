

# Amazon Titan Text Embeddings models
<a name="titan-embedding-models"></a>

Amazon Titan Embeddings models include Amazon Titan Text Embeddings V2 and Titan Text Embeddings G1 model.

**Note**  
Embedding models on Amazon Bedrock are throttled by Requests Per Minute (RPM), not Tokens Per Minute (TPM). When planning capacity or requesting quota increases for embedding models, use the RPM quota. For more information, see [Quotas for Amazon Bedrock](quotas.md).

Text embeddings represent meaningful vector representations of unstructured text such as documents, paragraphs, and sentences. You input a body of text and the output is a (1 x n) vector. You can use embedding vectors for a wide variety of applications.

The Amazon Titan Text Embedding v2 model (`amazon.titan-embed-text-v2:0`) can intake up to 8,192 tokens or 50,000 characters and outputs a vector of 1,024 dimensions. The model is optimized for text retrieval tasks, but can also be used for additional tasks, such as semantic similarity and clustering.

Amazon Titan Embeddings models generate meaningful semantic representation of documents, paragraphs and sentences. Amazon Titan Text Embeddings takes as input a body of text and generates a (1 x n) vector. Amazon Titan Text Embeddings is offered via latency-optimized endpoint invocation for generating vectors at low latency (recommended during the retrieval step) as well as throughput optimized batch jobs for faster indexing. The actual similarity computation and retrieval are performed by your vector database, not by the embedding model. Amazon Titan Text Embeddings v2 supports long documents, however for retrieval tasks, it is recommended to segment documents into logical segments, such as paragraphs or sections.

**Note**  
Amazon Titan Text Embeddings v2 model and Titan Text Embeddings v1 model do not support inference parameters such as `maxTokenCount` or `topP`.

**Amazon Titan Text Embeddings V2 model**
+ **Model ID** – `amazon.titan-embed-text-v2:0`
+ **Max input text tokens** – 8,192
+ **Max input text characters** – 50,000
+ **Languages** – English (100\+ languages in preview)
+ **Output vector size** – 1,024 (default), 512, 256
+ **Inference types** – On-Demand, Provisioned Throughput
+ **Supported use cases** – RAG, document search, reranking, classification, etc.

**Note**  
Titan Text Embeddings V2 takes as input a non-empty string with up to 8,192 tokens or 50,000 characters. The characters to token ratio in English is 4.7 characters per token, on average. While Titan Text Embeddings V1 and Titan Text Embeddings V2 are able to accommodate up to 8,192 tokens, it is recommended to segment documents into logical segments (such as paragraphs or sections).

The Amazon Titan Embedding Text v2 model is optimized for English, with multilingual support for the following languages. Cross-language queries (such as providing a knowledge base in Korean and querying it in German) will return sub-optimal results.
+ Afrikaans
+ Albanian
+ Amharic
+ Arabic
+ Armenian
+ Assamese
+ Azerbaijani
+ Bashkir
+ Basque
+ Belarusian
+ Bengali
+ Bosnian
+ Breton
+ Bulgarian
+ Burmese
+ Catalan
+ Cebuano
+ Chinese
+ Corsican
+ Croatian
+ Czech
+ Danish
+ Dhivehi
+ Dutch
+ English
+ Esperanto
+ Estonian
+ Faroese
+ Finnish
+ French
+ Galician
+ Georgian
+ German
+ Gujarati
+ Haitian
+ Hausa
+ Hebrew
+ Hindi
+ Hungarian
+ Icelandic
+ Indonesian
+ Irish
+ Italian
+ Japanese
+ Javanese
+ Kannada
+ Kazakh
+ Khmer
+ Kinyarwanda
+ Kirghiz
+ Korean
+ Kurdish
+ Lao
+ Latin
+ Latvian
+ Lithuanian
+ Luxembourgish
+ Macedonian
+ Malagasy
+ Malay
+ Malayalam
+ Maltese
+ Maori
+ Marathi
+ Modern Greek
+ Mongolian
+ Nepali
+ Norwegian
+ Norwegian Nynorsk
+ Occitan
+ Oriya
+ Panjabi
+ Persian
+ Polish
+ Portuguese
+ Pushto
+ Romanian
+ Romansh
+ Russian
+ Sanskrit
+ Scottish Gaelic
+ Serbian
+ Sindhi
+ Sinhala
+ Slovak
+ Slovenian
+ Somali
+ Spanish
+ Sundanese
+ Swahili
+ Swedish
+ Tagalog
+ Tajik
+ Tamil
+ Tatar
+ Telugu
+ Thai
+ Tibetan
+ Turkish
+ Turkmen
+ Uighur
+ Ukrainian
+ Urdu
+ Uzbek
+ Vietnamese
+ Waray
+ Welsh
+ Western Frisian
+ Xhosa
+ Yiddish
+ Yoruba
+ Zulu