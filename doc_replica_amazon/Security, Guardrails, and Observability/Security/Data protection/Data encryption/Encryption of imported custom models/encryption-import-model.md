

# Encryption of imported custom models
<a name="encryption-import-model"></a>

Amazon Bedrock supports creating custom models through two methods that both use the same encryption approach. Your custom models are managed and stored by AWS:
+ **Custom model import jobs** — For importing customized open-source foundation models (such as Mistral AI or Llama models).
+ **Create custom model** — For importing Amazon Nova models that you customized in SageMaker AI.

For encryption of your custom models, Amazon Bedrock provides the following options: 
+ **AWS owned keys** – By default, Amazon Bedrock encrypts imported custom models with AWS owned keys. You can't view, manage, or use AWS owned keys, or audit their use. However, you don't have to take any action or change any programs to protect the keys that encrypt your data. For more information, see [AWS owned keys](https://docs.aws.amazon.com//kms/latest/developerguide/concepts.html#aws-owned-cmk) in the *AWS Key Management Service Developer Guide*.
+ **Customer managed keys (CMK)** – You can choose to add a second layer of encryption over the existing AWS owned encryption keys by choosing a customer managed key(CMK). You create, own, and manage your customer managed keys.

   Because you have full control of this layer of encryption, in it you can perform the following tasks: 
  + Establish and maintain key policies
  + Establish and maintain IAM policies and grants
  + Enable and disable key policies
  + Rotate key cryptographic material
  + Add tags
  + Create key aliases
  + Schedule keys for deletion

  For more information, see [customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the *AWS Key Management Service Developer Guide*.

**Note**  
For all the custom models that you import, Amazon Bedrock automatically enables encryption at rest using AWS owned keys to protect customer data at no charge. If you use a customer managed key, AWS KMS charges apply. For more information about pricing, see [AWS Key Management Service Pricing.](https://docs.aws.amazon.com/).

## How Amazon Bedrock uses grants in AWS KMS
<a name="import-model-kms-grants"></a>

If you specify a customer managed key to encrypt the imported model. Amazon Bedrock creates a **primary** AWS KMS [grant](https://docs.aws.amazon.com/) associated with the imported model on your behalf by sending a [CreateGrant](https://docs.aws.amazon.com//kms/latest/APIReference/API_CreateGrant.html) request to AWS KMS. This grant allows Amazon Bedrock to access and use your customer managed key. Grants in AWS KMS are used to give Amazon Bedrock access to a KMS key in a customer’s account.

Amazon Bedrock requires the primary grant to use your customer managed key for the following internal operations:
+ Send [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) requests to AWS KMS to verify that the symmetric customer managed KMS key ID you entered when creating the job is valid.
+ Send [GenerateDataKey](https://docs.aws.amazon.com//kms/latest/APIReference/API_GenerateDataKey.html) and [Decrypt](https://docs.aws.amazon.com//kms/latest/APIReference/API_Decrypt.html) requests to AWS KMS to generate data keys encrypted by your customer managed key and decrypt the encrypted data keys so that they can be used to encrypt the model artifacts.
+ Send [CreateGrant](https://docs.aws.amazon.com//kms/latest/APIReference/API_CreateGrant.html) requests to AWS KMS to create scoped down secondary grants with a subset of the above operations (`DescribeKey`, `GenerateDataKey`, `Decrypt`), for the asynchronous execution of model import and for on-demand inference. 
+ Amazon Bedrock specifies a retiring principal during the creation of grants, so the service can send a [RetireGrant](https://docs.aws.amazon.com//kms/latest/APIReference/API_RetireGrant.html) request.

You have full access to your customer managed AWS KMS key. You can revoke access to the grant by following the steps at [Retiring and revoking grants](https://docs.aws.amazon.com//kms/latest/developerguide/grant-manage.html#grant-delete) in the *AWS Key Management Service Developer Guide* or remove the service’s access to your customer managed key at any time by modifying the key policy. If you do so, Amazon Bedrock won’t be able to access the imported model encrypted by your key.

### Life cycle of primary and secondary grants for custom imported models
<a name="import-model-kms-grants-lifecycle"></a>
+ **Primary grants** have a long lifespan and remain active as long as the associated custom models are still in use. When a custom imported model is deleted, the corresponding primary grant is automatically retired.
+ **Secondary grants** are short-lived. They are automatically retired as soon as the operation that Amazon Bedrock performs on behalf of the customers is completed. For example, once a custom model import job is finished, the secondary grant that allowed Amazon Bedrock to encrypt the custom imported model will be retired immediately.