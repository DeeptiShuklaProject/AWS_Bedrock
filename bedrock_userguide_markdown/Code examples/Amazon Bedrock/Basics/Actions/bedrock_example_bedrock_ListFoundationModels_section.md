

# Use `ListFoundationModels` with an AWS SDK
<a name="bedrock_example_bedrock_ListFoundationModels_section"></a>

The following code examples show how to use `ListFoundationModels`.

------
#### [ .NET ]

**SDK for .NET (v4)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/dotnetv4/Bedrock#code-examples). 
List the available Bedrock foundation models.  

```
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
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/DotNetSDKV4/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for .NET API Reference*. 

------
#### [ Go ]

**SDK for Go V2**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/gov2/bedrock#code-examples). 
List the available Bedrock foundation models.  

```
import (
	"context"
	"log"

	"github.com/aws/aws-sdk-go-v2/service/bedrock"
	"github.com/aws/aws-sdk-go-v2/service/bedrock/types"
)

// FoundationModelWrapper encapsulates Amazon Bedrock actions used in the examples.
// It contains a Bedrock service client that is used to perform foundation model actions.
type FoundationModelWrapper struct {
	BedrockClient *bedrock.Client
}



// ListPolicies lists Bedrock foundation models that you can use.
func (wrapper FoundationModelWrapper) ListFoundationModels(ctx context.Context) ([]types.FoundationModelSummary, error) {

	var models []types.FoundationModelSummary

	result, err := wrapper.BedrockClient.ListFoundationModels(ctx, &bedrock.ListFoundationModelsInput{})

	if err != nil {
		log.Printf("Couldn't list foundation models. Here's why: %v\n", err)
	} else {
		models = result.ModelSummaries
	}
	return models, err
}
```
+  For API details, see [ListFoundationModels](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/bedrock#Client.ListFoundationModels) in *AWS SDK for Go API Reference*. 

------
#### [ Java ]

**SDK for Java 2.x**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/bedrock#code-examples). 
List the available Amazon Bedrock foundation models using the synchronous Amazon Bedrock client.  

```
    /**
     * Lists Amazon Bedrock foundation models that you can use.
     * You can filter the results with the request parameters.
     *
     * @param bedrockClient The service client for accessing Amazon Bedrock.
     * @return A list of objects containing the foundation models' details
     */
    public static List<FoundationModelSummary> listFoundationModels(BedrockClient bedrockClient) {

        try {
            ListFoundationModelsResponse response = bedrockClient.listFoundationModels(r -> {});

            List<FoundationModelSummary> models = response.modelSummaries();

            if (models.isEmpty()) {
                System.out.println("No available foundation models in " + region.toString());
            } else {
                for (FoundationModelSummary model : models) {
                    System.out.println("Model ID: " + model.modelId());
                    System.out.println("Provider: " + model.providerName());
                    System.out.println("Name:     " + model.modelName());
                    System.out.println();
                }
            }

            return models;

        } catch (SdkClientException e) {
            System.err.println(e.getMessage());
            throw new RuntimeException(e);
        }
    }
```
List the available Amazon Bedrock foundation models using the asynchronous Amazon Bedrock client.  

```
    /**
     * Lists Amazon Bedrock foundation models that you can use.
     * You can filter the results with the request parameters.
     *
     * @param bedrockClient The async service client for accessing Amazon Bedrock.
     * @return A list of objects containing the foundation models' details
     */
    public static List<FoundationModelSummary> listFoundationModels(BedrockAsyncClient bedrockClient) {
        try {
            CompletableFuture<ListFoundationModelsResponse> future = bedrockClient.listFoundationModels(r -> {});

            List<FoundationModelSummary> models = future.get().modelSummaries();

            if (models.isEmpty()) {
                System.out.println("No available foundation models in " + region.toString());
            } else {
                for (FoundationModelSummary model : models) {
                    System.out.println("Model ID: " + model.modelId());
                    System.out.println("Provider: " + model.providerName());
                    System.out.println("Name:     " + model.modelName());
                    System.out.println();
                }
            }

            return models;

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println(e.getMessage());
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            System.err.println(e.getMessage());
            throw new RuntimeException(e);
        }
    }
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/SdkForJavaV2/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for Java 2.x API Reference*. 

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascriptv3/example_code/bedrock#code-examples). 
List the available foundation models.  

```
import { fileURLToPath } from "node:url";

import {
  BedrockClient,
  ListFoundationModelsCommand,
} from "@aws-sdk/client-bedrock";

/**
 * List the available Amazon Bedrock foundation models.
 *
 * @return {FoundationModelSummary[]} - The list of available bedrock foundation models.
 */
export const listFoundationModels = async () => {
  const client = new BedrockClient();

  const input = {
    // byProvider: 'STRING_VALUE',
    // byCustomizationType: 'FINE_TUNING' || 'CONTINUED_PRE_TRAINING',
    // byOutputModality: 'TEXT' || 'IMAGE' || 'EMBEDDING',
    // byInferenceType: 'ON_DEMAND' || 'PROVISIONED',
  };

  const command = new ListFoundationModelsCommand(input);

  const response = await client.send(command);

  return response.modelSummaries;
};

// Invoke main function if this file was run directly.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const models = await listFoundationModels();
  console.log(models);
}
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock/command/ListFoundationModelsCommand) in *AWS SDK for JavaScript API Reference*. 

------
#### [ Kotlin ]

**SDK for Kotlin**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/kotlin/services/bedrock#code-examples). 
List the available Amazon Bedrock foundation models.  

```
suspend fun listFoundationModels(): List<FoundationModelSummary>? {
    BedrockClient.fromEnvironment { region = "us-east-1" }.use { bedrockClient ->
        val response = bedrockClient.listFoundationModels(ListFoundationModelsRequest {})
        response.modelSummaries?.forEach { model ->
            println("==========================================")
            println(" Model ID: ${model.modelId}")
            println("------------------------------------------")
            println(" Name: ${model.modelName}")
            println(" Provider: ${model.providerName}")
            println(" Input modalities: ${model.inputModalities}")
            println(" Output modalities: ${model.outputModalities}")
            println(" Supported customizations: ${model.customizationsSupported}")
            println(" Supported inference types: ${model.inferenceTypesSupported}")
            println("------------------------------------------\n")
        }
        return response.modelSummaries
    }
}
```
+  For API details, see [ListFoundationModels](https://sdk.amazonaws.com/kotlin/api/latest/index.html) in *AWS SDK for Kotlin API reference*. 

------
#### [ PHP ]

**SDK for PHP**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/php/example_code/bedrock#code-examples). 
List the available Amazon Bedrock foundation models.  

```
    public function listFoundationModels()
    {
        $bedrockClient = new BedrockClient([
            'region' => 'us-west-2',
            'profile' => 'default'
        ]);
        $response = $bedrockClient->listFoundationModels();
        return $response['modelSummaries'];
    }
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/SdkForPHPV3/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for PHP API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock#code-examples). 
List the available Amazon Bedrock foundation models.  

```
    def list_foundation_models(self):
        """
        List the available Amazon Bedrock foundation models.

        :return: The list of available bedrock foundation models.
        """

        try:
            response = self.bedrock_client.list_foundation_models()
            models = response["modelSummaries"]
            logger.info("Got %s foundation models.", len(models))
            return models

        except ClientError:
            logger.error("Couldn't list foundation models.")
            raise
```
+  For API details, see [ListFoundationModels](https://docs.aws.amazon.com/goto/boto3/bedrock-2023-04-20/ListFoundationModels) in *AWS SDK for Python (Boto3) API Reference*. 

------
#### [ Swift ]

**SDK for Swift**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/swift/example_code/bedrock#code-examples). 

```
import AWSBedrock

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
```
+  For API details, see [ListFoundationModels](https://sdk.amazonaws.com/swift/api/awsbedrock/latest/documentation/awsbedrock/bedrockclient/listfoundationmodels(input:)) in *AWS SDK for Swift API reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.