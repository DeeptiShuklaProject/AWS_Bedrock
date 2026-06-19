

# Enable code interpretation in Amazon Bedrock
<a name="agents-enable-code-interpretation"></a>

You can enable code interpretation in the Amazon Bedrock console when you [create](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-create.html) or [update](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-manage.html#agents-edit) your agent. If you are using API or SDKs, you can enable code interpretation when you [create](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) or [update](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_UpdateAgentActionGroup.html) action group.

To learn how to enable code interpretation in Amazon Bedrock, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To enable code interpretation for your agent**

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent Builder**

1. Go to **Additional settings** and expand the section.

1. For **Code Interpreter**, select **Enable**.

1. Make sure to first **Save** and then **Prepare** to apply the changes you have made to the agent before testing it.

------
#### [ API ]

To enable code interpretation for your agent, send an [CreateActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the following fields:


****  

| Field | Short description | 
| --- | --- | 
| actionGroupName | Name of the action group | 
| parentActionGroupSignature | Specify AMAZON.CodeInterpreter to allow the agent to generate and test code | 
| actionGroupState | Specify ENABLED to allow the agent to invoke code interpretation | 

The following shows the general format of the required fields for enabling code interpretation with an [CreateActionGroup](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_CreateAgentActionGroup.html) request.

```
CreateAgentActionGroup:
{
  "actionGroupName": "CodeInterpreterAction",
  "parentActionGroupSignature": "AMAZON.CodeInterpreter",
  "actionGroupState": "ENABLED"
}
```

------