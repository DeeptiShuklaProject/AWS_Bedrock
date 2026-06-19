

# Review metrics for RAG evaluations that use LLMs (console)
<a name="knowledge-base-eval-llm-results"></a>

You can review the metrics presented in a report for a RAG evaluation job using the Amazon Bedrock console.

RAG evaluations that use Large Language Models (LLMs) compute evaluation metrics to assess the performance of how well the Amazon Bedrock knowledge base or external RAG source is retrieving information and generating responses.

In your RAG evaluation report card, you will see the metrics and the breakdown graphs of the metrics relevant to your evaluation type of either retrieval only or retrieval with response generation. Different metrics are relevant to different evaluation types. The computed scores for each metric are an average score for retrieved texts or generated responses across all the user queries in your prompts dataset. The computed score for each metric is a value between 0 and 1. The closer to 1, the more that metric’s characteristic appears in the retrieved texts or responses. The breakdown graphs for each metric plots a histogram and counts how many retrieved texts or responses for the queries fall within each score range.

For example, you created an evaluation job to evaluate retrieval with response generation. The console report card shows a computed score for *Completeness* in responses to be at 0.82. The *Completeness* score measures how generated responses address all aspects of users’ questions. It is computed as an average score for responses to questions across all prompts in your dataset. The histogram graph for *Completeness* shows that most of the responses (highest bar) fall between a completeness score range of 0.7 to 0.8. However, the knowledge base also scored high for Stereotyping, where generalized statements are made in the responses at 0.94 on average. The knowledge base can generate fairly complete responses most of the time, but those responses include a high amount of generalized statements about individuals or groups of people.

## Report card for RAG evaluations that use LLMs
<a name="kb-eval-llm-report"></a>

Follow the steps to open the report card in the Amazon Bedrock console for RAG evaluation jobs that use LLMs. Refer to the information below for each metric that is relevant to the evaluation types of retrieval only and retrieval with response generation.
+ Sign in to the AWS Management Console and open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock/](https://console.aws.amazon.com/bedrock/).
+ Choose **Evaluations** from the navigation pane, then choose **Knowledge base evaluation**.
+ Select the name of your knowledge base evaluation job. You will be directed to the report card, which is the main page of the knowledge base evaluation.
**Note**  
To open the report card, the status of your RAG evaluation must be either ready or available.

## Metrics relevant to retrieval only type evaluations
<a name="kb-eval-metrics-retrieve"></a>

There are certain metrics relevant to evaluating your knowledge base’s ability to retrieve highly relevant information.

**Contents**
+ [Context relevance](#kb-eval-metric-context-relevance)
+ [Context coverage (requires ground truth)](#kb-eval-metric-context-coverage)

### Context relevance
<a name="kb-eval-metric-context-relevance"></a>

This metric is relevant to the quality of the retrieved information. The score is an average score for retrieved text chunks across all prompts in your dataset. Context relevance means the retrieved text chunks are contextually relevant to the questions. The higher the score, the more contextually relevant the information is on average. The lower the score, the less contextually relevant the information is on average.

### Context coverage (requires ground truth)
<a name="kb-eval-metric-context-coverage"></a>

This metric is relevant to the quality of the retrieved information. The score is an average score for retrieved text chunks across all prompts in your dataset. Context coverage means the retrieved text chunks cover all the information provided in the ground truth texts. The higher the score, the more context coverage on average. The lower the score, the less context coverage on average.

## Metrics relevant to retrieval with response generation type evaluations
<a name="kb-eval-metrics-retrieve-generate"></a>

There are certain metrics relevant to evaluating your knowledge base’s ability to generate useful, appropriate responses based on retrieved information.

**Contents**
+ [Correctness](#kb-eval-metric-correctness)
+ [Completeness](#kb-eval-metric-completeness)
+ [Helpfulness](#kb-eval-metric-helpfulness)
+ [Logical coherence](#kb-eval-metric-coherence)
+ [Faithfulness](#kb-eval-metric-faithfulness)
+ [Citation precision](#kb-eval-metric-cit-precision)
+ [Citation coverage](#kb-eval-metric-cit-coverage)
+ [Harmfulness](#kb-eval-metric-harmfulness)
+ [Stereotyping](#kb-eval-metric-stereotyping)
+ [Refusal](#kb-eval-metric-refusal)

### Correctness
<a name="kb-eval-metric-correctness"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Correctness means accurately answering the questions. The higher the score, the more correct the generated responses are on average. The lower the score, the less correct the generated responses are on average.

### Completeness
<a name="kb-eval-metric-completeness"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Completeness means answering and resolving all aspects of the questions. The higher the score, the more complete the generated responses are on average. The lower the score, the less complete the generated responses are on average.

### Helpfulness
<a name="kb-eval-metric-helpfulness"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Helpfulness means holistically useful responses to the questions. The higher the score, the more helpful the generated responses are on average. The lower the score, the less helpful the generated responses are on average.

### Logical coherence
<a name="kb-eval-metric-coherence"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Logical coherence means responses are free from logical gaps, inconsistencies or contradictions. The higher the score, the more coherent the generated responses are on average. The lower the score, the less coherent the generated responses are on average.

### Faithfulness
<a name="kb-eval-metric-faithfulness"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Faithfulness means avoiding hallucination with resect to the retrieved text chunks. The higher the score, the more faithful the generated responses are on average. The lower the score, the less faithful the generated responses are on average.

### Citation precision
<a name="kb-eval-metric-cit-precision"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Citation precision is a measure of the number of cited passages that are cited correctly. The higher the score, the more citations in the responses are correct on average. The lower the score, the fewer citations are correct on average.

If you choose to use citation precision then you should also use citation coverage, and the other way around. Citation coverage is approximately citation recall. Using both together gives the complete view of the citation quality.

### Citation coverage
<a name="kb-eval-metric-cit-coverage"></a>

This metric is relevant to the quality of the generated responses. The score is an average score for responses across all prompts in your dataset. Citation coverage is approximately citation recall, and is a measure of how well the response is supported by cited passages. The higher the score, the better the responses are supported by citations on average. The lower the score, the less well the responses are supported by citations on average.

If you choose to use citation coverage then you should also use citation precision, and the other way around. Using both together gives the complete view of the citation quality.

### Harmfulness
<a name="kb-eval-metric-harmfulness"></a>

This metric is relevant to the appropriateness of the generated responses. The score is an average score for responses across all prompts in your dataset. Harmfulness means making hateful, insulting, or violent statements. The higher the score, the more harmful the generated responses on average. The lower the score, the less harmful the generated responses on average.

### Stereotyping
<a name="kb-eval-metric-stereotyping"></a>

This metric is relevant to the appropriateness of the generated responses. The score is an average score for responses across all prompts in your dataset. Stereotyping means making generalized statements about individuals or groups of people. The higher the score, the more stereotyping in the generated responses on average. The lower the score, the less stereotyping in the generated responses on average. Note that a strong presence of both flattering and derogatory stereotypes will result in a high score.

### Refusal
<a name="kb-eval-metric-refusal"></a>

This metric is relevant to the appropriateness of the generated responses. The score is an average score for responses across all prompts in your dataset. Refusal means evasive responses to the questions. The higher the score, the more evasive the generated responses are on average. The lower the score, the less evasive the generated responses are on average.