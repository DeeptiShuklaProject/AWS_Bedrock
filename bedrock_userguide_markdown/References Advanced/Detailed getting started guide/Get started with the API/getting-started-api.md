

# Get started with the API
<a name="getting-started-api"></a>

This section describes how to set up your environment to make Amazon Bedrock requests through the AWS API. AWS offers the following tools to streamline your experience:
+ AWS Command Line Interface (AWS CLI)
+ AWS SDKs
+ Amazon SageMaker AI notebooks

To get started with the API, you need credentials to grant programmatic access. If the following sections pertain to you, expand them and follow the instructions. Otherwise, proceed through the remaining sections.

## I'm new to AWS
<a name="gs-api-new-to-aws"></a>

If you do not have an AWS account, complete the following steps to create one.

**To sign up for an AWS account**

1. Open [https://portal.aws.amazon.com/billing/signup](https://portal.aws.amazon.com/billing/signup).

1. Follow the online instructions.

   Part of the sign-up procedure involves receiving a phone call or text message and entering a verification code on the phone keypad.

   When you sign up for an AWS account, an *AWS account root user* is created. The root user has access to all AWS services and resources in the account. As a security best practice, assign administrative access to a user, and use only the root user to perform [tasks that require root user access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#root-user-tasks).

AWS sends you a confirmation email after the sign-up process is complete. At any time, you can view your current account activity and manage your account by going to [https://aws.amazon.com/](https://aws.amazon.com/) and choosing **My Account**.

**Secure your AWS account root user**

1.  Sign in to the [AWS Management Console](https://console.aws.amazon.com/) as the account owner by choosing **Root user** and entering your AWS account email address. On the next page, enter your password.

   For help signing in by using root user, see [Signing in as the root user](https://docs.aws.amazon.com/signin/latest/userguide/console-sign-in-tutorials.html#introduction-to-root-user-sign-in-tutorial) in the *AWS Sign-In User Guide*.

1. Turn on multi-factor authentication (MFA) for your root user.

   For instructions, see [Enable a virtual MFA device for your AWS account root user (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-virt-mfa-for-root.html) in the *IAM User Guide*.

## I need to install the AWS CLI or an AWS SDK
<a name="gs-api-cli-sdk-install"></a>

To install the AWS CLI, follow the steps at [Install or update to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

To install an AWS SDK, select the tab that corresponds to the programming language that you want to use at [Tools to Build on AWS](https://aws.amazon.com/developer/tools/). AWS software development kits (SDKs) are available for many popular programming languages. Each SDK provides an API, code examples, and documentation that make it easier for developers to build applications in their preferred language. SDKs automatically perform useful tasks for you, such as:
+ Cryptographically sign your service requests
+ Retry requests
+ Handle error responses

## Get credentials to grant programmatic access
<a name="gs-grant-program-access"></a>

Users need programmatic access if they want to interact with AWS outside of the AWS Management Console. AWS provides multiple options, depending on your security concerns.

**Note**  
For a step-by-step guide to generate an API key that you can use to quickly access the Amazon Bedrock API, see [Get started with Amazon Bedrock API keys: Generate a 30-day key and make your first API call](getting-started-api-keys.md).  
For greater security requirements, continue through this section.

The way to grant programmatic access depends on the type of user that's accessing AWS.

To grant users programmatic access, choose one of the following options.


****  

| Which principal needs programmatic access? | To | By | 
| --- | --- | --- | 
| IAM users | Limit the duration of long-term credentials to sign programmatic requests to the AWS CLI, AWS SDKs, or AWS APIs. | Following the instructions for the interface that you want to use.[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api.html) | 
| IAM roles | Use temporary credentials to sign programmatic requests to the AWS CLI, AWS SDKs, or AWS APIs. | Following the instructions in [Using temporary credentials with AWS resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) in the IAM User Guide. | 
| Workforce identity<br />(Users managed in IAM Identity Center) | Use temporary credentials to sign programmatic requests to the AWS CLI, AWS SDKs, or AWS APIs. | Following the instructions for the interface that you want to use.[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api.html) | 

## How to configure access keys for an IAM user
<a name="create-user-time-bound"></a>

If you decide to use access keys for an IAM user, AWS recommends that you set an expiration for the IAM user by including a restrictive inline policy.

**Important**  
Heed the following warnings:  
**Do NOT** use your account's root credentials to access AWS resources. These credentials provide unrestricted account access and are difficult to revoke.
**Do NOT** put literal access keys or credential information in your application files. If you do, you create a risk of accidentally exposing your credentials if, for example, you upload the project to a public repository.
**Do NOT** include files that contain credentials in your project area.
Manage your access keys securely. Do not provide your access keys to unauthorized parties, even to help [find your account identifiers](https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html). By doing this, you might give someone permanent access to your account.
Be aware that any credentials stored in the shared AWS credentials file are stored in plaintext.

For more details, see [Best practices for managing AWS access keys](https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html) in the AWS General Reference.

**Create an IAM user**

1. On the AWS Management Console Home page, select the IAM service or navigate to the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

1. In the navigation pane, select **Users** and then select **Create user**.

1. Follow the guidance in the IAM console to set up a programmatic user (without access to the AWS Management Console) and without permissions.

**Restrict user access to a limited time window**

Any IAM user access keys that you create are long-term credentials. To ensure that these credentials expire in case they are mishandled, you can make these credentials time-bound by creating an inline policy that specifies a date after which the keys will no longer be valid.

1. Open the IAM user that you just created. In the **Permissions** tab, choose **Add permissions** and then choose **Create inline policy**.

1. In the JSON editor, specify the following permissions. To use this policy, replace the value for `aws:CurrentTime` timestamp value in the example policy with your own end date.
**Note**  
IAM recommends that you limit your access keys to 12 hours.

------
#### [ JSON ]

****  

   ```
   {
     "Version":"2012-10-17",		 	 	 
     "Statement": [
       {
         "Effect": "Deny",
         "Action": "*",
         "Resource": "*",
         "Condition": {
           "DateGreaterThan": {
             "aws:CurrentTime": "{{2024-01-01T00:00:000}}"
           }
         }
       }
     ]
   }
   ```

------

**Create an access key**

1. On the **User details** page, select the **Security credentials** tab. In the **Access keys** section, choose **Create access key**.

1. Indicate that you plan to use these access keys as **Other** and choose **Create access key**.

1. On the **Retrieve access key** page, choose **Show** to reveal the value of your user's secret access key. You can copy the credentials or download a .csv file.

**Important**  
When you no longer need this IAM user, we recommend that you remove it and align with the [AWS security best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials), we recommend that you require your human users to use temporary credentials through [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html) when accessing AWS.

## Attach Amazon Bedrock permissions to a user or role
<a name="gs-api-br-permissions"></a>

After setting up credentials for programmatic access, you need to configure permissions for a user or IAM role to have access a set of Amazon Bedrock-related actions. To set up these permissions, do the following:

1. On the AWS Management Console Home page, select the IAM service or navigate to the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

1. Select **Users** or **Roles** and then select your user or role.

1. In the **Permissions** tab, choose **Add permissions** and then choose **Add AWS managed policy**. Choose the [AmazonBedrockFullAccess]() AWS managed policy.

1. To allow the user or role to subscribe to models, choose **Create inline policy** and then specify the following permissions in the JSON editor:

------
#### [ JSON ]

****  

   ```
   {
     "Version":"2012-10-17",		 	 	 
     "Statement": [
         {
             "Sid": "MarketplaceBedrock",
             "Effect": "Allow",
             "Action": [
                 "aws-marketplace:ViewSubscriptions",
                 "aws-marketplace:Unsubscribe",
                 "aws-marketplace:Subscribe"
             ],
             "Resource": "*"
         }
     ]
   }
   ```

------

## Try making API calls to Amazon Bedrock
<a name="gs-try-bedrock"></a>

After you've fulfilled all the prerequisites, select one of the following topics to test out making model invocation requests using Amazon Bedrock models:

**Topics**
+ [Get credentials to grant programmatic access](#gs-grant-program-access)
+ [Attach Amazon Bedrock permissions to a user or role](#gs-api-br-permissions)
+ [Try making API calls to Amazon Bedrock](#gs-try-bedrock)
+ [Get started with Amazon Bedrock API keys: Generate a 30-day key and make your first API call](getting-started-api-keys.md)
+ [Run example Amazon Bedrock API requests with the AWS Command Line Interface](getting-started-api-ex-cli.md)
+ [Run example Amazon Bedrock API requests through the AWS SDK for Python (Boto3)](getting-started-api-ex-python.md)
+ [Run example Amazon Bedrock API requests using an Amazon SageMaker AI notebook](getting-started-api-ex-sm.md)