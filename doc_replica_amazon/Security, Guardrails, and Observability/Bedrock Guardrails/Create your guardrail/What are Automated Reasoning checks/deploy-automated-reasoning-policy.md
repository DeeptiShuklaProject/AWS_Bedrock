

# Deploy your Automated Reasoning policy in your application
<a name="deploy-automated-reasoning-policy"></a>

After you've tested your Automated Reasoning policy and are satisfied with its performance, you can deploy it for use in your application with Amazon Bedrock Guardrails. This page covers the full deployment workflow: saving an immutable version, attaching it to a guardrail, automating deployment with CloudFormation, and integrating into CI/CD pipelines.

## Save a version of your Automated Reasoning policy
<a name="save-policy-version"></a>

When you're done testing your policy, create an immutable version. Immutable versions ensure that the policy attached to your guardrail doesn't change unexpectedly when you continue editing the DRAFT. Each version is identified by a numeric version number (1, 2, 3, ...) and cannot be modified after creation.

### Using the console
<a name="save-policy-version-console"></a>

1. In the left navigation, choose **Automated Reasoning**.

1. Choose the Automated Reasoning policy that you want to use with your application.

1. Choose **Save as new version**. You can use this version of your policy with your guardrail.

### Using the API
<a name="save-policy-version-api"></a>

Use the `CreateAutomatedReasoningPolicyVersion` API to create an immutable version of your Automated Reasoning policy.

#### Request parameters
<a name="save-policy-version-api-request"></a>

`policyArn` (required)  
The Amazon Resource Name (ARN) of the Automated Reasoning policy for which to create a version.

`lastUpdatedDefinitionHash` (required)  
The hash of the policy definition for the new version. Retrieve this hash from the `GetAutomatedReasoningPolicy` API. This ensures you're versioning the exact policy definition you tested.

#### Example
<a name="save-policy-version-api-example"></a>

```
# Get the current definition hash
aws bedrock get-automated-reasoning-policy \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --query "definitionHash" --output text

# Create the version
aws bedrock create-automated-reasoning-policy-version \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}" \
  --last-updated-definition-hash "{{583463f067a8a4f49fc1206b4642fd40...}}"
```

Example response:

```
{
  "policyArn": "arn:aws:bedrock:us-east-1:111122223333:automated-reasoning-policy/lnq5hhz70wgk",
  "version": "1",
  "name": "MyHRPolicy"
}
```

## Add your Automated Reasoning policy to your guardrail
<a name="add-policy-to-guardrail"></a>

Once you have a saved version of your Automated Reasoning policy, add it to a guardrail. The guardrail is the runtime component that your application calls to validate LLM responses. You can add an Automated Reasoning policy to a new or existing guardrail.

### Using the console
<a name="add-policy-to-guardrail-console"></a>

1. In the left navigation, choose **Guardrails**, then choose **Create guardrail** (or select an existing guardrail and choose **Edit**).

1. When you get to the **Add Automated Reasoning checks** screen, choose **Enable Automated Reasoning policy**.

1. For **Policy name**, choose a saved version of an Automated Reasoning policy, then choose **Next**.

1. Finish creating or updating your guardrail.

### Using the API
<a name="add-policy-to-guardrail-api"></a>

Use the `CreateGuardrail` or `UpdateGuardrail` API to add an Automated Reasoning policy to your guardrail. Include the `automatedReasoningConfig` parameter with the versioned policy ARN.

#### Request parameters
<a name="add-policy-to-guardrail-api-request"></a>

`automatedReasoningConfig`  
The configuration for Automated Reasoning checks in Amazon Bedrock Guardrails.

`policyArn` (required)  
The ARN of the Automated Reasoning policy version to use with your guardrail. Use the versioned ARN (ending in `:1`, `:2`, etc.), not the unversioned ARN.

#### Example
<a name="add-policy-to-guardrail-api-example"></a>

```
aws bedrock create-guardrail \
  --name "{{HR-Policy-Guardrail}}" \
  --description "{{Guardrail for HR policy validation}}" \
  --automated-reasoning-policy-config policies="arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}:{{1}}" \
  --cross-region-config '{"guardrailProfileIdentifier": "{{us}}.guardrail.v1:0"}' \
  --blocked-input-messaging "I cannot process this request." \
  --blocked-outputs-messaging "I cannot provide this response."
```

**Important**  
Use the versioned policy ARN (for example, `arn:aws:bedrock:us-east-1:111122223333:automated-reasoning-policy/lnq5hhz70wgk:1`). If you use the unversioned ARN, the API returns an error. Create a version first using `CreateAutomatedReasoningPolicyVersion`.

**Important**  
Guardrails that use Automated Reasoning checks require a cross-Region inference profile. Include the `--cross-region-config` parameter with a `guardrailProfileIdentifier` that matches your Region prefix (for example, `us.guardrail.v1:0` for US Regions or `eu.guardrail.v1:0` for EU Regions). If you omit this parameter, the API returns a `ValidationException`.

## Export a policy version for deployment
<a name="export-policy-version"></a>

To deploy a policy through CloudFormation or a CI/CD pipeline, you need the policy definition JSON. Use the `ExportAutomatedReasoningPolicyVersion` API to export the complete policy definition — including all rules, variables, and custom types — from a saved version.

The exported definition is the same format accepted by the CloudFormation `AWS::Bedrock::AutomatedReasoningPolicy` resource's `PolicyDefinition` property. This makes it straightforward to move a policy from the interactive console workflow to automated deployment.

```
# Export the policy definition from version 1
aws bedrock export-automated-reasoning-policy-version \
  --policy-arn "arn:aws:bedrock:{{us-east-1}}:{{111122223333}}:automated-reasoning-policy/{{lnq5hhz70wgk}}:{{1}}" \
  --query "policyDefinition" \
  --output json > {{policy-definition.json}}
```

The exported JSON contains the following structure:

```
{
  "version": "1.0",
  "variables": [
    {
      "name": "isFullTime",
      "type": "BOOL",
      "description": "Whether the employee works full-time (true) or part-time (false)."
    },
    {
      "name": "tenureMonths",
      "type": "INT",
      "description": "The number of complete months the employee has been continuously employed."
    }
  ],
  "rules": [
    {
      "id": "A1B2C3D4E5F6",
      "expression": "(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)"
    }
  ],
  "types": []
}
```

Store this file in version control alongside your CloudFormation templates. When you update your policy, export the new version and update the file to trigger a deployment.

## Automate deployment with CloudFormation
<a name="deploy-cfn"></a>

Use CloudFormation to deploy your Automated Reasoning policy and guardrail as infrastructure as code. The `AWS::Bedrock::AutomatedReasoningPolicy` resource creates a policy with a policy definition that you export from the API or console. Combined with `AWS::Bedrock::Guardrail`, you can deploy the complete validation stack in a single template.

**Note**  
CloudFormation creates the policy resource with the policy definition you provide. It does not run a build workflow or extract rules from source documents. You must first create and test your policy interactively (using the console, API, or Kiro CLI), then export the tested policy definition for use in your template. For more information, see [Export a policy version for deployment](#export-policy-version).

For the complete property reference of the policy resource, see [AWS::Bedrock::AutomatedReasoningPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-automatedreasoningpolicy.html) in the *CloudFormation Template Reference*.

### Example: Deploy a policy and guardrail
<a name="deploy-cfn-template-example"></a>

The following CloudFormation template creates an Automated Reasoning policy with a policy definition and a guardrail that references it. Replace the policy definition with the JSON exported from your tested policy.

```
AWSTemplateFormatVersion: '2010-09-09'
Description: Deploy an Automated Reasoning policy and guardrail

Parameters:
  PolicyName:
    Type: String
    Default: {{MyHRPolicy}}
    Description: Name of the Automated Reasoning policy
  GuardrailName:
    Type: String
    Default: {{HR-Policy-Guardrail}}
    Description: Name of the guardrail

Resources:
  AutomatedReasoningPolicy:
    Type: AWS::Bedrock::AutomatedReasoningPolicy
    Properties:
      Name: !Ref PolicyName
      Description: Validates HR chatbot responses about leave eligibility
      PolicyDefinition:
        Version: '1.0'
        Variables:
          - Name: isFullTime
            Type: BOOL
            Description: >-
              Whether the employee works full-time (true) or part-time (false).
              Set to true when users mention being full-time or working 40+ hours
              per week.
          - Name: tenureMonths
            Type: INT
            Description: >-
              The number of complete months the employee has been continuously
              employed. When users mention years of service, convert to months
              (for example, 2 years = 24 months).
          - Name: eligibleForParentalLeave
            Type: BOOL
            Description: >-
              Whether the employee is eligible for parental leave based on
              employment status and tenure.
        Rules:
          - Id: {{A1B2C3D4E5F6}}
            Expression: >-
              (=> (and isFullTime (> tenureMonths 12))
              eligibleForParentalLeave)
          - Id: {{G7H8I9J0K1L2}}
            Expression: >-
              (=> (or (not isFullTime) (<= tenureMonths 12))
              (not eligibleForParentalLeave))
        Types: []
      Tags:
        - Key: Environment
          Value: Production
        - Key: Team
          Value: HR

  Guardrail:
    Type: AWS::Bedrock::Guardrail
    Properties:
      Name: !Ref GuardrailName
      Description: Guardrail with Automated Reasoning checks for HR policy
      BlockedInputMessaging: I cannot process this request.
      BlockedOutputsMessaging: I cannot provide this response.
      AutomatedReasoningPolicyConfig:
        Policies:
          - !GetAtt AutomatedReasoningPolicy.PolicyArn
      CrossRegionConfig:
        GuardrailProfileArn: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:guardrail-profile/{{us}}.guardrail.v1:0"

Outputs:
  PolicyArn:
    Description: ARN of the Automated Reasoning policy
    Value: !GetAtt AutomatedReasoningPolicy.PolicyArn
  PolicyId:
    Description: ID of the Automated Reasoning policy
    Value: !GetAtt AutomatedReasoningPolicy.PolicyId
  GuardrailId:
    Description: ID of the guardrail
    Value: !Ref Guardrail
```

**Tip**  
For production deployments, keep the policy definition in a separate JSON file and reference it using `Fn::Include` or by loading it as a template parameter. This keeps your template clean and makes it easier to update the policy definition independently.

**Important**  
Guardrails that use Automated Reasoning checks require a cross-Region inference profile. The `CrossRegionConfig` property specifies the guardrail profile ARN for your Region. Replace the Region prefix (`us`) with the appropriate prefix for your deployment Region (for example, `eu` for EU Regions). If you omit this property, the guardrail creation fails.

### Example: Deploy with a customer managed KMS key
<a name="deploy-cfn-kms-example"></a>

To encrypt your policy with a customer managed KMS key, add the `KmsKeyId` property. You must also configure the key policy to allow Amazon Bedrock to use the key. For the required key policy permissions, see [KMS permissions for Automated Reasoning policies](create-automated-reasoning-policy.md#automated-reasoning-policy-kms-permissions).

```
  AutomatedReasoningPolicy:
    Type: AWS::Bedrock::AutomatedReasoningPolicy
    Properties:
      Name: !Ref PolicyName
      Description: Validates HR chatbot responses about leave eligibility
      KmsKeyId: !GetAtt PolicyEncryptionKey.Arn
      PolicyDefinition:
        # ... policy definition ...
      Tags:
        - Key: Environment
          Value: Production
```

**Important**  
Changing the `KmsKeyId` property requires replacement of the resource. CloudFormation will delete the existing policy and create a new one with a new ARN. Update any guardrails that reference the old policy ARN.

## Next steps
<a name="deploy-next-steps"></a>

After deploying your policy and guardrail, integrate Automated Reasoning checks into your application to validate LLM responses at runtime. For more information, see [Integrate Automated Reasoning checks in your application](integrate-automated-reasoning-checks.md).