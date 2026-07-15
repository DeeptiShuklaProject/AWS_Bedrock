

# Tag propagation
<a name="lambda-managed-instances-tag-propagation"></a>

With tag propagation, you can specify a set of tags on your capacity provider configuration, and Lambda automatically applies those tags to all managed resources it creates, including Amazon EC2 instances, Amazon EBS volumes, and ENIs. This ensures consistent tagging for cost allocation, service control policies (SCPs), and compliance requirements without requiring manual intervention or custom automation.

## Configuring tag propagation
<a name="lambda-managed-instances-tag-propagation-configuring"></a>

Specify the `PropagateTags` setting when creating or updating a capacity provider using the `CreateCapacityProvider` or `UpdateCapacityProvider` APIs.

**PropagateTags parameters:**
+ **Mode** (required) – The tag propagation mode:
  + `Explicit` – Propagate the tags specified in `ExplicitTags` to managed resources.
  + `None` – Disable tag propagation. No custom tags are applied to managed resources except system tags applied by default.
+ **ExplicitTags** (required when Mode is `Explicit`) – A map of key-value pairs to apply to managed resources. You can specify up to 40 tags.

**Important**  
Tag propagation applies only to new managed resources provisioned after the configuration is applied. Existing resources are not retroactively tagged.

## Examples
<a name="lambda-managed-instances-tag-propagation-examples"></a>

**Create a capacity provider with tag propagation (AWS CLI):**

```
aws lambda create-capacity-provider \
  --capacity-provider-name my-capacity-provider \
  --vpc-config SubnetIds=subnet-12345,subnet-67890,SecurityGroupIds=sg-12345 \
  --permissions-config CapacityProviderOperatorRoleArn=arn:aws:iam::123456789012:role/MyOperatorRole \
  --propagate-tags '{"Mode": "Explicit", "ExplicitTags": {"CostCenter": "12345", "Environment": "Production"}}'
```

**Update an existing capacity provider to enable tag propagation:**

```
aws lambda update-capacity-provider \
  --capacity-provider-name my-capacity-provider \
  --propagate-tags '{"Mode": "Explicit", "ExplicitTags": {"CostCenter": "12345", "Environment": "Production"}}'
```

**Disable tag propagation:**

```
aws lambda update-capacity-provider \
  --capacity-provider-name my-capacity-provider \
  --propagate-tags '{"Mode": "None"}'
```

## Tag propagation behavior
<a name="lambda-managed-instances-tag-propagation-behavior"></a>
+ Changes to `PropagateTags` configuration only affect resources provisioned after the update. Previously launched resources retain their original tags.
+ Tag propagation tags are separate from the `Tags` parameter on the capacity provider itself. Capacity provider tags identify the capacity provider resource; propagated tags are applied to the managed resources the capacity provider launches.
+ Propagated tags count toward the AWS resource tag limits on the target resources.