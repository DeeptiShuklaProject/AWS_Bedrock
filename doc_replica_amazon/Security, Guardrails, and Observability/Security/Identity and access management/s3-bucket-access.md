

# Configure access to Amazon S3 buckets
<a name="s3-bucket-access"></a>

Multiple Amazon Bedrock features require access to data that is stored in Amazon S3 buckets. To access this data, you must configure the following permissions:


****  

| Use case | Permissions | 
| --- | --- | 
| Permissions to retrieve data from S3 bucket | s3:GetObjects3:ListBucket | 
| Permissions to write data to S3 bucket | s3:PutObject | 
| Permissions to decrypt KMS key that encrypted the S3 bucket | kms:Decryptkms:DescribeKey<br />kms:GenerateDataKey (required for write operations to buckets with default SSE-KMS encryption) | 

The identities or resources to which you need to attach the above permissions depends on the following factors:
+ Multiple features in Amazon Bedrock use [service roles](security-iam-sr.md). If a feature uses a service role, you must configure the permissions such that the service role, rather than the user's IAM identity, has access to the S3 data. Some Amazon Bedrock features can automatically create a service role for you and attach the required [identity-based permissions](https://docs.aws.amazon.com//IAM/latest/UserGuide/access_policies.html#policies_id-based) to the service role, if you use the AWS Management Console.
+ Some features in Amazon Bedrock allow an identity to access an S3 bucket in a different account. If S3 data needs to be accessed from a different account, the bucket owner must include the above [resource-based permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_resource-based) in an [S3 bucket policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html) attached to the S3 bucket.

The following describes how to determine where you need to attach the necessary permissions to access S3 data:
+ IAM identity permissions
  + If you can auto-create a service role in the console, the permissions will be configured for the service role, so you don't need to configure it yourself.
  + If you prefer to use a custom service role or the identity that requires access isn't a service role, navigate to [Attach permissions to an IAM identity to allow it to access an Amazon S3 bucket](#s3-bucket-access-identity) to learn how to create an identity-based policy with the proper permissions.
+ Resource-based permissions
  + If the identity requires access to S3 data in the same account, you don't need attach an S3 bucket policy to the bucket containing the data.
  + If the identity requires access to S3 data in a different account, navigate to [Attach a bucket policy to an Amazon S3 bucket to allow another account to access it](#s3-bucket-access-cross-account) to learn how to create an S3 bucket policy with the proper permissions.
**Important**  
Automatic creation of a service role in the AWS Management Console attaches the proper identity-based permissions to the role, but you still must configure the S3 bucket policy if the identity that requires access to it is in a different AWS account.

For more information, see the following links:
+ To learn more about controlling access to data in Amazon S3, see [Access control in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-management.html).
+ To learn more about Amazon S3 permissions, see [Actions defined by Amazon S3](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html#amazons3-actions-as-permissions).
+ To learn more about AWS KMS permissions, see [Actions defined by AWS Key Management Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awskeymanagementservice.html#awskeymanagementservice-actions-as-permissions).

Proceed through the topics that pertain to your use case:

**Topics**
+ [Attach permissions to an IAM identity to allow it to access an Amazon S3 bucket](#s3-bucket-access-identity)
+ [Attach a bucket policy to an Amazon S3 bucket to allow another account to access it](#s3-bucket-access-cross-account)
+ [(Advanced security option) Include conditions in a statement for more fine-grained access](#s3-bucket-access-conditions)

## Attach permissions to an IAM identity to allow it to access an Amazon S3 bucket
<a name="s3-bucket-access-identity"></a>

This topic provides a template for a policy to attach to an IAM identity. The policy includes the following statements defining permissions to grant an IAM identity access to an S3 bucket:

1. Permissions to retrieve data from an S3 bucket. This statement also includes a condition using the `s3:prefix` [condition key](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html#amazons3-policy-keys) to restrict access to a specific folder in the bucket. For more information about this condition, see the **User policy** section in [Example 2: Getting a list of objects in a bucket with a specific prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#condition-key-bucket-ops-2).

1. (If you need to write data to an S3 location) Permissions to write data to an S3 bucket. This statement also includes a condition using the `aws:ResourceAccount` [condition key](https://docs.aws.amazon.com//IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-resourceaccount) to restrict access to requests sent from a specific AWS account.

1. (If the S3 bucket is encrypted with an KMS key) Permissions to describe and decrypt the KMS key that encrypted the S3 bucket.
**Note**  
If your S3 bucket is versioning-enabled, each object version that you upload by using this feature can have its own encryption key. You're responsible for tracking which encryption key was used for which object version.

Add, modify, and remove the statements, resources, and conditions in the following policy and replace {{${values}}} as necessary:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ReadS3Bucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{${S3Bucket}}}",
                "arn:aws:s3:::{{${S3Bucket}}}/*"
            ]
        },
        {
            "Sid": "WriteToS3Bucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{${S3Bucket}}}",
                "arn:aws:s3:::{{${S3Bucket}}}/*"
            ]
        },
        {
            "Sid": "DecryptKMSKey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{${KMSKeyId}}}"
        }
    ]
}
```

------

After modifying the policy to your use case, attach it to the service role (or IAM identity) that requires access to the S3 bucket. To learn how to attach permissions to an IAM identity, see [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html).

## Attach a bucket policy to an Amazon S3 bucket to allow another account to access it
<a name="s3-bucket-access-cross-account"></a>

This topic provides a template for a resource-based policy to attach to an S3 bucket to allow an IAM identity to access data in the bucket. The policy includes the following statements defining permissions for an identity to access the bucket:

1. Permissions to retrieve data from an S3 bucket.

1. (If you need to write data to an S3 location) Permissions to write data to an S3 bucket.

1. (If the S3 bucket is encrypted with an KMS key) Permissions to describe and decrypt the KMS key that encrypted the S3 bucket.
**Note**  
If your S3 bucket is versioning-enabled, each object version that you upload by using this feature can have its own encryption key. You're responsible for tracking which encryption key was used for which object version.

The permissions are similar to the identity-based permissions described in [Attach permissions to an IAM identity to allow it to access an Amazon S3 bucket](#s3-bucket-access-identity). However, each statement also requires you to specify the identity for which to grant permissions to the resource in the `Principal` field. Specify the identity (with most features in Amazon Bedrock, this is the service role) in the `Principal` field. Add, modify, and remove the statements, resources, and conditions in the following policy and replace {{${values}}} as necessary:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ReadS3Bucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:role/{{ServiceRole}}"
            },
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{${S3Bucket}}}",
                "arn:aws:s3:::{{${S3Bucket}}}/*"
            ]
        },
        {
            "Sid": "WriteToS3Bucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:role/{{ServiceRole}}"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{${S3Bucket}}}",
                "arn:aws:s3:::{{${S3Bucket}}}/*"
            ]
        },
        {
            "Sid": "DecryptKMSKey",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{{111122223333}}:role/{{ServiceRole}}"
            },
            "Action": [
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:{{us-east-1}}:{{123456789012}}:key/{{${KMSKeyId}}}"
        }
    ]
}
```

------

After modifying the policy to your use case, attach it to the S3 bucket. To learn how to attach a bucket policy to an S3 bucket, see [Adding a bucket policy by using the Amazon S3 console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/add-bucket-policy.html).

## (Advanced security option) Include conditions in a statement for more fine-grained access
<a name="s3-bucket-access-conditions"></a>

For greater control over the identities that can access your resources, you can include conditions in a policy statement. The policy in this topic provides an example that uses the following condition keys:
+ `s3:prefix` – An S3 condition key that restricts access to a specific folder in an S3 bucket. For more information about this condition key, see the **User policy** section in [Example 2: Getting a list of objects in a bucket with a specific prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#condition-key-bucket-ops-2).
+ `aws:ResourceAccount` – A global condition key that restricts access to requests from a specific AWS account.

The following policy restricts read access to the {{my-folder}} folder in the {{amzn-s3-demo-bucket}} S3 bucket and restricts write access for the {{amzn-s3-demo-destination-bucket}} S3 bucket to requests from the AWS account with the ID {{111122223333}}:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ReadS3Bucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}",
                "arn:aws:s3:::{{amzn-s3-demo-bucket}}/*"
            ],
            "Condition" : {
                "StringEquals" : {
                    "s3:prefix": "{{my-folder}}" 
                }
            }
        },
        {
            "Sid": "WriteToS3Bucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-destination-bucket}}",
                "arn:aws:s3:::{{amzn-s3-demo-destination-bucket}}/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "{{111122223333}}"
                }
            }
        }
    ]
}
```

------

To learn more about conditions and condition keys, see the following links:
+ To learn about conditions, see [IAM JSON policy elements: Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html) in the IAM User Guide.
+ To learn about condition keys specific to S3, see [Condition keys for Amazon S3](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html#amazons3-policy-keys) in the Service Authorization Reference.
+ To learn about global condition keys used across AWS services, see [AWS global condition context keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-resourceaccount).