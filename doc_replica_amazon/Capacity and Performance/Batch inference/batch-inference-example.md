

# Code example for batch inference
<a name="batch-inference-example"></a>

The code example in this chapter shows how to create a batch inference job, view information about it, and stop it. This example uses the `InvokeModel` API format. For information about using the `Converse` API format, see [Format and upload your batch inference data](batch-inference-data.md).

Select a language to see a code example for it:

------
#### [ Python ]

Create a JSONL file named {{abc.jsonl}} and include a JSON object for each record that contains at least the minimum number of records (see the **Minimum number of records per batch inference job for {{{Model}}}** [Quotas for Amazon Bedrock](quotas.md)). In this example, you'll use the Anthropic Claude 3 Haiku model. The following example shows the first input JSON in the file:

```
{
    "recordId": "CALL0000001", 
    "modelInput": {
        "anthropic_version": "bedrock-2023-05-31", 
        "max_tokens": 1024,
        "messages": [ 
            { 
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": "Summarize the following call transcript: ..." 
                    } 
                ]
            }
        ]
    }
}
... 
# Add records until you hit the minimum
```

Create an S3 bucket called {{amzn-s3-demo-bucket-input}} and upload the file to it. Then create an S3 bucket called {{amzn-s3-demo-bucket-output}} to write your output files to. Run the following code snippet to submit a job and get the {{jobArn}} from the response:

```
import boto3

bedrock = boto3.client(service_name="bedrock")

inputDataConfig=({
    "s3InputDataConfig": {
        "s3Uri": "s3://amzn-s3-demo-bucket-input/abc.jsonl"
    }
})

outputDataConfig=({
    "s3OutputDataConfig": {
        "s3Uri": "s3://amzn-s3-demo-bucket-output/"
    }
})

response=bedrock.create_model_invocation_job(
    roleArn="arn:aws:iam::123456789012:role/MyBatchInferenceRole",
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    jobName="my-batch-job",
    inputDataConfig=inputDataConfig,
    outputDataConfig=outputDataConfig
)

jobArn = response.get('jobArn')
```

Return the `status` of the job.

```
bedrock.get_model_invocation_job(jobIdentifier=jobArn)['status']
```

List batch inference jobs that {{Failed}}.

```
bedrock.list_model_invocation_jobs(
    maxResults=10,
    statusEquals="Failed",
    sortOrder="Descending"
)
```

Stop the job that you started.

```
bedrock.stop_model_invocation_job(jobIdentifier=jobArn)
```

------
#### [ Java ]

```
package com.amazon.aws.sample.bedrock.inference;

import software.amazon.awssdk.services.bedrock.BedrockClient;
import software.amazon.awssdk.services.bedrock.model.*;

public class BedrockBatchInference {
    private final BedrockClient bedrockClient = BedrockClient.create();

    public void createModelInvokeJobSampleCode() {

        CreateModelInvocationJobResponse response = bedrockClient.createModelInvocationJob(request -> request
                .modelId("anthropic.claude-haiku-4-5-20251001-v1:0")
                .jobName("unique-job-name")
                .roleArn("arn:aws:iam::123456789:role/bedrock-role")
                .clientRequestToken("client-token")
                .inputDataConfig(input -> input
                        .s3InputDataConfig(s3 -> s3
                                .s3Uri("s3://batch-input/abc.jsonl")
                                .s3InputFormat(S3InputFormat.JSONL)))
                .outputDataConfig(output -> output
                        .s3OutputDataConfig(s3 -> s3
                                .s3Uri("s3://batch-output/"))));

        System.out.println(response.jobArn());
    }

    public void getModelInvokeJobSampleCode() {
        GetModelInvocationJobResponse response = bedrockClient.getModelInvocationJob(request -> request
                .jobIdentifier("jobArn"));

        System.out.println(response.status());
    }

    public void listModelInvokeJobSampleCode() {
        ListModelInvocationJobsResponse response = bedrockClient.listModelInvocationJobs(request -> request
                .maxResults(10)
                .nameContains("matching-string"));

        response.invocationJobSummaries().forEach(job ->
                System.out.println(job.jobName() + ": " + job.status()));
    }

    public void stopModelInvokeJobSampleCode() {
        bedrockClient.stopModelInvocationJob(request -> request
                .jobIdentifier("jobArn"));
    }
}
```

------