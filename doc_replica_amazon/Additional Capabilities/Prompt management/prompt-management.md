

# Construct and store reusable prompts with Prompt management in Amazon Bedrock
<a name="prompt-management"></a>

Amazon Bedrock provides you the ability to create, edit, and save your own prompts using Prompt management so that you can save time by applying the same prompt to different workflows. When you create a prompt, you can select a model to run inference on it and modify the inference parameters to use. You can include variables in the prompt so that you can adjust the prompt for different use cases.

When you test your prompt, you have the option of comparing different variants of the prompt and choosing the variant that yields outputs that are best-suited for your use case. While iterating on your prompt, you can save versions of it. You integrate a prompt into your application with the help of [Amazon Bedrock Flows](flows.md).

The following is the general workflow for using Prompt management:

1. Create a prompt in Prompt management that you want to reuse across different use cases. Include variables to provide flexibility in the model prompt.

1. Choose a model, inference profile, or agent to run inference on the prompt and modify the inference configurations as necessary.

1. Fill in test values for the variables and run the prompt. You can create variants of your prompt and compare the outputs of different variants to choose the best one for your use case.

1. Integrate the prompt into your application in one of the following ways:
   + Specify the prompt when [running model inference](inference.md).
   + Add a prompt node to a [flow](flows.md) and specify the prompt.

**Topics**
+ [Key definitions](#prompt-management-definitions)
+ [Supported Regions and models for Prompt management](prompt-management-supported.md)
+ [Prerequisites for prompt management](prompt-management-prereq.md)
+ [Create a prompt using Prompt management](prompt-management-create.md)
+ [View information about prompts using Prompt management](prompt-management-view.md)
+ [Modify a prompt using Prompt management](prompt-management-modify.md)
+ [Test a prompt using Prompt management](prompt-management-test.md)
+ [Optimize a prompt](prompt-management-optimize.md)
+ [Deploy a prompt to your application using versions in Prompt management](prompt-management-deploy.md)
+ [Delete a prompt in Prompt management](prompt-management-delete.md)
+ [Run Prompt management code samples](prompt-management-code-ex.md)

## Key definitions
<a name="prompt-management-definitions"></a>

The following list introduces you to the basic concepts of Prompt management:
+ **Prompt** – An input provided to a model to guide it to generate an appropriate response or output.
+ **Variable** – A placeholder that you can include in the prompt. You can include values for each variable when testing the prompt or when you invoke the model at runtime.
+ **Prompt variant** – An alternative configuration of the prompt, including its message or the model or inference configurations used. You can create different variants of a prompt, test them, and save the variant that you want to keep.
+ **Prompt builder** – A tool in the Amazon Bedrock console that lets you create, edit, and test prompts and their variants in a visual interface.