

# Process multiple prompts with batch inference
<a name="batch-inference"></a>

With batch inference, you can submit multiple prompts and generate responses asynchronously. You can format your input data by using either the `InvokeModel` or `Converse` API format. Batch inference helps you process a large number of requests efficiently by sending a single request and generating the responses in an Amazon S3 bucket. After defining model inputs in files you create, you upload the files to an S3 bucket. You then submit a batch inference request and specify the S3 bucket. After the job is complete, you can retrieve the output files from S3. You can use batch inference to improve the performance of model inference on large datasets.

**Note**  
Batch inference isn't supported for provisioned models.

**Note**  
Batch inference does not support tool calling (function calling) or structured output (`response_format`). Each record in the input JSONL file is processed independently without multi-turn interaction, so features that require back-and-forth exchanges between the model and client are not available.

See the following resources for general information about batch inference:
+ To see pricing for batch inference, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).
+ To see quotas for batch inference, see [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) in the AWS General Reference.
+ To receive notifications when batch inference jobs complete or change state instead of polling, see [Monitor Amazon Bedrock job state changes using Amazon EventBridgeMonitor event changes](monitoring-eventbridge.md).

**Topics**
+ [Supported Regions and models for batch inference](batch-inference-supported.md)
+ [Prerequisites for batch inference](batch-inference-prereq.md)
+ [Create a batch inference job](batch-inference-create.md)
+ [Monitor batch inference jobs](batch-inference-monitor.md)
+ [Stop a batch inference job](batch-inference-stop.md)
+ [View the results of a batch inference job](batch-inference-results.md)
+ [Code example for batch inference](batch-inference-example.md)
+ [Submit a batch of prompts with the OpenAI Batch API](inference-openai-batch.md)