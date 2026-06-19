

# Prerequisites for your Amazon Bedrock knowledge base data
<a name="knowledge-base-ds"></a>

A data source contains files or content with information that can be retrieved when your knowledge base is queried. You must store your documents or content in at least one of the [supported data sources](https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html).

## Supported document formats and limits for knowledge base data
<a name="kb-ds-supported-doc-formats-limits"></a>

When you connect to a [supported data source](https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html), the content is ingested into your knowledge base.

If you use Amazon S3 to store your files or your data source includes attached files, then you first must check that each source document file adheres to the following:
+ The source files are of the following supported formats:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html)
+ Each file size doesn't exceed the quota of 50 MB.

**Note**  
The maximum chunk size quota (measured in KB) refers to the size of individual text chunks after your documents are split by the chunking strategy — not the maximum size of the source document itself. Documents larger than the chunk size are automatically split into multiple chunks. For approximately 1 KB of plain text, expect roughly 1,000 characters or 200–250 English words.

If you use an Amazon S3 or custom data source, you can use multimodal data, including JPEG (.jpeg) or PNG (.png) images or files that contain tables, charts, diagrams, or other images.

**Note**  
The maximum size of .JPEG and .PNG files is 3.75 MB.