

# Model evaluation task types in Amazon Bedrock
<a name="model-evaluation-tasks"></a>

In a model evaluation job, an evaluation task type is a task you want the model to perform based on information in your prompts. You can choose one task type per model evaluation job.

The following table summarizes available tasks types for automatic model evaluations, built-in datasets, and relevant metrics for each task type.


**Available built-in datasets for automatic model evaluation jobs in Amazon Bedrock**  


- **General text generation **
  - **Metric:** Accuracy  / **Built-in datasets:** [TREX](https://hadyelsahar.github.io/t-rex/) / **Computed metric:** Real world knowledge (RWK) score
  - **Metric:** Robustness / **Built-in datasets:** [BOLD](https://github.com/amazon-science/bold) / **Computed metric:** Word error rate
  - **Built-in datasets:** [TREX](https://hadyelsahar.github.io/t-rex/)
  - **Built-in datasets:** [WikiText2](https://huggingface.co/datasets/Salesforce/wikitext)
  - **Metric:** Toxicity / **Built-in datasets:** [RealToxicityPrompts](https://github.com/allenai/real-toxicity-prompts) / **Computed metric:** Toxicity 
  - **Built-in datasets:** [BOLD](https://github.com/amazon-science/bold)

- **Text summarization**
  - **Metric:** Accuracy  / **Built-in datasets:** Gigaword / **Computed metric:** BERTScore
  - **Metric:** Toxicity / **Built-in datasets:** Gigaword / **Computed metric:** Toxicity 
  - **Metric:**  Robustness  / **Built-in datasets:** Gigaword / **Computed metric:** BERTScore and deltaBERTScore

- **Question and answer**
  - **Metric:** Accuracy / **Built-in datasets:** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Computed metric:** NLP-F1
  - **Built-in datasets:** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions)
  - **Built-in datasets:** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/)
  - **Metric:** Robustness / **Built-in datasets:** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Computed metric:** F1 and deltaF1 
  - **Built-in datasets:** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions)
  - **Built-in datasets:** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/)
  - **Metric:** Toxicity / **Built-in datasets:** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Computed metric:** Toxicity 
  - **Built-in datasets:** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions)
  - **Built-in datasets:** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/)

- **Text classification**
  - **Metric:** Accuracy  / **Built-in datasets:** [Women's Ecommerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews) / **Computed metric:** Accuracy (Binary accuracy from classification\_accuracy\_score)
  - **Metric:** Robustness  / **Built-in datasets:** [Women's Ecommerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews) / **Computed metric:** classification\_accuracy\_score and delta\_classification\_accuracy\_score



**Topics**
+ [General text generation for model evaluation in Amazon Bedrock](model-evaluation-tasks-general-text.md)
+ [Text summarization for model evaluation in Amazon Bedrock](model-evaluation-tasks-text-summary.md)
+ [Question and answer for model evaluation in Amazon Bedrock](model-evaluation-tasks-question-answer.md)
+ [Text classification for model evaluation in Amazon Bedrock](model-evaluation-text-classification.md)