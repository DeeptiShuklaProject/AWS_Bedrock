

# Optimize performance for Amazon Bedrock agents using a single knowledge base
<a name="agents-optimize-performance"></a>

Amazon Bedrock Agents offers options to choose different flows that can optimize on latency for simpler use cases in which agents have a single knowledge base. To ensure that your agent is able to take advantage of this optimization, check that the following conditions apply to the relevant version of your agent:
+ Your agent contains only one knowledge base.
+ Your agent contains no action groups or they are all disabled.
+ Your agent doesn't request more information from the user if it doesn't have enough information.
+ Your agent is using the default orchestration prompt template.

When these conditions are met, the service reduces the number of LLM calls needed to process a request. If you override the default orchestration prompt template, the agent uses the standard orchestration flow instead, which may require additional LLM calls and increase latency.

To learn how to check for these conditions, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

1. In the **Agent overview** section, check that the **User input** field is **DISABLED**.

1. If you're checking if the optimization is being applied to the working draft of the agent, select the **Working draft** in the **Working draft** section. If you're checking if the optimization is being applied to a version of the agent, select the version in the **Versions** section.

1. Check that the **Knowledge bases** section contains only one knowledge base. If there's more than one knowledge base, disable all of them except for one. To learn how to disable knowledge bases, see [Disassociate a knowledge base from an agent](agents-kb-delete.md).

1. Check that the **Action groups** section contains no action groups. If there are action groups, disable all of them. To learn how to disable action groups, see [Modify an action group](agents-action-edit.md).

1. In the **Advanced prompts** section, check that the **Orchestration** field value is **Default**. If it's **Overridden**, choose **Edit** (if you're viewing a version of your agent, you must first navigate to the working draft) and do the following:

   1. In the **Advanced prompts** section, select the **Orchestration** tab.

   1. If you revert the template to the default settings, your custom prompt template will be deleted. Make sure to save your template if you need it later.

   1. Clear **Override orchestration template defaults**. Confirm the message that appears.

1. To apply any changes you've made, select **Prepare** at the top of the **Agent details** page or in the test window. Then, test the agent's optimized performance by submitting a message in the test window.

1. (Optional) If necessary, create a new version of your agent by following the steps at [Deploy and use an Amazon Bedrock agent in your application](agents-deploy.md).

------
#### [ API ]

1. Send a [ListAgentKnowledgeBases](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentKnowledgeBases.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ID of your agent. For the `agentVersion`, use `DRAFT` for the working draft or specify the relevant version. In the response, check that `agentKnowledgeBaseSummaries` contains only one object (corresponding to one knowledge base). If there's more than one knowledge base, disable all of them except for one. To learn how to disable knowledge bases, see [Disassociate a knowledge base from an agent](agents-kb-delete.md).

1. Send a [ListAgentActionGroups](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListAgentActionGroups.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ID of your agent. For the `agentVersion`, use `DRAFT` for the working draft or specify the relevant version. In the response, check that the `actionGroupSummaries` list is empty. If there are action groups, disable all of them. To learn how to disable action groups, see [Modify an action group](agents-action-edit.md).

1. Send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ID of your agent. In the response, within the `promptConfigurations` list in the `promptOverrideConfiguration` field, look for the [PromptConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptConfiguration.html) object whose `promptType` value is `ORCHESTRATION`. If the `promptCreationMode` value is `DEFAULT`, you don't have to do anything. If it's `OVERRIDDEN`, do the following to revert the template to the default settings:

   1. If you revert the template to the default settings, your custom prompt template will be deleted. Make sure to save your template from the `basePromptTemplate` field if you need it later.

   1. Send an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). For the [PromptConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptConfiguration.html) object corresponding to the orchestration template, set the value of `promptCreationMode` to `DEFAULT`.

1. To apply any changes you've made, send a [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PrepareAgent.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). Then, test the agent's optimized performance by submitting an [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) request with an [Agents for Amazon Bedrock runtime endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-rt), using the `TSTALIASID` alias of the agent.

1. (Optional) If necessary, create a new version of your agent by following the steps at [Deploy and use an Amazon Bedrock agent in your application](agents-deploy.md).

------