

# Configure and customize queries for managed knowledge bases
<a name="kb-managed-test-config"></a>

You can configure and customize retrieval, further improving the relevancy of results. For example, you can apply filters to document metadata fields/attributes to use the most recently updated documents or documents with recent modification times.

**Note**  
All of the following configurations are only applicable to unstructured data sources.

To learn more about these configurations in the console or the API, select from the following topics:

## Number of source chunks
<a name="kb-managed-test-config-number"></a>

When you query a knowledge base, Amazon Bedrock returns up to five results in the response by default. Each result corresponds to a source chunk.

**Note**  
The actual number of results in the response might be less than the specified `numberOfResults` value, since this parameter sets the maximum number of results to return. If you have configured hierarchical chunking for your chunking strategy, the `numberOfResults` parameter maps to the number of child chunks that the knowledge base will retrieve. Since child chunks that share the same parent chunk are replaced with the parent chunk in the final response, the number of results returned might be less than the requested amount.

To modify the maximum number of results to return, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

Follow the console steps at [Query a knowledge base and retrieve data](kb-test-retrieve.md). In the **Configurations** pane, expand the **Source chunks** section and enter the maximum number of source chunks to return.

------
#### [ API ]

When you make a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request, include a `retrievalConfiguration` field, mapped to a [KnowledgeBaseRetrievalConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalConfiguration.html) object. To see the location of this field, refer to the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) and [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request bodies in the API reference.

The following JSON object shows the minimal fields required in the [KnowledgeBaseRetrievalConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalConfiguration.html) object to set the maximum number of results to return:

```
"retrievalConfiguration": {
    "vectorSearchConfiguration": {
        "numberOfResults": number
    }
}
```

Specify the maximum number of retrieved results (see the `numberOfResults` field in [KnowledgeBaseRetrievalConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalConfiguration.html) for the range of accepted values) to return in the `numberOfResults` field.

------

## Manual metadata filtering
<a name="kb-managed-test-config-filters"></a>

You can apply filters to document fields/attributes to help you further improve the relevancy of responses. Your data sources can include document metadata attributes/fields to filter on and can specify which fields to include in the embeddings.

**Managed knowledge base considerations**  
When using metadata filtering with a managed knowledge base:  
The `startsWith` and `stringContains` metadata filters are not supported. Use `equals`, `greaterThan`, `lessThan`, `in`, or `notIn` operators instead.
For custom knowledge bases, metadata fields prefixed with `x-amz-bedrock` are reserved by the service. For fully managed knowledge bases, reserved metadata fields use an underscore prefix (for example, `_source_uri`, `_data_source_id`). You cannot override reserved metadata fields in either knowledge base type.

For example, "epoch\_modification\_time" represents the time in number of seconds since January 1, 1970 (UTC) when the document was last updated. You can filter on the most recent data, where "epoch\_modification\_time" is *greater than* a certain number. These most recent documents can be used for the query.

To use filters when querying a knowledge base, check that your knowledge base fulfills the following requirements:
+ When configuring your data source connector, most connectors crawl the main metadata fields of your documents. If you're using an Amazon S3 bucket as your data source, the bucket must include at least one `fileName.extension.metadata.json` for the file or document it's associated with. See **Document metadata fields** in [Connection configuration](s3-data-source-connector.md#configuration-s3-connector) for more information about configuring the metadata file.
+ If your knowledge base's vector index is in an Amazon OpenSearch Serverless vector store, check that the vector index is configured with the `faiss` engine. If the vector index is configured with the `nmslib` engine, you'll have to do one of the following:
  + [Create a new knowledge base](knowledge-base-create.md) in the console and let Amazon Bedrock automatically create a vector index in Amazon OpenSearch Serverless for you.
  + [Create another vector index](knowledge-base-setup.md) in the vector store and select `faiss` as the **Engine**. Then [Create a new knowledge base](knowledge-base-create.md) and specify the new vector index.
+ If your knowledge base uses a vector index in an S3 vector bucket, you cannot use the `startsWith` and `stringContains` filters.
+ If you're adding metadata to an existing vector index in an Amazon Aurora database cluster, we recommend that you provide the field name of the custom metadata column to store all your metadata in a single column. During [data ingestion](kb-data-source-sync-ingest.md), this column will be used to populate all the information in your metadata files from your data sources. If you choose to provide this field, you must create an index on this column.
  + When you [create a new knowledge base](knowledge-base-create.md) in the console and let Amazon Bedrock configure your Amazon Aurora database, it will automatically create a single column for you and populate it with the information from your metadata files.
  + When you choose to [create another vector index](knowledge-base-setup.md) in the vector store, you must provide the custom metadata field name to store information from your metadata files. If you don't provide this field name, you must create a column for each metadata attribute in your files and specify the data type (text, number, or boolean). For example, if the attribute `genre` exists in your data source, you would add a column named `genre` and specify `text` as the data type. During ingestion, these separate columns will be populated with the corresponding attribute values.

If you have PDF documents in your data source and use Amazon OpenSearch Serverless or Amazon Aurora for your vector store: Amazon Bedrock knowledge bases will generate document page numbers and store them in a metadata field/attribute called *x-amz-bedrock-kb-document-page-number*. Note that page numbers stored in a metadata field is not supported if you choose no chunking for your documents.

You can use the following filtering operators to filter results when you query:


**Filtering operators**  

| Operator | Console | API filter name | Supported attribute data types | Filtered results | 
| --- | --- | --- | --- | --- | 
| Equals | = | [equals](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-equals) | string, number, boolean | Attribute matches the value you provide | 
| Not equals | \!= | [notEquals](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-notEquals) | string, number, boolean | Attribute doesn’t match the value you provide | 
| Greater than | > | [greaterThan](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-greaterThan) | number | Attribute is greater than the value you provide | 
| Greater than or equals | >= | [greaterThanOrEquals](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-greaterThanOrEquals) | number | Attribute is greater than or equal to the value you provide | 
| Less than | < | [lessThan](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-lessThan) | number | Attribute is less than the value you provide | 
| Less than or equals | <= | [lessThanOrEquals](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-lessThanOrEquals) | number | Attribute is less than or equal to the value you provide | 
| In | : | [in](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-in) | string list | Attribute is in the list you provide (currently best supported with Amazon OpenSearch Serverless and Neptune Analytics GraphRAG vector stores) | 
| Not in | \!: | [notIn](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-notIn) | string list | Attribute isn’t in the list you provide (currently best supported with Amazon OpenSearch Serverless and Neptune Analytics GraphRAG vector stores) | 
| String contains | Not available | [stringContains](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-stringContains) | string | Attribute must be a string. Attribute name matches the key and whose value is a string that contains the value that you provided as a substring, or a list with a member that contains the value that you provided as a substring (currently best supported with Amazon OpenSearch Serverless vector store. The Neptune Analytics GraphRAG vector store supports the string variant but not the list variant of this filter). | 
| List contains | Not available | [listContains](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-listContains) | string | Attribute must be a string list. Attribute name matches the key and whose value is a list that contains the value that you provided as one of its members (currently best supported with Amazon OpenSearch Serverless vector stores). | 

To combine filtering operators, you can use the following logical operators:


**Logical operators**  

| Operator | Console | API filter field name | Filtered results | 
| --- | --- | --- | --- | 
| And | and | [andAll](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-andAll) | Results fulfill all of the filtering expressions in the group | 
| Or | or | [orAll](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrievalFilter.html#bedrock-Type-agent-runtime_RetrievalFilter-orAll) | Results fulfill at least one of the filtering expressions in the group | 

To learn how to filter results using metadata, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

Follow the console steps at [Query a knowledge base and retrieve data](kb-test-retrieve.md). When you open the **Configurations** pane, you'll see a **Filters section**. The following procedures describe different use cases:
+ To add a filter, create a filtering expression by entering a metadata attribute, filtering operator, and value in the box. Separate each part of the expression with a whitespace. Press **Enter** to add the filter.

  For a list of accepted filtering operators, see the **Filtering operators** table above. You can also see a list of filtering operators when you add a whitespace after the metadata attribute.
**Note**  
You must surround strings with quotation marks.

  For example, you can filter for results from source documents that contain a `genre` metadata attribute whose value is `"entertainment"` by adding the following filter: **genre = "entertainment"**.  
![Add one filter.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-one.png)
+ To add another filter, enter another filtering expression in the box and press **Enter**. You can add up to 5 filters in the group.  
![Add another filter.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-more.png)
+ By default, the query will return results that fulfill all the filtering expressions you provide. To return results that fulfill at least one of the filtering expressions, choose the **and** dropdown menu between any two filtering operations and select **or**.  
![Change the logical operation between filters.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-logical.png)
+ To combine different logical operators, select **\+ Add Group** to add a filter group. Enter filtering expressions in the new group. You can add up to 5 filter groups.  
![Add a filter group to combine different logical operators.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-group.png)
+ To change the logical operator used between all the filtering groups, choose the **AND** dropdown menu between any two filter groups and select **OR**.  
![Change the logical operation between filter groups.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-group-logical.png)
+ To edit a filter, select it, modify the filtering operation, and choose **Apply**.  
![Edit a filter.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-edit.png)
+ To remove a filter group, choose the trash can icon (![Trash can icon representing a delete action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/trash.png)) next to the group. To remove a filter, choose the delete icon (![Close or cancel icon represented by an "X" symbol.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/close.png)) next to the filter.  
![Delete a filter or filter group.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-delete.png)

The following image shows an example filter configuration that returns all documents written after **2018** whose genre is **"entertainment"**, in addition to documents whose genre is **"cooking"** or **"sports"** and whose author starts with **"C"**.

![Example filter configuration.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/filter-example.png)


------
#### [ API ]

When you make a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) or [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request, include a `retrievalConfiguration` field, mapped to a [KnowledgeBaseRetrievalConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalConfiguration.html) object. To see the location of this field, refer to the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html) and [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request bodies in the API reference.

The following JSON objects show the minimal fields required in the [KnowledgeBaseRetrievalConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_KnowledgeBaseRetrievalConfiguration.html) object to set filters for different use cases:

1. Use one filtering operator (see the **Filtering operators** table above).

   ```
   "retrievalConfiguration": {
       "vectorSearchConfiguration": {
           "filter": {
               "{{<filter-type>}}": {
                   "key": "string",
                   "value": "string" | number | boolean | ["string", "string", ...]
               }
           }
       }
   }
   ```

1. Use a logical operator (see the **Logical operators** table above) to combine up to 5.

   ```
   "retrievalConfiguration": {
       "vectorSearchConfiguration": {
           "filter": {
               "{{andAll | orAll}}": [
                   "{{<filter-type>}}": {
                       "key": "string",
                       "value": "string" | number | boolean | ["string", "string", ...]
                   },
                   "{{<filter-type>}}": {
                       "key": "string",
                       "value": "string" | number | boolean | ["string", "string", ...]
                   },
                   ...
               ]
           }
       }
   }
   ```

1. Use a logical operator to combine up to 5 filtering operators into a filter group, and a second logical operator to combine that filter group with another filtering operator.

   ```
   "retrievalConfiguration": {
       "vectorSearchConfiguration": {
           "filter": {
               "{{andAll | orAll}}": [
                   "{{andAll | orAll}}": [
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       ...
                   ],
                   "{{<filter-type>}}": {
                       "key": "string",
                       "value": "string" | number | boolean | ["string", "string", ...]
                   }
               ]
           }
       }
   }
   ```

1. Combine up to 5 filter groups by embedding them within another logical operator. You can create one level of embedding.

   ```
   "retrievalConfiguration": {
       "vectorSearchConfiguration": {
           "filter": {
               "{{andAll | orAll}}": [
                   "{{andAll | orAll}}": [
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       ...
                   ],
                   "{{andAll | orAll}}": [
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       "{{<filter-type>}}": {
                           "key": "string",
                           "value": "string" | number | boolean | ["string", "string", ...]
                       },
                       ...
                   ]
               ]
           }
       }
   }
   ```

The following table describes the filter types that you can use:


****  

| Field | Supported value data types | Filtered results | 
| --- | --- | --- | 
| equals | string, number, boolean | Attribute matches the value you provide | 
| notEquals | string, number, boolean | Attribute doesn't match the value you provide  | 
| greaterThan | number | Attribute is greater than the value you provide | 
| greaterThanOrEquals | number | Attribute is greater than or equal to the value you provide | 
| lessThan | number | Attribute is less than the value you provide  | 
| lessThanOrEquals | number | Attribute is less than or equal to the value you provide | 
| in | list of strings | Attribute is in the list you provide | 
| notIn | list of strings | Attribute isn't in the list you provide | 
| startsWith | string | Attribute starts with the string you provide (only supported for Amazon OpenSearch Serverless vector stores) | 

To combine filter types, you can use one of the following logical operators:


****  

| Field | Maps to | Filtered results | 
| --- | --- | --- | 
| andAll | List of up to 5 filter types | Results fulfill all of the filtering expressions in the group | 
| orAll | List of up to 5 filter types | Results fulfill at least one of the filtering expressions in the group | 

For examples, see [Send a query and include filters (Retrieve)](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html#API_agent-runtime_Retrieve_Example_2) and [Send a query and include filters (RetrieveAndGenerate)](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html#API_agent-runtime_RetrieveAndGenerate_Example_2).

------

## Guardrails
<a name="kb-managed-test-config-guardrails"></a>

You can implement safeguards for your knowledge base for your use cases and responsible AI policies. You can create multiple guardrails tailored to different use cases and apply them across multiple request and response conditions, providing a consistent user experience and standardizing safety controls across your knowledge base. You can configure denied topics to disallow undesirable topics and content filters to block harmful content in model inputs and responses. For more information, see [Detect and filter harmful content by using Amazon Bedrock Guardrails](guardrails.md).

**Note**  
Using guardrails with contextual grounding for knowledge bases is currently not supported on Claude 3 Sonnet and Haiku.

For general prompt engineering guidelines, see [Prompt engineering concepts](prompt-engineering-guidelines.md).

Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

Follow the console steps at [Query a knowledge base and retrieve data](kb-test-retrieve.md). In the test window, turn on **Generate responses**. Then, in the **Configurations** pane, expand the **Guardrails** section.

1. In the **Guardrails** section, choose the **Name** and the **Version** of your guardrail. If you would like to see the details for your chosen guardrail and version, choose **View**.

   Alternatively, you can create a new one by choosing the **Guardrail** link.

1. When you're finished editing, choose **Save changes**. To exit without saving choose **Discard changes**.

------
#### [ API ]

When you make a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request, include the `guardrailConfiguration` field within the `generationConfiguration` to use your guardrail with the request. To see the location of this field, refer to the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) request body in the API reference.

The following JSON object shows the minimal fields required in the [GenerationConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_GenerationConfiguration.html) to set the `guardrailConfiguration`:

```
"generationConfiguration": {
    "guardrailConfiguration": {
        "guardrailId": "{{string}}",
        "guardrailVersion": "{{string}}"
    }
}
```

Specify the `guardrailId` and `guardrailVersion` of your chosen guardrails. 

------

## Reranking
<a name="kb-managed-test-config-rerank"></a>

You can use a reranker model to rerank results from knowledge base query. Follow the console steps at [Query a knowledge base and retrieve data](kb-test-retrieve.md). When you open the **Configurations** pane, expand the **Reranking** section. Select a reranker model, update permissions if necessary, and modify any additional options. Enter a prompt and select **Run** to test the results after reranking.