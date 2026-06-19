

# Fallback credit for refused requests (beta)
<a name="claude-messages-fallback-credit"></a>

When Claude Fable 5 refuses a request, customers who retry the same conversation on a different model (such as Claude Opus 4.8) normally re-pay cache-write rates for the conversation prefix that was already cached on Fable 5. Fallback credit eliminates this double-charge by issuing a one-time credit token on refusal that can be redeemed on the retry.

This feature requires the beta flag `fallback-credit-2026-06-09` in the `anthropic_beta` array on both the original request and the retry.

## Supported models
<a name="claude-messages-fallback-credit-supported-models"></a>


| **Role** | **Model** | 
| --- | --- | 
| Source (issues credit on refusal) | Claude Fable 5 | 
| Target (redeems credit on retry) | Must be a valid fallback target of the source model | 

## How it works
<a name="claude-messages-fallback-credit-how-it-works"></a>

**Step 1: Receive a fallback credit token on refusal**

When a request to Claude Fable 5 returns `stop_reason: "refusal"` and the beta flag is present, the `stop_details` object includes a `fallback_credit_token`:

```
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "model": "anthropic.claude-fable-5",
  "content": [],
  "stop_reason": "refusal",
  "stop_details": {
    "type": "refusal",
    "category": "cyber",
    "explanation": "This request triggered restrictions on violative cyber content and was blocked under Anthropic's Usage Policy.",
    "fallback_credit_token": "<opaque token>"
  },
  "usage": {
    "input_tokens": 106,
    "output_tokens": 1
  }
}
```

The `fallback_credit_token` is an opaque string. It is `null` when mint conditions are not met (no cache was read on the original request, model is not credit-eligible, or beta flag is absent). Server-side minting failures produce `null`, never an error.

In streaming mode, the token is delivered in the final `message_delta` event's `stop_details`.

**Step 2: Redeem the token on a retry request**

Pass the token as a top-level parameter on the retry to the fallback model:

```
{
  "anthropic_version": "bedrock-2023-05-31",
  "anthropic_beta": ["fallback-credit-2026-06-09"],
  "model": "anthropic.claude-opus-4-8",
  "max_tokens": 4096,
  "system": "...",
  "messages": [...],
  "tools": [...],
  "fallback_credit_token": "<token from the refusal's stop_details>"
}
```

## Redemption rules
<a name="claude-messages-fallback-credit-redemption-rules"></a>


| **Rule** | **Requirement** | 
| --- | --- | 
| Time window | Token must be redeemed within 5 minutes of being issued. | 
| Platform binding | A token minted on bedrock-mantle can only be redeemed on bedrock-mantle. | 
| Body match | The system, messages, and tools fields must match the refused request exactly. Send them as-is; do not strip thinking blocks. | 
| Retry shapes | The retry body must either (a) match the refused request exactly (the fallback model regenerates the response), or (b) match it with one appended assistant message containing the refused response's partial output (the fallback model continues from where Fable 5 was interrupted). | 
| Target model | Must be a valid fallback target of the refused model. | 

## Error handling
<a name="claude-messages-fallback-credit-error-handling"></a>

With the beta flag present, any redemption validation failure returns a `400 invalid_request_error`. The recovery path in every case is to retry without `fallback_credit_token`. Failure conditions include:
+ Malformed or unrecognizable token
+ Token older than 5 minutes
+ Request body does not match the original refused request
+ Target model is not a valid fallback target
+ Token has already been redeemed

Without the beta flag, `fallback_credit_token` is rejected as an unknown field (400). The parameter is also rejected on `count_tokens` requests.

## Billing impact
<a name="claude-messages-fallback-credit-billing-impact"></a>

When a fallback credit token is successfully redeemed, the retry request receives a credit for cache-write tokens that overlap with the refused request's cached prefix. The customer pays only for net-new tokens on the retry, not for re-caching the conversation prefix.

## Example workflow
<a name="claude-messages-fallback-credit-example-workflow"></a>

1. Send a request to Claude Fable 5 with `anthropic_beta: ["fallback-credit-2026-06-09"]`.

1. Receive a refusal with a `fallback_credit_token` in `stop_details`.

1. Immediately retry to Claude Opus 4.8 with the same `system`, `messages`, and `tools`, plus the `fallback_credit_token`.

1. The retry is billed at reduced rates for the overlapping cached prefix.

If the token is `null`, expired, or invalid — retry normally without it. The credit is a cost optimization, not a functional requirement for the retry to succeed.