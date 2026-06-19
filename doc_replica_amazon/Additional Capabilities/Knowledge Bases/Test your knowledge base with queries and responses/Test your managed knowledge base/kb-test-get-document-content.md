

# Retrieve the content of documents from knowledge base
<a name="kb-test-get-document-content"></a>

The `GetDocumentContent` API allows you to retrieve the content of documents that have been ingested into an Amazon Bedrock Knowledge Base. This API returns a pre-signed URL that provides temporary, secure access to download or view the original or extracted content of a document.

This is useful when you want to:
+ Access the source document referenced in a `Retrieve` API response
+ Download the original file (PDF, Word, HTML, etc.) from a knowledge base
+ Retrieve the extracted/parsed text content of a document in JSON format
+ Build applications that let users view or download source documents behind `Retrieve` API responses

## How it works
<a name="kb-get-doc-content-how-it-works"></a>

1. You call `GetDocumentContent` with the knowledge base ID, data source ID, and document ID.

1. The service validates your access permissions (including any ACL-based access controls configured on the knowledge base).

1. The API returns a pre-signed URL and the document's MIME type.

1. You use the pre-signed URL to download the document content. The URL expires after **5 minutes**.

## IAM permissions
<a name="kb-get-doc-content-iam"></a>

Calling `GetDocumentContent` requires both `bedrock:Retrieve` and `bedrock:GetDocumentContent` IAM actions on the knowledge base resource. This is because the API internally validates retrieval-level access before returning document content. Ensure your IAM policy includes both actions:

```
{
    "Effect": "Allow",
    "Action": [
        "bedrock:Retrieve",
        "bedrock:GetDocumentContent"
    ],
    "Resource": "arn:aws:bedrock:{{region}}:{{account-id}}:knowledge-base/{{kb-id}}"
}
```

## Usage examples
<a name="kb-get-doc-content-examples"></a>

### Same account with ACL enabled
<a name="kb-get-doc-content-same-account-acl"></a>

When your knowledge base has ACL-based access control enabled, pass `userContext` with the user's identity to ensure document-level permission checks:

```
import boto3
import requests

client = boto3.client('bedrock-agent-runtime')

# Step 1: Retrieve relevant documents
retrieve_response = client.retrieve(
    knowledgeBaseId='{{KBID1234567}}',
    retrievalQuery={'text': 'What is the refund policy?'}
)

# Step 2: Get the full document content for the top result
result = retrieve_response['retrievalResults'][0]

doc_response = client.get_document_content(
    knowledgeBaseId='{{KBID1234567}}',
    dataSourceId=result['metadata']['_data_source_id'],
    documentId=result['documentId'],
    outputFormat='RAW',
    userContext={
        'userId': '{{user-email}}',
        'groups': [
            {'id': '{{group-engineering}}'},
            {'id': '{{group-project-alpha}}'}
        ]
    }
)

# Step 3: Download the document
download = requests.get(doc_response['presignedUrl'])
with open('document.pdf', 'wb') as f:
    f.write(download.content)
```

### Same account without ACL enabled
<a name="kb-get-doc-content-same-account-no-acl"></a>

When ACLs are not configured, omit `userContext`:

```
import boto3
import requests

client = boto3.client('bedrock-agent-runtime')

# Step 1: Retrieve relevant documents
retrieve_response = client.retrieve(
    knowledgeBaseId='{{KBID1234567}}',
    retrievalQuery={'text': 'What is the refund policy?'}
)

# Step 2: Get the full document content
result = retrieve_response['retrievalResults'][0]

doc_response = client.get_document_content(
    knowledgeBaseId='{{KBID1234567}}',
    dataSourceId=result['metadata']['_data_source_id'],
    documentId=result['documentId'],
    outputFormat='RAW'
)

# Step 3: Download the document
download = requests.get(doc_response['presignedUrl'])
with open('document.pdf', 'wb') as f:
    f.write(download.content)
```

### Cross-account without ACL enabled
<a name="kb-get-doc-content-cross-account"></a>

For cross-account access, the knowledge base owner must attach a **resource policy** to their knowledge base that grants the caller's account permission. Then the caller uses the full knowledge base ARN.

**Step 1: KB owner attaches a resource policy to the knowledge base**

The account that owns the knowledge base (for example, `999999999999`) must attach a resource policy granting the caller account (for example, `111111111111`) access:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "111111111111"
            },
            "Action": [
                "bedrock:Retrieve",
                "bedrock:GetDocumentContent"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:999999999999:knowledge-base/{{KBID1234567}}"
        }
    ]
}
```

This is done via the `PutKnowledgeBaseResourcePolicy` API or through the Amazon Bedrock console.

**Step 2: Caller account has IAM permissions to invoke the API**

The caller's IAM role/user (in account `111111111111`) needs an IAM policy allowing the actions on the cross-account KB ARN:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock:GetDocumentContent"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:999999999999:knowledge-base/{{KBID1234567}}"
        }
    ]
}
```

**Step 3: Call the API using the full KB ARN**

```
import boto3
import requests

client = boto3.client('bedrock-agent-runtime')

CROSS_ACCOUNT_KB_ARN = 'arn:aws:bedrock:us-east-1:999999999999:knowledge-base/{{KBID1234567}}'

# Step 1: Retrieve relevant documents using the KB ARN
retrieve_response = client.retrieve(
    knowledgeBaseId=CROSS_ACCOUNT_KB_ARN,
    retrievalQuery={'text': 'What is the refund policy?'}
)

# Step 2: Get the full document content using the same ARN
result = retrieve_response['retrievalResults'][0]

doc_response = client.get_document_content(
    knowledgeBaseId=CROSS_ACCOUNT_KB_ARN,
    dataSourceId=result['metadata']['_data_source_id'],
    documentId=result['documentId'],
    outputFormat='RAW'
)

# Step 3: Download the document
download = requests.get(doc_response['presignedUrl'])
with open('document.pdf', 'wb') as f:
    f.write(download.content)
```

Both the resource policy (on the KB owner side) and the IAM policy (on the caller side) must be in place. Access is denied if either is missing.