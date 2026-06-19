

# A tool use demo illustrating how to connect AI models on Amazon Bedrock with a custom tool or API
<a name="bedrock-runtime_example_bedrock-runtime_Scenario_ToolUseDemo_AnthropicClaude_section"></a>

The following code examples show how to build a typical interaction between an application, a generative AI model, and connected tools or APIs to mediate interactions between the AI and the outside world. It uses the example of connecting an external weather API to the AI model so it can provide real-time weather information based on user input.

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples). 
The primary execution script of the demo. This script orchestrates the conversation between the user, the Amazon Bedrock Converse API, and a weather tool.  

```
"""
This demo illustrates a tool use scenario using Amazon Bedrock's Converse API and a weather tool.
The script interacts with a foundation model on Amazon Bedrock to provide weather information based on user
input. It uses the Open-Meteo API (https://open-meteo.com) to retrieve current weather data for a given location.
"""

import boto3
import logging
from enum import Enum

import utils.tool_use_print_utils as output
import weather_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")

AWS_REGION = "us-east-1"


# For the most recent list of models supported by the Converse API's tool use functionality, visit:
# https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
class SupportedModels(Enum):
    CLAUDE_OPUS = "anthropic.claude-3-opus-20240229-v1:0"
    CLAUDE_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    COHERE_COMMAND_R = "cohere.command-r-v1:0"
    COHERE_COMMAND_R_PLUS = "cohere.command-r-plus-v1:0"


# Set the model ID, e.g., Claude 3 Haiku.
MODEL_ID = SupportedModels.CLAUDE_HAIKU.value

SYSTEM_PROMPT = """
You are a weather assistant that provides current weather data for user-specified locations using only
the Weather_Tool, which expects latitude and longitude. Infer the coordinates from the location yourself.
If the user provides coordinates, infer the approximate location and refer to it in your response.
To use the tool, you strictly apply the provided tool specification.

- Explain your step-by-step process, and give brief updates before each step.
- Only use the Weather_Tool for data. Never guess or make up information. 
- Repeat the tool use for subsequent requests if necessary.
- If the tool errors, apologize, explain weather is unavailable, and suggest other options.
- Report temperatures in °C (°F) and wind in km/h (mph). Keep weather reports concise. Sparingly use
  emojis where appropriate.
- Only respond to weather queries. Remind off-topic users of your purpose. 
- Never claim to search online, access external data, or use tools besides Weather_Tool.
- Complete the entire process until you have all required data before sending the complete response.
"""

# The maximum number of recursive calls allowed in the tool_use_demo function.
# This helps prevent infinite loops and potential performance issues.
MAX_RECURSIONS = 5


class ToolUseDemo:
    """
    Demonstrates the tool use feature with the Amazon Bedrock Converse API.
    """

    def __init__(self):
        # Prepare the system prompt
        self.system_prompt = [{"text": SYSTEM_PROMPT}]

        # Prepare the tool configuration with the weather tool's specification
        self.tool_config = {"tools": [weather_tool.get_tool_spec()]}

        # Create a Bedrock Runtime client in the specified AWS Region.
        self.bedrockRuntimeClient = boto3.client(
            "bedrock-runtime", region_name=AWS_REGION
        )

    def run(self):
        """
        Starts the conversation with the user and handles the interaction with Bedrock.
        """
        # Print the greeting and a short user guide
        output.header()

        # Start with an emtpy conversation
        conversation = []

        # Get the first user input
        user_input = self._get_user_input()

        while user_input is not None:
            # Create a new message with the user input and append it to the conversation
            message = {"role": "user", "content": [{"text": user_input}]}
            conversation.append(message)

            # Send the conversation to Amazon Bedrock
            bedrock_response = self._send_conversation_to_bedrock(conversation)

            # Recursively handle the model's response until the model has returned
            # its final response or the recursion counter has reached 0
            self._process_model_response(
                bedrock_response, conversation, max_recursion=MAX_RECURSIONS
            )

            # Repeat the loop until the user decides to exit the application
            user_input = self._get_user_input()

        output.footer()

    def _send_conversation_to_bedrock(self, conversation):
        """
        Sends the conversation, the system prompt, and the tool spec to Amazon Bedrock, and returns the response.

        :param conversation: The conversation history including the next message to send.
        :return: The response from Amazon Bedrock.
        """
        output.call_to_bedrock(conversation)

        # Send the conversation, system prompt, and tool configuration, and return the response
        return self.bedrockRuntimeClient.converse(
            modelId=MODEL_ID,
            messages=conversation,
            system=self.system_prompt,
            toolConfig=self.tool_config,
        )

    def _process_model_response(
        self, model_response, conversation, max_recursion=MAX_RECURSIONS
    ):
        """
        Processes the response received via Amazon Bedrock and performs the necessary actions
        based on the stop reason.

        :param model_response: The model's response returned via Amazon Bedrock.
        :param conversation: The conversation history.
        :param max_recursion: The maximum number of recursive calls allowed.
        """

        if max_recursion <= 0:
            # Stop the process, the number of recursive calls could indicate an infinite loop
            logging.warning(
                "Warning: Maximum number of recursions reached. Please try again."
            )
            exit(1)

        # Append the model's response to the ongoing conversation
        message = model_response["output"]["message"]
        conversation.append(message)

        if model_response["stopReason"] == "tool_use":
            # If the stop reason is "tool_use", forward everything to the tool use handler
            self._handle_tool_use(message, conversation, max_recursion)

        if model_response["stopReason"] == "end_turn":
            # If the stop reason is "end_turn", print the model's response text, and finish the process
            output.model_response(message["content"][0]["text"])
            return

    def _handle_tool_use(
        self, model_response, conversation, max_recursion=MAX_RECURSIONS
    ):
        """
        Handles the tool use case by invoking the specified tool and sending the tool's response back to Bedrock.
        The tool response is appended to the conversation, and the conversation is sent back to Amazon Bedrock for further processing.

        :param model_response: The model's response containing the tool use request.
        :param conversation: The conversation history.
        :param max_recursion: The maximum number of recursive calls allowed.
        """

        # Initialize an empty list of tool results
        tool_results = []

        # The model's response can consist of multiple content blocks
        for content_block in model_response["content"]:
            if "text" in content_block:
                # If the content block contains text, print it to the console
                output.model_response(content_block["text"])

            if "toolUse" in content_block:
                # If the content block is a tool use request, forward it to the tool
                tool_response = self._invoke_tool(content_block["toolUse"])

                # Add the tool use ID and the tool's response to the list of results
                tool_results.append(
                    {
                        "toolResult": {
                            "toolUseId": (tool_response["toolUseId"]),
                            "content": [{"json": tool_response["content"]}],
                        }
                    }
                )

        # Embed the tool results in a new user message
        message = {"role": "user", "content": tool_results}

        # Append the new message to the ongoing conversation
        conversation.append(message)

        # Send the conversation to Amazon Bedrock
        response = self._send_conversation_to_bedrock(conversation)

        # Recursively handle the model's response until the model has returned
        # its final response or the recursion counter has reached 0
        self._process_model_response(response, conversation, max_recursion - 1)

    def _invoke_tool(self, payload):
        """
        Invokes the specified tool with the given payload and returns the tool's response.
        If the requested tool does not exist, an error message is returned.

        :param payload: The payload containing the tool name and input data.
        :return: The tool's response or an error message.
        """
        tool_name = payload["name"]

        if tool_name == "Weather_Tool":
            input_data = payload["input"]
            output.tool_use(tool_name, input_data)

            # Invoke the weather tool with the input data provided by
            response = weather_tool.fetch_weather_data(input_data)
        else:
            error_message = (
                f"The requested tool with name '{tool_name}' does not exist."
            )
            response = {"error": "true", "message": error_message}

        return {"toolUseId": payload["toolUseId"], "content": response}

    @staticmethod
    def _get_user_input(prompt="Your weather info request"):
        """
        Prompts the user for input and returns the user's response.
        Returns None if the user enters 'x' to exit.

        :param prompt: The prompt to display to the user.
        :return: The user's input or None if the user chooses to exit.
        """
        output.separator()
        user_input = input(f"{prompt} (x to exit): ")

        if user_input == "":
            prompt = "Please enter your weather info request, e.g. the name of a city"
            return ToolUseDemo._get_user_input(prompt)

        elif user_input.lower() == "x":
            return None

        else:
            return user_input


if __name__ == "__main__":
    tool_use_demo = ToolUseDemo()
    tool_use_demo.run()
```
The weather tool used by the demo. This script defines the tool specification and implements the logic to retrieve weather data using from the Open-Meteo API.  

```
import requests
from requests.exceptions import RequestException


def get_tool_spec():
    """
    Returns the JSON Schema specification for the Weather tool. The tool specification
    defines the input schema and describes the tool's functionality.
    For more information, see https://json-schema.org/understanding-json-schema/reference.

    :return: The tool specification for the Weather tool.
    """
    return {
        "toolSpec": {
            "name": "Weather_Tool",
            "description": "Get the current weather for a given location, based on its WGS84 coordinates.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "string",
                            "description": "Geographical WGS84 latitude of the location.",
                        },
                        "longitude": {
                            "type": "string",
                            "description": "Geographical WGS84 longitude of the location.",
                        },
                    },
                    "required": ["latitude", "longitude"],
                }
            },
        }
    }


def fetch_weather_data(input_data):
    """
    Fetches weather data for the given latitude and longitude using the Open-Meteo API.
    Returns the weather data or an error message if the request fails.

    :param input_data: The input data containing the latitude and longitude.
    :return: The weather data or an error message.
    """
    endpoint = "https://api.open-meteo.com/v1/forecast"
    latitude = input_data.get("latitude")
    longitude = input_data.get("longitude", "")
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}

    try:
        response = requests.get(endpoint, params=params)
        weather_data = {"weather_data": response.json()}
        response.raise_for_status()
        return weather_data
    except RequestException as e:
        return e.response.json()
    except Exception as e:
        return {"error": type(e), "message": str(e)}
```
+  For API details, see [Converse](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/Converse) in *AWS SDK for Python (Boto3) API Reference*. 

------
#### [ Rust ]

**SDK for Rust**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/rustv1/examples/bedrock-runtime#code-examples). 
The primary scenario and logic for the demo. This orchestrates the conversation between the user, the Amazon Bedrock Converse API, and a weather tool.  

```
#[derive(Debug)]
#[allow(dead_code)]
struct InvokeToolResult(String, ToolResultBlock);
struct ToolUseScenario {
    client: Client,
    conversation: Vec<Message>,
    system_prompt: SystemContentBlock,
    tool_config: ToolConfiguration,
}

impl ToolUseScenario {
    fn new(client: Client) -> Self {
        let system_prompt = SystemContentBlock::Text(SYSTEM_PROMPT.into());
        let tool_config = ToolConfiguration::builder()
            .tools(Tool::ToolSpec(
                ToolSpecification::builder()
                    .name(TOOL_NAME)
                    .description(TOOL_DESCRIPTION)
                    .input_schema(ToolInputSchema::Json(make_tool_schema()))
                    .build()
                    .unwrap(),
            ))
            .build()
            .unwrap();

        ToolUseScenario {
            client,
            conversation: vec![],
            system_prompt,
            tool_config,
        }
    }

    async fn run(&mut self) -> Result<(), ToolUseScenarioError> {
        loop {
            let input = get_input().await?;
            if input.is_none() {
                break;
            }

            let message = Message::builder()
                .role(User)
                .content(ContentBlock::Text(input.unwrap()))
                .build()
                .map_err(ToolUseScenarioError::from)?;
            self.conversation.push(message);

            let response = self.send_to_bedrock().await?;

            self.process_model_response(response).await?;
        }

        Ok(())
    }

    async fn send_to_bedrock(&mut self) -> Result<ConverseOutput, ToolUseScenarioError> {
        debug!("Sending conversation to bedrock");
        self.client
            .converse()
            .model_id(MODEL_ID)
            .set_messages(Some(self.conversation.clone()))
            .system(self.system_prompt.clone())
            .tool_config(self.tool_config.clone())
            .send()
            .await
            .map_err(ToolUseScenarioError::from)
    }

    async fn process_model_response(
        &mut self,
        mut response: ConverseOutput,
    ) -> Result<(), ToolUseScenarioError> {
        let mut iteration = 0;

        while iteration < MAX_RECURSIONS {
            iteration += 1;
            let message = if let Some(ref output) = response.output {
                if output.is_message() {
                    Ok(output.as_message().unwrap().clone())
                } else {
                    Err(ToolUseScenarioError(
                        "Converse Output is not a message".into(),
                    ))
                }
            } else {
                Err(ToolUseScenarioError("Missing Converse Output".into()))
            }?;

            self.conversation.push(message.clone());

            match response.stop_reason {
                StopReason::ToolUse => {
                    response = self.handle_tool_use(&message).await?;
                }
                StopReason::EndTurn => {
                    print_model_response(&message.content[0])?;
                    return Ok(());
                }
                _ => (),
            }
        }

        Err(ToolUseScenarioError(
            "Exceeded MAX_ITERATIONS when calling tools".into(),
        ))
    }

    async fn handle_tool_use(
        &mut self,
        message: &Message,
    ) -> Result<ConverseOutput, ToolUseScenarioError> {
        let mut tool_results: Vec<ContentBlock> = vec![];

        for block in &message.content {
            match block {
                ContentBlock::Text(_) => print_model_response(block)?,
                ContentBlock::ToolUse(tool) => {
                    let tool_response = self.invoke_tool(tool).await?;
                    tool_results.push(ContentBlock::ToolResult(tool_response.1));
                }
                _ => (),
            };
        }

        let message = Message::builder()
            .role(User)
            .set_content(Some(tool_results))
            .build()?;
        self.conversation.push(message);

        self.send_to_bedrock().await
    }

    async fn invoke_tool(
        &mut self,
        tool: &ToolUseBlock,
    ) -> Result<InvokeToolResult, ToolUseScenarioError> {
        match tool.name() {
            TOOL_NAME => {
                println!(
                    "\x1b[0;90mExecuting tool: {TOOL_NAME} with input: {:?}...\x1b[0m",
                    tool.input()
                );
                let content = fetch_weather_data(tool).await?;
                println!(
                    "\x1b[0;90mTool responded with {:?}\x1b[0m",
                    content.content()
                );
                Ok(InvokeToolResult(tool.tool_use_id.clone(), content))
            }
            _ => Err(ToolUseScenarioError(format!(
                "The requested tool with name {} does not exist",
                tool.name()
            ))),
        }
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    let sdk_config = aws_config::defaults(BehaviorVersion::latest())
        .region(CLAUDE_REGION)
        .load()
        .await;
    let client = Client::new(&sdk_config);

    let mut scenario = ToolUseScenario::new(client);

    header();
    if let Err(err) = scenario.run().await {
        println!("There was an error running the scenario! {}", err.0)
    }
    footer();
}
```
The weather tool used by the demo. This script defines the tool specification and implements the logic to retrieve weather data using from the Open-Meteo API.  

```
const ENDPOINT: &str = "https://api.open-meteo.com/v1/forecast";
async fn fetch_weather_data(
    tool_use: &ToolUseBlock,
) -> Result<ToolResultBlock, ToolUseScenarioError> {
    let input = tool_use.input();
    let latitude = input
        .as_object()
        .unwrap()
        .get("latitude")
        .unwrap()
        .as_string()
        .unwrap();
    let longitude = input
        .as_object()
        .unwrap()
        .get("longitude")
        .unwrap()
        .as_string()
        .unwrap();
    let params = [
        ("latitude", latitude),
        ("longitude", longitude),
        ("current_weather", "true"),
    ];

    debug!("Calling {ENDPOINT} with {params:?}");

    let response = reqwest::Client::new()
        .get(ENDPOINT)
        .query(&params)
        .send()
        .await
        .map_err(|e| ToolUseScenarioError(format!("Error requesting weather: {e:?}")))?
        .error_for_status()
        .map_err(|e| ToolUseScenarioError(format!("Failed to request weather: {e:?}")))?;

    debug!("Response: {response:?}");

    let bytes = response
        .bytes()
        .await
        .map_err(|e| ToolUseScenarioError(format!("Error reading response: {e:?}")))?;

    let result = String::from_utf8(bytes.to_vec())
        .map_err(|_| ToolUseScenarioError("Response was not utf8".into()))?;

    Ok(ToolResultBlock::builder()
        .tool_use_id(tool_use.tool_use_id())
        .content(ToolResultContentBlock::Text(result))
        .build()?)
}
```
Utilities to print the Message Content Blocks.  

```
fn print_model_response(block: &ContentBlock) -> Result<(), ToolUseScenarioError> {
    if block.is_text() {
        let text = block.as_text().unwrap();
        println!("\x1b[0;90mThe model's response:\x1b[0m\n{text}");
        Ok(())
    } else {
        Err(ToolUseScenarioError(format!(
            "Content block is not text ({block:?})"
        )))
    }
}
```
Use statements, Error utility, and constants.  

```
use std::{collections::HashMap, io::stdin};

use aws_config::BehaviorVersion;
use aws_sdk_bedrockruntime::{
    error::{BuildError, SdkError},
    operation::converse::{ConverseError, ConverseOutput},
    types::{
        ContentBlock, ConversationRole::User, Message, StopReason, SystemContentBlock, Tool,
        ToolConfiguration, ToolInputSchema, ToolResultBlock, ToolResultContentBlock,
        ToolSpecification, ToolUseBlock,
    },
    Client,
};
use aws_smithy_runtime_api::http::Response;
use aws_smithy_types::Document;
use tracing::debug;

// Set the model ID, e.g., Claude 3 Haiku.
const MODEL_ID: &str = "anthropic.claude-3-haiku-20240307-v1:0";
const CLAUDE_REGION: &str = "us-east-1";

const SYSTEM_PROMPT: &str = "You are a weather assistant that provides current weather data for user-specified locations using only
the Weather_Tool, which expects latitude and longitude. Infer the coordinates from the location yourself.
If the user provides coordinates, infer the approximate location and refer to it in your response.
To use the tool, you strictly apply the provided tool specification.

- Explain your step-by-step process, and give brief updates before each step.
- Only use the Weather_Tool for data. Never guess or make up information. 
- Repeat the tool use for subsequent requests if necessary.
- If the tool errors, apologize, explain weather is unavailable, and suggest other options.
- Report temperatures in °C (°F) and wind in km/h (mph). Keep weather reports concise. Sparingly use
  emojis where appropriate.
- Only respond to weather queries. Remind off-topic users of your purpose. 
- Never claim to search online, access external data, or use tools besides Weather_Tool.
- Complete the entire process until you have all required data before sending the complete response.
";

// The maximum number of recursive calls allowed in the tool_use_demo function.
// This helps prevent infinite loops and potential performance issues.
const MAX_RECURSIONS: i8 = 5;

const TOOL_NAME: &str = "Weather_Tool";
const TOOL_DESCRIPTION: &str =
    "Get the current weather for a given location, based on its WGS84 coordinates.";
fn make_tool_schema() -> Document {
    Document::Object(HashMap::<String, Document>::from([
        ("type".into(), Document::String("object".into())),
        (
            "properties".into(),
            Document::Object(HashMap::from([
                (
                    "latitude".into(),
                    Document::Object(HashMap::from([
                        ("type".into(), Document::String("string".into())),
                        (
                            "description".into(),
                            Document::String("Geographical WGS84 latitude of the location.".into()),
                        ),
                    ])),
                ),
                (
                    "longitude".into(),
                    Document::Object(HashMap::from([
                        ("type".into(), Document::String("string".into())),
                        (
                            "description".into(),
                            Document::String(
                                "Geographical WGS84 longitude of the location.".into(),
                            ),
                        ),
                    ])),
                ),
            ])),
        ),
        (
            "required".into(),
            Document::Array(vec![
                Document::String("latitude".into()),
                Document::String("longitude".into()),
            ]),
        ),
    ]))
}

#[derive(Debug)]
struct ToolUseScenarioError(String);
impl std::fmt::Display for ToolUseScenarioError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Tool use error with '{}'. Reason: {}", MODEL_ID, self.0)
    }
}
impl From<&str> for ToolUseScenarioError {
    fn from(value: &str) -> Self {
        ToolUseScenarioError(value.into())
    }
}
impl From<BuildError> for ToolUseScenarioError {
    fn from(value: BuildError) -> Self {
        ToolUseScenarioError(value.to_string().clone())
    }
}
impl From<SdkError<ConverseError, Response>> for ToolUseScenarioError {
    fn from(value: SdkError<ConverseError, Response>) -> Self {
        ToolUseScenarioError(match value.as_service_error() {
            Some(value) => value.meta().message().unwrap_or("Unknown").into(),
            None => "Unknown".into(),
        })
    }
}
```
+  For API details, see [Converse](https://docs.rs/aws-sdk-bedrockruntime/latest/aws_sdk_bedrockruntime/client/struct.Client.html#method.converse) in *AWS SDK for Rust API reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.