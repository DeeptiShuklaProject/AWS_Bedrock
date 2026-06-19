

# Create a batch inference job
<a name="batch-inference-create"></a>

After you've set up an Amazon S3 bucket with files for running model inference, you can create a batch inference job. Before you begin, check that you set up the files in accordance with the instructions described in [Format and upload your batch inference data](batch-inference-data.md).

**Note**  
To submit a batch inference job using a VPC, you must use the API. Select the API tab to learn how to include the VPC configuration.

To learn how to create a batch inference job, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To create a batch inference job**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, select **Batch inference**.

1. In the **Batch inference jobs** section, choose **Create job**.

1. In the **Job details** section, give the batch inference job a **Job name** and select a model to use for the batch inference job by choosing **Select model**.

1. In the **Model invocation type** section, choose the API format for your input data. Choose **InvokeModel** if your input data uses model-specific request formats, or choose **Converse** if your input data uses the Converse API format. The default is **InvokeModel**.

1. In the **Input data** section, choose **Browse S3** and select an S3 location for your batch inference job. Batch inference processes all JSONL and accompanying content files at that S3 location, whether the location is an S3 folder or a single JSONL file.
**Note**  
If the input data is in an S3 bucket that belongs to a different account from the one from which you're submitting the job, you must use the API to submit the batch inference job. To learn how to do this, select the API tab above.

1. In the **Output data** section, choose **Browse S3** and select an S3 location to store the output files from your batch inference job. By default, the output data will be encrypted by an AWS managed key. To choose a custom KMS key, select **Customize encryption settings (advanced)** and choose a key. For more information about encryption of Amazon Bedrock resources and setting up a custom KMS key see [Data encryption](data-encryption.md).
**Note**  
If you plan to write the output data to an S3 bucket that belongs to a different account from the one from which you're submitting the job, you must use the API to submit the batch inference job. To learn how to do this, select the API tab above.

1. In the **Service access** section, select one of the following options:
   + **Use an existing service role** – Select a service role from the drop-down list. For more information on setting up a custom role with the appropriate permissions, see [Required permissions for batch inference](batch-inference-permissions.md).
   + **Create and use a new service role** – Enter a name for the service role.

1. (Optional) To associate tags with the batch inference job, expand the **Tags** section and add a key and optional value for each tag. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

1. Choose **Create batch inference job**.

------
#### [ API ]

To create a batch inference job, send a [CreateModelInvocationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelInvocationJob.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp).

The following fields are required:


****  

| Field | Use case | 
| --- | --- | 
| jobName | To specify a name for the job. | 
| roleArn | To specify the Amazon Resource Name (ARN) of the service role with permissions to create and manage the job. For more information, see [Create a custom service role for batch inference](batch-iam-sr.md). | 
| modelId | To specify the ID or ARN of the model to use in inference. | 
| inputDataConfig | To specify the S3 location containing the input data. Batch inference processes all JSONL and accompanying content files at that S3 location, whether the location is an S3 folder or a single JSONL file. For more information, see [Format and upload your batch inference data](batch-inference-data.md). | 
| outputDataConfig | To specify the S3 location to write the model responses to. | 

The following fields are optional:


****  

| Field | Use case | 
| --- | --- | 
| modelInvocationType | To specify the API format of the input data. Set to Converse to use the Converse API format, or InvokeModel (default) to use model-specific request formats. For more information about the Converse request format, see [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html). | 
| timeoutDurationInHours | To specify the duration in hours after which the job will time out. | 
| tags | To specify any tags to associate with the job. For more information, see [Tagging Amazon Bedrock resources](tagging.md). | 
| vpcConfig | To specify the VPC configuration to use to protect your data during the job. For more information, see [Protect batch inference jobs using a VPC](batch-vpc.md). | 
| clientRequestToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). | 

The response returns a `jobArn` that you can use to refer to the job when carrying out other batch inference-related API calls.

------