

# Encryption of custom models
<a name="encryption-custom-job"></a>

Amazon Bedrock uses your training data with the [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) action, or with the [console](model-customization-submit.md), to create a custom model which is a fine tuned version of an Amazon Bedrock foundational model. Your custom models are managed and stored by AWS.

Amazon Bedrock uses the fine tuning data you provide only for fine tuning an Amazon Bedrock foundation model. Amazon Bedrock doesn't use fine tuning data for any other purpose. Your training data isn't used to train the base Titan models or distributed to third parties. Other usage data, such as usage timestamps, logged account IDs, and other information logged by the service, is also not used to train the models. 

None of the training or validation data you provide for fine tuning is stored by Amazon Bedrock, once the fine tuning job completes.

Note that fine-tuned models can replay some of the fine tuning data while generating completions. If your app should not expose fine tuning data in any form, then you should first filter out confidential data from your training data. If you already created a customized model using confidential data by mistake, you can delete that custom model, filter out confidential information from the training data, and then create a new model.

For encrypting custom models (including copied models), Amazon Bedrock offers you two options:

1. **AWS owned keys** – By default, Amazon Bedrock encrypts custom models with AWS owned keys. You can't view, manage, or use AWS owned keys, or audit their use. However, you don't have to take any action or change any programs to protect the keys that encrypt your data. For more information, see [AWS owned keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk) in the *AWS Key Management Service Developer Guide*.

1. **Customer managed keys** – You can choose to encrypt custom models with customer managed keys that you manage yourself. For more information about AWS KMS keys, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the *AWS Key Management Service Developer Guide*.

**Note**  
Amazon Bedrock automatically enables encryption at rest using AWS owned keys at no charge. If you use a customer managed key, AWS KMS charges apply. For more information about pricing, see [AWS Key Management Service pricing](https://aws.amazon.com/kms/pricing/).

For more information about AWS KMS, see the [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/).

**Topics**
+ [How Amazon Bedrock uses grants in AWS KMS](#encryption-br-grants)
+ [Understand how to create a customer managed key and how to attach a key policy to it](#encryption-key-policy)
+ [Permissions and key policies for custom and copied models](#encryption-cm-statements)
+ [Monitor your encryption keys for the Amazon Bedrock service](#encryption-monitor-key)
+ [Encryption of training, validation, and output data](#encryption-custom-job-data)

## How Amazon Bedrock uses grants in AWS KMS
<a name="encryption-br-grants"></a>

If you specify a customer managed key to encrypt a custom model for a model customization or model copy job, Amazon Bedrock creates a **primary** KMS [grant](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html) associated with the custom model on your behalf by sending a [CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) request to AWS KMS. This grant allows Amazon Bedrock to access and use your customer managed key. Grants in AWS KMS are used to give Amazon Bedrock access to a KMS key in a customer’s account.

Amazon Bedrock requires the primary grant to use your customer managed key for the following internal operations:
+ Send [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) requests to AWS KMS to verify that the symmetric customer managed KMS key ID you entered when creating the job is valid.
+ Send [GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html) and [Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) requests to AWS KMS to generate data keys encrypted by your customer managed key and decrypt the encrypted data keys so that they can be used to encrypt the model artifacts.
+ Send [CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) requests to AWS KMS to create scoped down secondary grants with a subset of the above operations (`DescribeKey`, `GenerateDataKey`, `Decrypt`), for the asynchronous execution of model customization, model copy, or Provisioned Throughput creation.
+ Amazon Bedrock specifies a retiring principal during the creation of grants, so the service can send a [RetireGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_RetireGrant.html) request.

You have full access to your customer managed AWS KMS key. You can revoke access to the grant by following the steps at [Retiring and revoking grants](https://docs.aws.amazon.com/kms/latest/developerguide/grant-manage.html#grant-delete) in the [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/) or remove the service’s access to your customer managed key at any time by modifying the [key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html). If you do so, Amazon Bedrock won’t be able to access the custom model encrypted by your key.

### Life cycle of primary and secondary grants for custom models
<a name="encryption-primary-secondary-grants"></a>
+ **Primary grants** have a long lifespan and remain active as long as the associated custom models are still in use. When a custom model is deleted, the corresponding primary grant is automatically retired.
+ **Secondary grants** are short-lived. They are automatically retired as soon as the operation that Amazon Bedrock performs on behalf of the customers is completed. For example, once a model copy job is finished, the secondary grant that allowed Amazon Bedrock to encrypt the copied custom model will be retired immediately.

## Understand how to create a customer managed key and how to attach a key policy to it
<a name="encryption-key-policy"></a>

To encrypt an AWS resource with a key that you create and manage, you perform the following general steps:

1. (Prerequisite) Ensure that your IAM role has permissions for the [CreateKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateKey.html) action.

1. Follow the steps at [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) to create a customer managed key by using the AWS KMS console or the [CreateKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateKey.html) operation.

1. Creation of the key returns an `Arn` for the key that you can use for operations that require using the key (for example, when [submitting a model customization job](model-customization-submit.md) or [running model inference](inference-invoke.md)).

1. Create and attach a key policy to the key with the required permissions. To create a key policy, follow the steps at [Creating a key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-overview.html) in the AWS Key Management Service Developer Guide.

## Permissions and key policies for custom and copied models
<a name="encryption-cm-statements"></a>

After you create a KMS key, you attach a key policy to it. Key policies are [resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html) that you attach to your customer managed key to control access to it. Every customer managed key must have exactly one key policy, which contains statements that determine who can use the key and how they can use it. You can specify a key policy when you create your customer managed key. You can modify the key policy at any time, but there might be a brief delay before the change becomes available throughout AWS KMS. For more information, see [Managing access to customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/control-access-overview.html#managing-access) in the [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/).

The following KMS [actions](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awskeymanagementservice.html#awskeymanagementservice-actions-as-permissions) are used for keys that encrypt custom and copied models:

1. [kms:CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) – Creates a grant for a customer managed key by allowing the Amazon Bedrock service principal access to the specified KMS key through [grant operations](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html#terms-grant-operations). For more information about grants, see [Grants in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html) in the [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/).
**Note**  
Amazon Bedrock also sets up a retiring principal and automatically retires the grant after it is no longer required.

1. [kms:DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) – Provides the customer managed key details to allow Amazon Bedrock to validate the key.

1. [kms:GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html) – Provides the customer managed key details to allow Amazon Bedrock to validate user access. Amazon Bedrock stores generated ciphertext alongside the custom model to be used as an additional validation check against custom model users.

1. [kms:Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) – Decrypts the stored ciphertext to validate that the role has proper access to the KMS key that encrypts the custom model.

As a best security practice, we recommend that you include the [kms:ViaService](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-via-service) condition key to limit access to the key to the Amazon Bedrock service.

Although you can only attach one key policy to a key, you can attach multiple statements to the key policy by adding staements to the list in the `Statement` field of the policy.

The following statements are relevant to encrypting custom and copied models:

### Encrypt a model
<a name="encryption-key-policy-encrypt"></a>

To use your customer managed key to encrypt a custom or copied model, include the following statement in a key policy to allow encryption of a model. In the `Principal` field, add accounts that you want to allow to encrypt and decrypt the key to the list that the `AWS` subfield maps to. If you use the `kms:ViaService` condition key, you can add a line for each Region, or use {{\*}} in place of {{${region}}} to allow all Regions that support Amazon Bedrock.

```
{
    "Sid": "PermissionsEncryptDecryptModel",
    "Effect": "Allow",
    "Principal": {
        "AWS": [
            "arn:aws:iam::{{${account-id}}}:role/{{${role}}}"
        ]
    },
    "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey",
        "kms:CreateGrant"
    ],
    "Resource": "*",
    "Condition": {
        "StringLike": {
            "kms:ViaService": [
                "bedrock.{{${region}}}.amazonaws.com"
            ] 
        }
    }
}
```

### Allow access to an encrypted model
<a name="encryption-key-policy-decrypt"></a>

To allow access to a model that has been encrypted with a KMS key, include the following statement in a key policy to allow decryption of the key. In the `Principal` field, add accounts that you want to allow to decrypt the key to the list that the `AWS` subfield maps to. If you use the `kms:ViaService` condition key, you can add a line for each Region, or use {{\*}} in place of {{${region}}} to allow all Regions that support Amazon Bedrock.

```
{
    "Sid": "PermissionsDecryptModel",
    "Effect": "Allow",
    "Principal": {
        "AWS": [
            "arn:aws:iam::{{${account-id}}}:role/{{${role}}}"
        ]
    },
    "Action": [
        "kms:Decrypt"
    ],
    "Resource": "*",
    "Condition": {
        "StringLike": {
            "kms:ViaService": [
                "bedrock.{{${region}}}.amazonaws.com"
            ] 
        }
    }
}
```

To learn about the key policies that you need to create, expand the section that corresponds to your use case:

### Set up key permissions for encrypting custom models
<a name="encryption-cm"></a>

If you plan to encrypt a model that you customize with a KMS key, the key policy for the key will depend on your use case. Expand the section that corresponds to your use case:

#### The roles that will customize the model and the roles that will invoke the model are the same
<a name="encryption-cm-custom-invoke-same"></a>

If the roles that will invoke the custom model are the same as the roles that will customize the model, you only need the statement from [Encrypt a model](#encryption-key-policy-encrypt). In the `Principal` field in the following policy template, add accounts that you want to allow to customize and invoke the custom model to the list that the `AWS` subfield maps to.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "{{PermissionsCustomModelKey}}",
    "Statement": [
        {
            "Sid": "PermissionsEncryptCustomModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

#### The roles that will customize the model and the roles that will invoke the model are different
<a name="encryption-custom-invoke-different"></a>

If the roles that will invoke the custom model are different from the role that will customize the model, you need both the statement from [Encrypt a model](#encryption-key-policy-encrypt) and [Allow access to an encrypted model](#encryption-key-policy-decrypt). Modify the statements in the following policy template as follows:

1. The first statement allows encryption and decryption of the key. In the `Principal` field, add accounts that you want to allow to customize the custom model to the list that the `AWS` subfield maps to.

1. The second statement allows only decryption of the key. In the `Principal` field, add accounts that you want to only allow to invoke the custom model to the list that the `AWS` subfield maps to.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "{{PermissionsCustomModelKey}}",
    "Statement": [
        {
            "Sid": "PermissionsEncryptCustomModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "PermissionsDecryptModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

### Set up key permissions for copying custom models
<a name="encryption-copy"></a>

When you copy a model that you own or that has been shared with you, you might have to manage up to two key policies:

#### Key policy for key that will encrypt a copied model
<a name="encryption-copied-model-key-policy"></a>

If you plan to use a KMS key to encrypt a copied model, the key policy for the key will depend on your use case. Expand the section that corresponds to your use case:

##### The roles that will copy the model and the roles that will invoke the model are the same
<a name="encryption-copied-model-copy-invoke-same"></a>

If the roles that will invoke the copied model are the same as the roles that will create the model copy, you only need the statement from [Encrypt a model](#encryption-key-policy-encrypt). In the `Principal` field in the following policy template, add accounts that you want to allow to copy and invoke the copied model to the list that the `AWS` subfield maps to:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "{{PermissionsCopiedModelKey}}",
    "Statement": [
        {
            "Sid": "PermissionsEncryptCopiedModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

##### The roles that will copy the model and the roles that will invoke the model are different
<a name="encryption-copied-model-copy-invoke-different"></a>

If the roles that will invoke the copied model are different from the role that will create the model copy, you need both the statement from [Encrypt a model](#encryption-key-policy-encrypt) and [Allow access to an encrypted model](#encryption-key-policy-decrypt). Modify the statements in the following policy template as follows:

1. The first statement allows encryption and decryption of the key. In the `Principal` field, add accounts that you want to allow to create the copied model to the list that the `AWS` subfield maps to.

1. The second statement allows only decryption of the key. In the `Principal` field, add accounts that you want to only allow to invoke the copied model to the list that the `AWS` subfield maps to.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "{{PermissionsCopiedModelKey}}",
    "Statement": [
        {
            "Sid": "PermissionsEncryptCopiedModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "PermissionsDecryptCopiedModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

#### Key policy for key that encrypts the source model to be copied
<a name="encryption-copy-source-model-key-policy"></a>

If the source model that you will copy is encrypted with a KMS key, attach the statement from [Allow access to an encrypted model](#encryption-key-policy-decrypt) to the key policy for the key that encrypts the source model. This stamtement allows the model copy role to decrypt the key that encrypts the source model. In the `Principal` field in the following policy template, add accounts that you want to allow to copy the source model to the list that the `AWS` subfield maps to:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Id": "{{PermissionsSourceModelKey}}",
    "Statement": [
        {
            "Sid": "PermissionsDecryptModel",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::{{111122223333}}:role/{{Role}}"
                ]
            },
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.{{us-east-1}}.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

## Monitor your encryption keys for the Amazon Bedrock service
<a name="encryption-monitor-key"></a>

When you use an AWS KMS customer managed key with your Amazon Bedrock resources, you can use [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) or [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to track requests that Amazon Bedrock sends to AWS KMS.

The following is an example AWS CloudTrail event for [CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) to monitor KMS operations called by Amazon Bedrock to create a primary grant:

```
{
    "eventVersion": "1.09",
    "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROAIGDTESTANDEXAMPLE:SampleUser01",
        "arn": "arn:aws:sts::111122223333:assumed-role/RoleForModelCopy/SampleUser01",
        "accountId": "111122223333",
        "accessKeyId": "EXAMPLE",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROAIGDTESTANDEXAMPLE",
                "arn": "arn:aws:iam::111122223333:role/RoleForModelCopy",
                "accountId": "111122223333",
                "userName": "RoleForModelCopy"
            },
            "attributes": {
                "creationDate": "2024-05-07T21:46:28Z",
                "mfaAuthenticated": "false"
            }
        },
        "invokedBy": "bedrock.amazonaws.com"
    },
    "eventTime": "2024-05-07T21:49:44Z",
    "eventSource": "kms.amazonaws.com",
    "eventName": "CreateGrant",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "bedrock.amazonaws.com",
    "userAgent": "bedrock.amazonaws.com",
    "requestParameters": {
        "granteePrincipal": "bedrock.amazonaws.com",
        "retiringPrincipal": "bedrock.amazonaws.com",
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE",
        "operations": [
            "Decrypt",
            "CreateGrant",
            "GenerateDataKey",
            "DescribeKey"
        ]
    },
    "responseElements": {
        "grantId": "0ab0ac0d0b000f00ea00cc0a0e00fc00bce000c000f0000000c0bc0a0000aaafSAMPLE",
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE"
    },
    "requestID": "ff000af-00eb-00ce-0e00-ea000fb0fba0SAMPLE",
    "eventID": "ff000af-00eb-00ce-0e00-ea000fb0fba0SAMPLE",
    "readOnly": false,
    "resources": [
        {
            "accountId": "111122223333",
            "type": "AWS::KMS::Key",
            "ARN": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-123456SAMPLE"
        }
    ],
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management"
}
```

## Encryption of training, validation, and output data
<a name="encryption-custom-job-data"></a>

When you use Amazon Bedrock to run a model customization job, you store the input files in your Amazon S3 bucket. When the job completes, Amazon Bedrock stores the output metrics files in the S3 bucket that you specifed when creating the job and the resulting custom model artifacts in an S3 bucket controlled by AWS.

The output files are encrypted with the encryption configurations of the S3 bucket. These are encrypted either with [SSE-S3 server-side encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html) or with [AWS KMS SSE-KMS encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html), depending on how you set up the S3 bucket.