

# Making inference requests
<a name="inference"></a>

Inference is the process of generating an output from an input provided to a model. Before you can send an inference request to Amazon Bedrock, you need to allow your role to perform the model invocation API actions. This depends on the endpoint you are using.

**`bedrock-mantle` endpoint**

If your role has the `AmazonBedrockMantleInferenceAccess` AWS managed policy attached, you can skip this section. Otherwise, attach the following permissions to allow inference via the `bedrock-mantle` endpoint (Responses API, Chat Completions, Messages API):

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "MantleInferencePermissions",
            "Effect": "Allow",
            "Action": [
                "bedrock-mantle:CreateInference",
                "bedrock-mantle:GetProject",
                "bedrock-mantle:ListProjects",
                "bedrock-mantle:ListTagsForResources"
            ],
            "Resource": "*"
        }
    ]
}
```

**`bedrock-runtime` endpoint**

If your role has the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) AWS managed policy attached, you can skip this section. Otherwise, attach the following permissions to allow inference via the `bedrock-runtime` endpoint (Converse and Invoke APIs):

```
{
    "Version": "2012-10-17", 		 	 	 
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

For a detailed breakdown of each permission, see [Prerequisites for running model inference](inference-prereq.md).

**Topics**
+ [Inference using Responses API](bedrock-mantle.md)
+ [Inference using Chat Completions API](inference-chat-completions-mantle.md)
+ [Inference using Anthropic Messages API](inference-messages-api.md)
+ [Inference using Invoke API](inference-api.md)
+ [Inference using Converse API](conversation-inference.md)
+ [Influence response generation with inference parameters](inference-parameters.md)
+ [Get validated JSON results from models](structured-output.md)
+ [Enhance model responses with model reasoning](inference-reasoning.md)
+ [Optimize model inference for latency](latency-optimized-inference.md)
+ [Supported Regions and models for running model inference](inference-supported.md)