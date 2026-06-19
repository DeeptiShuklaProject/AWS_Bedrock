

# Using customer managed key (CMK)
<a name="import-model-using-cmk"></a>

If you are planning to use customer managed key to encrypt your custom imported model, complete the following steps:

1. Create a customer managed key with the AWS Key Management Service.

1. Attach a [resource-based policy](https://docs.aws.amazon.com//IAM/latest/UserGuide/access_policies_identity-vs-resource.html) with permissions for the specified-roles to create and use custom imported models.

**Create a customer managed key**

First ensure that you have `CreateKey` permissions. Then follow the steps at [creating keys](https://docs.aws.amazon.com//kms/latest/developerguide/create-keys.html) to create a customer managed keys either in the AWS KMS console or the [CreateKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateKey.html) API operation. Make sure to create a symmetric encryption key.

Creation of the key returns an `Arn` for the key that you can use as the `importedModelKmsKeyId ` when importing a custom model with custom model import.

**Create a key policy and attach it to the customer managed key**

Key policies are [resource-based policy](https://docs.aws.amazon.com//IAM/latest/UserGuide/access_policies_identity-vs-resource.html) that you attach to your customer managed key to control access to it. Every customer managed key must have exactly one key policy, which contains statements that determine who can use the key and how they can use it. You can specify a key policy when you create your customer managed key. You can modify the key policy at any time, but there might be a brief delay before the change becomes available throughout AWS KMS. For more information, see [Managing access to customer managed keys](https://docs.aws.amazon.com//kms/latest/developerguide/control-access-overview.html#managing-access) in the *AWS Key Management Service Developer Guide*.

**Encrypt an imported custom model**

To use your customer managed key to encrypt an imported custom model, you must include the following AWS KMS operations in the key policy:
+ [kms:CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) – creates a grant for a customer managed key by allowing the Amazon Bedrock service principal access to the specified KMS key through [grant operations](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html#terms-grant-operations). For more information about grants, see [Grants in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html) in the *AWS Key Management Service Developer Guide*.
**Note**  
Amazon Bedrock also sets up a retiring principal and automatically retires the grant after it is no longer required.
+ [kms:DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) – provides the customer managed key details to allow Amazon Bedrock to validate the key.
+ [kms:GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html) – Provides the customer managed key details to allow Amazon Bedrock to validate user access. Amazon Bedrock stores generated ciphertext alongside the imported custom model to be used as an additional validation check against imported custom model users
+ [kms:Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) – Decrypts the stored ciphertext to validate that the role has proper access to the KMS key that encrypts the imported custom model.

The following is an example policy that you can attach to a key for a role that you'll use to encrypt models that you import:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "KMS key policy for a key to encrypt an imported custom model",
    "Statement": [
        {
            "Sid": "Permissions for model import API invocation role",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:user/role"
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "*"
        }
    ]
}
```

------

**Decrypt an encrypted imported custom model**

If you're importing a custom model that has already been encrypted by another customer managed key, you must add `kms:Decrypt` permissions for the same role, as in the following policy:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "KMS key policy for a key that encrypted a custom imported model",
    "Statement": [
        {
            "Sid": "Permissions for model import API invocation role",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:user/role"
            },
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "*"
        }
    ]
}
```

------