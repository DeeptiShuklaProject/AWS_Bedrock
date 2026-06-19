

# Concepts: Messages, content block types, and checks
<a name="guardrails-use-invoke-guardrail-checks-concepts"></a>

The following concepts describe the structure of requests to the `InvokeGuardrailChecks` API.

## Messages
<a name="guardrails-use-invoke-guardrail-checks-messages"></a>

A message is the basic unit of content you submit for evaluation. Each message has two fields: a role that identifies who produced the content, and a content array that holds the actual text as one or more typed content blocks.

```
{
  "role": "user",
  "content": [{ "text": "Hello world" }]
}
```

This mirrors the role-plus-content-blocks structure used elsewhere in Amazon Bedrock, so the conversation you already build for a model can be passed to `InvokeGuardrailChecks` with little or no reshaping. The `messages` field of a request is an array, so you can submit a single message or a sequence that represents a multi-turn exchange (for example, a system instruction followed by a user turn). Messages are evaluated in the order you provide them, and their positions matter: some results refer back to a message by its zero-based `messageIndex`, and to a block within that message by its `contentIndex` (see the sensitive information results).

The role labels the origin of the content. The following roles are supported:
+ `system` – Instructions that configure the model's behavior.
+ `user` – Input from the end user.
+ `assistant` – Output produced by the model.

## Content block types
<a name="guardrails-use-invoke-guardrail-checks-content"></a>

The `content` field is an array of typed blocks rather than a plain string. A typed block is a small object whose key names its type. This design lets the message format carry other kinds of content (such as images or documents) in the future without changing the overall message shape. Currently, the only supported block type is `text`, whose value is a bare string:

```
{ "text": "Hello world" }
```

A message can contain at most ten content blocks. A content block can contain at most one `text` block. Because `text` is the only supported type today, this effectively means one block of text per content block. To evaluate several distinct pieces of text within one role, send them as separate content blocks in the `content` array. To evaluate several distinct pieces of text across multiple roles, send them as separate messages in the `messages` array.

## Checks
<a name="guardrails-use-invoke-guardrail-checks-checks"></a>

The term *checks* is interchangeable with the term *safeguards* offered by Amazon Bedrock Guardrails. The `checks` object is a configuration object with one optional field per check type, and you include only the checks you want to run. You don't set a separate enable/disable flag: a check runs if and only if its field is present, and omitted checks produce no result and no usage. You must set at least one check field.

```
"checks": {
  "contentFilter":         { ... },
  "promptAttack":          { ... },
  "sensitiveInformation":  { ... }
}
```

Because the configuration is inline per request, you can vary your safety posture from call to call without managing a stored guardrail resource. Different steps in an agent loop can request different combinations of checks against the same or different messages.

Each check carries its own configuration shape. The field name selects the check; the object inside it lists what that check looks for:
+ `contentFilter` – Takes a `categories` list (HATE, INSULTS, SEXUAL, VIOLENCE, MISCONDUCT).
+ `promptAttack` – Takes a `categories` list (JAILBREAK, PROMPT\_INJECTION, PROMPT\_LEAKAGE).
+ `sensitiveInformation` – Takes an `entities` list (31 supported PII entities).

**Request and response are symmetric** – The keys you set under `checks` are the same keys that come back under `results` and `usage`. If you request `contentFilter` and `sensitiveInformation`, only those two appear in the response; `promptAttack` is absent because it was never run. This makes it easy to map a finding back to the check that produced it.

**Detect-only across every check** – No check blocks, masks, or rewrites content. Each returns scores (a `severityScore` for content filter and prompt attack, a `confidenceScore` plus location offsets for sensitive information), and you decide how your application acts on them based on specific requirements.