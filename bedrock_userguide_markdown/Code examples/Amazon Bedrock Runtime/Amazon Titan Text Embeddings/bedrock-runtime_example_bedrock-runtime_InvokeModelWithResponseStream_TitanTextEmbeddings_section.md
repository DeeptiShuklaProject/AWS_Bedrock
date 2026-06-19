

# Invoke Amazon Titan Text Embeddings on Amazon Bedrock
<a name="bedrock-runtime_example_bedrock-runtime_InvokeModelWithResponseStream_TitanTextEmbeddings_section"></a>

The following code examples show how to:
+ Get started creating your first embedding.
+ Create embeddings configuring the number of dimensions and normalization (V2 only).

------
#### [ Java ]

**SDK for Java 2.x**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/bedrock-runtime#code-examples). 
Create your first embedding with Titan Text Embeddings V2.  

```
// Generate and print an embedding with Amazon Titan Text Embeddings.

import org.json.JSONObject;
import org.json.JSONPointer;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

public class InvokeModel {

    public static String invokeModel() {

        // Create a Bedrock Runtime client in the AWS Region you want to use.
        // Replace the DefaultCredentialsProvider with your preferred credentials provider.
        var client = BedrockRuntimeClient.builder()
                .credentialsProvider(DefaultCredentialsProvider.create())
                .region(Region.US_EAST_1)
                .build();

        // Set the model ID, e.g., Titan Text Embeddings V2.
        var modelId = "amazon.titan-embed-text-v2:0";

        // The InvokeModel API uses the model's native payload.
        // Learn more about the available inference parameters and response fields at:
        // https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-embed-text.html
        var nativeRequestTemplate = "{ \"inputText\": \"{{inputText}}\" }";

        // The text to convert into an embedding.
        var inputText = "Please recommend books with a theme similar to the movie 'Inception'.";

        // Embed the prompt in the model's native request payload.
        String nativeRequest = nativeRequestTemplate.replace("{{inputText}}", inputText);

        try {
            // Encode and send the request to the Bedrock Runtime.
            var response = client.invokeModel(request -> request
                    .body(SdkBytes.fromUtf8String(nativeRequest))
                    .modelId(modelId)
            );

            // Decode the response body.
            var responseBody = new JSONObject(response.body().asUtf8String());

            // Retrieve the generated text from the model's response.
            var text = new JSONPointer("/embedding").queryFrom(responseBody).toString();
            System.out.println(text);

            return text;

        } catch (SdkClientException e) {
            System.err.printf("ERROR: Can't invoke '%s'. Reason: %s", modelId, e.getMessage());
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        invokeModel();
    }
}
```
Invoke Titan Text Embeddings V2 configuring the number of dimensions and normalization.  

```
    /**
     * Invoke Amazon Titan Text Embeddings V2 with additional inference parameters.
     *
     * @param inputText  - The text to convert to an embedding.
     * @param dimensions - The number of dimensions the output embeddings should have.
     *                   Values accepted by the model: 256, 512, 1024.
     * @param normalize  - A flag indicating whether or not to normalize the output embeddings.
     * @return The {@link JSONObject} representing the model's response.
     */
    public static JSONObject invokeModel(String inputText, int dimensions, boolean normalize) {

        // Create a Bedrock Runtime client in the AWS Region of your choice.
        var client = BedrockRuntimeClient.builder()
                .region(Region.US_WEST_2)
                .build();

        // Set the model ID, e.g., Titan Embed Text v2.0.
        var modelId = "amazon.titan-embed-text-v2:0";

        // Create the request for the model.
        var nativeRequest = """
                {
                    "inputText": "%s",
                    "dimensions": %d,
                    "normalize": %b
                }
                """.formatted(inputText, dimensions, normalize);

        // Encode and send the request.
        var response = client.invokeModel(request -> {
            request.body(SdkBytes.fromUtf8String(nativeRequest));
            request.modelId(modelId);
        });

        // Decode the model's response.
        var modelResponse = new JSONObject(response.body().asUtf8String());

        // Extract and print the generated embedding and the input text token count.
        var embedding = modelResponse.getJSONArray("embedding");
        var inputTokenCount = modelResponse.getBigInteger("inputTextTokenCount");
        System.out.println("Embedding: " + embedding);
        System.out.println("\nInput token count: " + inputTokenCount);

        // Return the model's native response.
        return modelResponse;
    }
```
+  For API details, see [InvokeModel](https://docs.aws.amazon.com/goto/SdkForJavaV2/bedrock-runtime-2023-09-30/InvokeModel) in *AWS SDK for Java 2.x API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples). 
Create your first embedding with Amazon Titan Text Embeddings.  

```
# Generate and print an embedding with Amazon Titan Text Embeddings V2.

import boto3
import json

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Text Embeddings V2.
model_id = "amazon.titan-embed-text-v2:0"

# The text to convert to an embedding.
input_text = "Please recommend books with a theme similar to the movie 'Inception'."

# Create the request for the model.
native_request = {"inputText": input_text}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
response = client.invoke_model(modelId=model_id, body=request)

# Decode the model's native response body.
model_response = json.loads(response["body"].read())

# Extract and print the generated embedding and the input text token count.
embedding = model_response["embedding"]
input_token_count = model_response["inputTextTokenCount"]

print("\nYour input:")
print(input_text)
print(f"Number of input tokens: {input_token_count}")
print(f"Size of the generated embedding: {len(embedding)}")
print("Embedding:")
print(embedding)
```
+  For API details, see [InvokeModel](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/InvokeModel) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.