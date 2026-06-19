

# Create a custom service role for batch inference
<a name="batch-iam-sr"></a>

To use a custom service role for batch inference instead of the one Amazon Bedrock automatically creates for you in the AWS Management Console, create an IAM role and attach the following permissions by following the steps at [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

**Topics**
+ [Trust relationship](#batch-iam-sr-trust)
+ [Identity-based permissions for the batch inference service role.](#batch-iam-sr-identity)

## Trust relationship
<a name="batch-iam-sr-trust"></a>

The following trust policy allows Amazon Bedrock to assume this role and submit and manage batch inference jobs. Replace the {{values}} as necessary. The policy contains optional condition keys (see [Condition keys for Amazon Bedrock](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys) and [AWS global condition context keys](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-policy-keys)) in the `Condition` field that we recommend you use as a security best practice.

**Note**  
As a best practice for security purposes, replace the {{\*}} with specific batch inference job IDs after you have created them.

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
                    "aws:SourceArn": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-invocation-job/{{*}}"
                }
            }
        }
    ]
}
```

------

## Identity-based permissions for the batch inference service role.
<a name="batch-iam-sr-identity"></a>

The following topics describe and provide examples of permissions policies that you might need to attach to your custom batch inference service role, depending on your use case.

**Topics**
+ [(Required) Permissions to access input and output data in Amazon S3](#batch-iam-sr-s3)
+ [(Optional) Permissions to run batch inference with inference profiles](#batch-iam-sr-ip)

### (Required) Permissions to access input and output data in Amazon S3
<a name="batch-iam-sr-s3"></a>

To allow a service role to access the Amazon S3 bucket containing your input data and the bucket to which to write your output data, attach the following policy to the service role. Replace {{values}} as necessary.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
         "Sid": "S3Access",
         "Effect": "Allow",
         "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket"
         ],
         "Resource": [
            "arn:aws:s3:::{{${InputBucket}}}",
            "arn:aws:s3:::{{${InputBucket}/*}}",
            "arn:aws:s3:::{{${OutputBucket}}}",
            "arn:aws:s3:::{{${OutputBucket}/*}}"
         ],
         "Condition": {
            "StringEquals": {
                "aws:ResourceAccount": [
                    "{{123456789012}}"
                ]
            }
         }
        }
    ]
}
```

------

### (Optional) Permissions to run batch inference with inference profiles
<a name="batch-iam-sr-ip"></a>

To run batch inference with an [inference profile](inference-profiles.md), a service role must have permissions to invoke the inference profile in an AWS Region, in addition to the model in each Region in the inference profile.

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

For permissions to invoke with an application inference profile, use the following policy as a template for the permissions policy to attach to your service role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "ApplicationInferenceProfile",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:application-inference-profile/{{${InferenceProfileId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}",
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/{{${ModelId}}}"
            ]
        }
    ]
}
```

------