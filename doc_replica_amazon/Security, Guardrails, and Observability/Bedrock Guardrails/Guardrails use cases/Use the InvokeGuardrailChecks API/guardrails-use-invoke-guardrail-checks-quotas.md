

# Quotas
<a name="guardrails-use-invoke-guardrail-checks-quotas"></a>

The following quotas are enforced for `InvokeGuardrailChecks`. Quotas marked as adjustable can be raised through Service Quotas; others are hard limits.


**InvokeGuardrailChecks quotas**  

| Name | Default value | Description | 
| --- | --- | --- | 
| Requests per minute (RPM) | 1,500 | Maximum number of InvokeGuardrailChecks calls per account, per Region, per minute. | 

**Note**  
**Burst traffic** – Even when your overall traffic is below the per-minute limits, a sudden burst of requests within a short window might be throttled with a `ThrottlingException`. Smooth traffic over time and use exponential backoff with jitter on retries.