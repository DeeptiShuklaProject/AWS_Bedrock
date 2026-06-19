

# Query a knowledge base connected to an Amazon Kendra GenAI index
<a name="kb-test-kendra"></a>

You can query a knowledge base that uses an Amazon Kendra GenAI index, and return only relevant text from data sources. For this query, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt), like with a standard knowledge base.

The structure of a response returned from a knowledge base with an Amazon Kendra GenAI index is the same as a standard [ KnowledgeBaseRetrievalResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalResult.html). However, the response also includes a few additional fields from Amazon Kendra.

The following table describes the fields from Amazon Kendra that you might see in a returned response. Amazon Bedrock gets these fields from the Amazon Kendra response. If that response doesn't contain these fields, then the returned query result from Amazon Bedrock won't have these fields either.


| Field | Description | 
| --- | --- | 
| x-amz-kendra-document-title | The title of the returned document. | 
| x-amz-kendra-score-confidence | A relative ranking of how relevant the response is to the query. Possible values are VERY\_HIGH, HIGH, MEDIUM, LOW, and NOT\_AVAILABLE. | 
| x-amz-kendra-passage-id | The ID of the returned passage. | 
| x-amz-kendra-document-id | The ID of the returned document. | 
| DocumentAttributes | Document attributes or metadata fields from Amazon Kendra. The returned query result from the knowledge base stores these as metadata key-value pairs. You can filter the results with metadata filtering from Amazon Bedrock. For more information, see [DocumentAttribute](https://docs.aws.amazon.com/kendra/latest/APIReference/API_DocumentAttribute.html). | 