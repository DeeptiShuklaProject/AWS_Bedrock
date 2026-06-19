

# Disable user input in Amazon Bedrock
<a name="agents-disable-user-input"></a>

If you disable user input, the agent doesn't request the user for additional details. if it needs to invoke an API in an action group, but doesn't have enough information to complete the API request. Instead, the model within the agent will use the default values and make a best guess at invoking the appropriate function or the method. This might cause agent to hallucinate on the function call prediction. 

You can disable user input in Amazon Bedrock at any time.

To learn how to disable user input, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To disable user input,**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. Choose **Edit in Agent builder**.

1. Expand **Additional setting** section, choose **Disabled** for **User input**.

1. Select **Prepare** at the top of the page. And then select **Save** to save the changes to your agent.

------
#### [ API ]

To disable user input, send an [UpdateAgentActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the following fields:


****  

| Field | Short description | 
| --- | --- | 
| actionGroupName | Name of the action group | 
| parentActionGroupSignature | Specify AMAZON.UserInput to disable the user input for agent | 
| actionGroupState | Specify DISABLED to disable user input for the agent | 

The following example shows the general format for specifying the required fields to disable user input.

```
CreateAgentActionGroup:
{
  "actionGroupName": "AskUserAction",
  "parentActionGroupSignature": "AMAZON.UserInput",
  "actionGroupState": "DISABLED"
}
```

------

After you've disabled user input for your agent, make sure to send a [PrepareAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_PrepareAgent.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).