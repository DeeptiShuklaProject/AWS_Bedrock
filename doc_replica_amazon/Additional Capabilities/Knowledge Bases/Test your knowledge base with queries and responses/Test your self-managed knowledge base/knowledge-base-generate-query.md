

# Generate a query for structured data
<a name="knowledge-base-generate-query"></a>

When you connect a structured data store to your knowledge base, your knowledge base can query it by converting the natural language query provided by the user into an SQL query, based on the structure of the data source being queried. When you use:
+ [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html): The response returns the result of the SQL query execution.
+ [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html): The generated response is based on the result of the SQL query execution.
+ [GenerateQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerateQuery.html): Amazon Bedrock Knowledge Bases decouples the conversion of the query from the retrieval process. You can use this API operation to transform a query into SQL.

## Using the `GenerateQuery` API
<a name="knowledge-base-generate-query-api"></a>

You can use the response from the `GenerateQuery` API operation with a subsequent `Retrieve` or `RetrieveAndGenerate` action, or insert it into other workflows. `GenerateQuery` allows you to efficiently transform queries into SQL queries by taking into consideration the structure of your knowledge base's data source.

To turn a natural language query into a SQL query, submit a [GenerateQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerateQuery.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt). The `GenerateQuery` request contains the following fields:
+ queryGenerationInput – Specify `TEXT` as the `type` and include the query in the `text` field.
**Note**  
Queries must be written in English.
+ transformationConfiguration – Specify `TEXT_TO_SQL` as the `mode`. In the `textToSqlConfiguration` field, specify `KNOWLEDGE_BASE` as the `type`. Then, specify the ARN of the knowledge base.

The response returns an array containing a [GeneratedQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GeneratedQuery.html) object in the `queries` field. The object contains an SQL query for the query in the `sql` field.

## Key considerations
<a name="knowledge-base-generate-query-considerations"></a>

The following are some key considerations when generating a query using structured data.
+ 

**Cross-region inference and structured data retrieval**  
Structured data retrieval uses cross-Region inference to select the optimal AWS Region within your geography to process your inference request. This doesn't incur any additional charges, and improves customer experience by maximizing available resources and model availability.

  Cross-inference requests are kept within the AWS Regions that are part of the geography where the data originally resides. Your data remains stored within the source Region but the input prompts and output results might move outside of this Region. All data will be transmitted encrypted across Amazon’s secure network.

  For more information, see [Increase throughput with cross-Region inference](cross-region-inference.md).
+ 

**Accuracy of generated SQL queries**  
The accuracy of a generated SQL query can vary depending on context, table schemas, and the intent of a user query. Evaluate the generated queries to ensure that they suit your use case before using them in your workload.
+ 

**Number of retrieved results**  
The following limitations apply when generating the response.
  + When using the `InvokeAgent`, `RetrieveAndGenerate`, and `RetrieveAndGenerateStream` API operations, only 10 retrieved results are used when generating the response.
  + When using the `InvokeAgent` API, if there are more than 10 rows of retrieved results, the total number of retrieved rows is not passed to the agent for generating the response. If you use the `RetrieveAndGenerate` API instead, the total number of rows is included in the prompt for generating the final response.
+ 

**`GenerateQuery` API quota**  
The `GenerateQuery` API has a quota of 2 requests per second.

## Grant a role permissions to access generated queries
<a name="knowledge-base-structured-permissions"></a>

For your knowledge base that's conencted to a structured data source, if you want to to perform some additional operations on the generated squeries, then you must grant permissions to perform the `GenerateQuery` API action. To allow your IAM role to query a knowledge base connected to a structured data store, attach the following policy to the role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "GetKB",
            "Effect": "Allow",
            "Action": [
                "bedrock:GetKnowledgeBase"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{KnowledgeBaseId}}"
            ]
        },
        {
            "Sid": "GenerateQueryAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:GenerateQuery",
                "sqlworkbench:GetSqlRecommendations"
            ],
            "Resource": "*"
        },
        {
            "Sid": "Retrieve",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:knowledge-base/{{KnowledgeBaseId}}"
            ]
        },
        {
            "Sid": "RetrieveAndGenerate",
            "Effect": "Allow",
            "Action": [
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

------

You can remove statements that you don't need, depending on your use case:
+ The `GetKB` and `GenerateQuery` statements are required to call [GenerateQuery](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerateQuery.html) to generate SQL queries that take into account user queries and your connected data source.
+ The `Retrieve` statement is required to call [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) to retrieve data from your structured data store.
+ The `RetrieveAndGenerate` statement is required to call [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) to retrieve data from your structured data store and generate responses based off the data.