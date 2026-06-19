

# Quotas for Amazon Bedrock
<a name="quotas"></a>

Your AWS account has default quotas, formerly referred to as limits, for Amazon Bedrock. To view service quotas for Amazon Bedrock, do one of the following:
+ Follow the steps at [Viewing service quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html) and select **Amazon Bedrock** as the service.
+ Refer to the [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) in the AWS General Reference.

Model inference in Amazon Bedrock is controlled by quotas on token usage. Some models use tokens at a higher rate. For more information about these rates and how to optimize your token usage, see [How tokens are counted in Amazon Bedrock](quotas-token-burndown.md).

Amazon Bedrock offers two inference endpoints – `bedrock-runtime` and `bedrock-mantle` – each with its own per-model quota allocations. Traffic to the two endpoints is tracked against separate quotas, even when calling the same underlying model. For details, see [Quotas for the bedrock-runtime endpoint](quotas-runtime.md) and [Quotas for the bedrock-mantle endpoint](quotas-mantle.md).

To maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock, the default quotas assigned to an account might be updated depending on regional factors, payment history, fraudulent usage, and/or approval of a [quota increase request](quotas-increase.md).

**Topics**
+ [How tokens are counted in Amazon Bedrock](quotas-token-burndown.md)
+ [Monitor your token usage by counting tokens before running inference](count-tokens.md)
+ [Quotas for the bedrock-runtime endpoint](quotas-runtime.md)
+ [Quotas for the bedrock-mantle endpoint](quotas-mantle.md)
+ [Request an increase for Amazon Bedrock quotas](quotas-increase.md)