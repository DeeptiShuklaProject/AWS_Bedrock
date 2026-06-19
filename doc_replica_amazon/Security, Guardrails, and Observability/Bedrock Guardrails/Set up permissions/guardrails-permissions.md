

# Set up permissions to use Amazon Bedrock Guardrails
<a name="guardrails-permissions"></a>

To set up a role with permissions for guardrails, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

If you're using guardrails with an agent, attach the permissions to a service role with permissions to create and manage agents. You can set up this role in the console or create a custom role by following the steps at [Create a service role for Amazon Bedrock Agents](agents-permissions.md).

## Permissions to create and manage guardrails for the policy role
<a name="guardrails-permissions-use"></a>

Append the following statement to the `Statement` field in the policy for your role to use guardrails.

**Note**  
If you pass tags when creating a guardrail (for example, by using the `tags` parameter in the `CreateGuardrail` API), you must also include the `bedrock:TagResource` permission in your policy.

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
                "bedrock:CreateGuardrailVersion",
                "bedrock:DeleteGuardrail", 
                "bedrock:GetGuardrail", 
                "bedrock:ListGuardrails", 
                "bedrock:UpdateGuardrail"
            ],
            "Resource": "*"
        }
    ]   
}
```

------

## Permissions for invoking guardrails to filter content
<a name="guardrails-permissions-invoke"></a>

Append the following statement to the `Statement` field in the policy for the role to allow for model inference and to invoke guardrails. These `InvokeModel` permissions are only required when using guardrails with Amazon Bedrock foundation models. If you are using guardrails independently with the `ApplyGuardrail` API (for example, to filter content from third-party models), you only need the `bedrock:ApplyGuardrail` permission.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModel",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ]
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
            ]
        }
    ]
}
```

------