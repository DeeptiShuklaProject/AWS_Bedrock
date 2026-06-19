

# Resource policies for managed knowledge bases
<a name="kb-managed-cross-account"></a>

A resource-based policy is a JSON document that you attach directly to a managed knowledge base. It controls which IAM principals can perform actions on the knowledge base, enabling use cases such as cross-account access. The policy supports both `Allow` and `Deny` effects.

**Important**  
Resource-based policies are supported only for managed knowledge bases (type `MANAGED`). Vector knowledge bases (type `VECTOR`) do not support resource policies.

## Supported actions
<a name="kb-managed-cross-account-supported-actions"></a>

The following actions can be used in a knowledge base resource policy:


****  

| Action | Description | 
| --- | --- | 
| bedrock:Retrieve | Query the knowledge base and retrieve relevant results from the data sources. | 
| bedrock:GetDocumentContent | Retrieve the full content of a specific document from the knowledge base data source. | 

**Note**  
Control-plane operations such as `GetKnowledgeBase`, `UpdateKnowledgeBase`, `DeleteKnowledgeBase`, and data source management operations cannot be used in resource policies. These operations must be performed by principals in the knowledge base owner account.

## Resource policy requirements
<a name="kb-managed-cross-account-resource-policy"></a>

Knowledge base resource policies follow standard IAM policy syntax. For details on policy elements and evaluation logic, see [IAM JSON policy elements reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html) in the *AWS Identity and Access Management User Guide*.

The following service-specific constraints apply:
+ **Only managed knowledge bases.** Resource policies can only be attached to knowledge bases of type `MANAGED`. Attempting to attach a resource policy to a `VECTOR` type knowledge base returns an error.
+ **Supported actions.** Only `bedrock:Retrieve` and `bedrock:GetDocumentContent` can be used in resource policies.
+ **No wildcards in Resource or Action.** You must specify the full knowledge base ARN in the `Resource` element and explicitly list each action. Wildcards are not supported in these elements.

## How cross-account access works
<a name="kb-managed-cross-account-how-it-works"></a>

Cross-account access allows principals in other AWS accounts to call `Retrieve` and `GetDocumentContent` on your knowledge base. For cross-account access to work, both of the following conditions must be met:
+ The knowledge base owner attaches a resource policy that grants access to the calling principal.
+ The calling principal has an identity-based policy that allows the corresponding Amazon Bedrock actions on the knowledge base ARN.

For more information about how IAM evaluates cross-account access, see [Cross-account policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic-cross-account.html) in the AWS Identity and Access Management User Guide.

**Example: Grant cross-account access**

The following resource policy grants a specific IAM role in another account permission to call `Retrieve` and `GetDocumentContent`:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCrossAccountRetrieve",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{CONSUMER_ACCOUNT_ID}}:role/{{service-role-name}}"
            },
            "Action": [
                "bedrock:Retrieve",
                "bedrock:GetDocumentContent"
            ],
            "Resource": "arn:aws:bedrock:{{REGION}}:{{OWNER_ACCOUNT_ID}}:knowledge-base/{{KB_ID}}"
        }
    ]
}
```

**Granting access to multiple principals**

To grant access to multiple consuming roles, list each role ARN in `Principal.AWS` as an array:

```
"Principal": {
    "AWS": [
        "arn:aws:iam::{{ACCOUNT_ID_1}}:role/{{role-name-1}}",
        "arn:aws:iam::{{ACCOUNT_ID_2}}:role/{{role-name-2}}"
    ]
}
```

To grant access to all principals in another account, use the account root as the principal:

```
"Principal": {
    "AWS": "arn:aws:iam::{{CONSUMER_ACCOUNT_ID}}:root"
}
```

## Using Deny statements
<a name="kb-managed-cross-account-deny"></a>

Resource policies support both `Allow` and `Deny` effects. An explicit `Deny` in a resource policy overrides any `Allow` in the principal's identity-based policy.

```
{
    "Sid": "DenySpecificPrincipals",
    "Effect": "Deny",
    "Principal": {
        "AWS": "arn:aws:iam::{{ACCOUNT_ID}}:role/{{role-name}}"
    },
    "Action": [
        "bedrock:Retrieve",
        "bedrock:GetDocumentContent"
    ],
    "Resource": "arn:aws:bedrock:{{REGION}}:{{OWNER_ACCOUNT_ID}}:knowledge-base/{{KB_ID}}"
}
```

## Manage resource policies
<a name="kb-managed-cross-account-manage-policies"></a>

To manage resource policies on knowledge bases, the knowledge base owner's IAM principal needs the following permissions:


****  

| Action | Description | 
| --- | --- | 
| bedrock:PutResourcePolicy | Attach or update a resource-based policy on a knowledge base. | 
| bedrock:GetResourcePolicy | View the resource-based policy attached to a knowledge base. | 
| bedrock:DeleteResourcePolicy | Remove the resource-based policy from a knowledge base. | 

**Example policy for the knowledge base owner**

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:PutResourcePolicy",
                "bedrock:GetResourcePolicy",
                "bedrock:DeleteResourcePolicy"
            ],
            "Resource": "arn:aws:bedrock:{{REGION}}:{{ACCOUNT_ID}}:knowledge-base/{{KB_ID}}"
        }
    ]
}
```

**API operations**

**PutResourcePolicy** — Attaches or replaces a resource-based policy on a knowledge base.

```
PUT /resourcepolicy/{{{knowledgeBaseArn}}} HTTP/1.1
Content-Type: application/json

{
    "policy": "{{{policyDocument}}}"
}
```

The `policy` field is a JSON-escaped string containing the policy document.

**GetResourcePolicy** — Returns the resource-based policy currently attached to a knowledge base.

```
GET /resourcepolicy/{{{knowledgeBaseArn}}} HTTP/1.1
```

Returns a `ResourceNotFoundException` if no policy is attached.

**DeleteResourcePolicy** — Removes the resource-based policy from a knowledge base.

```
DELETE /resourcepolicy/{{{knowledgeBaseArn}}} HTTP/1.1
```

## Resource policy versioning
<a name="kb-managed-cross-account-version-parameter"></a>

When you call `PutResourcePolicy`, the API returns a `policyRevisionId` that represents the current version of the policy. You can optionally include this revision ID in subsequent `PutResourcePolicy` calls to enforce optimistic locking.
+ If you provide a `policyRevisionId` that matches the current version, the update succeeds and a new revision ID is returned.
+ If you provide a `policyRevisionId` that does not match the current version (because another principal updated the policy in the meantime), the call fails with a conflict error. Retrieve the current policy, merge your changes, and retry.
+ If you omit the `policyRevisionId`, the policy is unconditionally replaced regardless of any concurrent modifications.

Use the revision ID when multiple administrators or automation systems may update the same knowledge base policy concurrently, to prevent accidental overwrites.

## Set up the consumer account
<a name="kb-managed-cross-account-identity-policy"></a>

In the consuming account, attach an identity-based policy to the principal that needs to access the shared knowledge base. The policy must allow the corresponding Amazon Bedrock actions on the knowledge base ARN in the owner account.

**Example identity-based policy**

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
            "Resource": "arn:aws:bedrock:{{REGION}}:{{OWNER_ACCOUNT_ID}}:knowledge-base/{{KB_ID}}"
        }
    ]
}
```