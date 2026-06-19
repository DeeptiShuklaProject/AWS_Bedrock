

# Prerequisites for Amazon Bedrock Flows
<a name="flows-prereq"></a>

Before creating a flow, review the following prerequisites and determine which ones you need to fulfill:

1. Define or create resources for one or more nodes you plan to add to your flow: 
   + For a prompt node – Create a prompt by using Prompt management. For more information, see [Construct and store reusable prompts with Prompt management in Amazon Bedrock](prompt-management.md). If you plan to define prompts inline when creating the node in the flow, you don't have to create a prompt in Prompt management.
   + For a knowledge base node – Create a knowledge base that you plan to use in the flow. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](knowledge-base.md).
   + For an agent node – Create an agent that you plan to use in the flow. For more information, see [Automate tasks in your application using AI agents](agents.md).
   + For an S3 storage node – Create an S3 bucket to store an output from a node in the flow.
   + For an S3 retrieval node – Create an S3 object in a bucket from which to retrieve data for the flow. The S3 object must be a UTF-8 encoded string.
   + For a Lambda node – Define a AWS Lambda function for the business logic you plan to implement in the flow. For more information, see the [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/).
   + For a Amazon Lex node – Create a Amazon Lex bot to identify intents. For more information, see the [Amazon Lex Developer Guide](https://docs.aws.amazon.com/lex/latest/dg/).

1. To use flows, you must have two different roles:

   1. **User role** – The IAM role that you use to log into the AWS Management Console or to make API calls must have permissions to carry out flows-related actions.

      If your role has the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) policy attached, you don't need to configure additional permissions for this role. To restrict a role's permissions to only actions that are used for flows, attach the following identity-based policy to the IAM role:

------
#### [ JSON ]

****  

      ```
      {
          "Version":"2012-10-17",		 	 	 
          "Statement": [
              {
                  "Sid": "FlowPermissions",
                  "Effect": "Allow",
                  "Action": [  
                      "bedrock:CreateFlow",
                      "bedrock:UpdateFlow",
                      "bedrock:GetFlow",
                      "bedrock:ListFlows", 
                      "bedrock:DeleteFlow",
                      "bedrock:ValidateFlowDefinition", 
                      "bedrock:CreateFlowVersion",
                      "bedrock:GetFlowVersion",
                      "bedrock:ListFlowVersions",
                      "bedrock:DeleteFlowVersion",
                      "bedrock:CreateFlowAlias",
                      "bedrock:UpdateFlowAlias",
                      "bedrock:GetFlowAlias",
                      "bedrock:ListFlowAliases",
                      "bedrock:DeleteFlowAlias",
                      "bedrock:InvokeFlow",
                      "bedrock:TagResource",
                      "bedrock:UntagResource", 
                      "bedrock:ListTagsForResource"
                  ],
                  "Resource": "*"
              }
          ]   
      }
      ```

------

      You can further restrict permissions by omitting [actions](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-actions) or specifying [resources](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-resources) and [condition keys](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-conditionkeys). An IAM identity can call API operations on specific resources. If you specify an API operation that can't be used on the resource specified in the policy, Amazon Bedrock returns an error.

   1. **Service role** – A role that allows Amazon Bedrock to perform actions on your behalf. You must specify this role when creating or updating a flow. You can create a [custom AWS Identity and Access Management [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role)](flows-permissions.md).
**Note**  
If you plan to use the Amazon Bedrock console to automatically create a role when you create a flow, you don't need to manually set up this role.