

# Server-side tool use
<a name="tool-use-server-side"></a>

If you use the Responses API to invoke the model, then it can use server-side tool calling, in addition to the client-side tool calling we discussed before. Server-side tool calling is a mechanism where tools (APIs, functions, workflows) are executed in a trusted, backend environment, not on the client. This improves the security, reliability, and governance posture of the application. Before Amazon Bedrock executes the Lambda function which implements the tool use, it ensures that the Lambda function has the same IAM policy as that of the application that calls it. As Amazon Bedrock is driving the execution of the tools against, clients can focus on implementing their business logic, rather than adding tool functionality. Amazon Bedrock also supports the highest governance standards such as ISO, SOC, and HIPAA eligible. Customers can either submit their own custom Lambda function to run the tool or use existing pre-defined tools, such as notes and tasks. Server-side tools using the Responses API is available starting with OpenAI's GPT OSS 20B/120B models, with support for other models coming soon. You can use the Models API to discover available models that you can use with the Responses API. For more details on the Responses API, see [Generate responses using OpenAI APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html).

There are two types of tools you can use with Amazon Bedrock: Custom tools using Lambda, or pre-defined tools supported by Bedrock. In this section we will review how to create a custom Lambda tool with the Responses API. Let's discuss both in details.

**Custom tools using Lambda in Responses API**

By using a Lambda function as a custom tool in Bedrock, you can extend the capabilities of the agent by integrating custom AWS Lambda functions as tools. This enables you to create serverless, scalable tools that can be called by AI assistants and other applications through the Model Context Protocol (MCP). Here are the advantages of this feature:
+ Extend Functionality: Add custom business logic, API integrations, or data processing capabilities.
+ Run tools securely: Lambda allows tools to access resources inside a VPC without having to grant full VPC access.
+ Serverless Architecture: No infrastructure management, Lambda handles scaling automatically.
+ Cost Effective: Pay only for execution time, not idle resources.
+ Easy Integration: Lambda functions appear alongside built-in tools seamlessly.

To let a model in Amazon Bedrock use a tool to complete a response for a message, you send the message and the definitions for one or more tools to the model. Based on your application's prompt, if the model determines that one of the tools can help generate a response, it returns a request for Bedrock to use the tool and send the tool results back to the model. The model then uses the results to generate a response to the original message.

The following steps show how to use a tool with the [Responses API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html).

**How it works**

1. **Lambda function**: Create your Lambda function that implements the MCP protocol

1. **Tool Discovery**: Bedrock calls your Lambda function to discover available tools

1. **Tool Registration**: Your tools are registered with Bedrock

1. **Tool Execution**: When agent request your tool, Bedrock invokes your Lambda function

1. **Response Handling**: Results are returned to the agent through the standard interface

**Step 1: Define the Lambda function to get the most popular song**

Create a Lambda function that implements the MCP protocol. Here's a simple Python example:

```
import json

def lambda_handler(event, context):
    # Parse JSON-RPC request
    method = event.get('method')
    params = event.get('params', {})
    request_id = event.get('id')
    
    if method == 'tools/list':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "my_custom_tool",
                        "description": "My custom business logic tool",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "string",
                                    "description": "Input text to process"
                                }
                            },
                            "required": ["input"]
                        }
                    }
                ]
            }
        }
    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        if tool_name == 'my_custom_tool':
            # Your custom logic here
            result = f"Processed: {arguments.get('input', '')}"
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
    
    # Error response for unsupported methods
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }
```

**Step 2: Deploy the Lambda function**

Next, use your IAM role to deploy this Lambda function to get an ARN. You can read more on deploying a Lambda function [here](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html).

```
# Example using AWS CLI
aws lambda create-function \
  --function-name my-custom-tool \
  --runtime python3.14 \
  --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

Let's say that your ARN is: `arn:aws:lambda:us-west-2:123456789012:function:my-custom-tool`

**Step 3: Define the message and tool definition in your inference request**

To send the message and tool definition, you use the [Responses API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html) operations. Amazon Bedrock uses the [connectors and remote MCP servers functionality](https://platform.openai.com/docs/guides/tools-connectors-mcp) of the Responses API to provide tool-use capability. The definition of the tool is a JSON schema that you pass in the mcp request parameter to the Create operation. In the `connector_id` field in the Responses connectors API, you can pass in the Lambda ARN that you have created in the previous step. You do not need to provide authorization credentials since Bedrock uses the same IAM roles and policy that is used for your application that invokes the model. The following is an example schema for a tool that gets the most popular song played on a radio station.

```
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="oss-gpt-120b",
    tools=[
        {
            "type": "mcp",
            "server_label": "xamzn_arn",
            "connector_id": "arn:aws:lambda:us-west-2:123456789012:function:my-custom-tool",
            "require_approval": "never",
        },
    ],
    input="My custom prompt.",
)

print(resp.output_text)
```

**Step 4: Bedrock calls the tool and passes the response back to the model**

The ability to use the connector tool is available in the models that support the [Responses API](https://platform.openai.com/docs/api-reference/responses/create). Check which tools support your model [here](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html). When you're using tools using the Responses API, you only pay for [tokens](https://platform.openai.com/docs/pricing) used when importing tool definitions or making tool calls. There are no additional fees involved per tool call.

When you specify a Lambda function in the `tools` parameter, the API will attempt to get a list of tools from the server. If successful in retrieving the list of tools, a new `mcp_list_tools` output item will appear in the model response output. The `tools` property of this object will show the tools that were successfully imported. Once the model has access to these tool definitions, it may choose to call them depending on what's in the model's context. When the model decides to call a Lambda tool, the API will make a request to the Lambda function to call the tool and put its output into the model's context. You can read more on the list tools and calling tools in the [OpenAI documentation](https://platform.openai.com/docs/guides/tools-connectors-mcp?quickstart-panels=connector). Note that your Lambda function must have the same IAM roles and policy attached to it as that of the application calling the model in Bedrock, otherwise the Lambda function will fail. The following is the error definition.

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32000,
        "message": "Tool execution failed",
        "data": "Additional error details"
    }
}
```

**Using AWS provided tools in Responses API**

There are two AWS provided tools built into the `openai.gpt-oss-20b` and `openai.gpt-oss-120b` models: Note-taking functionality (notes tool) and Task management (tasks tool). These tools are automatically available — you do not need to define them in the `tools` parameter.

**Notes Tool Overview**

The `notes` tool allows the model to store notes within the same conversation session. This provides a simple memory mechanism for maintaining context across multiple interactions. Memory is scoped to the current conversation only.

When the model uses the notes tool, it emits an `mcp_call` output with `name` set to `"notes"`. The model determines the appropriate arguments based on your request.

You can use either natural language (e.g. "Remember that my favorite color is blue", "What did I tell you about my favorite color?", "Store the fact that I prefer morning meetings", "Recall what I said about meeting preferences") or you can use direct tool calls in your prompt ("Use the notes tool to store my email as john@example.com", "Check the notes for my email address").

**Tasks Tool Overview**

The `tasks` tool provides a stack for managing tasks within a conversation session. You can push tasks onto the stack and pop them off, making it useful for managing workflows, reminders, or hierarchical task management. Tasks persist throughout the entire conversation session. Memory is scoped to the current conversation only.

When the model uses the tasks tool, it emits an `mcp_call` output with `name` set to `"tasks"`. The model determines the appropriate arguments (such as `method`, `task.title`, and `task.description`) based on your request.

You can call the Tasks tool by either using natural language (e.g. "Add a task to review the budget", "Push a reminder to call the client", "What's the next task I need to do?", "Pop the most recent task", "Get the latest task from my stack") or you can call the tool directly in your prompt ("Use the tasks tool to push 'finish presentation'", "Pop a task from the stack", "Add 'schedule meeting' to my task list").

**Code example: Using the notes and tasks tools**

The notes and tasks tools are built into the `openai.gpt-oss-20b` and `openai.gpt-oss-120b` models. You do not need to define them explicitly in the `tools` parameter — simply reference them in your prompt:

```
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock-mantle.us-east-1.api.aws/v1"
)

# The notes tool is built-in — just ask the model to use it
resp = client.responses.create(
    model="openai.gpt-oss-120b",
    input="Use the notes tool to store that my preferred language is Python.",
)

print(resp.output)
# The model automatically calls the notes tool via mcp_call

# Use the tasks tool to push a task
resp = client.responses.create(
    model="openai.gpt-oss-120b",
    input="Use the tasks tool to push a task: review the API documentation",
)

print(resp.output)
```

## Server-side tool-use integration with AgentCore Gateway
<a name="tool-use-agentcore-gateway"></a>

Amazon Bedrock now supports [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) as a server-side tool calling integration type. This feature allows you to connect your models directly to AgentCore Gateway endpoints, enabling seamless access to tools managed through the gateway infrastructure.

The AgentCore Gateway integration follows the same pattern as Lambda function integration, with one key difference.

**Lambda Integration:**
+ Uses Lambda function ARNs
+ Directly invokes AWS Lambda functions

**AgentCore Gateway Integration:**
+ Uses AgentCore Gateway ARNs
+ Routes tool calls through the AgentCore Gateway infrastructure
+ Provides centralized tool management and discovery

### Configuration
<a name="agentcore-gateway-configuration"></a>

**Request Structure**

When configuring AgentCore Gateway as a tool source, use the following structure in your `tools` array in your Responses API request.

```
{
  "type":"mcp",
  "server_label":"agentcore_tools",
  "connector_id":"arn:aws:bedrock-agentcore:us-west-2:342789630635:gateway/agentcore-intro-gateway-v2-swvq44sovp",
  "server_description":"AgentCore Gateway providing custom tools",
  "require_approval":"never"
}
```

**Parameters**


| Parameter | Type | Required | Description | 
| --- | --- | --- | --- | 
| type | string | Yes | Must be set to mcp | 
| server\_label | string | Yes | A unique identifier for this tool connector within your request | 
| connector\_id | string | Yes | The ARN of your AgentCore Gateway | 
| server\_description | string | No | Human-readable description of the tools provided by this gateway | 
| require\_approval | string | Yes | Field has to be "never" | 

**Complete Request Example**

```
{
  "model":"openai.gpt-oss-120b",
  "stream":true,
  "background":false,
  "store":false,
  "tools": [
    {
      "type":"mcp",
      "server_label":"agentcore_tools",
      "connector_id":"arn:aws:bedrock-agentcore:us-west-2:342789630635:gateway/agentcore-intro-gateway-v2-swvq44sovp",
      "server_description":"AgentCore Gateway providing custom tools",
      "require_approval":"never"
    }
  ],
  "input": [
    {
      "type":"message",
      "role":"user",
      "content": [
        {
          "type":"input_text",
          "text":"What is the weather in Seattle?"
        }
      ]
    }
  ]
}
```

### Prerequisites
<a name="agentcore-gateway-prerequisites"></a>

Before using AgentCore Gateway integration, ensure you have:

1. **Created an AgentCore Gateway** with configured targets (Lambda functions, API Gateway stages, OpenAPI schemas, or MCP servers)

1. **Configured IAM permissions** allowing your Bedrock service role to invoke the gateway. Note that Bedrock only supports gateways with IAM authentication.

1. **Gateway ARN** in the correct format

### Benefits of AgentCore Gateway Integration
<a name="agentcore-gateway-benefits"></a>
+ **Centralized Tool Management**: Manage all your tools through a single gateway endpoint
+ **Tool Discovery**: Agents can dynamically discover available tools through the gateway
+ **Security**: Built-in authentication and authorization through IAM and gateway policies
+ **Observability**: Comprehensive monitoring and logging of tool invocations
+ **Flexibility**: Support for multiple target types (Lambda, API Gateway, OpenAPI, MCP servers)

### IAM Permissions
<a name="agentcore-gateway-iam"></a>

Your Bedrock execution role needs permission to invoke the AgentCore Gateway:

```
{
  "Version": "2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:InvokeGateway"
      ],
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:342789630635:gateway/agentcore-intro-gateway-v2-swvq44sovp"
    }
  ]
}
```

### Next Steps
<a name="agentcore-gateway-next-steps"></a>
+ Learn more about [creating AgentCore Gateways](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-create.html)
+ Explore [gateway target types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-targets.html)
+ Review [gateway security best practices](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-security.html)