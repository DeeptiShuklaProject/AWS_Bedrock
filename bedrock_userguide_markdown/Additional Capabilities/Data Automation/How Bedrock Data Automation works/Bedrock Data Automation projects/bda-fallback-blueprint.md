

# Using a fallback blueprint while using projects
<a name="bda-fallback-blueprint"></a>

When you use custom output with multiple blueprints, BDA attempts to match each document to the most appropriate blueprint. If no blueprint matches a document, BDA normally returns a `customOutputStatus` of `NO_MATCH` and no custom output is generated for that document. A fallback blueprint lets you specify a blueprint to use when no other blueprint matches, so you still receive custom output for every document.

## How fallback blueprints work
<a name="bda-fallback-blueprint-how-it-works"></a>

When BDA processes a document and cannot match it to any of the blueprints in your project, the following occurs:
+ **Without a fallback blueprint** — BDA returns `customOutputStatus: NO_MATCH` and no custom output for that document.
+ **With a fallback blueprint** — If the result is `NO_MATCH`, BDA uses the fallback blueprint to extract custom output and returns `customOutputStatus: FALLBACK`.

This is useful when you have specialized blueprints for known document types but still want structured output for unexpected or miscellaneous documents.

## Matching behavior with different blueprint configurations
<a name="bda-fallback-blueprint-matching-behavior"></a>

The matching behavior and confidence scores depend on how many blueprints are in your project and whether a fallback blueprint is configured:


| Configuration | Matching behavior | Confidence score | 
| --- | --- | --- | 
| One blueprint, no fallback | BDA forces a match to the single blueprint without running the matcher. | Always 1.0 | 
| One blueprint, with fallback | BDA runs the matcher against the single blueprint. If the document does not match, BDA uses the fallback blueprint. | True score, or 0 if fallback is used | 
| Multiple blueprints, no fallback | BDA runs the matcher against all blueprints and selects the best match. If no blueprint matches, returns `NO_MATCH`. | True score, or no custom output if no match | 
| Multiple blueprints, with fallback | BDA runs the matcher against all blueprints and selects the best match. If no blueprint matches, BDA uses the fallback blueprint. | True score, or 0 if fallback is used | 

Adding a fallback blueprint enables actual match confidence scoring in all configurations. In the single-blueprint case without a fallback, BDA skips the matcher entirely and always forces a match. With a fallback configured, BDA runs the matcher and gives you visibility into how well documents actually match your blueprints.

## Configuring a fallback blueprint
<a name="bda-fallback-blueprint-configure"></a>

You configure a fallback blueprint in the `customOutputConfiguration` when creating or updating a project. The fallback blueprint is specified under the `document` field and accepts a single blueprint.

The following example creates a project with two regular blueprints and one fallback blueprint. For more information about the fallback blueprint configuration, see [DocumentCustomOutputConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_DocumentCustomOutputConfiguration.html) in the API Reference.

**Python SDK**

```
response = client.create_data_automation_project(
    projectName={{project_name}},
    projectDescription="{{Provide a project description}}",
    projectStage='LIVE',
    standardOutputConfiguration=output_config,
    customOutputConfiguration={
        'blueprints': [
            {
                'blueprintArn': {{Blueprint ARN}},
                'blueprintStage': 'LIVE'
            },
            ...
        ],
        'document': {
            'fallbackBlueprints': [
                {
                    'blueprintArn': {{Fallback Blueprint ARN}},
                    'blueprintStage': 'LIVE'
                }
            ]
        }
    }
)
```

**AWS CLI**

```
aws bedrock-data-automation create-data-automation-project \
    --project-name {{project_name}} \
    --project-stage LIVE \
    --standard-output-configuration '{"document":{}}' \
    --custom-output-configuration '{
        "blueprints": [
            {
                "blueprintArn": "{{Blueprint ARN}}",
                "blueprintStage": "LIVE"
            }
        ],
        "document": {
            "fallbackBlueprints": [
                {
                    "blueprintArn": "{{Fallback Blueprint ARN}}",
                    "blueprintStage": "LIVE"
                }
            ]
        }
    }'
```

In this example, BDA first attempts to match each document to the invoice or receipt blueprint. If neither matches, BDA uses the general-document blueprint as a fallback.

**Note**  
You can specify at most one fallback blueprint per project. Fallback blueprints are supported for the document modality only.

## Understanding fallback output
<a name="bda-fallback-blueprint-output"></a>

The `customOutputStatus` field in the output indicates how the document was processed:


| customOutputStatus | Description | 
| --- | --- | 
| `MATCH` | The document matched one of the regular blueprints in the project. | 
| `NO_MATCH` | No blueprint matched and no fallback blueprint was configured. | 
| `FALLBACK` | No regular blueprint matched, but the fallback blueprint was used to generate custom output. | 

The following is an example output snippet from the [InvokeDataAutomationAsync](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomationAsync.html) API when a fallback blueprint is used:

```
{
  "semanticModality": "DOCUMENT",
  "outputSegments": [
    {
      "customOutputStatus": "FALLBACK",
      "standardOutput": {
        ...
      },
      "customOutput": {
        "matched_blueprint": {
          "arn": "arn:aws:bedrock:us-east-1:123456789012:blueprint/general-document",
          "version": "1",
          "name": "general-document",
          "confidence": 1.0
        },
        "inference_result": {
          ...
        }
      }
    }
  ]
}
```