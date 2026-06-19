

# Get list of models
<a name="models-get-info"></a>

Amazon Bedrock provides two separate inference endpoints, each with its own API for listing the models available on it. For an overview of the endpoints, see [Endpoints supported by Amazon Bedrock](endpoints.md).
+ **`bedrock-mantle`** – Use the OpenAI-compatible `/models` endpoint (for example, `client.models.list()` with the OpenAI SDK) to list the models available on `bedrock-mantle`.
+ **`bedrock-runtime`** – Use the AWS-native [ListFoundationModels](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) API. The response returns a [FoundationModelSummary](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_FoundationModelSummary.html) object for each model, including its ARN, model ID, supported modalities and features, and deprecation status. To get details for a specific model, use [GetFoundationModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html), specifying the [model ID](models-supported.md).
**Note**  
The response also returns model IDs that aren't in the [base model ID](models-supported.md) or base model IDs for Provisioned Throughput charts. These model IDs are deprecated or for backwards compatibility.

Choose a tab to see code examples in an interface or language.

**List models on `bedrock-mantle`**

------
#### [ OpenAI SDK (Python) ]

```
# List all available models using the OpenAI SDK
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

from openai import OpenAI

client = OpenAI()

models = client.models.list()

for model in models.data:
    print(model.id)
```

------
#### [ Anthropic SDK (Python) ]

```
from anthropic import AnthropicBedrockMantle

client = AnthropicBedrockMantle(aws_region="us-east-1")
models = client.models.list()

for model in models.data:
    print(model.id)
```

**Note**  
The `bedrock-mantle` `/v1/models` endpoint returns OpenAI-shaped model entries. Only `model.id` is reliable when using the Anthropic SDK; other fields on `ModelInfo` may be empty.

------
#### [ curl ]

```
# List all available models
# Requires OPENAI_API_KEY and OPENAI_BASE_URL environment variables

curl -X GET $OPENAI_BASE_URL/models \
   -H "Authorization: Bearer $OPENAI_API_KEY"
```

------

**List and get models on `bedrock-runtime`**

------
#### [ AWS CLI ]

List the Amazon Bedrock foundation models.

```
aws bedrock list-foundation-models
```

Get information about Anthropic Claude v2.

```
aws bedrock get-foundation-model --model-identifier anthropic.claude-sonnet-4-20250514-v1:0
```

------
#### [ Python ]

List the Amazon Bedrock foundation models.

```
import boto3 
bedrock = boto3.client(service_name='bedrock')

bedrock.list_foundation_models()
```

Get information about Anthropic Claude v2.

```
import boto3 
bedrock = boto3.client(service_name='bedrock')

bedrock.get_foundation_model(modelIdentifier='anthropic.claude-sonnet-4-20250514-v1:0')
```

------
#### [ curl ]

List the Amazon Bedrock foundation models. Requires AWS credentials in the environment (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`) and curl 7.75.0 or later for `--aws-sigv4` support.

```
curl -X GET "https://bedrock.us-east-1.amazonaws.com/foundation-models" \
    --aws-sigv4 "aws:amz:us-east-1:bedrock" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY"
```

Get information about Anthropic Claude v2.

```
curl -X GET "https://bedrock.us-east-1.amazonaws.com/foundation-model/anthropic.claude-sonnet-4-20250514-v1:0" \
    --aws-sigv4 "aws:amz:us-east-1:bedrock" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY"
```

------