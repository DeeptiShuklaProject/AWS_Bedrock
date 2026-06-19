

# Model availability & compatibility
<a name="models"></a>

Amazon Bedrock supports a wide catalog of foundation models from leading providers. This chapter explains where each model is available, which APIs and endpoints support it, how to access it, and how to manage models throughout their lifecycle. For an overview of all available models with their capabilities and pricing, see [Models at a glance](model-cards.md).

**In this chapter**
+ [API compatibility](models-api-compatibility.md) – Which APIs (InvokeModel, Converse, Chat Completions, Responses, Messages) each model supports.
+ [Endpoint availability](models-endpoint-availability.md) – Which endpoints (`bedrock-runtime`, `bedrock-mantle`) each model is hosted on.
+ [Regional availability](models-region-compatibility.md) – AWS Regions and cross-Region inference profiles each model is available in.
+ [Get list of models](models-get-info.md) – Programmatically list and discover available models on each endpoint.
+ [Model lifecycle](model-lifecycle.md) – Model versioning, deprecation timelines, and migration guidance.
+ [Request access to models](model-access.md) – Request and manage access to models in your account.
+ [Use product ID condition keys to control access](model-access-product-ids.md) – Use IAM product ID condition keys to control which models users can invoke.

**Choosing a model**

When picking a model, consider:
+ **Capabilities** – modalities (text, image, embeddings), context window, and tool use support.
+ **Endpoint and API** – whether the model is on `bedrock-runtime`, `bedrock-mantle`, or both, and which APIs it supports. See [Endpoints supported by Amazon Bedrock](endpoints.md).
+ **Region** – whether the model is available in the AWS Regions you operate in, or via a cross-Region inference profile.
+ **Cost and throughput** – on-demand pricing vs. [Increase model invocation capacity with Provisioned Throughput in Amazon Bedrock](prov-throughput.md).