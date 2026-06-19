

# (Optional) Protect custom model import jobs using a VPC
<a name="vpc-custom-model-import"></a>

When you run a custom model import job, the job accesses your Amazon S3 bucket to download the input data and to upload job metrics. To control access to your data, we recommend that you use a virtual private cloud (VPC) with [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html). You can further protect your data by configuring your VPC so that your data isn't available over the internet and instead creating a VPC interface endpoint with [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to establish a private connection to your data. For more information about how Amazon VPC and AWS PrivateLink integrate with Amazon Bedrock, see [Protect your data using Amazon VPC and AWS PrivateLink](usingVPC.md).

Carry out the following steps to configure and use a VPC for importing your custom models.

**Topics**
+ [Set up a VPC](#create-vpc-cmi)
+ [Create an Amazon S3 VPC Endpoint](#train-vpc-s3-cmi)
+ [(Optional) Use IAM policies to restrict access to your S3 files](#train-vpc-policy-cmi)
+ [Attach VPC permissions to a custom model import role.](#vpc-data-access-role-cmi)
+ [Add the VPC configuration when submitting a model import job](#vpc-config-cmi)

## Set up a VPC
<a name="create-vpc-cmi"></a>

You can use a [default VPC](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html) for your model import data or create a new VPC by following the guidance at [Get started with Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-getting-started.html) and [Create a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html).

When you create your VPC, we recommend that you use the default DNS settings for your endpoint route table, so that standard Amazon S3 URLs (for example, `http://s3-aws-region.amazonaws.com/{{model-bucket}}`) resolve.

## Create an Amazon S3 VPC Endpoint
<a name="train-vpc-s3-cmi"></a>

If you configure your VPC with no internet access, you need to create an [Amazon S3 VPC endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) to allow your model import jobs to access the S3 buckets that store your training and validation data and that will store the model artifacts.

Create the S3 VPC endpoint by following the steps at [Create a gateway endpoint for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#create-gateway-endpoint-s3).

**Note**  
If you don't use the default DNS settings for your VPC, you need to ensure that the URLs for the locations of the data in your training jobs resolve by configuring the endpoint route tables. For information about VPC endpoint route tables, see [Routing for Gateway endpoints](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpce-gateway.html#vpc-endpoints-routing).

## (Optional) Use IAM policies to restrict access to your S3 files
<a name="train-vpc-policy-cmi"></a>

You can use [resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html) to more tightly control access to your S3 files. You can the following type of resource-based policy.
+ **Endpoint policies** – Endpoint policies restrict access through the VPC endpoint. The default endpoint policy allows full access to Amazon S3 for any user or service in your VPC. While creating or after you create the endpoint, you can optionally attach a resource-based policy to the endpoint to add restrictions, such as only allowing the endpoint to access a specific bucket or only allowing a specific IAM role to access the endpoint. For examples, see [Edit the VPC endpoint policy](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#edit-vpc-endpoint-policy-s3).

  The following is an example policy you can attach to your VPC endpoint to only allow it to access the bucket containing your model weights.

------
#### [ JSON ]

****  

  ```
  {
      "Version":"2012-10-17",		 	 	 
      "Statement": [
          {
              "Sid": "RestrictAccessToModelWeightsBucket",
              "Effect": "Allow",
              "Principal": "*",
              "Action": [
                  "s3:GetObject",
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::{{model-weights-bucket}}",
                  "arn:aws:s3:::{{model-weights-bucket/*}}"
              ]
          }
      ]
  }
  ```

------

## Attach VPC permissions to a custom model import role.
<a name="vpc-data-access-role-cmi"></a>

After you finish setting up your VPC and endpoint, you need to attach the following permissions to your [model import IAM role](model-import-iam-role.md). Modify this policy to allow access to only the VPC resources that your job needs. Replace the {{subnet-ids}} and {{security-group-id}} with the values from your VPC.

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
                    "aws:RequestTag/BedrockModelImportJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-import-job/*"
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
                    "ec2:ResourceTag/BedrockModelImportJobArn": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:model-import-job/*"
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
                        "BedrockModelImportJobArn"
                    ]
                }
            }
        }
    ]
}
```

------

## Add the VPC configuration when submitting a model import job
<a name="vpc-config-cmi"></a>

After you configure the VPC and the required roles and permissions as described in the previous sections, you can create a model import job that uses this VPC.

When you specify the VPC subnets and security groups for a job, Amazon Bedrock creates *elastic network interfaces* (ENIs) that are associated with your security groups in one of the subnets. ENIs allow the Amazon Bedrock job to connect to resources in your VPC. For information about ENIs, see [Elastic Network Interfaces](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_ElasticNetworkInterfaces.html) in the *Amazon VPC User Guide*. Amazon Bedrock tags ENIs that it creates with `BedrockManaged` and `BedrockModelImportJobArn` tags. 

We recommend that you provide at least one subnet in each Availability Zone.

You can use security groups to establish rules for controlling Amazon Bedrock access to your VPC resources.

You can configure the VPC to use in either the console or through the API. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

For the Amazon Bedrock console, you specify VPC subnets and security groups in the optional **VPC settings** section when you create the model import job. For more information about configuring model import jobs, see [Submit a model import job](model-customization-import-model-job.md).

------
#### [ API ]

When you submit a [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) request, you can include a `VpcConfig` as a request parameter to specify the VPC subnets and security groups to use, as in the following example.

```
"VpcConfig": { 
"SecurityGroupIds": [
    "{{sg-0123456789abcdef0}}"
    ],
    "Subnets": [
          "{{subnet-0123456789abcdef0}}",
          "{{subnet-0123456789abcdef1}}",
          "{{subnet-0123456789abcdef2}}"
     ]
 }
```

------