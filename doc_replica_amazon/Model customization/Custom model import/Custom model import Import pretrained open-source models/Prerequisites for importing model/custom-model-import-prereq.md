

# Prerequisites for importing custom model
<a name="custom-model-import-prereq"></a>

Before you can start a custom model import job, you need to fulfill the following prerequisites:

1. If you are importing your model from Amazon S3 bucket, prepare your model files in the Hugging Face weights format. For more information see, [Import a model source from Amazon S3](model-customization-import-model.md#model-customization-import-model-source).

1. If you are using cross-account Amazon S3 or KMS keys, make sure to grant access to Amazon S3 bucket or the KMS key. For more information, see [Cross-account access to Amazon S3 bucket for custom model import jobs](cross-account-access-cmi.md).

1. (Optional) Create a custom AWS Identity and Access Management (IAM) [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) with the proper permissions by following the instructions at [Create a service role for importing pre-trained models](model-import-iam-role.md) to set up the role. You can skip this prerequisite if you plan to use the AWS Management Console to automatically create a service role for you.

1. (Optional) Set up extra security configurations.
   + You can encrypt input and output data, import jobs, or inference requests made to imported models. For more information see [Encryption of custom model import](https://docs.aws.amazon.com//bedrock/latest/userguide/encryption-import-model.html).
   + You can create a virtual private cloud (VPC) to protect your customization jobs. For more information, see [(Optional) Protect custom model import jobs using a VPC](vpc-custom-model-import.md).