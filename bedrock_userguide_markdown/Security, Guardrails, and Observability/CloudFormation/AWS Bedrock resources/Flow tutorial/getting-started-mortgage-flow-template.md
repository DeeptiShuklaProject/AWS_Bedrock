

# CloudFormation templates
<a name="getting-started-mortgage-flow-template"></a>

The `cloudformation-mortgage-flow-setup.zip` file that you download contains the following files:
+ `deploy.sh` – A shell script that deploys your resources and prepares the main CloudFormation template that you'll use.
+ `artifacts` – A folder that contains .zip files with functions for the agent and knowledge base templates:
  + Lambda functions for the agent's action groups
    + `agent_loan_calculator.zip`
    + `mls_lookup.zip`
    + `loader_deployment_package.zip`
  + Functions for setting up the knowledge base
    + `custom-resource-lambda.zip`
    + `opensearchpy-layer.zip`
    + `provider-event-handler.zip`
+ `api-schema` – A folder that contains API schemas for action groups.
+ `knowledge-base-data-source` – A folder that contains the PDF for [Fannie Mae's Selling Guide](https://selling-guide.fanniemae.com/).
+ `templates` – A folder that contains the templates for the resources in this flow, both in JSON and YAML format:
  + `main-stack-tmp` – The main template that deploys the remaining templates as nested stacks. This file is turned into `main-stack` after the deployment script is run.
  + `guardrails-template` – The template for the guardrail to be associated with the agent.
  + `prompts-template` – The template for the prompts to be used in flow.
  + `kb-role-template` – The template for the knowledge base role, to be used both by the OpenSearch template and by the knowledge base template.
  + `oss-infra-template` – The template for the Amazon OpenSearch Serverless vector store to be used for the knowledge base.
  + `kb-infra-template` – The template for the mortgage loan knowledge base to be associated with the agent.
  + `agent-template` – The template for mortgage processing agent to be used in the flow.
  + `mortgage-flow-template` – The template for the mortgage processing flow that combines all the resources.
+ `README.md` – A README file that describes the steps for using the template.

The following topics show the CloudFormation templates used for each stack. The main stack deploys the remaining stacks as [nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html).

**Topics**
+ [Main stack](#getting-started-mortgage-templates-main)
+ [Amazon Bedrock Guardrails stack](#getting-started-mortgage-guardrail-templates)
+ [Amazon Bedrock Prompt management stack](#getting-started-mortgage-prompts-templates)
+ [Amazon Bedrock Knowledge Bases stack](#getting-started-mortgage-kb-templates)

## Main stack
<a name="getting-started-mortgage-templates-main"></a>

The main stack defines the parameters that you can define when you upload the template. These values are passed on to each of the remaining nested stacks. The deployment script replaces {{MortgageFlowBucket}} for the default value of the `Q01pS3BucketName` parameter with your actual S3 bucket that contains the resources deployed by the script.

------
#### [ YAML ]

```
AWSTemplateFormatVersion: '2010-09-09'
Description: "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow"

Parameters:
  Q01pS3BucketName:
    Type: String
    Description: Provide existing S3 bucket name where data is already stored
    Default: MortgageFlowBucket
  Q02pFlowName:
    Type: String
    Description: Name for the flow
    Default: MortgageFlow
  Q03pGuardrailName:
    Type: String
    Description: Name for guardrail to attach to agent
    Default: MortgageGR
  Q04pKnowledgeBaseName:
    Type: String
    Description: Name for knowledge base to associate with agent
    Default: MortgageKB
  Q05pAgentName:
    Type: String
    Description: Name for agent to create
    Default: MortgageAgent
  Q06pKBEmbedModel:
    Type: String
    Description: Select Embedding model
    Default: amazon.titan-embed-text-v1
  Q07pKBChunkingStrategy:
    Type: String
    Description: Select Chunking strategy
    AllowedValues:
      - Default chunking
      - Fixed-size chunking
      - No chunking
    Default: Default chunking
  Q08pKBMaxTokens:
    Type: Number
    Description: Maximum number of tokens in a chunk
    Default: 300
  Q09pKBOverlapPercentage:
    Type: Number
    Description: Percent overlap in each chunk
    Default: 20
  Q10pKBVectorStore:
    Type: String
    Description: Select vector store
    AllowedValues:
    - Open-Search-Serverless
    Default: Open-Search-Serverless
  Q11pOSSCollectionName:
    Type: String
    Description: Name of the Collection
    MinLength: 1
    MaxLength: 63
    Default: mortgage-kb-collection
    AllowedPattern: ^[a-z0-9](-*[a-z0-9])*
    ConstraintDescription: Must be lowercase or numbers with a length of 1-32 characters
  Q12pOSSIndexName:
    Type: String
    Description: Index name to be created in vector store
    MinLength: 1
    MaxLength: 63
    Default: mortgage-kb-index
    AllowedPattern: ^[a-z0-9](-*[a-z0-9])*
    ConstraintDescription: Must be lowercase or numbers with a length of 1-63 characters
  # Q13pVectorFieldName:
  #   Type: String
  #   Description: Vector field name
  #   Default: bedrock-knowledge-base-default-vector
  # Q14pMetaDataFieldName:
  #   Type: String
  #   Description: Metadata field name
  #   Default: AMAZON_BEDROCK_METADATA
  # Q15pTextFieldName:
  #   Type: String
  #   Description: Text field name
  #   Default: AMAZON_BEDROCK_TEXT_CHUNK
Resources:
  KBRoleStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/kb-role-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        Q01pS3BucketName:
          Ref: Q01pS3BucketName
  OSSStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: KBRoleStack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/oss-infra-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        Q01pS3BucketName:
          Ref: Q01pS3BucketName
        Q06pKBEmbedModel:
          Ref: Q06pKBEmbedModel
        Q11pOSSCollectionName:
          Ref: Q11pOSSCollectionName
        Q12pOSSIndexName:
          Ref: Q12pOSSIndexName
        pKBRole:
          Fn::GetAtt:
          - KBRoleStack
          - Outputs.KBRole
        pKBRoleArn:
          Fn::GetAtt:
          - KBRoleStack
          - Outputs.KBRoleArn
  KBStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: OSSStack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/kb-infra-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        KnowledgeBaseName:
          Ref: Q04pKnowledgeBaseName
        Q01pS3BucketName:
          Ref: Q01pS3BucketName
        Q06pKBEmbedModel:
          Ref: Q06pKBEmbedModel
        Q07pKBChunkingStrategy:
          Ref: Q07pKBChunkingStrategy
        Q08pKBMaxTokens:
          Ref: Q08pKBMaxTokens
        Q09pKBOverlapPercentage:
          Ref: Q09pKBOverlapPercentage
        Q11pOSSCollectionName:
          Ref: Q11pOSSCollectionName
        Q12pOSSIndexName:
          Ref: Q12pOSSIndexName
        # Q13pVectorFieldName:
        #   Ref: Q13pVectorFieldName
        # Q14pMetaDataFieldName:
        #   Ref: Q14pMetaDataFieldName
        # Q15pTextFieldName:
        #   Ref: Q15pTextFieldName
        pCollectionArn:
          Fn::GetAtt:
          - OSSStack
          - Outputs.CollectionArn
        pKBRoleArn:
          Fn::GetAtt:
          - KBRoleStack
          - Outputs.KBRoleArn
        pKBRole:
          Fn::GetAtt:
          - KBRoleStack
          - Outputs.KBRole
  GRStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/guardrails-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        GuardrailName:
          Ref: Q03pGuardrailName
  AgentStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: 
      - KBStack
      - GRStack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/agent-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        Q01pS3BucketName:
          Ref: Q01pS3BucketName
        KnowledgeBaseId:
          Fn::GetAtt:
          - KBStack
          - Outputs.KBId
        GuardrailArn:
          Fn::GetAtt:
          - GRStack
          - Outputs.GuardrailArn
        GuardrailVersion:
          Fn::GetAtt:
          - GRStack
          - Outputs.GuardrailVersion
  PromptsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/prompts-template.yaml
      TimeoutInMinutes: 15
  FlowStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: 
      - AgentStack
      - PromptsStack
    Properties:
      TemplateURL: !Sub https://${Q01pS3BucketName}.s3.amazonaws.com/templates/yaml/mortgage-flow-template.yaml
      TimeoutInMinutes: 15
      Parameters:
        FlowName:
          Ref: Q02pFlowName
        Q01pS3BucketName:
          Ref: Q01pS3BucketName
        ProcessApplicationPromptArn:
          Fn::GetAtt:
          - PromptsStack
          - Outputs.ProcessApplicationPromptArn
        RejectionPromptArn:
          Fn::GetAtt:
          - PromptsStack
          - Outputs.RejectionPromptArn
        AgentId:
          Fn::GetAtt:
          - AgentStack
          - Outputs.AgentId
```

------
#### [ JSON ]

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow",
  "Parameters": {
    "Q01pS3BucketName": {
      "Type": "String",
      "Description": "Provide existing S3 bucket name where data is already stored",
      "Default": "MortgageFlowBucket"
    },
    "Q02pFlowName": {
      "Type": "String",
      "Description": "Name for the flow",
      "Default": "MortgageFlow"
    },
    "Q03pGuardrailName": {
      "Type": "String",
      "Description": "Name for guardrail to attach to agent",
      "Default": "MortgageGR"
    },
    "Q04pKnowledgeBaseName": {
      "Type": "String",
      "Description": "Name for knowledge base to associate with agent",
      "Default": "MortgageKB"
    },
    "Q05pAgentName": {
      "Type": "String",
      "Description": "Name for agent to create",
      "Default": "MortgageAgent"
    },
    "Q06pKBEmbedModel": {
      "Type": "String",
      "Description": "Select Embedding model",
      "Default": "amazon.titan-embed-text-v1"
    },
    "Q07pKBChunkingStrategy": {
      "Type": "String",
      "Description": "Select Chunking strategy",
      "AllowedValues": [
        "Default chunking",
        "Fixed-size chunking",
        "No chunking"
      ],
      "Default": "Default chunking"
    },
    "Q08pKBMaxTokens": {
      "Type": "Number",
      "Description": "Maximum number of tokens in a chunk",
      "Default": 300
    },
    "Q09pKBOverlapPercentage": {
      "Type": "Number",
      "Description": "Percent overlap in each chunk",
      "Default": 20
    },
    "Q10pKBVectorStore": {
      "Type": "String",
      "Description": "Select vector store",
      "AllowedValues": [
        "Open-Search-Serverless"
      ],
      "Default": "Open-Search-Serverless"
    },
    "Q11pOSSCollectionName": {
      "Type": "String",
      "Description": "Name of the Collection",
      "MinLength": 1,
      "MaxLength": 63,
      "Default": "mortgage-kb-collection",
      "AllowedPattern": "^[a-z0-9](-*[a-z0-9])*",
      "ConstraintDescription": "Must be lowercase or numbers with a length of 1-32 characters"
    },
    "Q12pOSSIndexName": {
      "Type": "String",
      "Description": "Index name to be created in vector store",
      "MinLength": 1,
      "MaxLength": 63,
      "Default": "mortgage-kb-index",
      "AllowedPattern": "^[a-z0-9](-*[a-z0-9])*",
      "ConstraintDescription": "Must be lowercase or numbers with a length of 1-63 characters"
    }
  },
  "Resources": {
    "KBRoleStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/kb-role-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "Q01pS3BucketName": {
            "Ref": "Q01pS3BucketName"
          }
        }
      }
    },
    "OSSStack": {
      "Type": "AWS::CloudFormation::Stack",
      "DependsOn": "KBRoleStack",
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/oss-infra-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "Q01pS3BucketName": {
            "Ref": "Q01pS3BucketName"
          },
          "Q06pKBEmbedModel": {
            "Ref": "Q06pKBEmbedModel"
          },
          "Q11pOSSCollectionName": {
            "Ref": "Q11pOSSCollectionName"
          },
          "Q12pOSSIndexName": {
            "Ref": "Q12pOSSIndexName"
          },
          "pKBRole": {
            "Fn::GetAtt": [
              "KBRoleStack",
              "Outputs.KBRole"
            ]
          },
          "pKBRoleArn": {
            "Fn::GetAtt": [
              "KBRoleStack",
              "Outputs.KBRoleArn"
            ]
          }
        }
      }
    },
    "KBStack": {
      "Type": "AWS::CloudFormation::Stack",
      "DependsOn": "OSSStack",
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/kb-infra-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "KnowledgeBaseName": {
            "Ref": "Q04pKnowledgeBaseName"
          },
          "Q01pS3BucketName": {
            "Ref": "Q01pS3BucketName"
          },
          "Q06pKBEmbedModel": {
            "Ref": "Q06pKBEmbedModel"
          },
          "Q07pKBChunkingStrategy": {
            "Ref": "Q07pKBChunkingStrategy"
          },
          "Q08pKBMaxTokens": {
            "Ref": "Q08pKBMaxTokens"
          },
          "Q09pKBOverlapPercentage": {
            "Ref": "Q09pKBOverlapPercentage"
          },
          "Q11pOSSCollectionName": {
            "Ref": "Q11pOSSCollectionName"
          },
          "Q12pOSSIndexName": {
            "Ref": "Q12pOSSIndexName"
          },
          "pCollectionArn": {
            "Fn::GetAtt": [
              "OSSStack",
              "Outputs.CollectionArn"
            ]
          },
          "pKBRoleArn": {
            "Fn::GetAtt": [
              "KBRoleStack",
              "Outputs.KBRoleArn"
            ]
          },
          "pKBRole": {
            "Fn::GetAtt": [
              "KBRoleStack",
              "Outputs.KBRole"
            ]
          }
        }
      }
    },
    "GRStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/guardrails-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "GuardrailName": {
            "Ref": "Q03pGuardrailName"
          }
        }
      }
    },
    "AgentStack": {
      "Type": "AWS::CloudFormation::Stack",
      "DependsOn": [
        "KBStack",
        "GRStack"
      ],
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/agent-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "Q01pS3BucketName": {
            "Ref": "Q01pS3BucketName"
          },
          "KnowledgeBaseId": {
            "Fn::GetAtt": [
              "KBStack",
              "Outputs.KBId"
            ]
          },
          "GuardrailArn": {
            "Fn::GetAtt": [
              "GRStack",
              "Outputs.GuardrailArn"
            ]
          },
          "GuardrailVersion": {
            "Fn::GetAtt": [
              "GRStack",
              "Outputs.GuardrailVersion"
            ]
          }
        }
      }
    },
    "PromptsStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/prompts-template.json"
        },
        "TimeoutInMinutes": 15
      }
    },
    "FlowStack": {
      "Type": "AWS::CloudFormation::Stack",
      "DependsOn": [
        "AgentStack",
        "PromptsStack"
      ],
      "Properties": {
        "TemplateURL": {
          "Fn::Sub": "https://${Q01pS3BucketName}.s3.amazonaws.com/templates/json/mortgage-flow-template.json"
        },
        "TimeoutInMinutes": 15,
        "Parameters": {
          "FlowName": {
            "Ref": "Q02pFlowName"
          },
          "Q01pS3BucketName": {
            "Ref": "Q01pS3BucketName"
          },
          "ProcessApplicationPromptArn": {
            "Fn::GetAtt": [
              "PromptsStack",
              "Outputs.ProcessApplicationPromptArn"
            ]
          },
          "RejectionPromptArn": {
            "Fn::GetAtt": [
              "PromptsStack",
              "Outputs.RejectionPromptArn"
            ]
          },
          "AgentId": {
            "Fn::GetAtt": [
              "AgentStack",
              "Outputs.AgentId"
            ]
          }
        }
      }
    }
  }
}
```

------

## Amazon Bedrock Guardrails stack
<a name="getting-started-mortgage-guardrail-templates"></a>

This stack creates the following [guardrails](guardrails.md)-related resources:
+ AgentGuardrail ([AWS::Bedrock::Guardrail](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-guardrail.html)) – A guardrail that provides content filtering, topic policy, and PII protection. This guardrail will be attached to the agent in the Agent stack.
+ AgentGuardrailVersion ([AWS::Bedrock::GuardrailVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-guardrailversion.html)) – The version of the `AgentGuardrail` resource applied to the agent.

------
#### [ YAML ]

```
AWSTemplateFormatVersion: "2010-09-09"
Description: "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow"

Parameters:
  GuardrailName:
    Type: String
    Description: Name for guardrail
    Default: MortgageGuardrail

Resources:
  AgentGuardrail:
    Type: AWS::Bedrock::Guardrail
    Properties:
      Name: !Sub AWSDocsTutorial-${GuardrailName}
      Description: Guardrail for mortgage processing with investment advice blocking, content filtering, and PII protection
      BlockedInputMessaging: "Sorry, the model cannot answer this question."
      BlockedOutputsMessaging: "Sorry, the model cannot answer this question."
      TopicPolicyConfig:
        TopicsConfig:
          - Name: InvestmentAdvice
            Definition: "Investment advice refers to inquires, guidance or recommendations regarding the management or allocation of fund or asset with the goal of generating returns or achieving specific financial objectives"
            Examples:
              - "Is investing in the stocks better than bonds?"
              - "Should I invest in gold?"
            Type: DENY
      ContentPolicyConfig:
        FiltersConfig:
          - Type: VIOLENCE
            InputStrength: HIGH
            OutputStrength: HIGH
          - Type: PROMPT_ATTACK
            InputStrength: HIGH
            OutputStrength: NONE
          - Type: MISCONDUCT
            InputStrength: HIGH
            OutputStrength: HIGH
          - Type: HATE
            InputStrength: HIGH
            OutputStrength: HIGH
          - Type: SEXUAL
            InputStrength: HIGH
            OutputStrength: HIGH
          - Type: INSULTS
            InputStrength: HIGH
            OutputStrength: HIGH
      WordPolicyConfig:
        WordsConfig:
          - Text: "crypto currency"
          - Text: "bitcoin"
        ManagedWordListsConfig:
          - Type: PROFANITY
      SensitiveInformationPolicyConfig:
        PiiEntitiesConfig:
          - Type: EMAIL
            Action: ANONYMIZE
          - Type: CREDIT_DEBIT_CARD_NUMBER
            Action: BLOCK
      ContextualGroundingPolicyConfig:
        FiltersConfig:
          - Type: GROUNDING
            Threshold: 0.85
          - Type: RELEVANCE
            Threshold: 0.5
            
  AgentGuardrailVersion:
    Type: AWS::Bedrock::GuardrailVersion
    Properties:
      GuardrailIdentifier: !Ref AgentGuardrail
      Description: Version 1 of the mortgage agent guardrail

Outputs:
  GuardrailArn:
    Value:
      Ref: AgentGuardrail
    Description: ARN of guardrail to associate with agent
  GuardrailVersion:
    Value:
      Fn::GetAtt:
      - AgentGuardrailVersion
      - Version
    Description: Version of guardrail to associate with agent
```

------
#### [ JSON ]

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow",
  "Parameters": {
    "GuardrailName": {
      "Type": "String",
      "Description": "Name for guardrail",
      "Default": "MortgageGuardrail"
    }
  },
  "Resources": {
    "AgentGuardrail": {
      "Type": "AWS::Bedrock::Guardrail",
      "Properties": {
        "Name": {
          "Fn::Sub": "AWSDocsTutorial-${GuardrailName}"
        },
        "Description": "Guardrail for mortgage processing with investment advice blocking, content filtering, and PII protection",
        "BlockedInputMessaging": "Sorry, the model cannot answer this question.",
        "BlockedOutputsMessaging": "Sorry, the model cannot answer this question.",
        "TopicPolicyConfig": {
          "TopicsConfig": [
            {
              "Name": "InvestmentAdvice",
              "Definition": "Investment advice refers to inquires, guidance or recommendations regarding the management or allocation of fund or asset with the goal of generating returns or achieving specific financial objectives",
              "Examples": [
                "Is investing in the stocks better than bonds?",
                "Should I invest in gold?"
              ],
              "Type": "DENY"
            }
          ]
        },
        "ContentPolicyConfig": {
          "FiltersConfig": [
            {
              "Type": "VIOLENCE",
              "InputStrength": "HIGH",
              "OutputStrength": "HIGH"
            },
            {
              "Type": "PROMPT_ATTACK",
              "InputStrength": "HIGH",
              "OutputStrength": "NONE"
            },
            {
              "Type": "MISCONDUCT",
              "InputStrength": "HIGH",
              "OutputStrength": "HIGH"
            },
            {
              "Type": "HATE",
              "InputStrength": "HIGH",
              "OutputStrength": "HIGH"
            },
            {
              "Type": "SEXUAL",
              "InputStrength": "HIGH",
              "OutputStrength": "HIGH"
            },
            {
              "Type": "INSULTS",
              "InputStrength": "HIGH",
              "OutputStrength": "HIGH"
            }
          ]
        },
        "WordPolicyConfig": {
          "WordsConfig": [
            {
              "Text": "crypto currency"
            },
            {
              "Text": "bitcoin"
            }
          ],
          "ManagedWordListsConfig": [
            {
              "Type": "PROFANITY"
            }
          ]
        },
        "SensitiveInformationPolicyConfig": {
          "PiiEntitiesConfig": [
            {
              "Type": "EMAIL",
              "Action": "ANONYMIZE"
            },
            {
              "Type": "CREDIT_DEBIT_CARD_NUMBER",
              "Action": "BLOCK"
            }
          ]
        },
        "ContextualGroundingPolicyConfig": {
          "FiltersConfig": [
            {
              "Type": "GROUNDING",
              "Threshold": 0.85
            },
            {
              "Type": "RELEVANCE",
              "Threshold": 0.5
            }
          ]
        }
      }
    },
    "AgentGuardrailVersion": {
      "Type": "AWS::Bedrock::GuardrailVersion",
      "Properties": {
        "GuardrailIdentifier": {
          "Ref": "AgentGuardrail"
        },
        "Description": "Version 1 of the mortgage agent guardrail"
      }
    }
  },
  "Outputs": {
    "GuardrailArn": {
      "Value": {
        "Ref": "AgentGuardrail"
      },
      "Description": "ARN of guardrail to associate with agent"
    },
    "GuardrailVersion": {
      "Value": {
        "Fn::GetAtt": [
          "AgentGuardrailVersion",
          "Version"
        ]
      },
      "Description": "Version of guardrail to associate with agent"
    }
  }
}
```

------

## Amazon Bedrock Prompt management stack
<a name="getting-started-mortgage-prompts-templates"></a>

This stack creates the following [prompt](prompt-management.md) ([AWS::IAM::Prompt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-prompt.html)) resources, which are added to the flow:
+ RejectionPrompt – A prompt that returns a generated rejection letter based on financial information.
+ ProcessApplicationPrompt – A prompt that sends a customer's financial information to an agent and prompts the agent to assess whether the customer qualifies for a loan.

------
#### [ YAML ]

```
AWSTemplateFormatVersion: "2010-09-09"
Description: "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow"

Resources:
  RejectionPrompt:
    Type: AWS::Bedrock::Prompt
    Properties:
      Name: !Sub AWSDocsTutorial-RejectionPrompt
      Description: "Use this prompt to generate a rejection letter triggered by an unsatisfactory income to debt ratio"
      DefaultVariant: variantOne
      Variants:
        - Name: variantOne
          TemplateType: TEXT
          ModelId: anthropic.claude-haiku-4-5-20251001-v1:0
          TemplateConfiguration:
            Text:
              Text: |
                Write a mortgage loan rejection letter for a candiate with income {{income}}, totalDebt {{totalDebt}}, loanAmount {{loanAmount}}. 
                The reason for rejection is their income to debt ratio. 
                Do not mention any other reason. 
                Make the letter as concise as possible. 
                Treat all numeric inputs as whole numbers.
                Let the general structure be like the below:

                Dear [Applicant's Name],
                We appreciate your interest in obtaining a mortgage loan with our institution...
                The primary reason for this decision is that ...
                While we understand that this news may be disappointing, ...
                Thank you again for your interest, and we wish you the best in your future endeavors...

                Sincerely,
                [Your Institution's Name]
              InputVariables:
                - Name: income
                - Name: totalDebt
                - Name: loanAmount
          InferenceConfiguration:
            Text:
              MaxTokens: 2000
              Temperature: 0.0
              TopP: 0.999
              StopSequences:
                - "\n\nHuman:"
          AdditionalModelRequestFields:
            top_k: 250

  ProcessApplicationPrompt:
    Type: AWS::Bedrock::Prompt
    Properties:
      Name: !Sub AWSDocsTutorial-ProcessApplicationPrompt
      Description: "Use this prompt to generate a question for an agent to process the mortgage application"
      DefaultVariant: variantOne
      Variants:
        - Name: variantOne
          TemplateType: TEXT
          ModelId: anthropic.claude-haiku-4-5-20251001-v1:0
          TemplateConfiguration:
            Text:
              Text: |
                Generate a question asking if the user will qualify for a loan for the specified criteria. 

                Include instruction to base the answer on key features of the property retrieved from MLS listing. 

                Start with "will an applicant...".

                { "income": {{income}}, "creditScore": {{creditScore}}, "totalDebt": {{totalDebt}}, "loanAmount": {{loanAmount}}, "mlsId": {{mlsId}} }

                Include a second question on loan requirements an applicant with the below attributes should consider for a Fannie Mae backed loan (other than debt to income).
              InputVariables:
                - Name: income
                - Name: creditScore
                - Name: totalDebt
                - Name: loanAmount
                - Name: mlsId
          InferenceConfiguration:
            Text:
              MaxTokens: 2000
              Temperature: 0.0
              TopP: 0.999
              StopSequences:
                - "\n\nHuman:"
          AdditionalModelRequestFields:
            top_k: 250

Outputs:
  ProcessApplicationPromptArn:
    Value:
      Ref: ProcessApplicationPrompt
    Description: ARN of the prompt to process a mortgage application
  RejectionPromptArn:
    Value:
      Ref: RejectionPrompt
    Description: ARN of the prompt to reject a mortgage application
```

------
#### [ JSON ]

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow",
  "Resources": {
    "RejectionPrompt": {
      "Type": "AWS::Bedrock::Prompt",
      "Properties": {
        "Name": {
          "Fn::Sub": "AWSDocsTutorial-RejectionPrompt"
        },
        "Description": "Use this prompt to generate a rejection letter triggered by an unsatisfactory income to debt ratio",
        "DefaultVariant": "variantOne",
        "Variants": [
          {
            "Name": "variantOne",
            "TemplateType": "TEXT",
            "ModelId": "anthropic.claude-haiku-4-5-20251001-v1:0",
            "TemplateConfiguration": {
              "Text": {
                "Text": "Write a mortgage loan rejection letter for a candiate with income {{income}}, totalDebt {{totalDebt}}, loanAmount {{loanAmount}}. \nThe reason for rejection is their income to debt ratio. \nDo not mention any other reason. \nMake the letter as concise as possible. \nTreat all numeric inputs as whole numbers.\nLet the general structure be like the below:\n\nDear [Applicant's Name],\nWe appreciate your interest in obtaining a mortgage loan with our institution...\nThe primary reason for this decision is that ...\nWhile we understand that this news may be disappointing, ...\nThank you again for your interest, and we wish you the best in your future endeavors...\n\nSincerely,\n[Your Institution's Name]\n",
                "InputVariables": [
                  {
                    "Name": "income"
                  },
                  {
                    "Name": "totalDebt"
                  },
                  {
                    "Name": "loanAmount"
                  }
                ]
              }
            },
            "InferenceConfiguration": {
              "Text": {
                "MaxTokens": 2000,
                "Temperature": 0.0,
                "TopP": 0.999,
                "StopSequences": [
                  "\n\nHuman:"
                ]
              }
            },
            "AdditionalModelRequestFields": {
              "top_k": 250
            }
          }
        ]
      }
    },
    "ProcessApplicationPrompt": {
      "Type": "AWS::Bedrock::Prompt",
      "Properties": {
        "Name": {
          "Fn::Sub": "AWSDocsTutorial-ProcessApplicationPrompt"
        },
        "Description": "Use this prompt to generate a question for an agent to process the mortgage application",
        "DefaultVariant": "variantOne",
        "Variants": [
          {
            "Name": "variantOne",
            "TemplateType": "TEXT",
            "ModelId": "anthropic.claude-haiku-4-5-20251001-v1:0",
            "TemplateConfiguration": {
              "Text": {
                "Text": "Generate a question asking if the user will qualify for a loan for the specified criteria. \n\nInclude instruction to base the answer on key features of the property retrieved from MLS listing. \n\nStart with \"will an applicant...\".\n\n{ \"income\": {{income}}, \"creditScore\": {{creditScore}}, \"totalDebt\": {{totalDebt}}, \"loanAmount\": {{loanAmount}}, \"mlsId\": {{mlsId}} }\n\nInclude a second question on loan requirements an applicant with the below attributes should consider for a Fannie Mae backed loan (other than debt to income).\n",
                "InputVariables": [
                  {
                    "Name": "income"
                  },
                  {
                    "Name": "creditScore"
                  },
                  {
                    "Name": "totalDebt"
                  },
                  {
                    "Name": "loanAmount"
                  },
                  {
                    "Name": "mlsId"
                  }
                ]
              }
            },
            "InferenceConfiguration": {
              "Text": {
                "MaxTokens": 2000,
                "Temperature": 0.0,
                "TopP": 0.999,
                "StopSequences": [
                  "\n\nHuman:"
                ]
              }
            },
            "AdditionalModelRequestFields": {
              "top_k": 250
            }
          }
        ]
      }
    }
  },
  "Outputs": {
    "ProcessApplicationPromptArn": {
      "Value": {
        "Ref": "ProcessApplicationPrompt"
      },
      "Description": "ARN of the prompt to process a mortgage application"
    },
    "RejectionPromptArn": {
      "Value": {
        "Ref": "RejectionPrompt"
      },
      "Description": "ARN of the prompt to reject a mortgage application"
    }
  }
}
```

------

## Amazon Bedrock Knowledge Bases stack
<a name="getting-started-mortgage-kb-templates"></a>

This template creates the [knowledge base](knowledge-base.md) and its data source containing the loan guidelines:
+ KnowledgeBase ([AWS::Bedrock::KnowledgeBase](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html))
+ KnowledgeBaseDataSource ([AWS::Bedrock::DataSource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html))

------
#### [ YAML ]

```
AWSTemplateFormatVersion: '2010-09-09'
Description: "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow"
Parameters:
  KnowledgeBaseName:
    Type: String
    Description: Name of knowledge base
    Default: MortgageKB
  Q01pS3BucketName:
    Type: String
    Description: Name of S3 bucket where knowledge base data is stored
  Q06pKBEmbedModel:
    Type: String
    Description: Selected Embedding model
  Q07pKBChunkingStrategy:
    Type: String
    Description: Selected Chunking strategy
  Q08pKBMaxTokens:
    Type: Number
    Description: Maximum number of tokens in a chunk
  Q09pKBOverlapPercentage:
    Type: Number
    Description: Percent overlap in each chunk
  Q11pOSSCollectionName:
    Type: String
    Description: Name of the Collection
  Q12pOSSIndexName:
    Type: String
    Description: Index name to be created in vector store
  Q13pVectorFieldName:
    Type: String
    Description: Vector field name
    Default: bedrock-knowledge-base-default-vector
  Q14pMetaDataFieldName:
    Type: String
    Description: Metadata field name
    Default: AMAZON_BEDROCK_METADATA
  Q15pTextFieldName:
    Type: String
    Description: Text field name
    Default: AMAZON_BEDROCK_TEXT_CHUNK
  pCollectionArn:
    Type: String
    Description: Name of the Collection Arn
  pKBRole:
    Type: String
    Description: KB role for e2e RAG
  pKBRoleArn:
    Type: String
    Description: KB role Arn for e2e RAG
Conditions:
  IsChunkingStrategyFixed:
    Fn::Equals:
      - Ref: Q07pKBChunkingStrategy
      - Fixed-size chunking
  IsChunkingStrategyDefault:
    Fn::Equals:
      - Ref: Q07pKBChunkingStrategy
      - Default chunking
  IsChunkingStrategyNoChunking:
    Fn::Equals:
      - Ref: Q07pKBChunkingStrategy
      - No chunking
  IsChunkingStrategyFixedOrDefault:
    Fn::Or:
      - Condition: IsChunkingStrategyFixed
      - Condition: IsChunkingStrategyDefault
Resources:
  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      Description: Test KB Deployment
      KnowledgeBaseConfiguration:
        Type: VECTOR
        VectorKnowledgeBaseConfiguration:
          EmbeddingModelArn:
            Fn::Sub: arn:aws:bedrock:${AWS::Region}::foundation-model/${Q06pKBEmbedModel}
      Name: !Sub AWSDocsTutorial-${KnowledgeBaseName}
      RoleArn:
        Ref: pKBRoleArn
      StorageConfiguration:
        OpensearchServerlessConfiguration:
          CollectionArn:
            Ref: pCollectionArn
          FieldMapping:
            MetadataField:
              Ref: Q14pMetaDataFieldName
            TextField:
              Ref: Q15pTextFieldName
            VectorField:
              Ref: Q13pVectorFieldName
          VectorIndexName:
            Ref: Q12pOSSIndexName
        Type: OPENSEARCH_SERVERLESS

  KnowledgeBaseDataSource:
    Type: AWS::Bedrock::DataSource
    DependsOn:
    - KnowledgeBase
    Properties:
      DataSourceConfiguration:
        Type: S3
        S3Configuration:
          BucketArn:
            Fn::Sub: arn:aws:s3:::${Q01pS3BucketName}
          InclusionPrefixes:
            - knowledge-base-data-source/
      Description: Knowledge base data source
      KnowledgeBaseId:
        Ref: KnowledgeBase
      Name: !Sub AWSDocsTutorial-${KnowledgeBaseName}-DS
      VectorIngestionConfiguration:
        ChunkingConfiguration:
          Fn::If:
            - IsChunkingStrategyFixed
            - ChunkingStrategy: FIXED_SIZE
              FixedSizeChunkingConfiguration:
                MaxTokens: !Ref Q08pKBMaxTokens
                OverlapPercentage: !Ref Q09pKBOverlapPercentage
            - Fn::If:
                - IsChunkingStrategyDefault
                - ChunkingStrategy: FIXED_SIZE
                  FixedSizeChunkingConfiguration:
                    MaxTokens: 300
                    OverlapPercentage: 20
                - Fn::If:
                    - IsChunkingStrategyNoChunking
                    - ChunkingStrategy: NONE
                    - !Ref AWS::NoValue
Outputs:
  KBId:
    Value:
      Ref: KnowledgeBase
    Description: KnowledgeBase ID
  DS:
    Value:
      Ref: KnowledgeBaseDataSource
    Description: KnowledgeBase Datasource
```

------
#### [ JSON ]

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "[AWSDocs] AmazonBedrockDocs: getting-started-mortgage-flow",
  "Parameters": {
    "KnowledgeBaseName": {
      "Type": "String",
      "Description": "Name of knowledge base",
      "Default": "MortgageKB"
    },
    "Q01pS3BucketName": {
      "Type": "String",
      "Description": "Name of S3 bucket where knowledge base data is stored"
    },
    "Q06pKBEmbedModel": {
      "Type": "String",
      "Description": "Selected Embedding model"
    },
    "Q07pKBChunkingStrategy": {
      "Type": "String",
      "Description": "Selected Chunking strategy"
    },
    "Q08pKBMaxTokens": {
      "Type": "Number",
      "Description": "Maximum number of tokens in a chunk"
    },
    "Q09pKBOverlapPercentage": {
      "Type": "Number",
      "Description": "Percent overlap in each chunk"
    },
    "Q11pOSSCollectionName": {
      "Type": "String",
      "Description": "Name of the Collection"
    },
    "Q12pOSSIndexName": {
      "Type": "String",
      "Description": "Index name to be created in vector store"
    },
    "Q13pVectorFieldName": {
      "Type": "String",
      "Description": "Vector field name",
      "Default": "bedrock-knowledge-base-default-vector"
    },
    "Q14pMetaDataFieldName": {
      "Type": "String",
      "Description": "Metadata field name",
      "Default": "AMAZON_BEDROCK_METADATA"
    },
    "Q15pTextFieldName": {
      "Type": "String",
      "Description": "Text field name",
      "Default": "AMAZON_BEDROCK_TEXT_CHUNK"
    },
    "pCollectionArn": {
      "Type": "String",
      "Description": "Name of the Collection Arn"
    },
    "pKBRole": {
      "Type": "String",
      "Description": "KB role for e2e RAG"
    },
    "pKBRoleArn": {
      "Type": "String",
      "Description": "KB role Arn for e2e RAG"
    }
  },
  "Conditions": {
    "IsChunkingStrategyFixed": {
      "Fn::Equals": [
        {
          "Ref": "Q07pKBChunkingStrategy"
        },
        "Fixed-size chunking"
      ]
    },
    "IsChunkingStrategyDefault": {
      "Fn::Equals": [
        {
          "Ref": "Q07pKBChunkingStrategy"
        },
        "Default chunking"
      ]
    },
    "IsChunkingStrategyNoChunking": {
      "Fn::Equals": [
        {
          "Ref": "Q07pKBChunkingStrategy"
        },
        "No chunking"
      ]
    },
    "IsChunkingStrategyFixedOrDefault": {
      "Fn::Or": [
        {
          "Condition": "IsChunkingStrategyFixed"
        },
        {
          "Condition": "IsChunkingStrategyDefault"
        }
      ]
    }
  },
  "Resources": {
    "KnowledgeBase": {
      "Type": "AWS::Bedrock::KnowledgeBase",
      "Properties": {
        "Description": "Test KB Deployment",
        "KnowledgeBaseConfiguration": {
          "Type": "VECTOR",
          "VectorKnowledgeBaseConfiguration": {
            "EmbeddingModelArn": {
              "Fn::Sub": "arn:aws:bedrock:${AWS::Region}::foundation-model/${Q06pKBEmbedModel}"
            }
          }
        },
        "Name": {
          "Fn::Sub": "AWSDocsTutorial-${KnowledgeBaseName}"
        },
        "RoleArn": {
          "Ref": "pKBRoleArn"
        },
        "StorageConfiguration": {
          "OpensearchServerlessConfiguration": {
            "CollectionArn": {
              "Ref": "pCollectionArn"
            },
            "FieldMapping": {
              "MetadataField": {
                "Ref": "Q14pMetaDataFieldName"
              },
              "TextField": {
                "Ref": "Q15pTextFieldName"
              },
              "VectorField": {
                "Ref": "Q13pVectorFieldName"
              }
            },
            "VectorIndexName": {
              "Ref": "Q12pOSSIndexName"
            }
          },
          "Type": "OPENSEARCH_SERVERLESS"
        }
      }
    },
    "KnowledgeBaseDataSource": {
      "Type": "AWS::Bedrock::DataSource",
      "DependsOn": [
        "KnowledgeBase"
      ],
      "Properties": {
        "DataSourceConfiguration": {
          "Type": "S3",
          "S3Configuration": {
            "BucketArn": {
              "Fn::Sub": "arn:aws:s3:::${Q01pS3BucketName}"
            },
            "InclusionPrefixes": [
              "knowledge-base-data-source/"
            ]
          }
        },
        "Description": "Knowledge base data source",
        "KnowledgeBaseId": {
          "Ref": "KnowledgeBase"
        },
        "Name": {
          "Fn::Sub": "AWSDocsTutorial-${KnowledgeBaseName}-DS"
        },
        "VectorIngestionConfiguration": {
          "ChunkingConfiguration": {
            "Fn::If": [
              "IsChunkingStrategyFixed",
              {
                "ChunkingStrategy": "FIXED_SIZE",
                "FixedSizeChunkingConfiguration": {
                  "MaxTokens": {
                    "Ref": "Q08pKBMaxTokens"
                  },
                  "OverlapPercentage": {
                    "Ref": "Q09pKBOverlapPercentage"
                  }
                }
              },
              {
                "Fn::If": [
                  "IsChunkingStrategyDefault",
                  {
                    "ChunkingStrategy": "FIXED_SIZE",
                    "FixedSizeChunkingConfiguration": {
                      "MaxTokens": 300,
                      "OverlapPercentage": 20
                    }
                  },
                  {
                    "Fn::If": [
                      "IsChunkingStrategyNoChunking",
                      {
                        "ChunkingStrategy": "NONE"
                      },
                      {
                        "Ref": "AWS::NoValue"
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
      }
    }
  },
  "Outputs": {
    "KBId": {
      "Value": {
        "Ref": "KnowledgeBase"
      },
      "Description": "KnowledgeBase ID"
    },
    "DS": {
      "Value": {
        "Ref": "KnowledgeBaseDataSource"
      },
      "Description": "KnowledgeBase Datasource"
    }
  }
}
```

------