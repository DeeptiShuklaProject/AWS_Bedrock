

# Service roles
<a name="security-iam-sr"></a>

Amazon Bedrock uses [IAM service roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) for some features to let Amazon Bedrock carry out tasks on your behalf.

The console automatically creates service roles for supported features.

You can also create a custom service role and customize the attached permissions to your specific use-case. If you use the console, you can select this role instead of letting Amazon Bedrock create one for you.

To set up the custom service role, you carry out the following general steps.

1. Create the role by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

1. Attach a **trust policy**.

1. Attach the relevant **identity-based permissions**.

**Important**  
When setting the `iam:PassRole` permission, make sure that a user can't pass a role where the role has more permissions than you want the user to have. For example, Alice might not be allowed to perform `bedrock:InvokeModel` on a custom model. If Alice can pass a role to Amazon Bedrock to create an evaluation of that custom model, the service could invoke that model on behalf of Alice while running the job.

Refer to the following links for more information about IAM concepts that are relevant to setting service role permissions.
+ [AWS service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role)
+ [Identity-based policies and resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html)
+ [Using resource-based policies for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html)
+ [AWS global condition context keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
+ [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)

Select a topic to learn more about service roles for a specific feature.

**Topics**
+ [Create a custom service role for batch inference](batch-iam-sr.md)
+ [Create a service role for model customization](model-customization-iam-role.md)
+ [Create a service role for importing pre-trained models](model-import-iam-role.md)
+ [Create a service role for Amazon Bedrock Agents](agents-permissions.md)
+ [Create a service role for Amazon Bedrock Knowledge Bases](kb-permissions.md)
+ [Create a service role for Amazon Bedrock Flows in Amazon Bedrock](flows-permissions.md)
+ [Service role requirements for model evaluation jobs](model-evaluation-security-service-roles.md)