

# Use product ID condition keys to control access
<a name="model-access-product-ids"></a>

The `aws-marketplace:ProductId` condition key can be used to control the ability to subscribe to Amazon Bedrock serverless models that have a product ID in AWS Marketplace. To learn how to use the product ID condition key, see the examples in [Grant IAM permissions to request access to Amazon Bedrock foundation models with a product ID](model-access.md#model-access-permissions).

**Note**  
Models from the following providers aren't sold through AWS Marketplace and don't have product keys, so you can't scope the `aws-marketplace` actions to them:  
Amazon
DeepSeek
Mistral AI
Meta
Qwen
OpenAI
You can, however, prevent the usage of these models by denying Amazon Bedrock actions and specifying these model IDs in the `Resource` field. For an example, see [Prevent an identity from using a model after access has already been granted](model-access.md#model-access-prevent-usage).

Please refer to [models at a glance](model-cards.md) to see product IDs for individual models. The following table shows product IDs for models not available on that page:


| Model | Product ID | 
| --- | --- | 
| AI21 Labs Jurassic-2 Mid | 1d288c71-65f9-489a-a3e2-9c7f4f6e6a85 | 
| AI21 Labs Jurassic-2 Ultra | cc0bdd50-279a-40d8-829c-4009b77a1fcc | 
| AI21 Jamba-Instruct | prod-dr2vpvd4k73aq | 
| Anthropic Claude | c468b48a-84df-43a4-8c46-8870630108a7 | 
| Anthropic Claude Instant | b0eb9475-3a2c-43d1-94d3-56756fd43737 | 
| Anthropic Claude 3 Sonnet | prod-6dw3qvchef7zy | 
| Anthropic Claude 3.5 Sonnet | prod-m5ilt4siql27k | 
| Anthropic Claude 3.5 Sonnet v2 | prod-cx7ovbu5wex7g | 
| Anthropic Claude 3.7 Sonnet | prod-4dlfvry4v5hbi | 
| Anthropic Claude 3 Opus | prod-fm3feywmwerog | 
| Anthropic Claude Opus 4 | prod-azycxvnd5mhqi | 
| Cohere Command | a61c46fe-1747-41aa-9af0-2e0ae8a9ce05 | 
| Cohere Command Light | 216b69fd-07d5-4c7b-866b-936456d68311 | 
| Stable Image Core 1.0 | prod-eacdrmv7zfc5e | 
| Stable Image Ultra 1.0 | prod-7boen2z2wnxrg | 
| Stability 3.5 Large 1.0 | prodview-ajc3gw4mjy7my | 

You can use the following template to attach an IAM policy that controls model access permissions to a role:

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "AllowBedrockModelAccess",
            "Effect": "Allow",
            "Action": [
                "aws-marketplace:Subscribe",
                "aws-marketplace:Unsubscribe",
                "aws-marketplace:ViewSubscriptions"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws-marketplace:ProductId": [
                        "{{product-id-1}}",
                        "{{product-id-2}}"
                    ]
                }
            }
        },
        {
            "Sid": "AllowBedrockInvokeModel",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        }
    ]
}
```

For more examples of how to manage model access with IAM policies, see [Identity-based policy examples for Amazon Bedrock](security_iam_id-based-policy-examples.md).