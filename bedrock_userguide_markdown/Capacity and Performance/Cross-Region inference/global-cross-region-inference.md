

# Global cross-Region inference
<a name="global-cross-region-inference"></a>

Global cross-Region inference extends cross-Region inference beyond geographic boundaries, enabling the routing of inference requests to supported commercial AWS Regions worldwide, optimizing available resources and enabling higher model throughput.

## Benefits of global cross-Region inference
<a name="global-cris-benefits"></a>

Global cross-Region inference for Anthropic's Claude Sonnet 4.5 delivers multiple advantages over traditional geographic cross-Region inference profiles:
+ **Enhanced throughput during peak demand** – Global cross-Region inference provides improved resilience during periods of peak demand by automatically routing requests to AWS Regions with available capacity. This dynamic routing happens seamlessly without additional configuration or intervention from developers. Unlike traditional approaches that might require complex client-side load balancing between AWS Regions, global cross-Region inference handles traffic spikes automatically. This is particularly important for business-critical applications where downtime or degraded performance can have significant financial or reputational impacts.
+ **Cost-efficiency** – Global cross-Region inference for Anthropic's Claude Sonnet 4.5 offers approximately 10% savings on both input and output token pricing compared to geographic cross-Region inference. The price is calculated based on the AWS Region from which the request is made (source AWS Region). This means organizations can benefit from improved resilience with even lower costs. This pricing model makes global cross-Region inference a cost-effective solution for organizations looking to optimize their generative AI deployments. By improving resource use and enabling higher throughput without additional costs, it helps organizations maximize the value of their investment in Amazon Bedrock.
+ **Streamlined monitoring** – When using global cross-Region inference, CloudWatch and CloudTrail continue to record log entries in your source AWS Region, simplifying observability and management. Even though your requests are processed across different AWS Regions worldwide, you maintain a centralized view of your application's performance and usage patterns through your familiar AWS monitoring tools.
+ **On-demand quota flexibility** – With global cross-Region inference, your workloads are no longer limited by individual Regional capacity. Instead of being restricted to the capacity available in a specific AWS Region, your requests can be dynamically routed across the AWS global infrastructure. This provides access to a much larger pool of resources, making it less complicated to handle high-volume workloads and sudden traffic spikes.

## Global cross-Region inference considerations
<a name="global-cris-considerations"></a>

Note the following information about Global cross-Region inference:
+ Global Cross-Region inference profiles provide higher throughput than an inference profile tied to a particular geography. An inference profile tied to a particular geography offers higher throughput than single-region inference.
+ To see the default quotas for cross-Region throughput when using Global inference profiles, refer to the **Global Cross-region model inference requests per minute for ${Model}** and **Global Cross-region model inference tokens per minute for ${Model}** values in [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) in the *AWS General Reference*.

  You can request, view, and manage quotas for the Global Cross-Region Inference Profile from the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home/services/bedrock/quotas) or by using AWS CLI commands in your **source region**.

## IAM policy requirements for global cross-Region inference
<a name="global-cris-iam-setup"></a>

To enable global cross-Region inference for your users, you must apply a three-part IAM policy to the role. The following is an example IAM policy to provide granular control. You can replace `<REQUESTING REGION>` in the example policy with the AWS Region you are operating in.

```
{
    "Version": "2012-10-17"		 	 	 ,
    "Statement": [
        {
            "Sid": "GrantGlobalCrisInferenceProfileRegionAccess",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:<REQUESTING REGION>:<ACCOUNT>:inference-profile/global.<MODEL NAME>"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "<REQUESTING REGION>"
                }
            }
        },
        {
            "Sid": "GrantGlobalCrisInferenceProfileInRegionModelAccess",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:<REQUESTING REGION>::foundation-model/<MODEL NAME>"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "<REQUESTING REGION>",
                    "bedrock:InferenceProfileArn": "arn:aws:bedrock:<REQUESTING REGION>:<ACCOUNT>:inference-profile/global.<MODEL NAME>"
                }
            }
        },
        {
            "Sid": "GrantGlobalCrisInferenceProfileGlobalModelAccess",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:::foundation-model/<MODEL NAME>"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "unspecified",
                    "bedrock:InferenceProfileArn": "arn:aws:bedrock:<REQUESTING REGION>:<ACCOUNT>:inference-profile/global.<MODEL NAME>"
                }
            }
        }
    ]
}
```

The first part of the policy grants access to the Regional inference profile in your requesting AWS Region. The second part provides access to the Regional FM resource. The third part grants access to the global FM resource, which enables the cross-Region routing capability.

When implementing these policies, make sure all three resource Amazon Resource Names (ARNs) are included in your IAM statements:
+ The Regional inference profile ARN follows the pattern `arn:aws:bedrock:REGION:ACCOUNT:inference-profile/global.MODEL-NAME`. This is used to give access to the global inference profile in the source AWS Region.
+ The Regional FM uses `arn:aws:bedrock:REGION::foundation-model/MODEL-NAME`. This is used to give access to the FM in the source AWS Region.
+ The global FM requires `arn:aws:bedrock:::foundation-model/MODEL-NAME`. This is used to give access to the FM in different global AWS Regions.

The global FM ARN has no AWS Region or account specified, which is intentional and required for the cross-Region functionality.

### Disable global cross-Region inference
<a name="global-cris-iam-disable"></a>

You can choose from two primary approaches to implement deny policies to global CRIS for specific IAM roles, each with different use cases and implications:
+ **Remove an IAM policy** – The first method involves removing one or more of the three required IAM policies from user permissions. Because global CRIS requires all three policies to function, removing a policy will result in denied access.
+ **Implement a deny policy** – The second approach is to implement an explicit deny policy that specifically targets global CRIS inference profiles. This method provides clear documentation of your security intent and makes sure that even if someone accidentally adds the required allow policies later, the explicit deny will take precedence. The deny policy should use a `StringEquals` condition matching the pattern `"aws:RequestedRegion": "unspecified"`. This pattern specifically targets inference profiles with the `global` prefix.

When implementing deny policies, it's crucial to understand that global CRIS changes how the `aws:RequestedRegion` field behaves. Traditional AWS Region-based deny policies that use `StringEquals` conditions with specific AWS Region names such as `"aws:RequestedRegion": "us-west-2"` will not work as expected with global CRIS because the service sets this field to `global` rather than the actual destination AWS Region. However, as mentioned earlier, `"aws:RequestedRegion": "unspecified"` will result in the deny effect.

## Service Control Policy requirements for Global cross-Region inference
<a name="global-cris-scp-setup"></a>

For Global cross-Region inference, if your organization's security policy uses SCPs to block unused Regions, you must update your region-specific SCP conditions to allow access with `"aws:RequestedRegion": "unspecified"`. This condition is specific to Amazon Bedrock Global cross-Region inference and ensures that requests can be routed to all supported AWS commercial Regions.

The following example SCP blocks all AWS API calls outside of approved Regions while allowing Amazon Bedrock Global cross-Region inference calls that use `"unspecified"` as the Region for global routing:

```
{
    "Version": "2012-10-17"		 	 	 ,
    "Statement": [
        {
            "Sid": "DenyAllOutsideApprovedRegions",
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "aws:RequestedRegion": [
                        "us-east-1",
                        "us-east-2",
                        "us-west-2",
                        "unspecified"
                    ]
                }
            }
        }
    ]
}
```

### Disable global cross-Region inference
<a name="global-cris-disable"></a>

Organizations with data residency or compliance requirements should assess whether Global cross-Region inference fits their compliance framework, since requests may be processed in other supported AWS commercial Regions. To explicitly disable Global cross-Region inference, implement the following SCP policy:

```
{
    "Effect": "Deny",
    "Action": "bedrock:*",
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "aws:RequestedRegion": "unspecified"
        },
        "ArnLike": {
            "bedrock:InferenceProfileArn": "arn:aws:bedrock:*:*:inference-profile/global.*"
        }
    }
}
```

This SCP explicitly denies Global cross-Region inference because the `"aws:RequestedRegion"` is `"unspecified"` and the `"ArnLike"` condition targets inference profiles with the `global` prefix in the ARN.

### AWS Control Tower implementation
<a name="control-tower-scp"></a>

Manually editing SCPs managed by AWS Control Tower is strongly discouraged as it can cause drift. Instead, use the mechanisms provided by Control Tower to manage these exceptions. The core principles involve either extending existing region-deny controls or enabling regions and then applying a custom, conditional blocking policy.

For detailed, step-by-step guidance on implementing cross-Region inference with Control Tower, see the blog post [ Enable Amazon Bedrock cross-Region inference in multi-account environments](https://aws.amazon.com/blogs/machine-learning/enable-amazon-bedrock-cross-region-inference-in-multi-account-environments/). This covers extending existing Region deny SCPs, enabling denied regions with custom SCPs, and using Customizations for AWS Control Tower (CfCT) to deploy custom SCPs as infrastructure as code.

## Request limit increases for global cross-Region inference
<a name="global-cris-quotas"></a>

When using global CRIS inference profiles, you can use global CRIS from over 20 supported source AWS Regions. Because this will be a global limit, requests to view, manage, or increase quotas for global cross-Region inference profiles must be made through the Service Quotas console or AWS Command Line Interface (AWS CLI) in the requested source AWS Region.

Complete the following steps to request a limit increase:

1. Sign in to the Service Quotas console in your AWS account.

1. In the navigation pane, choose **AWS services**.

1. From the list of services, find and choose **Amazon Bedrock**.

1. In the list of quotas for Amazon Bedrock, use the search filter to find the specific global CRIS quotas. For example:
   + Global cross-Region model inference tokens per minute for Anthropic Claude Sonnet 4.5 V1

1. Select the quota you want to increase.

1. Choose **Request increase at account level**.

1. Enter your desired new quota value.

1. Choose **Request** to submit your request.

When calculating your required quota increase, remember to take into account for the burndown rate, defined as the rate at which input and output tokens are converted into token quota usage for the throttling system. The following models have a **5x burn down rate for output tokens (1 output token consumes 5 tokens from your quotas)**:
+ Anthropic Claude Opus 4
+ Anthropic Claude Sonnet 4.5
+ Anthropic Claude Sonnet 4
+ Anthropic Claude 3.7 Sonnet

For all other models, the burndown rate is **1:1** (1 output token consumes 1 token from your quota). For input tokens, the token to quota ratio is 1:1. The calculation for the total number of tokens per request is as follows:

`Input token count + Cache write input tokens + (Output token count x Burndown rate)`

## Use Global cross-Region inference
<a name="global-cris-usage"></a>

To use global cross-Region inference with Anthropic's Claude Sonnet 4.5, developers must complete the following key steps:
+ **Use the global inference profile ID** – When making API calls to Amazon Bedrock, specify the global Anthropic's Claude Sonnet 4.5 inference profile ID (`global.anthropic.claude-sonnet-4-5-20250929-v1:0`) instead of a AWS Region-specific model ID.
+ **Configure IAM permissions** – Grant appropriate IAM permissions to access the inference profile and FMs in potential destination AWS Regions.

Global cross-Region inference is supported for:
+ On-demand model inference
+ Batch inference
+ Agents
+ Model evaluation
+ Prompt management
+ Prompt flows

**Note**  
Global inference profile is supported for On-demand model inference, Batch inference, Agents, Model evaluation, Prompt management, and Prompt flows.

## Implement global cross-Region inference
<a name="global-cris-implementation"></a>

Implementing global cross-Region inference with Anthropic's Claude Sonnet 4.5 is straightforward, requiring only a few changes to your existing application code. The following is an example of how to update your code in Python:

```
import boto3
import json
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"  
response = bedrock.converse(
    messages=[{"role": "user", "content": [{"text": "Explain cloud computing in 2 sentences."}]}],
    modelId=model_id,
)

print("Response:", response['output']['message']['content'][0]['text'])
print("Token usage:", response['usage'])
print("Total tokens:", response['usage']['totalTokens'])
```