

# Prerequisites
<a name="inline-agent-prereq"></a>

**Note**  
Configuring and invoking an inline agent feature is in preview release for Amazon Bedrock and is subject to change.

Complete the following prerequisites before you invoke your inline agent:

1. Decide on the foundation model you want to use for configuring your inline agent, Region where you want to invoke the agent, and an instruction that tells the inline agent what it should do. 

1. Create or prepare one or more of the following Amazon Bedrock agent properties you want to use for your inline agent.   
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/inline-agent-prereq.html)

1. Create a AWS Identity and Access Management (IAM) role and attach the policy mentioned in this step to the role. 

   Before you can invoke an inline agent, you must create an IAM role that provides the necessary permissions for using the `InvokeInlineAgent` API and to access resources like Lambda functions, knowledge bases, and foundation models. 

   Create a custom service role for your inline agent by following steps at [Creating a role to delegate permissions to an IAM user](https://docs.aws.amazon.com//bedrock/latest/userguide/getting-started.html). After you create the IAM role, attach the following policy to the role.
**Note**  
As a best practice for security purposes, replace the {{${region}}}, {{${account-id}}}, and {{\*.ids}} with Region, your account id, and specific resource ids. after you have created them.

   ```
   {
       "Version": "2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "InvokeInlineAgent",
               "Effect": "Allow",
               "Action": "bedrock:InvokeInlineAgent",
               "Resource": "*"
           },
           {
               "Sid": "InvokeFoundationModel",
               "Effect": "Allow",
               "Action": "bedrock:InvokeModel",
               "Resource": "arn:aws:bedrock:{{region}}::foundation-model/{{model-id}}"
           },
           {
               "Sid": "KnowledgeBaseAccess",
               "Effect": "Allow",
               "Action": [
                   "bedrock:Retrieve",
                   "bedrock:RetrieveAndGenerate"
               ],
               "Resource": "arn:aws:bedrock:{{region}}:{{account-id}}:knowledge-base/{{knowledge-base-id}}"
           },
           {
               "Sid": "GuardrailAccess",
               "Effect": "Allow",
               "Action": "bedrock:ApplyGuardrail",
               "Resource": "arn:aws:bedrock:{{region}}:{{account-id}}:guardrail/{{guardrail-id}}"
           },
           {
               "Sid": "LambdaInvoke",
               "Effect": "Allow",
               "Action": "lambda:InvokeFunction",
               "Resource": "arn:aws:lambda:{{region}}:{{account-id}}:function:{{function-name}}"
           },
           {
               "Sid": "S3AccessForKBAndActions",
               "Effect": "Allow",
               "Action": [
                   "s3:GetObject",
                   "s3:GetObjectMetadata"
               ],
               "Resource": "arn:aws:s3:::{{bucket-name}}/*"
           },
           {
               "Sid": "S3AccessForCodeInterpreter",
               "Effect": "Allow",
               "Action": [
                   "s3:GetObjectVersion",
                   "s3:GetObjectVersionAttributes",
                   "s3:GetObjectAttributes"
               ],
               "Resource": "arn:aws:s3:::{{bucket-name}}/{{path/to/file}}"
           },
           {
               "Sid": "KMSAccess",
               "Effect": "Allow",
               "Action": [
                   "kms:GenerateDataKey*",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:{{region}}:{{account-id}}:key/{{key-id}}"
           }
       ]
   }
   ```