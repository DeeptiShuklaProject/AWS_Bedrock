

# Code samples for model customization
<a name="model-customization-code-samples"></a>

The following code samples show how to prepare a basic dataset, set up permissions, create a custom model, view the output files, purchase throughput for the model, and run inference on the model. You can modify these code snippets to your specific use-case.

1. Prepare the training dataset.

   1. Create a training dataset file containing the following one line and name it {{train.jsonl}}.

      ```
      {"prompt": "what is AWS", "completion": "it's Amazon Web Services"}
      ```

   1. Create an S3 bucket for your training data and another one for your output data (the names must be unique).

   1. Upload {{train.jsonl}} into the training data bucket.

1. Create a policy to access your training and attach it to an IAM role with an Amazon Bedrock trust relationship. Choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

   1. Create the S3 policy.

      1. Navigate to the IAM console at [https://console.aws.amazon.com/iam](https://console.aws.amazon.com/iam) and choose **Policies** from the left navigation pane.

      1. Select **Create policy** and then choose **JSON** to open the **Policy editor**.

      1. Paste the following policy, replacing {{${training-bucket}}} and {{${output-bucket}}} with your bucket names, and then select **Next**.

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
                         "arn:aws:s3:::{{${training-bucket}}}",
                         "arn:aws:s3:::{{${training-bucket}}}/*"
                     ]
                 },
                 {
                     "Effect": "Allow",
                     "Action": [
                         "s3:GetObject",
                         "s3:PutObject",
                         "s3:ListBucket"
                     ],
                     "Resource": [
                         "arn:aws:s3:::{{${output-bucket}}}",
                         "arn:aws:s3:::{{${output-bucket}}}/*"
                     ]
                 }
             ]
         }
         ```

------

      1. Name the policy {{MyFineTuningDataAccess}} and select **Create policy**.

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

      1. Search for the {{MyFineTuningDataAccess}} policy you created, select the checkbox, and choose **Next**.

      1. Name the role {{MyCustomizationRole}} and select {{Create role}}.

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

   1. Create another file called {{MyFineTuningDataAccess.json}} and paste the following policy into it, replacing {{${training-bucket}}} and {{${output-bucket}}} with your bucket names.

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
                      "arn:aws:s3:::{{${training-bucket}}}",
                      "arn:aws:s3:::{{${training-bucket}}}/*"
                  ]
              },
              {
                  "Effect": "Allow",
                  "Action": [
                      "s3:GetObject",
                      "s3:PutObject",
                      "s3:ListBucket"
                  ],
                  "Resource": [
                      "arn:aws:s3:::{{${output-bucket}}}",
                      "arn:aws:s3:::{{${output-bucket}}}/*"
                  ]
              }
          ]
      }
      ```

------

   1. In a terminal, navigate to the folder containing the policies you created.

   1. Make a [CreateRole](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html) request to create an IAM role called {{MyCustomizationRole}} and attach the {{BedrockTrust.json}} trust policy that you created.

      ```
      aws iam create-role \
          --role-name MyCustomizationRole \
          --assume-role-policy-document file://BedrockTrust.json
      ```

   1. Make a [CreatePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html) request to create the S3 data access policy with the {{MyFineTuningDataAccess.json}} file you created. The response returns an `Arn` for the policy.

      ```
      aws iam create-policy \
          --policy-name MyFineTuningDataAccess \
          --policy-document file://MyFineTuningDataAccess.json
      ```

   1. Make an [AttachRolePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachRolePolicy.html) request to attach the S3 data access policy to your role, replacing the `policy-arn` with the ARN in the response from the previous step:

      ```
      aws iam attach-role-policy \
          --role-name MyCustomizationRole \
          --policy-arn {{${policy-arn}}}
      ```

------
#### [ Python ]

   1. Run the following code to make a [CreateRole](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html) request to create an IAM role called {{MyCustomizationRole}} and to make a [CreatePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html) request to create an S3 data access policy called {{MyFineTuningDataAccess}}. For the S3 data access policy, replace {{${training-bucket}}} and {{${output-bucket}}} with your S3 bucket names.

      ```
      import boto3
      import json
      
      iam = boto3.client("iam")
      
      iam.create_role(
          RoleName="MyCustomizationRole",
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
          PolicyName="MyFineTuningDataAccess",
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
                  },
                  {
                      "Effect": "Allow",
                      "Action": [
                          "s3:GetObject",
                          "s3:PutObject",
                          "s3:ListBucket"
                      ],
                      "Resource": [
                          "arn:aws:s3:::{{${output-bucket}}}",
                          "arn:aws:s3:::{{${output-bucket}}}/*"
                      ]
                  }
              ]
          })
      )
      ```

   1. An `Arn` is returned in the response. Run the following code snippet to make an [AttachRolePolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AttachRolePolicy.html) request, replacing {{${policy-arn}}} with the returned `Arn`.

      ```
      iam.attach_role_policy(
          RoleName="MyCustomizationRole",
          PolicyArn="{{${policy-arn}}}"
      )
      ```

------

1. Select a language to see code samples to call the model customization API operations.

------
#### [ CLI ]

First, create a text file named {{FineTuningData.json}}. Copy the JSON code from below into the text file, replacing {{${training-bucket}}} and {{${output-bucket}}} with your S3 bucket names.

```
{
    "trainingDataConfig": {
        "s3Uri": "s3://{{${training-bucket}}}/train.jsonl"
    },
    "outputDataConfig": {
        "s3Uri": "s3://{{${output-bucket}}}"
    }
}
```

To submit a model customization job, navigate to the folder containing {{FineTuningData.json}} in a terminal and run the following command in the command line, replacing {{${your-customization-role-arn}}} with the model customization role that you set up.

```
aws bedrock create-model-customization-job \
    --customization-type FINE_TUNING \
    --base-model-identifier arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-express-v1 \
    --role-arn {{${your-customization-role-arn}}} \
    --job-name MyFineTuningJob \
    --custom-model-name MyCustomModel \
    --hyper-parameters epochCount=1,batchSize=1,learningRate=.0001,learningRateWarmupSteps=0 \
    --cli-input-json file://FineTuningData.json
```

The response returns a {{jobArn}}. Allow the job some time to complete. You can check its status with the following command.

```
aws bedrock get-model-customization-job \
    --job-identifier "{{jobArn}}"
```

When the `status` is `COMPLETE`, you can see the `trainingMetrics` in the response. You can download the artifacts to the current folder by running the following command, replacing {{aet.et-bucket}} with your output bucket name and {{jobId}} with the ID of the customization job (the sequence following the last slash in the `jobArn`).

```
aws s3 cp s3://{{${output-bucket}}}/model-customization-job-{{jobId}} . --recursive
```

Purchase a no-commitment Provisioned Throughput for your custom model with the following command.

**Note**  
You will be charged hourly for this purchase. Use the console to see price estimates for different options.

```
aws bedrock create-provisioned-model-throughput \
    --model-id MyCustomModel \
    --provisioned-model-name MyProvisionedCustomModel \
    --model-units 1
```

The response returns a `provisionedModelArn`. Allow the Provisioned Throughput some time to be created. To check its status, provide the name or ARN of the provisioned model as the `provisioned-model-id` in the following command.

```
aws bedrock get-provisioned-model-throughput \
    --provisioned-model-id {{${provisioned-model-arn}}}
```

When the `status` is `InService`, you can run inference with your custom model with the following command. You must provide the ARN of the provisioned model as the `model-id`. The output is written to a file named {{output.txt}} in your current folder.

```
aws bedrock-runtime invoke-model \
    --model-id {{${provisioned-model-arn}}} \
    --body '{"inputText": "What is AWS?", "textGenerationConfig": {"temperature": 0.5}}' \
    --cli-binary-format raw-in-base64-out \
    output.txt
```

------
#### [ Python ]

Run the following code snippet to submit a fine-tuning job. Replace {{${your-customization-role-arn}}} with the ARN of the {{MyCustomizationRole}} that you set up and replace {{${training-bucket}}} and {{${output-bucket}}} with your S3 bucket names.

```
import boto3

bedrock = boto3.client(service_name='bedrock')
    
# Set parameters
customizationType = "FINE_TUNING"
baseModelIdentifier = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-express-v1"
roleArn = "{{${your-customization-role-arn}}}"
jobName = "MyFineTuningJob"
customModelName = "MyCustomModel"
hyperParameters = {
        "epochCount": "1",
        "batchSize": "1",
        "learningRate": ".0001",
        "learningRateWarmupSteps": "0"
    }
trainingDataConfig = {"s3Uri": "s3://{{${training-bucket}}}/myInputData/train.jsonl"}
outputDataConfig = {"s3Uri": "s3://{{${output-bucket}}}/myOutputData"}

# Create job
response_ft = bedrock.create_model_customization_job(
    jobName=jobName, 
    customModelName=customModelName,
    roleArn=roleArn,
    baseModelIdentifier=baseModelIdentifier,
    hyperParameters=hyperParameters,
    trainingDataConfig=trainingDataConfig,
    outputDataConfig=outputDataConfig
)

jobArn = response_ft.get('jobArn')
```

The response returns a {{jobArn}}. Allow the job some time to complete. You can check its status with the following command.

```
bedrock.get_model_customization_job(jobIdentifier=jobArn).get('status')
```

When the `status` is `COMPLETE`, you can see the `trainingMetrics` in the [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html) response. You can also follow the steps at [Downloading objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/download-objects.html) to download the metrics.

Purchase a no-commitment Provisioned Throughput for your custom model with the following command.

```
response_pt = bedrock.create_provisioned_model_throughput(
    modelId="MyCustomModel",
    provisionedModelName="MyProvisionedCustomModel",
    modelUnits="1"
)

provisionedModelArn = response_pt.get('provisionedModelArn')
```

The response returns a `provisionedModelArn`. Allow the Provisioned Throughput some time to be created. To check its status, provide the name or ARN of the provisioned model as the `provisionedModelId` in the following command.

```
bedrock.get_provisioned_model_throughput(provisionedModelId=provisionedModelArn)
```

When the `status` is `InService`, you can run inference with your custom model with the following command. You must provide the ARN of the provisioned model as the `modelId`. 

```
import json
import logging
import boto3

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by the model"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using your provisioned custom model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        response (json): The response from the model.
    """

    logger.info(
        "Generating text with your provisioned custom model %s", model_id)

    brt = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = brt.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with provisioned custom model %s", model_id)

    return response_body


def main():
    """
    Entrypoint for example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = provisionedModelArn

        body = json.dumps({
            "inputText": "what is AWS?"
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Token count: {result['tokenCount']}")
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(
            f"Finished generating text with your provisioned custom model {model_id}.")


if __name__ == "__main__":
    main()
```

------