

# Prerequisites for model distillation
<a name="prequisites-model-distillation"></a>

Before you can begin, make sure that you understand access and security controls for Model Distillation. You must also choose a teacher and student model for your distillation job.

## Permissions
<a name="model-distillation-access-security"></a>

Before you can begin, make sure that you understand access and security controls for Model Distillation. You must have an IAM service role that can access the Amazon S3 bucket where you want to store your Model Distillation training and validation data. Amazon Bedrock also has options for encrypting and further securing your distillation jobs and artifacts. For more information, see [Model customization access and security](custom-model-job-access-security.md). 

To use a cross-region inference profile for a teacher model in a Distillation job, your service role must have permissions to invoke the inference profile in an AWS Region, in addition to the model in each Region in the inference profile. For a policy example, see [(Optional) Permissions to create a Distillation job with a cross-region inference profile](custom-model-job-access-security.md#custom-models-cross-region-inference-profile-permissions). For more information about cross-region inference, see [Increase throughput with cross-Region inference](cross-region-inference.md).

## Choose teacher and student models for distillation
<a name="prequisites-teacher-student-models"></a>


****  

| Model Type | Selection Criteria | Key Considerations | Requirements | 
| --- | --- | --- | --- | 
| Teacher Model | Choose a teacher model that's significantly larger and more capable than the student model, and whose accuracy you want to achieve for your use case. | To make distillation more effective, choose a model that's already trained on tasks similar to your use case. For some teacher models, you can choose a Cross-Region inference profile. | Must have permissions to invoke inference profiles and models in each Region. See cross-region inference documentation for policy examples. | 
| Student Model | Choose a student model that's significantly smaller in size than the teacher model. | The student model must be one of the student models paired with your teacher model in the supported models table. | Must be compatible with selected teacher model as shown in the following table. | 

The following section lists the supported models and regions for Amazon Bedrock Model Distillation. After you choose your teacher and student models, you prepare and optimize your training datasets for distillation. For more information, see [Prepare your training datasets for distillation](distillation-prepare-datasets.md).

### Supported models and Regions for Amazon Bedrock Model Distillation
<a name="model-distillation-supported"></a>

The following table shows which models and AWS Regions Amazon Bedrock Model Distillation supports for teacher and student models. If you use a Cross Region Inference Profile, only System Inference Profiles are supported for model distillation. For more information, see [Increase throughput with cross-Region inference](cross-region-inference.md). 

**Important**  
Distillation is not currently available for Anthropic models on Amazon Bedrock. There is no confirmed timeline for when Anthropic distillation will be restored. For currently supported teacher–student combinations, see the table below.


****  


- **Amazon**
  - **Teacher:** Nova Pro / **Teacher ID:** amazon.nova-pro-v1:0 / **Inference profile support:** Both / **Student:** Nova Lite<br />Nova Micro / **Student ID:** amazon.nova-lite-v1:0:300k<br />amazon.nova-micro-v1:0:128k / **Region:** US East (N. Virginia)
  - **Teacher:** Nova Premier / **Teacher ID:** amazon.nova-premier-v1:0 / **Inference profile support:** Inference profile only / **Student:** Nova Lite<br />Nova Micro<br />Nova Pro / **Student ID:** amazon.nova-lite-v1:0:300k<br />amazon.nova-micro-v1:0:128k<br />amazon.nova-pro-v1:0:300k / **Region:** US East (N. Virginia)

- **Meta**
  - **Teacher:** Llama 3.1 405B / **Teacher ID:** meta.llama3-1-405b-instruct-v1:0 / **Inference profile support:** On demand / **Student:** Llama 3.1 8B<br />Llama 3.1 70B<br />Llama 3.2 1B<br />Llama 3.3 70B / **Student ID:** meta.llama3-1-8b-instruct-v1:0:128k<br />meta.llama3-1-70b-instruct-v1:0:128k<br />meta.llama3-2-1b-instruct-v1:0:128k<br />meta.llama3-3-70b-instruct-v1:0:128k / **Region:** US West (Oregon)
  - **Teacher:** Llama 3.1 70B / **Teacher ID:** meta.llama3-1-70b-instruct-v1:0 / **Inference profile support:** Both / **Student:** Llama 3.1 8B<br />Llama 3.2 1B<br />Llama 3.2 3B / **Student ID:** meta.llama3-1-8b-instruct-v1:0:128k<br />meta.llama3-2-1b-instruct-v1:0:128k<br />meta.llama3-2-3b-instruct-v1:0:128k / **Region:** US West (Oregon)
  - **Teacher:** Llama 3.3 70B / **Teacher ID:** meta.llama3-3-70b-instruct-v1:0 / **Inference profile support:** Inference profile only / **Student:** Llama 3.1 8B<br />Llama 3.2 1B<br />Llama 3.2 3B / **Student ID:** meta.llama3-1-8b-instruct-v1:0:128k<br />meta.llama3-2-1b-instruct-v1:0:128k<br />meta.llama3-2-3b-instruct-v1:0:128k / **Region:** US West (Oregon)



**Note**  
For Claude  and Llama models, the distillation job is run in US West (Oregon). You can either buy [provisioned throughput](https://docs.aws.amazon.com//bedrock/latest/userguide/prov-throughput.html) in US West (Oregon) or [copy distilled model](https://docs.aws.amazon.com//bedrock/latest/userguide/copy-model.html) to another Region and then buy [provisioned throughput](https://docs.aws.amazon.com//bedrock/latest/userguide/prov-throughput.html).