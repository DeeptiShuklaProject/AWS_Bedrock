

# Get started in the Amazon Bedrock console
<a name="getting-started-console"></a>

This section describes how to use the [playgrounds](playgrounds.md) in the AWS console to submit a text prompt to an Amazon Bedrock foundation model (FM) and generate a text or image response. Before you run the following examples, you should check that you have fulfilled the following prerequisites:

**Prerequisites**
+ You have an AWS account and have permissions to access a role in that account with the necessary permissions for Amazon Bedrock. Otherwise, follow the steps at [Quickstart](getting-started.md).
+ You're in the US East (N. Virginia) (us-east-1) Region. To change Regions, choose the Region name at the top right of the console, next to your IAM role. Then select US East (N. Virginia) (us-east-1).

**Topics**
+ [Explore the text playground](#getting-started-text)
+ [Explore the image playground](#getting-started-image)

## Explore the text playground
<a name="getting-started-text"></a>

The following example demonstrates how to use the text playground:

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Text** under **Playgrounds**.

1. Choose **Select model** and select a provider and model. For this example, we will select **Amazon Titan Text G1 - Lite**. Then choose **Apply**

1. Select a default prompt from below the text panel, or enter a prompt into the text panel, such as **Describe the purpose of a "hello world" program in one line**.

1. Choose **Run** to run inference on the model. The generated text appears below your prompt in the text panel.

## Explore the image playground
<a name="getting-started-image"></a>

The following example demonstrates how to use the image playground.

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Image** under **Playgrounds**.

1. Choose **Select model** and select a provider and model. For this example, we will select **Amazon Titan Image Generator G1 V1**. Then choose **Apply**

1. Select a default prompt from below the text panel, or enter a prompt into the text panel, such as **Generate an image of happy cats**.

1. In the **Configurations** pane, change the **Number of images** to **1**.

1. Choose **Run** to run inference on the model. The generated image appears above the prompt.