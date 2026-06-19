

# Configure advanced prompts
<a name="configure-advanced-prompts"></a>

You can configure advanced prompts in either the AWS Management Console or through the API.

------
#### [ Console ]

In the console, you can configure advanced prompts after you have created the agent. You configure them while editing the agent.

**To view or edit advanced prompts for your agent**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. In the left navigation pane, choose **Agents**. Then choose an agent in the **Agents** section.

1. On the agent details page, in the **Working draft** section, select **Working draft**.

1. On the **Working draft** page, in the **Orchestration strategy** section, choose **Edit**.

1. On the **Orchestration strategy** page, in the **Orchestration strategy details** section, make sure the **Default orchestration** is selected and then choose the tab corresponding to the step of the agent sequence that you want to edit.

1. To enable editing of the template, turn on **Override template defaults**. In the **Override template defaults** dialog box, choose **Confirm**.
**Warning**  
If you turn off **Override template defaults** or change the model, the default Amazon Bedrock template is used and your template will be immediately deleted. To confirm, enter **confirm** in the text box to confirm the message that appears.

1. To allow the agent to use the template when generating responses, turn on **Activate template**. If this configuration is turned off, the agent doesn't use the template.

1. To modify the example prompt template, use the **Prompt template editor**.

1. In **Configurations**, you can modify inference parameters for the prompt. For definitions of parameters and more information about parameters for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md).

1. (Optional) To use a Lambda function that you have defined to parse the raw foundation model output, perform the following actions:
**Note**  
One Lambda function is used for all the prompt templates.

   1. In the **Configurations** section, select **Use Lambda function for parsing**. If you clear this setting, your agent will use the default parser for the prompt.

   1. For the **Parser Lambda function**, select a Lambda function from the dropdown menu.
**Note**  
You must attach permissions for your agent so that it can access the Lambda function. For more information, see [Resource-based policy to allow Amazon Bedrock to invoke an action group Lambda function](agents-permissions.md#agents-permissions-lambda).

1. To save your settings, choose one of the following options:

   1. To remain in the same window so that you can dynamically update the prompt settings while testing your updated agent, choose **Save**.

   1. To save your settings and return to the **Working draft** page, choose **Save and exit**.

1. To test the updated settings, choose **Prepare** in the **Test** window.

![Setting up advanced prompts in the console.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/agents/advanced-prompts.png)


------
#### [ API ]

To configure advanced prompts by using the API operations, you send an [UpdateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) call and modify the following `promptOverrideConfiguration` object.

```
"promptOverrideConfiguration": { 
    "overrideLambda": "string",
    "promptConfigurations": [ 
        { 
            "basePromptTemplate": "string",
            "inferenceConfiguration": { 
                "maximumLength": int,
                "stopSequences": [ "string" ],
                "temperature": float,
                "topK": float,
                "topP": float
            },
            "parserMode": "DEFAULT | OVERRIDDEN",
            "promptCreationMode": "DEFAULT | OVERRIDDEN",
            "promptState": "ENABLED | DISABLED",
            "promptType": "PRE_PROCESSING | ORCHESTRATION | KNOWLEDGE_BASE_RESPONSE_GENERATION | POST_PROCESSING | MEMORY_SUMMARIZATION"
        }
    ]
}
```

1. In the `promptConfigurations` list, include a `promptConfiguration` object for each prompt template that you want to edit.

1. Specify the prompt to modify in the `promptType` field.

1. Modify the prompt template through the following steps:

   1. Specify the `basePromptTemplate` fields with your prompt template.

   1. Include inference parameters in the `inferenceConfiguration` objects. For more information about inference configurations, see [Inference request parameters and response fields for foundation models](model-parameters.md).

1. To enable the prompt template, set the `promptCreationMode` to `OVERRIDDEN`.

1. To allow or prevent the agent from performing the step in the `promptType` field, modify the `promptState` value. This setting can be useful for troubleshooting the agent's behavior.
   + If you set `promptState` to `DISABLED` for the `PRE_PROCESSING`, `KNOWLEDGE_BASE_RESPONSE_GENERATION`, or `POST_PROCESSING` steps, the agent skips that step.
   + If you set `promptState` to `DISABLED` for the `ORCHESTRATION` step, the agent sends only the user input to the foundation model in orchestration. In addition, the agent returns the response as is without orchestrating calls between API operations and knowledge bases.
   + By default, the `POST_PROCESSING` step is `DISABLED`. By default, the `PRE_PROCESSING`, `ORCHESTRATION`, and `KNOWLEDGE_BASE_RESPONSE_GENERATION` steps are `ENABLED`.
   + By default, the `MEMORY_SUMMARIZATION` step is `ENABLED` if Memory is enabled and the `MEMORY_SUMMARIZATION` step is `DISABLED` if Memory is disabled.

1. To use a Lambda function that you have defined to parse the raw foundation model output, perform the following steps:

   1. For each prompt template that you want to enable the Lambda function for, set `parserMode` to `OVERRIDDEN`.

   1. Specify the Amazon Resource Name (ARN) of the Lambda function in the `overrideLambda` field in the `promptOverrideConfiguration` object.

------