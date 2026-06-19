

# Increase model invocation capacity with Provisioned Throughput in Amazon Bedrock
<a name="prov-throughput"></a>

**Throughput** refers to the number and rate of inputs and outputs that a model processes and returns. You can purchase **Provisioned Throughput** to provision a higher level of throughput for a model at a fixed cost. If you customized a model, you must purchase Provisioned Throughput to be able to use it.

You're billed hourly for a Provisioned Throughput that you purchase. For detailed information about pricing, see [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing). The price per hour depends on the following factors:

1. The model that you choose (for custom models, pricing is the same as the base model that it was customized from).

1. The number of Model Units (MUs) that you specify for the Provisioned Throughput. An MU delivers a specific throughput level for the specified model. The throughput level of an MU specifies the following:
   + The number of input tokens that an MU can process across all requests within a span of one minute. 
   + The number of output tokens that an MU can generate across all requests within a span of one minute.
**Note**  
For more information about what an MU specifies, pricing per MU, and to request limit increases, contact your AWS account manager.

1. The duration of time you commit to keeping the Provisioned Throughput. The longer the commitment duration, the more discounted the hourly price becomes. You can choose between the following levels of commitment:
   + No commitment – You can delete the Provisioned Throughput at any time.
   + 1 month – You can't delete the Provisioned Throughput until the one month commitment term is over.
   + 6 months – You can't delete the Provisioned Throughput until the six month commitment term is over.
**Note**  
Billing continues until you delete the Provisioned Throughput.

The following steps outline the process of setting up and using Provisioned Throughput.

1. Determine the number of MUs you wish to purchase for a Provisioned Throughput and the amount of time for which you want to commit to using the Provisioned Throughput.

1. Purchase Provisioned Throughput for a base or custom model.

1. After the provisioned model is created, you can use it to [run model inference](inference.md).

**Topics**
+ [Supported Region and models for Provisioned Throughput](prov-thru-supported.md)
+ [Prerequisites for Provisioned Throughput](prov-thru-prereq.md)
+ [Purchase a Provisioned Throughput for an Amazon Bedrock model](prov-thru-purchase.md)
+ [View information about a Provisioned Throughput](prov-thru-info.md)
+ [Modify a Provisioned Throughput](prov-thru-edit.md)
+ [Use a Provisioned Throughput with an Amazon Bedrock resource](prov-thru-use.md)
+ [Delete a Provisioned Throughput or cancel auto renew](prov-thru-delete.md)
+ [Code examples for Provisioned Throughput](prov-thru-code-examples.md)