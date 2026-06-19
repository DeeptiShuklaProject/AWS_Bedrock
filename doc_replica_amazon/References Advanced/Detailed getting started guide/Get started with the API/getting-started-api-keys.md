

# Get started with Amazon Bedrock API keys: Generate a 30-day key and make your first API call
<a name="getting-started-api-keys"></a>

This tutorial walks you through creating a long-term Amazon Bedrock API key that expires in 30 days and using it to make a simple [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API call using Python. This is the fastest way to start experimenting with Amazon Bedrock without setting up complex AWS credentials.

**Warning**  
Long-term API keys are recommended only for exploration and development of Amazon Bedrock. For production applications, use [alternatives to long-term access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html#security-creds-alternatives-to-long-term-access-keys) such as IAM roles or temporary credentials.

Follow these steps to create a long-term Amazon Bedrock API key that expires in 30 days:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, select **API keys**.

1. In the **Long-term API keys** tab, choose **Generate long-term API keys**.

1. In the **API key expiration** section, select **30 days**.

1. Choose **Generate**. The key you generate provides permissions to carry out core Amazon Bedrock actions, as defined in the attached [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) policy.

1. Copy the generated API key and store it securely. You'll need this key for the next step.
**Important**  
The API key is only displayed once. Make sure to copy and save it before closing the dialog. Remember that your API key will expire in 30 days. You can generate a new one by following the same steps, or consider transitioning to more secure authentication methods for ongoing use.

1. Set the API key as an environment variable by replacing {{${api-key}}} with your generated API key value and use it to generate a response in your method of choice:

------
#### [ Python ]

   ```
   import boto3
   import os
   
   # Set the API key as an environment variable
   os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "{{${api-key}}}"
   
   # Create the Bedrock client
   client = boto3.client(
       service_name="bedrock-runtime",
       region_name="us-east-1"
   )
   
   # Define the model and message
   model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
   messages = [{"role": "user", "content": [{"text": "Hello! Can you tell me about Amazon Bedrock?"}]}]
   
   # Make the API call
   response = client.converse(
       modelId=model_id,
       messages=messages,
   )
   
   # Print the response
   print(response['output']['message']['content'][0]['text'])
   ```

------
#### [ HTTP client using Python ]

   ```
   import requests
   
   url = "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-3-5-haiku-20241022-v1:0/converse"
   
   payload = {
       "messages": [
           {
               "role": "user",
               "content": [{"text": "Hello"}]
           }
       ]
   }
   
   headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer {{${api-key}}}"
   }
   
   response = requests.request("POST", url, json=payload, headers=headers)
   
   print(response.text)
   ```

------
#### [ HTTP request using cURL ]

   ```
   curl -X POST "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-3-5-haiku-20241022-v1:0/converse" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer {{${api-key}}}" \
     -d '{
       "messages": [
           {
               "role": "user",
               "content": [{"text": "Hello"}]
           }
       ]
     }'
   ```

------

Congratulations\! You've successfully generated an Amazon Bedrock API key and made your first API call to the Amazon Bedrock service. After exploring some more Amazon Bedrock actions, you should transition to more secure methods of authentication such as short-term Amazon Bedrock API keys or AWS-wide temporary credentials. Refer to the following resources to learn more:
+ **Explore different models** – Learn about other foundation models available in Amazon Bedrock at [Using models with Bedrock](foundation-models-reference.md) and change the `model_id` in your code to try them out.
+ **Learn about model inference** – Learn about generating responses with model inference by reading about concepts and the options available in Amazon Bedrock at [Making inference requests](inference.md).
+ **Plan for production with more secure authentication methods** – Read about Amazon Bedrock API keys in greater detail in the Build chapter and how to create more secure, short-term Amazon Bedrock API keys. When you're ready to build production applications, you should also review [alternatives to long-term access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html#security-creds-alternatives-to-long-term-access-keys) for more secure options that also allow access to other AWS services.