

# Adding layers to functions
<a name="adding-layers"></a>

A Lambda layer is a .zip file archive that contains supplementary code or data. Layers usually contain library dependencies, a [custom runtime](runtimes-custom.md), or configuration files. 

This section explains how to add a layer to a Lambda function. For more conceptual information about layers and why you might consider using them, see [Managing Lambda dependencies with layers](chapter-layers.md).

Before you can configure a Lambda function to use a layer, you must:
+ [Package your layer content](packaging-layers.md)
+ [Create a layer in Lambda](creating-deleting-layers.md)
+ Make sure that you have permission to call the [GetLayerVersion](https://docs.aws.amazon.com/lambda/latest/api/API_GetLayerVersion.html) API on the layer version. For functions in your AWS account, you must have this permission in your [user policy](access-control-identity-based.md). To use a layer in another account, the owner of that account must grant your account permission in a [resource-based policy](access-control-resource-based.md). For examples, see [Granting Lambda layer access to other accounts](permissions-layer-cross-account.md).

You can add up to five layers to a Lambda function. The total unzipped size of the function and all layers cannot exceed the unzipped deployment package size quota of 250 MB. For more information, see [Lambda quotas](gettingstarted-limits.md).

Your functions can continue to use any layer version that you’ve already added, even after that layer version has been deleted, or after your permission to access the layer is revoked. However, you cannot create a new function that uses a deleted layer version.

**To add a layer to a function**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function.

1. Scroll down to the **Layers** section, and then choose **Add a layer**.

1. Under **Choose a layer**, choose a layer source:

   1. **AWS layers**: Choose from the list of [AWS-managed extensions](extensions-api-partners.md#aws-managed-extensions).

   1. **Custom layers**: Choose a layer created in your AWS account.

   1. **Specify an ARN**: To use a layer [from a different AWS account](permissions-layer-cross-account.md), such as a [third-party extension](extensions-api-partners.md), enter the Amazon Resource Name (ARN).

1. Choose **Add**.

The order in which you add the layers is the order in which Lambda merges the layer content into the execution environment. You can change the layer merge order using the console.

**To update layer merge order for your function (console)**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the function to configure.

1. Under **Layers**, choose **Edit**

1. Choose one of the layers.

1. Choose **Merge earlier** or **Merge later** to adjust the order of the layers.

1. Choose **Save**.

Layers are versioned. The content of each layer version is immutable. The owner of a layer can release new layer versions to provide updated content. You can use the console to update the layer version attached to your functions.

**To update layer versions for your function (console)**

1. Open the [Layers page](https://console.aws.amazon.com/lambda/home#/layers) of the Lambda console.

1. Choose the layer you want to update the version for.

1. Choose the **Functions using this version** tab.

1. Choose the functions you want to modify, then choose **Edit**.

1. For **Layer version**, choose the layer version to change to.

1. Choose **Update functions**.

You cannot update function layer versions across AWS accounts.

## Finding layer information
<a name="finding-layer-information"></a>

To find layers in your account that are compatible with your function’s runtime, use the [ListLayers](https://docs.aws.amazon.com/lambda/latest/api/API_ListLayers.html) API. For example, you can use the following [list-layers](https://docs.aws.amazon.com/cli/latest/reference/lambda/list-layers.html) AWS Command Line Interface (CLI) command:

```
aws lambda list-layers --compatible-runtime python3.14
```

You should see output similar to the following:

```
{
    "Layers": [
        {
            "LayerName": "my-layer",
            "LayerArn": "arn:aws:lambda:us-east-2:123456789012:layer:my-layer",
            "LatestMatchingVersion": {
                "LayerVersionArn": "arn:aws:lambda:us-east-2:123456789012:layer:my-layer:2",
                "Version": 2,
                "Description": "My layer",
                "CreatedDate": "2025-04-15T00:37:46.592+0000",
                "CompatibleRuntimes": [
                    "python3.14"
                ]
            }
        }
    ]
}
```

To list all layers in your account, omit the `--compatible-runtime` option. The response details show the latest version of each layer.

You can also get the latest version of a layer using the [ListLayerVersions](https://docs.aws.amazon.com/lambda/latest/api/API_ListLayerVersions.html) API. For example, you can use the following `list-layer-versions` CLI command:

```
aws lambda list-layer-versions --layer-name my-layer
```

You should see output similar to the following:

```
{
    "LayerVersions": [
        {
            "LayerVersionArn": "arn:aws:lambda:us-east-2:123456789012:layer:my-layer:2",
            "Version": 2,
            "Description": "My layer",
            "CreatedDate": "2023-11-15T00:37:46.592+0000",
            "CompatibleRuntimes": [
                "java11"
            ]
        },
        {
            "LayerVersionArn": "arn:aws:lambda:us-east-2:123456789012:layer:my-layer:1",
            "Version": 1,
            "Description": "My layer",
            "CreatedDate": "2023-11-15T00:27:46.592+0000",
            "CompatibleRuntimes": [
                "java11"
            ]
        }
    ]
}
```