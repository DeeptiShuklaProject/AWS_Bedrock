

# Run Prompt management code samples
<a name="prompt-management-code-ex"></a>

To try out some code samples for Prompt management, choose the tab for your preferred method, and then follow the steps: The following code samples assume that you've set up your credentials to use the AWS API. If you haven't, refer to [Get started with the API](getting-started-api.md).

------
#### [ Python ]

1. Run the following code snippet to load the AWS SDK for Python (Boto3), create a client, and create a prompt that creates a music playlist using two variables (`genre` and `number`) by making a [CreatePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreatePrompt.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Create a prompt in Prompt management
   import boto3
   
   # Create an Amazon Bedrock Agents client
   client = boto3.client(service_name="bedrock-agent")
   
   # Create the prompt
   response = client.create_prompt(
       name="MakePlaylist",
       description="My first prompt.",
       variants=[
           { 
               "name": "Variant1",
               "modelId": "amazon.titan-text-express-v1",
               "templateType": "TEXT",
               "inferenceConfiguration": {
                   "text": {
                       "temperature": 0.8
                   }
               },
               "templateConfiguration": { 
                   "text": {
                       "text": "Make me a {{{{genre}}}} playlist consisting of the following number of songs: {{{{number}}}}."
                   }
               }
         }
       ]
   )
                           
   prompt_id = response.get("id")
   ```

1. Run the following code snippet to see the prompt that you just created (alongside any other prompts in your account) to make a [ListPrompts](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListPrompts.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # List prompts that you've created
   client.list_prompts()
   ```

1. You should see the ID of the prompt you created in the `id` field in the object in the `promptSummaries` field. Run the following code snippet to show information for the prompt that you created by making a [GetPrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetPrompt.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Get information about the prompt that you created
   client.get_prompt(promptIdentifier=prompt_id)
   ```

1. Create a version of the prompt and get its ID by running the following code snippet to make a [CreatePromptVersion](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreatePromptVersion.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Create a version of the prompt that you created
   response = client.create_prompt_version(promptIdentifier=prompt_id)
                           
   prompt_version = response.get("version")
   prompt_version_arn = response.get("arn")
   ```

1. View information about the prompt version that you just created, alongside information about the draft version, by running the following code snippet to make a [ListPrompts](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListPrompts.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # List versions of the prompt that you just created
   client.list_prompts(promptIdentifier=prompt_id)
   ```

1. View information for the prompt version that you just created by running the following code snippet to make a [GetPrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetPrompt.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Get information about the prompt version that you created
   client.get_prompt(
       promptIdentifier=prompt_id, 
       promptVersion=prompt_version
   )
   ```

1. Test the prompt by adding it to a flow by following the steps at [Run Amazon Bedrock Flows code samples](flows-code-ex.md). In the first step when you create the flow, run the following code snippet instead to use the prompt that you created instead of defining an inline prompt in the flow (replace the ARN of the prompt version in the `promptARN` field with the ARN of the version of the prompt that you created):

   ```
   # Import Python SDK and create client
   import boto3
   
   client = boto3.client(service_name='bedrock-agent')
   
   FLOWS_SERVICE_ROLE = "arn:aws:iam::123456789012:role/MyPromptFlowsRole" # Flows service role that you created. For more information, see https://docs.aws.amazon.com/bedrock/latest/userguide/flows-permissions.html
   PROMPT_ARN = prompt_version_arn # ARN of the prompt that you created, retrieved programatically during creation.
   
   # Define each node
   
   # The input node validates that the content of the InvokeFlow request is a JSON object.
   input_node = {
       "type": "Input",
       "name": "FlowInput",
       "outputs": [
           {
               "name": "document",
               "type": "Object"
           }
       ]
   }
   
   # This prompt node contains a prompt that you defined in Prompt management.
   # It validates that the input is a JSON object that minimally contains the fields "genre" and "number", which it will map to the prompt variables.
   # The output must be named "modelCompletion" and be of the type "String".
   prompt_node = {
       "type": "Prompt",
       "name": "MakePlaylist",
       "configuration": {
           "prompt": {
               "sourceConfiguration": {
                   "resource": {
                       "promptArn": ""
                   }
               }
           }
       },
       "inputs": [
           {
               "name": "genre",
               "type": "String",
               "expression": "$.data.genre"
           },
           {
               "name": "number",
               "type": "Number",
               "expression": "$.data.number"
           }
       ],
       "outputs": [
           {
               "name": "modelCompletion",
               "type": "String"
           }
       ]
   }
   
   # The output node validates that the output from the last node is a string and returns it as is. The name must be "document".
   output_node = {
       "type": "Output",
       "name": "FlowOutput",
       "inputs": [
           {
               "name": "document",
               "type": "String",
               "expression": "$.data"
           }
       ]
   }
   
   # Create connections between the nodes
   connections = []
   
   #   First, create connections between the output of the flow input node and each input of the prompt node
   for input in prompt_node["inputs"]:
       connections.append(
           {
               "name": "_".join([input_node["name"], prompt_node["name"], input["name"]]),
               "source": input_node["name"],
               "target": prompt_node["name"],
               "type": "Data",
               "configuration": {
                   "data": {
                       "sourceOutput": input_node["outputs"][0]["name"],
                       "targetInput": input["name"]
                   }
               }
           }
       )
   
   # Then, create a connection between the output of the prompt node and the input of the flow output node
   connections.append(
       {
           "name": "_".join([prompt_node["name"], output_node["name"]]),
           "source": prompt_node["name"],
           "target": output_node["name"],
           "type": "Data",
           "configuration": {
               "data": {
                   "sourceOutput": prompt_node["outputs"][0]["name"],
                   "targetInput": output_node["inputs"][0]["name"]
               }
           }
       }
   )
   
   # Create the flow from the nodes and connections
   client.create_flow(
       name="FlowCreatePlaylist",
       description="A flow that creates a playlist given a genre and number of songs to include in the playlist.",
       executionRoleArn=FLOWS_SERVICE_ROLE,
       definition={
           "nodes": [input_node, prompt_node, output_node],
           "connections": connections
       }
   )
   ```

1. Delete the prompt version that you just created by running the following code snippet to make a [DeletePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeletePrompt.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Delete the prompt version that you created
   client.delete_prompt(
       promptIdentifier=prompt_id, 
       promptVersion=prompt_version
   )
   ```

1. Fully delete the prompt that you just created by running the following code snippet to make a [DeletePrompt](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_DeletePrompt.html) [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt):

   ```
   # Delete the prompt that you created
   client.delete_prompt(
       promptIdentifier=prompt_id
   )
   ```

------

## Invoke a managed prompt
<a name="prompt-management-invoke-ex"></a>

After you create and version a prompt, you can invoke it for inference using the [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) API. Specify the prompt ARN as the `modelId` and provide values for any prompt variables in the `promptVariables` field.

```
import boto3, json

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Use the prompt ARN (with version) as the modelId
prompt_arn = "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT_ID:VERSION"

response = bedrock_runtime.converse(
    modelId=prompt_arn,
    promptVariables={
        "genre": {"text": "jazz"},
        "number": {"text": "5"}
    }
)

# Print the response
print(response["output"]["message"]["content"][0]["text"])
```

**Note**  
When invoking a managed prompt, you don't need to specify `messages` or `system` fields — these are defined in the prompt template. You only need to provide values for the variables defined in the prompt.