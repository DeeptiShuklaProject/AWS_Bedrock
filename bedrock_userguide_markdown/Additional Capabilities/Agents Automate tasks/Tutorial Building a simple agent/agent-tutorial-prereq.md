

# Prerequisites
<a name="agent-tutorial-prereq"></a>

Before you begin this tutorial, make sure you have the following:
+ AWS account with the following managed policies:
  + [AmazonBedrockFullAccess](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-AmazonBedrockFullAccess)
  + [AWSLambda\_FullAccess](https://docs.aws.amazon.com/lambda/latest/dg/security-iam-awsmanpol.html#lambda-security-iam-awsmanpol-AWSLambda_FullAccess)
  + [IAMFullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/IAMFullAccess.html)
**Important**  
These permissions allow you to run this tutorial and other, unrelated, tasks. In production environments be sure to assign only those permissions that your users need to run your application.
+ Basic understanding of IAM roles and permissions ([IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html))
+ Familiarity with AWS Lambda functions ([Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html))