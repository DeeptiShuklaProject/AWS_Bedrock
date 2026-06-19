

# Invoke Amazon Titan Image on Amazon Bedrock to generate an image
<a name="bedrock-runtime_example_bedrock-runtime_InvokeModel_TitanImageGenerator_section"></a>

The following code examples show how to invoke Amazon Titan Image on Amazon Bedrock to generate an image.

------
#### [ Go ]

**SDK for Go V2**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/gov2/bedrock-runtime#code-examples). 
Create an image with the Amazon Titan Image Generator.  

```
import (
	"context"
	"encoding/json"
	"log"
	"strings"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
)

// InvokeModelWrapper encapsulates Amazon Bedrock actions used in the examples.
// It contains a Bedrock Runtime client that is used to invoke foundation models.
type InvokeModelWrapper struct {
	BedrockRuntimeClient *bedrockruntime.Client
}



type TitanImageRequest struct {
	TaskType              string                `json:"taskType"`
	TextToImageParams     TextToImageParams     `json:"textToImageParams"`
	ImageGenerationConfig ImageGenerationConfig `json:"imageGenerationConfig"`
}
type TextToImageParams struct {
	Text string `json:"text"`
}
type ImageGenerationConfig struct {
	NumberOfImages int     `json:"numberOfImages"`
	Quality        string  `json:"quality"`
	CfgScale       float64 `json:"cfgScale"`
	Height         int     `json:"height"`
	Width          int     `json:"width"`
	Seed           int64   `json:"seed"`
}

type TitanImageResponse struct {
	Images []string `json:"images"`
}

// Invokes the Titan Image model to create an image using the input provided
// in the request body.
func (wrapper InvokeModelWrapper) InvokeTitanImage(ctx context.Context, prompt string, seed int64) (string, error) {
	modelId := "amazon.titan-image-generator-v2:0"

	body, err := json.Marshal(TitanImageRequest{
		TaskType: "TEXT_IMAGE",
		TextToImageParams: TextToImageParams{
			Text: prompt,
		},
		ImageGenerationConfig: ImageGenerationConfig{
			NumberOfImages: 1,
			Quality:        "standard",
			CfgScale:       8.0,
			Height:         512,
			Width:          512,
			Seed:           seed,
		},
	})

	if err != nil {
		log.Fatal("failed to marshal", err)
	}

	output, err := wrapper.BedrockRuntimeClient.InvokeModel(ctx, &bedrockruntime.InvokeModelInput{
		ModelId:     aws.String(modelId),
		ContentType: aws.String("application/json"),
		Body:        body,
	})

	if err != nil {
		ProcessError(err, modelId)
	}

	var response TitanImageResponse
	if err := json.Unmarshal(output.Body, &response); err != nil {
		log.Fatal("failed to unmarshal", err)
	}

	base64ImageData := response.Images[0]

	return base64ImageData, nil

}
```
+  For API details, see [InvokeModel](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/bedrockruntime#Client.InvokeModel) in *AWS SDK for Go API Reference*. 

------
#### [ Java ]

**SDK for Java 2.x**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/bedrock-runtime#code-examples). 
Create an image with the Amazon Titan Image Generator.  

```
// Create an image with the Amazon Titan Image Generator.

import org.json.JSONObject;
import org.json.JSONPointer;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

import java.math.BigInteger;
import java.security.SecureRandom;

import static com.example.bedrockruntime.libs.ImageTools.displayImage;

public class InvokeModel {

    public static String invokeModel() {

        // Create a Bedrock Runtime client in the AWS Region you want to use.
        // Replace the DefaultCredentialsProvider with your preferred credentials provider.
        var client = BedrockRuntimeClient.builder()
                .credentialsProvider(DefaultCredentialsProvider.create())
                .region(Region.US_EAST_1)
                .build();

        // Set the model ID, e.g., Titan Image G2.
        var modelId = "amazon.titan-image-generator-v2:0";

        // The InvokeModel API uses the model's native payload.
        // Learn more about the available inference parameters and response fields at:
        // https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html
        var nativeRequestTemplate = """
                {
                    "taskType": "TEXT_IMAGE",
                    "textToImageParams": { "text": "{{prompt}}" },
                    "imageGenerationConfig": { "seed": {{seed}} }
                }""";

        // Define the prompt for the image generation.
        var prompt = "A stylized picture of a cute old steampunk robot";

        // Get a random 31-bit seed for the image generation (max. 2,147,483,647).
        var seed = new BigInteger(31, new SecureRandom());

        // Embed the prompt and seed in the model's native request payload.
        var nativeRequest = nativeRequestTemplate
                .replace("{{prompt}}", prompt)
                .replace("{{seed}}", seed.toString());

        try {
            // Encode and send the request to the Bedrock Runtime.
            var response = client.invokeModel(request -> request
                    .body(SdkBytes.fromUtf8String(nativeRequest))
                    .modelId(modelId)
            );

            // Decode the response body.
            var responseBody = new JSONObject(response.body().asUtf8String());

            // Retrieve the generated image data from the model's response.
            var base64ImageData = new JSONPointer("/images/0").queryFrom(responseBody).toString();

            return base64ImageData;

        } catch (SdkClientException e) {
            System.err.printf("ERROR: Can't invoke '%s'. Reason: %s", modelId, e.getMessage());
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        System.out.println("Generating image. This may take a few seconds...");

        String base64ImageData = invokeModel();

        displayImage(base64ImageData);
    }
}
```
+  For API details, see [InvokeModel](https://docs.aws.amazon.com/goto/SdkForJavaV2/bedrock-runtime-2023-09-30/InvokeModel) in *AWS SDK for Java 2.x API Reference*. 

------
#### [ PHP ]

**SDK for PHP**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/php/example_code/bedrock-runtime#code-examples). 
Create an image with the Amazon Titan Image Generator.  

```
    public function invokeTitanImage(string $prompt, int $seed)
    {
        // The different model providers have individual request and response formats.
        // For the format, ranges, and default values for Titan Image models refer to:
        // https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html

        $base64_image_data = "";
        try {
            $modelId = 'amazon.titan-image-generator-v2:0';
            $request = json_encode([
                'taskType' => 'TEXT_IMAGE',
                'textToImageParams' => [
                    'text' => $prompt
                ],
                'imageGenerationConfig' => [
                    'numberOfImages' => 1,
                    'quality' => 'standard',
                    'cfgScale' => 8.0,
                    'height' => 512,
                    'width' => 512,
                    'seed' => $seed
                ]
            ]);
            $result = $this->bedrockRuntimeClient->invokeModel([
                'contentType' => 'application/json',
                'body' => $request,
                'modelId' => $modelId,
            ]);
            $response_body = json_decode($result['body']);
            $base64_image_data = $response_body->images[0];
        } catch (Exception $e) {
            echo "Error: ({$e->getCode()}) - {$e->getMessage()}\n";
        }

        return $base64_image_data;
    }
```
+  For API details, see [InvokeModel](https://docs.aws.amazon.com/goto/SdkForPHPV3/bedrock-runtime-2023-09-30/InvokeModel) in *AWS SDK for PHP API Reference*. 

------
#### [ Python ]

**SDK for Python (Boto3)**  
 There's more on GitHub. Find the complete example and learn how to set up and run in the [AWS Code Examples Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples). 
Create an image with the Amazon Titan Image Generator.  

```
# Use the native inference API to create an image with Amazon Titan Image Generator

import base64
import boto3
import json
import os
import random

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Image Generator G1.
model_id = "amazon.titan-image-generator-v2:0"

# Define the image generation prompt for the model.
prompt = "A stylized picture of a cute old steampunk robot."

# Generate a random seed.
seed = random.randint(0, 2147483647)

# Format the request payload using the model's native structure.
native_request = {
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {"text": prompt},
    "imageGenerationConfig": {
        "numberOfImages": 1,
        "quality": "standard",
        "cfgScale": 8.0,
        "height": 512,
        "width": 512,
        "seed": seed,
    },
}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
response = client.invoke_model(modelId=model_id, body=request)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract the image data.
base64_image_data = model_response["images"][0]

# Save the generated image to a local folder.
i, output_dir = 1, "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
while os.path.exists(os.path.join(output_dir, f"titan_{i}.png")):
    i += 1

image_data = base64.b64decode(base64_image_data)

image_path = os.path.join(output_dir, f"titan_{i}.png")
with open(image_path, "wb") as file:
    file.write(image_data)

print(f"The generated image has been saved to {image_path}")
```
+  For API details, see [InvokeModel](https://docs.aws.amazon.com/goto/boto3/bedrock-runtime-2023-09-30/InvokeModel) in *AWS SDK for Python (Boto3) API Reference*. 

------

For a complete list of AWS SDK developer guides and code examples, see [Using Amazon Bedrock with an AWS SDK](sdk-general-information-section.md). This topic also includes information about getting started and details about previous SDK versions.