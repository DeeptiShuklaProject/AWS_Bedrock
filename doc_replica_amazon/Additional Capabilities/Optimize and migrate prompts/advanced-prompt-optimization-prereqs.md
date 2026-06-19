

# Prerequisites and permissions
<a name="advanced-prompt-optimization-prereqs"></a>

## Prerequisites
<a name="advanced-prompt-optimization-prereqs-overview"></a>

When you submit an Advanced Prompt Optimization job, Amazon Bedrock accesses resources in your account on your behalf using the permissions of your calling identity. The IAM user or role that you use to call the API or access AWS console must have permissions to:
+ Manage Advanced Prompt Optimization jobs
+ Invoke the target foundation models
+ Read input data from and write results to your Amazon S3 bucket
+ (Optional) Use your AWS KMS key, to encrypt job output with a customer-managed key (CMK) or to access S3 buckets that use CMK
+ (Optional) Invoke your Lambda function for custom evaluation

## Required IAM permissions
<a name="advanced-prompt-optimization-prereqs-iam"></a>

### API permissions
<a name="advanced-prompt-optimization-prereqs-api"></a>

Each Advanced Prompt Optimization API requires a specific IAM action on the job resource:


| API Operation | IAM Action | Resource | Access Level | 
| --- | --- | --- | --- | 
| CreateAdvancedPromptOptimizationJob | bedrock:CreateAdvancedPromptOptimizationJob | arn:aws:bedrock:{{region}}:{{account-id}}:advanced-prompt-optimization-job/\* | Write | 
| GetAdvancedPromptOptimizationJob | bedrock:GetAdvancedPromptOptimizationJob | arn:aws:bedrock:{{region}}:{{account-id}}:advanced-prompt-optimization-job/\* | Read | 
| ListAdvancedPromptOptimizationJobs | bedrock:ListAdvancedPromptOptimizationJobs | arn:aws:bedrock:{{region}}:{{account-id}}:advanced-prompt-optimization-job/\* | List | 
| StopAdvancedPromptOptimizationJob | bedrock:StopAdvancedPromptOptimizationJob | arn:aws:bedrock:{{region}}:{{account-id}}:advanced-prompt-optimization-job/\* | Write | 
| BatchDeleteAdvancedPromptOptimization Jobs | bedrock:BatchDeleteAdvancedPromptOptimization Job | arn:aws:bedrock:{{region}}:{{account-id}}:advanced-prompt-optimization-job/\* | Write | 

### Model invocation permissions
<a name="advanced-prompt-optimization-prereqs-model"></a>

When you create a job, Advanced Prompt Optimization invokes the target model(s) on your behalf using your caller credentials (Forward Access Session). Your IAM identity must have permission to invoke the specified models:


| Inference Path | IAM Action Required | Resource ARN | 
| --- | --- | --- | 
| ConverseStream (current) | bedrock:InvokeModelWithResponseStream | arn:aws:bedrock:{{region}}::foundation-model/{{model-id}} | 
| Converse (non-streaming) | bedrock:InvokeModel | arn:aws:bedrock:{{region}}::foundation-model/{{model-id}} | 
| Cross-region inference profile | bedrock:InvokeModelWithResponseStream | arn:aws:bedrock:\*:{{account-id}}:inference-profile/{{profile-id}} | 

**Important**  
If model access is not enabled for a model in your account, the job fails. The error message is: "No inference API is accessible for model. Verify that the role has permission to invoke the model."

### Amazon S3 bucket permissions
<a name="advanced-prompt-optimization-prereqs-s3"></a>

Your calling identity must have read access to the input dataset and write access to the output location. The S3 bucket must be in the same Region as the job.

```
{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:PutObject"
    ],
    "Resource": "arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"
},
{
    "Effect": "Allow",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::DOC-EXAMPLE-BUCKET"
}
```

If your S3 bucket uses CMK encryption, see the Encryption with AWS KMS section for the required KMS permissions.

### Encryption with AWS KMS (optional)
<a name="advanced-prompt-optimization-prereqs-kms"></a>

You can use AWS KMS customer-managed keys (CMKs) with Advanced Prompt Optimization in two ways:
+ **Job output encryption** – Encrypt optimization results with your CMK by specifying the `encryptionConfig` parameter when you create a job.
+ **S3 bucket encryption** – If your S3 bucket uses server-side encryption with a KMS key (SSE-KMS), your identity needs AWS KMS permissions to read input from and write results to that bucket.

You can use the same KMS key for both, or use separate keys.

The required AWS KMS actions depend on how you use AWS KMS:


| Use case | Required actions | 
| --- | --- | 
| Encrypt job output (encryptionConfig) | kms:Encrypt, kms:GenerateDataKey, kms:DescribeKey | 
| Read from SSE-KMS encrypted S3 bucket | kms:Decrypt | 
| Write to SSE-KMS encrypted S3 bucket | kms:GenerateDataKey | 

#### Single KMS key
<a name="advanced-prompt-optimization-prereqs-kms-single"></a>

If you use the same key for both output encryption and S3 bucket encryption:

```
{
    "Effect": "Allow",
    "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey"
    ],
    "Resource": "arn:aws:kms:us-west-2:123456789012:key/your-kms-key-id"
}
```

#### Separate KMS keys for S3 input and job output encryption
<a name="advanced-prompt-optimization-prereqs-kms-separate"></a>

If your S3 input bucket uses one KMS key and you want to encrypt job output with a different KMS key:

```
{
    "Sid": "KMSDecryptS3Input",
    "Effect": "Allow",
    "Action": [
        "kms:Decrypt"
    ],
    "Resource": "arn:aws:kms:us-west-2:123456789012:key/s3-bucket-kms-key-id"
},
{
    "Sid": "KMSEncryptJobOutput",
    "Effect": "Allow",
    "Action": [
        "kms:Encrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey"
    ],
    "Resource": "arn:aws:kms:us-west-2:123456789012:key/output-encryption-kms-key-id"
}
```

### Custom evaluation Lambda permissions (optional)
<a name="advanced-prompt-optimization-prereqs-lambda"></a>

If you use a custom Lambda function to evaluate prompt quality, your calling identity must have permission to invoke it:

```
{
    "Effect": "Allow",
    "Action": ["lambda:InvokeFunction","lambda:GetFunction"],
    "Resource": "arn:aws:lambda:us-west-2:123456789012:function:my-evaluation-metric"
}
```

## Sample IAM policies
<a name="advanced-prompt-optimization-prereqs-policies"></a>

### Identity-based policy: Allow AdvPO job management and model invocation
<a name="advanced-prompt-optimization-prereqs-policy-full"></a>

Attach this policy to the IAM user or role that will create and manage AdvPO jobs.

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "CreateAndManageAdvPOJobs",
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateAdvancedPromptOptimizationJob",
                "bedrock:GetAdvancedPromptOptimizationJob",
                "bedrock:ListAdvancedPromptOptimizationJobs",
                "bedrock:StopAdvancedPromptOptimizationJob",
                "bedrock:BatchDeleteAdvancedPromptOptimization		 	 	 Job"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:advanced-prompt-optimization-job/*"
        },
        {
            "Sid": "InvokeModelsForOptimization",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/*",
                "arn:aws:bedrock:*:123456789012:inference-profile/*"
            ]
        },
        {
            "Sid": "S3AccessForInputAndOutput",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-advpo-bucket/*"
        },
        {
            "Sid": "S3ListBucket",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::my-advpo-bucket"
        }
    ]
}
```

### Identity-based policy: Read-only access to AdvPO jobs
<a name="advanced-prompt-optimization-prereqs-policy-readonly"></a>

Use this policy for users who only need to view job status and results.

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "ViewAdvPOJobs",
            "Effect": "Allow",
            "Action": [
                "bedrock:GetAdvancedPromptOptimizationJob",
                "bedrock:ListAdvancedPromptOptimizationJobs"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:advanced-prompt-optimization-job/*"
        },
        {
            "Sid": "ReadOutputFromS3",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-advpo-bucket/output/*"
        }
    ]
}
```

### Identity-based policy: Restrict to specific models
<a name="advanced-prompt-optimization-prereqs-policy-restrict"></a>

Use this policy to allow AdvPO only with specific models (for example, only Claude Sonnet).

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "AdvPOJobManagement",
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateAdvancedPromptOptimizationJob",
                "bedrock:GetAdvancedPromptOptimizationJob",
                "bedrock:ListAdvancedPromptOptimizationJobs",
                "bedrock:StopAdvancedPromptOptimizationJob"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:advanced-prompt-optimization-job/*"
        },
        {
            "Sid": "InvokeOnlyClaudeSonnet",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-sonnet-*",
                "arn:aws:bedrock:*:123456789012:inference-profile/us.anthropic.claude-sonnet-*"
            ]
        },
        {
            "Sid": "S3Access",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-advpo-bucket/*"
        }
    ]
}
```

### Deny policy: Prevent AdvPO usage (SCP example)
<a name="advanced-prompt-optimization-prereqs-policy-deny"></a>

Use as a Service Control Policy (SCP) to prevent AdvPO usage across an organization.

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "DenyAdvPO",
            "Effect": "Deny",
            "Action": [
                "bedrock:CreateAdvancedPromptOptimizationJob",
                "bedrock:StopAdvancedPromptOptimizationJob",
                "bedrock:BatchDeleteAdvancedPromptOptimization		 	 	 Job"
            ],
            "Resource": "*"
        }
    ]
}
```

## Cross-region inference
<a name="advanced-prompt-optimization-prereqs-cris"></a>

The service may use cross-region inference (CRIS) for evaluation and prompt rewriting. For European regions, the service will use eu CRIS regions. For the following regions, it may use global CRIS: ap-south-1 (Mumbai), sa-east-1 (Sao Paulo), ap-northeast-2 (Seoul), ap-southeast-1 (Singapore).