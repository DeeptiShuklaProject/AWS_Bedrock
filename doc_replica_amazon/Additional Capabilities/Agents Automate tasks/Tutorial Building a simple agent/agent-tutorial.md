

# Tutorial: Building a simple Amazon Bedrock agent
<a name="agent-tutorial"></a>

This tutorial guides you through creating and configuring a simple Amazon Bedrock agent using the AWS Management Console. You'll learn how to create an agent that can respond to user queries about the current date and time by invoking a Lambda function.

In this tutorial, you will:

1. Create a Lambda function — Build a Python function that returns the current date and time when invoked by your agent.

1. Create an Amazon Bedrock agent — Set up an agent in the Amazon Bedrock console and configure it with instructions to handle date and time queries.

1. Test the agent — Use the built-in testing interface to verify your agent can correctly respond to date and time requests.

1. Deploy the agent with an alias — Create a version of your agent and deploy it with an alias to make it available for use.

1. Call the agent from Python code — Learn how to programmatically interact with your agent using the AWS SDK for Python (Boto). 

1. Clean up resources — Remove the AWS resources created during this tutorial to avoid incurring unnecessary charges.

By the end of this tutorial, you'll have a working Amazon Bedrock agent that can understand natural language requests for date and time information and respond with accurate data from your Lambda function.

This tutorial is based on the agent code example in the AWS documentation [GitHub repository](https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/bedrock-agent/scenario_get_started_with_agents.py). 

**Topics**
+ [Prerequisites](agent-tutorial-prereq.md)
+ [Step 1: Create a Lambda function](agent-tutorial-step1.md)
+ [Step 2: Create an Amazon Bedrock agent](agent-tutorial-step2.md)
+ [Step 3: Test the agent](agent-tutorial-step3.md)
+ [Step 4: Deploy the agent with an alias](agent-tutorial-step4.md)
+ [Step 5: Call the agent from Python code](agent-tutorial-step5.md)
+ [Step 6: Clean up resources](agent-tutorial-step6.md)
+ [Additional resources](agent-tutorial-resources.md)