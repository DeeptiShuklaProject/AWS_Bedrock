

# Permissions for using cross-Region inference with Amazon Bedrock Guardrails
<a name="guardrail-profiles-permissions"></a>

Using [cross-Region inference](guardrails-cross-region.md) with Amazon Bedrock Guardrails requires adding specific permissions to your IAM role, including allowing access to guardrail profiles in other Regions.

## Permissions to create and manage guardrails for cross-Region inference
<a name="guardrail-profiles-permissions-create-modify"></a>

Use the following IAM policy to [create](guardrails-components.md), [view](guardrails-view.md), [modify](guardrails-edit.md), and [delete](guardrails-delete.md) a guardrail that uses a specific guardrail profile. You only need these permissions for calling an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp).

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CreateAndManageGuardrails",
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateGuardrail",
                "bedrock:UpdateGuardrail",
                "bedrock:DeleteGuardrail",
                "bedrock:GetGuardrail",
                "bedrock:ListGuardrails"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/*",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail-profile/{{guardrail-profile-id}}"
            ]
        }
    ]
}
```

------

## Permissions for invoking guardrails with cross-Region inference
<a name="guardrail-profiles-permissions-invoking"></a>

When invoking a guardrail with cross-Region inference, you need an IAM policy that specifies the destination Regions defined in your guardrail profile. 

```
{
    "Effect": "Allow",
    "Action": ["bedrock:ApplyGuardrail"],
    "Resource": [
        "arn:aws:bedrock:us-east-1:{{account-id}}:guardrail/{{guardrail-id}}",
        "arn:aws:bedrock:us-east-1:{{account-id}}:guardrail-profile/us.guardrail.v1:0",
        "arn:aws:bedrock:us-east-2:{{account-id}}:guardrail-profile/us.guardrail.v1:0",
        "arn:aws:bedrock:us-west-2:{{account-id}}:guardrail-profile/us.guardrail.v1:0"
    ]
}
```

This example policy specifies the following resources:
+ The guardrail that you're invoking in your source Region (in this case, `us-east-1`).
+ The destination Regions defined in the guardrail profile you're using (in this case, `us.guardrail.v1:0`). For information on which destination Regions to specify in your policy, see the [Available guardrail profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-cross-region-support.html#available-guardrail-profiles).