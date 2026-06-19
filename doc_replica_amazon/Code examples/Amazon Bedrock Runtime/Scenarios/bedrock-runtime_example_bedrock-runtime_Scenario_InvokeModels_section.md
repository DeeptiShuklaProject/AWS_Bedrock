

# Invoke multiple foundation models on Amazon Bedrock
<a name="bedrock-runtime_example_bedrock-runtime_Scenario_InvokeModels_section"></a>

The following code examples show how to prepare and send a prompt to a variety of large-language models (LLMs) on Amazon Bedrock

------
#### [ Go ]

**SDK for Go V2**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/gov2/bedrock-runtime#code-examples). 
Invoke multiple foundation models on Amazon Bedrock.  

```
import (
	"context"
	"encoding/base64"
	"fmt"
	"log"
	"math/rand"
	"os"
	"path/filepath"
	"strings"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
	"github.com/awsdocs/aws-doc-sdk-examples/gov2/bedrock-runtime/actions"
	"github.com/awsdocs/aws-doc-sdk-examples/gov2/demotools"
)

// InvokeModelsScenario demonstrates how to use the Amazon Bedrock Runtime client
// to invoke various foundation models for text and image generation
//
// 1. Generate text with Anthropic Claude 2
// 2. Generate text with Meta Llama 2 Chat
// 3. Generate text and asynchronously process the response stream with Anthropic Claude 2
// 4. Generate an image with the Amazon Titan image generation model
type InvokeModelsScenario struct {
	sdkConfig             aws.Config
	invokeModelWrapper    actions.InvokeModelWrapper
	responseStreamWrapper actions.InvokeModelWithResponseStreamWrapper
	questioner            demotools.IQuestioner
}

// NewInvokeModelsScenario constructs an InvokeModelsScenario instance from a configuration.
// It uses the specified config to get a Bedrock Runtime client and create wrappers for the
// actions used in the scenario.
func NewInvokeModelsScenario(sdkConfig aws.Config, questioner demotools.IQuestioner) InvokeModelsScenario {
	client := bedrockruntime.NewFromConfig(sdkConfig)
	return InvokeModelsScenario{
		sdkConfig:             sdkConfig,
		invokeModelWrapper:    actions.InvokeModelWrapper{BedrockRuntimeClient: client},
		responseStreamWrapper: actions.InvokeModelWithResponseStreamWrapper{BedrockRuntimeClient: client},
		questioner:            questioner,
	}
}

// Runs the interactive scenario.
func (scenario InvokeModelsScenario) Run(ctx context.Context) {
	defer func() {
		if r := recover(); r != nil {
			log.Printf("Something went wrong with the demo: %v\n", r)
		}
	}()

	log.Println(strings.Repeat("=", 77))
	log.Println("Welcome to the Amazon Bedrock Runtime model invocation demo.")
	log.Println(strings.Repeat("=", 77))

	log.Printf("First, let's invoke a few large-language models using the synchronous client:\n\n")

	text2textPrompt := "In one paragraph, who are you?"

	log.Println(strings.Repeat("-", 77))
	log.Printf("Invoking Claude with prompt: %v\n", text2textPrompt)
	scenario.InvokeClaude(ctx, text2textPrompt)

	log.Println(strings.Repeat("=", 77))
	log.Printf("Now, let's invoke Claude with the asynchronous client and process the response stream:\n\n")

	log.Println(strings.Repeat("-", 77))
	log.Printf("Invoking Claude with prompt: %v\n", text2textPrompt)
	scenario.InvokeWithResponseStream(ctx, text2textPrompt)

	log.Println(strings.Repeat("=", 77))
	log.Printf("Now, let's create an image with the Amazon Titan image generation model:\n\n")

	text2ImagePrompt := "stylized picture of a cute old steampunk robot"
	seed := rand.Int63n(2147483648)

	log.Println(strings.Repeat("-", 77))
	log.Printf("Invoking Amazon Titan with prompt: %v\n", text2ImagePrompt)
	scenario.InvokeTitanImage(ctx, text2ImagePrompt, seed)

	log.Println(strings.Repeat("=", 77))
	log.Println("Thanks for watching!")
	log.Println(strings.Repeat("=", 77))
}

func (scenario InvokeModelsScenario) InvokeClaude(ctx context.Context, prompt string) {
	completion, err := scenario.invokeModelWrapper.InvokeClaude(ctx, prompt)
	if err != nil {
		panic(err)
	}
	log.Printf("\nClaude     : %v\n", strings.TrimSpace(completion))
}

func (scenario InvokeModelsScenario) InvokeWithResponseStream(ctx context.Context, prompt string) {
	log.Println("\nClaude with response stream:")
	_, err := scenario.responseStreamWrapper.InvokeModelWithResponseStream(ctx, prompt)
	if err != nil {
		panic(err)
	}
	log.Println()
}

func (scenario InvokeModelsScenario) InvokeTitanImage(ctx context.Context, prompt string, seed int64) {
	base64ImageData, err := scenario.invokeModelWrapper.InvokeTitanImage(ctx, prompt, seed)
	if err != nil {
		panic(err)
	}
	imagePath := saveImage(base64ImageData, "amazon.titan-image-generator-v2")
	fmt.Printf("The generated image has been saved to %s\n", imagePath)
}
```
+ For API details, see the following topics in *AWS SDK for Go API Reference*.
  + [InvokeModel](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/bedrockruntime#Client.InvokeModel)
  + [InvokeModelWithResponseStream](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/bedrockruntime#Client.InvokeModelWithResponseStream)

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascriptv3/example_code/bedrock-runtime#code-examples). 

```
import { fileURLToPath } from "node:url";
import {
  Scenario,
  ScenarioAction,
  ScenarioInput,
  ScenarioOutput,
} from "@aws-doc-sdk-examples/lib/scenario/index.js";
import { FoundationModels } from "../config/foundation_models.js";

/**
 * @typedef {Object} ModelConfig
 * @property {Function} module
 * @property {Function} invoker
 * @property {string} modelId
 * @property {string} modelName
 */

const greeting = new ScenarioOutput(
  "greeting",
  "Welcome to the Amazon Bedrock Runtime client demo!",
  { header: true },
);

const selectModel = new ScenarioInput("model", "First, select a model:", {
  type: "select",
  choices: Object.values(FoundationModels).map((model) => ({
    name: model.modelName,
    value: model,
  })),
});

const enterPrompt = new ScenarioInput("prompt", "Now, enter your prompt:", {
  type: "input",
});

const printDetails = new ScenarioOutput(
  "print details",
  /**
   * @param {{ model: ModelConfig, prompt: string }} c
   */
  (c) => console.log(`Invoking ${c.model.modelName} with '${c.prompt}'...`),
);

const invokeModel = new ScenarioAction(
  "invoke model",
  /**
   * @param {{ model: ModelConfig, prompt: string, response: string }} c
   */
  async (c) => {
    const modelModule = await c.model.module();
    const invoker = c.model.invoker(modelModule);
    c.response = await invoker(c.prompt, c.model.modelId);
  },
);

const printResponse = new ScenarioOutput(
  "print response",
  /**
   * @param {{ response: string }} c
   */
  (c) => c.response,
);

const scenario = new Scenario("Amazon Bedrock Runtime Demo", [
  greeting,
  selectModel,
  enterPrompt,
  printDetails,
  invokeModel,
  printResponse,
]);

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  scenario.run();
}
```
+ For API details, see the following topics in *AWS SDK for JavaScript API Reference*.
  + [InvokeModel](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock-runtime/command/InvokeModelCommand)
  + [InvokeModelWithResponseStream](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock-runtime/command/InvokeModelWithResponseStreamCommand)

------
#### [ PHP ]

**SDK for PHP**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/php/example_code/bedrock-runtime/#code-examples). 
Invoke multiple LLMs on Amazon Bedrock.  

```
namespace BedrockRuntime;

class GettingStartedWithBedrockRuntime
{
    protected BedrockRuntimeService $bedrockRuntimeService;
    public function runExample()
    {
        echo "\n";
        echo "---------------------------------------------------------------------\n";
        echo "Welcome to the Amazon Bedrock Runtime getting started demo using PHP!\n";
        echo "---------------------------------------------------------------------\n";
        $bedrockRuntimeService = new BedrockRuntimeService();
        $prompt = 'In one paragraph, who are you?';
        echo "\nPrompt: " . $prompt;
        echo "\n\nAnthropic Claude:\n";
        echo $bedrockRuntimeService->invokeClaude($prompt);
        echo "\n---------------------------------------------------------------------\n";
        $image_prompt = 'stylized picture of a cute old steampunk robot';
        echo "\nImage prompt: " . $image_prompt;
        echo "\n\nStability.ai Stable Diffusion XL:\n";
        $diffusionSeed = rand(0, 4294967295);
        $style_preset = 'photographic';
        $base64 = $bedrockRuntimeService->invokeStableDiffusion($image_prompt, $diffusionSeed, $style_preset);
        $image_path = $this->saveImage($base64, 'stability.stable-diffusion-xl');
        echo "The generated image has been saved to $image_path";
        echo "\n\nAmazon Titan Image Generation:\n";
        $titanSeed = rand(0, 2147483647);
        $base64 = $bedrockRuntimeService->invokeTitanImage($image_prompt, $titanSeed);
        $image_path = $this->saveImage($base64, 'amazon.titan-image-generator-v2');
        echo "The generated image has been saved to $image_path";
    }

    private function saveImage($base64_image_data, $model_id): string
    {
        $output_dir = "output";
        if (!file_exists($output_dir)) {
            mkdir($output_dir);
        }

        $i = 1;
        while (file_exists("$output_dir/$model_id" . '_' . "$i.png")) {
            $i++;
        }

        $image_data = base64_decode($base64_image_data);
        $file_path = "$output_dir/$model_id" . '_' . "$i.png";
        $file = fopen($file_path, 'wb');
        fwrite($file, $image_data);
        fclose($file);
        return $file_path;
    }
}
```
+ For API details, see the following topics in *AWS SDK for PHP API Reference*.
  + [InvokeModel](https://docs.aws.amazon.com/goto/SdkForPHPV3/bedrock-runtime-2023-09-30/InvokeModel)
  + [InvokeModelWithResponseStream](https://docs.aws.amazon.com/goto/SdkForPHPV3/bedrock-runtime-2023-09-30/InvokeModelWithResponseStream)

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.