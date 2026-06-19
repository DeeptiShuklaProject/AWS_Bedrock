

# Block harmful images with content filters
<a name="guardrails-mmfilter"></a>

Amazon Bedrock Guardrails can help block inappropriate or harmful images while configuring content filters within a guardrail.

**Prerequisites and Limitations**
+ This capability is supported for only images and not supported for images with embedded video content.
+ This capability is generally available in US East (N. Virginia), US West (Oregon), Europe (Frankfurt), and Asia Pacific (Tokyo) AWS Regions, where it is supported for Hate, Insults, Sexual, Violence, Misconduct, and Prompt Attack categories within content filters.
+ This capability is available in preview in US East (Ohio), Asia Pacific (Mumbai, Seoul, Singapore, Sydney), Europe (Ireland, London), and US GovCloud (US-West) AWS Regions, where it is supported for Hate, Insults, Sexual, and Violence categories within content filters.
+ Maximum image dimensions allowed for the feature are 8000x8000 (for both JPEG and PNG files).
+ Users can upload images with sizes up to a maximum of 4 MB, with a maximum of 20 images for a single request.
+ Default limit of 25 images per second. This value is not configurable.
+ Only PNG and JPEG formats are supported for image content.

**Overview**

The detection and blocking of harmful images are supported for only images or images with text in them. While creating a guardrail, users can select the image option by itself or along with the text option, and set the respective filtering strength to **NONE**, **LOW**, **MEDIUM**, or **HIGH**. These thresholds will be common to both text and image content if both modalities are selected. Guardrails will evaluate images sent as an input by users, or generated as outputs from model responses.

The supported categories for detection of harmful image content are described below: 
+ **Hate** – Describes contents that discriminate, criticize, insult, denounce, or dehumanize a person or group on the basis of an identity (such as race, ethnicity, gender, religion, sexual orientation, ability, and national origin). It also includes graphic and real-life visual content displaying symbols of hate groups, hateful symbols, and imagery associated with various organizations promoting discrimination, racism, and intolerance. 
+ **Insults** – Describes content that includes demeaning, humiliating, mocking, insulting, or belittling language. This type of language is also labeled as bullying. It also encompasses various forms of rude, disrespectful or offensive hand gestures intended to express contempt, anger, or disapproval. 
+ **Sexual** – Describes content that indicates sexual interest, activity, or arousal using direct or indirect references to body parts, physical traits, or sex. It also includes images displaying private parts and sexual activity involving intercourse. This category also encompasses cartoons, animé, drawings, sketches, and other illustrated content with sexual themes. 
+ **Violence** – Describes content that includes glorification of or threats to inflict physical pain, hurt, or injury toward a person, group, or thing. It also encompasses imagery related to weapons with the intent to harm. 
+ **Misconduct** – Describes input prompts and model responses that seeks or provides information about engaging in criminal activity, or harming, defrauding, or taking advantage of a person, group or institution. 
+ **Prompt attack** – Describes user prompts intended to bypass the safety and moderation capabilities of a foundation model in order to generate harmful content (also known as jailbreak), and to ignore and to override instructions specified by the developer (referred to as prompt injection). Requires input tagging to be used in order for prompt attack to be applied. Prompt attacks detection requires input tags to be used.

**Topics**
+ [Using the image content filter](#guardrails-use-mmfilter)
+ [Configuring content filters for images with API](#guardrails-use-mmfilter-configure)
+ [Configuring the image filter to work with ApplyGuardrail API](#guardrails-use-mmfilter-api)
+ [Configuring the image filter to work with Image generation models](#guardrails-use-mmfilter-image-models)

## Using the image content filter
<a name="guardrails-use-mmfilter"></a>

**Creating or updating a Guardrail with content filters for images**

While creating a new guardrail or updating an existing guardrail, users will now see an option to select image in addition to the existing text option.

**Note**  
By default, the text option is enabled, and the image option needs to be explicitly enabled. Users can choose both text and image or either one of them depending on the use case.

**Filter classification and blocking levels**

Filtering is done based on the confidence classification of user inputs and FM responses. All user inputs and model responses are classified across four strength levels - None, Low, Medium, and High. The filter strength determines the sensitivity of filtering harmful content. As the filter strength is increased, the likelihood of filtering harmful content increases and the probability of seeing harmful content in your application decreases. When both image and text options are selected, the same filter strength is applied to both modalities for a particular category.

1. To configure image and text filters for harmful categories, select **Configure harmful categories filter**. 

1. Select **Text** and/or **Image** to filter text or image content from prompts or responses to and from the model. 

1. Select **None, Low, Medium, or High** for the level of filtration you want to apply to each category. A setting of **High** helps to block the most text or images that apply to that category of the filter.

1. Select **Use the same harmful categories filters for responses** to use the same filter settings you used for prompts. You can also choose to have different filter levels for prompts or responses by not selecting this option. Select **Reset threshold** to reset all the filter levels for prompts or responses.

1. Select **Review and create** or **Next** to create the guardrail.

## Configuring content filters for images with API
<a name="guardrails-use-mmfilter-configure"></a>

You can use the guardrail API to configure the image content filter in Amazon Bedrock Guardrails. The example below shows an Amazon Bedrock Guardrails filter with different harmful content categories and filter strengths applied. You can use this template as an example for your own use case. 

With the `contentPolicyConfig` operation, `filtersConfig` is a object, as shown in the following example.

**Example Python Boto3 code for creating a Guardrail with Image Content Filters**

```
import boto3
import botocore
import json


def main():
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    try:
        create_guardrail_response = bedrock.create_guardrail(
            name='{{my-image-guardrail}}',
            contentPolicyConfig={
                'filtersConfig': [
                    {
                        'type': 'SEXUAL',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH',
                        'inputModalities': ['TEXT', 'IMAGE'],
                        'outputModalities': ['TEXT', 'IMAGE']
                    },
                    {
                        'type': 'VIOLENCE',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH',
                        'inputModalities': ['TEXT', 'IMAGE'],
                        'outputModalities': ['TEXT', 'IMAGE']
                    },
                    {
                        'type': 'HATE',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH',
                        'inputModalities': ['TEXT', 'IMAGE'],
                        'outputModalities': ['TEXT', 'IMAGE']
                    },
                    {
                        'type': 'INSULTS',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH',
                        'inputModalities': ['TEXT', 'IMAGE'],
                        'outputModalities': ['TEXT', 'IMAGE']
                    },
                    {
                        'type': 'MISCONDUCT',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH',
                        'inputModalities': ['TEXT'],
                        'outputModalities': ['TEXT']
                    },
                    {
                        'type': 'PROMPT_ATTACK',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'NONE',
                        'inputModalities': ['TEXT'],
                        'outputModalities': ['TEXT']
                    }
                ]
            },
            blockedInputMessaging='Sorry, the model cannot answer this question.',
            blockedOutputsMessaging='Sorry, the model cannot answer this question.',
        )
        create_guardrail_response['createdAt'] = create_guardrail_response['createdAt'].strftime('%Y-%m-%d %H:%M:%S')
        print("Successfully created guardrail with details:")
        print(json.dumps(create_guardrail_response, indent=2))
    except botocore.exceptions.ClientError as err:
        print("Failed while calling CreateGuardrail API with RequestId = " + err.response['ResponseMetadata']['RequestId'])
        raise err


if __name__ == "__main__":
    main()
```

## Configuring the image filter to work with ApplyGuardrail API
<a name="guardrails-use-mmfilter-api"></a>

You can use content filters for both image and text content using the `ApplyGuardrail` API. This option allows you to use the content filter settings without invoking the Amazon Bedrock model. You can update the request payload in the following script for various models by following the inference parameters documentation for each bedrock foundation model that is supported by Amazon Bedrock Guardrails. 

You can update the request payload in below script for various models by following the inference parameters documentation for each bedrock foundation model that is supported by Amazon Bedrock Guardrails.

```
import boto3
import botocore
import json


guardrail_id = 'guardrail-id'
guardrail_version = 'DRAFT'
content_source = 'INPUT'
image_path = '/path/to/image.jpg'

with open(image_path, 'rb') as image:
    image_bytes = image.read()

content = [
    {
        "text": {
            "text": "Hi, can you explain this image art to me."
        }
    },
    {
        "image": {
            "format": "jpeg",
            "source": {
                "bytes": image_bytes
            }
        }
    }
]


def main():
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    try:
        print("Making a call to ApplyGuardrail API now")
        response = bedrock_runtime_client.apply_guardrail(
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version,
            source=content_source,
            content=content
        )
        print("Received response from ApplyGuardrail API:")
        print(json.dumps(response, indent=2))
    except botocore.exceptions.ClientError as err:
        print("Failed while calling ApplyGuardrail API with RequestId = " + err.response['ResponseMetadata']['RequestId'])
        raise err


if __name__ == "__main__":
    main()
```

## Configuring the image filter to work with Image generation models
<a name="guardrails-use-mmfilter-image-models"></a>

You can also use Amazon Bedrock Guardrails image filters with Image generation models like Titan Image Generator and Stability Image or Diffusion models. These models are currently supported through the `InvokeModel` API which can be invoked with a guardrail. You can update the request payload in the following script for various models by following the inference parameters documentation for various Amazon Bedrock foundation models that are supported by guardrails.

```
import base64
import boto3
import botocore
import json
import os
import random
import string


guardrail_id = 'guardrail-id'
guardrail_version = 'DRAFT'

model_id = 'stability.sd3-5-large-v1:0'
output_images_folder = '/path/to/folder/'

body = json.dumps(
    {
        "prompt": "Create an image of a beautiful flower", # Prompt for image generation ("A gun" should get blocked by violence)
        "output_format": "jpeg"
    }
)


def main():
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name="us-west-2")
    try:
        print("Making a call to InvokeModel API for model: {}".format(model_id))
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            trace='ENABLED',
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version
        )
        response_body = json.loads(response.get('body').read())
        print("Received response from InvokeModel API (Request Id: {})".format(response['ResponseMetadata']['RequestId']))
        if 'images' in response_body and len(response_body['images']) > 0:
            os.makedirs(output_images_folder, exist_ok=True)
            images = response_body["images"]
            for image in images:
                image_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                image_file = os.path.join(output_images_folder, "generated-image-{}.jpg".format(image_id))
                print("Saving generated image {} at {}".format(image_id, image_file))
                with open(image_file, 'wb') as image_file_descriptor:
                    image_file_descriptor.write(base64.b64decode(image.encode('utf-8')))
        else:
            print("No images generated from model")
        guardrail_trace = response_body['amazon-bedrock-trace']['guardrail']
        guardrail_trace['modelOutput'] = ['<REDACTED>']
        print("Guardrail Trace: {}".format(json.dumps(guardrail_trace, indent=2)))
    except botocore.exceptions.ClientError as err:
        print("Failed while calling InvokeModel API with RequestId = {}".format(err.response['ResponseMetadata']['RequestId']))
        raise err


if __name__ == "__main__":
    main()
```