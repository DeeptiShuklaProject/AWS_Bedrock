

# Use agentic retrieval to query a knowledge base
<a name="kb-test-agentic-retrieve"></a>

Agentic retrieval uses a foundation model to intelligently decompose complex queries into sub-queries, iteratively retrieve relevant information from your knowledge bases, and evaluate whether the retrieved results are sufficient to answer the original query. This approach improves retrieval accuracy for complex, multi-step questions that a single retrieval pass might not fully address.

For example, given the query *"Which magazine was started first, Arthur's Magazine or First for Women?"*, agentic retrieval breaks this into separate sub-queries such as *"When was Arthur's Magazine founded?"* and *"When was First for Women founded?"*, retrieves results for each, and evaluates whether the combined results are sufficient.

## How agentic retrieval works
<a name="kb-agentic-retrieve-how-it-works"></a>

When you send a request to the `AgenticRetrieveStream` API, the following process occurs:

1. **Planning** – The foundation model analyzes your query and creates a plan to decompose it into one or more sub-queries. Each sub-query targets a specific retriever that you configured. After retrieval results are collected, the foundation model evaluates whether they are sufficient to answer the original query. If not, it plans and executes additional retrieval iterations, up to the configured maximum.

1. **Retrieval** – The sub-queries are executed against the configured knowledge base retrievers. Results are collected from each retrieval.

1. **Full document expansion** – When the foundation model determines that the full content of a document is needed (e.g., for summarization, to verify completeness, or to access specific sections), it calls the GetDocumentContent API to retrieve the complete document content.

1. **Response generation** – When `generateResponse` is set to `true` (the default), the foundation model synthesizes a natural-language answer from the retrieved results. The answer is streamed back to you via `responseEvent` events.

1. **Result event** – The deduplicated retrieval results from all iterations, the full synthesized natural-language answer and citations are returned to you. Trace events are streamed throughout the process for observability.

## Prerequisites
<a name="kb-agentic-retrieve-prereqs"></a>

Before you can use agentic retrieval, you must have the following:
+ A fully managed Amazon Bedrock knowledge base. Agentic retrieval currently supports only managed knowledge bases.
+ Access to a foundation model in Amazon Bedrock to use for query planning and evaluation.
+ The required IAM permissions. For more information, see [Required permissions for agentic retrieval](#kb-agentic-retrieve-permissions).

## Query a knowledge base with agentic retrieval
<a name="kb-agentic-retrieve-api"></a>

To use agentic retrieval, send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html) request. The response is a stream that includes retrieval results and trace events.

The following table describes the key request fields:


**Required fields**  

| Field | Description | 
| --- | --- | 
| messages | The input query and conversation history. Each message contains a content field with a text value and a role field (user or assistant). | 
| retrievers | The knowledge base retrievers to fetch data from. You can specify up to 5 retrievers, each pointing to a managed knowledge base by its ID. Each retriever can optionally include metadata filters and a maximum number of results. | 
| agenticRetrieveConfiguration | The agentic retrieval configuration, including the foundation model to use for query planning and evaluation, and optionally a reranking model and maximum agent iteration count. | 


**Optional fields**  

| Field | Description | 
| --- | --- | 
| policyConfiguration | Configures a Amazon Bedrock guardrail to apply during agentic retrieval. Specify a guardrailId and guardrailVersion. | 
| userContext | Provides a user context for access control filtering. | 
| generateResponse | A boolean field that, when set to true (the default), instructs the foundation model to generate a natural-language answer from the retrieved results. The answer is streamed back as text chunks and included in the result event. | 

For the full request and response syntax, see [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_AgenticRetrieveStream.html) in the API reference.

## Agentic retrieval response
<a name="kb-agentic-retrieve-response"></a>

The `AgenticRetrieveStream` response is a stream that contains the following event types:
+ **Result event** (`AgenticRetrieveResultEvent`) – The final event delivered when processing completes. Contains the retrieval results and, when response generation is enabled, the generated response. The result event includes:
  + **Retrieval results** (`results`) – The source chunks retrieved across all iterations. Each result includes content, source retriever identifier, and optional metadata. When the same chunk is retrieved by multiple sub-queries, it appears only once in the final results.
  + **Generated response** (`generatedResponse`) – When `generateResponse` is set to `true` (the default), the result event includes a `generatedResponse` object containing:
    + `answer` – The full synthesized natural-language answer text.
    + `citations` – An optional list that maps spans of the answer to supporting retrieval results. Each citation contains:
      + `startIndex` – The character offset where the cited passage begins within the `answer` string.
      + `endIndex` – The character offset where the cited passage ends (exclusive — the cited text runs from `startIndex` up to but not including `endIndex`).
      + `references` – A list where each reference has a `resultIndex` field that indexes into the `results` array on the same result event, indicating which retrieval result supports the cited span.
+ **Response events** (`AgenticRetrieveResponseEvent`) – When `generateResponse` is set to `true` (the default), `responseEvent` events are streamed during response generation. Each event contains a `text` field with an incremental portion of the synthesized natural-language answer.
+ **Trace events** (`AgenticRetrieveTraceEvent`) – Events streamed during the agentic retrieval process that provide visibility into each step. These are the types of trace events:
  + **Planning** – Indicates the foundation model is analyzing the query and creating sub-queries. Includes the planned actions and target retrievers.
  + **Retrieval** – Indicates a retrieval is being executed against a knowledge base. Includes the retrieval input, output, and any warnings or failures.
  + **Speculative retrieval** – An initial retrieval that runs before the first planning step to reduce latency. For a single knowledge base, this retrieves results using the raw user query. For multiple knowledge bases, this performs a probe search to help route queries to the appropriate retrievers.
  + **Full document expansion** – Indicates the agent is retrieving the full content of a specific document. Includes the document ID, source retriever, and status (InProgress, Success, or Failure).

## Required permissions for agentic retrieval
<a name="kb-agentic-retrieve-permissions"></a>

To use the `AgenticRetrieveStream` API, the calling IAM identity must have the following permissions:

```
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:AgenticRetrieveStream",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock:GetDocumentContent"
            ],
            "Resource": "arn:aws:bedrock:{{region}}:{{account-id}}:knowledge-base/*"
        },
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModelWithResponseStream",
            "Resource": "*"
        }
    ]
}
```

If you use guardrails with agentic retrieval, add the following permissions:

```
{
    "Effect": "Allow",
    "Action": [
        "bedrock:GetGuardrail",
        "bedrock:ApplyGuardrail"
    ],
    "Resource": "*"
}
```

## Considerations
<a name="kb-agentic-retrieve-considerations"></a>

Keep the following in mind when using agentic retrieval:
+ Agentic retrieval only supports managed Amazon Bedrock knowledge bases.
+ For quotas on retrievers per request, results per retrieval call, and maximum agent iterations, see [Service quotas for managed knowledge bases](kb-managed-quotas.md).
+ Reducing the maximum iteration count may cause the agent to stop earlier, potentially reducing accuracy for complex queries. 
+ When configuring guardrails, only the `BLOCK` action is supported. The `MASK` action is not supported with agentic retrieval.
+ The customer provides and owns the foundation model, embedding model, and reranking model used during agentic retrieval if provided. Your IAM credentials are used to invoke these models.