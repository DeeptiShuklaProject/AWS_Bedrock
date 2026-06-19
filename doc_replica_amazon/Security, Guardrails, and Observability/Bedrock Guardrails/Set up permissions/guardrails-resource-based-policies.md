

# Using resource-based policies for guardrails
<a name="guardrails-resource-based-policies"></a>

Amazon Bedrock Guardrails supports resource-based policies for guardrails and guardrails inference profiles. Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.

You can attach a resource-based policy (RBP) to Guardrails resources (guardrail or guardrail inference profile). In this policy, you specify permissions for Identity and Access Management (IAM) [principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html#intro-structure-principal) that can perform specific actions on these resources. For example, the policy attached to a guardrail will contain permissions to apply the guardrail or read the guardrail configuration.

Resource-based policies are recommended for use with account-level enforced guardrails, and are required for use of organization-level enforced guardrails, because for organizational enforced guardrails the member accounts are required to apply a guardrail that exists in the organization administrator account. To use a guardrail in a different account, the caller identity must have permission to call the `bedrock:ApplyGuardrail` API on the guardrail, and the guardrail must have a resource based policy attached which gives that caller permission. For more information, see [Cross-account policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic-cross-account.html) and [Identity-based policies and resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html).

RBPs are attached from the guardrails detail page. If the guardrail has Cross-Region Inference (CRIS) enabled, the caller must also have `ApplyGuardrail` permission on all destination-region guardrail-owner-account profile objects associated with that profile, and RBPs must be attached to the profiles in turn. For more information, see [Permissions for using cross-Region inference with Amazon Bedrock Guardrails](guardrail-profiles-permissions.md). Profiles detail pages can be reached from the "System-defined guardrail profiles" section on the guardrails dashboard, and RBPs attached from there.

For enforced guardrails (either organization or account-level), all callers of Bedrock Invoke or Converse APIs who do not have permissions to call that guardrail will start seeing their calls fail with an `AccessDenied` exception. For this reason it is strongly recommended to check that you are able to call [ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ApplyGuardrail.html) API on the guardrail from the identities it will be used by, in the accounts it will be enforced on, before creating an organizational or account enforced guardrail configuration.

The allowed policy language for guardrail and guardrail-profile resource-based policies is currently restricted and only supports a limited set of policy statements.

## Supported policy statement patterns
<a name="supported-policy-statement-patterns"></a>

### Share guardrail within your own account
<a name="share-guardrail-within-account"></a>

`account-id` must be the account containing the guardrail.

**Policy for a guardrail:**  


------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::{{111122223333}}:root"
        },
        "Action": [
            "bedrock:ApplyGuardrail",
            "bedrock:GetGuardrail"
        ],
	    "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail/guardrail-id"
    }]
}
```

------

**Policy for a guardrail-profile:**  


------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::{{111122223333}}:root"
        },
        "Action": [
            "bedrock:ApplyGuardrail"
        ],
        "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail-profile/profile-id"
    }]
}
```

------

### Share guardrail with your organization
<a name="share-guardrail-with-organization"></a>

`account-id` must match the account that you are attaching the RBP from, and that account must be in `org-id`.

**Policy for a guardrail:**  
 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
            "bedrock:GetGuardrail",
            "bedrock:ApplyGuardrail"
        ],
        "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail/guardrail-id",
        "Condition": {
            "StringEquals": { 
                "aws:PrincipalOrgID": "org-id"
            }
        }
    }]
}
```

------

**Policy for a guardrail-profile:**  
 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
            "bedrock:ApplyGuardrail"
        ],
        "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail-profile/profile-id",
        "Condition": {
            "StringEquals": { 
                "aws:PrincipalOrgID": "org-id"
            }
        }
    }]
}
```

------

### Share guardrail with specific OUs
<a name="share-guardrail-with-specific-ous"></a>

`account-id` must match the account that you are attaching the RBP from, and that account must be in `org-id`.

**Policy for a guardrail:**  
 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
            "bedrock:ApplyGuardrail",
            "bedrock:GetGuardrail"
        ],
        "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail/guardrail-id",
        "Condition": {
            "StringEquals": {
                "aws:PrincipalOrgID": "org-id"
            },
            "ForAnyValue:StringLike": {
                "aws:PrincipalOrgPaths": [
                    "org-id/*/org-unit-id/*"
                ]
            }
        }
    }]
}
```

------

**Policy for a guardrail-profile:**  
 

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
            "bedrock:ApplyGuardrail"
        ],
        "Resource": "arn:aws:bedrock:us-east-1:{{111122223333}}:guardrail-profile/profile-id",
        "Condition": {
            "StringEquals": {
                "aws:PrincipalOrgID": "org-id"
            },
            "ForAnyValue:StringLike": {
                "aws:PrincipalOrgPaths": [
                    "org-id/*/org-unit-id/*"
                ]
            }
        }
    }]
}
```

------

## Unsupported features
<a name="unsupported-features"></a>

Guardrails does not support sharing outside of your organization.

Guardrails does not support RBPs with conditions other than the ones listed above on `PrincipalOrgId` or `PrincipalOrgPaths`.

Guardrails does not support use of a `*` Principal without an organization or organizational unit condition.

Guardrails only supports the `bedrock:ApplyGuardrail` and `bedrock:GetGuardrail` actions in RBPs. For guardrail-profile resources, only `ApplyGuardrail` is supported.