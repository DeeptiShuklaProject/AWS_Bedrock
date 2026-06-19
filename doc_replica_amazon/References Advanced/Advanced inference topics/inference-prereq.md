

# Prerequisites for running model inference
<a name="inference-prereq"></a>

For a role to run model inference, you need to allow it to perform the model invocation API actions. If your role has the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) AWS managed policy attached, you can skip this section. Otherwise, attach the following permissions to the role to allow it to use the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), and [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) actions with all supported resources in Amazon Bedrock:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ModelInvocationPermissions",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:GetInferenceProfile",
                "bedrock:ListInferenceProfiles",
                "bedrock:RenderPrompt",
                "bedrock:GetCustomModel",
                "bedrock:ListCustomModels",
                "bedrock:GetImportedModel",
                "bedrock:ListImportedModels",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:GetGuardrail",
                "bedrock:ListGuardrails",
                "bedrock:ApplyGuardrail"
            ],
            "Resource": "*"
        }
    ]
}
```

------

To further restrict permissions, you can omit actions, or you can specify resources and condition keys by which to filter permissions. For more information about actions, resources, and condition keys, see the following topics in the *Service Authorization Reference*:
+ [Actions defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) – Learn about actions, the resource types that you can scope them to in the `Resource` field, and the condition keys that you can filter permissions on in the `Condition` field.
+ [Resource types defined by Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-resources-for-iam-policies) – Learn about the resource types in Amazon Bedrock.
+ [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) – Learn about the condition keys in Amazon Bedrock.

The following list summarizes whether you need an action, depending on your use case:
+ `bedrock:InvokeModel` – Required to carry out model invocation. Allows the role to call the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API operations.
+ `bedrock:InvokeModelWithResponseStream` – Required to carry out model invocation and return streaming responses. Allows the role to call the [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) and [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)Stream API operations.
+ The following actions allow a role to run inference with Amazon Bedrock resources other than foundation models:
  + `bedrock:GetInferenceProfile` – Required to run inference with an [inference profile](inference-profiles.md).
  + `bedrock:RenderPrompt` – Required to invoke a prompt from [Prompt management](prompt-management.md).
  + `bedrock:GetCustomModel` – Required to run inference with a [custom model](custom-models.md).
  + `bedrock:GetImportedModel` – Required to run inference with an [imported model](model-customization-import-model.md).
  + `bedrock:GetProvisionedModelThroughput` – Required to run inference with a [Provisioned Throughput](prov-throughput.md).
+ The following actions allow a role to see Amazon Bedrock resources other than foundation models in the Amazon Bedrock console and to select them:
  + `bedrock:ListInferenceProfiles` – Required to choose an [inference profile](custom-models.md) in the Amazon Bedrock console.
  + `bedrock:ListCustomModels` – Required to choose a [custom model](custom-models.md) in the Amazon Bedrock console.
  + `bedrock:ListImportedModels` – Required to choose an [imported model](model-customization-import-model.md) in the Amazon Bedrock console.
  + `bedrock:ListProvisionedModelThroughputs` – Required to choose a [Provisioned Throughput](prov-throughput.md) in the Amazon Bedrock console.
+ The following actions allow a role to access and apply guardrails from [Amazon Bedrock Guardrails](guardrails.md) during model invocation:
  + `bedrock:GetGuardrail` – Required to use a guardrail during model invocation.
  + `bedrock:ApplyGuardrail` – Required to apply a guardrail during model invocation.
  + `bedrock:ListGuardrails` – Required to choose a guardrail in the Amazon Bedrock console.