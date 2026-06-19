

# Cross-account access to Amazon S3 bucket for custom model import jobs
<a name="cross-account-access-cmi"></a>

If you are importing your model from an Amazon S3 bucket in a different AWS account, you will need to grant permissions for accessing the bucket before you import your customized model. See [Prerequisites for importing custom model](custom-model-import-prereq.md).

**Note**  
If the custom model import job was submitted through the Amazon Bedrock console, a default import execution role is created automatically. You must edit the default import execution role policy and replace the account ID specified for `aws:ResourceAccount` with the AWS account ID of the bucket owner.

## Configure cross-account access to Amazon S3 bucket
<a name="configure-cross-acct-access"></a>

Follow these steps to configure cross-account access to an Amazon S3 bucket for a custom model import job.

1. **Create an import execution role** – In the user's AWS account (the account that will run the import job), create an IAM role that Amazon Bedrock can assume. For more information about creating a service role for custom model import, see [Prerequisites for importing custom model](custom-model-import-prereq.md).

1. **Create a bucket policy** – In the bucket owner's account, create a bucket policy that grants access to the import execution role in the user's account.

   The following example bucket policy, created and applied to bucket `s3://amzn-s3-demo-bucket` by the bucket owner, grants access to a user in bucket owner's account `123456789123`. 

------
#### [ JSON ]

****  

   ```
   { 
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "CrossAccountAccess",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::{{123456789012}}:role/{{ImportRole}}"
               },           
               "Action": [
                   "s3:ListBucket",
                   "s3:GetObject"
               ],
               "Resource": [
                   "arn:aws:s3:::{{amzn-s3-demo-bucket}}",
                   "arn:aws:s3:::{{amzn-s3-demo-bucket/*}}"
               ]
           }
       ]
   }
   ```

------

1. **Create an import execution role policy** – In the user's AWS account, attach a policy to the import execution role that allows access to the cross-account bucket. For `aws:ResourceAccount`, specify the account ID of the bucket owner's AWS account.

   The following example import execution role policy in the user's account provides the bucket owner's account id `111222333444555` access to Amazon S3 bucket `s3://amzn-s3-demo-bucket`.

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
               "s3:ListBucket",
               "s3:GetObject"
           ],
           "Resource": [
               "{{arn:aws:s3:::amzn-s3-demo-bucket}}",
               "{{arn:aws:s3:::amzn-s3-demo-bucket/*}}"
           ],
           "Condition": {
               "StringEquals": {
                   "aws:ResourceAccount": "{{123456789012}}"
               }
           }
       }
     ]
   }
   ```

------

## Configure cross-account access to Amazon S3 bucket encrypted with a custom AWS KMS key
<a name="configure-cross-acct-access-kms"></a>

If the Amazon S3 bucket is encrypted with a custom AWS Key Management Service (AWS KMS) key, you need to perform additional steps to grant the import execution role permissions to decrypt the key.

1. **Create an import execution role** – In the user's AWS account, create an IAM role that Amazon Bedrock can assume. For more information, see [Prerequisites for importing custom model](custom-model-import-prereq.md).

1. **Create a bucket policy** – In the bucket owner's account, create a bucket policy that grants access to the import execution role in the user's account.

   The following example bucket policy, created and applied to bucket `s3://amzn-s3-demo-bucket` by the bucket owner, grants access to a user in bucket owner's account `123456789123`. 

------
#### [ JSON ]

****  

   ```
   { 
      "Version":"2012-10-17",		 	 	 
      "Statement": [
       {
           "Sid": "CrossAccountAccess",
           "Effect": "Allow",
           "Principal": {
               "AWS": "arn:aws:iam::{{123456789012}}:role/{{ImportRole}}"
           },           
           "Action": [
               "s3:ListBucket",
               "s3:GetObject"
           ],
           "Resource": [
               "{{arn:aws:s3:::amzn-s3-demo-bucket}}",
               "{{arn:aws:s3:::amzn-s3-demo-bucket}}/*"
           ]
        }
      ]
   }
   ```

------

1. **Update the AWS KMS key policy** – In the bucket owner's account, add the following statement to the AWS KMS key policy to allow the user's import execution role to decrypt objects.

   ```
   {
       "Sid": "Allow use of the key by the destination account",
       "Effect": "Allow",
       "Principal": {
           "AWS": "{{arn:aws:iam::123456789123:role/ImportRole}}"
       },
       "Action": [
           "kms:Decrypt",
           "kms:DescribeKey"
       ],
       "Resource": "*"
   }
   ```

1. **Create an import execution role policy** – In the user's AWS account, attach a policy to the import execution role that allows access to the cross-account bucket and the AWS KMS key. For `aws:ResourceAccount`, specify the account ID of the bucket owner's AWS account.

   The following example import execution role policy provides access to the bucket owner's Amazon S3 bucket `s3://amzn-s3-demo-bucket` in account `111222333444555` and the AWS KMS key `arn:aws:kms:{{us-west-2:123456789098}}:key/{{111aa2bb-333c-4d44-5555-a111bb2c33dd}}`.

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
               "s3:ListBucket",
               "s3:GetObject"
           ],
           "Resource": [
               "{{arn:aws:s3:::amzn-s3-demo-bucket}}",
               "{{arn:aws:s3:::amzn-s3-demo-bucket/*}}"
           ],
           "Condition": {
               "StringEquals": {
                   "aws:ResourceAccount": "{{123456789012}}"
               }
           }
        },
        {
         "Effect": "Allow",
         "Action": [
           "kms:Decrypt",
           "kms:DescribeKey"
         ],
         "Resource": "arn:aws:kms:{{us-west-2}}:{{123456789012}}:key/{{111aa2bb-333c-4d44-5555-a111bb2c33dd}}"
       }
     ]
    }
   ```

------