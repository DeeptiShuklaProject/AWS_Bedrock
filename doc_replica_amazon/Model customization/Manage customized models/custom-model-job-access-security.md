

# Model customization access and security
<a name="custom-model-job-access-security"></a>

This page provides comprehensive security and permissions information for all Amazon Bedrock model customization types including fine-tuning, reinforcement fine-tuning, distillation, and model operations. Before you begin customizing a model, make sure that you understand what kind of access Amazon Bedrock needs and consider some options for securing your customization jobs and artifacts.

The following sections contain the permissions required for different customization scenarios. Choose the appropriate permissions based on your specific use case:

## Basic model customization permissions
<a name="custom-model-job-basic-permissions"></a>

All model customization jobs require these basic permissions. These apply to fine-tuning, distillation, and other customization types.

### Create an IAM service role for model customization
<a name="custom-model-job-service-role"></a>

Amazon Bedrock needs an AWS Identity and Access Management (IAM) service role to access the S3 bucket where you want to store your model customization training and validation data. There are a couple ways to do this:
+ Create the service role automatically by using the AWS Management Console.
+ Create the service role manually with the proper permissions to access your S3 bucket.

For the manual option, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
+ Trust relationship
+ Permissions to access your training and validation data in S3 and to write your output data to S3
+ (Optional) If you encrypt any of the following resources with a KMS key, permissions to decrypt the key (see [Encryption of custom models](encryption-custom-job.md))
  + A model customization job or the resulting custom model
  + The training, validation, or output data for the model customization job

### Trust relationship
<a name="custom-model-job-service-role-trust-relationship"></a>

The following policy allows Amazon Bedrock to assume this role and carry out the model customization job. The following shows an example policy you can use.

You can optionally restrict the scope of the permission for [cross-service confused deputy prevention](cross-service-confused-deputy-prevention.md) by using one or more global condition context keys with the `Condition` field. For more information, see [AWS global condition context keys.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
+ Set the `aws:SourceAccount` value to your account ID.
+ (Optional) Use the `ArnEquals` or `ArnLike` condition to restrict the scope to specific model customization jobs in your account ID.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "{{123456789012}}"
                },
                "ArnEquals": {
                    "aws:SourceArn": "arn:aws:bedrock:us-east-1:{{111122223333}}:model-customization-job/*"
                }
            }
        }
    ]
}
```

------

### Permissions to access training and validation files and to write output files in S3
<a name="custom-model-job-service-role-s3-permissions"></a>

Attach the following policy to allow the role to access your training and validation data and the bucket to which to write your output data. Replace the values in the `Resource` list with your actual bucket names.

To restrict access to a specific folder in a bucket, add an `s3:prefix` condition key with your folder path. You can follow the **User policy** example in [Example 2: Getting a list of objects in a bucket with a specific prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#condition-key-bucket-ops-2) 

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
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{training-bucket}}",
                "arn:aws:s3:::{{training-bucket/*}}",
                "arn:aws:s3:::{{validation-bucket}}",
                "arn:aws:s3:::{{validation-bucket/*}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{{output-bucket}}",
                "arn:aws:s3:::{{output-bucket/*}}"
            ]
        }
    ]
}
```

------

## Model copying permissions
<a name="custom-model-job-model-copying-permissions"></a>

To copy a model to another Region, you need specific permissions depending on your role's current permissions and the model's configuration.

1. If your role doesn't have the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) policy attached, attach the following identity-based policy to the role to allow the minimal permissions to copy models and to track copy jobs.

------
#### [ JSON ]

****  

   ```
   {
       "Version":"2012-10-17",		 	 	 
       "Statement": [
           {
               "Sid": "CopyModels",
               "Effect": "Allow",
               "Action": [
                   "bedrock:CreateModelCopyJob",
                   "bedrock:GetModelCopyJob",
                   "bedrock:ListModelCopyJobs"
               ],
               "Resource": [
                   "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{model-id}}"
               ],
               "Condition": {
                   "StringEquals": {
                       "aws:RequestedRegion": [
                           "{{us-east-1}}"
                       ]
                   }
               }
           }
       ]
   }
   ```

------

1. (Optional) If the model to be copied is encrypted with a KMS key, attach a [key policy to the KMS key that encrypted the model](encryption-custom-job.md#encryption-key-policy-decrypt) to allow a role to decrypt it.

1. (Optional) If you plan to encrypt the model copy with a KMS key, attach a [key policy to the KMS key that will be used to encrypt the model](encryption-custom-job.md#encryption-key-policy-encrypt) to allow a role to encrypt the model with the key.

## Cross-region inference profile permissions
<a name="custom-models-cross-region-inference-profile-basic-permissions"></a>

To use a cross-region inference profile for a teacher model in a distillation job, the service role must have permissions to invoke the inference profile in an AWS Region, in addition to the model in each Region in the inference profile.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CrossRegionInference",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:inference-profile/{{${InferenceProfileId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}"
            ]
        }
    ]
}
```

------

## (Optional) Permissions to create a Distillation job with a cross-region inference profile
<a name="custom-models-cross-region-inference-profile-permissions"></a>

To use a cross-region inference profile for a teacher model in a distillation job, the service role must have permissions to invoke the inference profile in an AWS Region, in addition to the model in each Region in the inference profile.

For permissions to invoke with a cross-Region (system-defined) inference profile, use the following policy as a template for the permissions policy to attach to your service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "CrossRegionInference",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:inference-profile/{{${InferenceProfileId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}"
            ]
        }
    ]
}
```

------

## (Optional) Encrypt model customization jobs and artifacts
<a name="custom-model-job-encryption"></a>

Encrypt the input and output data, customization jobs, or inference requests made to custom models. For more information, see [Encryption of custom models](encryption-custom-job.md).

## (Optional) Protect your model customization jobs using a VPC
<a name="vpc-model-customization"></a>

When you run a model customization job, the job accesses your Amazon S3 bucket to download the input data and to upload job metrics. To control access to your data, we recommend that you use a virtual private cloud (VPC) with [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html). You can further protect your data by configuring your VPC so that your data isn't available over the internet and instead creating a VPC interface endpoint with [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to establish a private connection to your data. For more information about how Amazon VPC and AWS PrivateLink integrate with Amazon Bedrock, see [Protect your data using Amazon VPC and AWS PrivateLink](usingVPC.md).

Do the following steps to configure and use a VPC for the training, validation, and output data for your model customization jobs.

**Topics**
+ [Set up VPC to protect your data during model customization](#vpc-cm-setup)
+ [Attach VPC permissions to a model customization role](#vpc-data-access-role)
+ [Add the VPC configuration when submitting a model customization job](#vpc-config)

### Set up VPC to protect your data during model customization
<a name="vpc-cm-setup"></a>

To set up a VPC, follow the steps at [Set up a VPC](usingVPC.md#create-vpc). You can further secure your VPC by setting up an S3 VPC endpoint and using resource-based IAM policies to restrict access to the S3 bucket containing your model customization data by following the steps at [(Example) Restrict data access to your Amazon S3 data using VPC](vpc-s3.md).

### Attach VPC permissions to a model customization role
<a name="vpc-data-access-role"></a>

After you finish setting up your VPC, attach the following permissions to your [model customization service role](model-customization-iam-role.md) to allow it to access the VPC. Modify this policy to allow access to only the VPC resources that your job needs. Replace the {{${{subnet-ids}}}} and {{security-group-id}} with the values from your VPC.

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
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface"
            ],
            "Resource": [
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:network-interface/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestTag/BedrockManaged": [
                        "true"
                    ]
                },
                "ArnEquals": {
                    "aws:RequestTag/BedrockModelCustomizationJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-customization-job/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface"
            ],
            "Resource": [
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{subnet-id}}",
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{subnet-id2}}",
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:security-group/{{security-group-id}}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteNetworkInterfacePermission"
            ],
            "Resource": "*",
            "Condition": {
                "ArnEquals": {
                    "ec2:Subnet": [
                        "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{subnet-id}}",
                        "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{subnet-id2}}"
                    ],
                    "ec2:ResourceTag/BedrockModelCustomizationJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-customization-job/*"
                    ]
                },
                "StringEquals": {
                    "ec2:ResourceTag/BedrockManaged": "true"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags"
            ],
            "Resource": "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:network-interface/*",
            "Condition": {
                "StringEquals": {
                    "ec2:CreateAction": [
                        "CreateNetworkInterface"
                    ]
                },
                "ForAllValues:StringEquals": {
                    "aws:TagKeys": [
                        "BedrockManaged",
                        "BedrockModelCustomizationJobArn"
                    ]
                }
            }
        }
    ]
}
```

------

### Add the VPC configuration when submitting a model customization job
<a name="vpc-config"></a>

After you configure the VPC and the required roles and permissions as described in the previous sections, you can create a model customization job that uses this VPC.

When you specify the VPC subnets and security groups for a job, Amazon Bedrock creates *elastic network interfaces* (ENIs) that are associated with your security groups in one of the subnets. ENIs allow the Amazon Bedrock job to connect to resources in your VPC. For information about ENIs, see [Elastic Network Interfaces](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_ElasticNetworkInterfaces.html) in the *Amazon VPC User Guide*. Amazon Bedrock tags ENIs that it creates with `BedrockManaged` and `BedrockModelCustomizationJobArn` tags.

We recommend that you provide at least one subnet in each Availability Zone.

You can use security groups to establish rules for controlling Amazon Bedrock access to your VPC resources.

You can configure the VPC to use in either the console or through the API. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

For the Amazon Bedrock console, you specify VPC subnets and security groups in the optional **VPC settings** section when you create the model customization job. For more information about configuring jobs, see [Submit a model customization job for fine-tuning](model-customization-submit.md).

**Note**  
For a job that includes VPC configuration, the console can't automatically create a service role for you. Follow the guidance at [Create a service role for model customization](model-customization-iam-role.md) to create a custom role.

------
#### [ API ]

When you submit a [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) request, you can include a `VpcConfig` as a request parameter to specify the VPC subnets and security groups to use, as in the following example.

```
"vpcConfig": { 
    "securityGroupIds": [
        "{{${{sg-0123456789abcdef0}}}}"
    ],
    "subnets": [
        "{{${{subnet-0123456789abcdef0}}}}",
        "{{${{subnet-0123456789abcdef1}}}}",
        "{{${{subnet-0123456789abcdef2}}}}"
    ]
}
```

------