

# Create a model evaluation job that uses an LLM as a judge
<a name="model-evaluation-judge-create"></a>

You can create a model evaluation job using the AWS Management Console, AWS CLI, or a supported AWS SDK.

This type of job requires access to an evaluator model. If you are evaluating the performance of an Amazon Bedrock model, you need access to that model as well. Both models must be available in the same AWS Region. For a list of supported generator and evaluator models, see [Supported models](evaluation-judge.md#evaluation-judge-supported).

## Prerequisites
<a name="model-evaluation-judge-create-prereqs"></a>

In addition to having access to at least one evaluator model, to create an evaluation job that uses an LLM as a judge, you also need certain IAM service role permissions. To learn more about the necessary actions and trust policy requirements, see [Required service role permissions for creating a model evaluation job that uses a judge model](judge-service-roles.md).

When you create the job, you specify a prompt dataset in an Amazon S3 bucket, and an output bucket to store your results in. CORS configuration is not required for LLM-as-a-judge evaluation jobs. For human-based evaluation jobs, see [Required Cross Origin Resource Sharing (CORS) permissions on S3 buckets](model-evaluation-security-cors.md)

To create a job in the console, the console needs permission to perform a certain set of actions and have access to the needed resources. The following policy defines a minimum set of IAM permissions required to create a job in the console. In the policy, we recommend using the IAM JSON policy element [Resource](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html) to limit access to only the models and buckets required for the IAM user, group, or role.

The IAM policy must grant access to both generator and evaluator models.

### Required console permissions
<a name="model-evaluation-judge-create-prereqs-permissions"></a>

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "BedrockConsole",
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateEvaluationJob",
                "bedrock:GetEvaluationJob",
                "bedrock:ListEvaluationJobs",
                "bedrock:StopEvaluationJob",
                "bedrock:GetCustomModel",
                "bedrock:ListCustomModels",
                "bedrock:CreateProvisionedModelThroughput",
                "bedrock:UpdateProvisionedModelThroughput",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:GetImportedModel",
                "bedrock:ListImportedModels",
                "bedrock:ListTagsForResource",
                "bedrock:UntagResource",
                "bedrock:TagResource"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-west-2}}::foundation-model/*;"
            ]
        },
        {
            "Sid": "AllowConsoleS3AccessForModelEvaluation",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetBucketCORS",
                "s3:ListBucket",
                "s3:ListBucketVersions",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::{{amzn-s3-demo-destination-bucket}}/*",
                "arn:aws:s3:::{{input_datasets/prompts.jsonl}}"
            ]
        }
    ]
}
```

------

**Note**  
This example policy gives permissions for all Amazon Bedrock foundation models. In a production environment, we recommend that you follow the principal of [least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege) and only grant permissions for the models you need.

You can create an evaluation job using only Amazon Bedrock's built-in metrics, or you can create a job that uses your own custom metrics. See the following sections for instructions on creating model evaluation jobs.

**Topics**
+ [Prerequisites](#model-evaluation-judge-create-prereqs)
+ [Create a model evaluation job using built-in metrics](model-evaluation-built-in-metrics.md)
+ [Create a model evaluation job using custom metrics](model-evaluation-custom-metrics-create-job.md)