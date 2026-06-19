

# Submit a batch of prompts with the OpenAI Batch API
<a name="inference-openai-batch"></a>

You can run a batch inference job using the [OpenAI Create batch API](https://platform.openai.com/docs/api-reference/batch) with Amazon Bedrock OpenAI models.

You can call the OpenAI Create batch API in the following ways:
+ Make an HTTP request with an Amazon Bedrock Runtime endpoint.
+ Use an OpenAI SDK request with an Amazon Bedrock Runtime endpoint.

Select a topic to learn more:

**Topics**
+ [Supported models and Regions for the OpenAI batch API](#inference-openai-batch-supported)
+ [Prerequisites to use the OpenAI batch API](#inference-openai-batch-prereq)
+ [Create an OpenAI batch job](#inference-openai-batch-create)
+ [Retrieve an OpenAI batch job](#inference-openai-batch-retrieve)
+ [List OpenAI batch jobs](#inference-openai-batch-list)
+ [Cancel an OpenAI batch job](#inference-openai-batch-cancel)

## Supported models and Regions for the OpenAI batch API
<a name="inference-openai-batch-supported"></a>

You can use the OpenAI Create batch API with all OpenAI models supported in Amazon Bedrock and in the AWS Regions that support these models. For more information about supported models and regions, see [Supported foundation models in Amazon Bedrock](models-supported.md).

## Prerequisites to use the OpenAI batch API
<a name="inference-openai-batch-prereq"></a>

To see prerequisites for using the OpenAI batch API operations, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK ]
+ **Authentication** – The OpenAI SDK only supports authentication with an Amazon Bedrock API key. Generate an Amazon Bedrock API key to authenticate your request. To learn about Amazon Bedrock API keys and how to generate them, see the API keys section in the Build chapter.
+ **Endpoint** – Find the endpoint that corresponds to the AWS Region to use in [Amazon Bedrock Runtime endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt). If you use an AWS SDK, you might only need to specify the region code and not the whole endpoint when you set up the client.
+ **Model access** – Request access to an Amazon Bedrock model that supports this feature. For more information, see [Manage model access using SDK and CLI](model-access.md#model-access-modify).
+ **Install an OpenAI SDK** – For more information, see [Libraries](https://platform.openai.com/docs/libraries) in the OpenAI documentation.
+ **Batch JSONL file uploaded to S3** – Follow the steps at [Prepare your batch file](https://platform.openai.com/docs/guides/batch#1-prepare-your-batch-file) in the OpenAI documentation to prepare your batch file with the correct format. Then upload it to an Amazon S3 bucket.
+ **IAM permissions** – Make sure that you have the following IAM identities with the proper permissions:
  + An IAM identity that you authenticate with can carry out batch inference-related API operations. For more information, see [Required permissions for an IAM identity to submit and manage batch inference jobs](batch-inference-permissions.md).
  + The batch inference service role that you use can assume your identity, invoke the OpenAI model that you use, and has access to your batch JSONL file in S3. For more information, see [Service roles](security-iam-sr.md).

------
#### [ HTTP request ]
+ **Authentication** – You can authenticate with either your AWS credentials or with an Amazon Bedrock API key.

  Set up your AWS credentials or generate an Amazon Bedrock API key to authenticate your request.
  + To learn about setting up your AWS credentials, see [Programmatic access with AWS security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds-programmatic-access.html).
  + To learn about Amazon Bedrock API keys and how to generate them, see the API keys section in the Build chapter.
+ **Endpoint** – Find the endpoint that corresponds to the AWS Region to use in [Amazon Bedrock Runtime endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-rt). If you use an AWS SDK, you might only need to specify the region code and not the whole endpoint when you set up the client.
+ **Model access** – Request access to an Amazon Bedrock model that supports this feature. For more information, see [Manage model access using SDK and CLI](model-access.md#model-access-modify).
+ **Batch JSONL file uploaded to S3** – Follow the steps at [Prepare your batch file](https://platform.openai.com/docs/guides/batch#1-prepare-your-batch-file) in the OpenAI documentation to prepare your batch file with the correct format. Then upload it to an Amazon S3 bucket.
+ **IAM permissions** – Make sure that you have the following IAM identities with the proper permissions:
  + An IAM identity that you authenticate with can carry out batch inference-related API operations. For more information, see [Required permissions for an IAM identity to submit and manage batch inference jobs](batch-inference-permissions.md).
  + The batch inference service role that you use can assume your identity, invoke the OpenAI model that you use, and has access to your batch JSONL file in S3. For more information, see [Service roles](security-iam-sr.md).

------

## Create an OpenAI batch job
<a name="inference-openai-batch-create"></a>

For details about the OpenAI Create batch API, refer to the following resources in the OpenAI documentation:
+ [Create batch](https://platform.openai.com/docs/api-reference/batch/create) – Details both the request and response.
+ [The request output object](https://platform.openai.com/docs/api-reference/batch/request-output) – Details the fields of the generated output from the batch job. Refer to this documentation when interpreting the results in your S3 bucket.

**Form the request**  
When forming the batch inference request, note the following Amazon Bedrock-specific fields and values:

**Request headers**
+ X-Amzn-Bedrock-RoleArn (required) – The Amazon Resource Name (ARN) of the batch inference service role. For more information, see [Create a custom service role for batch inference](batch-iam-sr.md)
+ X-Amzn-Bedrock-ModelId (required) – The ID of the foundation model to use in inference. For more information, see [Supported foundation models in Amazon Bedrock](models-supported.md).
+ X-Amzn-Bedrock-OutputEncryptionKeyId (optional) – The ID of a KMS key that you want to use to encrypt the output S3 files. For more information, see [Specifying server-side encryption with AWS KMS (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/specifying-kms-encryption.html).
+ X-Amzn-Bedrock-Tags (optional) – A dictionary of keys and values that indicate tags to attach to the output. For more information, see [Tagging Amazon Bedrock resources](tagging.md).

**Request body parameters:**
+ endpoint – Must be `v1/chat/completions`.
+ input\_file\_id – Specify the S3 URI of your batch JSONL file.

**Find the generated results**  
The creation response includes a batch ID. The results and error logging of the batch inference job are written to the S3 folder containing the input file. The results will be in a folder with the same name as the batch ID, as in the following folder structure:

```
---- {batch_input_folder}
        |---- {batch_input}.jsonl
        |---- {batch_id}
	           |---- {batch_input}.jsonl.out
	           |---- {batch_input}.jsonl.err
```

To see examples of using the OpenAI Create batch API with different methods, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

To create a batch job with the OpenAI SDK, do the following:

1. Import the OpenAI SDK and set up the client with the following fields:
   + `base_url` – Prefix the Amazon Bedrock Runtime endpoint to `/openai/v1`, as in the following format:

     ```
     https://{{${bedrock-runtime-endpoint}}}/openai/v1
     ```
   + `api_key` – Specify an Amazon Bedrock API key.
   + `default_headers` – If you need to include any headers, you can include them as key-value pairs in this object. You can alternatively specify headers in the `extra_headers` when making a specific API call.

1. Use the [batches.create()](https://platform.openai.com/docs/api-reference/batch/create) method with the client.

Before running the following example, replace the placeholders in the following fields:
+ api\_key – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ X-Amzn-BedrockRoleArn – Replace {{arn:aws:iam::123456789012:role/BatchServiceRole}} with the actual batch inference service role you set up.
+ input\_file\_id – Replace {{s3://amzn-s3-demo-bucket/openai-input.jsonl}} with the actual S3 URI to which you uploaded your batch JSONL file.

The example calls the OpenAI Create batch job API in `us-west-2` and includes one piece of metadata.

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1", 
    api_key="$AWS_BEARER_TOKEN_BEDROCK", # Replace with actual API key
    default_headers={
        "X-Amzn-Bedrock-RoleArn": "arn:aws:iam::123456789012:role/BatchServiceRole" # Replace with actual service role ARN
    }
)

job = client.batches.create(
    input_file_id="s3://amzn-s3-demo-bucket/openai-input.jsonl", # Replace with actual S3 URI
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "test input"
    },
    extra_headers={
        "X-Amzn-Bedrock-ModelId": "openai.gpt-oss-20b-1:0",
    }
)
print(job)
```

------
#### [ HTTP request ]

To create a chat completion with a direct HTTP request, do the following:

1. Use the POST method and specify the URL by prefixing the Amazon Bedrock Runtime endpoint to `/openai/v1/batches`, as in the following format:

   ```
   {{https://${bedrock-runtime-endpoint}}}/openai/v1/batches
   ```

1. Specify your AWS credentials or an Amazon Bedrock API key in the `Authorization` header.

Before running the following example, first replace the placeholders in the following fields:
+ Authorization – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ X-Amzn-BedrockRoleArn – Replace {{arn:aws:iam::123456789012:role/BatchServiceRole}} with the actual batch inference service role you set up.
+ input\_file\_id – Replace {{s3://amzn-s3-demo-bucket/openai-input.jsonl}} with the actual S3 URI to which you uploaded your batch JSONL file.

The following example calls the Create chat completion API in `us-west-2` and includes one piece of metadata:

```
curl -X POST 'https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1/batches' \
    -H 'Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK' \  
    -H 'Content-Type: application/json' \
    -H 'X-Amzn-Bedrock-ModelId: openai.gpt-oss-20b-1:0' \
    -H 'X-Amzn-Bedrock-RoleArn: arn:aws:iam::123456789012:role/BatchServiceRole' \  
    -d '{    
    "input_file_id": "s3://amzn-s3-demo-bucket/openai-input.jsonl",    
    "endpoint": "/v1/chat/completions",    
    "completion_window": "24h",
    "metadata": {"description": "test input"}  
}'
```

------

## Retrieve an OpenAI batch job
<a name="inference-openai-batch-retrieve"></a>

For details about the OpenAI Retrieve batch API request and response, refer to [Retrieve batch](https://platform.openai.com/docs/api-reference/batch/retrieve).

When you make the request, you specify the ID of the batch job for which to get information. The response returns information about a batch job, including the output and error file names that you can look up in your S3 buckets.

To see examples of using the OpenAI Retrieve batch API with different methods, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

To retrieve a batch job with the OpenAI SDK, do the following:

1. Import the OpenAI SDK and set up the client with the following fields:
   + `base_url` – Prefix the Amazon Bedrock Runtime endpoint to `/openai/v1`, as in the following format:

     ```
     https://{{${bedrock-runtime-endpoint}}}/openai/v1
     ```
   + `api_key` – Specify an Amazon Bedrock API key.
   + `default_headers` – If you need to include any headers, you can include them as key-value pairs in this object. You can alternatively specify headers in the `extra_headers` when making a specific API call.

1. Use the [batches.retrieve()](https://platform.openai.com/docs/api-reference/batch/create) method with the client and specify the ID of the batch for which to retrieve information.

Before running the following example, replace the placeholders in the following fields:
+ api\_key – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ batch\_id – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.

The example calls the OpenAI Retrieve batch job API in `us-west-2` on a batch job whose ID is {{batch\_abc123}}.

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1", 
    api_key="$AWS_BEARER_TOKEN_BEDROCK" # Replace with actual API key
)

job = client.batches.retrieve(batch_id="batch_abc123") # Replace with actual ID

print(job)
```

------
#### [ HTTP request ]

To retrieve a batch job with a direct HTTP request, do the following:

1. Use the GET method and specify the URL by prefixing the Amazon Bedrock Runtime endpoint to `/openai/v1/batches/{{${batch_id}}}`, as in the following format:

   ```
   {{https://${bedrock-runtime-endpoint}}}/openai/v1/batches/{{batch_abc123}}
   ```

1. Specify your AWS credentials or an Amazon Bedrock API key in the `Authorization` header.

Before running the following example, first replace the placeholders in the following fields:
+ Authorization – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ batch\_abc123 – In the path, replace this value with the actual ID of your batch job.

The following example calls the OpenAI Retrieve batch API in `us-west-2` on a batch job whose ID is {{batch\_abc123}}.

```
curl -X GET 'https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1/batches/batch_abc123' \
    -H 'Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK'
```

------

## List OpenAI batch jobs
<a name="inference-openai-batch-list"></a>

For details about the OpenAI List batches API request and response, refer to [List batches](https://platform.openai.com/docs/api-reference/batch/list). The response returns an array of information about your batch jobs.

When you make the request, you can include query parameters to filter the results. The response returns information about a batch job, including the output and error file names that you can look up in your S3 buckets.

To see examples of using the OpenAI List batches API with different methods, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

To list batch jobs with the OpenAI SDK, do the following:

1. Import the OpenAI SDK and set up the client with the following fields:
   + `base_url` – Prefix the Amazon Bedrock Runtime endpoint to `/openai/v1`, as in the following format:

     ```
     https://{{${bedrock-runtime-endpoint}}}/openai/v1
     ```
   + `api_key` – Specify an Amazon Bedrock API key.
   + `default_headers` – If you need to include any headers, you can include them as key-value pairs in this object. You can alternatively specify headers in the `extra_headers` when making a specific API call.

1. Use the [batches.list()](https://platform.openai.com/docs/api-reference/batch/list) method with the client. You can include any of the optional parameters.

Before running the following example, replace the placeholders in the following fields:
+ api\_key – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.

The example calls the OpenAI List batch jobs API in `us-west-2` and specifies a limit of 2 results to return.

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1", 
    api_key="$AWS_BEARER_TOKEN_BEDROCK" # Replace with actual API key
)

job = client.batches.list(limit=2)

print(job)
```

------
#### [ HTTP request ]

To list batch jobs with a direct HTTP request, do the following:

1. Use the GET method and specify the URL by prefixing the Amazon Bedrock Runtime endpoint to `/openai/v1/batches`, as in the following format:

   ```
   {{https://${bedrock-runtime-endpoint}}}/openai/v1/batches
   ```

   You can include any of the optional query parameters.

1. Specify your AWS credentials or an Amazon Bedrock API key in the `Authorization` header.

Before running the following example, first replace the placeholders in the following fields:
+ Authorization – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.

The following example calls the OpenAI List batches API in `us-west-2` and specifies a limit of 2 results to return.

```
curl -X GET 'https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1/batches?limit=2' \
    -H 'Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK' \
```

------

## Cancel an OpenAI batch job
<a name="inference-openai-batch-cancel"></a>

For details about the OpenAI Cancel batch API request and response, refer to [Cancel batch](https://platform.openai.com/docs/api-reference/batch/cancel). The response returns information about the cancelled batch job.

When you make the request, you specify the ID of the batch job that you want to cancel.

To see examples of using the OpenAI Cancel batch API with different methods, choose the tab for your preferred method, and then follow the steps:

------
#### [ OpenAI SDK (Python) ]

To cancel a batch job with the OpenAI SDK, do the following:

1. Import the OpenAI SDK and set up the client with the following fields:
   + `base_url` – Prefix the Amazon Bedrock Runtime endpoint to `/openai/v1`, as in the following format:

     ```
     https://{{${bedrock-runtime-endpoint}}}/openai/v1
     ```
   + `api_key` – Specify an Amazon Bedrock API key.
   + `default_headers` – If you need to include any headers, you can include them as key-value pairs in this object. You can alternatively specify headers in the `extra_headers` when making a specific API call.

1. Use the [batches.cancel()](https://platform.openai.com/docs/api-reference/batch/cancel) method with the client and specify the ID of the batch for which to retrieve information.

Before running the following example, replace the placeholders in the following fields:
+ api\_key – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ batch\_id – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.

The example calls the OpenAI Cancel batch job API in `us-west-2` on a batch job whose ID is {{batch\_abc123}}.

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1", 
    api_key="$AWS_BEARER_TOKEN_BEDROCK" # Replace with actual API key
)

job = client.batches.cancel(batch_id="batch_abc123") # Replace with actual ID

print(job)
```

------
#### [ HTTP request ]

To cancel a batch job with a direct HTTP request, do the following:

1. Use the POST method and specify the URL by prefixing the Amazon Bedrock Runtime endpoint to `/openai/v1/batches/{{${batch_id}}}/cancel`, as in the following format:

   ```
   {{https://${bedrock-runtime-endpoint}}}/openai/v1/batches/{{batch_abc123}}/cancel
   ```

1. Specify your AWS credentials or an Amazon Bedrock API key in the `Authorization` header.

Before running the following example, first replace the placeholders in the following fields:
+ Authorization – Replace {{$AWS\_BEARER\_TOKEN\_BEDROCK}} with your actual API key.
+ batch\_abc123 – In the path, replace this value with the actual ID of your batch job.

The following example calls the OpenAI Cancel batch API in `us-west-2` on a batch job whose ID is {{batch\_abc123}}.

```
curl -X GET 'https://bedrock-runtime.us-west-2.amazonaws.com/openai/v1/batches/batch_abc123/cancel' \
    -H 'Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK'
```

------