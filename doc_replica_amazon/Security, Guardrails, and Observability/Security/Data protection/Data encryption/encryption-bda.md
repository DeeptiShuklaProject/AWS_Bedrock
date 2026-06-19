

# Encryption in Amazon Bedrock Data Automation
<a name="encryption-bda"></a>

 Amazon Bedrock Data Automation (BDA) uses encryption to protect your data at rest. This includes the blueprints, projects, libraries, and extracted insights stored by the service. BDA offers two options for encrypting your data: 

1.  AWS owned keys – By default, BDA encrypts your data with AWS owned keys. You can't view, manage, or use AWS owned keys, or audit their use. However, you don't have to take any action or change any programs to protect the keys that encrypt your data. For more information, see [AWS owned keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk) in the AWS Key Management Service Developer Guide. 

1.  Customer managed keys – You can choose to encrypt your data with customer managed keys that you manage yourself. For more information about AWS KMS keys, see [Customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) in the AWS Key Management Service Developer Guide. BDA does not support customer managed keys for use in the Amazon Bedrock console, only for API operations. 

 Amazon Bedrock Data Automation automatically enables encryption at rest using AWS owned keys at no charge. If you use a customer managed key, AWS KMS charges apply. For more information about pricing, see AWS KMS [pricing](https://aws.amazon.com/kms/pricing/). 

## How Amazon Bedrock uses grants in AWS KMS
<a name="encryption-bda-grants"></a>

 If you specify a customer managed key for encryption of your BDA when calling invokeDataAutomationAsync or CreateDataAutomationLibrary, the service creates a grant associated with your resources on your behalf by sending a CreateGrant request to AWS KMS. This grant allows BDA to access and use your customer managed key. The grant created by CreateDataAutomationLibrary is not utilized if the customer ingests vocabulary entities into the library. 

 BDA uses the grant for your customer managed key for the following internal operations: 
+ DescribeKey — Send requests to AWS KMS to verify that the symmetric customer managed AWS KMS key ID you provided is valid.
+ GenerateDataKey and Decrypt — Send requests to AWS KMS to generate data keys encrypted by your customer managed key and decrypt the encrypted data keys so that they can be used to encrypt your resources.
+ CreateGrant — Send requests to AWS KMS to create scoped down grants for the asynchronous execution of operations. The grant operations vary by API:
  + InvokeDataAutomationAsync: DescribeKey, GenerateDataKey, Decrypt
  + CreateDataAutomationLibrary: DescribeKey, GenerateDataKey, Decrypt, CreateGrant

 You have full access to your customer managed AWS KMS key. You can revoke access to the grant by following the steps at Retiring and revoking grants in the AWS KMS Developer Guide or remove the service's access to your customer managed key at any time by modifying the key policy. If you do so, BDA won't be able to access the resources encrypted by your key. 

If you initiate a new invokeDataAutomationAsync call after revoking a grant, BDA will recreate the grant.

The grants created by invokeDataAutomationAsync are retired by BDA after 30 hours.

The grants created by CreateDataAutomationLibrary are retired by BDA when the library is deleted.

## Creating a customer managed key and attaching a key policy
<a name="encryption-bda-creating-keys"></a>

 To encrypt BDA resources with a key that you create and manage, follow these general steps: 

1.  (Prerequisite) Ensure that your IAM role has permissions for the CreateKey action. 

1.  Follow the steps at [ Creating keys ](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) to create a customer managed key using the AWS KMS console or the CreateKey operation. 

1.  Creation of the key returns an ARN that you can use for operations that require using the key (for example, when creating a project or blueprint in BDA), like the invokeDataAutomationAsync operation. 

1.  Create and attach a key policy to the key with the required permissions. To create a key policy, follow the steps at [ Creating a key policy ](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-create.html) in the AWS KMS Developer Guide. 

## Permissions and key policies for Amazon Bedrock Data Automation resources
<a name="encryption-bda-key-policies.title"></a>

 After you create a AWS KMS key, you attach a key policy to it. The following AWS KMS actions are used for keys that encrypt BDA resources:

1.  kms:CreateGrant – Creates a grant for a customer managed key by allowing the BDA service access to the specified AWS KMS key through grant operations, needed for InvokeDataAutomationAsync and CreateDataAutomationLibrary. 

1.  kms:DescribeKey – Provides the customer managed key details to allow BDA to validate the key. 

1.  kms:GenerateDataKey – Provides the customer managed key details to allow BDA to validate user access. 

1.  kms:Decrypt – Decrypts the stored ciphertext to validate that the role has proper access to the AWS KMS key that encrypts the BDA resources. 

**Key policy for Amazon Bedrock Data Automation**

 To use your customer managed key to encrypt BDA resources, include the following statements in your key policy and replace `${account-id}`, `${region}`, and `${key-id}` with your specific values:

```
{
  "Version": "2012-10-17",		 	 	 
  "Id": "KMS key policy for a key to encrypt data for BDA resource",
  "Statement": [
    {
      "Sid": "Enable DescribeKey, Decrypt, GenerateDataKey",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/Role"
      },
      "Action": [
        "kms:DescribeKey",
        "kms:GenerateDataKey",
        "kms:Decrypt"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
        }
      }
    },
    {
      "Sid": "Enable CreateGrant",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/Role"
      },
      "Action": "kms:CreateGrant",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "bedrock.us-east-1.amazonaws.com"
        },
        "ForAllValues:StringEquals": {
          "kms:GrantOperations": [
            "CreateGrant",
            "GenerateDataKey",
            "Decrypt",
            "DescribeKey"
          ]
        }
      }
    }
  ]
}
```

**IAM role permissions**

The IAM role used to interact with BDA and AWS KMS should have the following permissions, replace `${region}`, `${account-id}`, and `${key-id}` with your specific values:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt",
                "kms:DescribeKey",
                "kms:CreateGrant"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/KeyId",
            "Condition": {
                "StringLike": {
                    "kms:ViaService": [
                        "bedrock.us-east-1.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

------

## Amazon Bedrock Data Automation encryption context
<a name="encryption-bda-context"></a>

For all DataAutomationLibrary operations including InvokeDataAutomationLibraryIngestionJob, BDA uses below encryption context in all AWS KMS cryptographic operations, where the key is `aws:bedrock:data-automation-library-arn` and the value is the `libraryArn`.

```
"encryptionContext": {
     "aws:bedrock:data-automation-library-arn": "<LibraryArn>"
}
```

For DataAutomationProject operations, BDA uses below encryption context:

```
"encryptionContext": {
     "DataAutomationProjectArn": "<DataAutomationProjectArn>"
}
```

For Blueprint operations, BDA uses below encryption context:

```
"encryptionContext": {
     "BlueprintArn": "<BlueprintArn>"
}
```

For all other operations, BDA uses below encryption context:

```
"encryptionContext": {
     "aws:bedrock:data-automation-customer-account-id": "111122223333"
}
```

**Using encryption context for monitoring**  
When you use a symmetric customer managed key to encrypt your data, you can also use the encryption context in audit records and logs to identify how the customer managed key is being used. The encryption context also appears in logs generated by AWS CloudTrail or Amazon CloudWatch Logs.

**Using encryption context to control access to your customer managed key**  
You can use the encryption context in key policies and IAM policies as conditions to control access to your symmetric customer managed key. You can also use encryption context constraints in a grant. BDA uses an encryption context constraint in grants to control access to the customer managed key in your account or Region. The grant constraint requires that the operations that the grant allows use the specified encryption context. 

The following are example key policy statements to grant access to a customer managed key for a specific encryption context. The condition in this policy statement requires that the grants have an encryption context constraint that specifies the encryption context.

```
[
    {
        "Sid": "Enable DescribeKey",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::111122223333:role/ExampleRole"
        },
        "Action": ["kms:DescribeKey"],
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:ViaService": [
                    "bedrock.${region}.amazonaws.com"
                ]
            }
        }
    },
    {
        "Sid": "Enable Decrypt, GenerateDataKey",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::111122223333:role/ExampleRole"
        },
        "Action": [
            "kms:GenerateDataKey",
            "kms:Decrypt"
        ],
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:ViaService": [
                    "bedrock.${region}.amazonaws.com"
                ],
                "kms:EncryptionContext:aws:bedrock:data-automation-customer-account-id": "111122223333"
            }
        }
    },
    {
        "Sid": "Enable CreateGrant",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::111122223333:role/ExampleRole"
        },
        "Action": "kms:CreateGrant",
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:ViaService": [
                    "bedrock.${region}.amazonaws.com"
                ],
                "kms:EncryptionContext:aws:bedrock:data-automation-customer-account-id": "111122223333"
            },
            "StringEquals": {
                "kms:GrantOperations": ["Decrypt", "DescribeKey", "GenerateDataKey"]
            }
        }
    }
]
```

When calling `CreateDataAutomationLibrary`, attach the following policy to grant BDA the necessary permission for accessing your customer managed key.

```
[
    {
        "Sid": "Enable CreateGrant for CreateDataAutomationLibrary",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::111122223333:role/ExampleRole"
        },
        "Action": "kms:CreateGrant",
        "Resource": "*",
        "Condition": {
            "StringLike": {
                "kms:ViaService": [
                    "bedrock.${region}.amazonaws.com"
                ]
            },
            "StringEquals": {
                "kms:GrantOperations": ["Decrypt", "DescribeKey", "GenerateDataKey", "CreateGrant"]
            }
        }
    }
]
```

## Monitoring your encryption keys for Amazon Bedrock Data Automation
<a name="encryption-bda-monitoring"></a>

 When you use an AWS KMS customer managed key with your Amazon Bedrock Data Automation resources, you can use [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) or [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to track requests that Amazon Bedrock Data Automation sends to AWS KMS. The following is an example AWS CloudTrail event for [CreateGrant](https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html) to monitor AWS KMS operations called by Amazon Bedrock Data Automation to create a primary grant: 

```
{
    "eventVersion": "1.09",
        "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROAIGDTESTANDEXAMPLE:SampleUser01",
        "arn": "arn:aws:sts::111122223333:assumed-role/RoleForDataAutomation/SampleUser01",
        "accountId": "111122223333",
        "accessKeyId": "EXAMPLE",
        "sessionContext": {
        "sessionIssuer": {
        "type": "Role",
        "principalId": "AROAIGDTESTANDEXAMPLE",
        "arn": "arn:aws:iam::111122223333:role/RoleForDataAutomation",
        "accountId": "111122223333",
        "userName": "RoleForDataAutomation"
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
     "constraints": {
            "encryptionContextSubset": {
                "aws:bedrock:data-automation-customer-account-id": "000000000000"
            }
        },
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