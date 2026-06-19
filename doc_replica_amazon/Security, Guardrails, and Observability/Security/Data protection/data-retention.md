

# Data retention
<a name="data-retention"></a>

## Overview
<a name="data-retention-overview"></a>

Amazon Bedrock gives you explicit control over whether your prompts and outputs are retained from your inference requests. You can configure data retention at the account or project level, and the setting is enforced consistently across the Messages, Chat Completions, and Responses APIs.

Your data retention configuration is yours to manage. If your account or project is configured for zero data retention (`data_retention_mode: none`) and you invoke a model that requires retention, Amazon Bedrock will block the request and return an error — you always control your retention policy.

**Important**  
There is no data retention change to models released before Claude Fable 5. AWS is committed to making sure that you are in full control over when and with whom your data is retained and shared.

## Data retention modes
<a name="data-retention-modes"></a>

Data retention is controlled by a **mode** rather than a simple on/off toggle:


| **Mode** | **Behavior** | 
| --- | --- | 
| default | Default means the data retention policy of the model applies. There is no change to previous model retention behavior; if ZDR applied previously, then ZDR still applies. Actual retention depends on the model — consult the model's terms for specifics. AWS may retain the data for safety and abuse-prevention purposes. The model provider does not receive it. On the Responses API, `store` defaults to `true` and may be set to either value.Setting `store=false` does not guarantee zero data retention. Some models may still retain data for safety review even when `store=false` — in this case, data is retained but is not retrievable by the customer via `GET /v1/responses/{id}`. If you require guaranteed zero retention, set `data_retention_mode` to `none`. | 
| provider\_data\_share | This mode allows Amazon Bedrock to retain and share your inference data with model providers per their requirements. It is required for access to certain models. See [Amazon Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html) and [AWS Service Terms](https://aws.amazon.com/service-terms/). | 
| none | Zero data retention. No request or response data is written to durable storage by AWS or shared with the model provider. On the Responses API, store defaults to false and store=true is rejected. Background mode is not available. Chat Completions and Messages requests are never retained. | 
| inherit | No opinion at this scope — defer to a broader scope. This is the default for new accounts and projects. | 

**Important**  
Configuring your account or project to `provider_data_share` does *not* mean all models will start sharing data with their providers. Your configured mode sets what you allow — each model independently declares which modes it supports via `allowed_modes`. Most models currently do not require or request `provider_data_share`. The interaction works as follows:  
If a model's `allowed_modes` includes `none`, we won't persist anything.
If a model's `allowed_modes` includes `default` but not `none`, AWS retains the data — the model provider does not receive it.
If a model's only allowed mode is `provider_data_share`, data will be shared with the provider — but only if your effective mode permits it. If your effective mode is `none` or `default`, the model will appear as unavailable.

## How your retention mode is determined
<a name="data-retention-resolution"></a>

Data retention is configured at two scopes, with the model's own default as the fallback:
+ **Project** (most specific) — set via `POST /v1/organization/projects/{project_id}`
+ **Account** — set via `PUT /v1/data_retention`
+ **Model default** (least specific, read-only) — the model's built-in default

The effective mode for any request is determined by taking the first scope whose value is not `inherit`:

```
effective mode = first non-inherit value of (project → account → model default)
```

For example, if your project is set to `inherit` and your account is set to `none`, the effective mode is `none` for all models invoked from that project.

## Configuring data retention
<a name="data-retention-configuration"></a>

### Set account-wide data retention
<a name="data-retention-set-account"></a>

```
curl -X PUT https://bedrock-mantle.us-east-1.api.aws/v1/data_retention \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mode": "provider_data_share" }'
```

**Response:**

```
{
  "mode": "provider_data_share",
  "updated_at": 1733529600
}
```

**Bedrock Control Plane:**

```
curl -X PUT https://bedrock.us-east-1.amazonaws.com/data-retention \
  -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
  -H "Content-Type: application/json" \
  -d '{ "mode": "provider_data_share" }'
```

**Response:**

```
{
  "mode": "provider_data_share",
  "updated_at": "2026-06-07T20:19:44.723Z"
}
```

### Set project-level data retention
<a name="data-retention-set-project"></a>

```
curl https://bedrock-mantle.us-east-1.api.aws/v1/organization/projects/proj_abc123 \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "data_retention": { "mode": "provider_data_share" } }'
```

### Check your current configuration
<a name="data-retention-check-config"></a>

```
# Account level
curl https://bedrock-mantle.us-east-1.api.aws/v1/data_retention \
  -H "x-api-key: $BEDROCK_API_KEY"

# Project level
curl https://bedrock-mantle.us-east-1.api.aws/v1/organization/projects/proj_abc123 \
  -H "x-api-key: $BEDROCK_API_KEY"
```

**Bedrock Control Plane:**

```
# Account level
curl https://bedrock.us-east-1.amazonaws.com/data-retention \
  -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK"
```

### Check a model's effective mode and allowed modes
<a name="data-retention-check-model"></a>

```
curl https://bedrock-mantle.us-east-1.api.aws/v1/models/anthropic.claude-fable-5 \
  -H "x-api-key: $BEDROCK_API_KEY"
```

**Response:**

```
{
  "id": "anthropic.claude-fable-5",
  "created": 1733443200,
  "owned_by": "system",
  "status": "available",
  "data_retention": {
    "mode": "provider_data_share",
    "source": "account",
    "allowed_modes": ["provider_data_share"]
  }
}
```

## Model availability and data retention
<a name="data-retention-model-availability"></a>

Each model specifies which retention modes it permits via `allowed_modes`. If your effective mode is not in a model's `allowed_modes`, the model will appear as `status: "unavailable"` in the models list and requests to it will be blocked.

**Example:** Claude Fable 5 and Claude Mythos 5 require provider data sharing (`allowed_modes: ["provider_data_share"]`). Customers must explicitly set their data retention mode to `provider_data_share` before they can invoke these models. If your effective mode is `none` or `default`, these models will be unavailable.

By setting `provider_data_share`, you are explicitly acknowledging instructing us to retain and share data with model providers per their requirements. It is required for access to certain models. See the [Abuse Detection page](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html) and [AWS Service Terms](https://aws.amazon.com/service-terms/).

**Note**  
At launch, there is no console UI for configuring data retention. Customers must use the API (see "Configuring data retention" above) or the Bedrock SDK.

**Response when a model is unavailable due to retention policy:**

```
{
  "id": "anthropic.claude-fable-5",
  "created": 1733443200,
  "owned_by": "system",
  "status": "unavailable",
  "status_reason": "This model is not available under data retention mode 'default'.",
  "data_retention": {
    "mode": "default",
    "source": "account",
    "allowed_modes": ["provider_data_share"]
  }
}
```

### How to opt in
<a name="data-retention-opt-in"></a>

To enable Claude Fable 5 and Claude Mythos 5 for your account:

```
curl https://bedrock-mantle.us-east-1.api.aws/v1/data_retention \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mode": "provider_data_share" }'
```

Or at the project level (if you want to limit provider data sharing to a specific project):

```
curl https://bedrock-mantle.us-east-1.api.aws/v1/organization/projects/proj_abc123 \
  -H "x-api-key: $BEDROCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "data_retention": { "mode": "provider_data_share" } }'
```

**Mixed-model projects**  
Setting a project to `provider_data_share` does not mean all model traffic in that project is shared with the model provider. Each model's `allowed_modes` determines what actually happens to your data:  
A model whose `allowed_modes` is `["provider_data_share"]` (e.g., Claude Fable 5) — data is retained and shared with the provider.
A model whose `allowed_modes` is `["default", "provider_data_share"]` (e.g., Claude Opus 4.8) — data is retained by AWS only. The model accepts `provider_data_share` as a valid mode but does not require data to leave AWS's boundary.
When a Claude Fable 5 request is declined by a safety classifier and the fallback credit is redeemed on Claude Opus 4.8, the fallback invocation follows Opus 4.8's data-handling rules, not Fable 5's. The Opus 4.8 response is not retained or shared with Anthropic.

## Zero data retention (ZDR) access
<a name="data-retention-zdr"></a>

Some models require data retention for safety and abuse-prevention purposes. If your organization requires zero data retention for compliance reasons and you need access to these models, contact your AWS account manager to discuss eligibility. ZDR access is evaluated on a per-account, per-model basis in coordination with the model provider.

Accounts approved for ZDR on a specific model will see `"none"` included in that model's `allowed_modes`.

## Enforcing retention policy with IAM
<a name="data-retention-iam"></a>

You can enforce a data retention policy across your organization using IAM policies or Service Control Policies (SCPs). The write actions publish a `bedrock-mantle:DataRetentionMode` condition key that lets you restrict which modes can be set.

**Example SCP — require zero data retention across the organization:**

```
{
    "Effect": "Deny",
    "Action": [
        "bedrock-mantle:PutAccountDataRetention",
        "bedrock-mantle:CreateProject",
        "bedrock-mantle:UpdateProject"
    ],
    "Condition": {
        "StringNotEquals": {
            "bedrock-mantle:DataRetentionMode": "none"
        }
    }
}
```

**Bedrock Control Plane:**

```
{
    "Effect": "Deny",
    "Action": [
        "bedrock:PutAccountDataRetention"
    ],
    "Condition": {
        "StringNotEquals": {
            "bedrock:DataRetentionMode": "none"
        }
    }
}
```

This prevents anyone in the organization from setting data retention to anything other than `none`, ensuring no inference data is ever retained.

## What data is retained and for how long
<a name="data-retention-what-is-retained"></a>

For models requiring `provider_data_share` (currently Claude Mythos 5 and Claude Fable 5): user prompts and completions are shared with Anthropic and retained for up to 30 days for trust and safety purposes.

For models under `default` mode: data may be retained for abuse detection purposes — see [Amazon Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html) for required retention details. For retention beyond abuse detection (e.g., Responses API with `store=true`), consult the model's documentation and terms.

If cross-region inference is enabled for these models, retained inputs and outputs are stored in destination regions (i.e., the region where your inference request is processed).

See [Anthropic Terms of Service](https://aws.amazon.com/legal/bedrock/third-party-models/) for model-specific data handling details.

## IAM actions reference
<a name="data-retention-iam-reference"></a>


| **Route** | **IAM action** | 
| --- | --- | 
| GET /v1/models | bedrock-mantle:ListModels | 
| GET /v1/models/{model} | bedrock-mantle:GetModel | 
| GET /v1/data\_retention | bedrock-mantle:GetAccountDataRetention | 
| PUT /v1/data\_retention | bedrock-mantle:PutAccountDataRetention | 
| GET /v1/organization/projects/{project\_id} | bedrock-mantle:GetProject | 
| POST /v1/organization/projects/{project\_id} | bedrock-mantle:UpdateProject | 


| **Route** | **IAM action** | 
| --- | --- | 
| GET /data-retention | bedrock:GetAccountDataRetention | 
| PUT /data-retention | bedrock:PutAccountDataRetention | 