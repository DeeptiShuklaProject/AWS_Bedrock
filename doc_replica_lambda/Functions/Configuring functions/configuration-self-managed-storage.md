

# Self-managed S3 code storage
<a name="configuration-self-managed-storage"></a>

By default, when you create or update a Lambda function or layer from a .zip file archive, Lambda stores a copy of your code in Lambda-managed storage. Each AWS account has a 300 GB quota for Lambda-managed storage per Region.

With self-managed S3 code storage, you can configure Lambda to reference your code directly from an S3 bucket in your account. Lambda does not store a copy of your code, so the code does not count against your Lambda-managed storage quota. Lambda accesses your code directly from your S3 bucket.

Self-managed S3 code storage is available for all functions and layers created and updated using .zip file archives. It is compatible with all S3 storage classes except Glacier storage classes.

**Note**  
Self-managed S3 code storage does not change the maximum .zip deployment package size, which remains at 250 MB (unzipped).

**Topics**
+ [Setting up self-managed S3 code storage](#self-managed-storage-setup)
+ [Configuring permissions](#self-managed-storage-permissions)
+ [Creating a function with self-managed S3 storage](#self-managed-storage-create-function)
+ [Using self-managed S3 storage with layers](#self-managed-storage-layers)
+ [Switching between storage modes](#self-managed-storage-switching)
+ [Function lifecycle with self-managed storage](#self-managed-storage-lifecycle)
+ [Cross-account and cross-Region usage](#self-managed-storage-cross-account)
+ [Considerations](#self-managed-storage-considerations)

## Setting up self-managed S3 code storage
<a name="self-managed-storage-setup"></a>

To use self-managed S3 code storage, complete the following steps:

1. Create an S3 bucket or use an existing bucket in your account.

1. Enable [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) for the bucket. Lambda requires S3 versioning to track which version of your source object to use. Each time you upload a new .zip package, S3 creates a new version so Lambda can distinguish updates.

1. Upload your .zip deployment package to the S3 bucket.

1. Grant the Lambda service principal `s3:GetObject` and `s3:GetObjectVersion` permissions for the source object. See [Configuring permissions](#self-managed-storage-permissions).

1. Create or update your function or layer, specifying the S3 object, S3 key, S3 object version, and setting `S3ObjectStorageMode` to `REFERENCE`.

## Configuring permissions
<a name="self-managed-storage-permissions"></a>

To use self-managed S3 code storage, grant the Lambda service principal (`lambda.amazonaws.com`) permission to access your source objects. Add the following S3 bucket policy:

```
{
  "Version": "2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid": "LambdaSelfManagedCodeAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": [
        "arn:aws:s3:::{{my-bucket}}/{{my-function.zip}}"
      ],
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:lambda:{{us-east-1}}:{{111122223333}}:function:{{my-function}}"
        }
      }
    }
  ]
}
```

## Creating a function with self-managed S3 storage
<a name="self-managed-storage-create-function"></a>

You can create a function with self-managed S3 code storage using the AWS CLI or AWS CloudFormation.

### Using the AWS CLI
<a name="self-managed-storage-cli"></a>

Use the `create-function` command with the `S3ObjectStorageMode=REFERENCE` parameter:

```
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --role arn:aws:iam::111122223333:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --code S3Bucket={{my-bucket}},\
S3Key={{my-function.zip}},\
S3ObjectVersion={{abc123def456}},\
S3ObjectStorageMode=REFERENCE
```

To update an existing function to use self-managed S3 storage:

```
aws lambda update-function-code \
  --function-name my-function \
  --s3-bucket {{my-bucket}} \
  --s3-key {{my-function.zip}} \
  --s3-object-version {{abc123def456}} \
  --s3-object-storage-mode REFERENCE
```

**Important**  
You must specify `S3ObjectStorageMode=REFERENCE` on every call to `update-function-code`. If you omit `S3ObjectStorageMode`, it defaults to `COPY` and Lambda stores your code in Lambda-managed storage.

### Using AWS CloudFormation
<a name="self-managed-storage-cfn"></a>

In your CloudFormation template, set `S3ObjectStorageMode` to `REFERENCE` in the `Code` property of the `AWS::Lambda::Function` resource:

```
Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-function
      Runtime: python3.12
      Handler: lambda_function.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: {{my-bucket}}
        S3Key: {{my-function.zip}}
        S3ObjectVersion: {{abc123def456}}
        S3ObjectStorageMode: REFERENCE
```

## Using self-managed S3 storage with layers
<a name="self-managed-storage-layers"></a>

You can also use self-managed S3 code storage for layer versions. Use the `publish-layer-version` command with `S3ObjectStorageMode=REFERENCE`:

```
aws lambda publish-layer-version \
  --layer-name my-layer \
  --content S3Bucket={{my-bucket}},S3Key={{my-layer.zip}},S3ObjectStorageMode=REFERENCE \
  --compatible-runtimes python3.12
```

You can use any combination of Lambda-managed and self-managed storage for function code and layer code.

## Switching between storage modes
<a name="self-managed-storage-switching"></a>

You can switch between Lambda-managed and self-managed S3 code storage when you update your function code or publish a new layer version. Set `S3ObjectStorageMode` to either `COPY` or `REFERENCE`:
+ `COPY` (default) – Lambda copies your source code to Lambda-managed storage.
+ `REFERENCE` – Lambda references your source code directly from your S3 bucket without storing a copy.

When you switch from `COPY` to `REFERENCE`, Lambda deletes the Lambda-managed copy of your source code. When you switch from `REFERENCE` to `COPY`, Lambda makes a copy of your source code in Lambda-managed storage. Switching to `COPY` fails if you exceed the Lambda-managed code storage limit.

## Function lifecycle with self-managed storage
<a name="self-managed-storage-lifecycle"></a>

Lambda periodically accesses the source object from your S3 bucket to reoptimize your function code. You must maintain access to the source object for your function to remain active.
+ If Lambda loses access to the source object for a function, the function transitions to the `Inactive` state. To restore the function, restore access to the source object and update the function.
+ If Lambda loses access to the source object for a layer, the function remains `Active`. You can update function configuration (without updating layers), update function code, or update function configuration with new layers. However, updating function configuration with the inaccessible layer fails.

## Cross-account and cross-Region usage
<a name="self-managed-storage-cross-account"></a>

You can create functions and layers from source code in S3 buckets in different accounts and in different Regions. Cross-Region object retrieval incurs additional S3 data transfer costs. See [S3 pricing](https://aws.amazon.com/s3/pricing/) for details.

## Considerations
<a name="self-managed-storage-considerations"></a>
+ Self-managed S3 code storage is available for .zip file archive functions and layers only. Container image functions continue to use Amazon ECR.
+ The maximum .zip deployment package size (250 MB unzipped) is unchanged.
+ You pay standard Amazon S3 storage rates for code stored in your self-managed buckets. Lambda does not charge for S3 object retrieval within the same Region.
+ Self-managed S3 code storage is compatible with all S3 storage classes except Glacier storage classes.
+ You can use S3 features like S3 Cross-Region Replication to share artifacts across Regions and S3 lifecycle policies to manage objects.