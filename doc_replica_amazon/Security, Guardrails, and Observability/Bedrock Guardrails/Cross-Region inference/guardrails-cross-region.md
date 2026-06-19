

# Distribute guardrail inference across AWS Regions
<a name="guardrails-cross-region"></a>

You can enable cross-Region inference with Amazon Bedrock Guardrails, which automatically routes inference requests during guardrail policy evaluation to the optimal AWS Region within your geography. (For more information on how this works, see [Increase throughput with cross-Region inference](cross-region-inference.md).) Distributing inference requests across AWS Regions maximizes available compute resources and model availability, helping maintain guardrail performance and reliability when demand increases. There's no additional cost for using cross-Region inferencing.

Cross-Region inference requests are kept within the Regions that are part of the geography where the data originally resides. For example, a request made in the US is kept within Regions in the US. Although your guardrail configuration remains stored only in the primary Region, your input prompts and output results might move outside of your primary Region when using cross-Region inference. All data is transmitted encrypted within Amazon's secure network.

## Set up cross-Region guardrail inference
<a name="guardrail-profiles-set-up"></a>

Cross-Region guardrail inference is handled through a *guardrail profile*, which is a system-defined resource that you can specify when [creating](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-create.html) or [modifying](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-edit.html) a guardrail one of the following ways:
+ Using the Amazon Bedrock console.
+ Sending a [CreateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateGuardrail.html) or [UpdateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UpdateGuardrail.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp).

You need specific permissions to use cross-Region guardrail inference. For more information, see [Permissions for using cross-Region inference with Amazon Bedrock Guardrails](guardrail-profiles-permissions.md).