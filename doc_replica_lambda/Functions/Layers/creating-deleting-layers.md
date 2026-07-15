

# Creating and deleting layers in Lambda
<a name="creating-deleting-layers"></a>

A Lambda layer is a .zip file archive that contains supplementary code or data. Layers usually contain library dependencies, a [custom runtime](runtimes-custom.md), or configuration files. 

This section explains how to create and delete layers in Lambda. For more conceptual information about layers and why you might consider using them, see [Managing Lambda dependencies with layers](chapter-layers.md).

After you’ve [packaged your layer content](packaging-layers.md), the next step is to create the layer in Lambda. This section demonstrates how to create and delete layers using the Lambda console or the Lambda API only. To create a layer using AWS CloudFormation, see [Using AWS CloudFormation with layers](layers-cfn.md). To create a layer using the AWS Serverless Application Model (AWS SAM), see [Using AWS SAM with layers](layers-sam.md).

**Topics**
+ [Creating a layer](#layers-create)
+ [Deleting a layer version](#layers-delete)

## Creating a layer
<a name="layers-create"></a>

To create a layer, you can either upload the .zip file archive from your local machine or from Amazon Simple Storage Service (Amazon S3). When uploading from Amazon S3, you can choose whether Lambda copies the code to Lambda-managed storage or references it directly from your S3 bucket. For more information, see [Self-managed S3 code storage](configuration-self-managed-storage.md).

Lambda extracts the layer contents into the `/opt` directory when setting up the execution environment for the function.

Layers can have one or more [layer versions](chapter-layers.md#lambda-layer-versions). When you create a layer, Lambda sets the layer version to version 1. You can change the permissions on an existing layer version at any time. However, to update the code or make other configuration changes, you must create a new version of the layer.

**To create a layer (console)**

1. Open the [Layers page](https://console.aws.amazon.com/lambda/home#/layers) of the Lambda console.

1. Choose **Create layer**.

1. Under **Layer configuration**, for **Name**, enter a name for your layer.

1. (Optional) For **Description**, enter a description for your layer.

1. To upload your layer code, do one of the following:
   + To upload a .zip file from your computer, choose **Upload a .zip file**. Then, choose **Upload** to select your local .zip file.
   + To upload a file from Amazon S3, choose **Upload a file from Amazon S3**. Then, for **Amazon S3 link URL**, enter a link to the file.

1. (Optional) For **Compatible architectures**, choose one value or both values. For more information, see [Selecting and configuring an instruction set architecture for your Lambda function](foundation-arch.md).

1. (Optional) For **Compatible runtimes**, choose the runtimes that your layer is compatible with.

1. (Optional) For **License**, enter any necessary license information.

1. Choose **Create**.

Alternatively, you can run the [publish-layer-version](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/publish-layer-version.html) AWS Command Line Interface (CLI) command. When uploading from Amazon S3, include `S3ObjectStorageMode=REFERENCE` to use [self-managed S3 code storage](configuration-self-managed-storage.md), or omit it (defaults to `COPY`) to use Lambda-managed storage. Example:

```
aws lambda publish-layer-version --layer-name {{my-layer}} --zip-file fileb://layer.zip --compatible-runtimes {{python3.14}}
```

Each time that you run `publish-layer-version`, Lambda creates a new [version of the layer](chapter-layers.md#lambda-layer-versions).

## Deleting a layer version
<a name="layers-delete"></a>

To delete a layer version, use the [DeleteLayerVersion](https://docs.aws.amazon.com/lambda/latest/api/API_DeleteLayerVersion.html) API operation. For example, run the [delete-layer-version](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/delete-layer-version.html) AWS CLI command with the layer name and layer version specified.

```
aws lambda delete-layer-version --layer-name my-layer --version-number 1
```

When you delete a layer version, you can no longer configure new functions to use it. However, any function that already references the deleted layer version continues to run with that layer content. Lambda never reuses version numbers for a layer name.

### Storage quota impact of deleting layers
<a name="layers-delete-storage"></a>

The storage quota impact of deleting a layer version depends on the storage mode used by the layer and by the functions that reference it.

Layer uses Lambda-managed storage (COPY)  
When you delete a layer version that uses Lambda-managed storage, the layer code is removed from your account's Lambda-managed storage quota. However, any function that still references the deleted layer version continues to have access to the layer content. The layer content counts towards the function's deployment package size quota (250 MB unzipped) but no longer counts towards the account-level Lambda-managed storage quota.

Layer uses self-managed S3 storage (REFERENCE)  
Layers that use [self-managed S3 code storage](configuration-self-managed-storage.md) do not consume Lambda-managed storage, so deleting them has no impact on your Lambda-managed storage quota. Functions that reference a deleted self-managed layer version continue to run normally. However, if you also delete the source object from your S3 bucket or revoke Lambda's access to it, you can no longer update function configuration with that layer.

**Note**  
Deleting a layer version never deactivates functions that reference it. Functions remain `Active` regardless of whether the layer used Lambda-managed or self-managed S3 storage. The `Inactive` state only applies when Lambda loses access to a function's own source code stored in a self-managed S3 bucket.