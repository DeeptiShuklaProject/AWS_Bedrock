

# Step 6: Clean up resources
<a name="agent-tutorial-step6"></a>

When you're done with your Amazon Bedrock agent, you should clean up the resources to avoid incurring unnecessary charges. In this final procedure, you'll systematically delete all the AWS resources created during this tutorial, including the Bedrock agent, Lambda function, and associated \*IAM roles. This cleanup process is important for cost management, as it prevents ongoing charges for resources you're no longer using. The procedure is organized into three parts: deleting the agent, removing the Lambda function, and cleaning up the IAM roles that were created to support these services.

**Topics**
+ [Delete the agent](#agent-tutorial-step6-console-agent)
+ [Delete the Lambda function](#agent-tutorial-step6-console-lambda)
+ [Delete the IAM roles](#agent-tutorial-step6-console-iam)

## Delete the agent
<a name="agent-tutorial-step6-console-agent"></a>

**Delete the agent**

1. In the Amazon Bedrock console, open the agent that you created in [Step 2: Create an Amazon Bedrock agent](agent-tutorial-step2.md)

1. Select the agent you created.

1. Choose **Delete**.

1. Confirm the deletion.

## Delete the Lambda function
<a name="agent-tutorial-step6-console-lambda"></a>

**Delete the Lambda function**

1. Open the AWS Lambda console at [https://console.aws.amazon.com/lambda/](https://console.aws.amazon.com/lambda/).

1. Select the Lambda function you created.

1. Choose **Actions**, then **Delete**.

1. Confirm the deletion.

## Delete the IAM roles
<a name="agent-tutorial-step6-console-iam"></a>

**Delete the IAM roles**

1. Open the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

1. In the navigation pane, choose **Roles**.

1. Select the agent service role that you created.

1. Choose **Delete**.

1. Confirm the deletion.

1. Repeat for the Lambda execution role.