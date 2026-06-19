

# Write a custom parser Lambda function in Amazon Bedrock Agents
<a name="lambda-parser"></a>

Each prompt template includes a parser Lambda function. You can write your own custom parser Lambda function and specify the templates whose default parser function you want to override. To write a custom parser Lambda function, you must understand the input event that your agent sends and the response that the agent expects as the output from the Lambda function. You write a handler function to manipulate variables from the input event and to return the response. For more information about how AWS Lambda works, see [Event-driven invocation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html#event-driven-invocation) in the AWS Lambda Developer Guide.

**Topics**
+ [Parser Lambda input event](#lambda-parser-input)
+ [Parser Lambda response](#lambda-parser-response)
+ [Parser Lambda examples](#lambda-parser-example)

## Parser Lambda input event
<a name="lambda-parser-input"></a>

The following is the general structure of the input event from the agent. Use the fields to write your Lambda handler function.

```
{
    "messageVersion": "1.0",
    "agent": {
        "name": "string",
        "id": "string",
        "alias": "string",
        "version": "string"
    },
    "invokeModelRawResponse": "string",
    "promptType": "ORCHESTRATION | ROUTING_CLASSIFIER | POST_PROCESSING | PRE_PROCESSING | KNOWLEDGE_BASE_RESPONSE_GENERATION | MEMORY_SUMMARIZATION",
    "overrideType": "OUTPUT_PARSER"
}
```

The following list describes the input event fields:
+ `messageVersion` – The version of the message that identifies the format of the event data going into the Lambda function and the expected format of the response from the Lambda function. Amazon Bedrock Agents only supports version 1.0.
+ `agent` – Contains information about the name, ID, alias, and version of the agent that the prompts belongs to.
+ `invokeModelRawResponse` – The raw foundation model output of the prompt whose output is to be parsed.
+ `promptType` – The prompt type whose output is to be parsed.
+ `overrideType` – The artifacts that this Lambda function overrides. Currently, only `OUTPUT_PARSER` is supported, which indicates that the default parser is to be overridden.

## Parser Lambda response
<a name="lambda-parser-response"></a>

Your agent expects a response from your Lambda function and uses the response to take further actions or to help it return a response to the user. Your agent executes the next action recommended by the agent’s model. The next actions can be executed in a serial order or in parallel depending on the agent’s model and when the agent was created and prepared. 

If you’ve created and prepared your agent *before October 4 2024* and if your agent is using Anthropic Claude 3 Sonnet or Anthropic Claude 3.5 Sonnet models, by default, the next top action recommended by the agent’s model will be run in serial order. 

If you’ve created a new agent or prepared an existing agent *after October 10 2024* and your agent is using Anthropic Claude 3 Sonnet, Anthropic Claude 3.5 Sonnet, or any non-Anthropic models, the next step actions recommended by the agent’s model will run in parallel. This means that multiple actions, for example, a mixture of action groups functions and knowledge bases, will be executed in parallel. This reduces the number of calls made to the model which reduces the overall latency.

You can enable parallel actions for your agents created and prepared *before October 4 2024* by calling [PrepareAgent](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_agent_PrepareAgent.html) API or by selecting **Prepare** in the your agent’s agent builder in the console. After the agent is prepared, you will see an updated prompt template and new version of parser Lambda schema. 

**Example parser Lambda response**

The following are examples of the general structure of the response from agent running next top recommended actions in serial order and agent running next actions in parallel. Use the Lambda function response fields to configure how the output is returned.

**Example of a response from an agent running next top recommended actions in serial order**

Select the tab corresponding to whether you defined the action group with an OpenAPI schema or with function details:

**Note**  
The `MessageVersion 1.0` indicates that the agent is running the next top recommended actions in serial order. 

------
#### [ OpenAPI schema ]

```
{
    "messageVersion": "1.0",
    "promptType": "ORCHESTRATION | PRE_PROCESSING | ROUTING_CLASSIFIER | POST_PROCESSING | KNOWLEDGE_BASE_RESPONSE_GENERATION",
    "preProcessingParsedResponse": {
        "isValidInput": "boolean",
        "rationale": "string"
    },
    "orchestrationParsedResponse": {
        "rationale": "string",
        "parsingErrorDetails": {
            "repromptResponse": "string"
        },
        "responseDetails": {
            "invocationType": "AGENT_COLLABORATOR | ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
            "agentAskUser": {
                "responseText": "string",
                "id": "string"
            },
            "agentCollaboratorInvocation": {
                "agentCollaboratorName": "string",
                "input": {
                    "text": "string"                    
                }
            },
            "actionGroupInvocation": {
                "actionGroupName": "string",
                "apiName": "string",
                "id": "string",
                "verb": "string",
                "actionGroupInput": {
                    "{{<parameter>}}": {
                        "value": "string"
                    },
                    ...
                }
            },
            "agentKnowledgeBase": {
                "knowledgeBaseId": "string",
                "id": "string",
                "searchQuery": {
                    "value": "string"
                }
            },
            "agentFinalResponse": {
                "responseText": "string",
                "citations": {
                    "generatedResponseParts": [{
                        "text": "string",
                        "references": [{"sourceId": "string"}]
                    }]
                }
            }
        }
    },
    "routingClassifierParsedResponse": {
        "parsingErrorDetails": {
            "repromptResponse": "string"
        },
        "responseDetails": {
            "type": "AGENT | LAST_AGENT | UNDECIDED",
            "agentCollaboratorInvocation": {
                "agentCollaboratorName": "string",
                "input": {
                    "text": "string"                    
                }
            }
        }
    },
    "knowledgeBaseResponseGenerationParsedResponse": { 
       "generatedResponse": {
            "generatedResponseParts": [
                {
                    "text": "string",
                    "references": [
                        {"sourceId": "string"},
                        ...
                    ]
                }
            ]
        }
    },
    "postProcessingParsedResponse": {
        "responseText": "string",
        "citations": {
            "generatedResponseParts": [{
                "text": "string",
                "references": [{
                    "sourceId": "string"
                }]
            }]
        }
    }
}
```

------
#### [ Function details ]

```
{
    "messageVersion": "1.0",
    "promptType": "ORCHESTRATION | PRE_PROCESSING | POST_PROCESSING | KNOWLEDGE_BASE_RESPONSE_GENERATION",
    "preProcessingParsedResponse": {
        "isValidInput": "boolean",
        "rationale": "string"
    },
    "orchestrationParsedResponse": {
        "rationale": "string",
        "parsingErrorDetails": {
            "repromptResponse": "string"
        },
        "responseDetails": {
            "invocationType": "ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
            "agentAskUser": {
                "responseText": "string",
                "id": "string"
            },
            "actionGroupInvocation": {
                "actionGroupName": "string",
                "functionName": "string",
                "id": "string",
                "actionGroupInput": {
                    "{{<parameter>}}": {
                        "value": "string"
                    },
                    ...
                }
            },
            "agentKnowledgeBase": {
                "knowledgeBaseId": "string",
                "id": "string",
                "searchQuery": {
                    "value": "string"
                }
            },
            "agentFinalResponse": {
                "responseText": "string",
                "citations": {
                    "generatedResponseParts": [{
                        "text": "string",
                        "references": [{"sourceId": "string"}]
                    }]
                }
            },
        }
    },
    "knowledgeBaseResponseGenerationParsedResponse": { 
       "generatedResponse": {
            "generatedResponseParts": [
                {
                    "text": "string",
                    "references": [
                        {"sourceId": "string"},
                        ...
                    ]
                }
            ]
        }
    },
    "postProcessingParsedResponse": {
        "responseText": "string",
        "citations": {
            "generatedResponseParts": [{
                "text": "string",
                "references": [{
                    "sourceId": "string"
                }]
            }]
        }
    }
}
```

------

**Example response from an agent running next actions in parallel **

Select the tab corresponding to whether you defined the action group with an OpenAPI schema or with function details:

**Note**  
The `MessageVersion 2.0` indicates that the agent is running the next recommended actions in parallel 

------
#### [ OpenAPI schema ]

```
{
    "messageVersion": "2.0",
    "promptType": "ORCHESTRATION | PRE_PROCESSING | POST_PROCESSING | KNOWLEDGE_BASE_RESPONSE_GENERATION",
    "preProcessingParsedResponse": {
        "isValidInput": "boolean",
        "rationale": "string"
    },
    "orchestrationParsedResponse": {
        "rationale": "string",
        "parsingErrorDetails": {
            "repromptResponse": "string"
        },
        "responseDetails": {
            "invocationType": "ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
            "agentAskUser": {
                "responseText": "string"
            },
            "actionGroupInvocations": [
                {
                    "actionGroupName": "string",
                    "apiName": "string",
                    "verb": "string",
                    "actionGroupInput": {
                        "{{<parameter>}}": {
                            "value": "string"
                        },
                        ...
                    }
                }
            ],
            "agentKnowledgeBases": [
                {
                    "knowledgeBaseId": "string",
                    "searchQuery": {
                        "value": "string"
                    }
                }
            ],
            "agentFinalResponse": {
                "responseText": "string",
                "citations": {
                    "generatedResponseParts": [{
                        "text": "string",
                        "references": [{"sourceId": "string"}]
                    }]
                }
            },
        }
    },
    "knowledgeBaseResponseGenerationParsedResponse": { 
       "generatedResponse": {
            "generatedResponseParts": [
                {
                    "text": "string",
                    "references": [
                        {"sourceId": "string"},
                        ...
                    ]
                }
            ]
        }
    },
    "postProcessingParsedResponse": {
        "responseText": "string",
        "citations": {
            "generatedResponseParts": [{
                "text": "string",
                "references": [{
                    "sourceId": "string"
                }]
            }]
        }
    }
}
```

------
#### [ Function details ]

```
{
    "messageVersion": "2.0",
    "promptType": "ORCHESTRATION | PRE_PROCESSING | POST_PROCESSING | KNOWLEDGE_BASE_RESPONSE_GENERATION",
    "preProcessingParsedResponse": {
        "isValidInput": "boolean",
        "rationale": "string"
    },
    "orchestrationParsedResponse": {
        "rationale": "string",
        "parsingErrorDetails": {
            "repromptResponse": "string"
        },
        "responseDetails": {
            "invocationType": "ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
            "agentAskUser": {
                "responseText": "string"
            },
            "actionGroupInvocations": [
                {
                    "actionGroupName": "string",
                    "functionName": "string",
                    "actionGroupInput": {
                        "{{<parameter>}}"": {
                            "value": "string"
                        },
                        ...
                    }
                }
            ],
            "agentKnowledgeBases": [
                {
                    "knowledgeBaseId": "string",
                    "searchQuery": {
                        "value": "string"
                    }
                }
            ],
            "agentFinalResponse": {
                "responseText": "string",
                "citations": {
                    "generatedResponseParts": [{
                        "text": "string",
                        "references": [{"sourceId": "string"}]
                    }]
                }
            },
        }
    },
    "knowledgeBaseResponseGenerationParsedResponse": { 
       "generatedResponse": {
            "generatedResponseParts": [
                {
                    "text": "string",
                    "references": [
                        {"sourceId": "string"},
                        ...
                    ]
                }
            ]
        }
    },
    "postProcessingParsedResponse": {
        "responseText": "string",
        "citations": {
            "generatedResponseParts": [{
                "text": "string",
                "references": [{
                    "sourceId": "string"
                }]
            }]
        }
    }
}
```

------

The following list describes the Lambda response fields:
+ `messageVersion` – The version of the message that identifies the format of the event data going into the Lambda function and the expected format of the response from a Lambda function. 
+ `promptType` – The prompt type of the current turn.
+ `preProcessingParsedResponse` – The parsed response for the `PRE_PROCESSING` prompt type.
+ `orchestrationParsedResponse` – The parsed response for the `ORCHESTRATION` prompt type. See below for more details.
+ `knowledgeBaseResponseGenerationParsedResponse` – The parsed response for the `KNOWLEDGE_BASE_RESPONSE_GENERATION` prompt type.
+ `postProcessingParsedResponse` – The parsed response for the `POST_PROCESSING` prompt type.

For more details about the parsed responses for the four prompt templates, see the following tabs.

------
#### [ preProcessingParsedResponse ]

```
{
    "isValidInput": "boolean",
    "rationale": "string"
}
```

The `preProcessingParsedResponse` contains the following fields.
+ `isValidInput` – Specifies whether the user input is valid or not. You can define the function to determine how to characterize the validity of user input.
+ `rationale` – The reasoning for the user input categorization. This rationale is provided by the model in the raw response, the Lambda function parses it, and the agent presents it in the trace for pre-processing.

------
#### [ orchestrationResponse ]

The format of the `orchestrationResponse` depends on whether you defined the action group with an OpenAPI schema or function details:
+ If you defined the action group with an OpenAPI schema, the response must be in the following format:

  ```
  {
      "rationale": "string",
      "parsingErrorDetails": {
          "repromptResponse": "string"
      },
      "responseDetails": {
          "invocationType": "ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
          "agentAskUser": {
              "responseText": "string",
              "id": "string"
          },
          "actionGroupInvocation": {
              "actionGroupName": "string",
              "apiName": "string",
              "id": "string",
              "verb": "string",
              "actionGroupInput": {
                  "{{<parameter>}}": {
                      "value": "string"
                  },
                  ...
              }
          },
          "agentKnowledgeBase": {
              "knowledgeBaseId": "string",
              "id": "string",
              "searchQuery": {
                  "value": "string"
              }
          },
          "agentFinalResponse": {
              "responseText": "string",
              "citations": {
                  "generatedResponseParts": [
                      {
                          "text": "string",
                          "references": [
                              {"sourceId": "string"},
                              ...
                          ]
                      },
                      ...
                  ]
              }
          },
      }
  }
  ```
+ If you defined the action group with function details, the response must be in the following format:

  ```
  {
      "rationale": "string",
      "parsingErrorDetails": {
          "repromptResponse": "string"
      },
      "responseDetails": {
          "invocationType": "ACTION_GROUP | KNOWLEDGE_BASE | FINISH | ASK_USER",
          "agentAskUser": {
              "responseText": "string",
              "id": "string"
          },
          "actionGroupInvocation": {
              "actionGroupName": "string",
              "functionName": "string",
              "id": "string",
              "actionGroupInput": {
                  "{{<parameter>}}": {
                      "value": "string"
                  },
                  ...
              }
          },
          "agentKnowledgeBase": {
              "knowledgeBaseId": "string",
              "id": "string",
              "searchQuery": {
                  "value": "string"
              }
          },
          "agentFinalResponse": {
              "responseText": "string",
              "citations": {
                  "generatedResponseParts": [
                      {
                          "text": "string",
                          "references": [
                              {"sourceId": "string"},
                              ...
                          ]
                      },
                      ...
                  ]
              }
          },
      }
  }
  ```

The `orchestrationParsedResponse` contains the following fields:
+ `rationale` – The reasoning for what to do next, based on the foundation model output. You can define the function to parse from the model output.
+ `parsingErrorDetails` – Contains the `repromptResponse`, which is the message to reprompt the model to update its raw response when the model response can't be parsed. You can define the function to manipulate how to reprompt the model.
+ `responseDetails` – Contains the details for how to handle the output of the foundation model. Contains an `invocationType`, which is the next step for the agent to take, and a second field that should match the `invocationType`. The following objects are possible.
  + `agentAskUser` – Compatible with the `ASK_USER` invocation type. This invocation type ends the orchestration step. Contains the `responseText` to ask the user for more information. You can define your function to manipulate this field.
  + `actionGroupInvocation` – Compatible with the `ACTION_GROUP` invocation type. You can define your Lambda function to determine action groups to invoke and parameters to pass. Contains the following fields:
    + `actionGroupName` – The action group to invoke.
    + The following fields are required if you defined the action group with an OpenAPI schema:
      + `apiName` – The name of the API operation to invoke in the action group.
      + `verb` – The method of the API operation to use.
    + The following field is required if you defined the action group with function details:
      + `functionName` – The name of the function to invoke in the action group.
    + `actionGroupInput` – Contains parameters to specify in the API operation request.
  + `agentKnowledgeBase` – Compatible with the `KNOWLEDGE_BASE` invocation type. You can define your function to determine how to query knowledge bases. Contains the following fields:
    + `knowledgeBaseId` – The unique identifier of the knowledge base.
    + `searchQuery` – Contains the query to send to the knowledge base in the `value` field.
  + `agentFinalResponse` – Compatible with the `FINISH` invocation type. This invocation type ends the orchestration step. Contains the response to the user in the `responseText` field and citations for the response in the `citations` object.

------
#### [ knowledgeBaseResponseGenerationParsedResponse ]

```
{ 
   "generatedResponse": {
        "generatedResponseParts": [
            {
                "text": "string",
                "references": [
                    { "sourceId": "string" },
                    ...
                ]
            },
            ...
        ]
    }
}
```

The `knowledgeBaseResponseGenerationParsedResponse` contains the `generatedResponse` from querying the knowledge base and references for the data sources.

------
#### [ postProcessingParsedResponse ]

```
{
    "responseText": "string",
    "citations": {
        "generatedResponseParts": [
            {
                "text": "string",
                "references": [
                    { "sourceId": "string" },
                    ...
                ]
            },
            ...
        ]
    }
}
```

The `postProcessingParsedResponse` contains the following fields:
+ `responseText` – The response to return to the end user. You can define the function to format the response.
+ `citations` – Contains a list of citations for the response. Each citation shows the cited text and its references.

------

## Parser Lambda examples
<a name="lambda-parser-example"></a>

To see example parser Lambda function input events and responses, select from the following tabs.

------
#### [ Pre-processing ]

**Example input event**

```
{
    "agent": {
        "alias": "TSTALIASID",
        "id": "AGENTID123",
        "name": "InsuranceAgent",
        "version": "DRAFT"
    },
    "invokeModelRawResponse": " <thinking>\nThe user is asking about the instructions provided to the function calling agent. This input is trying to gather information about what functions/API's or instructions our function calling agent has access to. Based on the categories provided, this input belongs in Category B.\n</thinking>\n\n<category>B</category>",
    "messageVersion": "1.0",
    "overrideType": "OUTPUT_PARSER",
    "promptType": "PRE_PROCESSING"
}
```

**Example response**

```
{
  "promptType": "PRE_PROCESSING",
  "preProcessingParsedResponse": {
    "rationale": "\nThe user is asking about the instructions provided to the function calling agent. This input is trying to gather information about what functions/API's or instructions our function calling agent has access to. Based on the categories provided, this input belongs in Category B.\n",
    "isValidInput": false
  }
}
```

------
#### [ Orchestration ]

**Example input event**

```
{
    "agent": {
        "alias": "TSTALIASID", 
        "id": "AGENTID123", 
        "name": "InsuranceAgent", 
        "version": "DRAFT"
    }, 
    "invokeModelRawResponse": "To answer this question, I will:\\n\\n1. Call the GET::x_amz_knowledgebase_KBID123456::Search function to search for a phone number to call.\\n\\nI have checked that I have access to the GET::x_amz_knowledgebase_KBID23456::Search function.\\n\\n</scratchpad>\\n\\n<function_call>GET::x_amz_knowledgebase_KBID123456::Search(searchQuery=\"What is the phone number I can call?\)",
    "messageVersion": "1.0",
    "overrideType": "OUTPUT_PARSER",
    "promptType": "ORCHESTRATION"
}
```

**Example response**

```
{
    "promptType": "ORCHESTRATION",
    "orchestrationParsedResponse": {
        "rationale": "To answer this question, I will:\\n\\n1. Call the GET::x_amz_knowledgebase_KBID123456::Search function to search for a phone number to call Farmers.\\n\\nI have checked that I have access to the GET::x_amz_knowledgebase_KBID123456::Search function.",
        "responseDetails": {
            "invocationType": "KNOWLEDGE_BASE",
            "agentKnowledgeBase": {
                "searchQuery": {
                    "value": "What is the phone number I can call?"
                },
                "knowledgeBaseId": "KBID123456"
            }
        }
    }
}
```

------
#### [ Knowledge base response generation ]

**Example input event**

```
{
    "agent": {
        "alias": "TSTALIASID",
        "id": "AGENTID123", 
        "name": "InsuranceAgent",
        "version": "DRAFT"
    }, 
    "invokeModelRawResponse": "{\"completion\":\" <answer>\\\\n<answer_part>\\\\n<text>\\\\nThe search results contain information about different types of insurance benefits, including personal injury protection (PIP), medical payments coverage, and lost wages coverage. PIP typically covers reasonable medical expenses for injuries caused by an accident, as well as income continuation, child care, loss of services, and funerals. Medical payments coverage provides payment for medical treatment resulting from a car accident. Who pays lost wages due to injuries depends on the laws in your state and the coverage purchased.\\\\n</text>\\\\n<sources>\\\\n<source>1234567-1234-1234-1234-123456789abc</source>\\\\n<source>2345678-2345-2345-2345-23456789abcd</source>\\\\n<source>3456789-3456-3456-3456-3456789abcde</source>\\\\n</sources>\\\\n</answer_part>\\\\n</answer>\",\"stop_reason\":\"stop_sequence\",\"stop\":\"\\\\n\\\\nHuman:\"}",
    "messageVersion": "1.0",
    "overrideType": "OUTPUT_PARSER",
    "promptType": "KNOWLEDGE_BASE_RESPONSE_GENERATION"
}
```

**Example response**

```
{
    "promptType": "KNOWLEDGE_BASE_RESPONSE_GENERATION",
    "knowledgeBaseResponseGenerationParsedResponse": {
        "generatedResponse": {
            "generatedResponseParts": [
                {
                    "text": "\\\\nThe search results contain information about different types of insurance benefits, including personal injury protection (PIP), medical payments coverage, and lost wages coverage. PIP typically covers reasonable medical expenses for injuries caused by an accident, as well as income continuation, child care, loss of services, and funerals. Medical payments coverage provides payment for medical treatment resulting from a car accident. Who pays lost wages due to injuries depends on the laws in your state and the coverage purchased.\\\\n",
                    "references": [
                        {"sourceId": "1234567-1234-1234-1234-123456789abc"},
                        {"sourceId": "2345678-2345-2345-2345-23456789abcd"},
                        {"sourceId": "3456789-3456-3456-3456-3456789abcde"}
                    ]
                }
            ]
        }
    }
}
```

------
#### [ Post-processing ]

**Example input event**

```
{
    "agent": {
        "alias": "TSTALIASID",
        "id": "AGENTID123",
        "name": "InsuranceAgent",
        "version": "DRAFT"
    },
    "invokeModelRawResponse": "<final_response>\\nBased on your request, I searched our insurance benefit information database for details. The search results indicate that insurance policies may cover different types of benefits, depending on the policy and state laws. Specifically, the results discussed personal injury protection (PIP) coverage, which typically covers medical expenses for insured individuals injured in an accident (cited sources: 1234567-1234-1234-1234-123456789abc, 2345678-2345-2345-2345-23456789abcd). PIP may pay for costs like medical care, lost income replacement, childcare expenses, and funeral costs. Medical payments coverage was also mentioned as another option that similarly covers medical treatment costs for the policyholder and others injured in a vehicle accident involving the insured vehicle. The search results further noted that whether lost wages are covered depends on the state and coverage purchased. Please let me know if you need any clarification or have additional questions.\\n</final_response>",
    "messageVersion": "1.0",
    "overrideType": "OUTPUT_PARSER",
    "promptType": "POST_PROCESSING"
}
```

**Example response**

```
{
    "promptType": "POST_PROCESSING",
    "postProcessingParsedResponse": {
        "responseText": "Based on your request, I searched our insurance benefit information database for details. The search results indicate that insurance policies may cover different types of benefits, depending on the policy and state laws. Specifically, the results discussed personal injury protection (PIP) coverage, which typically covers medical expenses for insured individuals injured in an accident (cited sources: 24c62d8c-3e39-4ca1-9470-a91d641fe050, 197815ef-8798-4cb1-8aa5-35f5d6b28365). PIP may pay for costs like medical care, lost income replacement, childcare expenses, and funeral costs. Medical payments coverage was also mentioned as another option that similarly covers medical treatment costs for the policyholder and others injured in a vehicle accident involving the insured vehicle. The search results further noted that whether lost wages are covered depends on the state and coverage purchased. Please let me know if you need any clarification or have additional questions."
    }
}
```

------
#### [ Memory summarization ]

**Example input event**

```
{
    "messageVersion": "1.0",
    "promptType": "MEMORY_SUMMARIZATION",
    "invokeModelRawResponse": "<summary> <topic name="user goals">User initiated the conversation with a greeting.</topic> </summary>"
}
```

**Example response**

```
{"topicwiseSummaries": [
    {
        "topic": "TopicName1",
        "summary": "My Topic 1 Summary"
    }
    ...
]
    
}
```

------

To see example parser Lambda functions, expand the section for the prompt template examples that you want to see. The `lambda_handler` function returns the parsed response to the agent.

### Pre-processing
<a name="parser-preprocessing"></a>

The following example shows a pre-processing parser Lambda function written in Python.

```
import json
import re
import logging

PRE_PROCESSING_RATIONALE_REGEX = "&lt;thinking&gt;(.*?)&lt;/thinking&gt;"
PREPROCESSING_CATEGORY_REGEX = "&lt;category&gt;(.*?)&lt;/category&gt;"
PREPROCESSING_PROMPT_TYPE = "PRE_PROCESSING"
PRE_PROCESSING_RATIONALE_PATTERN = re.compile(PRE_PROCESSING_RATIONALE_REGEX, re.DOTALL)
PREPROCESSING_CATEGORY_PATTERN = re.compile(PREPROCESSING_CATEGORY_REGEX, re.DOTALL)

logger = logging.getLogger()

# This parser lambda is an example of how to parse the LLM output for the default PreProcessing prompt
def lambda_handler(event, context):
    
    print("Lambda input: " + str(event))
    logger.info("Lambda input: " + str(event))
    
    prompt_type = event["promptType"]
    
    # Sanitize LLM response
    model_response = sanitize_response(event['invokeModelRawResponse'])
    
    if event["promptType"] == PREPROCESSING_PROMPT_TYPE:
        return parse_pre_processing(model_response)

def parse_pre_processing(model_response):
    
    category_matches = re.finditer(PREPROCESSING_CATEGORY_PATTERN, model_response)
    rationale_matches = re.finditer(PRE_PROCESSING_RATIONALE_PATTERN, model_response)

    category = next((match.group(1) for match in category_matches), None)
    rationale = next((match.group(1) for match in rationale_matches), None)

    return {
        "promptType": "PRE_PROCESSING",
        "preProcessingParsedResponse": {
            "rationale": rationale,
            "isValidInput": get_is_valid_input(category)
            }
        }

def sanitize_response(text):
    pattern = r"(\\n*)"
    text = re.sub(pattern, r"\n", text)
    return text
    
def get_is_valid_input(category):
    if category is not None and category.strip().upper() == "D" or category.strip().upper() == "E":
        return True
    return False
```

### Orchestration
<a name="parser-orchestration"></a>

The following examples shows an orchestration parser Lambda function written in Python.

The example code differs depending on whether your action group was defined with an OpenAPI schema or with function details:

1. To see examples for an action group defined with an OpenAPI schema, select the tab corresponding to the model that you want to see examples for.

------
#### [ Anthropic Claude 2.0 ]

   ```
   import json
   import re
   import logging
    
    
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_call>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
    
   RATIONALE_VALUE_REGEX_LIST = [
       "<scratchpad>(.*?)(</scratchpad>)",
       "(.*?)(</scratchpad>)",
       "(<scratchpad>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
    
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
    
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_call>"
    
   ASK_USER_FUNCTION_CALL_REGEX = r"(<function_call>user::askuser)(.*)\)"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
    
   ASK_USER_FUNCTION_PARAMETER_REGEX = r"(?<=askuser=\")(.*?)\""  
   ASK_USER_FUNCTION_PARAMETER_PATTERN = re.compile(ASK_USER_FUNCTION_PARAMETER_REGEX, re.DOTALL)
    
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
    
   FUNCTION_CALL_REGEX = r"<function_call>(\w+)::(\w+)::(.+)\((.+)\)"
    
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"  
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
    
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the argument askuser for user::askuser function call. Please try again with the correct argument added"
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <function_call>user::askuser(askuser=\"$ASK_USER_INPUT\")</function_call>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = 'The function call format is incorrect. The format for function calls must be: <function_call>$FUNCTION_NAME($FUNCTION_ARGUMENT_NAME=""$FUNCTION_ARGUMENT_NAME"")</function_call>.'
   
   logger = logging.getLogger()
    
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
       
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
       
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
       
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
       
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
           
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
           
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
          
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
       
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
               
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
           
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
           
       raise Exception("unrecognized prompt type")
    
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
       
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next((pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)), None)
       
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
           
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next((pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
           
           return rationale
       
       return None
       
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
    
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
           
       return None, None
     
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
       
   def parse_generated_response(sanitized_llm_response):
       results = []
       
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
           
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
           
           text = text_match.group(1).strip()        
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
       
       final_response = " ".join([r[0] for r in results])
       
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text, 
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
           
       return final_response, generated_response_parts
   
       
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
    
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
       
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               ask_user = ask_user_matcher.group(2).strip()
               ask_user_question_matcher = ASK_USER_FUNCTION_PARAMETER_PATTERN.search(ask_user)
               if ask_user_question_matcher:
                   return ask_user_question_matcher.group(1).strip()
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
           
       return None
    
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX, sanitized_response)
       if not match:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
       
       verb, resource_name, function = match.group(1), match.group(2), match.group(3)
       
       parameters = {}
       for arg in match.group(4).split(","):
           key, value = arg.split("=")
           parameters[key.strip()] = {'value': value.strip('" ')}
           
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
           
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
           
           return parsed_response
       
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
           "verb": verb, 
           "actionGroupName": resource_name,
           "apiName": function,
           "actionGroupInput": parameters
       }
       
       return parsed_response
       
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
       
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 2.1 ]

   ```
   import logging
   import re
   import xml.etree.ElementTree as ET
   
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_calls>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
   
   RATIONALE_VALUE_REGEX_LIST = [
       "<scratchpad>(.*?)(</scratchpad>)",
       "(.*?)(</scratchpad>)",
       "(<scratchpad>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
   
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
   
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_calls>"
   
   ASK_USER_FUNCTION_CALL_REGEX = r"<tool_name>user::askuser</tool_name>"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
   
   ASK_USER_TOOL_NAME_REGEX = r"<tool_name>((.|\n)*?)</tool_name>"
   ASK_USER_TOOL_NAME_PATTERN = re.compile(ASK_USER_TOOL_NAME_REGEX, re.DOTALL)
   
   TOOL_PARAMETERS_REGEX = r"<parameters>((.|\n)*?)</parameters>"
   TOOL_PARAMETERS_PATTERN = re.compile(TOOL_PARAMETERS_REGEX, re.DOTALL)
   
   ASK_USER_TOOL_PARAMETER_REGEX = r"<question>((.|\n)*?)</question>"
   ASK_USER_TOOL_PARAMETER_PATTERN = re.compile(ASK_USER_TOOL_PARAMETER_REGEX, re.DOTALL)
   
   
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
   
   FUNCTION_CALL_REGEX = r"(?<=<function_calls>)(.*)"
   
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
   
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user::askuser function call. Please try again with the correct argument added."
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <invoke> <tool_name>user::askuser</tool_name><parameters><question>$QUESTION</question></parameters></invoke>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls must be: <invoke> <tool_name>$TOOL_NAME</tool_name> <parameters> <$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>...</parameters></invoke>."
   
   logger = logging.getLogger()
   
   
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
   
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
   
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
   
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
   
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
   
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
   
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
   
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
   
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
   
       raise Exception("unrecognized prompt type")
   
   
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
   
   
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next(
           (pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)),
           None)
   
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
   
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next(
               (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
   
           return rationale
   
       return None
   
   
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
   
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
   
       return None, None
   
   
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
   
   
   def parse_generated_response(sanitized_llm_response):
       results = []
   
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
   
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
   
           text = text_match.group(1).strip()
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
   
       final_response = " ".join([r[0] for r in results])
   
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text,
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
   
       return final_response, generated_response_parts
   
   
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
   
   
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
   
   
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_llm_response)
               params = parameters_matches.group(1).strip()
               ask_user_question_matcher = ASK_USER_TOOL_PARAMETER_PATTERN.search(params)
               if ask_user_question_matcher:
                   ask_user_question = ask_user_question_matcher.group(1)
                   return ask_user_question
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
   
       return None
   
   
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX, sanitized_response)
       if not match:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
   
       tool_name_matches = ASK_USER_TOOL_NAME_PATTERN.search(sanitized_response)
       tool_name = tool_name_matches.group(1)
       parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_response)
       params = parameters_matches.group(1).strip()
   
       action_split = tool_name.split('::')
       verb = action_split[0].strip()
       resource_name = action_split[1].strip()
       function = action_split[2].strip()
   
       xml_tree = ET.ElementTree(ET.fromstring("<parameters>{}</parameters>".format(params)))
       parameters = {}
       for elem in xml_tree.iter():
           if elem.text:
               parameters[elem.tag] = {'value': elem.text.strip('" ')}
   
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
   
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
   
           return parsed_response
   
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
           "verb": verb,
           "actionGroupName": resource_name,
           "apiName": function,
           "actionGroupInput": parameters
       }
   
       return parsed_response
   
   
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
   
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 3 ]

   ```
   import logging
   import re
   import xml.etree.ElementTree as ET
    
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_calls>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
    
   RATIONALE_VALUE_REGEX_LIST = [
       "<thinking>(.*?)(</thinking>)",
       "(.*?)(</thinking>)",
       "(<thinking>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
    
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
    
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_calls>"
    
   ASK_USER_FUNCTION_CALL_REGEX = r"<tool_name>user::askuser</tool_name>"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_NAME_REGEX = r"<tool_name>((.|\n)*?)</tool_name>"
   ASK_USER_TOOL_NAME_PATTERN = re.compile(ASK_USER_TOOL_NAME_REGEX, re.DOTALL)
    
   TOOL_PARAMETERS_REGEX = r"<parameters>((.|\n)*?)</parameters>"
   TOOL_PARAMETERS_PATTERN = re.compile(TOOL_PARAMETERS_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_PARAMETER_REGEX = r"<question>((.|\n)*?)</question>"
   ASK_USER_TOOL_PARAMETER_PATTERN = re.compile(ASK_USER_TOOL_PARAMETER_REGEX, re.DOTALL)
    
    
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
    
   FUNCTION_CALL_REGEX = r"(?<=<function_calls>)(.*)"
    
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
    
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user::askuser function call. Please try again with the correct argument added."
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <invoke> <tool_name>user::askuser</tool_name><parameters><question>$QUESTION</question></parameters></invoke>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls must be: <invoke> <tool_name>$TOOL_NAME</tool_name> <parameters> <$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>...</parameters></invoke>."
    
   logger = logging.getLogger()
    
    
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
    
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
    
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
    
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
    
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
    
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
    
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
    
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
    
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
    
       raise Exception("unrecognized prompt type")
    
    
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
    
    
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next(
           (pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)),
           None)
    
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
    
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next(
               (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
    
           return rationale
    
       return None
    
    
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
    
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
    
       return None, None
    
    
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
    
    
   def parse_generated_response(sanitized_llm_response):
       results = []
    
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
    
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
    
           text = text_match.group(1).strip()
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
    
       final_response = " ".join([r[0] for r in results])
    
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text,
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
    
       return final_response, generated_response_parts
    
    
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
    
    
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
    
    
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_llm_response)
               params = parameters_matches.group(1).strip()
               ask_user_question_matcher = ASK_USER_TOOL_PARAMETER_PATTERN.search(params)
               if ask_user_question_matcher:
                   ask_user_question = ask_user_question_matcher.group(1)
                   return ask_user_question
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
    
       return None
    
    
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX, sanitized_response)
       if not match:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
    
       tool_name_matches = ASK_USER_TOOL_NAME_PATTERN.search(sanitized_response)
       tool_name = tool_name_matches.group(1)
       parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_response)
       params = parameters_matches.group(1).strip()
    
       action_split = tool_name.split('::')
       verb = action_split[0].strip()
       resource_name = action_split[1].strip()
       function = action_split[2].strip()
    
       xml_tree = ET.ElementTree(ET.fromstring("<parameters>{}</parameters>".format(params)))
       parameters = {}
       for elem in xml_tree.iter():
           if elem.text:
               parameters[elem.tag] = {'value': elem.text.strip('" ')}
    
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
    
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
    
           return parsed_response
    
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
           "verb": verb,
           "actionGroupName": resource_name,
           "apiName": function,
           "actionGroupInput": parameters
       }
    
       return parsed_response
    
    
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
    
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 3.5 ]

   ```
   import json
   import logging
   import re
   from collections import defaultdict
   
   RATIONALE_VALUE_REGEX_LIST = [
     "<thinking>(.*?)(</thinking>)",
     "(.*?)(</thinking>)",
     "(<thinking>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in
                               RATIONALE_VALUE_REGEX_LIST]
   
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
   
   ANSWER_TAG = "<answer>"
   ASK_USER = "user__askuser"
   
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
   
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX,
                                              re.DOTALL)
   
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user__askuser function call. Please try again with the correct argument added."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The tool name format is incorrect. The format for the tool name must be: 'httpVerb__actionGroupName__apiName."
   logger = logging.getLogger()
   
   
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
     logger.setLevel("INFO")
     logger.info("Lambda input: " + str(event))
   
     # Sanitize LLM response
     response = load_response(event['invokeModelRawResponse'])
   
     stop_reason = response["stop_reason"]
     content = response["content"]
     content_by_type = get_content_by_type(content)
   
     # Parse LLM response for any rationale
     rationale = parse_rationale(content_by_type)
   
     # Construct response fields common to all invocation types
     parsed_response = {
       'promptType': "ORCHESTRATION",
       'orchestrationParsedResponse': {
         'rationale': rationale
       }
     }
   
     match stop_reason:
       case 'tool_use':
         # Check if there is an ask user
         try:
           ask_user = parse_ask_user(content_by_type)
           if ask_user:
             parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'ASK_USER',
               'agentAskUser': {
                 'responseText': ask_user,
                 'id': content_by_type['tool_use'][0]['id']
               },
   
             }
   
             logger.info("Ask user parsed response: " + str(parsed_response))
             return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
         # Check if there is an agent action
         try:
           parsed_response = parse_function_call(content_by_type, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       case 'end_turn' | 'stop_sequence':
         # Check if there is a final answer
         try:
           if content_by_type["text"]:
             text_contents = content_by_type["text"]
             for text_content in text_contents:
               final_answer, generated_response_parts = parse_answer(text_content)
               if final_answer:
                 parsed_response['orchestrationParsedResponse'][
                   'responseDetails'] = {
                   'invocationType': 'FINISH',
                   'agentFinalResponse': {
                     'responseText': final_answer
                   }
                 }
   
               if generated_response_parts:
                 parsed_response['orchestrationParsedResponse']['responseDetails'][
                   'agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
                 }
   
               logger.info("Final answer parsed response: " + str(parsed_response))
               return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
       case _:
         addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
         logger.info(parsed_response)
         return parsed_response
   
   
   def load_response(text):
     raw_text = r'{}'.format(text)
     json_text = json.loads(raw_text)
     return json_text
   
   
   def get_content_by_type(content):
     content_by_type = defaultdict(list)
     for content_value in content:
       content_by_type[content_value["type"]].append(content_value)
     return content_by_type
   
   
   def parse_rationale(content_by_type):
     if "text" in content_by_type:
       rationale = content_by_type["text"][0]["text"]
       if rationale is not None:
         rationale_matcher = next(
             (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if
              pattern.search(rationale)),
             None)
         if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
       return rationale
     return None
   
   
   def parse_answer(response):
     if has_generated_response(response["text"].strip()):
       return parse_generated_response(response)
   
     answer_match = ANSWER_PATTERN.search(response["text"].strip())
     if answer_match:
       return answer_match.group(0).strip(), None
   
     return None, None
   
   
   def parse_generated_response(response):
     results = []
   
     for match in ANSWER_PART_PATTERN.finditer(response):
       part = match.group(1).strip()
   
       text_match = ANSWER_TEXT_PART_PATTERN.search(part)
       if not text_match:
         raise ValueError("Could not parse generated response")
   
       text = text_match.group(1).strip()
       references = parse_references(part)
       results.append((text, references))
   
     final_response = " ".join([r[0] for r in results])
   
     generated_response_parts = []
     for text, references in results:
       generatedResponsePart = {
         'text': text,
         'references': references
       }
       generated_response_parts.append(generatedResponsePart)
   
     return final_response, generated_response_parts
   
   
   def has_generated_response(raw_response):
     return ANSWER_PART_PATTERN.search(raw_response) is not None
   
   
   def parse_references(answer_part):
     references = []
     for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
       reference = match.group(1).strip()
       references.append({'sourceId': reference})
     return references
   
   
   def parse_ask_user(content_by_type):
     try:
       if content_by_type["tool_use"][0]["name"] == ASK_USER:
         ask_user_question = content_by_type["tool_use"][0]["input"]["question"]
         if not ask_user_question:
           raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
         return ask_user_question
     except ValueError as ex:
       raise ex
     return None
   
   
   def parse_function_call(content_by_type, parsed_response):
     try:
       content = content_by_type["tool_use"][0]
       tool_name = content["name"]
   
       action_split = tool_name.split('__')
       verb = action_split[0].strip()
       resource_name = action_split[1].strip()
       function = action_split[2].strip()
     except ValueError as ex:
       raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
   
     parameters = {}
     for param, value in content["input"].items():
       parameters[param] = {'value': value}
   
     parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
   
     # Function calls can either invoke an action group or a knowledge base.
     # Mapping to the correct variable names accordingly
     if resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
       parsed_response['orchestrationParsedResponse']['responseDetails'][
         'invocationType'] = 'KNOWLEDGE_BASE'
       parsed_response['orchestrationParsedResponse']['responseDetails'][
         'agentKnowledgeBase'] = {
         'searchQuery': parameters['searchQuery'],
         'knowledgeBaseId': resource_name.replace(
             KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, ''),
         'id': content["id"]
       }
       return parsed_response
     parsed_response['orchestrationParsedResponse']['responseDetails'][
       'invocationType'] = 'ACTION_GROUP'
     parsed_response['orchestrationParsedResponse']['responseDetails'][
       'actionGroupInvocation'] = {
       "verb": verb,
       "actionGroupName": resource_name,
       "apiName": function,
       "actionGroupInput": parameters,
       "id": content["id"]
     }
     return parsed_response
   
   
   def addRepromptResponse(parsed_response, error):
     error_message = str(error)
     logger.warn(error_message)
   
     parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
       'repromptResponse': error_message
     }
   ```

------

1. To see examples for an action group defined with function details, select the tab corresponding to the model that you want to see examples for.

------
#### [ Anthropic Claude 2.0 ]

   ```
   import json
   import re
   import logging
    
    
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_call>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
    
   RATIONALE_VALUE_REGEX_LIST = [
       "<scratchpad>(.*?)(</scratchpad>)",
       "(.*?)(</scratchpad>)",
       "(<scratchpad>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
    
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
    
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_call>"
    
   ASK_USER_FUNCTION_CALL_REGEX = r"(<function_call>user::askuser)(.*)\)"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
    
   ASK_USER_FUNCTION_PARAMETER_REGEX = r"(?<=askuser=\")(.*?)\""  
   ASK_USER_FUNCTION_PARAMETER_PATTERN = re.compile(ASK_USER_FUNCTION_PARAMETER_REGEX, re.DOTALL)
    
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
    
   FUNCTION_CALL_REGEX_API_SCHEMA = r"<function_call>(\w+)::(\w+)::(.+)\((.+)\)"
   FUNCTION_CALL_REGEX_FUNCTION_SCHEMA = r"<function_call>(\w+)::(.+)\((.+)\)"
    
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"  
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
    
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the argument askuser for user::askuser function call. Please try again with the correct argument added"
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <function_call>user::askuser(askuser=\"$ASK_USER_INPUT\")</function_call>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = 'The function call format is incorrect. The format for function calls must be: <function_call>$FUNCTION_NAME($FUNCTION_ARGUMENT_NAME=""$FUNCTION_ARGUMENT_NAME"")</function_call>.'
    
   logger = logging.getLogger()
   logger.setLevel("INFO")
    
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
       
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
       
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
       
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
       
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
           
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
           
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
          
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
       
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
               
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
           
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
           
       raise Exception("unrecognized prompt type")
    
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
       
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next((pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)), None)
       
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
           
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next((pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
           
           return rationale
       
       return None
       
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
    
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
           
       return None, None
     
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
       
   def parse_generated_response(sanitized_llm_response):
       results = []
       
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
           
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
           
           text = text_match.group(1).strip()        
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
       
       final_response = " ".join([r[0] for r in results])
       
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text, 
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
           
       return final_response, generated_response_parts
    
       
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
    
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
       
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               ask_user = ask_user_matcher.group(2).strip()
               ask_user_question_matcher = ASK_USER_FUNCTION_PARAMETER_PATTERN.search(ask_user)
               if ask_user_question_matcher:
                   return ask_user_question_matcher.group(1).strip()
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
           
       return None
    
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX_API_SCHEMA, sanitized_response)
       match_function_schema = re.search(FUNCTION_CALL_REGEX_FUNCTION_SCHEMA, sanitized_response)
       if not match and not match_function_schema:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
    
       if match:
           schema_type = 'API'
           verb, resource_name, function, param_arg = match.group(1), match.group(2), match.group(3), match.group(4)
       else:
           schema_type = 'FUNCTION'
           resource_name, function, param_arg = match_function_schema.group(1), match_function_schema.group(2), match_function_schema.group(3)
       
       parameters = {}
       for arg in param_arg.split(","):
           key, value = arg.split("=")
           parameters[key.strip()] = {'value': value.strip('" ')}
           
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
           
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if schema_type == 'API' and resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
           
           return parsed_response
       
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       
       if schema_type == 'API':
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "verb": verb, 
               "actionGroupName": resource_name,
               "apiName": function,
               "actionGroupInput": parameters
           }
       else:
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "actionGroupName": resource_name,
               "functionName": function,
               "actionGroupInput": parameters
           }
       
       return parsed_response
       
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
       
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 2.1 ]

   ```
   import logging
   import re
   import xml.etree.ElementTree as ET
    
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_calls>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
    
   RATIONALE_VALUE_REGEX_LIST = [
       "<scratchpad>(.*?)(</scratchpad>)",
       "(.*?)(</scratchpad>)",
       "(<scratchpad>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
    
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
    
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_calls>"
    
   ASK_USER_FUNCTION_CALL_REGEX = r"<tool_name>user::askuser</tool_name>"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_NAME_REGEX = r"<tool_name>((.|\n)*?)</tool_name>"
   ASK_USER_TOOL_NAME_PATTERN = re.compile(ASK_USER_TOOL_NAME_REGEX, re.DOTALL)
    
   TOOL_PARAMETERS_REGEX = r"<parameters>((.|\n)*?)</parameters>"
   TOOL_PARAMETERS_PATTERN = re.compile(TOOL_PARAMETERS_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_PARAMETER_REGEX = r"<question>((.|\n)*?)</question>"
   ASK_USER_TOOL_PARAMETER_PATTERN = re.compile(ASK_USER_TOOL_PARAMETER_REGEX, re.DOTALL)
    
    
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
    
   FUNCTION_CALL_REGEX = r"(?<=<function_calls>)(.*)"
    
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
    
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user::askuser function call. Please try again with the correct argument added."
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <invoke> <tool_name>user::askuser</tool_name><parameters><question>$QUESTION</question></parameters></invoke>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls must be: <invoke> <tool_name>$TOOL_NAME</tool_name> <parameters> <$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>...</parameters></invoke>."
    
   logger = logging.getLogger()
   logger.setLevel("INFO")
    
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
    
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
    
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
    
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
    
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
    
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
    
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
    
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
    
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
    
       raise Exception("unrecognized prompt type")
    
    
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
    
    
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next(
           (pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)),
           None)
    
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
    
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next(
               (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
    
           return rationale
    
       return None
    
    
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
    
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
    
       return None, None
    
    
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
    
    
   def parse_generated_response(sanitized_llm_response):
       results = []
    
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
    
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
    
           text = text_match.group(1).strip()
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
    
       final_response = " ".join([r[0] for r in results])
    
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text,
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
    
       return final_response, generated_response_parts
    
    
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
    
    
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
    
    
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_llm_response)
               params = parameters_matches.group(1).strip()
               ask_user_question_matcher = ASK_USER_TOOL_PARAMETER_PATTERN.search(params)
               if ask_user_question_matcher:
                   ask_user_question = ask_user_question_matcher.group(1)
                   return ask_user_question
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
    
       return None
    
    
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX, sanitized_response)
       if not match:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
    
       tool_name_matches = ASK_USER_TOOL_NAME_PATTERN.search(sanitized_response)
       tool_name = tool_name_matches.group(1)
       parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_response)
       params = parameters_matches.group(1).strip()
    
       action_split = tool_name.split('::')
       schema_type = 'FUNCTION' if len(action_split) == 2 else 'API'
    
       if schema_type == 'API':
           verb = action_split[0].strip()
           resource_name = action_split[1].strip()
           function = action_split[2].strip()
       else:
           resource_name = action_split[0].strip()
           function = action_split[1].strip()
    
       xml_tree = ET.ElementTree(ET.fromstring("<parameters>{}</parameters>".format(params)))
       parameters = {}
       for elem in xml_tree.iter():
           if elem.text:
               parameters[elem.tag] = {'value': elem.text.strip('" ')}
    
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
    
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if schema_type == 'API' and resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
    
           return parsed_response
    
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       if schema_type == 'API':
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "verb": verb,
               "actionGroupName": resource_name,
               "apiName": function,
               "actionGroupInput": parameters
           }
       else:
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "actionGroupName": resource_name,
               "functionName": function,
               "actionGroupInput": parameters
           }
    
       return parsed_response
    
    
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
    
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 3 ]

   ```
   import logging
   import re
   import xml.etree.ElementTree as ET
    
   RATIONALE_REGEX_LIST = [
       "(.*?)(<function_calls>)",
       "(.*?)(<answer>)"
   ]
   RATIONALE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_REGEX_LIST]
    
   RATIONALE_VALUE_REGEX_LIST = [
       "<thinking>(.*?)(</thinking>)",
       "(.*?)(</thinking>)",
       "(<thinking>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in RATIONALE_VALUE_REGEX_LIST]
    
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
    
   ANSWER_TAG = "<answer>"
   FUNCTION_CALL_TAG = "<function_calls>"
    
   ASK_USER_FUNCTION_CALL_REGEX = r"<tool_name>user::askuser</tool_name>"
   ASK_USER_FUNCTION_CALL_PATTERN = re.compile(ASK_USER_FUNCTION_CALL_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_NAME_REGEX = r"<tool_name>((.|\n)*?)</tool_name>"
   ASK_USER_TOOL_NAME_PATTERN = re.compile(ASK_USER_TOOL_NAME_REGEX, re.DOTALL)
    
   TOOL_PARAMETERS_REGEX = r"<parameters>((.|\n)*?)</parameters>"
   TOOL_PARAMETERS_PATTERN = re.compile(TOOL_PARAMETERS_REGEX, re.DOTALL)
    
   ASK_USER_TOOL_PARAMETER_REGEX = r"<question>((.|\n)*?)</question>"
   ASK_USER_TOOL_PARAMETER_PATTERN = re.compile(ASK_USER_TOOL_PARAMETER_REGEX, re.DOTALL)
    
    
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
    
   FUNCTION_CALL_REGEX = r"(?<=<function_calls>)(.*)"
    
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)
    
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user::askuser function call. Please try again with the correct argument added."
   ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls to the askuser function must be: <invoke> <tool_name>user::askuser</tool_name><parameters><question>$QUESTION</question></parameters></invoke>."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The function call format is incorrect. The format for function calls must be: <invoke> <tool_name>$TOOL_NAME</tool_name> <parameters> <$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>...</parameters></invoke>."
    
   logger = logging.getLogger()
    
    
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
       logger.info("Lambda input: " + str(event))
    
       # Sanitize LLM response
       sanitized_response = sanitize_response(event['invokeModelRawResponse'])
    
       # Parse LLM response for any rationale
       rationale = parse_rationale(sanitized_response)
    
       # Construct response fields common to all invocation types
       parsed_response = {
           'promptType': "ORCHESTRATION",
           'orchestrationParsedResponse': {
               'rationale': rationale
           }
       }
    
       # Check if there is a final answer
       try:
           final_answer, generated_response_parts = parse_answer(sanitized_response)
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       if final_answer:
           parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'FINISH',
               'agentFinalResponse': {
                   'responseText': final_answer
               }
           }
    
           if generated_response_parts:
               parsed_response['orchestrationParsedResponse']['responseDetails']['agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
               }
    
           logger.info("Final answer parsed response: " + str(parsed_response))
           return parsed_response
    
       # Check if there is an ask user
       try:
           ask_user = parse_ask_user(sanitized_response)
           if ask_user:
               parsed_response['orchestrationParsedResponse']['responseDetails'] = {
                   'invocationType': 'ASK_USER',
                   'agentAskUser': {
                       'responseText': ask_user
                   }
               }
    
               logger.info("Ask user parsed response: " + str(parsed_response))
               return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       # Check if there is an agent action
       try:
           parsed_response = parse_function_call(sanitized_response, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
       except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
    
       addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
       logger.info(parsed_response)
       return parsed_response
    
       raise Exception("unrecognized prompt type")
    
    
   def sanitize_response(text):
       pattern = r"(\\n*)"
       text = re.sub(pattern, r"\n", text)
       return text
    
    
   def parse_rationale(sanitized_response):
       # Checks for strings that are not required for orchestration
       rationale_matcher = next(
           (pattern.search(sanitized_response) for pattern in RATIONALE_PATTERNS if pattern.search(sanitized_response)),
           None)
    
       if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
    
           # Check if there is a formatted rationale that we can parse from the string
           rationale_value_matcher = next(
               (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if pattern.search(rationale)), None)
           if rationale_value_matcher:
               return rationale_value_matcher.group(1).strip()
    
           return rationale
    
       return None
    
    
   def parse_answer(sanitized_llm_response):
       if has_generated_response(sanitized_llm_response):
           return parse_generated_response(sanitized_llm_response)
    
       answer_match = ANSWER_PATTERN.search(sanitized_llm_response)
       if answer_match and is_answer(sanitized_llm_response):
           return answer_match.group(0).strip(), None
    
       return None, None
    
    
   def is_answer(llm_response):
       return llm_response.rfind(ANSWER_TAG) > llm_response.rfind(FUNCTION_CALL_TAG)
    
    
   def parse_generated_response(sanitized_llm_response):
       results = []
    
       for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
           part = match.group(1).strip()
    
           text_match = ANSWER_TEXT_PART_PATTERN.search(part)
           if not text_match:
               raise ValueError("Could not parse generated response")
    
           text = text_match.group(1).strip()
           references = parse_references(sanitized_llm_response, part)
           results.append((text, references))
    
       final_response = " ".join([r[0] for r in results])
    
       generated_response_parts = []
       for text, references in results:
           generatedResponsePart = {
               'text': text,
               'references': references
           }
           generated_response_parts.append(generatedResponsePart)
    
       return final_response, generated_response_parts
    
    
   def has_generated_response(raw_response):
       return ANSWER_PART_PATTERN.search(raw_response) is not None
    
    
   def parse_references(raw_response, answer_part):
       references = []
       for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
           reference = match.group(1).strip()
           references.append({'sourceId': reference})
       return references
    
    
   def parse_ask_user(sanitized_llm_response):
       ask_user_matcher = ASK_USER_FUNCTION_CALL_PATTERN.search(sanitized_llm_response)
       if ask_user_matcher:
           try:
               parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_llm_response)
               params = parameters_matches.group(1).strip()
               ask_user_question_matcher = ASK_USER_TOOL_PARAMETER_PATTERN.search(params)
               if ask_user_question_matcher:
                   ask_user_question = ask_user_question_matcher.group(1)
                   return ask_user_question
               raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
           except ValueError as ex:
               raise ex
           except Exception as ex:
               raise Exception(ASK_USER_FUNCTION_CALL_STRUCTURE_REMPROMPT_MESSAGE)
    
       return None
    
    
   def parse_function_call(sanitized_response, parsed_response):
       match = re.search(FUNCTION_CALL_REGEX, sanitized_response)
       if not match:
           raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
    
       tool_name_matches = ASK_USER_TOOL_NAME_PATTERN.search(sanitized_response)
       tool_name = tool_name_matches.group(1)
       parameters_matches = TOOL_PARAMETERS_PATTERN.search(sanitized_response)
       params = parameters_matches.group(1).strip()
    
       action_split = tool_name.split('::')
       schema_type = 'FUNCTION' if len(action_split) == 2 else 'API'
    
       if schema_type == 'API':
           verb = action_split[0].strip()
           resource_name = action_split[1].strip()
           function = action_split[2].strip()
       else:
           resource_name = action_split[0].strip()
           function = action_split[1].strip()
    
       xml_tree = ET.ElementTree(ET.fromstring("<parameters>{}</parameters>".format(params)))
       parameters = {}
       for elem in xml_tree.iter():
           if elem.text:
               parameters[elem.tag] = {'value': elem.text.strip('" ')}
    
       parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
    
       # Function calls can either invoke an action group or a knowledge base.
       # Mapping to the correct variable names accordingly
       if schema_type == 'API' and resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
           parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'KNOWLEDGE_BASE'
           parsed_response['orchestrationParsedResponse']['responseDetails']['agentKnowledgeBase'] = {
               'searchQuery': parameters['searchQuery'],
               'knowledgeBaseId': resource_name.replace(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, '')
           }
    
           return parsed_response
    
       parsed_response['orchestrationParsedResponse']['responseDetails']['invocationType'] = 'ACTION_GROUP'
       if schema_type == 'API':
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "verb": verb,
               "actionGroupName": resource_name,
               "apiName": function,
               "actionGroupInput": parameters
           }
       else:
           parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
               "actionGroupName": resource_name,
               "functionName": function,
               "actionGroupInput": parameters
           }
    
       return parsed_response
    
    
   def addRepromptResponse(parsed_response, error):
       error_message = str(error)
       logger.warn(error_message)
    
       parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
           'repromptResponse': error_message
       }
   ```

------
#### [ Anthropic Claude 3.5 ]

   ```
   import json
   import logging
   import re
   from collections import defaultdict
   
   RATIONALE_VALUE_REGEX_LIST = [
     "<thinking>(.*?)(</thinking>)",
     "(.*?)(</thinking>)",
     "(<thinking>)(.*?)"
   ]
   RATIONALE_VALUE_PATTERNS = [re.compile(regex, re.DOTALL) for regex in
                               RATIONALE_VALUE_REGEX_LIST]
   
   ANSWER_REGEX = r"(?<=<answer>)(.*)"
   ANSWER_PATTERN = re.compile(ANSWER_REGEX, re.DOTALL)
   
   ANSWER_TAG = "<answer>"
   ASK_USER = "user__askuser"
   
   KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX = "x_amz_knowledgebase_"
   
   ANSWER_PART_REGEX = "<answer_part\\s?>(.+?)</answer_part\\s?>"
   ANSWER_TEXT_PART_REGEX = "<text\\s?>(.+?)</text\\s?>"
   ANSWER_REFERENCE_PART_REGEX = "<source\\s?>(.+?)</source\\s?>"
   ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
   ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
   ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX,
                                              re.DOTALL)
   
   # You can provide messages to reprompt the LLM in case the LLM output is not in the expected format
   MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE = "Missing the parameter 'question' for user__askuser function call. Please try again with the correct argument added."
   FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE = "The tool name format is incorrect. The format for the tool name must be: 'httpVerb__actionGroupName__apiName."
   logger = logging.getLogger()
   
   
   # This parser lambda is an example of how to parse the LLM output for the default orchestration prompt
   def lambda_handler(event, context):
     logger.setLevel("INFO")
     logger.info("Lambda input: " + str(event))
   
     # Sanitize LLM response
     response = load_response(event['invokeModelRawResponse'])
   
     stop_reason = response["stop_reason"]
     content = response["content"]
     content_by_type = get_content_by_type(content)
   
     # Parse LLM response for any rationale
     rationale = parse_rationale(content_by_type)
   
     # Construct response fields common to all invocation types
     parsed_response = {
       'promptType': "ORCHESTRATION",
       'orchestrationParsedResponse': {
         'rationale': rationale
       }
     }
   
     match stop_reason:
       case 'tool_use':
         # Check if there is an ask user
         try:
           ask_user = parse_ask_user(content_by_type)
           if ask_user:
             parsed_response['orchestrationParsedResponse']['responseDetails'] = {
               'invocationType': 'ASK_USER',
               'agentAskUser': {
                 'responseText': ask_user,
                 'id': content_by_type['tool_use'][0]['id']
               },
   
             }
   
             logger.info("Ask user parsed response: " + str(parsed_response))
             return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
         # Check if there is an agent action
         try:
           parsed_response = parse_function_call(content_by_type, parsed_response)
           logger.info("Function call parsed response: " + str(parsed_response))
           return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
   
       case 'end_turn' | 'stop_sequence':
         # Check if there is a final answer
         try:
           if content_by_type["text"]:
             text_contents = content_by_type["text"]
             for text_content in text_contents:
               final_answer, generated_response_parts = parse_answer(text_content)
               if final_answer:
                 parsed_response['orchestrationParsedResponse'][
                   'responseDetails'] = {
                   'invocationType': 'FINISH',
                   'agentFinalResponse': {
                     'responseText': final_answer
                   }
                 }
   
               if generated_response_parts:
                 parsed_response['orchestrationParsedResponse']['responseDetails'][
                   'agentFinalResponse']['citations'] = {
                   'generatedResponseParts': generated_response_parts
                 }
   
               logger.info("Final answer parsed response: " + str(parsed_response))
               return parsed_response
         except ValueError as e:
           addRepromptResponse(parsed_response, e)
           return parsed_response
       case _:
         addRepromptResponse(parsed_response, 'Failed to parse the LLM output')
         logger.info(parsed_response)
         return parsed_response
   
   
   def load_response(text):
     raw_text = r'{}'.format(text)
     json_text = json.loads(raw_text)
     return json_text
   
   
   def get_content_by_type(content):
     content_by_type = defaultdict(list)
     for content_value in content:
       content_by_type[content_value["type"]].append(content_value)
     return content_by_type
   
   
   def parse_rationale(content_by_type):
     if "text" in content_by_type:
       rationale = content_by_type["text"][0]["text"]
       if rationale is not None:
         rationale_matcher = next(
             (pattern.search(rationale) for pattern in RATIONALE_VALUE_PATTERNS if
              pattern.search(rationale)),
             None)
         if rationale_matcher:
           rationale = rationale_matcher.group(1).strip()
       return rationale
     return None
   
   
   def parse_answer(response):
     if has_generated_response(response["text"].strip()):
       return parse_generated_response(response)
   
     answer_match = ANSWER_PATTERN.search(response["text"].strip())
     if answer_match:
       return answer_match.group(0).strip(), None
   
     return None, None
   
   
   def parse_generated_response(response):
     results = []
   
     for match in ANSWER_PART_PATTERN.finditer(response):
       part = match.group(1).strip()
   
       text_match = ANSWER_TEXT_PART_PATTERN.search(part)
       if not text_match:
         raise ValueError("Could not parse generated response")
   
       text = text_match.group(1).strip()
       references = parse_references(part)
       results.append((text, references))
   
     final_response = " ".join([r[0] for r in results])
   
     generated_response_parts = []
     for text, references in results:
       generatedResponsePart = {
         'text': text,
         'references': references
       }
       generated_response_parts.append(generatedResponsePart)
   
     return final_response, generated_response_parts
   
   
   def has_generated_response(raw_response):
     return ANSWER_PART_PATTERN.search(raw_response) is not None
   
   
   def parse_references(answer_part):
     references = []
     for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
       reference = match.group(1).strip()
       references.append({'sourceId': reference})
     return references
   
   
   def parse_ask_user(content_by_type):
     try:
       if content_by_type["tool_use"][0]["name"] == ASK_USER:
         ask_user_question = content_by_type["tool_use"][0]["input"]["question"]
         if not ask_user_question:
           raise ValueError(MISSING_API_INPUT_FOR_USER_REPROMPT_MESSAGE)
         return ask_user_question
     except ValueError as ex:
       raise ex
     return None
   
   
   def parse_function_call(content_by_type, parsed_response):
     try:
       content = content_by_type["tool_use"][0]
       tool_name = content["name"]
   
       action_split = tool_name.split('__')
   
       schema_type = 'FUNCTION' if len(action_split) == 2 else 'API'
       if schema_type == 'API':
         verb = action_split[0].strip()
         resource_name = action_split[1].strip()
         function = action_split[2].strip()
       else:
         resource_name = action_split[1].strip()
         function = action_split[2].strip()
   
     except ValueError as ex:
       raise ValueError(FUNCTION_CALL_STRUCTURE_REPROMPT_MESSAGE)
   
     parameters = {}
     for param, value in content["input"].items():
       parameters[param] = {'value': value}
   
     parsed_response['orchestrationParsedResponse']['responseDetails'] = {}
   
     # Function calls can either invoke an action group or a knowledge base.
     # Mapping to the correct variable names accordingly
     if schema_type == 'API' and resource_name.lower().startswith(KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX):
       parsed_response['orchestrationParsedResponse']['responseDetails'][
         'invocationType'] = 'KNOWLEDGE_BASE'
       parsed_response['orchestrationParsedResponse']['responseDetails'][
         'agentKnowledgeBase'] = {
         'searchQuery': parameters['searchQuery'],
         'knowledgeBaseId': resource_name.replace(
             KNOWLEDGE_STORE_SEARCH_ACTION_PREFIX, ''),
         'id': content["id"]
       }
       return parsed_response
     parsed_response['orchestrationParsedResponse']['responseDetails'][
       'invocationType'] = 'ACTION_GROUP'
     if schema_type == 'API':
       parsed_response['orchestrationParsedResponse']['responseDetails'][
         'actionGroupInvocation'] = {
         "verb": verb,
         "actionGroupName": resource_name,
         "apiName": function,
         "actionGroupInput": parameters,
         "id": content["id"]
       }
     else:
       parsed_response['orchestrationParsedResponse']['responseDetails']['actionGroupInvocation'] = {
         "actionGroupName": resource_name,
         "functionName": function,
         "actionGroupInput": parameters
        }
     return parsed_response
   
   
   def addRepromptResponse(parsed_response, error):
     error_message = str(error)
     logger.warn(error_message)
   
     parsed_response['orchestrationParsedResponse']['parsingErrorDetails'] = {
       'repromptResponse': error_message
     }
   ```

------

### Knowledge base response generation
<a name="parser-kb"></a>

The following example shows a knowledge base response generation parser Lambda function written in Python.

```
import json
import re
import logging
 
ANSWER_PART_REGEX = "&lt;answer_part\\s?>(.+?)&lt;/answer_part\\s?>"
ANSWER_TEXT_PART_REGEX = "&lt;text\\s?>(.+?)&lt;/text\\s?>"  
ANSWER_REFERENCE_PART_REGEX = "&lt;source\\s?>(.+?)&lt;/source\\s?>"
ANSWER_PART_PATTERN = re.compile(ANSWER_PART_REGEX, re.DOTALL)
ANSWER_TEXT_PART_PATTERN = re.compile(ANSWER_TEXT_PART_REGEX, re.DOTALL)
ANSWER_REFERENCE_PART_PATTERN = re.compile(ANSWER_REFERENCE_PART_REGEX, re.DOTALL)

logger = logging.getLogger()
 
# This parser lambda is an example of how to parse the LLM output for the default KB response generation prompt
def lambda_handler(event, context):
    logger.info("Lambda input: " + str(event))
    raw_response = event['invokeModelRawResponse']
    
    parsed_response = {
        'promptType': 'KNOWLEDGE_BASE_RESPONSE_GENERATION',
        'knowledgeBaseResponseGenerationParsedResponse': {
            'generatedResponse': parse_generated_response(raw_response)
        }
    }
    
    logger.info(parsed_response)
    return parsed_response
    
def parse_generated_response(sanitized_llm_response):
    results = []
    
    for match in ANSWER_PART_PATTERN.finditer(sanitized_llm_response):
        part = match.group(1).strip()
        
        text_match = ANSWER_TEXT_PART_PATTERN.search(part)
        if not text_match:
            raise ValueError("Could not parse generated response")
        
        text = text_match.group(1).strip()        
        references = parse_references(sanitized_llm_response, part)
        results.append((text, references))
    
    generated_response_parts = []
    for text, references in results:
        generatedResponsePart = {
            'text': text, 
            'references': references
        }
        generated_response_parts.append(generatedResponsePart)
        
    return {
        'generatedResponseParts': generated_response_parts
    }
    
def parse_references(raw_response, answer_part):
    references = []
    for match in ANSWER_REFERENCE_PART_PATTERN.finditer(answer_part):
        reference = match.group(1).strip()
        references.append({'sourceId': reference})
    return references
```

### Post-processing
<a name="parser-postprocessing"></a>

The following example shows a post-processing parser Lambda function written in Python.

```
import json
import re
import logging
 
FINAL_RESPONSE_REGEX = r"&lt;final_response>([\s\S]*?)&lt;/final_response>"
FINAL_RESPONSE_PATTERN = re.compile(FINAL_RESPONSE_REGEX, re.DOTALL)

logger = logging.getLogger()
 
# This parser lambda is an example of how to parse the LLM output for the default PostProcessing prompt
def lambda_handler(event, context):
    logger.info("Lambda input: " + str(event))
    raw_response = event['invokeModelRawResponse']
    
    parsed_response = {
        'promptType': 'POST_PROCESSING',
        'postProcessingParsedResponse': {}
    }
    
    matcher = FINAL_RESPONSE_PATTERN.search(raw_response)
    if not matcher:
        raise Exception("Could not parse raw LLM output")
    response_text = matcher.group(1).strip()
    
    parsed_response['postProcessingParsedResponse']['responseText'] = response_text
    
    logger.info(parsed_response)
    return parsed_response
```

### Memory summarization
<a name="parser-memory-summarization"></a>

The following example shows a memory summarization parser Lambda function written in Python.

```
import re
import logging

SUMMARY_TAG_PATTERN = r'<summary>(.*?)</summary>'
TOPIC_TAG_PATTERN = r'<topic name="(.+?)"\s*>(.+?)</topic>'
logger = logging.getLogger()

# This parser lambda is an example of how to parse the LLM output for the default LTM SUmmarization prompt
def lambda_handler(event, context):
    logger.info("Lambda input: " + str(event))
    
    # Sanitize LLM response
    model_response = sanitize_response(event['invokeModelRawResponse'])
    
    if event["promptType"] == "MEMORY_SUMMARIZATION":
        return format_response(parse_llm_response(model_response), event["promptType"])

def format_response(topic_summaries, prompt_type):
    return {
        "promptType": prompt_type,
        "memorySummarizationParsedResponse": {
            "topicwiseSummaries": topic_summaries
        }
    }
    
def parse_llm_response(output: str):
    # First extract content within summary tag
    summary_match = re.search(SUMMARY_TAG_PATTERN, output, re.DOTALL)
    if not summary_match:
        raise Exception("Error while parsing summarizer model output, no summary tag found!")
    
    summary_content = summary_match.group(1)
    topic_summaries = parse_topic_wise_summaries(summary_content)
        
    return topic_summaries

def parse_topic_wise_summaries(content):
    summaries = []
    # Then extract content within topic tag
    for match in re.finditer(TOPIC_TAG_PATTERN, content, re.DOTALL):
        topic_name = match.group(1)
        topic_summary = match.group(2).strip()
        summaries.append({
            'topic': topic_name,
            'summary': topic_summary
        })
    if not summaries:
        raise Exception("Error while parsing summarizer model output, no topics found!")
    return summaries

def sanitize_response(text):
    pattern = r"(\\n*)"
    text = re.sub(pattern, r"\n", text)
    return text
```