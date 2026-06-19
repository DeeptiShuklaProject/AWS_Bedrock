

# Prerequisites for inference profiles
<a name="inference-profiles-prereq"></a>

Before you can use an inference profile, check that you've fulfilled the following prerequisites:
+ Your role has access to the inference profile API actions. If your role has the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) AWS-managed policy attached, you can skip this step. Otherwise, do the following:

  1. Follow the steps at [Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) and create the following policy, which allows a role to do inference profile-related actions and run model inference using all foundation models and inference profiles.

------
#### [ JSON ]

****  

     ```
     {
         "Version":"2012-10-17",		 	 	 
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "bedrock:InvokeModel*",
                     "bedrock:CreateInferenceProfile"
                 ],
                 "Resource": [
                     "arn:aws:bedrock:*::foundation-model/*",
                     "arn:aws:bedrock:*:*:inference-profile/*",
                     "arn:aws:bedrock:*:*:application-inference-profile/*"
                 ]
             },
             {
                 "Effect": "Allow",
                 "Action": [
                     "bedrock:GetInferenceProfile",
                     "bedrock:ListInferenceProfiles",
                     "bedrock:DeleteInferenceProfile",
                     "bedrock:TagResource",
                     "bedrock:UntagResource",
                     "bedrock:ListTagsForResource"
                 ],
                 "Resource": [
                     "arn:aws:bedrock:*:*:inference-profile/*",
                     "arn:aws:bedrock:*:*:application-inference-profile/*"
                 ]
             }
         ]
     }
     ```

------

     (Optional) You can restrict the role's access in the following ways:
     + To restrict the API actions that the role can make, modify the list in the `Action` field to contain only the [API operations](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) that you want to allow access to.
     + To restrict the role's access to specific inference profiles, modify the `Resource` list to contain only the [inference profiles](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-resources-for-iam-policies) and foundation models that you want to allow access to. System-defined inference profiles begin with `inference-profile` and application inference profiles begin with `application-inference-profile`.
**Important**  
When you specify an inference profile in the `Resource` field in the first statement, you must also specify the foundation model in each Region associated with it.
     + To restrict user access such that they can invoke a foundation model only through an inference profile, add a `Condition` field and use the `aws:InferenceProfileArn` [condition key](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys). Specify the inference profile that you want to filter access on. This condition can be included in a statement that scopes to the `foundation-model` resources.
     + For example, you can attach the following policy to a role to allow it to invoke the Anthropic Claude 3 Haiku model only through the US Anthropic Claude 3 Haiku inference profile in the account {{111122223333}} in us-west-2:

------
#### [ JSON ]

****  

       ```
       {
           "Version":"2012-10-17",		 	 	 
           "Statement": [
               {
                   "Effect": "Allow",
                   "Action": [
                       "bedrock:InvokeModel*"
                   ],
                   "Resource": [
                       "arn:aws:bedrock:us-west-2:{{111122223333}}:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"
                   ]
               },
               {
                   "Effect": "Allow",
                   "Action": [
                       "bedrock:InvokeModel*"
                   ],
                   "Resource": [
                       "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                       "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
                   ],
                   "Condition": {
                       "StringLike": {
                           "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-west-2:{{111122223333}}:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"
                       }
                   }
               }
           ]
       }
       ```

------
     + For example, you can attach the following policy to a role to allow it to invoke the Anthropic Claude Sonnet 4 model only through the Global Claude Sonnet 4 inference profile in the account 111122223333 in us-east-2 (US East (Ohio)).

------
#### [ JSON ]

****  

       ```
       {
           "Version":"2012-10-17",		 	 	 
           "Statement": [
               {
                   "Effect": "Allow",
                   "Action": [
                       "bedrock:InvokeModel*"
                   ],
                   "Resource": [
                       "arn:aws:bedrock:us-east-2:111122223333:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0"
                   ]
               },
               {
                   "Effect": "Allow",
                   "Action": [
                       "bedrock:InvokeModel*"
                   ],
                   "Resource": [
                       "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-sonnet-4-20250514-v1:0",
                       "arn:aws:bedrock:::foundation-model/anthropic.claude-sonnet-4-20250514-v1:0"
                   ],
                   "Condition": {
                       "StringLike": {
                           "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-east-2:111122223333:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0"
                       }
                   }
               }
           ]
       }
       ```

------
     + You can also restrict the use of the Global Claude Sonnet 4 inference profile by adding an explicit Deny with a `StringEquals` condition that checks the request context key `aws:RequestedRegion` equals unspecified. Because it matches `StringEquals`, the Deny overrides any Allow and blocks Global routing of inference requests.

       ```
       {
           "Effect": "Deny",
           "Action": [
               "bedrock:InvokeModel*"
           ],
           "Resource": "*",
           "Condition": {
               "StringEquals": {
                   "aws:RequestedRegion": "unspecified"
               }
           }
       },
       ```

  1. Follow the steps at [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) to attach the policy to a role to grant the role permissions to view and use all the inference profiles.
+ You've requested access to the model defined in the inference profile that you want to use, in the Region from which you want to call the inference profile.