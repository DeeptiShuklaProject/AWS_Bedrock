

# Permissions for Automated Reasoning policies with ApplyGuardrail
<a name="guardrail-automated-reasoning-permissions"></a>

When using Automated Reasoning policies with the `ApplyGuardrail` API, you need an IAM policy that allows you to invoke the Automated Reasoning policy.

```
{
    "Sid": "AutomatedReasoningChecks",
    "Effect": "Allow",
    "Action": [
        "bedrock:InvokeAutomatedReasoningPolicy"
    ],
    "Resource": [
        "arn:aws:bedrock:{{region}}:{{account-id}}:automated-reasoning-policy/{{policy-id}}:{{policy-version}}"
    ]
}
```

This policy allows you to invoke the specified Automated Reasoning policy in your account.