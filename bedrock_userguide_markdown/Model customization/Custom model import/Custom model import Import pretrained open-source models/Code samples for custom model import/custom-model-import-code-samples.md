

# Code samples for custom model import
<a name="custom-model-import-code-samples"></a>

The following code samples show how to set up permissions, create a custom model import job, view the details of your import jobs and imported models, and delete imported model. These code samples apply to Mistral AI, Llama, Qwen, Flan, GPTBigCode, and Mixtral architectures.

## Important: Model Architecture Support
<a name="model-architecture-support"></a>

**GPT-OSS Model Limitations:**
+ **Converse API Not Supported:** GPT-OSS based custom model import models do NOT support the Converse API or ConverseStream API.
+ **Use InvokeModel API Instead:** Customers must use the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) API when working with GPT-OSS based custom models.
+ **API Schema Requirement:** GPT-OSS models require OpenAI-compatible API schemas:
  + Completion format for completion requests
  + ChatCompletion format for chat requests
  + Response format follows OpenAI API specifications
+ **Supported Models for Converse API:** The Converse API is supported for Mistral AI, Llama, Qwen, Flan, GPTBigCode, and Mixtral architectures only.

For GPT-OSS model usage examples with [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) API, refer to the OpenAI API documentation for request/response schemas.

1. Prepare model files for import

   1. If you are importing from an Amazon S3 bucket, you need to supply the model files in the Hugging Face weights format. For more information, see [Import a model source from Amazon S3](model-customization-import-model.md#model-customization-import-model-source). 

   1. Create an Amazon S3 bucket for your model files (the names must be unique).

   1. Upload the model files into the bucket.

1. Create a policy to access your model files and attach it to an IAM role with an Amazon Bedrock trust relationship. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

   1. Create Amazon S3 policy to access the Amazon S3 bucket that contains your model files

      1. Navigate to the IAM console at [https://console.aws.amazon.com/iam](https://console.aws.amazon.com/iam) and choose **Policies** from the left navigation pane.

      1. Select **Create policy** and then choose **JSON** to open the **Policy editor**.

      1. Paste the following policy, replacing {{${model-file-bucket}}} with your bucket name, and then select **Next**.

------
#### [ JSON ]

****  

         ```
         {
             "Version":"2012-10-17",		 	 	 
             "Statement": [
                 {
                     "Effect": "Allow",
                     "Action": [
                         "s3:GetObject",
                         "s3:ListBucket"
                     ],
                     "Resource": [
                         "arn:aws:s3:::{{${model-file-bucket}}}",
                         "arn:aws:s3:::{{${model-file-bucket}}}/*"
                     ]
                   }
                 ]
               }
         ```

------

      1. Name the policy {{S3BucketPolicy}} and select **Create policy**.

   1. Create an IAM role and attach the policy.

      1. From the left navigation pane, choose **Roles** and then select **Create role**.

      1. Select **Custom trust policy**, paste the following policy, and select **Next**.

------
#### [ JSON ]

****  

         ```
         {
             "Version":"2012-10-17",		 	 	 
             "Statement": [
                 {
                     "Effect": "Allow",
                     "Principal": {
                         "Service": "bedrock.amazonaws.com"
                     },
                     "Action": "sts:AssumeRole"
                 }
             ] 
         }
         ```

------

      1. Search for the {{S3BucketPolicy}} policy you created, select the checkbox, and choose **Next**.

      1. Name the role {{MyImportModelRole}} and select {{Create role}}.

------
#### [ CLI ]

   1. Create a file called {{BedrockTrust.json}} and paste the following policy into it.

------
#### [ JSON ]

****  

      ```
      {
          "Version":"2012-10-17",		 	 	 
          "Statement": [
              {
                  "Effect": "Allow",
                  "Principal": {
                      "Service": "bedrock.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
              }
          ] 
      }
      ```

------

   1. Create another file called {{S3BucketPolicy.json}} and paste the following policy into it, replacing {{${model-file-bucket}}} with your bucket names.

------
#### [ JSON ]

****  

      ```
      {
          "Version":"2012-10-17",		 	 	 
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": [
                      "s3:GetObject",
                      "s3:ListBucket"
                  ],
                  "Resource": [
                      "arn:aws:s3:::{{${model-file-bucket}}}",
                      "arn:aws:s3:::{{${model-file-bucket}}}/*"
                  ]
              }
           ]
      }
      ```

------

   1. In a terminal, navigate to the folder containing the policies you created.

   1. Make a [CreateRole](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html) request to create an IAM role called {{MyImportModelRole}} and attach the {{BedrockTrust.json}} trust policy that you created.

      ```
      aws iam create-role \
          --role-name MyImportModelRole \
          --assume-role-policy-document file://BedrockTrust.json
      ```

   1. Make a [CreatePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html) request to create the S3 data access policy with the {{S3BucketPolicy.json}} file you created. The response returns an `Arn` for the policy.

      ```
      aws iam create-policy \
          --policy-name S3BucketPolicy \
          --policy-document file://S3BucketPolicy.json
      ```

   1. Make an [AttachRolePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachRolePolicy.html) request to attach the S3 data access policy to your role, replacing the `policy-arn` with the ARN in the response from the previous step:

      ```
      aws iam attach-role-policy \
          --role-name MyImportModelRole \
          --policy-arn {{${policy-arn}}}
      ```

------
#### [ Python ]

   1. Run the following code to make a [CreateRole](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html) request to create an IAM role called {{MyImportModel}} and to make a [CreatePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html) request to create an S3 data access policy called {{S3BucketPolicy}}. For the S3 data access policy, replace {{${model-file-bucket}}} with your S3 bucket names.

      ```
      import boto3
      import json
      
      iam = boto3.client("iam")
      
      iam.create_role(
          RoleName="MyImportModelRole",
          AssumeRolePolicyDocument=json.dumps({
              "Version": "2012-10-17",		 	 	 
              "Statement": [
                  {
                      "Effect": "Allow",
                      "Principal": {
                          "Service": "bedrock.amazonaws.com"
                      },
                      "Action": "sts:AssumeRole"
                  }
              ] 
          })
      )
      
      iam.create_policy(
          PolicyName="S3BucketPolicy",
          PolicyDocument=json.dumps({
              "Version": "2012-10-17",		 	 	 
              "Statement": [
                  {
                      "Effect": "Allow",
                      "Action": [
                          "s3:GetObject",
                          "s3:ListBucket"
                      ],
                      "Resource": [
                          "arn:aws:s3:::{{${training-bucket}}}",
                          "arn:aws:s3:::{{${training-bucket}}}/*"
                      ]
                  }
                ]
             })
           )
      ```

   1. An `Arn` is returned in the response. Run the following code snippet to make an [AttachRolePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachRolePolicy.html) request, replacing {{${policy-arn}}} with the returned `Arn`.

      ```
      iam.attach_role_policy(
          RoleName="MyImportModelRole",
          PolicyArn="{{${policy-arn}}}"
      )
      ```

------

1. Select a language to see code samples to call the custom model import API operations.

------
#### [ CLI ]

To submit a custom model import job, in a terminal run the following command in the command line, replacing {{${my-import-model-role-arn}}} with the model role that you set up and the {{s3-bucket-path}} with the S3 bucket path of your model files.

```
aws bedrock create-model-import-job 
    --job-name {{MyImportedModelJobName}}
    --imported-model-name {{MyImportedModelName}}
    --role-arn {{${my-import-model-role-arn}}}  
    --model-data-source '{"s3DataSource": {"s3Uri": {{s3-bucket-path}} }}
```

The response returns a {{jobArn}}. The custom import job will take some time to complete. You can use the `jobArn` with the following command to check the status of the import job.

The following fields are optional:
+ To add a VPC configuration, add the following argument to the preceding command to specify the security group and subnets:

  ```
     -\\-vpc-config '{securityGroupIds": ["sg-xx"], "subnetIds": ["subnet-yy", "subnet-zz"]}'
  ```
+ To encrypt your model with a KMS key, add the following argument to the preceding command, replacing the values to specify the key with which you want to encrypt your model.

  ```
     -\\-customModelKmsKeyId 'arn:aws:kms:{{region}}:{{account-id}}:key/{{key-id}}'
  ```
+ To add tags, add the following argument to the preceding command, replacing the keys and values with the tags you want to attach to the job and/or output model and making sure to separate key/value pairs with a space:

  ```
     -\\-tags key={{key1}},value={{value1}} key={{key2}},value={{value2}}
  ```

The response returns a {{jobArn}}. The custom import job will take some time to complete. You can use the `jobArn` with the following command to check the status of the import job.

```
aws bedrock get-model-import-job \
    --job-identifier "{{jobArn}}"
```

The response looks similar to this:

```
{
    "jobArn": {{${job-arn}}} ,
    "jobName": {{MyImportedModelJobName}},
    "importedModelName": {{MyImportedModelName}},
    "roleArn": {{${my-role-arn}}},
    "modelDataSource": {
        "s3DataSource": {
            "s3Uri": "${S3Uri}"
        }
    },
    "status": "Complete",
    "creationTime": "2024-08-13T23:38:42.457Z",
    "lastModifiedTime": "2024-08-13T23:39:25.158Z"
```

When the `status` is `Complete`. the import job is complete.

To run inference on your newly imported model, you must provide the ARN of the imported model as the `model-id`. Get ARN of the imported model.

```
aws bedrock list-imported-models              
```

The response contains the model name and the model ARN. Use the model ARN to invoke the imported model. For more information, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md).

```
{
    "modelSummaries": [
        {
            "modelArn": {{model-arn}},
            "modelName": "MyImportedModelName",
            "modelArchitecture":{{model-architecture}},
            "instructSupported":{{Y}},
            "creationTime": "2024-08-13T19:20:14.058Z"
            
        }
    ]
}
```

To delete your imported model, in a terminal run the following command in the command line, using the model name or the model ARN of the imported model you want to delete.

```
aws bedrock delete-imported-model 
                --model-identifier {{MyImportedModelName}}
```

------
#### [ Python ]

Run the following code snippet to submit an custom model import job. Replace {{my-region}} with the Region where you imported the model, {{${my-import-model-role-arn}}} with the ARN of the {{MyImportModelRole}} that you set up and replace {{${model-file-bucket}}} with your S3 bucket name.

```
import boto3
import json

REGION_NAME = {{my-region}}
bedrock = boto3.client(service_name='bedrock',
                       region_name=REGION_NAME)

JOB_NAME = {{MyImportedModelJobName}} 
ROLE_ARN = {{${my-import-model-role-arn}}}
IMPORTED_MODEL_NAME = {{ImportedModelName}}
S3_URI = {{${S3Uri}}}

# createModelImportJob API
create_job_response = bedrock.create_model_import_job(
    jobName=JOB_NAME,
    importedModelName=IMPORTED_MODEL_NAME,
    roleArn=ROLE_ARN,
    modelDataSource={
        "s3DataSource": {
            "s3Uri": S3_URI
        }
    },
)
job_arn = create_job_response.get("jobArn")
```

The following fields are optional.
+ To add a VPC configuration, add the following argument to the preceding command to specify the security group and subnets:

  ```
     vpc-config = {'securityGroupIds: ["sg-xx".], 'subnetIds': [subnet-yy, 'subnet-zz']}'
  ```
+ To encrypt your model with a KMS key, add the following argument to the preceding command, replacing the values to specify the key with which you want to encrypt your model.

  ```
     importedModelKmsKeyId = 'arn:aws:kms:{{region}}:{{account-id}}:key/{{key-id}}'
  ```
+ To add tags, add the following argument to the preceding command, replacing the keys and values with the tags you want to attach to the job and/or output model and making sure to separate key/value pairs with a space:

  ```
     jobTags key={{key1}},value={{value1}} key={{key2}},value={{value2}}
  ```

The response returns a jobArn

```
               job_arn = create_job_response.get("{{jobArn}}")
```

The custom import job will take some time to complete. You can use the `jobArn` with the following command to check the status of the import job.

```
bedrock.get_model_import_job(jobIdentifier={{jobArn}})
```

When the `status` is `Completed`, the import job is complete.

To run inference on your newly imported model, you must provide the ARN of the imported model as the `model-id`. Get ARN of the imported model.

```
response_pt = bedrock.list_imported_models(
    creationTimeBefore=datetime ({{2015,1,1}},
    creationTimeAfter= datetime ({{2015,1,1}},
    nameContains = '{{MyImportedModelName}},
    maxresults = {{123}}
    nextToken = '{{none}}',
    sortBy = '{{creationTime}}',
    sortOrder = '{{Ascending}}'
```

The response returns the `modelArn` along with other details of the imported model. 

```
{
    'nextToken': '',
    'modelSummaries': [
        {
            'modelArn': '{{your-model-arn}}',
            'modelName': '{{MyImportedModelName}}',
            'modelArchitecture':{{model-architecture}},
            'instructSupported':{{Y}},
            'creationTime': datetime(2015, 1, 1)
        },
    ]
```

Use the model ARN to invoke the imported model. For more information, see [Submit a single prompt with InvokeModelSubmit a single prompt with InvokeModel (moved)](inference-invoke.md).

To delete your imported model, use the following command using the model name or the model ARN of the imported model you want to delete.

```
response = client.delete_imported_model(
    modelIdentifier='{{MyImportedModelName}}'
            )
```

------