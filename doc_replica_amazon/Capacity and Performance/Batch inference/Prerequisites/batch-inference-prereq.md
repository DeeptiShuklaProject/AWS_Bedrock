

# Prerequisites for batch inference
<a name="batch-inference-prereq"></a>

To perform batch inference, you must fulfill the following prerequisites:

1. Prepare your dataset and upload it to an Amazon S3 bucket.

1. Create an S3 bucket for your output data.

1. Set up batch inference-related permissions for the relevant IAM identities.

1. (Optional) Set up a VPC to protect the data in your S3 while carrying out batch inference. You can skip this step if you don't need to use a VPC.

To learn how to fulfill these prerequisites, navigate through the following topics:

**Topics**
+ [Format and upload your batch inference data](batch-inference-data.md)
+ [Required permissions for batch inference](batch-inference-permissions.md)
+ [Protect batch inference jobs using a VPC](batch-vpc.md)