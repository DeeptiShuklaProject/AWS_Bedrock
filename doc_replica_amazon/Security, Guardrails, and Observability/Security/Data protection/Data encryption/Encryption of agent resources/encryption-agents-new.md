

# Encryption of agent resources
<a name="encryption-agents-new"></a>

Encryption of data at rest by default helps reduce the operational overhead and complexity involved in protecting sensitive data. At the same time, it enables you to build secure applications that meet strict encryption compliance and regulatory requirements.

Amazon Bedrock uses default AWS-owned keys to automatically encrypt agent's information. This includes control plane data and session data. You can't view, manage, or audit the use of AWS owned keys. For more information, see [AWS owned keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk). 

While you can't disable this layer of encryption, you can choose to use customer managed keys instead of AWS-owned keys to encrypt agent's information. Amazon Bedrock supports the use of a symmetric customer managed keys (CMK) that you can create, own, and manage instead of the default AWS owned encryption. For more information, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk).

**Important**  
Amazon Bedrock automatically encrypts your agent's session information using AWS owned keys at no charge.
AWS KMS charges apply for using a customer managed keys. For more information about pricing, see [AWS Key Management Service Pricing](https://aws.amazon.com/kms/pricing/).
If you've created your agent *before* January 22, 2025 and want to use customer managed key for encrypting agent resources, follow instructions for [Encryption of agent resources for agents created before January 22, 2025](encryption-agents.md).