

# Configure content filters for Amazon Bedrock Guardrails
<a name="guardrails-content-filters-overview"></a>

With Amazon Bedrock Guardrails, you can configure content filters to block model prompts and responses in natural language for text and images containing harmful content. For example, an e-commerce site can design its online assistant to avoid using inappropriate language and or images.

## Filter classification and blocking levels
<a name="guardrails-filters-classification"></a>

Filtering is done based on confidence classification of user inputs and FM responses across each of the six categories. All user inputs and FM responses are classified across four strength levels - `NONE`, `LOW`, `MEDIUM`, and `HIGH`. For example, if a statement is classified as Hate with `HIGH` confidence, the likelihood of that statement representing hateful content is high. A single statement can be classified across multiple categories with varying confidence levels. For example, a single statement can be classified as **Hate** with `HIGH` confidence, **Insults** with `LOW` confidence, **Sexual** with `NONE`, and **Violence** with `MEDIUM` confidence.

## Filter strength
<a name="guardrails-filters-strength"></a>

You can configure the strength of the filters for each of the content filter categories. The filter strength determines the sensitivity of filtering harmful content. As the filter strength is increased, the likelihood of filtering harmful content increases and the probability of seeing harmful content in your application decreases.

You have four levels of filter strength
+ **None** — There are no content filters applied. All user inputs and FM-generated outputs are allowed.
+ **Low** — The strength of the filter is low. Content classified as harmful with `HIGH` confidence will be filtered out. Content classified as harmful with `NONE`, `LOW`, or `MEDIUM` confidence will be allowed.
+ **Medium** — Content classified as harmful with `HIGH` and `MEDIUM` confidence will be filtered out. Content classified as harmful with `NONE` or `LOW` confidence will be allowed.
+ **High** — This represents the strictest filtering configuration. Content classified as harmful with `HIGH`, `MEDIUM` and `LOW` confidence will be filtered out. Content deemed harmless will be allowed.


| Filter strength | Blocked content confidence | Allowed content confidence | 
| --- | --- | --- | 
| None | No filtering | None, Low, Medium, High | 
| Low | High | None, Low, Medium | 
| Medium | High, Medium | None, Low | 
| High | High, Medium, Low | None | 