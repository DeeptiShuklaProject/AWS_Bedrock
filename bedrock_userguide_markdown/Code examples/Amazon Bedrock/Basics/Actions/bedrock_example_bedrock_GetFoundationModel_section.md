

# Use `GetFoundationModel` with an AWS SDK
<a name="bedrock_example_bedrock_GetFoundationModel_section"></a>

The following code examples show how to use `GetFoundationModel`.

------
#### [ Java ]

**SDK for Java 2.x**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/bedrock#code-examples). 
Get details about a foundation model using the synchronous Amazon Bedrock client.  

```
    /**
     * Get details about an Amazon Bedrock foundation model.
     *
     * @param bedrockClient   The service client for accessing Amazon Bedrock.
     * @param modelIdentifier The model identifier.
     * @return An object containing the foundation model's details.
     */
    public static FoundationModelDetails getFoundationModel(BedrockClient bedrockClient, String modelIdentifier) {
        try {
            GetFoundationModelResponse response = bedrockClient.getFoundationModel(
                    r -> r.modelIdentifier(modelIdentifier)
            );

            FoundationModelDetails model = response.modelDetails();

            System.out.println(" Model ID:                     " + model.modelId());
            System.out.println(" Model ARN:                    " + model.modelArn());
            System.out.println(" Model Name:                   " + model.modelName());
            System.out.println(" Provider Name:                " + model.providerName());
            System.out.println(" Lifecycle status:             " + model.modelLifecycle().statusAsString());
            System.out.println(" Input modalities:             " + model.inputModalities());
            System.out.println(" Output modalities:            " + model.outputModalities());
            System.out.println(" Supported customizations:     " + model.customizationsSupported());
            System.out.println(" Supported inference types:    " + model.inferenceTypesSupported());
            System.out.println(" Response streaming supported: " + model.responseStreamingSupported());

            return model;

        } catch (ValidationException e) {
            throw new IllegalArgumentException(e.getMessage());
        } catch (SdkException e) {
            System.err.println(e.getMessage());
            throw new RuntimeException(e);
        }
    }
```
Get details about a foundation model using the asynchronous Amazon Bedrock client.  

```
    /**
     * Get details about an Amazon Bedrock foundation model.
     *
     * @param bedrockClient   The async service client for accessing Amazon Bedrock.
     * @param modelIdentifier The model identifier.
     * @return An object containing the foundation model's details.
     */
    public static FoundationModelDetails getFoundationModel(BedrockAsyncClient bedrockClient, String modelIdentifier) {
        try {
            CompletableFuture<GetFoundationModelResponse> future = bedrockClient.getFoundationModel(
                    r -> r.modelIdentifier(modelIdentifier)
            );

            FoundationModelDetails model = future.get().modelDetails();

            System.out.println(" Model ID:                     " + model.modelId());
            System.out.println(" Model ARN:                    " + model.modelArn());
            System.out.println(" Model Name:                   " + model.modelName());
            System.out.println(" Provider Name:                " + model.providerName());
            System.out.println(" Lifecycle status:             " + model.modelLifecycle().statusAsString());
            System.out.println(" Input modalities:             " + model.inputModalities());
            System.out.println(" Output modalities:            " + model.outputModalities());
            System.out.println(" Supported customizations:     " + model.customizationsSupported());
            System.out.println(" Supported inference types:    " + model.inferenceTypesSupported());
            System.out.println(" Response streaming supported: " + model.responseStreamingSupported());

            return model;

        } catch (ExecutionException e) {
            if (e.getMessage().contains("ValidationException")) {
                throw new IllegalArgumentException(e.getMessage());
            } else {
                System.err.println(e.getMessage());
                throw new RuntimeException(e);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println(e.getMessage());
            throw new RuntimeException(e);
        }
    }
```
+  For API details, see [GetFoundationModel](https://docs.aws.amazon.com/goto/SdkForJavaV2/bedrock-2023-04-20/GetFoundationModel) in *AWS SDK for Java 2.x API Reference*. 

------
#### [ JavaScript ]

**SDK for JavaScript (v3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascriptv3/example_code/bedrock#code-examples). 
Get details about a foundation model.  

```
import { fileURLToPath } from "node:url";

import {
  BedrockClient,
  GetFoundationModelCommand,
} from "@aws-sdk/client-bedrock";

/**
 * Get details about an Amazon Bedrock foundation model.
 *
 * @return {FoundationModelDetails} - The list of available bedrock foundation models.
 */
export const getFoundationModel = async () => {
  const client = new BedrockClient();

  const command = new GetFoundationModelCommand({
    modelIdentifier: "amazon.titan-embed-text-v1",
  });

  const response = await client.send(command);

  return response.modelDetails;
};

// Invoke main function if this file was run directly.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const model = await getFoundationModel();
  console.log(model);
}
```
+  For API details, see [GetFoundationModel](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/bedrock/command/GetFoundationModelCommand) in *AWS SDK for JavaScript API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock#code-examples). 
Get details about a foundation model.  

```
    def get_foundation_model(self, model_identifier):
        """
        Get details about an Amazon Bedrock foundation model.

        :return: The foundation model's details.
        """

        try:
            return self.bedrock_client.get_foundation_model(
                modelIdentifier=model_identifier
            )["modelDetails"]
        except ClientError:
            logger.error(
                f"Couldn't get foundation models details for {model_identifier}"
            )
            raise
```
+  For API details, see [GetFoundationModel](https://docs.aws.amazon.com/goto/boto3/bedrock-2023-04-20/GetFoundationModel) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.