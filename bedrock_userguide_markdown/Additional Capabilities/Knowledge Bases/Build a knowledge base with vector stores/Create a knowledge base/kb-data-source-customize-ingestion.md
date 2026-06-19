

# Customize ingestion for a data source
<a name="kb-data-source-customize-ingestion"></a>

You can customize vector ingestion when connecting a data source in the AWS Management Console or by modifying the value of the `vectorIngestionConfiguration` field when sending a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request.

Select a topic to learn how to include configurations for customizing ingestion when connecting to a data source:

**Topics**
+ [Choose the tool to use for parsing](#kb-data-source-customize-parsing)
+ [Choose a chunking strategy](#kb-data-source-customize-chunking)
+ [Use a Lambda function during ingestion](#kb-data-source-customize-lambda)

## Choose the tool to use for parsing
<a name="kb-data-source-customize-parsing"></a>

You can customize how the documents in your data are parsed. To learn about options for parsing data in Amazon Bedrock Knowledge Bases, see [Parsing options for your data source](kb-advanced-parsing.md).

**Warning**  
You can't change the parsing strategy type (for example, from `BEDROCK_FOUNDATION_MODEL` to `BEDROCK_DATA_AUTOMATION`) after connecting to the data source. To use a different parsing strategy type, you must add a new data source. However, you can update configuration parameters within the same parsing strategy, such as the `modelArn` in `bedrockFoundationModelConfiguration` or the `parsingPrompt`. When updating, retrieve the complete existing configuration using `GetDataSource` and pass the full `vectorIngestionConfiguration` with only the specific values modified.  
You can't add an S3 location to store multimodal data (including images, figures, charts, and tables) after you've created a knowledge base. If you want to include multimodal data and use a parser that supports it, you must create a new knowledge base.

The steps involved in choosing a parsing strategy depend on whether you use the AWS Management Console or the Amazon Bedrock API and the parsing method you choose. If you choose a parsing method that supports multimodal data, you must specify an S3 URI in which to store the multimodal data extracted from your documents. This data can be returned in knowledge base query.
+ In the AWS Management Console, do the following:

  1. Select the parsing strategy when you connect to a data source while setting up a knowledge base or when you add a new data source to your existing knowledge base.

  1. (If you choose Amazon Bedrock Data Automation or a foundation model as your parsing strategy) Specify an S3 URI in which to store the multimodal data extracted from your documents in the **Multimodal storage destination** section when you select an embeddings model and configure your vector store. You can also optionally use a customer managed key to encrypt your S3 data at this step.
+ In the Amazon Bedrock API, do the following:

  1. (If you plan to use Amazon Bedrock Data Automation or a foundation model as your parsing strategy) Include a [SupplementalDataStorageLocation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_SupplementalDataStorageLocation.html) in the [VectorKnowledgeBaseConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorKnowledgeBaseConfiguration.html) of a [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request.

  1. Include a [ParsingConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ParsingConfiguration.html) in the `parsingConfiguration` field of the [VectorIngestionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorIngestionConfiguration.html) in the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request.
**Note**  
If you omit this configuration, Amazon Bedrock Knowledge Bases uses the Amazon Bedrock default parser.

For more details about how to specify a parsing strategy in the API, expand the section that corresponds to the parsing strategy that you want to use:

### Amazon Bedrock default parser
<a name="w2aac32c12c25c15c17c11c13b1"></a>

To use the default parser, don't include a `parsingConfiguration` field within the `VectorIngestionConfiguration`.

### Amazon Bedrock Data Automation parser (preview)
<a name="w2aac32c12c25c15c17c11c13b3"></a>

To use the Amazon Bedrock Data Automation parser, specify `BEDROCK_DATA_AUTOMATION` in the `parsingStrategy` field of the `ParsingConfiguration` and include a [BedrockDataAutomationConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_BedrockDataAutomationConfiguration.html) in the `bedrockDataAutomationConfiguration` field, as in the following format:

```
{
    "parsingStrategy": "BEDROCK_DATA_AUTOMATION",
    "bedrockDataAutomationConfiguration": {
        "parsingModality": "string"
    }
}
```

### Foundation model
<a name="w2aac32c12c25c15c17c11c13b5"></a>

To use a foundation model as a parser, specify the `BEDROCK_FOUNDATION_MODEL` in the `parsingStrategy` field of the `ParsingConfiguration` and include a [BedrockFoundationModelConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_BedrockFoundationModelConfiguration.html) in the `bedrockFoundationModelConfiguration` field, as in the following format:

```
{
    "parsingStrategy": "BEDROCK_FOUNDATION_MODEL",
    "bedrockFoundationModelConfiguration": {
        "modelArn": "string",
        "parsingModality": "string",
        "parsingPrompt": {
            "parsingPromptText": "string"
        }
    }
}
```

## Choose a chunking strategy
<a name="kb-data-source-customize-chunking"></a>

You can customize how the documents in your data are chunked for storage and retrieval. To learn about options for chunking data in Amazon Bedrock Knowledge Bases, see [How content chunking works for knowledge bases](kb-chunking.md).

**Warning**  
You can't change the chunking strategy after connecting to the data source.

In the AWS Management Console you choose the chunking strategy when connecting to a data source. With the Amazon Bedrock API, you include a [ChunkingConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ChunkingConfiguration.html) in the `chunkingConfiguration` field of the [VectorIngestionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorIngestionConfiguration.html).

**Note**  
If you omit this configuration, Amazon Bedrock splits your content into chunks of approximately 300 tokens, while preserving sentence boundaries.

Expand the section that corresponds to the parsing strategy that you want to use:

### No chunking
<a name="w2aac32c12c25c15c17c13c13b1"></a>

To treat each document in your data source as a single source chunk, specify `NONE` in the `chunkingStrategy` field of the `ChunkingConfiguration`, as in the following format:

```
{
    "chunkingStrategy": "NONE"
}
```

### Fixed-size chunking
<a name="w2aac32c12c25c15c17c13c13b3"></a>

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

### Hierarchical chunking
<a name="w2aac32c12c25c15c17c13c13b5"></a>

To divide each document in your data source into two levels, where the second layer contains smaller chunks derived from the first layer, specify `HIERARCHICAL` in the `chunkingStrategy` field of the `ChunkingConfiguration` and include the `hierarchicalChunkingConfiguration` field, as in the following format:

```
{
    "chunkingStrategy": "HIERARCHICAL",
    "hierarchicalChunkingConfiguration": {
        "levelConfigurations": [{
            "maxTokens": number
        }],
        "overlapTokens": number
    }
}
```

### Semantic chunking
<a name="w2aac32c12c25c15c17c13c13b7"></a>

To divide each document in your data source into chunks that prioritize semantic meaning over syntactic structure, specify `SEMANTIC` in the `chunkingStrategy` field of the `ChunkingConfiguration` and include the `semanticChunkingConfiguration` field, as in the following format:

```
{
    "chunkingStrategy": "SEMANTIC",
    "semanticChunkingConfiguration": {
        "breakpointPercentileThreshold": number,
        "bufferSize": number,
        "maxTokens": number
    }
}
```

## Use a Lambda function during ingestion
<a name="kb-data-source-customize-lambda"></a>

You can post-process how the source chunks from your data are written to the vector store with a Lambda function in the following ways:
+ Include chunking logic to provide a custom chunking strategy.
+ Include logic to specify chunk-level metadata.

To learn about writing a custom Lambda function for ingestion, see [Use a custom transformation Lambda function to define how your data is ingested](kb-custom-transformation.md). In the AWS Management Console you choose the Lambda function when connecting to a data source. With the Amazon Bedrock API, you include a [CustomTransformationConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CustomTransformationConfiguration.html) in the `CustomTransformationConfiguration` field of the [VectorIngestionConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorIngestionConfiguration.html) and specify the ARN of the Lambda, as in the following format:

```
{
    "transformations": [{
        "transformationFunction": {
            "transformationLambdaConfiguration": {
                "lambdaArn": "string"
            }
        },
        "stepToApply": "POST_CHUNKING"
    }],
    "intermediateStorage": {
        "s3Location": {
            "uri": "string"
        }
    }
}
```

You also specify the S3 location in which to store the output after applying the Lambda function.

You can include the `chunkingConfiguration` field to apply the Lambda function after applying one of the chunking options that Amazon Bedrock offers.