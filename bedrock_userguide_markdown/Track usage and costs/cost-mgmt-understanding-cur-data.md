

# Understanding your Amazon Bedrock Cost and Usage Report data
<a name="cost-mgmt-understanding-cur-data"></a>

AWS Data Exports Cost and Usage Reports (CUR 2.0) is the AWS recommended way to receive your detailed cost and usage data. CUR 2.0 provides line-item detail for every Amazon Bedrock inference request. Each request generates separate line items for each token type, with distinct usage types and unit prices. This page explains how to read Amazon Bedrock entries in CUR and reconcile them to your actual spend. For more information about AWS CUR 2.0, see [AWS Data Exports documentation](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html).

## Understanding Amazon Bedrock pricing in CUR
<a name="cost-mgmt-cur-pricing"></a>

Amazon Bedrock pricing in CUR is determined by three factors: the token type, the service tier, and whether the request was routed through cross-region inference. Understanding each of these is essential for accurate cost reconciliation.

### Token types
<a name="cost-mgmt-cur-token-types"></a>

Amazon Bedrock charges are broken down by four token types. Each has a different unit price.


| Token type | CUR usage type pattern | Description | 
| --- | --- | --- | 
| Input tokens | \*-input-tokens or \*-mantle-input-tokens-\* | Tokens sent in the request prompt | 
| Output tokens | \*-output-tokens or \*-mantle-output-tokens-\* | Tokens generated in the response | 
| Cache read tokens | \*-cache-read-input-token-count | Tokens read from prompt cache (significantly cheaper than input) | 
| Cache write tokens | \*-cache-write-input-token-count | Tokens written to prompt cache (more expensive than input) | 

**Important**  
All four token types must be accounted for when reconciling usage to spend. If you only sum input and output tokens, your totals will not match your bill. This is the most common source of reconciliation gaps, particularly for workloads that use prompt caching heavily.

### Service tiers
<a name="cost-mgmt-cur-service-tiers"></a>

Amazon Bedrock supports different service tiers that affect pricing and availability. The service tier for a request is reflected in the CUR usage type. When reconciling costs, ensure you apply the correct unit price for the service tier associated with each line item.

For more information on service tiers and how they affect inference pricing, see [Service tiers for optimizing performance and cost](service-tiers-inference.md).

## CUR usage type examples
<a name="cost-mgmt-cur-usage-type-examples"></a>

The `line_item_usage_type` field identifies the model, token type, service tier, and whether the request used cross-region inference. The format varies by endpoint:
+ `{region}-{model}-{token-type}` for `bedrock-runtime` standard tier requests
+ `{region}-{model}-{token-type}-{tier}` for `bedrock-runtime` priority or flex tier requests
+ `{region}-{model}-mantle-{token-type}-standard` for `bedrock-mantle` requests
+ `{region}-{model}-{token-type}-cross-region-global` for cross-region requests


| Usage type | Model | Service Tier | Token type | Routing | 
| --- | --- | --- | --- | --- | 
| USE1-openai.gpt-oss-120b-mantle-input-tokens-standard | OpenAI gpt-oss-120b | Standard | Input | In-region | 
| USE1-gpt-oss-120b-output-tokens-priority | OpenAI gpt-oss-120b | Priority | Output | In-region | 
| USE1-Nova2.0Lite-input-tokens-flex | Amazon Nova 2 Lite | Flex | Input | In-region | 
| USE1-Claude4.6Sonnet-input-tokens | Claude Sonnet 4.6 | Standard | Input | In-region | 
| USE1-Claude4.6Sonnet-cache-read-input-token-count | Claude Sonnet 4.6 | Standard | Cache read | In-region | 
| USE1-Claude4.6Sonnet-output-tokens-cross-region-global | Claude Sonnet 4.6 | Standard | Output | Cross-region | 

## Cost allocation tags in CUR
<a name="cost-mgmt-cur-cost-allocation-tags"></a>

Cost allocation tags from [IAM principals](cost-mgmt-iam-principal-tracking.md), [Projects](cost-mgmt-projects.md), and [application inference profiles](cost-mgmt-application-inference-profiles.md) appear as columns in CUR with the prefix `resourceTags/{key}` and `iamPrincipal/{key}`. For example, a tag with key `Team` appears as `resourceTags/Team`.


| Attribution method | How tags appear in CUR | 
| --- | --- | 
| IAM principal tags | Tags from the IAM user or role making the request | 
| Session tags | Tags passed during role assumption or federation | 
| Project tags | Tags assigned to a Amazon Bedrock Project | 
| Application inference profile tags | Tags assigned to an application inference profile | 

Tags must be activated as cost allocation tags in the AWS Billing console before they appear in CUR. For more information, see [Activating cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html).

## Key things to know when reading your CUR data
<a name="cost-mgmt-cur-key-things"></a>

To get the most out of your CUR data and avoid confusion when analyzing costs, keep the following in mind.
+ **Account for all token types.** Amazon Bedrock charges separately for input, output, cache read, and cache write tokens. Each has a different unit price. If you only look at input and output tokens, your analysis will undercount costs, especially for workloads that use prompt caching heavily.
+ **Apply the correct rate for each routing type.** In-region and cross-region inference have different unit prices. If your workloads use both, make sure you use the matching rate for each when analyzing costs.
+ **Activate tags before expecting them in CUR.** Cost allocation tags must be activated in the AWS Billing console before they appear in CUR or Cost Explorer. After activation, allow up to 24 hours for tags to begin populating.
+ **Use CUR 2.0 for IAM principal attribution.** IAM principal identity and tag data requires CUR 2.0 (AWS Data Exports). If you are using the legacy CUR format, IAM principal fields will not be available. Per-token cost breakdowns are available in both CUR formats. For detailed setup instructions, see [Using IAM principal for cost allocation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/iam-principal-cost-allocation.html).
+ **CUR does not contain per-request line items.** Both classic CUR and CUR 2.0 aggregate Amazon Bedrock cost by usage type, operation, and pricing/resource over an hour or a day; neither carries a per-`requestId` identifier. To attribute cost to an individual request or prompt, use your [model invocation logs](model-invocation-logging.md) rather than CUR. To reconcile dollars to your invoice while keeping the per-prompt detail in logs, join logs to CUR at the model and usage-type grain.