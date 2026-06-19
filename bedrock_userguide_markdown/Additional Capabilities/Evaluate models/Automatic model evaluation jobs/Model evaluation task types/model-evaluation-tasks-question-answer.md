

# Question and answer for model evaluation in Amazon Bedrock
<a name="model-evaluation-tasks-question-answer"></a>

Question and answer is used for tasks including generating automatic help-desk responses, information retrieval, and e-learning. If the text used to train the foundation model contains issues including incomplete or inaccurate data, sarcasm or irony, the quality of responses can deteriorate.

**Important**  
For question and answer, there is a known system issue that prevents Cohere models from completing the toxicity evaluation successfully.

The following built-in datasets are recommended for use with the question and answer answer task type.

**BoolQ**  
BoolQ is a dataset consisting of yes/no question and answer pairs. The prompt contains a short passage, and then a question about the passage. This dataset is recommended for use with question and answer task type.

**Natural Questions**  
Natural questions is a dataset consisting of real user questions submitted to Google search.

**TriviaQA**  
TriviaQA is a dataset that contains over 650K question-answer-evidence-triples. This dataset is used in question and answer tasks.

The following table summarizes the metrics calculated, and recommended built-in dataset. To successfully specify the available built-in datasets using the AWS CLI, or a supported AWSSDK use the parameter names in the column, *Built-in datasets (API)*.


**Available built-in datasets for the question and answer task type in Amazon Bedrock**  


- **Question and answer**
  - **Metric:** Accuracy / **Built-in datasets (console):** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Built-in datasets (API):** Builtin.BoolQ / **Computed metric:** NLP-F1
  - **Built-in datasets (console):** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions) / **Built-in datasets (API):** Builtin.NaturalQuestions
  - **Built-in datasets (console):** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/) / **Built-in datasets (API):** Builtin.TriviaQa
  - **Metric:** Robustness / **Built-in datasets (console):** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Built-in datasets (API):** Builtin.BoolQ / **Computed metric:** F1 and deltaF1
  - **Built-in datasets (console):** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions) / **Built-in datasets (API):** Builtin.NaturalQuestions
  - **Built-in datasets (console):** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/) / **Built-in datasets (API):** Builtin.TriviaQa
  - **Metric:** Toxicity / **Built-in datasets (console):** [BoolQ](https://github.com/google-research-datasets/boolean-questions) / **Built-in datasets (API):** Builtin.BoolQ / **Computed metric:** Toxicity
  - **Built-in datasets (console):** [NaturalQuestions](https://github.com/google-research-datasets/natural-questions) / **Built-in datasets (API):** Builtin.NaturalQuestions
  - **Built-in datasets (console):** [TriviaQA](https://nlp.cs.washington.edu/triviaqa/) / **Built-in datasets (API):** Builtin.TriviaQa



To learn more about how the computed metric for each built-in dataset is calculated, see [Review model evaluation job reports and metrics in Amazon Bedrock](model-evaluation-report.md)