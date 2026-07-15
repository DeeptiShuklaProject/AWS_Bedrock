

# Security model for Lambda SnapStart
<a name="snapstart-security"></a>

AWS Lambda SnapStart supports encryption at rest. Lambda encrypts snapshots with an AWS KMS key. By default, Lambda uses an AWS managed key. If this default behavior suits your workflow, then you don't need to set up anything else. Otherwise, you can use the `--kms-key-arn` option in the [create-function](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/create-function.html) or [update-function-configuration](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/update-function-configuration.html) command to provide an AWS KMS customer managed key. You might do this to control rotation of the KMS key or to meet the requirements of your organization for managing KMS keys. Customer managed keys incur standard AWS KMS charges. For more information, see [AWS Key Management Service pricing](https://aws.amazon.com/kms/pricing/).

If your function is also a durable function, the customer managed key that encrypts SnapStart snapshots is independent of the customer managed key that encrypts durable execution data. For more information, see [Encrypting AWS Lambda durable execution data](durable-encryption.md).

When you delete a SnapStart function or function version, all `Invoke` requests to that function or function version fail. Lambda removes all resources associated with deleted snapshots in compliance with the General Data Protection Regulation (GDPR).