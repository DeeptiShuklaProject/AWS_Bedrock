

# Build and orchestrate generative AI applications with Amazon Bedrock and Step Functions
<a name="bedrock-agent-runtime_example_cross_ServerlessPromptChaining_section"></a>

The following code example shows how to build and orchestrate generative AI applications with Amazon Bedrock and Step Functions.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 The Amazon Bedrock Serverless Prompt Chaining scenario demonstrates how [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html), [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html), and [https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) can be used to build and orchestrate complex, serverless, and highly scalable generative AI applications. It contains the following working examples:   
+  Write an analysis of a given novel for a literature blog. This example illustrates a simple, sequential chain of prompts. 
+  Generate a short story about a given topic. This example illustrates how the AI can iteratively process a list of items that it previously generated. 
+  Create an itinerary for a weekend vacation to a given destination. This example illustrates how to parallelize multiple distinct prompts. 
+  Pitch movie ideas to a human user acting as a movie producer. This example illustrates how to parallelize the same prompt with different inference parameters, how to backtrack to a previous step in the chain, and how to include human input as part of the workflow. 
+  Plan a meal based on ingredients the user has at hand. This example illustrates how prompt chains can incorporate two distinct AI conversations, with two AI personas engaging in a debate with each other to improve the final outcome. 
+  Find and summarize today's highest trending GitHub repository. This example illustrates chaining multiple AI agents that interact with external APIs. 
 For complete source code and instructions to set up and run, see the full project on [GitHub](https://github.com/aws-samples/amazon-bedrock-serverless-prompt-chaining).   

**Services used in this example**
+ Amazon Bedrock
+ Amazon Bedrock Runtime
+ Amazon Bedrock Agents
+ Amazon Bedrock Agents Runtime
+ Step Functions

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.