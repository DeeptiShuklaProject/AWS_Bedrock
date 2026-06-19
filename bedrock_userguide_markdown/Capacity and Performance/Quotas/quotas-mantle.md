

# Quotas for the bedrock-mantle endpoint
<a name="quotas-mantle"></a>

The `bedrock-mantle.{{region}}.api.aws` endpoint serves the OpenAI Responses API, the OpenAI Chat Completions API, and the Anthropic Messages API. Inference traffic to this endpoint is governed by a separate set of quotas from the `bedrock-runtime` endpoint.

You can view `bedrock-mantle` quotas in the [Service Quotas console](https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html) by selecting **Amazon Bedrock** as the service and searching for *Bedrock Mantle*. To request an increase to any of these quotas, see [Requesting a quota increase](#quotas-mantle-increase).

## Quota types
<a name="quotas-mantle-types"></a>

Inference on the `bedrock-mantle` endpoint is governed by two per-model quotas:


**bedrock-mantle per-model quotas**  

| Quota | Scope | Description | 
| --- | --- | --- | 
| Bedrock Mantle input tokens per minute for {{${model}}} | Per model, per Region | The maximum number of input tokens per minute that your account can submit to the model on the bedrock-mantle endpoint. Shared across all APIs served by the endpoint for that model. | 
| Bedrock Mantle output tokens per minute for {{${model}}} | Per model, per Region | The maximum number of output tokens per minute that the model can generate for your account on the bedrock-mantle endpoint. Shared across all APIs served by the endpoint for that model. | 

**Note**  
Cached input tokens read through prompt caching do not count against the input-tokens-per-minute quota.

**Note**  
The `bedrock-mantle` endpoint does not enforce requests-per-minute (RPM) quotas. Throttling is governed solely by the input and output token quotas described in this section.

## How requests are evaluated against quotas
<a name="quotas-mantle-evaluation"></a>

When you submit an inference request to the `bedrock-mantle` endpoint, AWS evaluates it against your quotas in the following order:

1. **Input tokens per minute** – The number of input tokens in the request, plus the value of `max_tokens` (or the model-specific maximum if `max_tokens` is not set), is checked against the input-tokens-per-minute quota for the requested model. If admitting the request would exceed the quota, the request is throttled with an HTTP 429 response.

1. **Output tokens per minute** – As the model streams or generates output, output tokens are counted against the output-tokens-per-minute quota for that model. If the quota is reached during generation, generation stops and the response is returned with a finish reason indicating the cutoff.

After the response completes, any unused portion of the initial input-token reservation (the difference between `max_tokens` and the actual output) is replenished to your quota.

The endpoint may apply additional internal rate limiting that is not exposed in Service Quotas. Use retry logic with exponential backoff to handle transient throttling.

The `bedrock-runtime` endpoint's TPM quotas count input and output tokens together against a single per-model quota, while the `bedrock-mantle` endpoint applies separate input-tokens-per-minute and output-tokens-per-minute quotas. If you run workloads on both endpoints, plan capacity for each endpoint independently. For details on the runtime endpoint's quotas, see [Quotas for the bedrock-runtime endpoint](quotas-runtime.md).

## Default quota values
<a name="quotas-mantle-defaults"></a>

The following table lists default quotas for models on the `bedrock-mantle` endpoint. New AWS accounts might receive reduced quotas, and quotas can vary by Region.


**Default bedrock-mantle quotas by model**  

| Model | Default input TPM | Default output TPM | 
| --- | --- | --- | 
| Anthropic Claude Opus 4.7 | 20,000,000 | 4,000,000 | 

Additional models will be listed in this table as they launch on the endpoint.

### Models without published TPM quotas
<a name="quotas-mantle-no-quota-models"></a>

The `bedrock-mantle` endpoint enforces published TPM quotas only for the models listed in the table above. Other models served on this endpoint don't have per-account TPM quotas exposed in Service Quotas today – their throughput is governed by internal service capacity. AWS might introduce per-account quotas for additional models as usage scales. Use retry logic with exponential backoff to handle transient throttling. If you need a published quota for a specific model, contact AWS Support.

## Supported Regions
<a name="quotas-mantle-supported-regions"></a>

`bedrock-mantle` quotas are visible in Service Quotas in the same AWS Regions where the `bedrock-mantle` endpoint is available. For the full list of Regions and endpoint URLs, see [Supported Regions and Endpoints](bedrock-mantle.md#bedrock-mantle-supported).

## Requesting a quota increase
<a name="quotas-mantle-increase"></a>

The `bedrock-mantle` quotas are visible in Service Quotas, but quota increase requests are not currently processed through the Service Quotas console. To request an increase, submit a request through the [AWS Support limit increase form](https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase) and select **Amazon Bedrock** as the service. In your request, specify:
+ The endpoint (`bedrock-mantle`).
+ The Region.
+ The model.
+ The quota name (input TPM or output TPM) and the value you are requesting.

You can request increases to input-tokens-per-minute and output-tokens-per-minute for the same model in a single support case. Approval depends on whether your existing usage justifies the increase, so include recent usage information from CloudWatch or the Service Quotas console with your request.

## Differences from bedrock-runtime quotas
<a name="quotas-mantle-differences"></a>

The `bedrock-mantle` quotas are independent from the `bedrock-runtime` quotas. Traffic to `bedrock-runtime.{{region}}.amazonaws.com` and traffic to `bedrock-mantle.{{region}}.api.aws` consume separate quota allocations, even when calling the same underlying model.

Custom inference profile quotas, batch inference quotas, and Provisioned Throughput allocations apply only to the `bedrock-runtime` endpoint and are not exposed on the `bedrock-mantle` endpoint.