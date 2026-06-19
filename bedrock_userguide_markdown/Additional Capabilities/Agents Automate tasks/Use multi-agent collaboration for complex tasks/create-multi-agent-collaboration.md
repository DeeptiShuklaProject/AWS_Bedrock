

# Create multi-agent collaboration
<a name="create-multi-agent-collaboration"></a>

Creating a multi-agent collaboration comprises of the following steps:

1. Create and deploy collaborator agents. Make sure to configure each collaborator agent to implement a specific task within the multi-agent collaboration work flow. 

1. Create a new supervisor agent or assign an existing agent the role of the supervisor. When you create a new supervisor agent or identify an existing agent as a supervisor agent, you can also specify how you want the supervisor agent to handle information across multiple collaborator agents.

   You can assign the supervisor agent the task of coordinating responses from the collaborator agents or you can assign the supervisor agent the task of routing information to the appropriate collaborator agent to send the final response. Assigning the supervisor agent the task of routing information reduces the latency. 

1. Associate the alias version of the collaborator agents with the supervisor agent.
**Note**  
You can associate a maximum of 10 collaborator agents with a supervisor agent at this time.

1. Prepare and test your multi-agent collaboration team.

1. Deploy and invoke supervisor agent.

You can create multi-agent collaboration in the Amazon Bedrock console, using the APIs, using the AWS CLI, or by using the AWS SDK. To learn how to create a multi-agent collaboration, choose the tab for your preferred method, and then follow the steps:.

------
#### [ Console ]

**Step 1: Create collaborator agents**
+ Follow instructions to [Create and configure an agent](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-create.html). Make sure to configure each collaborator agent to perform a specific task.

**Step 2: Create a new supervisor agent or assign supervisor role to an existing agent**

1. If you are creating a new supervisor agent follow instructions to [Create and configure agent manually](agents-create.md) and then continue with the next step.

   If you already have an agent configured and want to assign supervisor role to the agent, continue with the next step.

1. If you're not already in the agent builder, do the following:

   1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

   1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

   1. Choose **Edit in Agent builder**.

   1. In the **Agent builder**, scroll down to the **Multi-agent collaboration** section and choose **Edit**.

1. In the **Multi-agent collaboration** page, in the **Collaboration status** section, turn on **Multi-agent collaboration**. This will identify the agent as a supervisor agent.

1. In the **Collaboration configuration** section, choose how you want the supervisor agent to handle information across multiple collaborator agents to coordinate a final response.

   1. If you want supervisor agent to coordinate responses from the collaborator agents, select **Supervisor**.

   1. If you want supervisor agent to route information to the appropriate collaborator agent to send the final response, select **Supervisor with routing**.

   1. Continue with the next steps to add collaborator agents.

**Step 3: Add collaborator agents**

1. Expand the **Agent collaborator** section and provide details of the collaborator agent you created for multi-agent collaboration.

   1. For **Collaborator agent**, select a collaborator agent and **Agent alias**from the drop-down. You can choose **View** to view the details of the collaborator agent.

   1. For **Collaborator name**, enter an alternate name for your collaborator agent. This name will not replace the original name of this agent.

   1. In **Collaboration instructions**, enter the details for when this collaborator should be used by the supervisor agent. 

   1. (Optional) Turn on **Enable conversation history** if you want the supervisor agent to share context from previous conversations with this collaborator agent. If this is turned on, the supervisor will include the full history of the current session, including the user input text and the supervisor agent response from each turn of the conversation.

1. Choose **Add collaborator** to add this collaborator agent in your multi-agent-collaboration team. To add more collaborator agents, repeat step 1 until you've added all your collaborator agents. 

1. When you've finished adding collaborator agents, select one of the following options:
   + To stay in the **Multi-agent collaboration**, choose **Save** and continue with the next step to prepare and test your multi-agents collaboration team.
   + To return to the **Agent Details** page, choose **Save and exit**.

**Step 4: Prepare and test a multi-agent collaboration**
+ Follow instructions to [prepare and test](agents-test.md) your multi-agent collaboration team. 

**Step 5: Deploy a multi-agent collaboration**
+ [Deploy](agents-deploy.md) multi-agent collaboration by setting up the supervisor agent to make an `InvokeAgent` request.

------
#### [ API ]

Complete the following steps to create a multi-agent collaboration team,

**Step 1: Create collaborator agents**
+ Follow instructions to [Create and configure an agent](https://docs.aws.amazon.com//bedrock/latest/userguide/agents-create.html). Make sure to configure each collaborator agent to perform a specific task.

**Step 2: Create a new supervisor agent or assign supervisor role to an existing agent**
+ To create a new supervisor agent, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

  To assign a supervisor role to an existing agent, send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Because all fields will be overwritten, include both fields that you want to update as well as fields that you want to keep the same.

  You must minimally include the following fields:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/create-multi-agent-collaboration.html)

  The following fields are optional:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/create-multi-agent-collaboration.html)

  The response returns an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object that contains details about your newly created supervisor agent. If your agent fails to be created, the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object in the response returns a list of `failureReasons` and a list of `recommendedActions` for you to troubleshoot.

**Step 3: Add collaborator agents**
+ To associate collaborator agents with the supervisor agent, send a `AssociateAgentCollaborator` request (see link for request and response formats and field details) with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

  You must minimally include the following fields:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/create-multi-agent-collaboration.html)

**Step 4: Prepare and test your multi-agent collaborator team**
+ Follow instructions to [prepare and test](agents-test.md) your multi-agent collaboration team. 

**Step 4: Deploy your multi-agent collaboration team**
+ [Deploy](agents-deploy.md) your multi-agent collaboration team by setting up your supervisor agent to make an `InvokeAgent` request.

------