

# Amazon Quick integration with managed knowledge bases
<a name="kb-managed-byo-fmkb"></a>

You can connect a managed Amazon Bedrock knowledge base to Amazon Quick as a knowledge source. Amazon Quick uses the provided IAM actions on your knowledge base to pull data from your index. You can connect up to 2 managed knowledge bases per Amazon Quick instance. Access control list (ACL)-enabled connectors are supported — Amazon Quick automatically passes the user's identity for document-level access control.

## Prerequisites
<a name="kb-managed-byo-fmkb-requirements"></a>
+ Administrator-level permissions in Amazon Quick to manage AWS resource integrations.
+ A managed Amazon Bedrock knowledge base.
+ The knowledge base and Amazon Quick instance must be in the same AWS Region.
+ For cross-account access: the ability to attach a resource policy to the knowledge base, or coordination with the knowledge base owner to attach the policy.

## Connect a managed knowledge base to Amazon Quick
<a name="kb-managed-byo-fmkb-setup"></a>

To connect your managed knowledge base to Amazon Quick, complete the following steps.

**To connect a managed knowledge base to Amazon Quick**

1. **Create the managed knowledge base.** In the knowledge base owner account, create a managed knowledge base. See [Create a managed knowledge base](kb-managed-create.md).

   Note the knowledge base ARN. The ARN format is:

   ```
   arn:aws:bedrock:{{REGION}}:{{ACCOUNT_ID}}:knowledge-base/{{KB_ID}}
   ```

   You can find the ARN in the Amazon Bedrock console on the knowledge base details page, or by calling the `GetKnowledgeBase` API.

1. **(Optional) Grant Quick cross-account access.** Skip this step if the knowledge base and your Amazon Quick instance are in the same AWS account. Same-account setups do not need a resource policy.

   In the knowledge base owner account, attach a resource policy to the knowledge base granting your Amazon Quick service role `bedrock:Retrieve` and `bedrock:GetDocumentContent`:

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::{{QUICK_ACCOUNT_ID}}:role/{{quick-service-role}}"
               },
               "Action": [
                   "bedrock:Retrieve",
                   "bedrock:GetDocumentContent"
               ],
               "Resource": "arn:aws:bedrock:{{REGION}}:{{KB_OWNER_ACCOUNT_ID}}:knowledge-base/{{KB_ID}}"
           }
       ]
   }
   ```

   To grant access to multiple Quick instances, list each role ARN in `Principal.AWS` as an array.

   For more information about managing resource policies, see [Resource policies for managed knowledge bases](kb-managed-cross-account.md).

1. **Connect the knowledge base in Amazon Quick.**
   + Add the knowledge base ARN under **Admin** > **AWS Resources**. Amazon Quick automatically creates and attaches the `AWSQuickSightBedrockAccess` managed IAM policy to the Quick service role, scoped to the entered ARN.
   + Create a knowledge base under **Integrations**, selecting **Bedrock knowledge base** as the data source type.

   After connection completes, add the knowledge base to spaces. Amazon Quick automatically queries the knowledge base during chat.

## Related documentation
<a name="kb-managed-byo-fmkb-more-info"></a>

For detailed setup instructions, permissions configuration, monitoring, and troubleshooting, see [Bring Your Own Bedrock Managed Knowledge Base](https://docs.aws.amazon.com/quick/latest/userguide/quick-byo-bedrock-kb.html) in the *Amazon Quick User Guide*.