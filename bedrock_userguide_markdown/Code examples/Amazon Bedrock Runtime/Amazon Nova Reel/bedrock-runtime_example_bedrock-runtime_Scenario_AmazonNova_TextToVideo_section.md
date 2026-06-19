

# Use Amazon Nova Reel to generate a video from a text prompt
<a name="bedrock-runtime_example_bedrock-runtime_Scenario_AmazonNova_TextToVideo_section"></a>

The following code examples show how to use Amazon Nova Reel to generate a video from a text prompt.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples). 
Use Amazon Nova Reel to generate a video from a text prompt.  

```
"""
This example demonstrates how to use Amazon Nova Reel to generate a video from a text prompt.

It shows how to:
- Set up the Amazon Bedrock runtime client
- Configure a text-to-video request
- Submit an asynchronous job for video generation
- Poll for job completion status
- Access the generated video from S3
"""

import random
import time

import boto3

# Replace with your own S3 bucket to store the generated video
# Format: s3://your-bucket-name
OUTPUT_S3_URI = "s3://REPLACE-WITH-YOUR-S3-BUCKET-NAME"


def start_text_to_video_generation_job(bedrock_runtime, prompt, output_s3_uri):
    """
    Starts an asynchronous text-to-video generation job using Amazon Nova Reel.

    :param bedrock_runtime: The Bedrock runtime client
    :param prompt: The text description of the video to generate
    :param output_s3_uri: S3 URI where the generated video will be stored

    :return: The invocation ARN of the async job
    """
    # Specify the model ID for text-to-video generation
    model_id = "amazon.nova-reel-v1:0"

    # Generate a random seed between 0 and 2,147,483,646
    # This helps ensure unique video generation results
    seed = random.randint(0, 2147483646)

    # Configure the video generation request with additional parameters
    model_input = {
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": {"text": prompt},
        "videoGenerationConfig": {
            "fps": 24,
            "durationSeconds": 6,
            "dimension": "1280x720",
            "seed": seed,
        },
    }

    # Specify the S3 location for the output video
    output_config = {"s3OutputDataConfig": {"s3Uri": output_s3_uri}}

    # Invoke the model asynchronously
    response = bedrock_runtime.start_async_invoke(
        modelId=model_id, modelInput=model_input, outputDataConfig=output_config
    )

    invocation_arn = response["invocationArn"]

    return invocation_arn


def query_job_status(bedrock_runtime, invocation_arn):
    """
    Queries the status of an asynchronous video generation job.

    :param bedrock_runtime: The Bedrock runtime client
    :param invocation_arn: The ARN of the async invocation to check

    :return: The runtime response containing the job status and details
    """
    return bedrock_runtime.get_async_invoke(invocationArn=invocation_arn)


def main():
    """
    Main function that demonstrates the complete workflow for generating
    a video from a text prompt using Amazon Nova Reel.
    """
    # Create a Bedrock Runtime client
    # Note: Credentials will be loaded from the environment or AWS CLI config
    bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Configure the text prompt and output location
    prompt = "Closeup of a cute old steampunk robot. Camera zoom in."

    # Verify the S3 URI has been set to a valid bucket
    if "REPLACE-WITH-YOUR-S3-BUCKET-NAME" in OUTPUT_S3_URI:
        print("ERROR: You must replace the OUTPUT_S3_URI with your own S3 bucket URI")
        return

    print("Submitting video generation job...")
    invocation_arn = start_text_to_video_generation_job(
        bedrock_runtime, prompt, OUTPUT_S3_URI
    )
    print(f"Job started with invocation ARN: {invocation_arn}")

    # Poll for job completion
    while True:
        print("\nPolling job status...")
        job = query_job_status(bedrock_runtime, invocation_arn)
        status = job["status"]

        if status == "Completed":
            bucket_uri = job["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
            print(f"\nSuccess! The video is available at: {bucket_uri}/output.mp4")
            break
        elif status == "Failed":
            print(
                f"\nVideo generation failed: {job.get('failureMessage', 'Unknown error')}"
            )
            break
        else:
            print("In progress. Waiting 15 seconds...")
            time.sleep(15)


if __name__ == "__main__":
    main()
```
+ For API details, see the following topics in *AWS SDK for Python (Boto3) API Reference*.
  + [GetAsyncInvoke](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/GetAsyncInvoke)
  + [StartAsyncInvoke](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/StartAsyncInvoke)

------
#### [ Swift ]

**SDK for Swift**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/swift/example_code/bedrock-runtime#code-examples). 
Use Amazon Nova Reel to generate a video from a text prompt.  

```
// This example demonstrates how to use Amazon Nova Reel to generate a video from a text prompt.
// It shows how to:
// - Set up the Amazon Bedrock runtime client
// - Configure a text-to-video request
// - Submit an asynchronous job for video generation
// - Poll for job completion status
// - Access the generated video from S3

import AWSBedrockRuntime
import Foundation
import Smithy

func startTextToVideoGenerationJob(
    bedrockRuntimeClient: BedrockRuntimeClient, prompt: String, outputS3Uri: String
) async throws -> String? {
    // Specify the model ID for text-to-video generation
    let modelId = "amazon.nova-reel-v1:0"

    // Configure the video generation request with additional parameters
    let modelInputSource: [String: Any] = [
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": [
            "text": "\(prompt)"
        ],
        "videoGenerationConfig": [
            "durationSeconds": 6,
            "fps": 24,
            "dimension": "1280x720",
        ],
    ]

    let modelInput = try Document.make(from: modelInputSource)

    let input = StartAsyncInvokeInput(
        modelId: modelId,
        modelInput: modelInput,
        outputDataConfig: .s3outputdataconfig(
            BedrockRuntimeClientTypes.AsyncInvokeS3OutputDataConfig(
                s3Uri: outputS3Uri
            )
        )
    )

    // Invoke the model asynchronously
    let output = try await bedrockRuntimeClient.startAsyncInvoke(input: input)
    return output.invocationArn
}

func queryJobStatus(
    bedrockRuntimeClient: BedrockRuntimeClient, 
    invocationArn: String?
) async throws -> GetAsyncInvokeOutput {
    try await bedrockRuntimeClient.getAsyncInvoke(
        input: GetAsyncInvokeInput(invocationArn: invocationArn))
}

func main() async throws {
    // Create a Bedrock Runtime client
    let config =
        try await BedrockRuntimeClient.BedrockRuntimeClientConfiguration(
            region: "us-east-1"
        )
    let client = BedrockRuntimeClient(config: config)

    // Specify the S3 location for the output video
    let bucket = "s3://REPLACE-WITH-YOUR-S3-BUCKET-NAM"

    print("Submitting video generation job...")
    let invocationArn = try await startTextToVideoGenerationJob(
        bedrockRuntimeClient: client,
        prompt: "A pomegranate juice in a railway station",
        outputS3Uri: bucket
    )
    print("Job started with invocation ARN: \(String(describing:invocationArn))")

    // Poll for job completion
    var status: BedrockRuntimeClientTypes.AsyncInvokeStatus?
    var isReady = false
    var hasFailed = false

    while !isReady && !hasFailed {
        print("\nPolling job status...")
        status = try await queryJobStatus(
            bedrockRuntimeClient: client, invocationArn: invocationArn
        ).status
        switch status {
        case .completed:
            isReady = true
            print("Video is ready\nCheck S3 bucket: \(bucket)")
        case .failed:
            hasFailed = true
            print("Something went wrong")
        case .inProgress:
            print("Job is in progress...")
            try await Task.sleep(nanoseconds: 15 * 1_000_000_000)  // 15 seconds
        default:
            isReady = true
        }
    }
}

do {
    try await main()
} catch {
    print("An error occurred: \(error)")
}
```
+ For API details, see the following topics in *AWS SDK for Swift API reference*.
  + [GetAsyncInvoke](https://sdk.amazonaws.com/swift/api/awsbedrockruntime/latest/documentation/awsbedrockruntime/bedrockruntimeclient/getasyncinvoke(input:))
  + [StartAsyncInvoke](https://sdk.amazonaws.com/swift/api/awsbedrockruntime/latest/documentation/awsbedrockruntime/bedrockruntimeclient/startasyncinvoke(input:))

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.