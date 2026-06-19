

# How EventBridge for Amazon Bedrock works
<a name="monitoring-eventbridge-how-it-works"></a>

Amazon EventBridge is a serverless event bus that ingests state change events from AWS services, SaaS partners, and customer applications. It processes events based on rules or patterns that you create, and routes these events to one or more *targets* that you choose, such as AWS Lambda, Amazon Simple Queue Service, and Amazon Simple Notification Service. You can configure downstream workflows based on the contents of the event.

Before learning how to use Amazon EventBridge for Amazon Bedrock, review the following pages in the Amazon EventBridge User Guide.
+ [Event bus concepts in Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is-how-it-works-concepts.html) – Review the concepts of *events*, *rules*, and *targets*.
+ [Creating rules that react to events in Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule.html) – Learn how to create rules.
+ [Amazon EventBridge event patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html) – Learn how to define event patterns.
+ [Amazon EventBridge targets](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html) – Learn about the targets you can send events to.

Amazon Bedrock publishes your events via Amazon EventBridge whenever there is a change in the state of a job that you submit. In each case, a new event is created and sent to Amazon EventBridge, which then sends the event to your default event bus. The event shows which job’s state has changed and the current state of the job.

Amazon Bedrock events are identified in an event by the value of the `source` being `aws.bedrock`. The `detail-type` for events in Amazon Bedrock include the following:
+ `Model Customization Job State Change`
+ `Batch Inference Job State Change`

Select a tab to see a sample event for a job submitted in Amazon Bedrock.

------
#### [ Model Customization Job State Change ]

The following JSON object shows a sample event for when the status of a model customization job has changed:

```
{
  "version": "0",
  "id": "UUID",
  "detail-type": "Model Customization Job State Change",
  "source": "aws.bedrock",
  "account": "123456789012",
  "time": "2023-08-11T12:34:56Z",
  "region": "us-east-1",
  "resources": ["arn:aws:bedrock:us-east-1:123456789012:model-customization-job/abcdefghwxyz"],
  "detail": {
    "version": "0.0",
    "jobName": "abcd-wxyz",
    "jobArn": "arn:aws:bedrock:us-east-1:123456789012:model-customization-job/abcdefghwxyz",
    "outputModelName": "dummy-output-model-name",
    "outputModelArn": "arn:aws:bedrock:us-east-1:123456789012:dummy-output-model-name",
    "roleArn": "arn:aws:iam::123456789012:role/JobExecutionRole",
    "jobStatus": "Failed",
    "failureMessage": "Failure Message here.",
    "creationTime": "2023-08-11T10:11:12Z",
    "lastModifiedTime": "2023-08-11T12:34:56Z",
    "endTime": "2023-08-11T12:34:56Z",
    "baseModelArn": "arn:aws:bedrock:us-east-1:123456789012:base-model-name",
    "hyperParameters": {
      "batchSize": "1",
      "epochCount": "5",
      "learningRate": "0.05",
      "learningRateWarmupSteps": "10"
    },
    "trainingDataConfig": {
      "s3Uri": "s3://bucket/key"
    },
    "validationDataConfig": {
      "s3Uri": "s3://bucket/key"
    },
    "outputDataConfig": {
      "s3Uri": "s3://bucket/key"
    }
  }
}
```

To learn about the fields in the **detail** object that are specific to model customization, see [GetModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelCustomizationJob.html).

------
#### [ Batch Inference Job State Change ]

The following JSON object shows a sample event for when the status of a model customization job has changed:

```
{
  "version": "0",
  "id": "a1b2c3d4",
  "detail-type": "Batch Inference Job State Change",
  "source": "aws.bedrock",
  "account": "123456789012",
  "time": "Wed Aug 28 22:58:30 UTC 2024",
  "region": "us-east-1",
  "resources": ["arn:aws:bedrock:us-east-1:123456789012:model-invocation-job/abcdefghwxyz"],
  "detail": {
    "version": "0.0",
    "accountId": "123456789012",
    "batchJobName": "dummy-batch-job-name",
    "batchJobArn": "arn:aws:bedrock:us-east-1:123456789012:model-invocation-job/abcdefghwxyz",
    "batchModelId": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
    "status": "Completed",
    "failureMessage": "",
    "creationTime": "Aug 28, 2024, 10:47:53 PM"
  }
}
```

To learn about the fields in the **detail** object that are specific to batch inference, see [GetModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetModelInvocationJob.html).

------
#### [ Bedrock Data Automation sample event ]

The following JSON object shows a sample event for when the status of a BDA processing job has changed.

```
{
    "version": "0",
    "id": "0cc3eaf7-dff6-6f67-0ee0-ae572fccfe84",
    "detail-type": "Bedrock Data Automation Job Succeeded",
    "source": "aws.bedrock",
    "account": "123456789012",
    "time": "2025-05-27T22:48:36Z",
    "region": "us-west-2",
    "resources": [],
    "detail": {
        "job_id": "25010344-03f7-4167-803a-837afdc7ce98",
        "job_status": "SUCCESS",
        "semantic_modality": "Document",
        "input_s3_object": {
            "s3_bucket": "input-s3-bucket-name",
            "name": "key/name"
        },
        "output_s3_location": {
            "s3_bucket": "output-s3-bucket-name",
            "name": "key"
        },
        "error_message": ""
    }
}
```

------