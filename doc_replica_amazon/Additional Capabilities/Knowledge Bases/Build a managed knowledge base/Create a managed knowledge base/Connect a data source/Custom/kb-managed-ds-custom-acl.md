

# Document-level access controls
<a name="kb-managed-ds-custom-acl"></a>

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

Custom data sources optionally support document-level access control. Unlike crawled connectors, a custom data source has no native permission system, so you supply the access control list (ACL) for each document when you ingest it with the `IngestKnowledgeBaseDocuments` operation. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## How it works
<a name="kb-managed-ds-custom-acl-how"></a>

For an ACL-enabled custom data source, Bedrock Managed Knowledge Base applies the customer-provided access control lists during pre-retrieval filtering, returning only documents the querying user is permitted to access. Real-time ACL verification is not supported for custom data sources because the customer-provided ACL metadata is the source of truth.

## Enable ACL awareness
<a name="kb-managed-ds-custom-acl-enable"></a>

To enable ACL awareness for a custom data source, set `aclEnabled` to `true` in the `connectorParameters` when you create or update the data source. For the data source configuration structure, see [Custom](kb-managed-ds-custom.md).

```
"connectorParameters": {
    "type": "CUSTOM",
    "version": "1",
    "aclEnabled": true
}
```

## Provide access controls when you ingest documents
<a name="kb-managed-ds-custom-acl-ingest"></a>

You provide a document's ACL through the `accessControlList` field on the document's `metadata` in the `IngestKnowledgeBaseDocuments` request. The ACL source is determined by `metadata.type`, the same field that controls where metadata attributes come from:
+ **`IN_LINE_ATTRIBUTE`** — The ACL is read from the `accessControlList` array in the request body.
+ **`S3_LOCATION`** — The ACL is read from the `accessControlList` array in the document's `.metadata.json` file in Amazon S3.

Because `accessControlList` lives under `metadata` rather than as a top-level field on `KnowledgeBaseDocument`, a document has a single ACL source, controlled by `metadata.type`. This prevents conflicting ACLs from being supplied for the same document (for example, an inline ACL on the request and an ACL in the S3 file). The tradeoff is that you cannot mix an inline ACL with S3-based metadata attributes, or S3-based ACL with inline metadata attributes, for the same document.

Each `accessControlList` entry contains:
+ `name` — The email address of a user.
+ `type` — Must be `USER`.
+ `access` — Either `ALLOW` or `DENY`. Deny overrides allow.

### Inline ACL (metadata.type = IN\_LINE\_ATTRIBUTE)
<a name="kb-managed-ds-custom-acl-inline"></a>

Supply the `accessControlList` directly in the request body alongside the inline metadata attributes.

```
PUT /knowledgebases/{{KB12345678}}/datasources/{{DS12345678}}/documents HTTP/1.1
Content-type: application/json

{
    "documents": [
        {
            "content": {
                "dataSourceType": "CUSTOM",
                "custom": {
                    "customDocumentIdentifier": {
                        "id": "hr-policy-2026"
                    },
                    "inlineContent": {
                        "textContent": {
                            "data": "Annual leave policy: All full-time employees are entitled to..."
                        },
                        "type": "TEXT"
                    },
                    "sourceType": "IN_LINE"
                }
            },
            "metadata": {
                "type": "IN_LINE_ATTRIBUTE",
                "inlineAttributes": [
                    {
                        "key": "department",
                        "value": { "stringValue": "HR", "type": "STRING" }
                    }
                ],
                "accessControlList": [
                    {
                        "name": "{{alice@example.com}}",
                        "type": "USER",
                        "access": "ALLOW"
                    },
                    {
                        "name": "{{bob@example.com}}",
                        "type": "USER",
                        "access": "DENY"
                    }
                ]
            }
        }
    ]
}
```

### S3-based ACL (metadata.type = S3\_LOCATION)
<a name="kb-managed-ds-custom-acl-s3"></a>

Point the document's metadata at a `.metadata.json` file in Amazon S3. Both the metadata attributes and the `accessControlList` are read from that file.

```
"metadata": {
    "type": "S3_LOCATION",
    "s3Location": {
        "uri": "s3://{{amzn-s3-demo-bucket}}/{{hr-policy-2026}}.metadata.json"
    }
}
```

The `.metadata.json` file uses the same format as the [per-document metadata files](kb-managed-ds-s3-acl.md#kb-managed-ds-s3-acl-perdoc) for Amazon S3 data sources. This file uses capitalized ACL field names (`Name`, `Type`, `Access`), which differ from the lowercase field names (`name`, `type`, `access`) used in the inline request.

```
{
    "metadataAttributes": {},
    "accessControlList": [
        {
            "Name": "{{alice@example.com}}",
            "Type": "USER",
            "Access": "ALLOW"
        },
        {
            "Name": "{{bob@example.com}}",
            "Type": "USER",
            "Access": "DENY"
        }
    ]
}
```

## Verify your configuration
<a name="kb-managed-ds-custom-acl-verify"></a>

Because Custom ACLs are customer-provided through `IngestKnowledgeBaseDocuments`, validate them before you query:

1. Confirm `aclEnabled` is `true` in the data source's `connectorParameters` (`type` `CUSTOM`).

1. Confirm each ingested document includes an `accessControlList` under `metadata`, and that `metadata.type` matches the ACL source (`IN_LINE_ATTRIBUTE` for inline, `S3_LOCATION` for an S3 file).

1. Confirm the ACL entry field casing matches the source: lowercase `name`/`type`/`access` for inline ACLs, capitalized `Name`/`Type`/`Access` for the S3 `.metadata.json` file.

1. Confirm a test user's email exactly matches the `name` in an `ALLOW` entry for a document you expect them to retrieve.

## Troubleshooting
<a name="kb-managed-ds-custom-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the verification checks above to diagnose these issues.


**ACL-enabled Custom symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results for a user who should have access. | The userId email does not match any accessControlList entry. | Align the user's email with the name in an ALLOW entry. | 
| An inline ACL is rejected or ignored. | Wrong field casing, or metadata.type is not IN\_LINE\_ATTRIBUTE. | Use lowercase name/type/access and set metadata.type to IN\_LINE\_ATTRIBUTE. | 
| An S3-based ACL is not applied. | metadata.type is not S3\_LOCATION, or the .metadata.json file is missing accessControlList. | Set metadata.type to S3\_LOCATION and include accessControlList in the file. | 
| A document is never returned to anyone. | The document was ingested without an accessControlList. | Re-ingest the document with an accessControlList. | 