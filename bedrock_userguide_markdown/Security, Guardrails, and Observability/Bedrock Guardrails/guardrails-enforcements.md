

# Apply cross-account safeguards with Amazon Bedrock Guardrails enforcements
<a name="guardrails-enforcements"></a>

Amazon Bedrock Guardrails allows you to automatically apply safeguards across multiple accounts in an organization through [AWS Organizations Amazon Bedrock policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_bedrock.html). This enables uniform protection across all accounts with centralized control and management. Additionally, this capability also offers flexibility to apply account-level and application-specific controls depending on use-case requirements.

**Key capabilities**

The following are the key capabilities of guardrails enforcements:
+ **Organization-level enforcement** – Apply guardrails for all model invocations with Amazon Bedrock across organization units (OUs), individual accounts, or your entire organization using Amazon Bedrock policies with AWS Organizations.
+ **Account-level enforcement** – Designate a particular version of a guardrail within an AWS account for all Amazon Bedrock model invocations from that account.
+ **Layered protection** – Combine organization and application-specific guardrails when both are present. The effective safety control will be a union of both guardrails with the most restrictive controls taking precedence in case of the same control from both guardrails.

The following topics describe how to use Amazon Bedrock Guardrails enforcements:

**Topics**
+ [Implementation guide](#guardrails-enforcements-implementation-guide)
+ [Monitoring](#guardrails-monitoring)
+ [Pricing](#pricing)
+ [Frequently Asked Questions](#faq)

## Implementation guide
<a name="guardrails-enforcements-implementation-guide"></a>

The steps below provide details on implementing guardrails enforcements for accounts within an AWS Organization and for a single AWS account. With these enforcements, all model invocations to Amazon Bedrock will enforce the safeguards configured within the designated guardrail.

### Organization-level enforcement
<a name="organization-level-enforcement"></a>

This section details setting up guardrail enforcement across your AWS organization. Once set up, you'll have a guardrail that automatically applies to all Amazon Bedrock model invocations across specified accounts or OUs.

**Prerequisites**  
AWS Organization administrators (with management account access) with permissions to create guardrails and manage AWS Organizations policies.

**What you'll need**

The following are required:
+ [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html) with management account access
+ [IAM permissions](guardrails-permissions.md#guardrails-permissions-use) to create guardrails and [manage AWS Organizations policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_permissions_overview.html)
+ Understanding of your organization's safety requirements<a name="org-level-enforcement-steps"></a>

**To set up organization-level guardrail enforcement**

1. <a name="plan-guardrail-config"></a>

**Plan your guardrail configuration**

   1. Define your safeguards:
      + Review available guardrail filters in the [Amazon Bedrock Guardrails documentation](guardrails.md)
      + Identify which filter you need. Currently, content filters, denied topics, word filters, sensitive information filters, contextual grounding checks are supported.
      + 
**Important**  
Do not include the automated reasoning policy, as it is unsupported for guardrail enforcements and will cause runtime failures.

   1. Identify target accounts:
      + Determine which OUs, accounts, or your entire organization will have this guardrail enforced

1. <a name="create-guardrail-mgmt-account"></a>

**Create your guardrail in the management account**

   Create a guardrail in every region where you want to enforce it with one of the following methods:
   + Using the AWS Management Console:

     1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

     1. In the left navigation panel, choose **Guardrails**

     1. Choose **Create guardrail**

     1. Follow the wizard to configure your desired filters or safeguards (content filters, denied topics, word filters, sensitive information filters, contextual grounding checks)

     1. Do not enable the automated reasoning policy

     1. Complete the wizard to create your guardrail
   + Using the API: Use the [CreateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateGuardrail.html) API

**Verify**  
Once created, you should see it in the list of guardrails on the Guardrails landing page or search for it in the list of guardrails using the guardrail name

1. <a name="create-guardrail-version"></a>

**Create a guardrail version**

   Create a numeric version to ensure the guardrail configuration remains immutable and cannot be modified by member accounts.
   + Using the AWS Management Console:

     1. Select the guardrail created in the previous step in the Guardrails page on the Amazon Bedrock console

     1. Choose **Create version**

     1. Note the guardrail ARN and the version number (for example, "1", "2")
   + Using the API: Use the [CreateGuardrailVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateGuardrailVersion.html) API

**Verify**  
Confirm the version was created successfully by checking the list of versions on the Guardrail detail page.

1. <a name="attach-resource-policy"></a>

**Attach a resource-based policy**

   Enable cross-account access by attaching a resource-based policy to your guardrail.
   + Using the AWS Management Console – To attach a resource-based policy using the console:

     1. In the Amazon Bedrock Guardrails console, select your guardrail

     1. Choose **Add** to add a resource-based policy

     1. Add a policy that grants `bedrock:ApplyGuardrail` permission to all the member accounts or organization. See [Share guardrail with your organization](guardrails-resource-based-policies.md#share-guardrail-with-organization) in [Using resource-based policies for guardrails](guardrails-resource-based-policies.md).

     1. Save the policy

**Verify**  
Test access from a member account using the [ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ApplyGuardrail.html) API to ensure authorization is configured correctly.

1. <a name="configure-iam-permissions"></a>

**Configure IAM permissions in member accounts**

   Ensure all roles in member accounts have IAM permissions to access the enforced guardrail.

**Required permissions**  
Member account roles need `bedrock:ApplyGuardrail` permission for the management account's guardrail. See [Set up permissions to use Amazon Bedrock Guardrails](guardrails-permissions.md) for detailed IAM policy examples

**Verify**  
Confirm that roles with scoped down permissions in member accounts can successfully call the `ApplyGuardrail` API with the guardrail.

1. <a name="enable-bedrock-policy-type"></a>

**Enable the Amazon Bedrock Policy Type in AWS Organizations**
   + Using the AWS Management Console – To enable the Amazon Bedrock policy type using the console:

     1. Navigate to the AWS Organizations console

     1. Choose **Policies**

     1. Choose **Amazon Bedrock policies**

     1. Choose **Enable Amazon Bedrock policies** to enable the Amazon Bedrock policy type for your organization
   + Using the API – Use the AWS Organizations [EnablePolicyType](https://docs.aws.amazon.com/organizations/latest/APIReference/API_EnablePolicyType.html) API with policy type `BEDROCK_POLICY`

**Verify**  
Confirm the Amazon Bedrock policy type shows as enabled in the AWS Organizations console.

1. <a name="create-attach-organizations-policy"></a>

**Create and attach an AWS Organizations policy**

   Create a management policy that specifies your guardrail and attach it to your target accounts or OUs.
   + Using the AWS Management Console – To create and attach an AWS Organizations policy using the console:

     1. In the AWS Organizations console, navigate to **Policies** > **Amazon Bedrock policies**

     1. Choose **Create policy**

     1. Specify your guardrail ARN and version
**Important**  
Ensure you are specifying the accurate guardrail ARN in the policy. Specifying an incorrect or invalid ARN will result in policy violations, non-enforcement of safeguards, and the inability to use the models in Amazon Bedrock for inference.

     1. Configure selective content guarding controls (optional).
        + Amazon Bedrock APIs allow callers to [tag specific content within their input prompts](guardrails-tagging.md) for guardrail evaluation.
        + Selective content guarding controls let administrators decide whether to honor tagging decisions made by API callers.
        + The `system` and `messages` controls determine how system prompts and message content are processed by guardrails. Each accepts one of the following values:
          + **Selective**: Only evaluate content within guard content tags. When no tags are specified, the behavior depends on the control. For `system`, no content is evaluated, and for `messages`, all content is evaluated.
          + **Comprehensive**: Evaluate all content, regardless of guard content tags.
        + If not configured, both controls default to **Comprehensive**.

        ```
        {
            "bedrock": {
                "guardrail_inference": {
                    "us-east-1": {
                        "config_1": {
                            "identifier": {
                                "@@assign": "arn:aws:bedrock:us-east-1:123456789012:guardrail/guardrail-id:1"
                            },
                            "selective_content_guarding": {
                                "system": {
                                    "@@assign": "selective"
                                },
                                "messages": {
                                    "@@assign": "comprehensive"
                                }
                            },
                            "model_enforcement": {
                                "included_models": {
                                    "@@assign": ["ALL"]
                                },
                                "excluded_models": {
                                    "@@assign": ["amazon.titan-embed-text-v2:0", "cohere.embed-english-v3"]
                                }
                            }
                        }
                    }
                }
            }
        }
        ```

     1. Save the policy

     1. Attach the policy to your desired targets (organization root, OUs, or individual accounts) by navigating to the **Targets** tab and choosing **Attach**
   + Using the API – Use the AWS Organizations [CreatePolicy](https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreatePolicy.html) API with policy type `BEDROCK_POLICY`. Use [AttachPolicy](https://docs.aws.amazon.com/organizations/latest/APIReference/API_AttachPolicy.html) to attach to targets

   Learn more: [Amazon Bedrock policies in AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_bedrock.html)

**Verify**  
Check that the policy is attached to the correct targets in the AWS Organizations console.

1. <a name="test-verify-org-enforcement"></a>

**Test and verify enforcement**

   Test that the guardrail is being enforced on member accounts.

**Verify which guardrail is enforced**
   + Using the AWS Management Console – From a member account, navigate to the Amazon Bedrock console, choose **Guardrails** in the left navigation panel. On the Guardrails home page, you should see the organization enforced guardrail under the section **Organization-level enforcement configurations** in the management account and **Organization-level enforced guardrails** in the member account
   + Using the API – From a member account, call [DescribeEffectivePolicy](https://docs.aws.amazon.com/organizations/latest/APIReference/API_DescribeEffectivePolicy.html) with your member account ID as the target ID

**Test from a member account**

   1. Make a Amazon Bedrock inference call using [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), or [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html).

   1. The enforced guardrail should automatically apply to both inputs and outputs

   1. Check the response for guardrail assessment information. The guardrail response will include enforced guardrail information.

### Account-level enforcement
<a name="account-level-enforcement"></a>

This section details setting up guardrail enforcement within a single AWS account. Once set up, you'll have a guardrail that automatically applies to all Amazon Bedrock model invocations in your account.

**Prerequisites**  
AWS account administrators with permissions to create guardrails and configure account-level settings.

**What you'll need**  
The following are required:
+ An AWS account with appropriate IAM permissions
+ Understanding of your account's safety requirements<a name="account-level-enforcement-steps"></a>

**To set up account-level guardrail enforcement**

1. <a name="plan-account-guardrail-config"></a>

**Plan your guardrail configuration**

**Define your safeguards**  
To define your safeguards:
   + Review available guardrail filters in the [Amazon Bedrock Guardrails documentation](guardrails.md)
   + Identify which filter you need. Currently, content filters, denied topics, word filters, sensitive information filters, contextual grounding checks are supported.
   + 
**Important**  
Do not include the automated reasoning policy, as it is unsupported for guardrail enforcements and will cause runtime failures

1. <a name="create-account-guardrail"></a>

**Create your guardrail**

   Create a guardrail in every region where you want to enforce it.

**Via AWS Management Console**  
To create a guardrail using the console:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. In the left navigation panel, choose **Guardrails**

   1. Choose **Create guardrail**

   1. Follow the wizard to configure your desired policies (content filters, denied topics, word filters, sensitive information filters)

   1. Do not enable the automated reasoning policy

   1. Complete the wizard to create your guardrail

**Via API**  
Use the `CreateGuardrail` API

**Verify**  
Once created, you should see it in the list of guardrails on the Guardrails landing page or search for it in the list of guardrails using the guardrail name

1. <a name="create-account-guardrail-version"></a>

**Create a guardrail version**

   Create a numeric version to ensure the guardrail configuration remains immutable and cannot be modified by member accounts.

**Via AWS Management Console**  
To create a guardrail version using the console:

   1. Select the guardrail created in the previous step in the Guardrails page on the Amazon Bedrock console

   1. Choose **Create version**

   1. Note the guardrail ARN and the version number (for example, "1", "2")

**Via API**  
Use the `CreateGuardrailVersion` API

**Verify**  
Confirm the version was created successfully by checking the list of versions on the Guardrail detail page.

1. <a name="attach-account-resource-policy"></a>

**Attach a resource-based policy (optional)**

   If you want to share the guardrail with specific roles in your account, attach a resource-based policy.

**Via AWS Management Console**  
To attach a resource-based policy using the console:

   1. In the Amazon Bedrock Guardrails console, select your guardrail

   1. Choose **Add** to add a resource-based policy

   1. Add a policy that grants `bedrock:ApplyGuardrail` permission to the desired roles

   1. Save the policy

1. <a name="enable-account-enforcement"></a>

**Enable account-level enforcement**

   Configure the account to use your guardrail for all Amazon Bedrock invocations. This must be done in every region where you want enforcement.

**Via AWS Management Console**  
To enable account-level enforcement using the console:

   1. Navigate to the Amazon Bedrock console

   1. Choose **Guardrails** in the left navigation panel

   1. Under the **Account-level enforcement configurations** section, choose **Add**

   1. Select your guardrail and version

   1. Configure selective content guarding controls (optional).
      + Amazon Bedrock APIs allow callers to [tag specific content within their input prompts](guardrails-tagging.md) for guardrail evaluation.
      + Selective content guarding controls let administrators decide whether to honor tagging decisions made by API callers.
      + The `system` and `messages` controls determine how system prompts and message content are processed by guardrails. Each accepts one of the following values:
        + **Selective**: Only evaluate content within guard content tags.
        + **Comprehensive**: Evaluate all content, regardless of guard content tags.
      + If not configured, both controls default to **Comprehensive**.

   1. Submit the configuration

   1. Repeat for each region where you want enforcement

**Via API**  
Use the `PutEnforcedGuardrailConfiguration` API in every region where you want to enforce the guardrail

**Verify**  
You should see the account enforced guardrail under the section **Account enforced guardrail configuration** on the Guardrails page. You can call [ListEnforcedGuardrailsConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListEnforcedGuardrailsConfiguration.html) API to ensure that the enforced guardrail is listed

1. <a name="test-verify-account-enforcement"></a>

**Test and verify enforcement**

**Test using a role in your account**  
To test enforcement from your account:

   1. Make a Amazon Bedrock inference call using `InvokeModel`, `Converse`, `InvokeModelWithResponseStream`, or `ConverseStream`

   1. The account-enforced guardrail should automatically apply to both inputs and outputs

   1. Check the response for guardrail assessment information. The guardrail response will include enforced guardrail information.

## Monitoring
<a name="guardrails-monitoring"></a>
+ Track guardrail interventions and metrics using [CloudWatch metrics for Amazon Bedrock Guardrails](monitoring-guardrails-cw-metrics.md)
+ Review CloudTrail logs for `ApplyGuardrail` API calls to monitor usage patterns such as AccessDenied exceptions indicating IAM permission configuration issues. See [Amazon Bedrock data events in CloudTrail](logging-using-cloudtrail.md#service-name-data-events-cloudtrail)

## Pricing
<a name="pricing"></a>

Amazon Bedrock Guardrails enforcement follows the current pricing model for Amazon Bedrock Guardrails based on the number of text units consumed per configured safeguard. Charges apply to each enforced guardrail according to its configured safeguards. For detailed pricing information on individual safeguards, refer to [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/).

## Frequently Asked Questions
<a name="faq"></a>

**How is consumption towards quotas calculated when enforced guardrails apply?**  
Consumption will be calculated per guardrail ARN associated with each request and will be counted towards the AWS account making the API call. For example: an `ApplyGuardrail` call with 1000 characters of text and 3 guardrails would generate 3 text units of consumption per guardrail per safeguard in the guardrail.  
Member account calls using the Amazon Bedrock Policy will count towards the Service Quotas for the member account. Review the Service Quotas Console or [Service Quotas documentation](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) and be sure that your Guardrails runtime limits are sufficient for your call volume.

**What happens if I have both organization-level and account-level enforced guardrails as well as a guardrail in my request?**  
All 3 guardrails will be enforced at runtime. The net effect is a union of all guardrails, with the most restrictive control taking precedence.

**When should I use selective or comprehensive guarding control?**  
Use **Selective** when you trust callers to tag the right content and want to reduce unnecessary guardrail processing. This is useful when callers handle a mix of pre-validated and user-generated content, and only need guardrails applied to specific portions. Use **Comprehensive** when you want to enforce guardrails on everything, regardless of what the caller tags. This is the safer default when you don't want to rely on callers to correctly identify sensitive content.

**How can I include or exclude certain models from enforcement?**  
Use the model enforcement control to scope which models on Amazon Bedrock a guardrail applies to for inference. If not configured, enforcement applies to all models on Amazon Bedrock by default. This control accepts the following lists:  
+ **Included models:** Models to enforce the guardrail on. Accepts specific model identifiers or the keyword `ALL` to explicitly include all models. When empty, enforcement applies to all models.
+ **Excluded models:** Models to exclude from guardrail enforcement. When empty, no models are excluded.
If a model appears in both lists, it is excluded.

**When should I use include versus exclude models?**  
+ Use **Included models** when you want to enforce the guardrail on only specific models.
+ Use **Excluded models** when you want broad enforcement but need to carve out exceptions for specific models.

**Can I delete a guardrail that's being used in an enforcement configuration?**  
No. By default, the [DeleteGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeleteGuardrail.html) API prevents deletion of guardrails associated with account-level or organization-level enforcement configurations.