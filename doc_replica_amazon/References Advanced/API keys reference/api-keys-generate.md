

# Generate an Amazon Bedrock API key
<a name="api-keys-generate"></a>

You can generate an Amazon Bedrock API key using either the AWS Management Console or the AWS API. We recommend that you use the AWS Management Console to easily generate an Amazon Bedrock API key with few steps.

**Warning**  
We strongly recommend restricting the use of Amazon Bedrock API keys for exploration of Amazon Bedrock. When you're ready to incorporate Amazon Bedrock into applications with greater security requirements, you should switch to short-term credentials. For more information, see [Alternatives to long-term access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html#security-creds-alternatives-to-long-term-access-keys) in the IAM User Guide.

**Topics**
+ [Generate an Amazon Bedrock API key using the console](#api-keys-generate-console)
+ [Generate a long-term Amazon Bedrock API key using the API](#api-keys-generate-api-long-term)
+ [Generate a short-term Amazon Bedrock API key using a client library](#api-keys-generate-short-term)
+ [Set up automatic refresh of short-term Amazon Bedrock API keys](#api-keys-refresh-short-term)

## Generate an Amazon Bedrock API key using the console
<a name="api-keys-generate-console"></a>

To generate an Amazon Bedrock API key using the console, do the following:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, select **API keys**.

1. Generate one of the following types of keys:
   + **Short-term API key** – In the **Short-term API keys** tab, choose **Generate short-term API keys**. The key expires when your console session expires (and no longer than 12 hours) and lets you make calls to the AWS Region that you generated it from. To generate a key for a different Region, select that Region in the console before generating the key.
   + **Long-term API key** – In the **Long-term API keys** tab, choose **Generate long-term API keys**.

     1. In the **API key expiration** section, choose a time after which the key will expire.

     1. (Optional) By default, the [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) AWS-managed policy, which grants access to core Amazon Bedrock API operations, is attached to the IAM user associated with the key. To select more policies to attach to the user, expand the **Advanced permissions** section and select the policies that you want to add.

     1. Choose **Generate**.
**Warning**  
We strongly recommend restricting the use of Amazon Bedrock API keys for exploration of Amazon Bedrock. When you're ready to incorporate Amazon Bedrock into applications with greater security requirements, you should switch to short-term credentials. For more information, see [Alternatives to long-term access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html#security-creds-alternatives-to-long-term-access-keys) in the IAM User Guide.



## Generate a long-term Amazon Bedrock API key using the API
<a name="api-keys-generate-api-long-term"></a>

The general steps for creating a long-term Amazon Bedrock API key in the API are as follows:

1. Create an IAM user by sending a [CreateUser](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateUser.html) request with an [IAM endpoint](https://docs.aws.amazon.com/general/latest/gr/iam-service.html).

1. Attach the [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) to the IAM user by sending an [AttachUserPolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachUserPolicy.html) request with an [IAM endpoint](https://docs.aws.amazon.com/general/latest/gr/iam-service.html). You can repeat this step to attach other managed or custom policies as necessary to the user.
**Note**  
As a best security practice, we strongly recommend that you attach IAM policies to the IAM user to restrict the use of Amazon Bedrock API keys. For examples of time-bounding policies and restricting the IP addresses that can use the key, see [Control the use of access keys by attaching an inline policy to an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-keys_inline-policy.html).

1. Generate the long-term Amazon Bedrock API key by sending a [CreateServiceSpecificCredential](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateServiceSpecificCredential.html.html) request with an [IAM endpoint](https://docs.aws.amazon.com/general/latest/gr/iam-service.html) and specifying `bedrock.amazonaws.com` as the `ServiceName`.
   + The `ServiceApiKeyValue` returned in the response is your long-term Amazon Bedrock API key.
   + The `ServiceSpecificCredentialId` returned in the response can be used to carry out API operations related to the key.

To learn how to generate a long-term Amazon Bedrock API key, choose the tab for your preferred method, and then follow the steps:

------
#### [ CLI ]

To create a long-term Amazon Bedrock API key, you use AWS Identity and Access Management API operations. First, make sure that you've fulfilled the prerequisite:

**Prerequisite**  
Ensure that your setup allows the AWS CLI to automatically recognize your AWS credentials. To learn more, see [Configuring settings for the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Open a terminal and run the following commands:

1. Create an IAM user. You can replace the name with one of your choice:

   ```
   aws iam create-user --user-name bedrock-api-user
   ```

1. Attach the [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) to the user. You can repeat this step with the ARNs of any other AWS-managed or custom policies you want to add to the API key:

   ```
   aws iam attach-user-policy --user-name bedrock-api-user --policy-arn arn:aws:iam::aws:policy/AmazonBedrockLimitedAccess
   ```

1. Create the long-term Amazon Bedrock API key, replacing {{${NUMBER-OF-DAYS}}} with the number of days for which you want the key to last:

   ```
   aws iam create-service-specific-credential \
       --user-name bedrock-api-user \
       --service-name bedrock.amazonaws.com \
       --credential-age-days {{${NUMBER-OF-DAYS}}}
   ```

------
#### [ Python ]

To create a long-term Amazon Bedrock API key, you use AWS Identity and Access Management API operations. First, make sure that you've fulfilled the prerequisite:

**Prerequisite**  
Ensure that your setup allows Python to automatically recognize your AWS credentials. To learn more, see [Configuring settings for the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Run the following script to create an IAM user, attach permissions to perform Amazon Bedrock actions, and generate a long-term Amazon Bedrock API key to associate with the user:

```
import boto3
from datetime import datetime, timedelta

# Replace with name for your IAM user
username = "bedrock-api-user"
# Add any AWS-managed or custom policies that you want to the user
bedrock_policies = [
    "arn:aws:iam::aws:policy/AmazonBedrockLimitedAccess",        # Limited access
#    "arn:aws:iam::aws:policy/AmazonBedrockMarketplaceAccess",   # Optional: Access to Amazon Bedrock Marketplace actions
]
# Set the key expiration time to a number of your choice
expiration_time_in_days = 30

iam_client = boto3.client("iam")
    
# Create IAM user
user = iam_client.create_iam_user(username)

# Attach policies to user
for policy_arn in bedrock_policies:
    iam_client.attach_managed_policy(username, policy_arn)

# Create long-term Amazon Bedrock API key and return it
service_credentials = iam_client.create_service_specific_credential(
    user_name=username, 
    service_name="bedrock",
    credential_age_days=expiration_time_in_days
) 
api_key = service_credentials["ServiceApiKeyValue"]
print(api_key)
```

------

## Generate a short-term Amazon Bedrock API key using a client library
<a name="api-keys-generate-short-term"></a>

Short term keys have the following properties:
+ Valid for the shorter of the following values:
  + 12 hours
  + The duration of the session generated by the IAM principal used to generate the key.
+ Inherit the permissions attached to the principal used to generate the key.
+ Can be used only in the AWS Region from which you generated it.

For long-running applications, the [aws-bedrock-token-generator](https://github.com/aws/aws-bedrock-token-generator-js/blob/main/README.md) client library can create new Amazon Bedrock short-term API keys as needed when credentials are refreshed. For more information, see [Set up automatic refresh of short-term Amazon Bedrock API keys](#api-keys-refresh-short-term).

**Prerequisites**
+ Ensure that the IAM principal that you use to generate the key is set up with the proper permissions to use Amazon Bedrock. For experimentation, you can attach the AWS-managed [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) policy to the principal. You can refer to the [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) for protecting your credentials.
+ Ensure that your setup allows Python to automatically recognize your AWS credentials. The default method by which credentials are retrieved follows a defined hierarchy. You can see the hierarchy for a specific SDK or tool at [AWS SDKs and Tools standardized credential providers](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html).
+ Install the Amazon Bedrock token generator. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

Open a terminal and run the following command:

```
pip install aws-bedrock-token-generator
```

------
#### [ Javascript ]

Open a terminal and run the following command:

```
npm install @aws/bedrock-token-generator
```

------
#### [ Java ]

If you use Maven, add the following dependency to your `pom.xml`:

```
<dependency>
    <groupId>software.amazon.bedrock</groupId>
    <artifactId>aws-bedrock-token-generator</artifactId>
    <version>1.1.0</version>
</dependency>
```

If you use Gradle, add the following to your `build.gradle`:

```
implementation 'software.amazon.bedrock:aws-bedrock-token-generator:1.1.0'
```

------

**Examples**  
To see examples for using the token generator to generate a short-term Amazon Bedrock API key with your default credentials in different languages, choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

```
from aws_bedrock_token_generator import provide_token

token = provide_token()
print(f"Token: {token}")
```

------
#### [ Javascript ]

```
import { getTokenProvider } from "@aws/bedrock-token-generator";

// Create a token provider that uses default credentials and region providers.
// You can configure it to use other credential providers.
const provideToken = getTokenProvider();

async function example() {
    
  const token = await provideToken();

  // Use the token for API calls. The token has a default expiration of 12 hour.
  // If the expiresInSeconds parameter is specified during token creation, the 
  // expiration can be configured up to a maximum of 12 hours. However, the actual 
  // token validity period will always be the minimum of the requested expiration 
  // time and the AWS credentials' expiry time
  console.log(`Bearer Token: ${token}`);
}
```

------
#### [ Java ]

```
import software.amazon.bedrock.token.BedrockTokenGenerator;

// Credentials and region will be picked up from the default provider chain
BedrockTokenGenerator tokenGenerator = BedrockTokenGenerator.builder().build();
tokenGenerator.getToken();
```

------

To see more examples for different use cases when generating tokens, see the following links:
+ [Python](https://github.com/aws/aws-bedrock-token-generator-python/blob/main/README.md)
+ [Javascript](https://github.com/aws/aws-bedrock-token-generator-js/blob/main/README.md)
+ [Java](https://github.com/aws/aws-bedrock-token-generator-java/blob/main/README.md)

## Set up automatic refresh of short-term Amazon Bedrock API keys
<a name="api-keys-refresh-short-term"></a>

You can create a script with the help of the `aws-bedrock-token-generator` package to programmatically regenerate a new short-term key whenever your current one has expired. First, ensure that you've fulfilled the prerequisites at [Generate a short-term Amazon Bedrock API key using a client library](#api-keys-generate-short-term). To see example scripts that retrieve a token and make a Converse request, choose the tab for your preferred method, and then follow the steps:

------
#### [ Python ]

```
from aws_bedrock_token_generator import provide_token
import requests

def get_new_token():
    url = "https://bedrock-runtime.us-west-2.amazonaws.com/model/us.anthropic.claude-sonnet-4-6/converse"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": "Hello"}]
            }
        ]
    }

    # Create a token provider that uses default credentials and region providers.
    # You can configure it to use other credential providers.
    # https://github.com/aws/aws-bedrock-token-generator-python/blob/main/README.md
    # It can be used for each API call as it is inexpensive.
    token = provide_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

if __name__ == "__main__":
    get_new_token()
```

------
#### [ Javascript ]

```
import { getTokenProvider } from "@aws/bedrock-token-generator";

// Create a token provider that uses default credentials and region providers.
// You can configure it to use other credential providers.
// https://github.com/aws/aws-bedrock-token-generator-js/blob/main/README.md
// This can be created just once. Use await provideToken() to fetch the token
const provideToken = getTokenProvider();

async function example() {
    const url = "https://bedrock-runtime.us-east-1.amazonaws.com/model/us.anthropic.claude-sonnet-4-6/converse";
    const payload = {
        messages: [
            {
                role: "user",
                content: [{ text: "Hello" }]
            }
        ]
    };
    const headers = {
        "Content-Type": "application/json",
        // provideToken retrieves a valid token. It can be used for each API call as it is inexpensive.
        "Authorization": `Bearer ${await provideToken()}`
    };
    await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(payload)
    })
}
```

------
#### [ Java ]

```
package com.amazon.bedrocktoken;

import software.amazon.bedrock.token.BedrockTokenGenerator;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class GetNewToken {
    public static void main(String[] args) throws Exception {
        // Use default credentials and region from environment/profile chain
        // Create a token generator that uses default credentials and region providers.
        // You can configure it to use other credential providers.
        // https://github.com/aws/aws-bedrock-token-generator-java/blob/main/README.md
        BedrockTokenGenerator tokenGenerator = BedrockTokenGenerator.builder().build();

        // getToken() retrieves a valid token. It can be used for each API call as it is inexpensive.
        String token = tokenGenerator.getToken();

        String url = "https://bedrock-runtime.us-west-2.amazonaws.com/model/us.anthropic.claude-sonnet-4-6/converse";
        String payload = "{\n" +
                "    \"messages\": [\n" +
                "        {\n" +
                "            \"role\": \"user\",\n" +
                "            \"content\": [{ \"text\": \"Hello\" }]\n" +
                "        }\n" +
                "    ]\n" +
                "}";

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .header("Authorization", "Bearer " + token)
            .POST(HttpRequest.BodyPublishers.ofString(payload))
            .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println(response.body());
    }
}
```

------