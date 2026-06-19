

# Geographic cross-Region inference
<a name="geographic-cross-region-inference"></a>

Geographic cross-Region inference keeps data processing within specified geographic boundaries (US, EU, APAC, etc.) while providing higher throughput than single-region inference. This option is ideal for organizations with data residency requirements and compliance regulations.

## Geographic cross-Region inference considerations
<a name="geographic-cris-considerations"></a>

Note the following information about Geographic cross-Region inference:
+ Cross-Region inference requests to an inference profile tied to a geography (e.g. US, EU and APAC) are kept within the AWS Regions that are part of the geography where the data originally resides. For example, a request made within the US is kept within the AWS Regions in the US. By default the data remains stored only in the source Region, but your input prompts and output results might move outside of your source Region during cross-Region inference. To the extent we store data for abuse detection, your input prompts and output results will be stored in the destination region. See [Amazon Bedrock abuse detection](abuse-detection.md) for more information on which models require storage. All data will be transmitted encrypted across Amazon's secure network.
+ To see the default quotas for cross-Region throughput when using inference profiles tied to a geography (such as US, EU and APAC), refer to the **Cross-region model inference requests per minute for ${Model}** and **Cross-region model inference tokens per minute for ${Model}** values in [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) in the *AWS General Reference*.

## IAM policy requirements for Geographic cross-Region inference
<a name="geographic-cris-iam-setup"></a>

To allow an IAM user or role to invoke a Geographic cross-Region inference profile, you need to allow access to the following resources:

1. The geography-specific cross-Region inference profile (these profiles have geographic prefixes such as `us`, `eu`, `apac`)

1. The foundation model in the source Region

1. The foundation model in all destination Regions listed in the geographic profile

The following example policy grants the required permissions to use the Claude Sonnet 4.5 foundation model with a Geographic cross-Region inference profile for the US, where the source Region is `us-east-1` and the destination Regions are `us-east-1`, `us-east-2`, and `us-west-2`:

```
{
    "Version": "2012-10-17"		 	 	 ,
    "Statement": [
        {
            "Sid": "GrantGeoCrisInferenceProfileAccess",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:us-east-1:<ACCOUNT_ID>:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
            ]
        },
        {
            "Sid": "GrantGeoCrisModelAccess",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
                "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
                "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0"
            ],
            "Condition": {
                "StringEquals": {
                    "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-east-1:<ACCOUNT_ID>:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
                }
            }
        }
    ]
}
```

The first statement grants `bedrock:InvokeModel` API access to the Geographic cross-Region inference profile for requests originating from the requesting Region. The second statement grants `bedrock:InvokeModel` API access to the foundation model in both the requesting Region and all destination Regions listed in the inference profile.

## Service Control Policy requirements for Geographic cross-Region inference
<a name="geographic-cris-scp-setup"></a>

Many organizations implement Regional access controls through Service Control Policies in AWS Organizations for security and compliance. If your organization's security policy uses SCPs to block unused Regions, you must ensure that your Region-specific SCP conditions allow access to all destination Regions listed in the Geographic cross-Region inference profile for your source Region.

For Geographic cross-Region inference, you need to understand the relationship between your source Region (where you make the API call) and the destination Regions (where requests can be routed). Check the inference profile documentation to identify all destination Regions for your source Region, then ensure your SCPs allow access to all those destination Regions.

For example, if you're calling from us-east-1 (source Region) using the US Anthropic Claude Sonnet 4.5 Geographic profile, requests can be routed to us-east-1, us-east-2, and us-west-2 (destination Regions). If an SCP restricts access to only us-east-1, cross-Region inference will fail when trying to route to us-east-2 or us-west-2. Therefore, you need to allow all three destination regions in your SCP, regardless of which Region you're calling from.

When configuring SCPs for Region exclusion, remember that blocking any destination Region in the inference profile will prevent cross-Region inference from functioning properly, even if your source Region remains accessible. For SCP requirements for Global cross-Region inference, see [Service Control Policy requirements for Global cross-Region inference](global-cross-region-inference.md#global-cris-scp-setup).

To improve security, consider using the `bedrock:InferenceProfileArn` condition to limit access to specific inference profiles. This allows you to grant access to the required Regions while restricting which inference profiles can be used.

## Use Geographic cross-Region inference
<a name="geographic-cris-usage"></a>

To use Geographic cross-Region inference, you include an [inference profile](inference-profiles.md) when running model inference in the following ways:
+ **On-demand model inference** – Specify the ID of the inference profile as the `modelId` when sending an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) request. An inference profile defines one or more Regions to which it can route inference requests originating from your source Region. Use of cross-Region inference increases throughput and performance by dynamically routing model invocation requests across the Regions defined in inference profile. Routing factors in user traffic, demand and use of resources. For more information, see [Making inference requests](inference.md)
+ **Batch inference** – Submit requests asynchronously with batch inference by specifying the ID of the inference profile as the `modelId` when sending a [CreateModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelInvocationJob.html) request. Using an inference profile lets you use compute across multiple AWS Regions and achieve faster processing times for your batch jobs. After the job is complete, you can retrieve the output files from the Amazon S3 bucket in the source Region.
+ **Agents** – Specify the ID of the inference profile in the `foundationModel` field in a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) request. For more information, see [Create and configure agent manually](agents-create.md).
+ **Knowledge base response generation** – You can use cross-Region inference when generating a response after querying a knowledge base. For more information, see [Test your knowledge base with queries and responses](knowledge-base-test.md).
+ **Model evaluation** – You can submit an inference profile as a model to evaluate when submitting a model evaluation job. For more information, see [Evaluate the performance of Amazon Bedrock resources](evaluation.md).
+ **Prompt management** – You can use cross-Region inference when generating a response for a prompt you created in Prompt management. For more information, see [Construct and store reusable prompts with Prompt management in Amazon Bedrock](prompt-management.md)
+ **Prompt flows** – You can use cross-Region inference when generating a response for a prompt you define inline in a prompt node in a prompt flow. For more information, see [Build an end-to-end generative AI workflow with Amazon Bedrock Flows](flows.md).

To learn how to use an inference profile to send model invocation requests across Regions, see [Use an inference profile in model invocation](inference-profiles-use.md).

To learn more about cross-Region inference, see [Getting started with cross-Region inference in Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/getting-started-with-cross-region-inference-in-amazon-bedrock/).

For detailed information about global cross-Region inference, including IAM setup and service quota management, see [Global cross-Region inference](global-cross-region-inference.md).