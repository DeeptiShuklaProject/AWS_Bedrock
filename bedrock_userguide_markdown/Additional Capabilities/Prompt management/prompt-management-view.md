

# View information about prompts using Prompt management
<a name="prompt-management-view"></a>

To learn how to view information about prompts using Prompt management, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a prompt**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Prompt management** from the left navigation pane. Then, choose a prompt in the **Prompts** section.

1. The **Prompt details** page includes the following sections:
   + **Overview** – Contains general information about the prompt and when it was created and last updated.
   + **Prompt draft** – Contains the prompt message and configurations for the latest saved draft version of the prompt.
   + **Prompt versions** – A list of all versions of the prompt that have been created. For more information about prompt versions, see [Deploy a prompt to your application using versions in Prompt management](prompt-management-deploy.md).

------
#### [ API ]

To get information about a prompt, send a [GetPrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetPrompt.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt) and specify the ARN or ID of the prompt as the `promptIdentifier`. To get information about a specific version of the prompt, specify `DRAFT` or the version number in the `promptVersion` field.

To list information about your agents, send a [ListPrompts](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListPrompts.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

------