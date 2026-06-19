

# (Example) Restrict data access to your Amazon S3 data using VPC
<a name="vpc-s3"></a>

You can use a VPC to restrict access to data in your Amazon S3 buckets. For further security, you can configure your VPC with no internet access and create an endpoint for it with AWS PrivateLink. You can also restrict access by attaching resource-based policies to the VPC endpoint or to the S3 bucket.

**Topics**
+ [Create an Amazon S3 VPC Endpoint](#vpc-s3-create)
+ [(Optional) Use IAM policies to restrict access to your S3 files](#vpc-policy-rbp)

## Create an Amazon S3 VPC Endpoint
<a name="vpc-s3-create"></a>

If you configure your VPC with no internet access, you need to create an [Amazon S3 VPC endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) to allow your model customization jobs to access the S3 buckets that store your training and validation data and that will store the model artifacts.

Create the S3 VPC endpoint by following the steps at [Create a gateway endpoint for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#create-gateway-endpoint-s3).

**Note**  
If you don't use the default DNS settings for your VPC, you need to ensure that the URLs for the locations of the data in your training jobs resolve by configuring the endpoint route tables. For information about VPC endpoint route tables, see [Routing for Gateway endpoints](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpce-gateway.html#vpc-endpoints-routing).

## (Optional) Use IAM policies to restrict access to your S3 files
<a name="vpc-policy-rbp"></a>

You can use [resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html) to more tightly control access to your S3 files. You can use any combination of the following types of resource-based policies.
+ **Endpoint policies** – You can attach endpoint policies to your VPC endpoint to restrict access through the VPC endpoint. The default endpoint policy allows full access to Amazon S3 for any user or service in your VPC. While creating or after you create the endpoint, you can optionally attach a resource-based policy to the endpoint to add restrictions, such as only allowing the endpoint to access a specific bucket or only allowing a specific IAM role to access the endpoint. For examples, see [Edit the VPC endpoint policy](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#edit-vpc-endpoint-policy-s3).

  The following is an example policy you can attach to your VPC endpoint to only allow it to access the bucket that you specify.

------
#### [ JSON ]

****  

  ```
  {
      "Version":"2012-10-17",		 	 	 
      "Statement": [
          {
              "Sid": "RestrictAccessToTrainingBucket",
              "Effect": "Allow",
              "Principal": "*",
              "Action": [
                  "s3:GetObject",
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::{{bucket}}",
                  "arn:aws:s3:::{{bucket/*}}"
              ]
          }
      ]
  }
  ```

------
+ **Bucket policies** – You can attach a bucket policy to an S3 bucket to restrict access to it. To create a bucket policy, follow the steps at [Using bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html). To restrict access to traffic that comes from your VPC, you can use condition keys to specify the VPC itself, a VPC endpoint, or the IP address of the VPC. You can use the [aws:sourceVpc](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcevpc), [aws:sourceVpce](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcevpce), or [aws:VpcSourceIp](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-vpcsourceip) condition keys.

  The following is an example policy you can attach to an S3 bucket to deny all traffic to the bucket unless it comes from your VPC.

------
#### [ JSON ]

****  

  ```
  {
      "Version":"2012-10-17",		 	 	 
      "Statement": [
          {
              "Sid": "RestrictAccessToOutputBucket",
              "Effect": "Deny",
              "Principal": "*",
              "Action": [
                  "s3:GetObject",
                  "s3:PutObject",
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::{{bucket}}",
                  "arn:aws:s3:::{{bucket/*}}"
              ],
              "Condition": {
                  "StringNotEquals": {
                      "aws:sourceVpc": "{{vpc-11223344556677889}}"
                  }
              }
          }
      ]
  }
  ```

------

  For more examples, see [Control access using bucket policies](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#bucket-policies-s3).