

# Hello Amazon Bedrock
<a name="bedrock_example_bedrock_Hello_section"></a>

The following code examples show how to get started using Amazon Bedrock.

------
#### [ .NET ]

**SDK for .NET (v4)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/dotnetv4/Bedrock#code-examples). 

```
using Amazon;
using Amazon.Bedrock;
using Amazon.Bedrock.Model;

namespace BedrockActions;

/// <summary>
/// This example shows how to list foundation models.
/// </summary>
internal class HelloBedrock
{
    /// <summary>
    /// Main method to call the ListFoundationModelsAsync method.
    /// </summary>
    /// <param name="args"> The command line arguments. </param>
    static async Task Main(string[] args)
    {
        // Specify a region endpoint where Amazon Bedrock is available. For a list of supported region see https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html#bedrock-regions
        AmazonBedrockClient bedrockClient = new(RegionEndpoint.USWest2);

        await ListFoundationModelsAsync(bedrockClient);

    }


    /// <summary>
    /// List foundation models.
    /// </summary>
    /// <param name="bedrockClient"> The Amazon Bedrock client. </param>
    private static async Task ListFoundationModelsAsync(AmazonBedrockClient bedrockClient)
    {
        Console.WriteLine("List foundation models with no filter.");

        try
        {
            var response = await bedrockClient.ListFoundationModelsAsync(new ListFoundationModelsRequest()
            {
            });

            if (response?.HttpStatusCode == System.Net.HttpStatusCode.OK)
            {
                foreach (var fm in response.ModelSummaries)
                {
                    WriteToConsole(fm);
                }
            }
            else
            {
                Console.WriteLine("Something wrong happened");
            }
        }
        catch (AmazonBedrockException e)
        {
            Console.WriteLine(e.Message);
        }
    }


    /// <summary>
    /// Write the foundation model summary to console.
    /// </summary>
    /// <param name="foundationModel"> The foundation model summary to write to console. </param>
    private static void WriteToConsole(FoundationModelSummary foundationModel)
    {
        Console.WriteLine($"{foundationModel.ModelId}, Customization: {string.Join(", ", foundationModel.CustomizationsSupported)}, Stream: {foundationModel.ResponseStreamingSupported}, Input: {string.Join(", ", foundationModel.InputModalities)}, Output: {string.Join(", ", foundationModel.OutputModalities)}");
    }
}
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/DotNetSDKV4/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for .NET API Reference*. 

------
#### [ Go ]

**SDK for Go V2**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/gov2/bedrock#code-examples). 

```
package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/bedrock"
)

const region = "us-east-1"

// main uses the AWS SDK for Go (v2) to create an Amazon Bedrock client and
// list the available foundation models in your account and the chosen region.
// This example uses the default settings specified in your shared credentials
// and config files.
func main() {
	ctx := context.Background()
	sdkConfig, err := config.LoadDefaultConfig(ctx, config.WithRegion(region))
	if err != nil {
		fmt.Println("Couldn't load default configuration. Have you set up your AWS account?")
		fmt.Println(err)
		return
	}
	bedrockClient := bedrock.NewFromConfig(sdkConfig)
	result, err := bedrockClient.ListFoundationModels(ctx, &bedrock.ListFoundationModelsInput{})
	if err != nil {
		fmt.Printf("Couldn't list foundation models. Here's why: %v\n", err)
		return
	}
	if len(result.ModelSummaries) == 0 {
		fmt.Println("There are no foundation models.")
	}
	for _, modelSummary := range result.ModelSummaries {
		fmt.Println(*modelSummary.ModelId)
	}
}
```
+  For API details, see [ListFoundationModels](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/bedrock#Client.ListFoundationModels) in *AWS SDK for Go API Reference*. 

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascriptv3/example_code/bedrock#code-examples). 

```
import { fileURLToPath } from "node:url";

import {
  BedrockClient,
  ListFoundationModelsCommand,
} from "@aws-sdk/client-bedrock";

const REGION = "us-east-1";
const client = new BedrockClient({ region: REGION });

export const main = async () => {
  const command = new ListFoundationModelsCommand({});

  const response = await client.send(command);
  const models = response.modelSummaries;

  console.log("Listing the available Bedrock foundation models:");

  for (const model of models) {
    console.log("=".repeat(42));
    console.log(` Model: ${model.modelId}`);
    console.log("-".repeat(42));
    console.log(` Name: ${model.modelName}`);
    console.log(` Provider: ${model.providerName}`);
    console.log(` Model ARN: ${model.modelArn}`);
    console.log(` Input modalities: ${model.inputModalities}`);
    console.log(` Output modalities: ${model.outputModalities}`);
    console.log(` Supported customizations: ${model.customizationsSupported}`);
    console.log(` Supported inference types: ${model.inferenceTypesSupported}`);
    console.log(` Lifecycle status: ${model.modelLifecycle.status}`);
    console.log(`${"=".repeat(42)}\n`);
  }

  const active = models.filter(
    (m) => m.modelLifecycle.status === "ACTIVE",
  ).length;
  const legacy = models.filter(
    (m) => m.modelLifecycle.status === "LEGACY",
  ).length;

  console.log(
    `There are ${active} active and ${legacy} legacy foundation models in ${REGION}.`,
  );

  return response;
};

// Invoke main function if this file was run directly.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await main();
}
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock/command/ListFoundationModelsCommand) in *AWS SDK for JavaScript API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock#code-examples). 

```
"""
Lists the available Amazon Bedrock models.
"""
import logging
import json
import boto3


from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_foundation_models(bedrock_client):
    """
    Gets a list of available Amazon Bedrock foundation models.

    :return: The list of available bedrock foundation models.
    """

    try:
        response = bedrock_client.list_foundation_models()
        models = response["modelSummaries"]
        logger.info("Got %s foundation models.", len(models))
        return models

    except ClientError:
        logger.error("Couldn't list foundation models.")
        raise


def main():
    """Entry point for the example. Uses the AWS SDK for Python (Boto3)
    to create an Amazon Bedrock client. Then lists the available Bedrock models
    in the region set in the callers profile and credentials.
    """

    bedrock_client = boto3.client(service_name="bedrock")

    fm_models = list_foundation_models(bedrock_client)
    for model in fm_models:
        print(f"Model: {model['modelName']}")
        print(json.dumps(model, indent=2))
        print("---------------------------\n")

    logger.info("Done.")


if __name__ == "__main__":
    main()
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/boto3/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for Python (Boto3) API Reference*. 

------
#### [ Swift ]

**SDK for Swift**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/swift/example_code/bedrock#code-examples). 

```
import ArgumentParser
import AWSClientRuntime
import Foundation

import AWSBedrock

struct ExampleCommand: ParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "ListFoundationModels",
        abstract: """
        This example demonstrates how to retrieve a list of the available
        foundation models from Amazon Bedrock.
        """,
        discussion: """
        """
    )

    /// Construct a string listing the specified modalities.
    /// 
    /// - Parameter modalities: An array of the modalities to list.
    ///
    /// - Returns: A string with a human-readable list of modalities.
    func buildModalityList(modalities: [BedrockClientTypes.ModelModality]?) -> String {
        var first = true
        var str = ""

        if modalities == nil {
            return "<none>"
        }

        for modality in modalities! {
            if !first {
                str += ", "
            }
            first = false
            str += modality.rawValue
        }

        return str
    }

    /// Construct a string listing the specified customizations.
    /// 
    /// - Parameter customizations: An array of the customizations to list.
    /// 
    /// - Returns: A string listing the customizations.
    func buildCustomizationList(customizations: [BedrockClientTypes.ModelCustomization]?) -> String {
        var first = true
        var str = ""

        if customizations == nil {
            return "<none>"
        }

        for customization in customizations! {
            if !first {
                str += ", "
            }
            first = false
            str += customization.rawValue
        }

        return str
    }

    /// Construct a string listing the specified inferences.
    /// 
    /// - Parameter inferences: An array of inferences to list.
    /// 
    /// - Returns: A string listing the specified inferences.
    func buildInferenceList(inferences: [BedrockClientTypes.InferenceType]?) -> String {
        var first = true
        var str = ""

        if inferences == nil {
            return "<none>"
        }

        for inference in inferences! {
            if !first {
                str += ", "
            }
            first = false
            str += inference.rawValue
        }

        return str
    }

    /// Called by ``main()`` to run the bulk of the example.
    func runAsync() async throws {
        // Always use the Region "us-east-1" to have access to the most models.
        let config = try await BedrockClient.BedrockClientConfiguration(region: "us-east-1")
        let bedrockClient = BedrockClient(config: config)

        let output = try await bedrockClient.listFoundationModels(
            input: ListFoundationModelsInput()
        )

        guard let summaries = output.modelSummaries else {
            print("No models returned.")
            return
        }
        
        // Output a list of the models with their details.
        for summary in summaries {
            print("==========================================")
            print(" Model ID: \(summary.modelId ?? "<unknown>")")
            print("------------------------------------------")
            print(" Name: \(summary.modelName ?? "<unknown>")")
            print(" Provider: \(summary.providerName ?? "<unknown>")")
            print(" Input modalities: \(buildModalityList(modalities: summary.inputModalities))")
            print(" Output modalities: \(buildModalityList(modalities: summary.outputModalities))")
            print(" Supported customizations: \(buildCustomizationList(customizations: summary.customizationsSupported ))")
            print(" Supported inference types: \(buildInferenceList(inferences: summary.inferenceTypesSupported))")
            print("------------------------------------------\n")
        }
        
        print("\(summaries.count) models available.")
    }
}

/// The program's asynchronous entry point.
@main
struct Main {
    static func main() async {
        let args = Array(CommandLine.arguments.dropFirst())

        do {
            let command = try ExampleCommand.parse(args)
            try await command.runAsync()
        } catch {
            ExampleCommand.exit(withError: error)
        }
    }    
}
```
+  For API details, see [ListFoundationModels](https://sdk.amazonaws.com/swift/api/awsbedrock/latest/documentation/awsbedrock/bedrockclient/listfoundationmodels(input:)) in *AWS SDK for Swift API reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.