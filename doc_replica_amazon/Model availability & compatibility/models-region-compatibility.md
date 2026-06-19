

# Regional availability
<a name="models-region-compatibility"></a>

Amazon Bedrock gives you three options so you can match the routing behavior of your inference calls to the scale, compliance, and cost requirements of your workload.

**Process to enabling Bedrock models in GovCloud**  
Accessing Bedrock foundation models in AWS GovCloud (US) requires initiating the access request through the standard AWS account linked to your GovCloud account. You must first agree to the model's End User License Agreement (EULA) in a standard region (`us-east-1` or `us-west-2`), then enable the model in your GovCloud account. You can do this in two ways:  
**Console:** Sign in to your linked standard AWS account, open the Amazon Bedrock Chat/Text playground, choose the model, and run a prompt to establish the EULA.
**AWS CLI:** Run `aws bedrock list-foundation-models` to get the model ID, then `aws bedrock list-foundation-model-agreement-offers --model-id <model-id>` to get the offer token, and finally `aws bedrock create-foundation-model-agreement --model-id <model-id> --offer-token <offerToken>`.
After completing either method, go to your GovCloud account and enable the model via the Model Access page. It may take a few minutes for entitlements to propagate. For the full walkthrough, see [Process to enabling Bedrock models in GovCloud](https://repost.aws/articles/ARUT8Sy76NTUmRN7kuiU0UXQ).
+ **In-Region:** Your requests never leave the AWS Region you specify. Use this when regulations require strict single-Region data processing.
+ **Geographic (Geo):** Bedrock intelligently routes within a defined geography (US, EU, Japan, or Australia) to maximize throughput while keeping data within regional boundaries. Use this when you have data residency requirements tied to a geography rather than a single Region.
+ **Global:** Bedrock routes across all commercial Regions worldwide for the highest throughput and lowest cost. Use this when you have no data residency constraints and want the best performance and price.

## Inference options at a glance
<a name="inference-options-glance"></a>


|  | **In-Region** | **Geographic (Geo) Cross-Region** | **Global Cross-Region** | 
| --- | --- | --- | --- | 
| How it works | Request is processed entirely within the single AWS Region you specify | Bedrock automatically routes to the optimal Region within a defined geography (US, EU, APAC, JP, AU) | Bedrock routes to any commercial Region worldwide for optimal performance | 
| Data residency | Strictly within one Region | Within geographic boundaries (e.g., all EU Regions); prompts and outputs may move within the geography but not outside it | No geographic restrictions; data may be processed in any commercial Region | 
| Throughput | Limited to single-Region capacity; subject to per-Region service quotas | Higher than In-Region; absorbs regional traffic spikes within the geography | Highest throughput; uses global capacity | 
| Pricing | Standard on-demand pricing for that Region | Priced at source Region rates; no surcharge for cross-Region routing | Priced at source Region rates; no surcharge for cross-Region routing | 
| modelId format | Direct model ID: anthropic.claude-3-5-sonnet-20241022-v2:0 | Geography prefix \+ model ID: us.anthropic.claude-3-5-sonnet-20241022-v2:0 | Global prefix \+ model ID: global.anthropic.claude-3-5-sonnet-20241022-v2:0 | 
| Best for | Strict single-Region compliance; Provisioned Throughput workloads | Data residency regulations scoped to a geography (e.g., GDPR in EU, data sovereignty requirements) | Maximum throughput and cost efficiency with no data residency constraints | 

Now, let us look at Regional availability across all the models supported by Amazon Bedrock.

## AI21 Labs
<a name="model-regions-ai21-labs"></a>


**[Jamba 1.5 Large](model-card-ai21-labs-jamba-1-5-large.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Jamba 1.5 Mini](model-card-ai21-labs-jamba-1-5-mini.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Amazon
<a name="model-regions-amazon"></a>


**[Nova 2 Sonic](model-card-amazon-nova-2-sonic.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova 2 Lite](model-card-amazon-nova-2-lite.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Amazon Nova Multimodal Embeddings](model-card-amazon-amazon-nova-multimodal-embeddings.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Titan Image Generator G1 v2](model-card-amazon-titan-image-generator-g1-v2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Titan Text Embeddings V2](model-card-amazon-titan-text-embeddings-v2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Titan Multimodal Embeddings G1](model-card-amazon-titan-multimodal-embeddings-g1.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Titan Embeddings G1 - Text](model-card-amazon-titan-embeddings-g1---text.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Titan Embeddings G1 - Text v2](model-card-amazon-titan-text-embeddings-v2-2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Reel](model-card-amazon-nova-reel.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | Legacy (EOL: 2026-09-30) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Rerank**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Sonic](model-card-amazon-nova-sonic.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Pro](model-card-amazon-nova-pro.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Reel](model-card-amazon-nova-reel.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Lite](model-card-amazon-nova-lite.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Canvas](model-card-amazon-nova-canvas.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | Legacy (EOL: 2026-09-30) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Micro](model-card-amazon-nova-micro.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nova Premier](model-card-amazon-nova-premier.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Anthropic
<a name="model-regions-anthropic"></a>


**[Claude Mythos 5](model-card-anthropic-claude-mythos-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Claude Fable 5](model-card-anthropic-claude-fable-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Mythos Preview](model-card-anthropic-claude-mythos-preview.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Claude Sonnet 4](model-card-anthropic-claude-sonnet-4.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-10-14) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Claude Opus 4**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Claude Sonnet 4.6](model-card-anthropic-claude-sonnet-4-6.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Opus 4.8](model-card-anthropic-claude-opus-4-8.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Opus 4.7](model-card-anthropic-claude-opus-4-7.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Opus 4.6](model-card-anthropic-claude-opus-4-6.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Opus 4.5](model-card-anthropic-claude-opus-4-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Haiku 4.5](model-card-anthropic-claude-haiku-4-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Sonnet 4.5](model-card-anthropic-claude-sonnet-4-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-6 (New Zealand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Claude Opus 4.1](model-card-anthropic-claude-opus-4-1.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-05-31) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-05-31) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-05-31) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Claude 3 Haiku](model-card-anthropic-claude-3-haiku.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | Legacy (EOL: 2026-09-10) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Claude 3 Sonnet**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Claude 3.7 Sonnet**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Claude 3.5 Sonnet V2:0**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Claude 3.5 Haiku](model-card-anthropic-claude-3-5-haiku.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-06-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-06-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | Legacy (EOL: 2026-06-19) | Legacy (EOL: 2026-06-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Claude 3.5 Sonnet**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Cohere
<a name="model-regions-cohere"></a>


**[Embed v4](model-card-cohere-embed-v4.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 


**[Embed English](model-card-cohere-embed-english.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Embed Multilingual](model-card-cohere-embed-multilingual.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Rerank 3.5](model-card-cohere-rerank-3-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Command R](model-card-cohere-command-r.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | Legacy (EOL: 2026-08-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | Legacy (EOL: 2026-08-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Command R\+](model-card-cohere-command-r-plus.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | Legacy (EOL: 2026-08-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | Legacy (EOL: 2026-08-19) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## DeepSeek
<a name="model-regions-deepseek"></a>


**[DeepSeek V3.2](model-card-deepseek-deepseek-v3-2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[DeepSeek-V3.1](model-card-deepseek-deepseek-v3-1.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[DeepSeek-R1](model-card-deepseek-deepseek-r1.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Google
<a name="model-regions-google"></a>


**[Gemma 4 31B](model-card-google-gemma-4-31b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Gemma 4 26B-A4B](model-card-google-gemma-4-26b-a4b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Gemma 4 E2B](model-card-google-gemma-4-e2b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Gemma 3 27B PT](model-card-google-gemma-3-27b-pt.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Gemma 3 12B IT](model-card-google-gemma-3-12b-it.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Gemma 3 4B IT](model-card-google-gemma-3-4b-it.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Luma
<a name="model-regions-luma"></a>


**Ray V2:0**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Meta
<a name="model-regions-meta"></a>


**[Llama 4 Maverick 17B Instruct](model-card-meta-llama-4-maverick-17b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 4 Scout 17B Instruct](model-card-meta-llama-4-scout-17b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3 70B Instruct](model-card-meta-llama-3-70b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3 8B Instruct](model-card-meta-llama-3-8b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.3 70B Instruct](model-card-meta-llama-3-3-70b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.2 90B Instruct](model-card-meta-llama-3-2-90b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.2 11B Instruct](model-card-meta-llama-3-2-11b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.2 3B Instruct](model-card-meta-llama-3-2-3b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.2 1B Instruct](model-card-meta-llama-3-2-1b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.1 405B Instruct](model-card-meta-llama-3-1-405b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | Legacy (EOL: 2026-07-07) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.1 70B Instruct](model-card-meta-llama-3-1-70b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Llama 3.1 8B Instruct](model-card-meta-llama-3-1-8b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## MiniMax
<a name="model-regions-minimax"></a>


**[MiniMax M2](model-card-minimax-minimax-m2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[MiniMax M2.1](model-card-minimax-minimax-m2-1.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[MiniMax M2.5](model-card-minimax-minimax-m2-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[MiniMax M2.5](model-card-minimax-minimax-m2-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Mistral AI
<a name="model-regions-mistral-ai"></a>


**[Magistral Small 2509](model-card-mistral-ai-magistral-small-2509.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Pixtral Large](model-card-mistral-ai-pixtral-large.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Mistral Large 2407**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Mistral Small](model-card-mistral-ai-mistral-small.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Mistral Large](model-card-mistral-ai-mistral-large.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Voxtral Small 24B 2507](model-card-mistral-ai-voxtral-small-24b-2507.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Mixtral 8x7B Instruct](model-card-mistral-ai-mixtral-8x7b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Mistral 7B Instruct](model-card-mistral-ai-mistral-7b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Voxtral Mini 3B 2507](model-card-mistral-ai-voxtral-mini-3b-2507.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Mistral Large 3](model-card-mistral-ai-mistral-large-3.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Ministral 14B 3.0](model-card-mistral-ai-ministral-14b-3-0.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Ministral 3 8B](model-card-mistral-ai-ministral-3-8b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Ministral 3B](model-card-mistral-ai-ministral-3b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Devstral 2 123B](model-card-mistral-ai-devstral-2-123b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Moonshot AI
<a name="model-regions-moonshot-ai"></a>


**[Kimi K2.5](model-card-moonshot-ai-kimi-k2-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## NVIDIA
<a name="model-regions-nvidia"></a>


**[NVIDIA Nemotron Nano 12B v2 VL BF16](model-card-nvidia-nvidia-nemotron-nano-12b-v2-vl-bf16.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[NVIDIA Nemotron Nano 9B v2](model-card-nvidia-nvidia-nemotron-nano-9b-v2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Nemotron Nano 3 30B](model-card-nvidia-nemotron-nano-3-30b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[NVIDIA Nemotron 3 Super 120B](model-card-nvidia-nemotron-super-3-120b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## OpenAI
<a name="model-regions-openai"></a>


**[GPT-5.5](model-card-openai-gpt-55.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GPT-5.4](model-card-openai-gpt-54.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GPT OSS Safeguard 120B](model-card-openai-gpt-oss-safeguard-120b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[gpt-oss-120b](model-card-openai-gpt-oss-120b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GPT OSS Safeguard 20B](model-card-openai-gpt-oss-safeguard-20b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[gpt-oss-20b](model-card-openai-gpt-oss-20b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-west-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-gov-east-1 (GovCloud) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Qwen
<a name="model-regions-qwen"></a>


**[Qwen3 Coder Next](model-card-qwen-qwen3-coder-next.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3 Coder 480B A35B Instruct](model-card-qwen-qwen3-coder-480b-a35b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3 235B A22B 2507](model-card-qwen-qwen3-235b-a22b-2507.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3 VL 235B A22B](model-card-qwen-qwen3-vl-235b-a22b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3 Next 80B A3B](model-card-qwen-qwen3-next-80b-a3b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3 32B](model-card-qwen-qwen3-32b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Qwen3-Coder-30B-A3B-Instruct](model-card-qwen-qwen3-coder-30b-a3b-instruct.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Stability AI
<a name="model-regions-stability-ai"></a>


**Sd3.5 Large**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Stable Image Core V1:1**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**Stable Image Ultra V1:1**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Control Structure](model-card-stability-ai-stable-image-control-structure.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Conservative Upscale](model-card-stability-ai-stable-image-conservative-upscale.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Fast Upscale](model-card-stability-ai-stable-image-fast-upscale.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Control Sketch](model-card-stability-ai-stable-image-control-sketch.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Search and Recolor](model-card-stability-ai-stable-image-search-and-recolor.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Creative Upscale](model-card-stability-ai-stable-image-creative-upscale.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Erase Object](model-card-stability-ai-stable-image-erase-object.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Inpaint](model-card-stability-ai-stable-image-inpaint.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Outpaint](model-card-stability-ai-stable-image-outpaint.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Search and Replace](model-card-stability-ai-stable-image-search-and-replace.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Style Transfer](model-card-stability-ai-stable-image-style-transfer.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Style Guide](model-card-stability-ai-stable-image-style-guide.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Stable Image Remove Background](model-card-stability-ai-stable-image-remove-background.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## TwelveLabs
<a name="model-regions-twelvelabs"></a>


**[Marengo Embed 3.0](model-card-twelvelabs-marengo-embed-3-0.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Marengo Embed v2.7](model-card-twelvelabs-marengo-embed-v2-7.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Pegasus v1.2](model-card-twelvelabs-pegasus-v1-2.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-central-1 (Canada) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ca-west-1 (Calgary) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-central-2 (Zurich) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-south-2 (Spain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| eu-west-3 (Paris) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-east-2 (Taipei) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-2 (Seoul) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-northeast-3 (Osaka) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-south-2 (Hyderabad) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-1 (Singapore) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-4 (Melbourne) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-5 (Malaysia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| ap-southeast-7 (Thailand) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| il-central-1 (Tel Aviv) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-central-1 (UAE) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| me-south-1 (Bahrain) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| af-south-1 (Cape Town) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 
| mx-central-1 (Mexico) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | 

## Writer
<a name="model-regions-writer"></a>


**[Palmyra Vision 7B](model-card-writer-palmyra-vision-7b.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Palmyra X5](model-card-writer-palmyra-x5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[Palmyra X4](model-card-writer-palmyra-x4.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-1 (N. California) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## xAI
<a name="model-regions-xai"></a>


**[Grok 4.3](model-card-xai-grok-4-3.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 

## Z.AI
<a name="model-regions-z.ai"></a>


**[GLM 4.7 Flash](model-card-zai-glm-4-7-flash.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-central-1 (Frankfurt) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-south-1 (Milan) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-1 (Ireland) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GLM 4.7](model-card-zai-glm-4-7.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GLM 5](model-card-zai-glm-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 


**[GLM 5](model-card-zai-glm-5.md)**  

| Region | In-Region | Geo | Global | 
| --- | --- | --- | --- | 
| us-east-1 (N. Virginia) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-east-2 (Ohio) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| us-west-2 (Oregon) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-north-1 (Stockholm) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| eu-west-2 (London) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-northeast-1 (Tokyo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-south-1 (Mumbai) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-2 (Sydney) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| ap-southeast-3 (Jakarta) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 
| sa-east-1 (São Paulo) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-yes.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | ![](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/icon-no.png) | 