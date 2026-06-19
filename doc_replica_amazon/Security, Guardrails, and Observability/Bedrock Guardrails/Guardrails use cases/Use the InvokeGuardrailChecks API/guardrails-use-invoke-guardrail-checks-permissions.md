

# Set up permissions
<a name="guardrails-use-invoke-guardrail-checks-permissions"></a>

To call `InvokeGuardrailChecks`, the caller's IAM identity needs permission to invoke the operation on Amazon Bedrock. Create or use an IAM role or user with the following policy attached.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeGuardrailChecks"
      ],
      "Resource": "*"
    }
  ]
}
```

`InvokeGuardrailChecks` is resourceless — there is no guardrail ARN to scope the policy against. Use IAM identity-based policies, AWS Organizations service control policies, and standard AWS condition keys (such as `aws:SourceIp` or `aws:PrincipalTag`) to restrict who can call the API.