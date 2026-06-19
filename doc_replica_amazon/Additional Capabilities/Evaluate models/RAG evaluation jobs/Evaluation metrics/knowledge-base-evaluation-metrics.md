

# Use metrics to understand RAG system performance
<a name="knowledge-base-evaluation-metrics"></a>

When you run a RAG evaluation job, the evaluator model you select uses a set of metrics to characterize the performance of the RAG systems being evaluated. Amazon Bedrock provides a number of built-in metrics you can choose from, or you can define your own metrics.

Amazon Bedrock RAG evaluations offers two types of evaluation job, retrieve only and retrieve and generate. Each type of job has its own set of built-in metrics you can select from.

The following tables list the available built-in metrics for each evaluation type. To learn more about using custom metrics for RAG evaluation jobs, see [Create a prompt for a custom metric](kb-evaluation-custom-metrics-prompt-formats.md).


**Built-in metrics for retrieve-only RAG evaluation jobs**  

| Metric | Description | 
| --- | --- | 
| Context relevance (Builtin.ContextRelevance) | Measures how contextually relevant the retrieved texts are to the questions. | 
| Context coverage (Builtin.ContextCoverage) | Measures how much the retrieved texts cover all the information in the ground truth texts. You must supply a ground truth in your prompt dataset to use this metric. | 


**Built-in metrics for retrieve-and-generate RAG evaluation jobs**  

| Metric | Description | 
| --- | --- | 
| Correctness (Builtin.Correctness) | Measures how accurate the responses are in answering questions. | 
| Completeness (Builtin.Completeness) | Measures how well the responses answer and resolve all aspects of the questions. | 
| Helpfulness (Builtin.Helpfulness) | Measures holistically how useful responses are in answering questions. | 
| Logical coherence (Builtin.LogicalCoherence) | Measures whether the responses are free from logical gaps, inconsistencies or contradictions. | 
| Faithfulness (Builtin.Faithfulness) | Measures how well responses avoid hallucination with respect to the retrieved texts. | 
| Citation precision (Builtin.CitationPrecision) | Measures how many of the cited passages were correctly cited. | 
| Citation coverage (Builtin.CitationCoverage) | Measures how well the response is supported by the cited passages and if there are any missing citations. | 
| Harmfulness (Builtin.Harmfulness) | Measures harmful content in the responses, including hate, insults, violence, or sexual content. | 
| Stereotyping (Builtin.Stereotyping) | Measures generalized statements about individuals or groups of people in responses. | 
| Refusal (Builtin.Refusal) | Measures how evasive the responses are in answering questions. | 