

# Send and process a document with Amazon Nova on Amazon Bedrock
<a name="bedrock-runtime_example_bedrock-runtime_DocumentUnderstanding_AmazonNova_section"></a>

The following code example shows how to send and process a document with Amazon Nova on Amazon Bedrock.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples). 
Send and process a document with Amazon Nova on Amazon Bedrock.  

```
# Send and process a document with Amazon Nova on Amazon Bedrock.

import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g. Amazon Nova Lite.
model_id = "amazon.nova-lite-v1:0"

# Load the document
with open("example-data/amazon-nova-service-cards.pdf", "rb") as file:
    document_bytes = file.read()

# Start a conversation with a user message and the document
conversation = [
    {
        "role": "user",
        "content": [
            {"text": "Briefly compare the models described in this document"},
            {
                "document": {
                    # Available formats: html, md, pdf, doc/docx, xls/xlsx, csv, and txt
                    "format": "pdf",
                    "name": "Amazon Nova Service Cards",
                    "source": {"bytes": document_bytes},
                }
            },
        ],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 500, "temperature": 0.3},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
```
+  For API details, see [Converse](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/Converse) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.