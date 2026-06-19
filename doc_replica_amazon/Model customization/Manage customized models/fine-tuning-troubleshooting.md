

# Troubleshooting model customization issues
<a name="fine-tuning-troubleshooting"></a>

This section summarizes errors that you might encounter and what to check if you do.

## Permissions issues
<a name="w2aac17c31c44b5b1"></a>

If you encounter an issue with permissions to access an Amazon S3 bucket, check that the following are true:

1. If the Amazon S3 bucket uses a customer managed AWS Key Management Service (KMS key) for server-side encryption, ensure that the IAM role passed to Amazon Bedrock has `kms:Decrypt` permissions for the KMS key. For example, see [Allow a user to enccrypt and decrypt with any AWS KMS key in a specific AWS account](https://docs.aws.amazon.com/kms/latest/developerguide/customer-managed-policies.html#iam-policy-example-encrypt-decrypt-one-account).

1. The Amazon S3 bucket is in the same Region as the Amazon Bedrock model customization job.

1. The IAM role trust policy includes the service SP (`bedrock.amazonaws.com`).

The following messages indicate issues with permissions to access training or validation data in an Amazon S3 bucket:

```
Could not validate GetObject permissions to access Amazon S3 bucket: {{training-data-bucket}} at key {{train.jsonl}}
Could not validate GetObject permissions to access Amazon S3 bucket: {{validation-data-bucket}} at key {{validation.jsonl}}
```

If you encounter one of the preceding errors, check that the IAM role passed to the service has `s3:GetObject` and `s3:ListBucket` permissions for the training and validation dataset Amazon S3 URIs.

The following message indicates issues with permissions to write the output data in an Amazon S3 bucket:

```
Amazon S3 perms missing (PutObject): Could not validate PutObject permissions to access S3 bucket: {{bedrock-output-bucket}} at key {{output/.write_access_check_file.tmp}}
```

If you encounter the preceding error, check that the IAM role passed to the service has `s3:PutObject` permissions for the output data Amazon S3 URI.

## Data issues
<a name="w2aac17c31c44b5b3"></a>

The following errors are related to issues with the training, validation, or output data files:

**Invalid file format**

```
Unable to parse Amazon S3 file: {{fileName.jsonl}}. Data files must conform to JSONL format.
```

If you encounter the preceding error, check that the following are true:

1. Each line is in JSON.

1. Each JSON has two keys, an {{input}} and an {{output}}, and each key is a string. For example:

   ```
   {
       "input": "this is my input",
       "output": "this is my output"
   }
   ```

1. There are no additional new lines or empty lines.

**Character quota exceeded**

```
Input size exceeded in file {{fileName.jsonl}} for record starting with...
```

If you encounter an error beginning with the text above, ensure that the number of characters conforms to the character quota in [Prepare data for fine-tuning your models](model-customization-prepare.md).

**Token count exceeded**

```
Maximum input token count 4097 exceeds limit of 4096
Maximum output token count 4097 exceeds limit of 4096
Max sum of input and output token length 4097 exceeds total limit of 4096
```

If you encounter an error similar to the preceeding example, make sure that the number of tokens conforms to the token quota in [Prepare data for fine-tuning your models](model-customization-prepare.md).

## Third-party license terms and policy issues
<a name="w2aac17c31c44b5b5"></a>

The following errors are related to third-party's license terms and their policies:

**Fine-tuning materials inconsistent with third-party's license terms**

```
Automated tests flagged this fine-tuning job as including materials that are potentially inconsistent with Anthropic's third-party license terms. Please contact support.
```

If you encounter the preceding error, ensure your training dataset does not contain content that is inconsistent with Anthropic's usage policies. If the issue persists, contact Support.

## Internal error
<a name="w2aac17c31c44b5b7"></a>

```
Encountered an unexpected error when processing the request, please try again
```

If you encounter the preceding error, there might be an issue with the service. Try the job again. If the issue persists, contact Support.