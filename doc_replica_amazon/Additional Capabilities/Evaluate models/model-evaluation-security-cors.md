

# Required Cross Origin Resource Sharing (CORS) permissions on S3 buckets
<a name="model-evaluation-security-cors"></a>

**Cross Origin Resource Sharing (CORS) permission requirements**  
CORS permissions are only required on the Amazon S3 output bucket for **human-based** model evaluation jobs created using the Amazon Bedrock console. This is necessary to allow displaying prompts and inference results to human annotators in the annotation portal. Automated model evaluation jobs do not require CORS configuration.

When you create a human-based model evaluation job using the Amazon Bedrock console, you must specify a CORS configuration on the S3 output bucket.

A CORS configuration is a document that defines rules that identify the origins that you will allow to access your bucket, the operations (HTTP methods) supported for each origin, and other operation-specific information. To learn more about setting the required CORS configuration using the S3 console, see [Configuring cross-origin resource sharing (CORS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html) in the *Amazon S3 User Guide*.

The following is the minimal required CORS configuration for the S3 output bucket in human-based evaluation jobs:

```
[
    {
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "https://mturk-console-template-preview-hooks.s3.amazonaws.com"
        ]
    }
]
```