

# Call the endpoint
<a name="bedrock-marketplace-call-the-endpoint"></a>

You can start using your model after you've deployed it to an endpoint. You use either the `Converse` or `InvokeModel` operations to call the models.

For a list of models which are supported by `Converse` operation, see [Model compatibility](bedrock-marketplace-model-reference.md). For information about Agents, see [Automate tasks in your application using AI agents](agents.md). For information about knowledge bases, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md).

**To use a model**

1. Sign in to the AWS Management Console using an IAM role with Amazon Bedrock permissions.

1. In the search bar, specify "Amazon Bedrock" and choose **Amazon Bedrock** from the dropdown list.

1. Choose the tool you're using. **Playground** is the fastest way to access the model that you've deployed.

1. Choose **Select Model**.

1. Choose your model's endpoint.

You can also use the following example AWS Command Line Interface commands to call the endpoint.

```
aws bedrock-runtime converse --model-id arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint-name}} --messages '[{"role": "user", "content": [{"text": "Describe the purpose of a \"hello world\" program in one line."}]}]'
```

```
aws bedrock-runtime invoke-model --model-id arn:aws:sagemaker:region:{{111122223333}}:endpoint/{{example-endpoint-name}} --body '{"inputs": "Hello? How are you?", "parameters": {"details": true}}' --cli-binary-format raw-in-base64-out test.txt
```