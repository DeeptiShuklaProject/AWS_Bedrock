

# Document-level access controls
<a name="kb-managed-ds-s3-acl"></a>

**ACL awareness is not authorization**  
Bedrock Managed Knowledge Base provides ACL-aware filtering, not a security boundary. Bedrock Managed Knowledge Base does not authenticate end users — your application is responsible for authenticating users and passing verified identity context. Because Bedrock Managed Knowledge Base cannot verify the authenticity of the user context you provide, this feature filters results based on the identity you supply but does not constitute true authorization. You must not rely on this feature as a sole access control mechanism without upstream authentication.

Amazon S3 data sources optionally support document-level access control. Unlike other connectors, Amazon S3 has no native permission system to crawl, so you define ACLs through configuration files that you manage. For the overview of ACL awareness across all connectors, see [Access Control Lists awareness enablement](kb-managed-acl.md).

## How it works
<a name="kb-managed-ds-s3-acl-how"></a>

For an ACL-enabled Amazon S3 data source, Bedrock Managed Knowledge Base applies the customer-provided access control lists during pre-retrieval filtering, returning only documents the querying user is permitted to access. Real-time ACL verification is not supported for Amazon S3 because the customer-provided ACL metadata is the source of truth.

## Enable ACL awareness
<a name="kb-managed-ds-s3-acl-enable"></a>

To enable ACL awareness for an Amazon S3 data source, set `aclEnabled` to `true` in the `connectorParameters` and define access permissions using one of two methods:
+ **Global ACL configuration file** — A single centralized JSON file that defines access permissions at the folder (prefix) level. Ideal for organizations with stable permission structures. Changes to the global file require reindexing the affected prefix.
+ **Document-level metadata files** — Each document has its own metadata file containing access control information. This enables faster index updates when permissions change because only affected documents need reindexing.

**Important**  
For ACL-enabled Amazon S3 data sources, documents without an associated ACL entry are not ingested. Ensure every document has an ACL defined either through the global ACL file or in its metadata file.

```
"connectorParameters": {
    "type": "S3",
    "version": "1",
    "aclEnabled": true,
    "connectionConfiguration": {
        "bucketName": "{{your-bucket-name}}",
        "bucketOwnerAccountId": "{{123456789012}}"
    },
    "aclConfiguration": {
        "globalAccessControlListS3Uri": "s3://{{your-bucket-name}}/{{acl/global-acl.json}}"
    }
}
```

## Global ACL file structure
<a name="kb-managed-ds-s3-acl-global"></a>

The global ACL file is a JSON array where each entry maps a key prefix to a set of access control entries. Each `keyPrefix` is the absolute Amazon S3 URI of a folder (applying to all documents under it) or an individual document.

```
[
    {
        "keyPrefix": "s3://{{your-bucket-name}}/{{finance/}}",
        "aclEntries": [
            {
                "Name": "{{user1@example.com}}",
                "Type": "USER",
                "Access": "ALLOW"
            }
        ]
    }
]
```

Each `aclEntries` element contains:
+ `Name` — The email address of a user.
+ `Type` — Must be `USER`.
+ `Access` — Either `ALLOW` or `DENY`. Deny overrides allow.

## Per-document metadata files
<a name="kb-managed-ds-s3-acl-perdoc"></a>

As an alternative to the global ACL file, you can define ACLs per document using metadata files. For each document, create a file named `{{filename}}.metadata.json` in the same Amazon S3 path. Include an `accessControlList` array with the same entry format as the global file.

```
{
    "metadataAttributes": {},
    "accessControlList": [
        {
            "Name": "{{user1@example.com}}",
            "Type": "USER",
            "Access": "ALLOW"
        },
        {
            "Name": "{{user2@example.com}}",
            "Type": "USER",
            "Access": "DENY"
        }
    ]
}
```

Per-document metadata takes precedence over the global ACL file. If a document has both a matching global prefix entry and a per-document metadata file, the per-document metadata is used.

**Note**  
The ACL configuration file must be stored in the same Amazon S3 bucket as your data source content.

## Verify your configuration
<a name="kb-managed-ds-s3-acl-verify"></a>

Because Amazon S3 ACLs are customer-provided, validate them before you query:

1. Confirm `aclEnabled` is `true` in the data source's `connectorParameters`.

1. Confirm every document has an ACL — either an entry in the global ACL file or a per-document `.metadata.json` file. Documents without an ACL are not ingested.

1. Validate the ACL JSON: each entry has `Name` (user email), `Type` (`USER`), and `Access` (`ALLOW` or `DENY`), and the ACL files are in the same bucket as your content.

1. Confirm a test user's email exactly matches the `Name` in an `ALLOW` entry for a document you expect them to retrieve.

## Troubleshooting
<a name="kb-managed-ds-s3-acl-troubleshooting"></a>

**Note**  
ACL misconfigurations do not produce explicit errors during retrieval. Retrieval fails closed: affected documents are silently omitted, so a query returns fewer or zero results rather than an error. Use the verification checks above to diagnose these issues.


**ACL-enabled Amazon S3 symptoms, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Retrieve returns 0 results for a user who should have access. | The user's email does not match any ACL entry (email mismatch). | Ensure the ACL Name matches the user's email exactly. | 
| A document is never returned to anyone. | The document has no ACL entry, so it was not ingested. | Add an ACL for the document through the global ACL file or a per-document .metadata.json file, then resync. | 
| A per-document ACL is not taking effect. | The .metadata.json file is misnamed or in the wrong path. | Name it {{filename}}.metadata.json in the same S3 path; per-document metadata overrides the global file. | 
| ACL changes are not reflected. | Global ACL file changes require reindexing of the affected prefix. | Resync the affected prefix. | 