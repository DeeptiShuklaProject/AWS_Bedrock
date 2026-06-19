

# Creating your first model evaluation that uses human workers
<a name="model-evaluation-type-human"></a>

A model evaluation job that uses human workers requires access to the following service level resources. Use the linked topics to learn more about getting setting up.

**Required service level resources to start a model evaluation job that uses human workers**

1. Model evaluation jobs that use human workers allow you to rate/compare the responses for up two different foundation models. To start a job, at least one Amazon Bedrock foundation model is required. To learn more accessing Amazon Bedrock foundation models, see [Request access to models](model-access.md).

1. To create a model evaluation job using human workers, you need access to the [https://console.aws.amazon.com/bedrock/](https://console.aws.amazon.com/bedrock/), AWS Command Line Interface, or a supported AWS SDK. To learn more about the required IAM actions and resources, see [Required console permissions to create a human-based model evaluation job](#more-for-human).

1. When the model evaluation job starts, a service role is used to perform actions on your behalf. To learn more about required IAM actions and the trust policy requirements, see [Service role requirements for automatic model evaluation jobs](automatic-service-roles.md).

1. A prompt dataset is required to start the model evaluation job; it must be stored in a Amazon S3 bucket. To learn more about the prompt dataset requirements, see [Create a custom prompt dataset for a model evaluation job that uses human workers](model-evaluation-prompt-datasets-custom-human.md) 

1. The human evaluators are managed as a workteam. You can create a new Amazon Cognito managed workteam using the Amazon Bedrock console. To learn more about managing your workforce, see [Manage a work team for human evaluations of models in Amazon Bedrock](human-worker-evaluations.md). 

## Required console permissions to create a human-based model evaluation job
<a name="more-for-human"></a>

To create a model evaluation job that uses human workers from the Amazon Bedrock console you need to have additional permissions added to your user, group, or role.

The following policy contains the minimum set of IAM actions and resources in Amazon Bedrock, Amazon SageMaker AI, Amazon Cognito and Amazon S3 that are required to create a human-based model evaluation job using the Amazon Bedrock console.

------
#### [ JSON ]

****  

```
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid": "AllowPassingConsoleCreatedServiceRoles",
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": [
        "arn:aws:iam::111122223333:role/service-role/Amazon-Bedrock-IAM-Role-*"
      ],
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "bedrock.amazonaws.com"
        }
      }
    },
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
        "arn:aws:bedrock:us-west-2::foundation-model/model-id-of-foundational-model",
        "arn:aws:bedrock:us-west-2:111122223333:inference-profile/*",
        "arn:aws:bedrock:us-west-2:111122223333:provisioned-model/*",
        "arn:aws:bedrock:us-west-2:111122223333:imported-model/*"
      ]
    },
    {
      "Sid": "AllowCognitionActionsForWorkTeamCreations",
      "Effect": "Allow",
      "Action": [
        "cognito-idp:CreateUserPool",
        "cognito-idp:CreateUserPoolClient",
        "cognito-idp:CreateGroup",
        "cognito-idp:AdminCreateUser",
        "cognito-idp:AdminAddUserToGroup",
        "cognito-idp:CreateUserPoolDomain",
        "cognito-idp:UpdateUserPool",
        "cognito-idp:ListUsersInGroup",
        "cognito-idp:ListUsers",
        "cognito-idp:AdminRemoveUserFromGroup"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowModelEvaluationResourceCreation",
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateFlowDefinition",
        "sagemaker:CreateWorkforce",
        "sagemaker:CreateWorkteam",
        "sagemaker:DescribeFlowDefinition",
        "sagemaker:DescribeHumanLoop",
        "sagemaker:ListFlowDefinitions",
        "sagemaker:ListHumanLoops",
        "sagemaker:DescribeWorkforce",
        "sagemaker:DescribeWorkteam",
        "sagemaker:ListWorkteams",
        "sagemaker:ListWorkforces",
        "sagemaker:DeleteFlowDefinition",
        "sagemaker:DeleteHumanLoop",
        "sagemaker:RenderUiTemplate",
        "sagemaker:StartHumanLoop",
        "sagemaker:StopHumanLoop"
      ],
      "Resource": "*"
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
        "arn:aws:s3:::my_output_bucket",
        "arn:aws:s3:::input_datasets/prompts.jsonl"
      ]
    }
  ]
}
```

------