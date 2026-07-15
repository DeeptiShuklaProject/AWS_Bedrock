

# Lambda Managed Instances quotas
<a name="lambda-managed-instances-quotas"></a>

This page describes the service quotas for AWS Lambda Managed Instances. These quotas are separate from AWS Lambda (default) quotas. Some quotas can be increased upon request.

In addition to the quotas listed on this page, Lambda Managed Instances are subject to [Amazon EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) applied to your account. Quotas that commonly affect Lambda Managed Instances customers include [EC2 instance type vCPU limits](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html), [Amazon EBS volume limits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-resource-quotas.html), and [available IP addresses in your VPC subnets](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html).

## Lambda API request quotas
<a name="lambda-managed-instances-api-request-quotas"></a>

These quotas control the rate at which you can make API calls to manage Lambda Managed Instances capacity providers. The read and write API rate limits apply to all capacity provider operations combined, including creating, updating, describing, and deleting capacity providers.


| Resource | Quota | 
| --- | --- | 
| The maximum combined rate (requests per second) for all capacity provider read APIs | 15 requests per second. Cannot be increased. | 
| The maximum combined rate (requests per second) for all capacity provider write APIs | 1 request per second. Cannot be increased. | 

## Lambda Managed Instances resource quotas
<a name="lambda-managed-instances-resource-quotas"></a>

These quotas define the limits for core Lambda Managed Instances resources within your AWS account. They govern the number of capacity providers you can create and the number of function versions that can be associated with each capacity provider.


| Resource | Quota | 
| --- | --- | 
| Capacity providers | 1,000. The maximum number of capacity providers created in an account. | 
| Function versions per capacity provider | 100. The maximum number of function versions per capacity provider. Cannot be increased. | 
| vCPUs per capacity provider | 15,000. The maximum number of vCPUs per capacity provider. | 

## Event source mapping quotas
<a name="lambda-managed-instances-event-source-quotas"></a>

These quotas control the throughput and configuration limits for processing events from various AWS services on Lambda Managed Instances. The throughput limits ensure predictable performance while the mapping count limits help maintain service stability. Event source mappings on Lambda Managed Instances support Amazon SQS, DynamoDB Streams, Amazon Kinesis Data Streams, Amazon MSK, and self-managed Apache Kafka as event sources.


| Resource | Quota | 
| --- | --- | 
| Standard SQS event source mapping throughput on Lambda Managed Instances | 5 MB per second. Cannot be increased. | 
| Standard Kafka event source mapping throughput on Lambda Managed Instances | 1 MB per second. Cannot be increased. | 
| Standard Kafka event source mappings on Lambda Managed Instances | 100 event source mappings. Cannot be increased. | 
| Kinesis event source mapping throughput on Lambda Managed Instances | 25 MB per second. Can be increased. | 
| DynamoDB event source mapping throughput on Lambda Managed Instances | 10 MB per second. Can be increased. | 
| Invoke request throughput for asynchronous invocations on Lambda Managed Instances | 5 MB per second. Can be increased. | 

## Requesting a quota increase
<a name="lambda-managed-instances-requesting-quota-increase"></a>

For quotas that can be increased, you can request an increase through the Service Quotas console.

**To request a quota increase**

1. Open the Service Quotas console at [console.aws.amazon.com/servicequotas/](http://console.aws.amazon.com/servicequotas/).

1. In the navigation pane, choose **AWS services**.

1. Choose **AWS Lambda**.

1. Select the quota you want to increase.

1. Choose **Request quota increase**.

1. Enter the new quota value and provide a justification for the increase.

1. Choose **Request**.

## Next steps
<a name="lambda-managed-instances-quotas-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)
+ Configure [VPC connectivity for your capacity providers](lambda-managed-instances-networking.md)