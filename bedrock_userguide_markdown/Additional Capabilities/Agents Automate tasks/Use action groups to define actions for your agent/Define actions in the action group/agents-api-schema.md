

# Define OpenAPI schemas for your agent's action groups in Amazon Bedrock
<a name="agents-api-schema"></a>

When you create an action group in Amazon Bedrock, you must define the parameters that the agent needs to invoke from the user. You can also define API operations that the agent can invoke using these parameters. To define the API operations, create an OpenAPI schema in JSON or YAML format. You can create OpenAPI schema files and upload them to Amazon Simple Storage Service (Amazon S3). Alternatively, you can use the OpenAPI text editor in the console, which will validate your schema. After you create an agent, you can use the text editor when you add an action group to the agent or edit an existing action group. For more information, see [Modify an agent](agents-edit.md).

The agent uses the schema to determine the API operation that it needs to invoke and the parameters that are required to make the API request. These details are then sent through a Lambda function that you define to carry out the action or returned in the response of the agent invocation.

**Note**  
Amazon Bedrock agents support a subset of the OpenAPI 3.0 specification. The following schema features are not supported:  
The `enum` field for restricting parameter values to a fixed set.
If you need to constrain parameter values, describe the allowed values in the parameter's `description` field instead.

For more information about API schemas, see the following resources:
+ For more details about OpenAPI schemas, see [OpenAPI specification](https://swagger.io/specification/) on the Swagger website.
+ For best practices in writing API schemas, see [Best practices in API design](https://swagger.io/resources/articles/best-practices-in-api-design/) on the Swagger website.

The following is the general format of an OpenAPI schema for an action group.

```
{
    "openapi": "3.0.0",
    "paths": {
        "/{{path}}": {
            "{{method}}": {
                "description": "{{string}}",
                "operationId": "{{string}}",
                "parameters": [ ... ],
                "requestBody": { ... },
                "responses": { ... },
                "x-requireConfirmation": ENABLED | DISABLED
           }
       }
    }
}
```

The following list describes fields in the OpenAPI schema
+ `openapi` – (Required) The version of OpenAPI that's being used. This value must be `"3.0.0"` for the action group to work.
+ `paths` – (Required) Contains relative paths to individual endpoints. Each path must begin with a forward slash (`/`).
+ `method` – (Required) Defines the method to use.
+ `x-requireConfirmation` – (Optional) Specifies if the user confirmation is required before invoking the action. Enable this field to request confirmation from the user before the action is invoked. Requesting user confirmation before invoking the action may safeguard your application from taking actions due to malicious prompt injections. By default, user confirmation is `DISABLED` if this field is not specified.

Minimally, each method requires the following fields:
+ `description` – A description of the API operation. Use this field to inform the agent when to call this API operation and what the operation does.
+ `operationId` – A unique string that identifies an operation in an API, like a function name. This is a required field for all new toolUse enabled models such as Anthropic Claude 3.5 Sonnet, Meta Llama, etc. Ensure that the identifier (Id) you provide is unique across all operations and follows simple alphanumeric pattern with only hyphens or underscores as separators.
+ `responses` – Contains properties that the agent returns in the API response. The agent uses the response properties to construct prompts, accurately process the results of an API call, and determine a correct set of steps for performing a task. The agent can use response values from one operation as inputs for subsequent steps in the orchestration.

The fields within the following two objects provide more information for your agent to effectively take advantage of your action group. For each field, set the value of the `required` field to `true` if required and to `false` if optional.
+ `parameters` – Contains information about parameters that can be included in the request.
+ `requestBody` – Contains the fields in the request body for the operation. Don't include this field for `GET` and `DELETE` methods.

To learn more about a structure, select from the following tabs.

------
#### [ responses ]

```
"responses": {
    "200": {
        "content": {
            "{{<media type>}}": {
                "schema": {
                    "properties": {
                        "{{<property>}}": {
                            "type": "{{string}}",
                            "description": "{{string}}"
                        },
                        ...
                    }
                }
            }
        },
    },
    ...
}
```

Each key in the `responses` object is a response code, which describes the status of the response. The response code maps to an object that contains the following information for the response:
+ `content` – (Required for each response) The content of the response.
+ {{<media type>}} – The format of the response body. For more information, see [Media types](https://swagger.io/docs/specification/media-types/) on the Swagger website.
+ `schema` – (Required for each media type) Defines the data type of the response body and its fields.
+ `properties` – (Required if there are `items` in the schema) Your agent uses properties that you define in the schema to determine the information it needs to return to the end user to fulfill a task. Each property contains the following fields:
  + `type` – (Required for each property) The data type of the response field.
  + `description` – (Optional) Describes the property. The agent can use this information to determine the information that it needs to return to the end user.

------
#### [ parameters ]

```
"parameters": [
    {
        "name": "{{string}}",
        "description": "{{string}}",
        "required": boolean,
        "schema": {
            ...
        }
    },
    ...
]
```

Your agent uses the following fields to determine the information it must get from the end user to perform the action group's requirements.
+ `name` – (Required) The name of the parameter.
+ `description` – (Required) A description of the parameter. Use this field to help the agent understand how to elicit this parameter from the agent user or determine that it already has that parameter value from prior actions or from the user’s request to the agent.
+ `required` – (Optional) Whether the parameter is required for the API request. Use this field to indicate to the agent whether this parameter is needed for every invocation or if it's optional.
+ `schema` – (Optional) The definition of input and output data types. For more information, see [Data Models (Schemas)](https://swagger.io/docs/specification/data-models/) on the Swagger website.

------
#### [ requestBody ]

Following is the general structure of a `requestBody` field:

```
"requestBody": {
    "required": boolean,
    "content": {
        "{{<media type>}}": {
            "schema": {
                "properties": {
                    "{{<property>}}": {
                        "type": "{{string}}",
                        "description": "{{string}}"
                    },
                    ...
                }
            }
        }
    }
}
```

The following list describes each field:
+ `required` – (Optional) Whether the request body is required for the API request.
+ `content` – (Required) The content of the request body.
+ {{<media type>}} – (Optional) The format of the request body. For more information, see [Media types](https://swagger.io/docs/specification/media-types/) on the Swagger website.
+ `schema` – (Optional) Defines the data type of the request body and its fields.
+ `properties` – (Optional) Your agent uses properties that you define in the schema to determine the information it must get from the end user to make the API request. Each property contains the following fields:
  + `type` – (Optional) The data type of the request field.
  + `description` – (Optional) Describes the property. The agent can use this information to determine the information it needs to return to the end user.

------

To learn how to add the OpenAPI schema you created while creating the action group, see [Add an action group to your agent in Amazon Bedrock](agents-action-add.md).

## Example API schemas
<a name="agents-api-schema-example"></a>

The following example provides a simple OpenAPI schema in YAML format that gets the weather for a given location in Celsius.

```
openapi: 3.0.0
info:
  title: GetWeather API
  version: 1.0.0
  description: gets weather
paths:
  /getWeather/{location}/:
    get:
      summary: gets weather in Celsius
      description: gets weather in Celsius
      operationId: getWeather
      parameters:
        - name: location
          in: path
          description: location name
          required: true
          schema:
            type: string
      responses:
        "200":
          description: weather in Celsius
          content:
            application/json:
              schema:
                type: string
```

The following example API schema defines a group of API operations that help handle insurance claims. Three APIs are defined as follows:
+ `getAllOpenClaims` – Your agent can use the `description` field to determine that it should call this API operation if a list of open claims is needed. The `properties` in the `responses` specify to return the ID and the policy holder and the status of the claim. The agent returns this information to the agent user or uses some or all of the response as input to subsequent API calls.
+ `identifyMissingDocuments` – Your agent can use the `description` field to determine that it should call this API operation if missing documents must be identified for an insurance claim. The `name`, `description`, and `required` fields tell the agent that it must elicit the unique identifier of the open claim from the customer. The `properties` in the `responses` specify to return the IDs of the open insurance claims. The agent returns this information to the end user or uses some or all of the response as input to subsequent API calls.
+ `sendReminders` – Your agent can use the `description` field to determine that it should call this API operation if there is a need to send reminders to the customer. For example, a reminder about pending documents that they have for open claims. The `properties` in the `requestBody` tell the agent that it must find the claim IDs and the pending documents. The `properties` in the `responses` specify to return an ID of the reminder and its status. The agent returns this information to the end user or uses some or all of the response as input to subsequent API calls.

```
{
    "openapi": "3.0.0",
    "info": {
        "title": "Insurance Claims Automation API",
        "version": "1.0.0",
        "description": "APIs for managing insurance claims by pulling a list of open claims, identifying outstanding paperwork for each claim, and sending reminders to policy holders."
    },
    "paths": {
        "/claims": {
            "get": {
                "summary": "Get a list of all open claims",
                "description": "Get the list of all open insurance claims. Return all the open claimIds.",
                "operationId": "getAllOpenClaims",
                "responses": {
                    "200": {
                        "description": "Gets the list of all open insurance claims for policy holders",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "claimId": {
                                                "type": "string",
                                                "description": "Unique ID of the claim."
                                            },
                                            "policyHolderId": {
                                                "type": "string",
                                                "description": "Unique ID of the policy holder who has filed the claim."
                                            },
                                            "claimStatus": {
                                                "type": "string",
                                                "description": "The status of the claim. Claim can be in Open or Closed state"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/claims/{claimId}/identify-missing-documents": {
            "get": {
                "summary": "Identify missing documents for a specific claim",
                "description": "Get the list of pending documents that need to be uploaded by policy holder before the claim can be processed. The API takes in only one claim id and returns the list of documents that are pending to be uploaded by policy holder for that claim. This API should be called for each claim id",
                "operationId": "identifyMissingDocuments",
                "parameters": [{
                    "name": "claimId",
                    "in": "path",
                    "description": "Unique ID of the open insurance claim",
                    "required": true,
                    "schema": {
                        "type": "string"
                    }
                }],
                "responses": {
                    "200": {
                        "description": "List of documents that are pending to be uploaded by policy holder for insurance claim",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "pendingDocuments": {
                                            "type": "string",
                                            "description": "The list of pending documents for the claim."
                                        }
                                    }
                                }
                            }
                        }

                    }
                }
            }
        },
        "/send-reminders": {
            "post": {
                "summary": "API to send reminder to the customer about pending documents for open claim",
                "description": "Send reminder to the customer about pending documents for open claim. The API takes in only one claim id and its pending documents at a time, sends the reminder and returns the tracking details for the reminder. This API should be called for each claim id you want to send reminders for.",
                "operationId": "sendReminders",
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "claimId": {
                                        "type": "string",
                                        "description": "Unique ID of open claims to send reminders for."
                                    },
                                    "pendingDocuments": {
                                        "type": "string",
                                        "description": "The list of pending documents for the claim."
                                    }
                                },
                                "required": [
                                    "claimId",
                                    "pendingDocuments"
                                ]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Reminders sent successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "sendReminderTrackingId": {
                                            "type": "string",
                                            "description": "Unique Id to track the status of the send reminder Call"
                                        },
                                        "sendReminderStatus": {
                                            "type": "string",
                                            "description": "Status of send reminder notifications"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request. One or more required fields are missing or invalid."
                    }
                }
            }
        }
    }
}
```

For more examples of OpenAPI schemas, see [Example API Descriptions](https://learn.openapis.org/examples/) on the OpenAPI website.