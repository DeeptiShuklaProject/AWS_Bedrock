

# Protect your data using Amazon VPC and AWS PrivateLink
<a name="usingVPC"></a>

To control access to your data, we recommend that you use a virtual private cloud (VPC) with [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html). Using a VPC protects your data and lets you monitor all network traffic in and out of the AWS job containers by using [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html).

You can further protect your data by configuring your VPC so that your data isn't available over the internet and instead creating a VPC interface endpoint with [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to establish a private connection to your data.

The following lists some features of Amazon Bedrock in which you can use VPC to protect your data:
+ Model customization – [(Optional) Protect your model customization jobs using a VPC](custom-model-job-access-security.md#vpc-model-customization)
+ Batch inference – [Protect batch inference jobs using a VPC](batch-vpc.md)
+ Amazon Bedrock Knowledge Bases – [Access Amazon OpenSearch Serverless using an interface endpoint (AWS PrivateLink)](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vpc.html)

## Set up a VPC
<a name="create-vpc"></a>

You can use a [default VPC](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html) or create a new VPC by following the guidance at [Get started with Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-getting-started.html) and [Create a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html).

When you create your VPC, we recommend that you use the default DNS settings for your endpoint route table, so that standard Amazon S3 URLs (for example, `http://s3-aws-region.amazonaws.com/{{training-bucket}}`) resolve.

The following topics show how to set up VPC endpoint with the help of AWS PrivateLink and an example use case for using VPC to protect access to your S3 files.

**Topics**
+ [Set up a VPC](#create-vpc)
+ [Use interface VPC endpoints (AWS PrivateLink) to create a private connection between your VPC and Amazon Bedrock](vpc-interface-endpoints.md)
+ [(Example) Restrict data access to your Amazon S3 data using VPC](vpc-s3.md)