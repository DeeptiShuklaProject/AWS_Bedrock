

# Include metadata in a data source to improve knowledge base query
<a name="kb-metadata"></a>

When ingesting CSV (comma separate values) files, you have the ability to have the knowledge base treat certain columns as content fields versus metadata fields. Instead of potentially having hundreds or thousands of content/metadata file pairs, you can now have a single CSV file and a corresponding metadata.json file, giving the knowledge base hints as to how to treat each column inside of your CSV.

There are limits for document metadata fields/attributes per chunk. See [Quotas for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)

Before ingesting a CSV file, make sure:
+ Your CSV is in RFC4180 format and is UTF-8 encoded.
+ The first row of your CSV includes header information.
+ Metadata fields provided in your metadata.json are present as columns in your CSV.
+ You provide a fileName.csv.metadata.json file with the following format:

  ```
  {
      "metadataAttributes": {
          "${attribute1}": "${value1}",
          "${attribute2}": "${value2}",
          ...
      },
      "documentStructureConfiguration": {
          "type": "RECORD_BASED_STRUCTURE_METADATA",
          "recordBasedStructureMetadata": {
              "contentFields": [
                  {
                      "fieldName": "string"
                  }
              ],
              "metadataFieldsSpecification": {
                  "fieldsToInclude": [
                      {
                          "fieldName": "string"
                      }
                  ],
                  "fieldsToExclude": [
                      {
                          "fieldName": "string"
                      }
                  ]
              }
          }
      }
  }
  ```

The CSV file is parsed one row at a time and the chunking strategy and vector embedding is applied to the content field. Amazon Bedrock knowledge bases currently supports one content field. The content field is split into chunks, and the metadata fields (columns) that are associated with each chunk are treated as string values.

For example, say there's a CSV with a column 'Description' and a column 'Creation\_Date'. The description field is the content field and the creation date is an associated metadata field. The description text is split into chunks and converted into vector embeddings for each row in the CSV. The creation date value is treated as string representation of the date and is associated with each chunk for the description.

If no inclusion/exclusion fields are provided, all columns are treated as metadata columns, except the content column. If only inclusion fields are provided, only the provided columns are treated as metadata. If only exclusion fields are provided, all columns, except the exclusion columns are treated as metadata. If you provide the same `fieldName` in both `fieldsToInclude` and `fieldsToExclude`, Amazon Bedrock throws a validation exception. If there’s a conflict between inclusion and exclusion, it will result in a failure.

Blank rows found inside a CSV are ignored or skipped.

## Example: Multi-row CSV with metadata
<a name="kb-metadata-csv-example"></a>

The following example shows a complete CSV file and its corresponding metadata JSON file.

**Example CSV file (`properties.csv`)**

```
description,city,price,bedrooms
"Spacious 3-bedroom home with updated kitchen and large backyard.",Seattle,450000,3
"Modern downtown condo with floor-to-ceiling windows and city views.",Portland,325000,2
"Charming craftsman bungalow with original hardwood floors.",Austin,275000,2
```

**Corresponding metadata file (`properties.csv.metadata.json`)**

```
{
    "metadataAttributes": {
        "source": "property_listings_2024"
    },
    "documentStructureConfiguration": {
        "type": "RECORD_BASED_STRUCTURE_METADATA",
        "recordBasedStructureMetadata": {
            "contentFields": [
                {
                    "fieldName": "description"
                }
            ],
            "metadataFieldsSpecification": {
                "fieldsToInclude": [
                    {
                        "fieldName": "city"
                    },
                    {
                        "fieldName": "price"
                    }
                ]
            }
        }
    }
}
```

In this example:
+ `contentFields` – Specifies one column (`description`) as the content to be chunked and embedded. Only one content field is supported.
+ `fieldsToInclude` – Specifies which columns (`city` and `price`) to treat as filterable metadata. The `bedrooms` column is excluded because it is not listed.
+ `metadataAttributes` – Specifies document-level metadata applied to every chunk from this CSV. In this example, `source` is a static attribute applied to all rows.

Each row produces one chunk. For the first row, the chunk text is the description, and the metadata is `city: "Seattle"`, `price: "450000"`, and `source: "property_listings_2024"`. All metadata values from CSV columns are stored as strings.

## Supported metadata data types
<a name="kb-metadata-data-types"></a>

The following data types are supported for metadata attributes:
+ `STRING` – A text value.
+ `NUMBER` – A numeric value. When using the CSV-based metadata configuration described on this page, number values are stored as strings.
+ `BOOLEAN` – A true or false value.
+ `STRING_LIST` – A list of string values.

For the full metadata attribute schema used in filtering queries, see [MetadataAttributeSchema](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_MetadataAttributeSchema.html) in the API Reference.

## Related metadata configuration options
<a name="kb-metadata-related"></a>

In addition to the CSV-based metadata configuration described on this page, you can also configure metadata using a sidecar `.metadata.json` file for any document type in an Amazon S3 data source. This method supports the full set of data types and the `includeForEmbedding` option. For more information, see [Document metadata fields](s3-data-source-connector.md#ds-s3-metadata-fields).

To learn how to filter query results using metadata, see the **Knowledge base prompt templates** section in [Configure and customize queries and response generation](kb-test-config.md).