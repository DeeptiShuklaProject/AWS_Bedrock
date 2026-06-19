

# Step 2: Create an Amazon Bedrock agent
<a name="agent-tutorial-step2"></a>

Next, you'll create an Amazon Bedrock agent. In this procedure, you'll set up an agent in the Amazon Bedrock console, configure it with a foundation model, and provide instructions that define its behavior as a friendly chatbot that returns date and time information. You'll also create an action group with an OpenAPI schema that defines the API endpoints your agent can call, specifically the endpoint to get the current date and time. Additionally, you'll add an inline policy to your agent's IAM role to allow it to invoke your Lambda function. The agent will serve as the interface between users and your Lambda function, interpreting natural language requests and converting them into structured function calls to retrieve date and time information.

For more information, see [Create and configure agent manually](agents-create.md).

**Create an Amazon Bedrock agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Make sure that you are in an AWS [Region](https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/select-region.html) that supports Amazon Bedrock [agents](agents-supported.md). 

1. In the navigation pane, under **Builder tools**, choose **Agents**.

1. Choose **Create agent**.

1. For **Name**, enter a name for your agent (for example, `MyBedrockAgent`).

1. (Optional) For **Description**, enter a description.

1. Choose **Create**. The **Agent builder** pane opens.

1. In the **Agent details** section:
   + For **Agent resource role**, select **Create and use a new service role**.
   + For **Select model**, select a model, such as Claude 3 Haiku.
   + In the **Instructions for the Agent** section, enter the folowing instructions.

     ```
     You are a friendly chat bot. You have access to a function called that returns
     information about the current date and time. When responding with date or time,
     please make sure to add the timezone UTC.
     ```

1. Choose **Save**.

1. Choose the **Action groups** tab.

1. In **Action groups**, choose **Add**.

1. For **Enter Action group name**, enter a name for the action group (for example, `TimeActions`).

1. (Optional) For **Description** Enter a description for the action group.

1. In **Action group type**, select **Define with API schemas**.

1. In **Action group invocation**, choose **Select an existing Lambda function**. 

1. In **Select Lambda function**, select the name of the Lambda function that you created in [Step 1: Create a Lambda function](agent-tutorial-step1.md).

1. In **Action group schema**, select **Define via in-line schema editor**.

1. In **In-line OpenAPI schema** text box, replace the existing schema with the following OpenAPI YAML schema:

   ```
   openapi: 3.0.0
   info:
     title: Time API
     version: 1.0.0
     description: API to get the current date and time.
   paths:
     /get-current-date-and-time:
       get:
         summary: Gets the current date and time.
         description: Gets the current date and time.
         operationId: getDateAndTime
         responses:
           '200':
             description: Gets the current date and time.
             content:
               'application/json':
                 schema:
                   type: object
                   properties:
                     date:
                       type: string
                       description: The current date
                     time:
                       type: string
                       description: The current time
   ```

1. Review your action group configuration and choose **Create**.

1. Choose **Save** to save your changes.

1. Choose **Prepare** to prepare the agent.

1. Choose **Save and exit** to save your changes and exit the agent builder.

1. In the **Agent overview** section, under **Permissions**, choose the IAM service role. This opens the role in the IAM console. 

1. In the IAM console, Choose the **Permissions** tab.

1. Choose **Add permissions**, and then select **Create inline policy**.

1. Choose **JSON** and paste the following policy. Make sure `Resource` is the Amazon Resource Name (ARN) for your Lambda function. You noted the ARN in step 6 of [Step 1: Create a Lambda function](agent-tutorial-step1.md). 

   ```
   {
       "Version": "2012-10-17", 		 	 	 
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "lambda:InvokeFunction",
               "Resource": "arn:aws:lambda:{{region}}:{{account-id}}:function:{{function-name}}"
           }
       ]
   }
   ```

1. Choose **Next**.

1. Enter a name for the policy (for example, `BedrockAgentLambdaInvoke`).

1. Choose **Create policy**.