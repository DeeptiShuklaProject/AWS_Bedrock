

# What is prompt engineering?
<a name="what-is-prompt-engineering"></a>

Prompt engineering refers to the practice of crafting and optimizing input prompts by selecting appropriate words, phrases, sentences, punctuation, and separator characters to effectively use LLMs for a wide variety of applications. In other words, prompt engineering is the art of communicating with an LLM. High-quality prompts condition the LLM to generate desired or better responses. The detailed guidance provided within this document is applicable across all LLMs within Amazon Bedrock.

The best prompt engineering approach for your use case is dependent on both the task and the data. Common tasks supported by LLMs on Amazon Bedrock include:
+  **Classification:** The prompt includes a question with several possible choices for the answer, and the model must respond with the correct choice. An example classification use case is sentiment analysis: the input is a text passage, and the model must classify the sentiment of the text, such as whether it's positive or negative, or harmless or toxic. 
+  **Question-answer, without context:** The model must answer the question with its internal knowledge without any context or document. 
+  **Question-answer, with context:** The user provides an input text with a question, and the model must answer the question based on information provided within the input text. 
+  **Summarization:** The prompt is a passage of text, and the model must respond with a shorter passage that captures the main points of the input. 
+  **Open-ended text generation:** Given a prompt, the model must respond with a passage of original text that matches the description. This also includes the generation of creative text such as stories, poems, or movie scripts. 
+  **Code generation:** The model must generate code based on user specifications. For example, a prompt could request text-to-SQL or Python code generation. 
+  **Mathematics:** The input describes a problem that requires mathematical reasoning at some level, which may be numerical, logical, geometric or otherwise. 
+  **Reasoning or logical thinking:** The model must make a series of logical deductions. 
+  **Entity extraction:** Entity extraction can extracts entities based on a provided input question. You can extract specific entities from text or input based on your prompt. 
+  **Chain-of-thought reasoning:** Give step-by-step reasoning on how an answer is derived based on your prompt. 