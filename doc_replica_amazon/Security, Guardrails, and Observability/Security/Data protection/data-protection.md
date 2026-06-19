

# Data protection
<a name="data-protection"></a>

The AWS [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) applies to data protection in Amazon Bedrock. As described in this model, AWS is responsible for protecting the global infrastructure that runs all of the AWS Cloud. You are responsible for maintaining control over your content that is hosted on this infrastructure. You are also responsible for the security configuration and management tasks for the AWS services that you use. For more information about data privacy, see [Data Privacy FAQ](https://aws.amazon.com/compliance/data-privacy-faq/).  For information about data protection in Europe, see the [General Data Protection Regulation (GDPR) Center](https://aws.amazon.com/compliance/gdpr-center/). 

For data protection purposes, we recommend that you protect AWS account credentials and set up individual users with AWS IAM Identity Center or AWS Identity and Access Management (IAM). That way, each user is given only the permissions necessary to fulfill their job duties. We also recommend that you secure your data in the following ways:
+ Use multi-factor authentication (MFA) with each account.
+ Use SSL/TLS to communicate with AWS resources. We require TLS 1.2 and recommend TLS 1.3.
+ Set up API and user activity logging with AWS CloudTrail. For information about using CloudTrail trails to capture AWS activities, see [Working with CloudTrail trails](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-trails.html) in the *AWS CloudTrail User Guide*.
+ Use AWS encryption solutions, along with all default security controls within AWS services.
+ Use advanced managed security services such as Amazon Macie, which assists in discovering and securing sensitive data that is stored in Amazon S3.
+ If you require FIPS 140-3 validated cryptographic modules when accessing AWS through a command line interface or an API, use a FIPS endpoint. For more information about the available FIPS endpoints, see [Federal Information Processing Standard (FIPS) 140-3](https://aws.amazon.com/compliance/fips/).

We strongly recommend that you never put confidential or sensitive information, such as your customers' email addresses, into tags or free-form text fields such as a **Name** field. This includes when you work with Amazon Bedrock or other AWS services using the console, API, AWS CLI, or AWS SDKs. Any data that you enter into tags or free-form text fields used for names may be used for billing or diagnostic logs. If you provide a URL to an external server, we strongly recommend that you do not include credentials information in the URL to validate your request to that server.

For more information on how your data is processed for abuse detection, see [Amazon Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html).

Amazon Bedrock has a concept of a Model Deployment Account—in each AWS Region where Amazon Bedrock is available, there is one such deployment account per model provider. These accounts are owned and operated by the Amazon Bedrock service team. Model providers don't have any access to those accounts. After delivery of a model from a model provider to AWS, Amazon Bedrock will perform a deep copy of a model provider’s inference and training software into those accounts for deployment. Because the model providers don't have access to those accounts, they don't have access to Amazon Bedrock logs or to customer prompts and completions.

**Topics**
+ [Data encryption](data-encryption.md)
+ [Protect your data using Amazon VPC and AWS PrivateLink](usingVPC.md)
+ [Data retention](data-retention.md)