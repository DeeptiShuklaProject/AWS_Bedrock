

# Enable user input in Amazon Bedrock
<a name="agents-enable-user-input"></a>

Configure your agent to ask the user for more information if the required information is not available to complete a task. If user input is enabled, the agent reprompts the user for information about the missing parameters. You can configure the agent by enabling user input in your agent's action group.

You can enable user input in the Amazon Bedrock console when you [create](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-create.html) or [modify](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-manage.html#agents-edit) your agent. If you are using API or SDKs, you can enable user input when you [create](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [update](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) action group.

To learn how to enable user input in Amazon Bedrock, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To enable user input for your agent**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent Builder**

1. Go to **Additional settings** and expand the section.

1. For **User input**, select **Enabled**.  
![Agent user input configuration for requesting additional information.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/agents/agents-user-input.png)

1. Make sure to first **Save** and then **Prepare** to apply the changes you have made to the agent before testing it.

------
#### [ API ]

To enable user input for your agent, send an [CreateActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the following fields:


****  

| Field | Short description | 
| --- | --- | 
| actionGroupName | Name of the action group | 
| parentActionGroupSignature | Specify AMAZON.UserInput to allow the agent to request information from the user | 
| actionGroupState | Specify ENABLED to allow the agent to request information from user | 

The following shows the general format of the required fields for enabling user input with an [CreateActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) request.

```
CreateAgentActionGroup:
{
  "actionGroupName": "AskUserAction",
  "parentActionGroupSignature": "AMAZON.UserInput",
  "actionGroupState": "ENABLED"
}
```

------