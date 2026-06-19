

# Protect batch inference jobs using a VPC
<a name="batch-vpc"></a>

When you run a batch inference job, the job accesses your Amazon S3 bucket to download the input data and to write the output data. To control access to your data, we recommend that you use a virtual private cloud (VPC) with [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html). You can further protect your data by configuring your VPC so that your data isn't available over the internet and instead creating a VPC interface endpoint with [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to establish a private connection to your data. For more information about how Amazon VPC and AWS PrivateLink integrate with Amazon Bedrock, see [Protect your data using Amazon VPC and AWS PrivateLink](usingVPC.md).

Carry out the following steps to configure and use a VPC for the input prompts and output model responses for your batch inference jobs.

**Topics**
+ [Set up VPC to protect your data during batch inference](#batch-vpc-setup)
+ [Attach VPC permissions to a batch inference role](#batch-vpc-role)
+ [Add the VPC configuration when submitting a batch inference job](#batch-vpc-config)

## Set up VPC to protect your data during batch inference
<a name="batch-vpc-setup"></a>

To set up a VPC, follow the steps at [Set up a VPC](usingVPC.md#create-vpc). You can further secure your VPC by setting up an S3 VPC endpoint and using resource-based IAM policies to restrict access to the S3 bucket containing your batch inference data by following the steps at [(Example) Restrict data access to your Amazon S3 data using VPC](vpc-s3.md).

## Attach VPC permissions to a batch inference role
<a name="batch-vpc-role"></a>

After you finish setting up your VPC, attach the following permissions to your [batch inference service role](batch-iam-sr.md) to allow it to access the VPC. Modify this policy to allow access to only the VPC resources that your job needs. Replace the {{subnet-ids}} and {{security-group-id}} with the values from your VPC.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "2",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface"
            ],
            "Resource": [
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:network-interface/*",
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{${{subnet-id}}}}",
                "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:security-group/{{${{security-group-id}}}}"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestTag/BedrockManaged": [
                        "true"
                    ]
                },
                "ArnEquals": {
                    "aws:RequestTag/BedrockModelInvocationJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-invocation-job/*"
                    ]
                }
            }
        },
        {
            "Sid": "3",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteNetworkInterfacePermission"
            ],
            "Resource": [
                "*"
            ],
            "Condition": {
                "StringEquals": {
                    "ec2:Subnet": [
                        "arn:aws:ec2:{{us-east-1}}:{{123456789012}}:subnet/{{${{subnet-id}}}}"
                    ]
                },
                "ArnEquals": {
                    "ec2:ResourceTag/BedrockModelInvocationJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-invocation-job/*"
                    ]
                }
            }
        },
        {
            "Sid": "4",
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
                        "BedrockModelInvocationJobArn"
                    ]
                }
            }
        }
    ]
}
```

------

## Add the VPC configuration when submitting a batch inference job
<a name="batch-vpc-config"></a>

After you configure the VPC and the required roles and permissions as described in the previous sections, you can create a batch inference job that uses this VPC.

**Note**  
Currently, when creating a batch inference job, you can only use a VPC through the API.

When you specify the VPC subnets and security groups for a job, Amazon Bedrock creates *elastic network interfaces* (ENIs) that are associated with your security groups in one of the subnets. ENIs allow the Amazon Bedrock job to connect to resources in your VPC. For information about ENIs, see [Elastic Network Interfaces](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_ElasticNetworkInterfaces.html) in the *Amazon VPC User Guide*. Amazon Bedrock tags ENIs that it creates with `BedrockManaged` and `BedrockModelInvocationJobArn` tags.

We recommend that you provide at least one subnet in each Availability Zone.

You can use security groups to establish rules for controlling Amazon Bedrock access to your VPC resources.

When you submit a [CreateModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelInvocationJob.html) request, you can include a `VpcConfig` as a request parameter to specify the VPC subnets and security groups to use, as in the following example.

```
"vpcConfig": { 
    "securityGroupIds": [
        "{{sg-0123456789abcdef0}}"
    ],
    "subnets": [
        "{{subnet-0123456789abcdef0}}",
        "{{subnet-0123456789abcdef1}}",
        "{{subnet-0123456789abcdef2}}"
    ]
}
```