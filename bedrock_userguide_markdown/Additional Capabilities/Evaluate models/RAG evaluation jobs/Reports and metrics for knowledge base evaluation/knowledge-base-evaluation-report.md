

# Review RAG evaluation job reports and metrics
<a name="knowledge-base-evaluation-report"></a>

The results of a Retrieval Augmented Generation (RAG) evaluation job are presented in a report, and include key metrics or data that can help you assess the performance or effectiveness of a knowledge base. The results of a knowledge base evaluation job are available via the Amazon Bedrock console or in the Amazon S3 bucket you specified when creating the job.

For RAG evaluation jobs with one or more custom metrics, Amazon Bedrock also stores your metric definitions as JSON files in the output S3 bucket you specify. You can access these files by navigating to `s3://{{S3-output-bucket-name}}/{{job-name}}/{{job-uuid}}/custom_metrics`. To see the format for JSON definitions of custom metrics, see [Creating a JSON file to create a custom metric](model-evaluation-custom-metrics-prompt-formats.md#model-evaluation-custom-metrics-prompt-formats-json).

Use the following topics to learn how to review knowledge base evaluation reports and metrics.

**Topics**
+ [Review metrics for RAG evaluations that use LLMs (console)](knowledge-base-eval-llm-results.md)