

# Test your guardrail
<a name="guardrails-test"></a>

After you create a guardrail, a *working draft* (`DRAFT`) version is available. The working draft is a version of the guardrail that you can continually edit and iterate upon until you reach a satisfactory configuration for your use case. You can test and benchmark the working draft or other versions of the guardrail to ensure that the configurations meet your use-case requirements. Edit configurations in the working draft and test different prompts to see how well the guardrail evaluates and intercepts the prompts or responses.

When you are satisfied with the configuration, you can then create a version of the guardrail, which acts as a snapshot of the configurations of the working draft when you create the version. You can use versions to streamline guardrails deployment to production applications every time you make modifications to your guardrails. Any changes to the working draft or a new version created will not be reflected in your generative AI application until you specifically use the new version in the application.

------
#### [ Console ]

**To test a guardrail to see if blocks harmful content**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Choose **Guardrails** from the left navigation pane. Then, select a guardrail in the **Guardrails** section.

1. A test window appears on the right. You have the following options in the test window:

   1. By default, the working draft of the guardrail is used in the test window. To test a different version of the guardrail, choose **Working draft** at the top of the test window and then select the version.

   1. To select a model, choose **Select model**. After you make a choice, select **Apply**. To change the model, choose **Change**.

   1. Enter a prompt in the **Prompt** box.

   1. To elicit a model response, select **Run**.

   1. The model returns a response in the **Final response** box (that may be modified by the guardrail). If the guardrail blocks or filters the prompt or model response, a message appears under **Guardrail check** that informs you how many violations the guardrail detected.

   1. To view the topics or harmful categories in the prompt or response that were recognized and allowed past the filter or blocked by it, select **View trace**.

   1. Use the **Prompt** and **Model response** tabs to view the topics or harmful categories that were filtered or blocked by the guardrail.

You can also test the guardrail in the **Text playground**. Select the playground and select the **Guardrail** in the **Configurations** pane before testing prompts.

------
#### [ API ]

To use a guardrail in model invocation, send an [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) or [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) request. Alternatively, if you are building a conversational application, you can use the [Converse API](guardrails-use-converse-api.md).

**Request format**

The request endpoints for invoking a model, with and without streaming, are as follows. Replace {{modelId}} with the ID of the model to use.
+ `InvokeModel` – POST /model/{{modelId}}/invoke HTTP/1.1
+ `InvokeModelWithResponseStream` – POST /model/{{modelId}}/invoke-with-response-stream HTTP/1.1

The header for both API operations is of the following format.

```
Accept: {{accept}}
Content-Type: {{contentType}}
X-Amzn-Bedrock-Trace: {{trace}}
X-Amzn-Bedrock-GuardrailIdentifier: {{guardrailIdentifier}}
X-Amzn-Bedrock-GuardrailVersion: {{guardrailVersion}}
```

The parameters are described below.
+ Set `Accept` to the MIME type of the inference body in the response. The default value is `application/json`.
+ Set `Content-Type` to the MIME type of the input data in the request. The default value is `application/json`.
+ Set `X-Amzn-Bedrock-Trace` to `ENABLED` to enable a trace to see amongst other things what content was blocked by guardrails and why..
+ Set `X-Amzn-Bedrock-GuardrailIdentifier` with the guardrail identifier of the guardrail you want to apply to the request to the request and model response.
+ Set `X-Amzn-Bedrock-GuardrailVersion ` with the version of the guardrail you want to apply to the request and model response.

The general request body format is shown in the following example. The `tagSuffix` property is only used with *Input tagging*. You can also configure the guardrail on streaming synchronously or asynchronously by using `streamProcessingMode`. This only works with `InvokeModelWithResponseStream`.

```
{
    {{<see model details>}},
    "amazon-bedrock-guardrailConfig": {
        "tagSuffix": "{{string}}", 
        "streamProcessingMode": "{{SYNCHRONOUS" | "ASYNCHRONOUS}}"
    }
}
```

**Warning**  
You will get an error in the following situations  
You enable the guardrail but there is no `amazon-bedrock-guardrailConfig` field in the request body.
You disable the guardrail but you specify an `amazon-bedrock-guardrailConfig` field in the request body.
You enable the guardrail but the `contentType` is not `application/json`.

To see the request body for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md).

**Note**  
For Cohere Command models, you can only specify one generation in the `num_generations` field if you use a guardrail.

If you enable a guardrail and its trace, the general format of the response for invoking a model, with and without streaming, is as follows. To see the format of the rest of the `body` for each model, see [Inference request parameters and response fields for foundation models](model-parameters.md). The {{contentType}} matches what you specified in the request.
+ `InvokeModel`

  ```
  HTTP/1.1 200
  Content-Type: contentType
  
  {
      <see model details for model-specific fields>,
      "completion": "<model response>",
      "amazon-bedrock-guardrailAction": "INTERVENED | NONE",
      "amazon-bedrock-trace": {
          "guardrail": {
              "modelOutput": [
                  "<see model details for model-specific fields>"
              ],
              "input": {
                  "{{sample-guardrailId}}": {
                      "topicPolicy": {
                          "topics": [
                              {
                                  "name": "string",
                                  "type": "string",
                                  "action": "string"
                              }
                          ]
                      },
                      "contentPolicy": {
                          "filters": [
                              {
                                  "type": "string",
                                  "confidence": "string",
                                  "filterStrength": "string",
                                  "action": "string"
                              }
                          ]
                      },
                      "wordPolicy": {
                          "customWords": [
                              {
                                  "match": "string",
                                  "action": "string"
                              }
                          ],
                          "managedWordLists": [
                              {
                                  "match": "string",
                                  "type": "string",
                                  "action": "string"
                              }
                          ]
                      },
                      "sensitiveInformationPolicy": {
                          "piiEntities": [
                              {
                                  "type": "string",
                                  "match": "string",
                                  "action": "string"
                              }
                          ],
                          "regexes": [
                              {
                                  "name": "string",
                                  "regex": "string",
                                  "match": "string",
                                  "action": "string"
                              }
                          ]
                      },
                      "invocationMetrics": {
                          "guardrailProcessingLatency": "integer",
                          "usage": {
                              "topicPolicyUnits": "integer",
                              "contentPolicyUnits": "integer",
                              "wordPolicyUnits": "integer",
                              "sensitiveInformationPolicyUnits": "integer",
                              "sensitiveInformationPolicyFreeUnits": "integer",
                              "contextualGroundingPolicyUnits": "integer"
                          },
                          "guardrailCoverage": {
                              "textCharacters": {
                              "guarded": "integer",
                              "total": "integer"
                              }
                          }
                      }
                  }
              },
              "outputs": ["{{same guardrail trace format as input}}"]
          }
      }
  }
  ```
+ `InvokeModelWithResponseStream` – Each response returns a `chunk` whose text is in the `bytes` field, alongside any exceptions that occur. The guardrail trace is returned only for the last chunk.

  ```
  HTTP/1.1 200
  X-Amzn-Bedrock-Content-Type: {{contentType}}
  Content-type: application/json
  
  {
      "chunk": { 
        "bytes": "<blob>"
      },
    "internalServerException": {},
    "modelStreamErrorException": {},
    "throttlingException": {},
    "validationException": {},
    "amazon-bedrock-guardrailAction": "INTERVENED | NONE",
    "amazon-bedrock-trace": {
      "guardrail": {
        "modelOutput": ["<see model details for model-specific fields>"],
        "input": {
          "{{sample-guardrailId}}": {
            "topicPolicy": {
              "topics": [
                {
                  "name": "string",
                  "type": "string",
                  "action": "string"
                }
              ]
            },
            "contentPolicy": {
              "filters": [
                {
                  "type": "string",
                  "confidence": "string",
                  "filterStrength": "string",
                  "action": "string"
                }
              ]
            },
            "wordPolicy": {
              "customWords": [
                {
                  "match": "string",
                  "action": "string"
                }
              ],
              "managedWordLists": [
                {
                  "match": "string",
                  "type": "string",
                  "action": "string"
                }
              ]
            },
            "sensitiveInformationPolicy": {
              "piiEntities": [
                {
                  "type": "string",
                  "match": "string",
                  "action": "string"
                }
              ],
              "regexes": [
                {
                  "name": "string",
                  "regex": "string",
                  "match": "string",
                  "action": "string"
                }
              ]
            },
            "invocationMetrics": {
              "guardrailProcessingLatency": "integer",
              "usage": {
                "topicPolicyUnits": "integer",
                "contentPolicyUnits": "integer",
                "wordPolicyUnits": "integer",
                "sensitiveInformationPolicyUnits": "integer",
                "sensitiveInformationPolicyFreeUnits": "integer",
                "contextualGroundingPolicyUnits": "integer"
              },
              "guardrailCoverage": {
                "textCharacters": {
                  "guarded": "integer",
                  "total": "integer"
                }
              }
            }
          }
        },
        "outputs": ["{{same guardrail trace format as input}}"]
      }
    }
  }
  ```

The response returns the following fields if you enable a guardrail.
+ `amazon-bedrock-guardrailAction` – Specifies whether the guardrail `INTERVENED` or not (`NONE`).
+ `amazon-bedrock-trace` – Only appears if you enable the trace. Contains a list of traces, each of which provides information about the content that the guardrail blocked. The trace contains the following fields:
  + `modelOutput` – An object containing the outputs from the model that was blocked.
  + `input` – Contains the following details about the guardrail's assessment of the prompt:
    + `topicPolicy` – Contains `topics`, a list of assessments for each topic policy that was violated. Each topic includes the following fields:
      + `name` – The name of the topic policy.
      + `type` – Specifies whether to deny the topic.
      + `action` – Specifies that the topic was blocked 
    + `contentPolicy` – Contains `filters`, a list of assessments for each content filter that was violated. Each filter includes the following fields:
      + `type` – The category of the content filter.
      + `confidence` – The level of confidence that the output can be categorized as belonging to the harmful category.
      + `action` – Specifies that the content was blocked. This result depends on the strength of the filter set in the guardrail.
    + `wordPolicy` – Contains a collection of custom words and managed words were filtered and a corresponding assessment on those words. Each list contains the following fields:
      + `customWords` – A list of custom words that matched the filter.
        + `match` – The word or phrase that matched the filter.
        + `action` – Specifies that the word was blocked.
      + `managedWordLists` – A list of managed words that matched the filter.
        + `match` – The word or phrase that matched the filter.
        + `type` – Specifies the type of managed word that matched the filter. For example, `PROFANITY` if it matched the profanity filter.
        + `action` – Specifies that the word was blocked.
    + `sensitiveInformationPolicy` – Contains the following objects, which contain assessments for personally identifiable information (PII) and regex filters that were violated:
      + `piiEntities` – A list of assessments for each PII filter that was violated. Each filter contains the following fields:
        + `type` – The PII type that was found.
        + `match` – The word or phrase that matched the filter.
        + `action` – Specifies whether the word was `BLOCKED` or replaced with an identifier (`ANONYMIZED`).
      + `regexes` – A list of assessments for each regex filter that was violated. Each filter contains the following fields:
        + `name` – The name of the regex filter.
        + `regex` – The PII type that was found.
        + `match` – The word or phrase that matched the filter.
        + `action` – Specifies whether the word was `BLOCKED` or replaced with an identifier (`ANONYMIZED`).
  + `outputs` – A list of details about the guardrail's assessment of the model response. Each item in the list is an object that matches the format of the `input` object. For more details, see the `input` field.

------