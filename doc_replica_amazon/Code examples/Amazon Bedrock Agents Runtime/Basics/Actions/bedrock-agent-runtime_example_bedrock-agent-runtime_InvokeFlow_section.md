

# Use `InvokeFlow` with an AWS SDK
<a name="bedrock-agent-runtime_example_bedrock-agent-runtime_InvokeFlow_section"></a>

The following code examples show how to use `InvokeFlow`.

Action examples are code excerpts from larger programs and must be run in context. You can see this action in context in the following code examples: 
+  [Learn the basics](bedrock-agent-runtime_example_bedrock-agent-runtime_Scenario_ConverseWithFlow_section.md) 
+  [Create and invoke a flow](bedrock-agent-runtime_example_bedrock-agent_GettingStartedWithBedrockFlows_section.md) 

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascriptv3/example_code/bedrock-agent-runtime#code-examples). 

```
import { fileURLToPath } from "node:url";

import {
  BedrockAgentRuntimeClient,
  InvokeFlowCommand,
} from "@aws-sdk/client-bedrock-agent-runtime";

/**
 * Invokes an alias of a flow to run the inputs that you specify and return
 * the output of each node as a stream.
 *
 * @param {{
 *  flowIdentifier: string,
 *  flowAliasIdentifier: string,
 *  prompt?: string,
 *  region?: string
 * }} options
 * @returns {Promise<import("@aws-sdk/client-bedrock-agent").FlowNodeOutput>} An object containing information about the output from flow invocation.
 */
export const invokeBedrockFlow = async ({
  flowIdentifier,
  flowAliasIdentifier,
  prompt = "Hi, how are you?",
  region = "us-east-1",
}) => {
  const client = new BedrockAgentRuntimeClient({ region });

  const command = new InvokeFlowCommand({
    flowIdentifier,
    flowAliasIdentifier,
    inputs: [
      {
        content: {
          document: prompt,
        },
        nodeName: "FlowInputNode",
        nodeOutputName: "document",
      },
    ],
  });

  let flowResponse = {};
  const response = await client.send(command);

  for await (const chunkEvent of response.responseStream) {
    const { flowOutputEvent, flowCompletionEvent } = chunkEvent;

    if (flowOutputEvent) {
      flowResponse = { ...flowResponse, ...flowOutputEvent };
      console.log("Flow output event:", flowOutputEvent);
    } else if (flowCompletionEvent) {
      flowResponse = { ...flowResponse, ...flowCompletionEvent };
      console.log("Flow completion event:", flowCompletionEvent);
    }
  }

  return flowResponse;
};

// Call function if run directly
import { parseArgs } from "node:util";
import {
  isMain,
  validateArgs,
} from "@aws-doc-sdk-examples/lib/utils/util-node.js";

const loadArgs = () => {
  const options = {
    flowIdentifier: {
      type: "string",
      required: true,
    },
    flowAliasIdentifier: {
      type: "string",
      required: true,
    },
    prompt: {
      type: "string",
    },
    region: {
      type: "string",
    },
  };
  const results = parseArgs({ options });
  const { errors } = validateArgs({ options }, results);
  return { errors, results };
};

if (isMain(import.meta.url)) {
  const { errors, results } = loadArgs();
  if (!errors) {
    invokeBedrockFlow(results.values);
  } else {
    console.error(errors.join("\n"));
  }
}
```
+  For API details, see [InvokeFlow](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock-agent-runtime/command/InvokeFlowCommand) in *AWS SDK for JavaScript API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-agent-runtime#code-examples). 
Invoke a flow.  

```
    def invoke_flow(self, flow_id, flow_alias_id, input_data, execution_id):
        """
        Invoke an Amazon Bedrock flow and handle the response stream.

        Args:
            param flow_id: The ID of the flow to invoke.
            param flow_alias_id: The alias ID of the flow.
            param input_data: Input data for the flow.
            param execution_id: Execution ID for continuing a flow. Use the value None on first run.

        Return: Response from the flow.
        """
        try:
      
            request_params = None

            if execution_id is None:
                # Don't pass execution ID for first run.
                request_params = {
                    "flowIdentifier": flow_id,
                    "flowAliasIdentifier": flow_alias_id,
                    "inputs": input_data,
                    "enableTrace": True
                }
            else:
                request_params = {
                    "flowIdentifier": flow_id,
                    "flowAliasIdentifier": flow_alias_id,
                    "executionId": execution_id,
                    "inputs": input_data,
                    "enableTrace": True
                }

            response = self.agents_runtime_client.invoke_flow(**request_params)

            if "executionId" not in request_params:
                execution_id = response['executionId']

            result = ""

            # Get the streaming response
            for event in response['responseStream']:
                result = result + str(event) + '\n'
            print(result)

        except ClientError as e:
            logger.error("Couldn't invoke flow %s.", {e})
            raise

        return result
```
+  For API details, see [InvokeFlow](https://docs.aws.amazon.com/goto/boto3/bedrock-agent-runtime-2023-12-12/InvokeFlow) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.