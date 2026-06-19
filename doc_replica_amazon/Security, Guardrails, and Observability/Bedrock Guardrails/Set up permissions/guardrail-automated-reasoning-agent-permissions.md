

# Permissions for Automated Reasoning policies with agents
<a name="guardrail-automated-reasoning-agent-permissions"></a>

When you create an agent in Amazon Bedrock, the service role for the agent automatically includes policies for invoking guardrails (`bedrock:ApplyGuardrail`) and foundation models. To attach a guardrail that includes an Automated Reasoning policy to your agent, manually add permissions to the agent's service role.

Update the `AmazonBedrockAgentBedrockApplyGuardrailPolicy` policy on your agent's service role to include the `bedrock:GetGuardrail` action and access to guardrail profiles. Then, add a separate statement that grants the `bedrock:InvokeAutomatedReasoningPolicy` action for your Automated Reasoning policy resource.

The following example shows the complete statements list:

```
    "Statement": [
        {
            "Sid": "AmazonBedrockAgentBedrockApplyGuardrailPolicyProd",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail",
                "bedrock:GetGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{region}}:{{account-id}}:guardrail/{{guardrail-id}}",
                "arn:aws:bedrock:*:{{account-id}}:guardrail-profile/*"
            ]
        },
        {
            "Sid": "InvokeAutomatedReasoningPolicyProd",
            "Effect": "Allow",
            "Action": "bedrock:InvokeAutomatedReasoningPolicy",
            "Resource": [
                "arn:aws:bedrock:{{region}}:{{account-id}}:automated-reasoning-policy/{{policy-id}}:{{policy-version}}"
            ]
        }
    ]
```

**Note**  
The existing `AmazonBedrockAgentBedrockFoundationModelPolicy` on your agent's service role does not need to be modified. Only the `AmazonBedrockAgentBedrockApplyGuardrailPolicy` requires the changes described above.