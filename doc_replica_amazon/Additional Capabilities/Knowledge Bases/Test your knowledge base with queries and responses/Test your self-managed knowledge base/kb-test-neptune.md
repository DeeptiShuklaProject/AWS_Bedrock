

# Query a knowledge base connected to an Amazon Neptune Analytics graph
<a name="kb-test-neptune"></a>

You can query a knowledge base that uses an Amazon Neptune Analytics graph, and return only relevant text from data sources. For this query, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt), like with a standard knowledge base. For information about querying a knowledge base and retrieving data and generating responses, see:
+  [Query a knowledge base and retrieve data](kb-test-retrieve.md) 
+  [Query a knowledge base and generate responses based off the retrieved data](kb-test-retrieve-generate.md) 

The structure of a response returned from a knowledge base with an Amazon Neptune Analytics graph, is the same as a standard [ KnowledgeBaseRetrievalResult](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalResult.html). However, the response also includes a few additional fields from Amazon Neptune.

The following table describes the fields from Neptune Analytics that you might see in a returned response. Amazon Bedrock gets these fields from the Neptune Analytics response. If that response doesn't contain these fields, then the returned query result from Amazon Bedrock won't have these fields either.


| Field | Description | 
| --- | --- | 
| x-amz-bedrock-kb-source-uri | The Amazon S3 URL of the returned document. | 
| score | A distance measure that indicates how closely a response matches the provided query, where lower values indicate better matches. | 
| x-amz-bedrock-kb-data-source-id | The ID of the data source used for the knowledge base. | 
| x-amz-bedrock-kb-chunk-id | The ID of the chunk that was used to retrieve the information for the query and generate the response. | 
| DocumentAttributes | Document attributes or metadata fields from Amazon Kendra. The returned query result from the knowledge base stores these as metadata key-value pairs. You can filter the results with metadata filtering from Amazon Bedrock. | 

## Using metadata and filtering
<a name="kb-test-neptune-metadata"></a>

When you query the knowledge base and generate responses, you can filter on metadata for finding more relevant documents. For example, you can filter based on the publication date of the document. You can use the Amazon Bedrock console or the runtime API [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html) for this purpose, which can specify some general filter conditions.

The following are some considerations for using the `RetrievalFilter` API for Neptune Analytics graphs.
+ The `listContains` filter is not supported.
+ The list variant of the `stringContains` filter is not supported.
+ For best practices on choosing filter types and designing metadata attributes for efficient filtering, see [Best practices for metadata filtering in GraphRAG](https://docs.aws.amazon.com//neptune-analytics/latest/userguide/best-practices-graphrag-filters.html).

The following shows an example:

```
"vectorSearchConfiguration": {
        "numberOfResults": 5,
        "filter": {
            "orAll": [
                {
                    "andAll": [
                        {
                            "equals": {
                                "key": "genre",
                                "value": "entertainment"
                            }
                        },
                        {
                            "greaterThan": {
                                "key": "year",
                                "value": 2018
                            }
                        }
                    ]
                },
                {
                    "andAll": [                        
                        {
                            "startsWith": {
                                "key": "author",
                                "value": "C"
                            }
                        }
                    ]
                }
            ]
        }
    }
}
```