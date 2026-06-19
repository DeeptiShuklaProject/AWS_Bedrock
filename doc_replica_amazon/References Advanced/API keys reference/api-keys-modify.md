

# Modify permissions for long-term and short-term Amazon Bedrock API keys
<a name="api-keys-modify"></a>

When you generate a long-term Amazon Bedrock API key, you create an IAM user associated with the key. To change the permissions associated with the key, modify permissions for the IAM user through the IAM service. For more information, see [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the IAM User Guide.

**Note**  
If you generated the long-term key in the AWS Management Console, the [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) is attached to it by default. If you plan to modify permissions, remove this policy first before setting custom permissions.

## Example of modifying permissions for API keys
<a name="api-keys-modify-example"></a>

The following procedure shows how you can replace the [AmazonBedrockLimitedAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockLimitedAccess) with a more restrictive one:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, select **API keys**.

1. Select the **Long-term API keys** tab.

1. Select your API key and choose **Manage in IAM Console**.

1. Select the **Permissions** tab, choose the **AmazonBedrockLimitedAccess** policy, and choose **Remove**.
**Note**  
At this point, you've removed all permissions from the APi key and you won't be able to do anything with it.

1. In the **Permissions policies** section, select **Create inline policy** from the **Add permissions** dropdown.

1. In the **Policy editor**, select **JSON**. Then paste the following policy into the editor:

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
                   "bedrock:CallWithBearerToken"
               ],
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "bedrock:InvokeModel*"
               ],
               "Resource": [
                   "arn:aws:bedrock:us-west-2:111122223333:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"
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
                       "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-west-2:111122223333:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"
                   }
               }
           }
       ]
   }
   ```

------

1. Choose **Next**, provide a **Policy name**, and then choose **Create policy**.

1. With this API key, a user now can only run inference with the US Anthropic Claude Sonnet 4.6 inference profile in US West (Oregon).