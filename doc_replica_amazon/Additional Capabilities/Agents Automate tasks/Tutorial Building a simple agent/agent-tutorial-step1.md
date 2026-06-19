

# Step 1: Create a Lambda function
<a name="agent-tutorial-step1"></a>

First, create a Lambda function that your agent will invoke to perform actions. In this procedure, you'll create a Python Lambda function that returns the current date and time when invoked. You'll set up the function with basic permissions, add the necessary code to handle requests from your Amazon Bedrock agent, and deploy the function so it's ready to be connected to your agent.

For more information, see [Create your first Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) in the *AWS Lambda developer guide*.

**Create a Lambda function**

1. Sign in to the AWS Management Console and open the Lambda console at [https://console.aws.amazon.com/lambda/](https://console.aws.amazon.com/lambda/).

1. Choose **Create function**.

1. Select **Author from scratch**.

1. In the **Basic information** section:
   + For **Function name**, enter a function name (for example, `DateTimeFunction`). Note the name of the function, you'll need it in step 15 of [Step 2: Create an Amazon Bedrock agent](agent-tutorial-step2.md).
   + For **Runtime**, select **Python 3.9** (or your preferred version).
   + For **Architecture**, leave unchanged.
   + In **Permissions**, select **Change default execution role** and then select **Create a new role with basic Lambda permissions**.

1. Choose **Create function**.

1. In **Function overview**, under **Function ARN**, note the Amazon Resource Name (ARN) for the function. You need it for step 24 of [Step 2: Create an Amazon Bedrock agent](agent-tutorial-step2.md). 

1. In the **Code** tab, replace the existing code with the following:

   ```
   # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
   # SPDX-License-Identifier: Apache-2.0
   import datetime
   import json
   
   
   def lambda_handler(event, context):
       now = datetime.datetime.now()
   
       response = {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S")}
   
       response_body = {"application/json": {"body": json.dumps(response)}}
   
       action_response = {
           "actionGroup": event["actionGroup"],
           "apiPath": event["apiPath"],
           "httpMethod": event["httpMethod"],
           "httpStatusCode": 200,
           "responseBody": response_body,
       }
   
       session_attributes = event["sessionAttributes"]
       prompt_session_attributes = event["promptSessionAttributes"]
   
       return {
           "messageVersion": "1.0",
           "response": action_response,
           "sessionAttributes": session_attributes,
           "promptSessionAttributes": prompt_session_attributes,
       }
   ```

1. Choose **Deploy** to deploy your function.

1. Choose the **Configuration** tab.

1. Choose **Permissions**.

1. Under **Resource-based policy statements**, choose **Add permissions**.

1. In **Edit policy statement**, do the following:

   1. Choose **AWS service**

   1. In **Service** select **Other**.

   1. For **Statement ID**, enter a unique identifier (for example, `AllowBedrockInvocation`).

   1. For **Principal**, enter `bedrock.amazonaws.com`.

   1. For **Source ARN**, enter `arn:aws:bedrock:{{region}}:{{AWS account ID}}:agent/*`

      Replace `region` with AWS Region that you are using, such as `us-east-1`. Replace `AWS account ID` your AWS account Id.

   1. For **Action**, select `lambda:InvokeFunction`.

1. Choose **Save**.