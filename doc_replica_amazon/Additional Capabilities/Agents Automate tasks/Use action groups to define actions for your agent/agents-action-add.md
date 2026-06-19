

# Add an action group to your agent in Amazon Bedrock
<a name="agents-action-add"></a>

After setting up the OpenAPI schema and Lambda function for your action group, you can create the action group. Choose the tab for your preferred method, and then follow the steps:

**Note**  
If you are using Anthropic Claude 3.5 Sonnet, make sure that your tool name which will be of the form `httpVerb__actionGroupName__apiName` follows the Anthropic tool name format `^[a-zA-Z0-9_-]{1,64}$`. Your actionGroupName and apiName must not contain double underscores `'__'`.

------
#### [ Console ]

When you [create an agent](agents-create.md), you can add action groups to the working draft.

After an agent is created, you can add action groups to it by doing the following steps:

**To add an action group to an agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**.

1. In the **Action groups** section, choose **Add**.

1. (Optional) In the **Action group details** section, change the automatically generated **Name** and provide an optional **Description** for your action group.

1. In the **Action group type** section, select one of the following methods for defining the parameters that the agent can elicit from users to help carry out actions:

   1. **Define with function details** – Define parameters for your agent to elicit from the user to carry out the actions. For more information on adding functions, see [Define function details for your agent's action groups in Amazon Bedrock](agents-action-function.md).

   1. **Define with API schemas** – Define the API operations that the agent can invoke and the parameters . Use an OpenAPI schema that you created or use the console text editor to create the schema. For more information on setting up an OpenAPI schema, see [Define OpenAPI schemas for your agent's action groups in Amazon Bedrock](agents-api-schema.md)

1. In the **Action group invocation** section, you set up what the agent does after it predicts the API or function that it should invoke and receives the parameters that it needs. Choose one of the following options:
   + **Quick create a new Lambda function – *recommended*** – Let Amazon Bedrock create a basic Lambda function for your agent that you can later modify in AWS Lambda for your use case. The agent will pass the API or function that it predicts and the parameters, based on the session, to the Lambda function.
   + **Select an existing Lambda function** – Choose a [Lambda function that you created previously](agents-lambda.md) in AWS Lambda and the version of the function to use. The agent will pass the API or function that it predicts and the parameters, based on the session, to the Lambda function.
**Note**  
To allow the Amazon Bedrock service principal to access the Lambda function, [attach a resource-based policy to the Lambda function](agents-permissions.md#agents-permissions-lambda) to allow the Amazon Bedrock service principal to access the Lambda function.
   + **Return control** – Rather than passing the parameters for the API or function that it predicts to the Lambda function, the agent returns control to your application by passing the action that it predicts should be invoked, in addition to the parameters and information for the action that it determined from the session, in the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. For more information, see [Return control to the agent developer by sending elicited information in an InvokeAgent response](agents-returncontrol.md).

1. Depending on your choice for the **Action group type**, you'll see one of the following sections:
   + If you selected **Define with function details**, you'll have an **Action group function** section. Do the following to define the function:

     1. Provide a **Name** and optional (but recommended) **Description**.

     1. To request confirmation from the user before the function is invoked, select **Enabled**. Requesting confirmation before invoking the function may safeguard your application from taking actions due to malicious prompt injections.

     1. In the **Parameters** subsection, choose **Add parameter**. Define the following fields:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)

     1. To add another parameter, choose **Add parameter**.

     1. To edit a field in a parameter, select the field and edit it as necessary.

     1. To delete a parameter, choose the delete icon (![Trash can icon representing a delete action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/trash.png)) in the row containing the parameter.

     If you prefer to define the function by using a JSON object, choose **JSON editor** instead of **Table**. The JSON object format is as follows (each key in the `parameters` object is a parameter name that you provide):

     ```
     {
         "name": "string",
         "description": "string",
         "parameters": [
             {
                 "name": "string",
                 "description": "string",
                 "required": "True" | "False",
                 "type": "string" | "number" | "integer" | "boolean" | "array"
             }
         ]
     }
     ```

     To add another function to your action group by defining another set of parameters, choose **Add action group function**.
   + If you selected **Define with API schemas**, you'll have an **Action group schema** section with the following options:
     + To use an OpenAPI schema that you previously prepared with API descriptions, structures, and parameters for the action group, select **Select API schema** and provide a link to the Amazon S3 URI of the schema.
     + To define the OpenAPI schema with the in-line schema editor, select **Define via in-line schema editor**. A sample schema appears that you can edit.

       1. Select the format for the schema by using the dropdown menu next to **Format**.

       1. To import an existing schema from S3 to edit, select **Import schema**, provide the S3 URI, and select **Import**.

       1. To restore the schema to the original sample schema, select **Reset** and then confirm the message that appears by selecting **Reset** again.

1. When you're done creating the action group, choose **Add**. If you defined an API schema, a green success banner appears if there are no issues. If there are issues validating the schema, a red banner appears. You have the following options:
   + Scroll through the schema to see the lines where an error or warning about formatting exists. An X indicates a formatting error, while an exclamation mark indicates a warning about formatting.
   + Select **View details** in the red banner to see a list of errors about the content of the API schema.

1. Make sure to **Prepare** to apply the changes that you have made to the agent before testing it.

------
#### [ API ]

To create an action group, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). You must provide either a [ function schema](agents-action-function.md) or an [OpenAPI schema](agents-api-schema.md).

The following list describes the fields in the request:
+ The following fields are required:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)
+ To define the parameters for the action group, you must specify one of the following fields (you can't specify both).  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)

  The following shows the general format of the `functionSchema` and `apiSchema`:
  + Each item in the `functionSchema` array is a [FunctionSchema](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FunctionSchema.html) object. For each function, specify the following: 
    + Provide a `name` and optional (but recommended) `description`.
    + Optionally, specify `ENABLED` for `requireConfirmation` field to request confirmation from the user before the function is invoked. Requesting confirmation before invoking the function may safeguard your application from taking actions due to malicious prompt injections.
    + In the `parameters` object, each key is a parameter name, mapped to details about it in a [ParameterDetail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ParameterDetail.html) object.

    The general format of the `functionSchema` is as follows:

    ```
    "functionSchema": [
        {
            "name": "string",
            "description": "string",
            "requireConfirmation": ENABLED | DISABLED,
            "parameters": {
                "{{<string>}}": {
                    "type": "string" | number | integer | boolean | array,
                    "description": "string",
                    "required": boolean
                },
                ... // up to 5 parameters
            }
        },
        ... // up to 11 functions
    ]
    ```
  + The [APISchema](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_APISchema.html) can be in one of the following formats:

    1. For the following format, you can directly paste the JSON or YAML-formatted OpenAPI schema as the value.

       ```
       "apiSchema": {
           "payload": "string"
       }
       ```

    1. For the following format, specify the Amazon S3 bucket name and object key where the OpenAPI schema is stored.

       ```
       "apiSchema": {
           "s3": {
               "s3BucketName": "string",
               "s3ObjectKey": "string"
           }
       }
       ```
+ To configure how the action group handles the invocation of the action group after eliciting parameters from the user, you must specify one of the following fields within the `actionGroupExecutor` field.  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)
+ The following fields are optional:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)

  ```
      def create_agent_action_group(
              self, name, description, agent_id, agent_version, function_arn, api_schema
      ):
          """
          Creates an action group for an agent. An action group defines a set of actions that an
          agent should carry out for the customer.
  
          :param name: The name to give the action group.
          :param description: The description of the action group.
          :param agent_id: The unique identifier of the agent for which to create the action group.
          :param agent_version: The version of the agent for which to create the action group.
          :param function_arn: The ARN of the Lambda function containing the business logic that is
                               carried out upon invoking the action.
          :param api_schema: Contains the OpenAPI schema for the action group.
          :return: Details about the action group that was created.
          """
          try:
              response = self.client.create_agent_action_group(
                  actionGroupName=name,
                  description=description,
                  agentId=agent_id,
                  agentVersion=agent_version,
                  actionGroupExecutor={"lambda": function_arn},
                  apiSchema={"payload": api_schema},
              )
              agent_action_group = response["agentActionGroup"]
          except ClientError as e:
              logger.error(f"Error: Couldn't create agent action group. Here's why: {e}")
              raise
          else:
              return agent_action_group
  ```

  For more information, see [Hello Amazon Bedrock Agents](bedrock-agent_example_bedrock-agent_Hello_section.md).

------