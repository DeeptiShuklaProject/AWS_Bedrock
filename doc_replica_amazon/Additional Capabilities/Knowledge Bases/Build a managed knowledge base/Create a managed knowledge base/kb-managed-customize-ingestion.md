

# Customize ingestion for a data source
<a name="kb-managed-customize-ingestion"></a>

You can customize vector ingestion when connecting a data source in the AWS Management Console or by modifying the value of the `vectorIngestionConfiguration` field when sending a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request.

Select a topic to learn how to include configurations for customizing ingestion when connecting to a data source:

**Topics**
+ [Use smart parsing](#kb-managed-customize-parsing)
+ [Choose a chunking strategy](#kb-managed-customize-chunking)

## Use smart parsing
<a name="kb-managed-customize-parsing"></a>

Managed knowledge bases use smart parsing by default. Smart parsing is a service-managed parsing strategy that automatically selects the best parsing approach for your content. You do not need to configure a parsing model or provide additional settings.

To use smart parsing, you can either omit the `parsingConfiguration` field from the `vectorIngestionConfiguration`, or explicitly specify it as follows:

```
{
    "parsingConfiguration": {
        "parsingStrategy": "SMART_PARSING"
    }
}
```

**Note**  
Managed knowledge bases only support the `SMART_PARSING` strategy. Other parsing strategies such as `BEDROCK_FOUNDATION_MODEL` and `BEDROCK_DATA_AUTOMATION` are not supported.

## Choose a chunking strategy
<a name="kb-managed-customize-chunking"></a>

You can customize how the documents in your data are chunked for storage and retrieval. To learn about options for chunking data in Amazon Bedrock Knowledge Bases, see [How content chunking works for knowledge bases](kb-chunking.md).

**Warning**  
You can't change the chunking strategy after connecting to the data source.

In the AWS Management Console you choose the chunking strategy when connecting to a data source. With the Amazon Bedrock API, you include a [ChunkingConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ChunkingConfiguration.html) in the `chunkingConfiguration` field of the [VectorIngestionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorIngestionConfiguration.html).

If you omit this configuration or specify the default chunking strategy, the service uses fixed-size chunking with 300 tokens and 20% overlap.

```
{
    "chunkingConfiguration": {
        "chunkingStrategy": "DEFAULT"
    }
}
```

Expand the section that corresponds to the chunking strategy that you want to use:

### No chunking
<a name="w2aac32c12c23c13c17c11c15b1"></a>

To treat each document in your data source as a single source chunk, specify `NONE` in the `chunkingStrategy` field of the `ChunkingConfiguration`, as in the following format:

```
{
    "chunkingStrategy": "NONE"
}
```

### Fixed-size chunking
<a name="w2aac32c12c23c13c17c11c15b3"></a>

To divide each document in your data source into chunks of approximately the same size, specify `FIXED_SIZE` in the `chunkingStrategy` field of the `ChunkingConfiguration` and include a [FixedSizeChunkingConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FixedSizeChunkingConfiguration.html) in the `fixedSizeChunkingConfiguration` field, as in the following format:

```
{
    "chunkingStrategy": "FIXED_SIZE",
    "fixedSizeChunkingConfiguration": {
        "maxTokens": number,
        "overlapPercentage": number
    }
}
```

**Note**  
Semantic chunking is not supported for managed knowledge bases.